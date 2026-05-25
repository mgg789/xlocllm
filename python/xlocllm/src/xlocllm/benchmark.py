from __future__ import annotations

import os
import platform
import shutil
import socket
import sys
import time
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from ._paths import config_dir
from .bridge import Bridge, bridges
from .catalog import ModelInfo, models, normalize_unit
from .window import WindowHandle, find_chromium, window

HF_URL = "https://huggingface.co"


def benchmark(  # noqa: A002
    type: str | None = None,
    *,
    ping_hf: bool = True,
    timeout: float = 2.0,
    browser: bool = True,
    browser_timeout: float = 15.0,
    port: int | None = None,
) -> dict[str, Any]:
    snapshot = system_snapshot(
        ping_hf=ping_hf,
        timeout=timeout,
        browser=browser,
        browser_timeout=browser_timeout,
        port=port,
    )
    if not type:
        return snapshot
    unit_type = normalize_unit(type)
    snapshot["model_type"] = unit_type
    snapshot["recommendations"] = recommend_models(unit_type, snapshot)
    return snapshot


def system_snapshot(
    *,
    ping_hf: bool = True,
    timeout: float = 2.0,
    browser: bool = True,
    browser_timeout: float = 15.0,
    port: int | None = None,
) -> dict[str, Any]:
    memory = memory_snapshot()
    disk = disk_snapshot()
    browser_info = browser_capabilities(start_browser=browser, timeout=browser_timeout, port=port)
    return {
        "ok": True,
        "xlocllm": {"version": package_version()},
        "system": {
            "platform": platform.platform(),
            "os": platform.system(),
            "os_release": platform.release(),
            "machine": platform.machine(),
            "python": sys.version.split()[0],
            "cpu_count": os.cpu_count(),
            "hostname": socket.gethostname(),
        },
        "memory": memory,
        "disk": disk,
        "browser": browser_info,
        "network": {"huggingface": hf_ping(timeout=timeout) if ping_hf else {"checked": False}},
    }


def recommend_models(unit_type: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    raw_browser = snapshot.get("browser")
    browser: dict[str, Any] = raw_browser if isinstance(raw_browser, dict) else {}
    webgpu = browser.get("webgpu")
    candidates = models(unit=unit_type, webgpu=False if webgpu is not True else None)
    eligible, warnings = eligible_models(candidates, snapshot, webgpu is True)
    visible = eligible or candidates
    if not visible:
        return {
            "fast": None,
            "quality": None,
            "warnings": [f"No catalog models found for unit type {unit_type!r}"],
            "selection": selection_info(snapshot, webgpu is True),
        }
    if not eligible:
        warnings.append("No model matched local memory/disk limits; recommendations ignore those limits.")
    fast = sorted(visible, key=fast_weight)[0]
    quality = sorted(visible, key=quality_weight, reverse=True)[0]
    return {
        "fast": recommendation_item(fast),
        "quality": recommendation_item(quality),
        "warnings": warnings,
        "selection": selection_info(snapshot, webgpu is True),
        "candidate_count": len(candidates),
        "eligible_count": len(eligible),
    }


def eligible_models(items: list[ModelInfo], snapshot: dict[str, Any], has_webgpu: bool) -> tuple[list[ModelInfo], list[str]]:
    warnings: list[str] = []
    disk_free_mb = _nested_number(snapshot, "disk", "xlocllm_home", "free_mb")
    ram_free_mb = _nested_number(snapshot, "memory", "available_mb")
    ram_total_mb = _nested_number(snapshot, "memory", "total_mb")
    accelerator_limit_mb = estimated_accelerator_limit_mb(ram_total_mb, ram_free_mb, has_webgpu)
    result: list[ModelInfo] = []
    for item in items:
        if disk_free_mb is not None and item.disk_mb > disk_free_mb * 0.85:
            continue
        if accelerator_limit_mb is not None and item.vram_mb > accelerator_limit_mb:
            continue
        result.append(item)
    if disk_free_mb is None:
        warnings.append("Free disk space is unknown; disk fit was not checked.")
    if accelerator_limit_mb is None:
        warnings.append("Memory limit is unknown; memory fit was not checked.")
    if has_webgpu:
        warnings.append("WebGPU is available, but browser APIs do not expose exact GPU memory; fit is estimated.")
    else:
        warnings.append("WebGPU is not confirmed; recommendations use the CPU/WASM-compatible catalog subset.")
    return result, warnings


def estimated_accelerator_limit_mb(ram_total_mb: float | None, ram_free_mb: float | None, has_webgpu: bool) -> float | None:
    if has_webgpu:
        if ram_total_mb is None:
            return None
        if ram_total_mb >= 64000:
            return 24000
        if ram_total_mb >= 32000:
            return 12000
        if ram_total_mb >= 16000:
            return 7000
        return 3500
    if ram_free_mb is not None:
        return max(512, ram_free_mb * 0.6)
    if ram_total_mb is not None:
        return max(512, ram_total_mb * 0.35)
    return None


def recommendation_item(item: ModelInfo) -> dict[str, Any]:
    return {
        "unit": item.unit,
        "model": item.model_id,
        "label": item.label,
        "runtime": item.runtime,
        "hardware_tier": item.hardware_tier,
        "disk_mb": item.disk_mb,
        "vram_mb": item.vram_mb,
        "parameter_b": item.get("parameterB"),
        "aliases": item.aliases,
    }


def fast_weight(item: ModelInfo) -> tuple[int, int, int, int, float]:
    tier_order = {"tiny": 0, "small": 1, "medium": 2, "large": 3}
    verified_penalty = 0 if item.get("availability") == "verified" else 5
    cpu_penalty = 0 if item.cpu_fallback else 2
    return (
        verified_penalty,
        cpu_penalty,
        tier_order.get(item.hardware_tier, 99),
        item.vram_mb,
        float(item.get("parameterB") or 0),
    )


def quality_weight(item: ModelInfo) -> tuple[int, float, int, int]:
    tier_order = {"tiny": 0, "small": 1, "medium": 2, "large": 3}
    verified_bonus = 1 if item.get("availability") == "verified" else 0
    return (
        verified_bonus,
        float(item.get("parameterB") or 0),
        tier_order.get(item.hardware_tier, 0),
        item.vram_mb,
    )


def selection_info(snapshot: dict[str, Any], has_webgpu: bool) -> dict[str, Any]:
    ram_free_mb = _nested_number(snapshot, "memory", "available_mb")
    ram_total_mb = _nested_number(snapshot, "memory", "total_mb")
    return {
        "webgpu_confirmed": has_webgpu,
        "estimated_memory_limit_mb": estimated_accelerator_limit_mb(ram_total_mb, ram_free_mb, has_webgpu),
        "disk_free_mb": _nested_number(snapshot, "disk", "xlocllm_home", "free_mb"),
    }


def browser_capabilities(*, start_browser: bool = True, timeout: float = 15.0, port: int | None = None) -> dict[str, Any]:
    for bridge in bridges(active_only=True):
        try:
            status = bridge.status()
        except Exception:  # noqa: BLE001
            continue
        runtime = status.get("runtime")
        if not isinstance(runtime, dict) or not runtime.get("connected"):
            continue
        capabilities = runtime.get("capabilities")
        if isinstance(capabilities, dict):
            return {
                "status": "connected",
                "bridge_port": bridge.port,
                "webgpu": bool(capabilities.get("webgpu")),
                "webnn": bool(capabilities.get("webnn")),
                "npu": bool(capabilities.get("webnn")),
                "backend": capabilities.get("backend"),
                "cpu_fallback": bool(capabilities.get("cpuFallback")),
                "model_count": capabilities.get("modelCount"),
                "catalog_model_count": capabilities.get("catalogModelCount"),
            }
        raw_npu = runtime.get("npu")
        npu: dict[str, Any] = raw_npu if isinstance(raw_npu, dict) else {}
        return {
            "status": "connected",
            "bridge_port": bridge.port,
            "webgpu": None,
            "webnn": npu.get("status") == "active",
            "npu": npu.get("status") == "active",
            "backend": None,
            "cpu_fallback": None,
            "model_count": runtime.get("catalogModelCount"),
            "catalog_model_count": runtime.get("catalogModelCount"),
        }
    if not start_browser:
        return {
            "status": "unknown",
            "webgpu": None,
            "webnn": None,
            "npu": None,
            "backend": None,
            "reason": "No active paired browser runtime found and browser probing is disabled.",
        }
    return probe_browser_capabilities(timeout=timeout, port=port)


def probe_browser_capabilities(*, timeout: float = 15.0, port: int | None = None) -> dict[str, Any]:
    if find_chromium() is None:
        return {
            "status": "unknown",
            "webgpu": None,
            "webnn": None,
            "npu": None,
            "backend": None,
            "reason": "No supported Chromium/Edge/Chrome executable was found for temporary probing.",
        }
    bridge = Bridge(port=port or free_port())
    handle: WindowHandle | None = None
    try:
        bridge.activate(daemon=False)
        handle = window(
            port=bridge.port,
            token=bridge.token,
            close_on_exit=False,
            mode="mini",
            width=360,
            height=260,
        )
        bridge.wait_ready(timeout=timeout, require_browser=True)
        status = bridge.status()
        runtime = status.get("runtime")
        if isinstance(runtime, dict):
            capabilities = runtime.get("capabilities")
            if isinstance(capabilities, dict):
                return {
                    "status": "probed",
                    "bridge_port": bridge.port,
                    "window_url": handle.url if handle else None,
                    "webgpu": bool(capabilities.get("webgpu")),
                    "webnn": bool(capabilities.get("webnn")),
                    "npu": bool(capabilities.get("webnn")),
                    "backend": capabilities.get("backend"),
                    "cpu_fallback": bool(capabilities.get("cpuFallback")),
                    "model_count": capabilities.get("modelCount"),
                    "catalog_model_count": capabilities.get("catalogModelCount"),
                }
        return {
            "status": "unknown",
            "bridge_port": bridge.port,
            "webgpu": None,
            "webnn": None,
            "npu": None,
            "backend": None,
            "reason": "Temporary browser connected but did not report runtime capabilities.",
        }
    except Exception as error:  # noqa: BLE001
        return {
            "status": "unknown",
            "bridge_port": bridge.port,
            "webgpu": None,
            "webnn": None,
            "npu": None,
            "backend": None,
            "reason": str(error),
        }
    finally:
        if handle is not None:
            handle.close()
        try:
            bridge.close()
        except Exception:  # noqa: BLE001
            pass


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def hf_ping(*, timeout: float = 2.0) -> dict[str, Any]:
    request = Request(HF_URL, method="HEAD", headers={"User-Agent": "xlocllm-benchmark"})
    started = time.perf_counter()
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310
            elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
            return {
                "checked": True,
                "ok": 200 <= int(response.status) < 500,
                "url": HF_URL,
                "status_code": int(response.status),
                "latency_ms": elapsed_ms,
            }
    except (OSError, URLError) as error:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "checked": True,
            "ok": False,
            "url": HF_URL,
            "latency_ms": elapsed_ms,
            "error": str(error),
        }


def disk_snapshot() -> dict[str, Any]:
    home = config_dir()
    return {
        "xlocllm_home": disk_usage(home),
        "cwd": disk_usage(os.getcwd()),
    }


def disk_usage(path: os.PathLike[str] | str) -> dict[str, Any]:
    usage = shutil.disk_usage(path)
    return {
        "path": str(path),
        "total_mb": round(usage.total / 1024 / 1024, 2),
        "used_mb": round(usage.used / 1024 / 1024, 2),
        "free_mb": round(usage.free / 1024 / 1024, 2),
    }


def memory_snapshot() -> dict[str, Any]:
    if sys.platform == "win32":
        return windows_memory_snapshot()
    page_size = os.sysconf("SC_PAGE_SIZE") if hasattr(os, "sysconf") and "SC_PAGE_SIZE" in os.sysconf_names else None
    phys_pages = os.sysconf("SC_PHYS_PAGES") if hasattr(os, "sysconf") and "SC_PHYS_PAGES" in os.sysconf_names else None
    avail_pages = os.sysconf("SC_AVPHYS_PAGES") if hasattr(os, "sysconf") and "SC_AVPHYS_PAGES" in os.sysconf_names else None
    total = page_size * phys_pages if page_size and phys_pages else None
    available = page_size * avail_pages if page_size and avail_pages else None
    return memory_dict(total, available)


def windows_memory_snapshot() -> dict[str, Any]:
    import ctypes

    class MemoryStatusEx(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    status = MemoryStatusEx()
    status.dwLength = ctypes.sizeof(MemoryStatusEx)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):  # type: ignore[attr-defined]
        return memory_dict(None, None)
    return memory_dict(int(status.ullTotalPhys), int(status.ullAvailPhys), int(status.dwMemoryLoad))


def memory_dict(total_bytes: int | None, available_bytes: int | None, load_percent: int | None = None) -> dict[str, Any]:
    return {
        "total_mb": round(total_bytes / 1024 / 1024, 2) if total_bytes is not None else None,
        "available_mb": round(available_bytes / 1024 / 1024, 2) if available_bytes is not None else None,
        "load_percent": load_percent,
    }


def package_version() -> str | None:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "pyproject.toml"
        if not candidate.exists():
            continue
        text = candidate.read_text(encoding="utf-8")
        if 'name = "xlocllm"' not in text:
            continue
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("version = "):
                return stripped.split("=", 1)[1].strip().strip('"')
    try:
        return version("xlocllm")
    except PackageNotFoundError:
        return None


def _nested_number(data: dict[str, Any], *keys: str) -> float | None:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    if isinstance(current, int | float):
        return float(current)
    return None
