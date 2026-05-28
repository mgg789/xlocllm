"""Python SDK for xlocllm."""

from ._mode import DEFAULT_MODE
from ._scopes import native, web, webgpu
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
__author__ = "mgg789"
__license__ = "BSD-3-Clause"
REPOSITORY_URL = "https://github.com/mgg789/xlocllm/"
DOCUMENTATION_URL = "https://github.com/mgg789/xlocllm/wiki/Python-Unit"
WIKI_URL = "https://github.com/mgg789/xlocllm/wiki"
PROJECT_URLS = {
    "repository": REPOSITORY_URL,
    "documentation": DOCUMENTATION_URL,
    "wiki": WIKI_URL,
}

__all__ = [
    "Bridge",
    "BridgeGroup",
    "BridgeNotReady",
    "BrowserNotConnected",
    "GetBridge",
    "ModelInfo",
    "ModelNotFound",
    "NativeBridge",
    "DOCUMENTATION_URL",
    "PROJECT_URLS",
    "REPOSITORY_URL",
    "Runtime",
    "RuntimeNotFound",
    "Unit",
    "UnitRuntime",
    "UnitRequest",
    "UnitNotFound",
    "WIKI_URL",
    "XlocLLMError",
    "benchmark",
    "bridges",
    "cpu_fallback_model_ids",
    "model",
    "mode",
    "models",
    "native",
    "rag",
    "runtime",
    "runtimes",
    "status",
    "supports_cpu_fallback",
    "supports_reasoning",
    "unit",
    "vectorstorage",
    "web",
    "webgpu",
    "window",
]
