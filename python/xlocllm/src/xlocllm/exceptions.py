from __future__ import annotations


class XlocLLMError(Exception):
    """Base exception for xlocllm SDK errors."""


class BridgeNotReady(RuntimeError, XlocLLMError):
    """Raised when a local bridge cannot be reached."""


class BrowserNotConnected(RuntimeError, XlocLLMError):
    """Raised when the bridge is up but no browser runtime is paired."""


class ModelNotFound(ValueError, XlocLLMError):
    """Raised when a model name or alias is not present in the catalog."""


class UnitNotFound(ValueError, XlocLLMError):
    """Raised when a unit type is not present in the catalog."""


class RuntimeNotFound(ValueError, XlocLLMError):
    """Raised when a runtime id is not known to the local registry."""
