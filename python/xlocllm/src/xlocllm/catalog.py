from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any

from ._paths import repo_root_from_here
from ._mode import current_mode, normalize_mode
from .exceptions import ModelNotFound, UnitNotFound

CPU_FALLBACK_TIERS = {"tiny", "small"}
CPU_FALLBACK_MAX_VRAM_MB = 1500
CPU_FALLBACK_MAX_DISK_MB = 1600
NATIVE_MODELS_PER_UNIT = 4
DEFAULT_GGUF_QUANT = "q4"
GGUF_QUANT_FALLBACK_ORDER = ["q4", "q8", "fp16", "fp32", "q6", "q5", "q3", "q2"]
GGUF_QUANTIZATION_PATTERNS: dict[str, list[str]] = {
    "q2": ["*Q2_K*.gguf", "*Q2*.gguf"],
    "q3": ["*Q3_K_M*.gguf", "*Q3_K*.gguf", "*Q3*.gguf"],
    "q4": ["*Q4_K_M*.gguf", "*Q4_K*.gguf", "*Q4*.gguf"],
    "q5": ["*Q5_K_M*.gguf", "*Q5_K*.gguf", "*Q5*.gguf"],
    "q6": ["*Q6_K*.gguf", "*Q6*.gguf"],
    "q8": ["*Q8_0*.gguf", "*Q8*.gguf"],
    "fp16": ["*F16*.gguf", "*f16*.gguf", "*FP16*.gguf", "*fp16*.gguf"],
    "fp32": ["*F32*.gguf", "*f32*.gguf", "*FP32*.gguf", "*fp32*.gguf"],
}
NATIVE_PRIORITY_ALIASES: dict[str, list[str]] = {
    "embedding": ["multilingual-e5-small", "all-MiniLM-L6-v2"],
    "reranker": ["bge-reranker-v2-m3", "bge-reranker-base"],
    "translator": ["opus-en-ru", "nllb-200"],
    "tts": ["kokoro", "speecht5"],
    "image-classification": ["mobilenet", "vit-base-224"],
    "object-detection": ["yolos-tiny", "detr"],
    "image-segmentation": ["modnet", "ben2"],
    "depth-estimation": ["depth-anything-small", "midas"],
    "vlm": ["blip", "git-base"],
    "asr": ["whisper-tiny", "whisper-base"],
    "ocr": ["trocr", "ocr"],
    "text-classification": ["sentiment", "toxic"],
    "ner": ["bert-ner", "token-classification"],
    "summarization": ["distilbart", "rut5"],
    "text2text": ["t5-small", "flan-t5-small"],
    "code": ["codebert-base", "codebert-javascript"],
}


NATIVE_LLM_MODELS: list[dict[str, Any]] = [
    {
        "unit": "LLM",
        "runtime": "native",
        "backend": "llama.cpp",
        "format": "gguf",
        "task": "text-generation",
        "taskGroup": "LLM",
        "modelId": "Qwen3-0.6B-GGUF",
        "backendModelId": "Qwen/Qwen3-0.6B-GGUF",
        "repo": "Qwen/Qwen3-0.6B-GGUF",
        "files": GGUF_QUANTIZATION_PATTERNS[DEFAULT_GGUF_QUANT],
        "quantizations": GGUF_QUANTIZATION_PATTERNS,
        "defaultQuantization": DEFAULT_GGUF_QUANT,
        "quantizationFallbackOrder": GGUF_QUANT_FALLBACK_ORDER,
        "aliases": [
            "Qwen3-0.6B-Q4_K_M-GGUF",
            "Qwen-3.5-0.8b",
            "Qwen-3.5-0.8b-full",
            "Qwen-3.5-0.8b-fp32",
            "Qwen3.5-0.8B-q4f16_1-MLC",
            "Qwen3.5-0.8B-fp32-ONNX",
            "qwen3-0.6b",
            "qwen-native-small",
        ],
        "label": "Qwen3 0.6B GGUF",
        "provider": "Qwen",
        "logoKey": "model",
        "languages": ["multilingual"],
        "license": "apache-2.0",
        "hardwareTier": "small",
        "parameterB": 0.6,
        "modelSizeGb": 0.45,
        "diskMB": 480,
        "vramMB": 900,
        "dtype": "Q4_K_M",
        "quantization": "Q4_K_M",
        "providers": ["cuda", "metal", "vulkan", "cpu"],
        "npuEligible": False,
        "availability": "verified",
        "verified": True,
        "notes": "Small native GGUF chat model for fast local smoke tests and low-memory devices.",
        "tags": ["native", "llama.cpp", "gguf", "reasoning"],
    },
    {
        "unit": "LLM",
        "runtime": "native",
        "backend": "llama.cpp",
        "format": "gguf",
        "task": "text-generation",
        "taskGroup": "LLM",
        "modelId": "SmolLM2-360M-Instruct-GGUF",
        "backendModelId": "bartowski/SmolLM2-360M-Instruct-GGUF",
        "repo": "bartowski/SmolLM2-360M-Instruct-GGUF",
        "files": GGUF_QUANTIZATION_PATTERNS[DEFAULT_GGUF_QUANT],
        "quantizations": GGUF_QUANTIZATION_PATTERNS,
        "defaultQuantization": DEFAULT_GGUF_QUANT,
        "quantizationFallbackOrder": GGUF_QUANT_FALLBACK_ORDER,
        "aliases": ["SmolLM2-360M-Instruct-Q4_K_M-GGUF", "SmolLM2-360M", "smollm2", "smollm2-native"],
        "label": "SmolLM2 360M Instruct GGUF",
        "provider": "HuggingFaceTB",
        "logoKey": "huggingface",
        "languages": ["en"],
        "license": "apache-2.0",
        "hardwareTier": "tiny",
        "parameterB": 0.36,
        "modelSizeGb": 0.28,
        "diskMB": 300,
        "vramMB": 650,
        "dtype": "Q4_K_M",
        "quantization": "Q4_K_M",
        "providers": ["cuda", "metal", "vulkan", "cpu"],
        "npuEligible": False,
        "availability": "verified",
        "verified": True,
        "notes": "Very small native chat model for CPU-first checks.",
        "tags": ["native", "llama.cpp", "gguf"],
    },
    {
        "unit": "LLM",
        "runtime": "native",
        "backend": "llama.cpp",
        "format": "gguf",
        "task": "text-generation",
        "taskGroup": "LLM",
        "modelId": "Llama-3.2-1B-Instruct-GGUF",
        "backendModelId": "bartowski/Llama-3.2-1B-Instruct-GGUF",
        "repo": "bartowski/Llama-3.2-1B-Instruct-GGUF",
        "files": GGUF_QUANTIZATION_PATTERNS[DEFAULT_GGUF_QUANT],
        "quantizations": GGUF_QUANTIZATION_PATTERNS,
        "defaultQuantization": DEFAULT_GGUF_QUANT,
        "quantizationFallbackOrder": GGUF_QUANT_FALLBACK_ORDER,
        "aliases": ["Llama-3.2-1B-Instruct-Q4_K_M-GGUF", "Llama-3.2-1b", "llama-1b", "llama-native-small"],
        "label": "Llama 3.2 1B Instruct GGUF",
        "provider": "Meta",
        "logoKey": "model",
        "languages": ["en", "multilingual"],
        "license": "llama3.2",
        "hardwareTier": "small",
        "parameterB": 1.0,
        "modelSizeGb": 0.75,
        "diskMB": 820,
        "vramMB": 1400,
        "dtype": "Q4_K_M",
        "quantization": "Q4_K_M",
        "providers": ["cuda", "metal", "vulkan", "cpu"],
        "npuEligible": False,
        "availability": "verified",
        "verified": True,
        "notes": "Small general native chat model.",
        "tags": ["native", "llama.cpp", "gguf"],
    },
    {
        "unit": "LLM",
        "runtime": "native",
        "backend": "llama.cpp",
        "format": "gguf",
        "task": "text-generation",
        "taskGroup": "LLM",
        "modelId": "Phi-3.5-mini-instruct-GGUF",
        "backendModelId": "bartowski/Phi-3.5-mini-instruct-GGUF",
        "repo": "bartowski/Phi-3.5-mini-instruct-GGUF",
        "files": GGUF_QUANTIZATION_PATTERNS[DEFAULT_GGUF_QUANT],
        "quantizations": GGUF_QUANTIZATION_PATTERNS,
        "defaultQuantization": DEFAULT_GGUF_QUANT,
        "quantizationFallbackOrder": GGUF_QUANT_FALLBACK_ORDER,
        "aliases": ["Phi-3.5-mini-instruct-Q4_K_M-GGUF", "Phi-4-mini", "phi4-mini", "phi3.5-mini-native"],
        "label": "Phi 3.5 mini Instruct GGUF",
        "provider": "Microsoft",
        "logoKey": "microsoft",
        "languages": ["en", "multilingual"],
        "license": "mit",
        "hardwareTier": "medium",
        "parameterB": 3.8,
        "modelSizeGb": 2.4,
        "diskMB": 2600,
        "vramMB": 4200,
        "dtype": "Q4_K_M",
        "quantization": "Q4_K_M",
        "providers": ["cuda", "metal", "vulkan", "cpu"],
        "npuEligible": False,
        "availability": "verified",
        "verified": True,
        "notes": "Quality native small model for stronger local chat.",
        "tags": ["native", "llama.cpp", "gguf"],
    },
]


@dataclass(frozen=True)
class ModelInfo:
    data: dict[str, Any]

    @property
    def unit(self) -> str:
        return str(self.data["unit"])

    @property
    def runtime(self) -> str:
        return str(self.data["runtime"])

    @property
    def task(self) -> str:
        return str(self.data["task"])

    @property
    def model_id(self) -> str:
        return str(self.data["modelId"])

    @property
    def label(self) -> str:
        return str(self.data["label"])

    @property
    def aliases(self) -> list[str]:
        return [str(alias) for alias in self.data.get("aliases", [])]

    @property
    def hardware_tier(self) -> str:
        return str(self.data["hardwareTier"])

    @property
    def disk_mb(self) -> int:
        return int(self.data["diskMB"])

    @property
    def vram_mb(self) -> int:
        return int(self.data["vramMB"])

    @property
    def npu_eligible(self) -> bool:
        return bool(self.data.get("npuEligible", False))

    @property
    def cpu_fallback(self) -> bool:
        return supports_cpu_fallback(self.data)

    @property
    def supports_reasoning(self) -> bool:
        return supports_reasoning(self.data)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.data)


@lru_cache(maxsize=2)
def load_catalog(mode: str | None = None) -> dict[str, Any]:
    resolved_mode = normalize_mode(mode) if mode is not None else "web"
    if resolved_mode == "native":
        return load_native_catalog()
    return load_web_catalog()


@lru_cache(maxsize=1)
def load_web_catalog() -> dict[str, Any]:
    root = repo_root_from_here()
    if root is not None:
        path = root / "packages" / "catalog" / "models.json"
        return json.loads(path.read_text(encoding="utf-8"))
    data = resources.files("xlocllm.data").joinpath("models.json").read_text(encoding="utf-8")
    return json.loads(data)


@lru_cache(maxsize=1)
def load_native_catalog() -> dict[str, Any]:
    root = repo_root_from_here()
    if root is not None:
        path = root / "packages" / "catalog" / "native-models.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    try:
        data = resources.files("xlocllm.data").joinpath("native_models.json").read_text(encoding="utf-8")
        return json.loads(data)
    except FileNotFoundError:
        return build_native_catalog()


def build_native_catalog() -> dict[str, Any]:
    web_catalog = load_web_catalog()
    result: dict[str, Any] = {
        "schemaVersion": 3,
        "mode": "native",
        "units": list(web_catalog["units"]),
        "models": [],
    }
    result["models"].extend(dict(item) for item in NATIVE_LLM_MODELS)
    for unit in result["units"]:
        unit_type = str(unit["type"])
        if unit_type == "LLM":
            continue
        candidates = [
            candidate
            for candidate in web_catalog["models"]
            if candidate.get("unit") == unit_type
            and candidate.get("runtime") == "transformers"
            and candidate.get("availability") != "unsupported"
        ]
        selected = prioritized_native_candidates(unit_type, candidates)
        for candidate in selected:
            result["models"].append(native_onnx_model(candidate))
    return result


def prioritized_native_candidates(unit_type: str, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for alias in NATIVE_PRIORITY_ALIASES.get(unit_type, []):
        normalized = _normalize(alias)
        match = next(
            (
                candidate
                for candidate in candidates
                if normalized
                in {
                    _normalize(str(candidate.get("modelId", ""))),
                    _normalize(str(candidate.get("label", ""))),
                    *[_normalize(str(item)) for item in candidate.get("aliases", [])],
                }
            ),
            None,
        )
        if match is not None and match not in selected:
            selected.append(match)
    for candidate in sorted(candidates, key=_model_weight):
        if candidate not in selected:
            selected.append(candidate)
        if len(selected) >= NATIVE_MODELS_PER_UNIT:
            break
    return selected[:NATIVE_MODELS_PER_UNIT]


def all_models(mode: str | None = None) -> list[dict[str, Any]]:
    return list(load_catalog(mode or current_mode())["models"])


def all_units(mode: str | None = None) -> list[dict[str, Any]]:
    return list(load_catalog(mode or current_mode())["units"])


def native_onnx_model(candidate: dict[str, Any]) -> dict[str, Any]:
    item = dict(candidate)
    item["runtime"] = "native"
    item["backend"] = "onnxruntime"
    item["format"] = "onnx"
    item["backendModelId"] = candidate.get("backendModelId") or candidate.get("modelId")
    item["repo"] = candidate.get("backendModelId") or candidate.get("modelId")
    item["providers"] = ["cuda", "directml", "coreml", "cpu"]
    item["verified"] = candidate.get("availability") == "verified"
    item["availability"] = "verified" if item["verified"] else candidate.get("availability", "candidate")
    item["notes"] = str(candidate.get("notes") or "Native ONNX Runtime pipeline candidate.")
    item["tags"] = sorted({*[str(tag) for tag in candidate.get("tags", [])], "native", "onnxruntime"})
    return item


def supports_cpu_fallback(candidate: dict[str, Any]) -> bool:
    if candidate.get("runtime") == "native":
        return True
    if candidate.get("runtime") != "transformers":
        return False
    if candidate.get("availability") == "unsupported":
        return False
    if str(candidate.get("hardwareTier", "")).lower() in CPU_FALLBACK_TIERS:
        return True
    return (
        int(candidate.get("vramMB") or 0) <= CPU_FALLBACK_MAX_VRAM_MB
        and int(candidate.get("diskMB") or 0) <= CPU_FALLBACK_MAX_DISK_MB
    )


def supports_reasoning(candidate: dict[str, Any]) -> bool:
    if candidate.get("unit") != "LLM":
        return False
    haystack = " ".join(
        [
            str(candidate.get("modelId", "")),
            str(candidate.get("label", "")),
            str(candidate.get("notes", "")),
            *[str(alias) for alias in candidate.get("aliases", [])],
            *[str(tag) for tag in candidate.get("tags", [])],
        ]
    ).lower()
    return any(marker in haystack for marker in ("qwen3", "qwen3.5", "qwen3_5", "deepseek-r1", "gpt-oss", "qwq"))


def cpu_fallback_model_ids(*, min_per_unit: int = 2, mode: str | None = None) -> set[str]:
    resolved_mode = current_mode(mode)
    catalog_models = all_models(mode=resolved_mode)
    result = {str(candidate["modelId"]) for candidate in catalog_models if supports_cpu_fallback(candidate)}
    for unit in all_units(mode=resolved_mode):
        unit_type = str(unit["type"])
        available = [candidate for candidate in catalog_models if candidate["unit"] == unit_type]
        if len([candidate for candidate in available if str(candidate["modelId"]) in result]) >= min_per_unit:
            continue
        fallback = sorted(
            [
                candidate
                for candidate in available
                if candidate.get("runtime") == "transformers" and candidate.get("availability") != "unsupported"
            ],
            key=_model_weight,
        )[:min_per_unit]
        result.update(str(candidate["modelId"]) for candidate in fallback)
    return result


def resolve_model(
    unit_type: str,
    model_name: str,
    *,
    mode: str | None = None,
    quant: str | None = None,
) -> dict[str, Any]:
    resolved_mode = current_mode(mode)
    normalized_unit = normalize_unit(unit_type)
    normalized_model = _normalize(model_name)
    for model in all_models(mode=resolved_mode):
        if model["unit"] != normalized_unit:
            continue
        aliases = [_normalize(alias) for alias in model.get("aliases", [])]
        if normalized_model in {
            _normalize(model["modelId"]),
            _normalize(model["label"]),
            *aliases,
        }:
            return select_quantization(model, quant=quant) if resolved_mode == "native" else model
    raise ModelNotFound(f"Model not found for unit={unit_type!r} model={model_name!r} mode={resolved_mode!r}")


def model(
    name: str,
    unit: str | None = None,
    *,
    mode: str | None = None,
    quant: str | None = None,
) -> ModelInfo:
    resolved_mode = current_mode(mode)
    if unit is not None:
        return ModelInfo(resolve_model(unit, name, mode=resolved_mode, quant=quant))
    normalized_model = _normalize(name)
    for candidate in all_models(mode=resolved_mode):
        aliases = [_normalize(alias) for alias in candidate.get("aliases", [])]
        if normalized_model in {
            _normalize(candidate["modelId"]),
            _normalize(candidate["label"]),
            *aliases,
        }:
            return ModelInfo(select_quantization(candidate, quant=quant) if resolved_mode == "native" else candidate)
    raise ModelNotFound(f"Model not found: {name!r} mode={resolved_mode!r}")


def select_quantization(candidate: dict[str, Any], *, quant: str | None = None) -> dict[str, Any]:
    if candidate.get("format") != "gguf":
        return dict(candidate)
    quantizations = candidate.get("quantizations")
    if not isinstance(quantizations, dict):
        return dict(candidate)
    selected = normalize_quantization(quant or str(candidate.get("defaultQuantization") or DEFAULT_GGUF_QUANT))
    if selected not in quantizations:
        available = ", ".join(sorted(str(key) for key in quantizations))
        raise ModelNotFound(
            f"Quantization {quant!r} is not declared for {candidate.get('modelId')!r}. Available: {available}"
        )
    result = dict(candidate)
    result["selectedQuantization"] = selected
    result["requestedQuantization"] = normalize_quantization(quant) if quant else None
    result["files"] = [str(item) for item in quantizations[selected]]
    return result


def models(
    *,
    unit: str | None = None,
    mode: str | None = None,
    runtime: str | None = None,
    task: str | None = None,
    task_group: str | None = None,
    hardware_tier: str | None = None,
    language: str | None = None,
    provider: str | None = None,
    availability: str | None = None,
    npu: bool | None = None,
    webgpu: bool | None = None,
    cpu: bool | None = None,
    available_without_webgpu: bool | None = None,
    installed: bool | None = None,
    hardware: str | None = None,
    include_unavailable: bool = False,
    quant: str | None = None,
    subtype: str | None = None,
    modality: str | None = None,
    use_case: str | None = None,
    license: str | None = None,  # noqa: A002
    min_context: int | None = None,
    search: str | None = None,
    max_vram_mb: int | None = None,
    max_disk_mb: int | None = None,
    max_size_gb: float | None = None,
    max_parameters_b: float | None = None,
    limit_per_unit: int | None = None,
) -> list[ModelInfo]:
    resolved_mode = current_mode(mode)
    normalized_unit = normalize_unit(unit) if unit is not None else None
    normalized_search = _normalize(search) if search else None
    normalized_subtype = _normalize(subtype) if subtype else None
    normalized_modality = _normalize(modality) if modality else None
    normalized_use_case = _normalize(use_case) if use_case else None
    normalized_license = _normalize(license) if license else None
    require_cpu_fallback = (webgpu is False) or (cpu is True) or (available_without_webgpu is True)
    cpu_model_ids = cpu_fallback_model_ids(mode=resolved_mode) if require_cpu_fallback else set()
    normalized_hardware = _normalize(hardware) if hardware else None
    result: list[ModelInfo] = []
    for candidate in all_models(mode=resolved_mode):
        if normalized_unit is not None and candidate["unit"] != normalized_unit:
            continue
        if not include_unavailable and candidate.get("availability") == "unsupported":
            continue
        if installed is not None and _model_cache_exists(candidate, mode=resolved_mode) is not installed:
            continue
        if require_cpu_fallback and str(candidate["modelId"]) not in cpu_model_ids:
            continue
        if runtime is not None and _normalize(candidate["runtime"]) != _normalize(runtime):
            continue
        if normalized_hardware is not None and normalized_hardware not in {
            _normalize(str(provider)) for provider in candidate.get("providers", [])
        }:
            continue
        if task is not None and _normalize(candidate["task"]) != _normalize(task):
            continue
        if task_group is not None and _normalize(candidate["taskGroup"]) != _normalize(task_group):
            continue
        if hardware_tier is not None and _normalize(candidate["hardwareTier"]) != _normalize(hardware_tier):
            continue
        if language is not None and _normalize(language) not in {
            _normalize(str(value)) for value in candidate.get("languages", [])
        }:
            continue
        if provider is not None and _normalize(candidate["provider"]) != _normalize(provider):
            continue
        if availability is not None and _normalize(candidate.get("availability", "")) != _normalize(availability):
            continue
        if normalized_subtype is not None and _normalize(str(candidate.get("subtype", ""))) != normalized_subtype:
            continue
        if normalized_modality is not None and normalized_modality not in {
            _normalize(str(value)) for value in candidate.get("modalities", [])
        }:
            continue
        if normalized_use_case is not None and normalized_use_case not in {
            _normalize(str(value)) for value in candidate.get("useCases", [])
        }:
            continue
        if normalized_license is not None and _normalize(str(candidate.get("license", ""))) != normalized_license:
            continue
        context_length = candidate.get("contextLength")
        if min_context is not None and (not isinstance(context_length, int | float) or int(context_length) < min_context):
            continue
        if npu is not None and bool(candidate.get("npuEligible", False)) is not npu:
            continue
        if max_vram_mb is not None and int(candidate["vramMB"]) > max_vram_mb:
            continue
        if max_disk_mb is not None and int(candidate["diskMB"]) > max_disk_mb:
            continue
        if max_size_gb is not None and float(candidate["modelSizeGb"]) > max_size_gb:
            continue
        parameter_b = candidate.get("parameterB")
        if (
            max_parameters_b is not None
            and isinstance(parameter_b, int | float)
            and float(parameter_b) > max_parameters_b
        ):
            continue
        if normalized_search is not None:
            haystack = " ".join(
                [
                    str(candidate["modelId"]),
                    str(candidate["label"]),
                    str(candidate["provider"]),
                    str(candidate["unit"]),
                    str(candidate["taskGroup"]),
                    *[str(alias) for alias in candidate.get("aliases", [])],
                    *[str(tag) for tag in candidate.get("tags", [])],
                ]
            )
            if normalized_search not in _normalize(haystack):
                continue
        result_candidate = select_quantization(candidate, quant=quant) if resolved_mode == "native" else candidate
        result.append(ModelInfo(result_candidate))
    if limit_per_unit is not None:
        result = _limit_models_per_unit(result, limit_per_unit)
    return result


def _model_cache_exists(candidate: dict[str, Any], *, mode: str) -> bool:
    if mode != "native":
        return False
    repo = str(candidate.get("repo") or candidate.get("backendModelId") or candidate.get("modelId") or "")
    if not repo:
        return False
    from ._paths import native_model_dir

    hf_cache_name = "models--" + repo.replace("/", "--")
    return (native_model_dir() / hf_cache_name).exists()


def normalize_unit(unit_type: str) -> str:
    value = _normalize(unit_type)
    aliases = {
        "embeddings": "embedding",
        "translation": "translator",
        "image-to-text": "vlm",
        "background-removing": "image-segmentation",
        "segmentation": "image-segmentation",
        "zero-shot-image-classification": "zero-shot-image",
        "language-identification": "language-id",
        "speech-to-text": "asr",
        "text-generation": "LLM",
        "chat": "LLM",
        "text2text-generation": "text2text",
        "text-to-text": "text2text",
        "text-ranking": "reranker",
    }
    if value in aliases:
        return aliases[value]
    for unit in all_units():
        if _normalize(unit["type"]) == value or _normalize(unit["label"]) == value:
            return str(unit["type"])
    raise UnitNotFound(f"Unknown xlocllm unit type: {unit_type!r}")


def normalize_quantization(value: str | None) -> str:
    normalized = _normalize(value or DEFAULT_GGUF_QUANT).replace("-", "")
    aliases = {
        "2": "q2",
        "q2k": "q2",
        "q2": "q2",
        "3": "q3",
        "q3k": "q3",
        "q3km": "q3",
        "q3": "q3",
        "4": "q4",
        "q4k": "q4",
        "q4km": "q4",
        "q4": "q4",
        "5": "q5",
        "q5k": "q5",
        "q5km": "q5",
        "q5": "q5",
        "6": "q6",
        "q6k": "q6",
        "q6": "q6",
        "8": "q8",
        "q80": "q8",
        "q8": "q8",
        "f16": "fp16",
        "float16": "fp16",
        "fp16": "fp16",
        "f32": "fp32",
        "float32": "fp32",
        "fp32": "fp32",
    }
    if normalized not in aliases:
        available = ", ".join(GGUF_QUANTIZATION_PATTERNS)
        raise ValueError(f"Unknown quantization {value!r}. Use one of: {available}")
    return aliases[normalized]


def catalog_path() -> Path:
    root = repo_root_from_here()
    if root is None:
        raise FileNotFoundError("Cannot find repository root")
    return root / "packages" / "catalog" / "models.json"


def _normalize(value: str) -> str:
    return "-".join(value.strip().lower().replace("_", "-").split())


def _model_weight(candidate: dict[str, Any]) -> tuple[int, int, int, float]:
    tier_order = {"tiny": 0, "small": 1, "medium": 2, "large": 3}
    return (
        tier_order.get(str(candidate.get("hardwareTier", "")).lower(), 99),
        int(candidate.get("vramMB") or 0),
        int(candidate.get("diskMB") or 0),
        float(candidate.get("parameterB") or 0),
    )


def _limit_models_per_unit(items: list[ModelInfo], limit: int) -> list[ModelInfo]:
    if limit <= 0:
        return []
    counts: dict[str, int] = {}
    result: list[ModelInfo] = []
    for item in items:
        current = counts.get(item.unit, 0)
        if current >= limit:
            continue
        counts[item.unit] = current + 1
        result.append(item)
    return result
