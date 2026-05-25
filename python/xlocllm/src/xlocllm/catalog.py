from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any

from ._paths import repo_root_from_here
from .exceptions import ModelNotFound, UnitNotFound

CPU_FALLBACK_TIERS = {"tiny", "small"}
CPU_FALLBACK_MAX_VRAM_MB = 1500
CPU_FALLBACK_MAX_DISK_MB = 1600


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


@lru_cache(maxsize=1)
def load_catalog() -> dict[str, Any]:
    root = repo_root_from_here()
    if root is not None:
        path = root / "packages" / "catalog" / "models.json"
        return json.loads(path.read_text(encoding="utf-8"))
    data = resources.files("xlocllm.data").joinpath("models.json").read_text(encoding="utf-8")
    return json.loads(data)


def all_models() -> list[dict[str, Any]]:
    return list(load_catalog()["models"])


def all_units() -> list[dict[str, Any]]:
    return list(load_catalog()["units"])


def supports_cpu_fallback(candidate: dict[str, Any]) -> bool:
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


def cpu_fallback_model_ids(*, min_per_unit: int = 2) -> set[str]:
    result = {str(candidate["modelId"]) for candidate in all_models() if supports_cpu_fallback(candidate)}
    for unit in all_units():
        unit_type = str(unit["type"])
        available = [candidate for candidate in all_models() if candidate["unit"] == unit_type]
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


def resolve_model(unit_type: str, model_name: str) -> dict[str, Any]:
    normalized_unit = normalize_unit(unit_type)
    normalized_model = _normalize(model_name)
    for model in all_models():
        if model["unit"] != normalized_unit:
            continue
        aliases = [_normalize(alias) for alias in model.get("aliases", [])]
        if normalized_model in {
            _normalize(model["modelId"]),
            _normalize(model["label"]),
            *aliases,
        }:
            return model
    raise ModelNotFound(f"Model not found for unit={unit_type!r} model={model_name!r}")


def model(name: str, unit: str | None = None) -> ModelInfo:
    if unit is not None:
        return ModelInfo(resolve_model(unit, name))
    normalized_model = _normalize(name)
    for candidate in all_models():
        aliases = [_normalize(alias) for alias in candidate.get("aliases", [])]
        if normalized_model in {
            _normalize(candidate["modelId"]),
            _normalize(candidate["label"]),
            *aliases,
        }:
            return ModelInfo(candidate)
    raise ModelNotFound(f"Model not found: {name!r}")


def models(
    *,
    unit: str | None = None,
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
    search: str | None = None,
    max_vram_mb: int | None = None,
    max_disk_mb: int | None = None,
    max_size_gb: float | None = None,
    max_parameters_b: float | None = None,
    limit_per_unit: int | None = None,
) -> list[ModelInfo]:
    normalized_unit = normalize_unit(unit) if unit is not None else None
    normalized_search = _normalize(search) if search else None
    require_cpu_fallback = (webgpu is False) or (cpu is True) or (available_without_webgpu is True)
    cpu_model_ids = cpu_fallback_model_ids() if require_cpu_fallback else set()
    result: list[ModelInfo] = []
    for candidate in all_models():
        if normalized_unit is not None and candidate["unit"] != normalized_unit:
            continue
        if require_cpu_fallback and str(candidate["modelId"]) not in cpu_model_ids:
            continue
        if runtime is not None and _normalize(candidate["runtime"]) != _normalize(runtime):
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
        result.append(ModelInfo(candidate))
    if limit_per_unit is not None:
        result = _limit_models_per_unit(result, limit_per_unit)
    return result


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
