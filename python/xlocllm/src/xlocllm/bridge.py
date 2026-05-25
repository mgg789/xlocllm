from __future__ import annotations

import secrets
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from typing import Any

from ._http import request_json
from ._server import run_server
from .catalog import all_models, all_units
from .registry import active_bridge_ports, bridge_record, process_exists, remove_bridge, upsert_bridge


@dataclass
class Bridge:
    port: int = 1146
    ttl: float | None = None
    live_time: float | None = None

    def __post_init__(self) -> None:
        record = bridge_record(self.port)
        self.token = str(record.get("token")) if record and record.get("token") else secrets.token_urlsafe(24)
        self._thread: threading.Thread | None = None

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    @property
    def url(self) -> str:
        return f"{self.base_url}/v1"

    def activate(self, daemon: bool = False) -> "Bridge":
        if self._is_healthy():
            upsert_bridge(self.port, token=self.token)
            return self
        record = upsert_bridge(self.port, token=self.token)
        self.token = str(record["token"])
        if daemon:
            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
            subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "xlocllm._server",
                    "--port",
                    str(self.port),
                    "--token",
                    self.token,
                    *([] if self.live_time is None else ["--live-time", str(self.live_time)]),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=sys.platform != "win32",
                creationflags=creationflags,
            )
        else:
            self._thread = threading.Thread(
                target=run_server,
                kwargs={"port": self.port, "token": self.token, "live_time": self.live_time},
                daemon=True,
            )
            self._thread.start()
        self.wait_ready(timeout=15)
        return self

    def close(self) -> dict[str, Any]:
        result = self._post("/xlocllm/v1/shutdown", {}, timeout=5)
        remove_bridge(self.port)
        return result

    def status(self) -> dict[str, Any]:
        return self._get("/xlocllm/v1/status")

    def health(self) -> dict[str, Any]:
        return self._get("/health")

    def processes(self) -> dict[str, Any]:
        record = bridge_record(self.port) or {}
        pid = _int_or_none(record.get("pid"))
        window_pid = _int_or_none(record.get("window_pid"))
        return {
            "bridge": {"pid": pid, "alive": process_exists(pid)},
            "window": {"pid": window_pid, "alive": process_exists(window_pid)},
        }

    def models(self) -> list[dict[str, Any]]:
        try:
            return list(self._get("/xlocllm/v1/models").get("models", []))
        except Exception:
            return all_models()

    def units(self) -> list[dict[str, Any]]:
        try:
            return list(self._get("/xlocllm/v1/units").get("units", []))
        except Exception:
            return all_units()

    def logs(self, limit: int = 200) -> list[dict[str, Any]]:
        return list(self._get(f"/xlocllm/v1/logs?limit={limit}").get("logs", []))

    def wait_ready(self, timeout: float | None = None, require_browser: bool = False) -> "Bridge":
        deadline = time.time() + (timeout if timeout is not None else 60)
        last_error: Exception | None = None
        while time.time() < deadline:
            try:
                health = self.health()
                if health.get("ok") and (not require_browser or health.get("browser_connected")):
                    return self
            except Exception as error:  # noqa: BLE001
                last_error = error
            time.sleep(0.2)
        if last_error:
            raise TimeoutError(f"xlocllm bridge did not become ready: {last_error}") from last_error
        raise TimeoutError("xlocllm bridge did not become ready")

    def reload(self, units: list[dict[str, str]] | None = None) -> dict[str, Any]:
        return self._post("/xlocllm/v1/runtime/reload", {"units": units or []}, timeout=1800)

    def set_active(self, unit: str, active: bool = True, model: str | None = None) -> dict[str, Any]:
        payload = {"unit": unit, "model": model or "", "active": active}
        if active:
            return self._post(
                "/xlocllm/v1/runtime/run",
                {"units": [{"type": unit, "model": model or ""}]},
                timeout=1800,
            )
        return self._post("/xlocllm/v1/runtime/set_active", payload, timeout=300)

    def delete_model(self, unit_or_model: str, model: str | None = None) -> dict[str, Any]:
        payload = {"unit": unit_or_model, "model": model or unit_or_model}
        return self._post("/xlocllm/v1/models/delete", payload, timeout=300)

    def delete_all_models(self, confirm: bool = True) -> dict[str, Any]:
        if not confirm:
            raise ValueError("delete_all_models requires confirm=True")
        return self._post("/xlocllm/v1/models/delete_all", {}, timeout=600)

    def invoke(self, unit: str, payload: dict[str, Any], timeout: float | None = None) -> dict[str, Any]:
        endpoint = unit.strip("/")
        return self._post(f"/xlocllm/v1/invoke/{endpoint}", payload, timeout=timeout or 1800)

    def _get(self, path: str, timeout: float = 15.0) -> dict[str, Any]:
        return request_json("GET", self.base_url + path, timeout=timeout)

    def _post(self, path: str, payload: dict[str, Any], timeout: float = 60.0) -> dict[str, Any]:
        return request_json("POST", self.base_url + path, payload, timeout=timeout)

    def _is_healthy(self) -> bool:
        try:
            return bool(self.health().get("ok"))
        except Exception:
            return False


class BridgeGroup:
    def __init__(self, bridges: list[Bridge]) -> None:
        self.bridges = bridges

    def __iter__(self) -> Any:
        return iter(self.bridges)

    def __len__(self) -> int:
        return len(self.bridges)

    def activate(self, daemon: bool = False) -> list[Bridge]:
        return [bridge.activate(daemon=daemon) for bridge in self.bridges]

    def close(self) -> list[dict[str, Any]]:
        return [bridge.close() for bridge in self.bridges]

    def status(self) -> list[dict[str, Any]]:
        return [bridge.status() for bridge in self.bridges]

    def health(self) -> list[dict[str, Any]]:
        return [bridge.health() for bridge in self.bridges]


def GetBridge(port: int | None = None) -> Bridge | BridgeGroup:
    if port is not None:
        return Bridge(port=port)
    return BridgeGroup(bridges())


def bridges(active_only: bool = True) -> list[Bridge]:
    bridges: list[Bridge] = []
    for candidate in active_bridge_ports():
        record = bridge_record(candidate)
        if not record:
            continue
        pid = _int_or_none(record.get("pid"))
        if not active_only or process_exists(pid):
            bridges.append(Bridge(port=candidate))
    return bridges


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
