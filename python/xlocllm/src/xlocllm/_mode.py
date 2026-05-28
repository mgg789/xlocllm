from __future__ import annotations

import sys
from typing import Literal

RuntimeMode = Literal["native", "web"]
DEFAULT_MODE: RuntimeMode = "native"
VALID_MODES = {"native", "web"}


def normalize_mode(mode: str | None) -> RuntimeMode:
    value = (mode or DEFAULT_MODE).strip().lower()
    if value not in VALID_MODES:
        raise ValueError("xlocllm mode must be 'native' or 'web'")
    return value  # type: ignore[return-value]


def current_mode(mode: str | None = None) -> RuntimeMode:
    if mode is not None:
        return normalize_mode(mode)
    module = sys.modules.get("xlocllm")
    if module is not None:
        configured = getattr(module, "mode", DEFAULT_MODE)
        if isinstance(configured, str):
            return normalize_mode(configured)
    return DEFAULT_MODE
