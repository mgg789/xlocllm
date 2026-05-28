from __future__ import annotations

import contextvars
from contextlib import ContextDecorator
from types import TracebackType
from typing import Any

from ._mode import pop_scope, push_scope


class ModeScope(ContextDecorator):
    def __init__(self, mode: str, *, web_device: str | None = None) -> None:
        self.mode = mode
        self.web_device = web_device
        self._tokens: contextvars.ContextVar[tuple[Any, ...]] = contextvars.ContextVar(
            f"xlocllm_{mode}_{web_device or 'default'}_tokens",
            default=(),
        )

    def __enter__(self) -> ModeScope:
        stack = self._tokens.get()
        self._tokens.set((*stack, push_scope(self.mode, self.web_device)))
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        stack = self._tokens.get()
        if not stack:
            return False
        tokens = stack[-1]
        self._tokens.set(stack[:-1])
        pop_scope(tokens)
        return False


native = ModeScope("native")
web = ModeScope("web", web_device="wasm")
webgpu = ModeScope("web", web_device="webgpu")
