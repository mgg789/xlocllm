from __future__ import annotations

import contextvars
import sys
from typing import Literal

RuntimeMode = Literal["native", "web"]
DEFAULT_MODE: RuntimeMode = "native"
VALID_MODES = {"native", "web"}
_scoped_mode: contextvars.ContextVar[RuntimeMode | None] = contextvars.ContextVar("xlocllm_mode", default=None)
_scoped_web_device: contextvars.ContextVar[str | None] = contextvars.ContextVar("xlocllm_web_device", default=None)


def normalize_mode(mode: str | None) -> RuntimeMode:
    value = (mode or DEFAULT_MODE).strip().lower()
    if value not in VALID_MODES:
        raise ValueError("xlocllm mode must be 'native' or 'web'")
    return value  # type: ignore[return-value]


def current_mode(mode: str | None = None) -> RuntimeMode:
    if mode is not None:
        return normalize_mode(mode)
    scoped = _scoped_mode.get()
    if scoped is not None:
        return scoped
    module = sys.modules.get("xlocllm")
    if module is not None:
        configured = getattr(module, "mode", DEFAULT_MODE)
        if isinstance(configured, str):
            return normalize_mode(configured)
    return DEFAULT_MODE


def current_web_device() -> str | None:
    return _scoped_web_device.get()


def push_scope(mode: str, web_device: str | None = None) -> tuple[contextvars.Token[RuntimeMode | None], contextvars.Token[str | None]]:
    return _scoped_mode.set(normalize_mode(mode)), _scoped_web_device.set(web_device)


def pop_scope(tokens: tuple[contextvars.Token[RuntimeMode | None], contextvars.Token[str | None]]) -> None:
    mode_token, device_token = tokens
    _scoped_web_device.reset(device_token)
    _scoped_mode.reset(mode_token)
