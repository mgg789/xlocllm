from __future__ import annotations

import json
import os
import secrets
import time
from typing import Any

from ._paths import registry_path


def load_registry() -> dict[str, Any]:
    path = registry_path()
    if not path.exists():
        return {"bridges": {}, "runtimes": {}}
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"bridges": {}, "runtimes": {}}
    registry.setdefault("bridges", {})
    registry.setdefault("runtimes", {})
    return registry


def save_registry(registry: dict[str, Any]) -> None:
    path = registry_path()
    tmp = path.with_name(f"{path.stem}.{os.getpid()}.{secrets.token_hex(4)}.tmp")
    tmp.write_text(json.dumps(registry, indent=2, sort_keys=True), encoding="utf-8")
    last_error: PermissionError | None = None
    for _ in range(10):
        try:
            tmp.replace(path)
            return
        except PermissionError as error:
            last_error = error
            time.sleep(0.05)
    try:
        tmp.unlink(missing_ok=True)
    except OSError:
        pass
    if last_error is not None:
        raise last_error


def bridge_record(port: int) -> dict[str, Any] | None:
    return load_registry().get("bridges", {}).get(str(port))


def upsert_bridge(port: int, **values: Any) -> dict[str, Any]:
    registry = load_registry()
    bridges = registry.setdefault("bridges", {})
    record = bridges.setdefault(str(port), {})
    record.update(values)
    record.setdefault("port", port)
    record.setdefault("token", secrets.token_urlsafe(24))
    record["updated_at"] = time.time()
    save_registry(registry)
    return record


def remove_bridge(port: int) -> None:
    registry = load_registry()
    registry.setdefault("bridges", {}).pop(str(port), None)
    save_registry(registry)


def runtime_record(runtime_id: str) -> dict[str, Any] | None:
    record = load_registry().get("runtimes", {}).get(runtime_id)
    return record if isinstance(record, dict) else None


def upsert_runtime(runtime_id: str, **values: Any) -> dict[str, Any]:
    registry = load_registry()
    runtimes = registry.setdefault("runtimes", {})
    record = runtimes.setdefault(runtime_id, {})
    record.update(values)
    record.setdefault("id", runtime_id)
    record["updated_at"] = time.time()
    save_registry(registry)
    return record


def remove_runtime(runtime_id: str) -> None:
    registry = load_registry()
    registry.setdefault("runtimes", {}).pop(runtime_id, None)
    save_registry(registry)


def all_runtime_records() -> list[dict[str, Any]]:
    records = []
    for value in load_registry().get("runtimes", {}).values():
        if isinstance(value, dict):
            records.append(value)
    return records


def active_bridge_ports() -> list[int]:
    ports = []
    for value in load_registry().get("bridges", {}):
        try:
            ports.append(int(value))
        except ValueError:
            continue
    return sorted(ports)


def process_exists(pid: int | None) -> bool:
    if not pid:
        return False
    if os.name == "nt":
        import subprocess

        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            check=False,
        )
        return str(pid) in result.stdout
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True
