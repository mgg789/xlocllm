from __future__ import annotations

import os
from pathlib import Path


def config_dir() -> Path:
    override = os.environ.get("XLOCLLM_HOME")
    if override:
        path = Path(override).expanduser()
    elif os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
        path = base / "xlocllm"
    else:
        path = Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state"))) / "xlocllm"
    path.mkdir(parents=True, exist_ok=True)
    return path


def registry_path() -> Path:
    return config_dir() / "bridges.json"


def native_dir() -> Path:
    path = config_dir() / "native"
    path.mkdir(parents=True, exist_ok=True)
    return path


def native_engine_dir() -> Path:
    path = native_dir() / "engines"
    path.mkdir(parents=True, exist_ok=True)
    return path


def native_model_dir() -> Path:
    path = native_dir() / "models"
    path.mkdir(parents=True, exist_ok=True)
    return path


def native_store_dir() -> Path:
    path = native_dir() / "stores"
    path.mkdir(parents=True, exist_ok=True)
    return path


def browser_profile_dir(port: int, profile: str | None = None) -> Path:
    suffix = "" if not profile else "-" + "".join(char if char.isalnum() or char in {"-", "_"} else "-" for char in profile)
    path = config_dir() / "browser-profiles" / f"{port}{suffix}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def repo_root_from_here() -> Path | None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "packages" / "catalog" / "models.json").exists():
            return parent
    return None


def web_dist_dir() -> Path | None:
    root = repo_root_from_here()
    if root is not None:
        dist = root / "apps" / "web" / "dist"
        if (dist / "index.html").exists():
            return dist
    package_dist = Path(__file__).resolve().parent / "webui"
    if (package_dist / "index.html").exists():
        return package_dist
    return None
