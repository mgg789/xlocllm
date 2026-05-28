from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from collections.abc import Mapping, Sequence
from typing import Any, Iterable, Literal
from urllib.parse import urlencode

from .bridge import Bridge, bridges
from .catalog import ModelInfo, all_models, model as catalog_model, resolve_model
from ._mode import RuntimeMode, current_mode
from .native_bridge import NativeBridge
from .registry import all_runtime_records, bridge_record, process_exists, remove_runtime, upsert_runtime
from .types import UnitRequest
from .window import WindowHandle, discover_web_url, window


SERVICE_UNIT_TYPES = {"vectorstorage", "RAG"}
_RAG_UNSET: Any = object()
BridgeLike = Bridge | NativeBridge


@dataclass
class Unit:
    type: str
    model: str
    model_info: ModelInfo | None = None
    mode: RuntimeMode | None = None
    reasoning: bool | None = None
    options: dict[str, Any] = field(default_factory=dict)
    rag: Unit | None = field(default=None, repr=False, compare=False)
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
        if self.rag is not None:
            payload["rag"] = self.rag.to_payload()
        return payload

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = self.to_payload()
        payload.update(
            {
                "id": self.id,
                "label": self.label,
                "supports_reasoning": self.supports_reasoning,
                "mode": self.mode,
            }
        )
        if self.model_info is not None:
            payload["model_info"] = self.model_info.to_dict()
        if self.rag is not None:
            payload["rag_unit"] = self.rag.to_dict()
        return payload

    def status(self) -> dict[str, Any]:
        if self._runtime is not None:
            return self._runtime.unit_status(self.id)
        return {"ok": True, "attached": False, "status": "selected", "unit": self.to_dict()}

    def remove(self) -> dict[str, Any]:
        if self._runtime is None:
            return {"ok": True, "removed": False, "unit": self.to_dict()}
        return self._runtime.remove_unit(self.id, delete_cache=False)

    def delete_cache(self, *, bridge: BridgeLike | None = None) -> dict[str, Any]:
        if _is_service_unit_type(self.type):
            raise ValueError(f"{self.type} units do not have model cache")
        active_bridge = (
            bridge
            or (self._runtime.bridge if self._runtime is not None else None)
            or _default_bridge_for_mode(self.mode)
        )
        return active_bridge.delete_model(self.type, self.model)

    def set_reasoning(self, enabled: bool | None) -> dict[str, Any]:
        if enabled is not None and not self.supports_reasoning:
            raise ValueError(f"{self.label} does not advertise reasoning control")
        self.reasoning = enabled
        if self._runtime is None:
            return {"ok": True, "updated": self.to_dict(), "runtime_updated": False}
        return self._runtime.configure_unit(self.id, reasoning=enabled)

    def add(
        self,
        documents: str | Sequence[str | Mapping[str, Any]] | None = None,
        *,
        ids: Sequence[str] | None = None,
        metadatas: Sequence[Mapping[str, Any] | None] | None = None,
        embeddings: Sequence[Sequence[float]] | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        if self.type == "RAG":
            return self._invoke_bound(
                "rag.add",
                {"documents": _documents_payload(documents), "ids": ids, "metadatas": metadatas, **params},
            )
        if self.type == "vectorstorage":
            return self._invoke_bound(
                "vector.add",
                {
                    "documents": _documents_payload(documents),
                    "ids": ids,
                    "metadatas": metadatas,
                    "embeddings": embeddings,
                    **params,
                },
            )
        raise ValueError(f"{self.type} units do not support add()")

    def search(
        self,
        query: str | None = None,
        *,
        embedding: Sequence[float] | None = None,
        top_k: int | None = None,
        filter: Mapping[str, Any] | None = None,  # noqa: A002
        **params: Any,
    ) -> dict[str, Any]:
        endpoint = "rag.search" if self.type == "RAG" else "vector.search" if self.type == "vectorstorage" else None
        if endpoint is None:
            raise ValueError(f"{self.type} units do not support search()")
        payload: dict[str, Any] = {"query": query, "embedding": embedding, "top_k": top_k, "filter": filter, **params}
        return self._invoke_bound(endpoint, payload)

    def clear(self, **params: Any) -> dict[str, Any]:
        endpoint = "rag.clear" if self.type == "RAG" else "vector.clear" if self.type == "vectorstorage" else None
        if endpoint is None:
            raise ValueError(f"{self.type} units do not support clear()")
        return self._invoke_bound(endpoint, params)

    def stats(self) -> dict[str, Any]:
        endpoint = "rag.stats" if self.type == "RAG" else "vector.stats" if self.type == "vectorstorage" else None
        if endpoint is None:
            raise ValueError(f"{self.type} units do not support stats()")
        return self._invoke_bound(endpoint, {})

    def reindex(self, **params: Any) -> dict[str, Any]:
        if self.type != "RAG":
            raise ValueError(f"{self.type} units do not support reindex()")
        return self._invoke_bound("rag.reindex", params)

    def delete(
        self,
        ids: str | Sequence[str] | None = None,
        *,
        filter: Mapping[str, Any] | None = None,  # noqa: A002
        delete_cache: bool = True,
        bridge: BridgeLike | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        if self.type == "RAG":
            return self._invoke_bound("rag.delete", {"ids": _ids_payload(ids), "filter": filter, **params})
        if self.type == "vectorstorage":
            return self._invoke_bound("vector.delete", {"ids": _ids_payload(ids), "filter": filter, **params})
        if self._runtime is not None:
            return self._runtime.remove_unit(self.id, delete_cache=delete_cache)
        if not delete_cache:
            return {"ok": True, "deleted": False, "unit": self.to_dict()}
        return (bridge or _default_bridge_for_mode(self.mode)).delete_model(self.type, self.model)

    def as_runtime(self, port: int | str = 1146) -> Runtime:
        resolved_port = int(port)
        if self._single_runtime is None or self._single_runtime.port != resolved_port or self._single_runtime.mode != current_mode(self.mode):
            self._single_runtime = Runtime([self], port=resolved_port, mode=self.mode)
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

    def _invoke_bound(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        if self._runtime is None:
            raise RuntimeError(f"{self.type}:{self.model} is not attached to a running Runtime")
        request_payload = dict(payload)
        request_payload["unit"] = self.to_payload()
        return self._runtime.invoke(endpoint, request_payload)


UnitRuntime = Unit
_REASONING_UNSET: Any = object()


class Runtime:
    def __init__(
        self,
        units: Iterable[Unit | UnitRequest],
        *,
        port: int | str = 1146,
        bridge: BridgeLike | None = None,
        runtime_id: str | None = None,
        mode: str | None = None,
    ) -> None:
        self.id = runtime_id or f"rt_{uuid.uuid4().hex}"
        self.port = int(port)
        self.mode = current_mode(mode)
        self.bridge = bridge
        self.window_handle: WindowHandle | None = None
        self.chat_window_handle: WindowHandle | None = None
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
    def unit_requests(self) -> list[dict[str, Any]]:
        return [unit.to_payload() for unit in self._units]

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
            self._attach_unit(existing)
            return existing
        self._attach_unit(unit)
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
        if self.bridge is not None and delete_cache and not _is_service_unit_type(unit.type):
            result["delete"] = self.bridge.delete_model(unit.type, unit.model)
        elif self.bridge is not None and self.running and not _is_service_unit_type(unit.type):
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
            for service_state in runtime_state.get("services", []):
                if not isinstance(service_state, dict):
                    continue
                if service_state.get("runtimeId") == unit.id or service_state.get("runtimeId") == f"{unit.type}:{unit.model}":
                    return {"ok": True, "attached": True, "unit": unit.to_dict(), "state": service_state}
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
        rag_update = options.get("rag") if options is not None else _RAG_UNSET
        if isinstance(rag_update, Unit):
            unit.rag = rag_update
            self._attach_unit(rag_update)
        elif isinstance(rag_update, dict):
            restored_rag = _unit_from_payload(rag_update, mode=self.mode)
            if restored_rag is not None:
                unit.rag = restored_rag
                self._attach_unit(restored_rag)
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
        self._ensure_runtime_window(bridge)
        if self.mode == "web":
            self._wait_for_browser(bridge)
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
        self._ensure_runtime_window(bridge)
        if self.mode == "web":
            self._wait_for_browser(bridge)
        result = bridge._post(
            "/xlocllm/v1/runtime/run",
            {"units": [unit.to_payload() for unit in self._units]},
            timeout=1800,
        )
        self.installed = True
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
        if self.chat_window_handle:
            self.chat_window_handle.close()
            self.chat_window_handle = None
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
            "mode": self.mode,
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
        use_rag: bool | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = dict(params)
        payload["model"] = model or self._default_model("LLM")
        payload["messages"] = messages or [{"role": "user", "content": prompt or ""}]
        if use_rag is not None:
            payload["use_rag"] = use_rag
        return self.invoke("chat.completions", payload)

    def embed(self, input: str | list[str], *, model: str | None = None) -> list[Any]:  # noqa: A002
        payload = {"model": model or self._default_model("embedding"), "input": input}
        result = self.invoke("embeddings", payload)
        embeddings = result.get("embeddings")
        return list(embeddings) if isinstance(embeddings, list) else []

    def open(self) -> WindowHandle:
        bridge = self._require_bridge()
        web_url = f"http://127.0.0.1:{bridge.port}/native-dashboard" if self.mode == "native" else None
        self.window_handle = window(port=bridge.port, token=bridge.token, close_on_exit=False, mode="mini", web_url=web_url)
        return self.window_handle

    def chatui(
        self,
        *,
        model: str | None = None,
        session: str = "default",
        use_rag: bool = True,
        open_browser: bool = True,
        block: bool = True,
        width: int = 760,
        height: int = 860,
    ) -> WindowHandle:
        if not any(unit.type == "LLM" for unit in self._units):
            raise ValueError("runtime.chatui() requires at least one LLM unit")
        if not self.running:
            self.run()
        bridge = self._require_bridge()
        query = {
            "bridgePort": str(bridge.port),
            "pairingToken": bridge.token,
            "mode": "chat",
            "session": session,
            "useRag": "1" if use_rag else "0",
        }
        if model:
            query["model"] = model
        base_url = f"http://127.0.0.1:{bridge.port}/native-chat" if self.mode == "native" else discover_web_url(bridge.port)
        separator = "&" if "?" in base_url else "?"
        url = f"{base_url}{separator}{urlencode(query)}"
        if not open_browser:
            return WindowHandle(port=bridge.port, url=url, pid=None, owned=False)
        ui_query = {"session": session, "useRag": "1" if use_rag else "0"}
        if model:
            ui_query["model"] = model
        ui_separator = "&" if "?" in base_url else "?"
        ui_base_url = f"{base_url}{ui_separator}{urlencode(ui_query)}"
        self.chat_window_handle = window(
            port=bridge.port,
            token=bridge.token,
            close_on_exit=False,
            mode="chat",
            width=width,
            height=height,
            profile=f"chat-{session}",
            web_url=ui_base_url,
        )
        if block:
            self.chat_window_handle.wait()
        return self.chat_window_handle

    def close(self) -> dict[str, Any]:
        result = self._require_bridge().close()
        remove_runtime(self.id)
        self.running = False
        if self.window_handle:
            self.window_handle.close()
            self.window_handle = None
        if self.chat_window_handle:
            self.chat_window_handle.close()
            self.chat_window_handle = None
        return result

    def wait_ready(self, timeout: float | None = None, require_browser: bool = False) -> Runtime:
        self._require_bridge().wait_ready(timeout=timeout, require_browser=require_browser)
        return self

    def _ensure_bridge(self, port: int, daemon: bool) -> BridgeLike:
        self.port = port
        bridge_cls: type[BridgeLike] = NativeBridge if self.mode == "native" else Bridge
        if self.bridge is None or self.bridge.port != port or not isinstance(self.bridge, bridge_cls):
            self.bridge = bridge_cls(port=port)
        self.bridge.activate(daemon=daemon)
        self._save_runtime_state("configured")
        return self.bridge

    def _require_bridge(self) -> BridgeLike:
        if self.bridge is None:
            self.bridge = NativeBridge(port=self.port) if self.mode == "native" else Bridge(port=self.port)
        return self.bridge

    def _bridge_or_default(self) -> BridgeLike:
        return self.bridge or (NativeBridge(port=self.port) if self.mode == "native" else Bridge(port=self.port))

    def _ensure_runtime_window(self, bridge: BridgeLike) -> WindowHandle:
        if (
            self.window_handle is None
            or (self.window_handle.owned and self.window_handle.pid is not None and not process_exists(self.window_handle.pid))
        ):
            web_url = f"http://127.0.0.1:{bridge.port}/native-dashboard" if self.mode == "native" else None
            self.window_handle = window(
                port=bridge.port,
                token=bridge.token,
                close_on_exit=False,
                mode="mini",
                width=420,
                height=340,
                web_url=web_url,
            )
        return self.window_handle

    def _wait_for_browser(self, bridge: BridgeLike) -> None:
        try:
            bridge.wait_ready(timeout=30, require_browser=True)
        except TimeoutError as error:
            url = self.window_handle.url if self.window_handle is not None else bridge.base_url
            if self.window_handle is not None:
                self.window_handle.close()
                self.window_handle = None
            try:
                bridge.close()
            except Exception:  # noqa: BLE001
                pass
            raise TimeoutError(
                "xlocllm bridge was started, but the browser runtime did not connect within 30 seconds. "
                f"The bridge was shut down to avoid an orphan process. Last URL: {url}"
            ) from error

    def _coerce_unit(self, item: Unit | UnitRequest) -> Unit:
        if isinstance(item, Unit):
            if item.mode is None:
                item.mode = self.mode
            elif item.mode != self.mode and not _is_service_unit_type(item.type):
                raise ValueError(
                    f"Unit {item.id!r} was resolved for mode={item.mode!r}, "
                    f"but this runtime uses mode={self.mode!r}. Recreate the unit with mode={self.mode!r}."
                )
            return item
        if isinstance(item, UnitRequest):
            if _is_service_unit_type(item.type):
                return Unit(
                    type=_normalize_service_unit_type(item.type),
                    model=item.model,
                    mode=self.mode,
                    reasoning=item.reasoning,
                    options=dict(item.options or {}),
                )
            resolved = resolve_model(item.type, item.model, mode=self.mode)
            return Unit(
                type=str(resolved["unit"]),
                model=str(resolved["modelId"]),
                model_info=ModelInfo(resolved),
                mode=self.mode,
                reasoning=item.reasoning,
                options=dict(item.options or {}),
            )
        raise TypeError(f"Unsupported runtime item: {type(item)!r}")

    def _attach_unit(self, unit: Unit) -> None:
        unit._runtime = self
        for child in _nested_units(unit):
            child._runtime = self

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
            "mode": self.mode,
            "port": self.port,
            "url": self.url,
            "running": self.running,
            "installed": self.installed,
            "units": self.units(as_dict=True),
            "runtime": {
                "connected": False,
                "backend": self.mode,
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
            mode=self.mode,
            state=state,
            running=self.running,
            installed=self.installed,
            units=[unit.to_payload() for unit in self._units],
        )


def unit(
    type: str,  # noqa: A002
    model: str,
    *,
    mode: str | None = None,
    reasoning: bool | None = None,
    options: dict[str, Any] | None = None,
    rag: Unit | UnitRequest | None = None,
) -> Unit:
    resolved_mode = current_mode(mode)
    if _is_service_unit_type(type):
        return Unit(
            type=_normalize_service_unit_type(type),
            model=model,
            mode=resolved_mode,
            reasoning=reasoning,
            options=dict(options or {}),
        )
    resolved = resolve_model(type, model, mode=resolved_mode)
    rag_unit = _coerce_nested_unit(rag, mode=resolved_mode) if rag is not None else None
    unit_item = Unit(
        type=str(resolved["unit"]),
        model=str(resolved["modelId"]),
        model_info=ModelInfo(resolved),
        mode=resolved_mode,
        reasoning=reasoning,
        options=dict(options or {}),
        rag=rag_unit,
    )
    if reasoning is not None and not unit_item.supports_reasoning:
        raise ValueError(f"{unit_item.label} does not advertise reasoning control")
    return unit_item


def vectorstorage(
    name: str = "default",
    *,
    mode: str | None = None,
    backend: str = "indexeddb",
    metric: str = "cosine",
    persist: bool = True,
    namespace: str = "default",
    options: dict[str, Any] | None = None,
) -> Unit:
    storage_options: dict[str, Any] = {
        "backend": backend,
        "metric": metric,
        "persist": persist,
        "namespace": namespace,
    }
    if options:
        storage_options.update(options)
    resolved_mode = current_mode(mode)
    if resolved_mode == "native" and backend == "indexeddb":
        storage_options["backend"] = "native"
    return Unit(type="vectorstorage", model=name, mode=resolved_mode, options=storage_options)


def rag(
    *,
    emb: Unit | UnitRequest,
    rerank: Unit | UnitRequest | None = None,
    store: Unit | UnitRequest | None = None,
    name: str = "default",
    mode: str | None = None,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
    top_k: int = 5,
    candidate_k: int = 30,
    score_threshold: float | None = None,
    options: dict[str, Any] | None = None,
) -> Unit:
    resolved_mode = current_mode(mode)
    emb_unit = _coerce_nested_unit(emb, mode=resolved_mode)
    rerank_unit = _coerce_nested_unit(rerank, mode=resolved_mode) if rerank is not None else None
    store_unit = _coerce_nested_unit(store, mode=resolved_mode) if store is not None else vectorstorage(name=f"{name}-store", mode=resolved_mode)
    if emb_unit.type != "embedding":
        raise ValueError("rag(emb=...) requires an embedding unit")
    if rerank_unit is not None and rerank_unit.type != "reranker":
        raise ValueError("rag(rerank=...) requires a reranker unit")
    if store_unit.type != "vectorstorage":
        raise ValueError("rag(store=...) requires a vectorstorage unit")
    rag_options: dict[str, Any] = {
        "emb": emb_unit.to_payload(),
        "store": store_unit.to_payload(),
        "rerank": rerank_unit.to_payload() if rerank_unit is not None else None,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "top_k": top_k,
        "candidate_k": candidate_k,
        "score_threshold": score_threshold,
    }
    if options:
        rag_options.update(options)
    return Unit(type="RAG", model=name, mode=resolved_mode, options=rag_options)


def runtime(
    units: Iterable[Unit | UnitRequest],
    *,
    port: int | str = 1146,
    bridge: BridgeLike | None = None,
    runtime_id: str | None = None,
    mode: str | None = None,
) -> Runtime:
    return Runtime(units, port=port, bridge=bridge, runtime_id=runtime_id, mode=mode)


def runtimes(active_only: bool = True) -> list[Runtime]:
    result: list[Runtime] = []
    for record in all_runtime_records():
        runtime_id = str(record.get("id") or "")
        if not runtime_id:
            continue
        port = _int_or_default(record.get("port"), 1146)
        record_mode = current_mode(str(record.get("mode") or current_mode()))
        bridge: BridgeLike = NativeBridge(port=port) if record_mode == "native" else Bridge(port=port)
        if active_only:
            bridge_registry_record = bridge_record(port)
            pid = _int_or_none(bridge_registry_record.get("pid") if bridge_registry_record else None)
            if not process_exists(pid):
                continue
        unit_items = []
        for item in record.get("units", []):
            if isinstance(item, dict) and isinstance(item.get("type"), str) and isinstance(item.get("model"), str):
                restored = _unit_from_payload(item, mode=record_mode)
                if restored is not None:
                    unit_items.append(restored)
        if not unit_items:
            continue
        result.append(Runtime(unit_items, port=port, bridge=bridge, runtime_id=runtime_id, mode=record_mode))
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


def model(name: str, unit: str | None = None, *, mode: str | None = None) -> ModelInfo:
    return catalog_model(name, unit=unit, mode=mode)


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _int_or_default(value: Any, default: int) -> int:
    result = _int_or_none(value)
    return default if result is None else result


def _is_service_unit_type(unit_type: str) -> bool:
    return _normalize_service_unit_type(unit_type) in SERVICE_UNIT_TYPES


def _normalize_service_unit_type(unit_type: str) -> str:
    normalized = unit_type.strip().lower().replace("_", "").replace("-", "")
    if normalized in {"vectorstorage", "vectorstore", "vector"}:
        return "vectorstorage"
    if normalized == "rag":
        return "RAG"
    return unit_type


def _default_bridge_for_mode(mode: str | None = None) -> BridgeLike:
    return NativeBridge() if current_mode(mode) == "native" else Bridge()


def _coerce_nested_unit(item: Unit | UnitRequest | None, *, mode: str | None = None) -> Unit:
    resolved_mode = current_mode(mode)
    if item is None:
        raise TypeError("nested unit cannot be None")
    if isinstance(item, Unit):
        if item.mode is None:
            item.mode = resolved_mode
        elif item.mode != resolved_mode and not _is_service_unit_type(item.type):
            raise ValueError(
                f"Nested unit {item.id!r} was resolved for mode={item.mode!r}, "
                f"but parent uses mode={resolved_mode!r}"
            )
        return item
    if isinstance(item, UnitRequest):
        if _is_service_unit_type(item.type):
            return Unit(
                type=_normalize_service_unit_type(item.type),
                model=item.model,
                mode=resolved_mode,
                reasoning=item.reasoning,
                options=dict(item.options or {}),
            )
        resolved = resolve_model(item.type, item.model, mode=resolved_mode)
        return Unit(
            type=str(resolved["unit"]),
            model=str(resolved["modelId"]),
            model_info=ModelInfo(resolved),
            mode=resolved_mode,
            reasoning=item.reasoning,
            options=dict(item.options or {}),
        )
    raise TypeError(f"Unsupported nested unit: {type(item)!r}")


def _nested_units(unit: Unit) -> list[Unit]:
    result: list[Unit] = []
    if unit.rag is not None:
        result.append(unit.rag)
        result.extend(_nested_units(unit.rag))
    if unit.type == "RAG":
        for key in ("emb", "store", "rerank"):
            child = _unit_from_payload(unit.options.get(key), mode=unit.mode)
            if child is not None:
                result.append(child)
                result.extend(_nested_units(child))
    return result


def _unit_from_payload(value: Any, *, mode: str | None = None) -> Unit | None:
    resolved_mode = current_mode(mode)
    if isinstance(value, Unit):
        return value
    if not isinstance(value, dict):
        return None
    unit_type = value.get("type")
    model = value.get("model")
    if not isinstance(unit_type, str) or not isinstance(model, str):
        return None
    options = value.get("options")
    rag_payload = value.get("rag")
    if _is_service_unit_type(unit_type):
        return Unit(
            type=_normalize_service_unit_type(unit_type),
            model=model,
            mode=resolved_mode,
            reasoning=value.get("reasoning") if isinstance(value.get("reasoning"), bool) else None,
            options=options if isinstance(options, dict) else {},
            rag=_unit_from_payload(rag_payload, mode=resolved_mode),
        )
    resolved = resolve_model(unit_type, model, mode=resolved_mode)
    return Unit(
        type=str(resolved["unit"]),
        model=str(resolved["modelId"]),
        model_info=ModelInfo(resolved),
        mode=resolved_mode,
        reasoning=value.get("reasoning") if isinstance(value.get("reasoning"), bool) else None,
        options=options if isinstance(options, dict) else {},
        rag=_unit_from_payload(rag_payload, mode=resolved_mode),
    )


def _documents_payload(
    documents: str | Sequence[str | Mapping[str, Any]] | None,
) -> str | list[str | dict[str, Any]] | None:
    if documents is None:
        return None
    if isinstance(documents, str):
        return documents
    return [dict(item) if isinstance(item, Mapping) else str(item) for item in documents]


def _ids_payload(ids: str | Sequence[str] | None) -> list[str] | None:
    if ids is None:
        return None
    if isinstance(ids, str):
        return [ids]
    return [str(item) for item in ids]
