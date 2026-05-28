from pathlib import Path

import pytest

import xlocllm
from xlocllm.catalog import all_units, model, models, normalize_unit, resolve_model


def test_resolve_aliases() -> None:
    llm = resolve_model("LLM", "Qwen-3.5-0.8b")
    llm_full = resolve_model("LLM", "Qwen-3.5-0.8b-full")
    embedding = resolve_model("embedding", "multilingual-e5-small")
    web_llm = resolve_model("LLM", "Qwen-3.5-0.8b", mode="web")

    assert llm["runtime"] == "native"
    assert llm["backend"] == "llama.cpp"
    assert llm_full["modelId"] == llm["modelId"]
    assert embedding["modelId"] == "Xenova/multilingual-e5-small"
    assert web_llm["modelId"] == "Qwen3.5-0.8B-q4f16_1-MLC"


def test_normalize_units() -> None:
    assert normalize_unit("Embeddings") == "embedding"
    assert normalize_unit("image-to-text") == "vlm"


def test_unit_and_runtime_shape() -> None:
    runtime = xlocllm.runtime(
        [
            xlocllm.unit(type="LLM", model="Qwen-3.5-0.8b"),
            xlocllm.unit(type="embedding", model="multilingual-e5-small"),
        ],
        port=1234,
    )

    assert runtime.url == "http://127.0.0.1:1234/v1"
    assert runtime.mode == "native"
    assert [unit.type for unit in runtime.units()] == ["LLM", "embedding"]
    assert runtime.units(as_dict=True)[0]["model"] == "Qwen3-0.6B-GGUF"
    assert runtime.units(as_dict=True)[0]["quant"] == "q4"


def test_web_mode_preserves_browser_catalog_shape() -> None:
    llm = xlocllm.unit(type="LLM", model="Qwen-3.5-0.8b", mode="web")
    runtime = xlocllm.runtime([llm], mode="web")

    assert llm.mode == "web"
    assert runtime.mode == "web"
    assert runtime.units(as_dict=True)[0]["model"] == "Qwen3.5-0.8B-q4f16_1-MLC"


def test_runtime_add_remove_unit_offline() -> None:
    runtime = xlocllm.runtime([xlocllm.unit(type="LLM", model="Qwen-3.5-0.8b")])
    embedding = runtime.add_unit(xlocllm.unit(type="embedding", model="multilingual-e5-small"))

    assert [unit.type for unit in runtime.units()] == ["LLM", "embedding"]

    result = runtime.remove_unit(embedding.id)

    assert result["ok"] is True
    assert [unit.type for unit in runtime.units()] == ["LLM"]


def test_runtime_context_manager_offline() -> None:
    runtime = xlocllm.runtime([xlocllm.unit(type="LLM", model="Qwen-3.5-0.8b")])

    with runtime as active:
        assert active is runtime


def test_no_webgpu_catalog_keeps_at_least_one_model_per_unit() -> None:
    units = {item["type"] for item in all_units(mode="web")}
    fallback_models = models(mode="web", webgpu=False)
    fallback_units = {item.unit for item in fallback_models}

    assert units <= fallback_units
    assert all(item.runtime == "transformers" for item in fallback_models)


def test_reasoning_unit_option_and_hot_update_offline() -> None:
    llm = xlocllm.unit(type="LLM", model="Qwen-3.5-0.8b-fp32", reasoning=False)
    runtime = xlocllm.runtime([llm])

    assert llm.supports_reasoning is True
    assert llm.to_payload()["reasoning"] is False

    result = runtime.set_reasoning(llm.id, True)

    assert result["ok"] is True
    assert result["updated"]["reasoning"] is True


def test_reasoning_rejected_for_models_without_control() -> None:
    with pytest.raises(ValueError):
        xlocllm.unit(type="embedding", model="multilingual-e5-small", reasoning=False)


def test_model_helpers_return_typed_catalog_items() -> None:
    qwen = model("Qwen-3.5-0.8b", unit="LLM")
    small_llms = models(unit="LLM", max_vram_mb=1500)
    web_qwen = model("Qwen-3.5-0.8b", unit="LLM", mode="web")

    assert qwen.model_id == "Qwen3-0.6B-GGUF"
    assert web_qwen.model_id == "Qwen3.5-0.8B-q4f16_1-MLC"
    assert all(item.unit == "LLM" for item in small_llms)
    assert any(item.model_id == qwen.model_id for item in small_llms)


def test_native_quant_parameter_selects_files_without_changing_model_id() -> None:
    q4 = xlocllm.unit(type="LLM", model="Qwen-3.5-0.8b")
    q8 = xlocllm.unit(type="LLM", model="Qwen-3.5-0.8b", quant="q8")

    assert q4.model == q8.model == "Qwen3-0.6B-GGUF"
    assert q4.quant == "q4"
    assert q8.quant == "q8"
    assert "Q8" in q8.model_info.to_dict()["files"][0]


def test_native_installed_filter_uses_xlocllm_cache(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("XLOCLLM_HOME", str(tmp_path))

    qwen = model("Qwen-3.5-0.8b", unit="LLM", mode="native")
    assert models(unit="LLM", mode="native", installed=True) == []

    cache_dir = tmp_path / "native" / "models" / "models--Qwen--Qwen3-0.6B-GGUF"
    cache_dir.mkdir(parents=True)

    installed = models(unit="LLM", mode="native", installed=True)
    assert any(item.model_id == qwen.model_id for item in installed)


def test_top_level_status_is_dict() -> None:
    snapshot = xlocllm.status()

    assert "bridges" in snapshot
    assert "runtimes" in snapshot
    assert snapshot["models"]["catalog_count"] > 0


def test_benchmark_without_browser_probe() -> None:
    snapshot = xlocllm.benchmark(ping_hf=False, browser=False)

    assert snapshot["ok"] is True
    assert snapshot["network"]["huggingface"]["checked"] is False
    assert snapshot["mode"] == "native"
    assert snapshot["browser"]["status"] == "skipped"
    assert "hardware" in snapshot["native"]


def test_benchmark_recommends_models_for_type_without_browser_probe() -> None:
    snapshot = xlocllm.benchmark("LLM", ping_hf=False, browser=False)

    assert snapshot["model_type"] == "LLM"
    assert snapshot["recommendations"]["fast"]["unit"] == "LLM"
    assert snapshot["recommendations"]["quality"]["unit"] == "LLM"
