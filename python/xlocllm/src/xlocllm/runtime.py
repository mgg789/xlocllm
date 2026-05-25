from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Iterable, Literal

from .bridge import Bridge, bridges
from .catalog import ModelInfo, all_models, model as catalog_model, resolve_model
from .registry import all_runtime_records, bridge_record, process_exists, remove_runtime, upsert_runtime
from .types import UnitRequest
from .window import WindowHandle, window


@dataclass
class Unit:
    type: str
    model: str
    model_info: ModelInfo | None = None
    reasoning: bool | None = None
    options: dict[str, Any] = field(default_factory=dict)
    _runtime: Runtime | None = field(default=None, init=False, repr=False, compare=False)
    _single_runtime: Runtime | None = field(default=None, init=False, repr=False, compare=False)

    @property
    def id(self) -> str:
        return f"{self.type}:{self.model}"

    @property
    def label(self) -> str:
        if self.model_info is not None:
            return self.model_info.label
        return self.model

    @property
    def supports_reasoning(self) -> bool:
        return bool(self.model_info and self.model_info.supports_reasoning)

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"type": self.type, "model": self.model}
        if self.reasoning is not None:
            payload["reasoning"] = self.reasoning
        if self.options:
            payload["options"] = dict(self.options)
        return payload

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = self.to_payload()
        payload.update(
            {
                "id": self.id,
                "label": self.label,
                "supports_reasoning": self.supports_reasoning,
            }
        )
        if self.model_info is not None:
            payload["model_info"] = self.model_info.to_dict()
        return payload

    def status(self) -> dict[str, Any]:
        if self._runtime is not None:
            return self._runtime.unit_status(self.id)
        return {"ok": True, "attached": False, "status": "selected", "unit": self.to_dict()}

    def remove(self) -> dict[str, Any]:
        if self._runtime is None:
            return {"ok": True, "removed": False, "unit": self.to_dict()}
        return self._runtime.remove_unit(self.id, delete_cache=False)

    def delete_cache(self, *, bridge: Bridge | None = None) -> dict[str, Any]:
        active_bridge = bridge or (self._runtime.bridge if self._runtime is not None else None) or Bridge()
        return active_bridge.delete_model(self.type, self.model)

    def set_reasoning(self, enabled: bool | None) -> dict[str, Any]:
        if enabled is not None and not self.supports_reasoning:
            raise ValueError(f"{self.label} does not advertise reasoning control")
        self.reasoning = enabled
        if self._runtime is None:
            return {"ok": True, "updated": self.to_dict(), "runtime_updated": False}
        return self._runtime.configure_unit(self.id, reasoning=enabled)

    def delete(self, *, delete_cache: bool = True, bridge: Bridge | None = None) -> dict[str, Any]:
        if self._runtime is not None:
            return self._runtime.remove_unit(self.id, delete_cache=delete_cache)
        if not delete_cache:
            return {"ok": True, "deleted": False, "unit": self.to_dict()}
        return (bridge or Bridge()).delete_model(self.type, self.model)

    def as_runtime(self, port: int | str = 1146) -> Runtime:
        resolved_port = int(port)
        if self._single_runtime is None or self._single_runtime.port != resolved_port:
            self._single_runtime = Runtime([self], port=resolved_port)
        return self._single_runtime

    def install(self, port: int | str = 1146) -> dict[str, Any]:
        return self.as_runtime(port).install()

    def run(self, port: int | str = 1146) -> dict[str, Any]:
        return self.as_runtime(port).run()

    def stop(self) -> dict[str, Any]:
        return self.as_runtime().stop()

    def hibernate(self) -> dict[str, Any]:
        return self.as_runtime().hibernate()

    def heatup(self) -> dict[str, Any]:
        return self.as_runtime().heatup()

    def invoke(self, endpoint: str, payload: dict[str, Any], timeout: float | None = None) -> dict[str, Any]:
        return self.as_runtime().invoke(endpoint, payload, timeout=timeout)


UnitRuntime = Unit
_REASONING_UNSET: Any = object()


class Runtime:
    def __init__(
        self,
        units: Iterable[Unit | UnitRequest],
        *,
        port: int | str = 1146,
        bridge: Bridge | None = None,
        runtime_id: str | None = None,
    ) -> None:
        self.id = runtime_id or f"rt_{uuid.uuid4().hex}"
        self.port = int(port)
        self.bridge = bridge
        self.window_handle: WindowHandle | None = None
        self.installed = False
        self.running = False
        self._units: list[Unit] = []
        for item in units:
            self.add_unit(item, activate=False)
        if not self._units:
            raise ValueError("runtime requires at least one unit")

    @property
    def base_url(self) -> str:
        return self._bridge_or_default().base_url

    @property
    def url(self) -> str:
        return self._bridge_or_default().url

    @property
    def unit_requests(self) -> list[UnitRequest]:
        return [
            UnitRequest(type=item.type, model=item.model, reasoning=item.reasoning, options=dict(item.options))
            for item in self._units
        ]

    def __iter__(self) -> Any:
        return iter(self._units)

    def __len__(self) -> int:
        return len(self._units)

    def __enter__(self) -> Runtime:
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> Literal[False]:
        if self.bridge is not None:
            try:
                self.close()
            except Exception:  # noqa: BLE001
                try:
                    self.stop()
                except Exception:  # noqa: BLE001
                    pass
        return False

    def add_unit(self, item: Unit | UnitRequest, *, activate: bool = True) -> Unit:
        unit = self._coerce_unit(item)
        existing = self._find_unit(unit.id)
        if existing is not None:
            existing._runtime = self
            return existing
        unit._runtime = self
        self._units.append(unit)
        if activate and self.bridge is not None and self.running:
            self.bridge._post("/xlocllm/v1/runtime/run", {"units": [unit.to_payload()]}, timeout=1800)
        self._save_runtime_state("running" if self.running else "configured")
        return unit

    def remove_unit(self, unit_id: str, *, delete_cache: bool = False) -> dict[str, Any]:
        unit = self._find_unit(unit_id)
        if unit is None:
            raise ValueError(f"Unit not found in runtime: {unit_id!r}")
        self._units.remove(unit)
        unit._runtime = None
        result: dict[str, Any] = {"ok": True, "removed": unit.to_dict(), "units": self.units(as_dict=True)}
        if self.bridge is not None and delete_cache:
            result["delete"] = self.bridge.delete_model(unit.type, unit.model)
        elif self.bridge is not None and self.running:
            result["deactivate"] = self.bridge.set_active(unit.type, active=False, model=unit.model)
        self._save_runtime_state("running" if self.running else "configured")
        return result

    def unit_status(self, unit_id: str) -> dict[str, Any]:
        unit = self._find_unit(unit_id)
        if unit is None:
            raise ValueError(f"Unit not found in runtime: {unit_id!r}")
        state = self.status()
        runtime_state = state.get("runtime")
        if isinstance(runtime_state, dict):
            for model_state in runtime_state.get("models", []):
                if not isinstance(model_state, dict):
                    continue
                if model_state.get("modelId") == unit.model or model_state.get("runtimeId") == unit.model:
                    return {"ok": True, "attached": True, "unit": unit.to_dict(), "state": model_state}
            for unit_state in runtime_state.get("units", []):
                if isinstance(unit_state, dict) and unit_state.get("type") == unit.type:
                    return {"ok": True, "attached": True, "unit": unit.to_dict(), "state": unit_state}
        return {"ok": True, "attached": True, "unit": unit.to_dict(), "state": {"status": "selected"}}

    def configure_unit(
        self,
        unit_id: str,
        *,
        reasoning: Any = _REASONING_UNSET,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        unit = self._find_unit(unit_id)
        if unit is None:
            raise ValueError(f"Unit not found in runtime: {unit_id!r}")
        if reasoning is not _REASONING_UNSET:
            if reasoning is not None and not isinstance(reasoning, bool):
                raise TypeError("reasoning must be True, False, or None")
            if reasoning is not None and not unit.supports_reasoning:
                raise ValueError(f"{unit.label} does not advertise reasoning control")
            unit.reasoning = reasoning
        if options is not None:
            unit.options.update(options)
        result: dict[str, Any] = {"ok": True, "updated": unit.to_dict(), "runtime_updated": False}
        if self.bridge is not None and self.running:
            result["runtime"] = self.bridge._post(
                "/xlocllm/v1/runtime/configure_unit",
                {"unit": unit.to_payload(), "unit_id": unit.id},
                timeout=300,
            )
            result["runtime_updated"] = True
        self._save_runtime_state("running" if self.running else "configured")
        return result

    def set_reasoning(self, unit_id: str, enabled: bool | None) -> dict[str, Any]:
        return self.configure_unit(unit_id, reasoning=enabled)

    def units(self, *, as_dict: bool = False, state: bool = False) -> list[Any]:
        if state:
            runtime_state = self.status().get("runtime")
            if isinstance(runtime_state, dict) and isinstance(runtime_state.get("units"), list):
                return list(runtime_state["units"])
        if as_dict:
            return [unit.to_dict() for unit in self._units]
        return list(self._units)

    def models(self) -> list[dict[str, Any]]:
        runtime_state = self.status().get("runtime")
        if isinstance(runtime_state, dict) and isinstance(runtime_state.get("models"), list):
            return list(runtime_state["models"])
        return [unit.to_dict() for unit in self._units]

    def install(self, port: int | str | None = None) -> dict[str, Any]:
        bridge = self._ensure_bridge(int(port) if port is not None else self.port, daemon=True)
        self.window_handle = window(
            port=bridge.port,
            token=bridge.token,
            close_on_exit=False,
            mode="mini",
            width=420,
            height=340,
        )
        try:
            bridge.wait_ready(timeout=30, require_browser=True)
        except TimeoutError as error:
            raise TimeoutError(
                "xlocllm bridge is running, but the browser runtime did not connect. "
                f"Open or reload this URL: {self.window_handle.url}"
            ) from error
        result = bridge._post(
            "/xlocllm/v1/runtime/install",
            {"units": [unit.to_payload() for unit in self._units]},
            timeout=3600,
        )
        self.installed = True
        self._save_runtime_state("installed")
        return result

    def run(self, port: int | str | None = None) -> dict[str, Any]:
        bridge = self._ensure_bridge(int(port) if port is not None else self.port, daemon=True)
        if not self.installed:
            self.install(bridge.port)
        result = bridge._post(
            "/xlocllm/v1/runtime/run",
            {"units": [unit.to_payload() for unit in self._units]},
            timeout=1800,
        )
        self.running = True
        self._save_runtime_state("running")
        return result

    def stop(self) -> dict[str, Any]:
        bridge = self._require_bridge()
        result = bridge._post("/xlocllm/v1/runtime/stop", {}, timeout=300)
        self.running = False
        self._save_runtime_state("stopped")
        if self.window_handle:
            self.window_handle.close()
            self.window_handle = None
        return result

    def hibernate(self) -> dict[str, Any]:
        result = self._require_bridge()._post("/xlocllm/v1/runtime/hibernate", {}, timeout=300)
        self.running = False
        self._save_runtime_state("hibernated")
        return result

    def heatup(self) -> dict[str, Any]:
        result = self._require_bridge()._post("/xlocllm/v1/runtime/heatup", {}, timeout=1800)
        self.running = True
        self._save_runtime_state("running")
        return result

    def status(self) -> dict[str, Any]:
        bridge = self.bridge
        if bridge is None:
            return self._offline_status()
        try:
            bridge_status = bridge.status()
        except Exception as error:  # noqa: BLE001
            status = self._offline_status()
            status["error"] = str(error)
            return status
        return {
            "ok": True,
            "id": self.id,
            "port": bridge.port,
            "url": bridge.url,
            "bridge": {
                "port": bridge.port,
                "base_url": bridge.base_url,
                "url": bridge.url,
                "processes": bridge.processes(),
            },
            "units": self.units(as_dict=True),
            **bridge_status,
        }

    def health(self) -> dict[str, Any]:
        return self._require_bridge().health()

    def logs(self, limit: int = 200) -> list[dict[str, Any]]:
        return self._require_bridge().logs(limit)

    def invoke(self, endpoint: str, payload: dict[str, Any], timeout: float | None = None) -> dict[str, Any]:
        return self._require_bridge().invoke(endpoint, payload, timeout=timeout)

    def client(self, api_key: str = "xlocllm", **kwargs: Any) -> Any:
        try:
            from openai import OpenAI
        except ImportError as error:
            raise ImportError("runtime.client() requires the optional 'openai' package") from error
        return OpenAI(base_url=self.url, api_key=api_key, **kwargs)

    def chat(
        self,
        prompt: str | None = None,
        *,
        messages: list[dict[str, Any]] | None = None,
        model: str | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = dict(params)
        payload["model"] = model or self._default_model("LLM")
        payload["messages"] = messages or [{"role": "user", "content": prompt or ""}]
        return self.invoke("chat.completions", payload)

    def embed(self, input: str | list[str], *, model: str | None = None) -> list[Any]:  # noqa: A002
        payload = {"model": model or self._default_model("embedding"), "input": input}
        result = self.invoke("embeddings", payload)
        embeddings = result.get("embeddings")
        return list(embeddings) if isinstance(embeddings, list) else []

    def open(self) -> WindowHandle:
        bridge = self._require_bridge()
        self.window_handle = window(port=bridge.port, token=bridge.token, close_on_exit=False, mode="mini")
        return self.window_handle

    def close(self) -> dict[str, Any]:
        result = self._require_bridge().close()
        remove_runtime(self.id)
        self.running = False
        if self.window_handle:
            self.window_handle.close()
            self.window_handle = None
        return result

    def wait_ready(self, timeout: float | None = None, require_browser: bool = False) -> Runtime:
        self._require_bridge().wait_ready(timeout=timeout, require_browser=require_browser)
        return self

    def _ensure_bridge(self, port: int, daemon: bool) -> Bridge:
        self.port = port
        if self.bridge is None or self.bridge.port != port:
            self.bridge = Bridge(port=port)
        self.bridge.activate(daemon=daemon)
        self._save_runtime_state("configured")
        return self.bridge

    def _require_bridge(self) -> Bridge:
        if self.bridge is None:
            self.bridge = Bridge(port=self.port)
        return self.bridge

    def _bridge_or_default(self) -> Bridge:
        return self.bridge or Bridge(port=self.port)

    def _coerce_unit(self, item: Unit | UnitRequest) -> Unit:
        if isinstance(item, Unit):
            return item
        if isinstance(item, UnitRequest):
            resolved = resolve_model(item.type, item.model)
            return Unit(
                type=str(resolved["unit"]),
                model=str(resolved["modelId"]),
                model_info=ModelInfo(resolved),
                reasoning=item.reasoning,
                options=dict(item.options or {}),
            )
        raise TypeError(f"Unsupported runtime item: {type(item)!r}")

    def _find_unit(self, unit_id: str) -> Unit | None:
        for unit in self._units:
            if unit.id == unit_id or unit.model == unit_id or unit.type == unit_id:
                return unit
        return None

    def _default_model(self, unit_type: str) -> str:
        for unit in self._units:
            if unit.type == unit_type:
                return unit.model
        raise ValueError(f"Runtime has no {unit_type!r} unit")

    def _offline_status(self) -> dict[str, Any]:
        return {
            "ok": False,
            "id": self.id,
            "port": self.port,
            "url": self.url,
            "running": self.running,
            "installed": self.installed,
            "units": self.units(as_dict=True),
            "runtime": {
                "connected": False,
                "running": self.running,
                "installing": False,
                "models": [unit.to_dict() for unit in self._units],
                "units": [
                    {
                        "type": unit.type,
                        "selectedModelId": unit.model,
                        "active": True,
                        "status": "selected",
                    }
                    for unit in self._units
                ],
            },
        }

    def _save_runtime_state(self, state: str) -> None:
        if self.bridge is None:
            return
        upsert_runtime(
            self.id,
            port=self.bridge.port,
            url=self.url,
            state=state,
            running=self.running,
            installed=self.installed,
            units=[unit.to_payload() for unit in self._units],
        )


def unit(
    type: str,  # noqa: A002
    model: str,
    *,
    reasoning: bool | None = None,
    options: dict[str, Any] | None = None,
) -> Unit:
    resolved = resolve_model(type, model)
    unit_item = Unit(
        type=str(resolved["unit"]),
        model=str(resolved["modelId"]),
        model_info=ModelInfo(resolved),
        reasoning=reasoning,
        options=dict(options or {}),
    )
    if reasoning is not None and not unit_item.supports_reasoning:
        raise ValueError(f"{unit_item.label} does not advertise reasoning control")
    return unit_item


def runtime(
    units: Iterable[Unit | UnitRequest],
    *,
    port: int | str = 1146,
    bridge: Bridge | None = None,
    runtime_id: str | None = None,
) -> Runtime:
    return Runtime(units, port=port, bridge=bridge, runtime_id=runtime_id)


def runtimes(active_only: bool = True) -> list[Runtime]:
    result: list[Runtime] = []
    for record in all_runtime_records():
        runtime_id = str(record.get("id") or "")
        if not runtime_id:
            continue
        port = _int_or_default(record.get("port"), 1146)
        bridge = Bridge(port=port)
        if active_only:
            bridge_registry_record = bridge_record(port)
            pid = _int_or_none(bridge_registry_record.get("pid") if bridge_registry_record else None)
            if not process_exists(pid):
                continue
        unit_items = []
        for item in record.get("units", []):
            if isinstance(item, dict) and isinstance(item.get("type"), str) and isinstance(item.get("model"), str):
                options = item.get("options")
                unit_items.append(
                    UnitRequest(
                        type=item["type"],
                        model=item["model"],
                        reasoning=item.get("reasoning") if isinstance(item.get("reasoning"), bool) else None,
                        options=options if isinstance(options, dict) else None,
                    )
                )
        if not unit_items:
            continue
        result.append(Runtime(unit_items, port=port, bridge=bridge, runtime_id=runtime_id))
    return result


def status() -> dict[str, Any]:
    bridge_items = bridges(active_only=False)
    bridge_statuses = []
    for bridge in bridge_items:
        item: dict[str, Any] = {
            "port": bridge.port,
            "base_url": bridge.base_url,
            "url": bridge.url,
            "processes": bridge.processes(),
        }
        try:
            item["status"] = bridge.status()
        except Exception as error:  # noqa: BLE001
            item["error"] = str(error)
        bridge_statuses.append(item)

    runtime_statuses = [runtime.status() for runtime in runtimes(active_only=False)]
    installed_models = []
    running_models = []
    resource_snapshots = []
    for runtime_status in runtime_statuses:
        runtime_state = runtime_status.get("runtime")
        if not isinstance(runtime_state, dict):
            continue
        models = runtime_state.get("models", [])
        if isinstance(models, list):
            installed_models.extend([item for item in models if isinstance(item, dict) and item.get("installed")])
            running_models.extend([item for item in models if isinstance(item, dict) and item.get("status") == "running"])
        metrics = runtime_state.get("metrics")
        if isinstance(metrics, dict):
            resource_snapshots.append(metrics)

    return {
        "ok": True,
        "bridges": bridge_statuses,
        "runtimes": runtime_statuses,
        "models": {
            "catalog_count": len(all_models()),
            "installed": installed_models,
            "running": running_models,
        },
        "resources": {"runtime_metrics": resource_snapshots},
    }


def model(name: str, unit: str | None = None) -> ModelInfo:
    return catalog_model(name, unit=unit)


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _int_or_default(value: Any, default: int) -> int:
    result = _int_or_none(value)
    return default if result is None else result
