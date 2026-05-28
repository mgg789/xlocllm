"""Python SDK for xlocllm."""

from ._mode import DEFAULT_MODE
from .bridge import Bridge, BridgeGroup, GetBridge, bridges
from .benchmark import benchmark
from .catalog import ModelInfo, cpu_fallback_model_ids, model, models, supports_cpu_fallback, supports_reasoning
from .exceptions import (
    BridgeNotReady,
    BrowserNotConnected,
    ModelNotFound,
    RuntimeNotFound,
    UnitNotFound,
    XlocLLMError,
)
from .native_bridge import NativeBridge
from .runtime import Runtime, Unit, UnitRuntime, rag, runtime, runtimes, status, unit, vectorstorage
from .types import UnitRequest
from .window import window

mode = DEFAULT_MODE

__all__ = [
    "Bridge",
    "BridgeGroup",
    "BridgeNotReady",
    "BrowserNotConnected",
    "GetBridge",
    "ModelInfo",
    "ModelNotFound",
    "NativeBridge",
    "Runtime",
    "RuntimeNotFound",
    "Unit",
    "UnitRuntime",
    "UnitRequest",
    "UnitNotFound",
    "XlocLLMError",
    "benchmark",
    "bridges",
    "cpu_fallback_model_ids",
    "model",
    "mode",
    "models",
    "rag",
    "runtime",
    "runtimes",
    "status",
    "supports_cpu_fallback",
    "supports_reasoning",
    "unit",
    "vectorstorage",
    "window",
]
