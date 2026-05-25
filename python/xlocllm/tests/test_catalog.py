import xlocllm
from xlocllm.catalog import model, models, normalize_unit, resolve_model


def test_resolve_aliases() -> None:
    llm = resolve_model("LLM", "Qwen-3.5-0.8b")
    llm_full = resolve_model("LLM", "Qwen-3.5-0.8b-full")
    embedding = resolve_model("embedding", "multilingual-e5-small")

    assert llm["modelId"] == "Qwen3.5-0.8B-q4f16_1-MLC"
    assert llm_full["backendModelId"] == "onnx-community/Qwen3.5-0.8B-ONNX"
    assert llm_full["dtype"] == "fp32"
    assert embedding["modelId"] == "Xenova/multilingual-e5-small"


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
    assert [unit.type for unit in runtime.units()] == ["LLM", "embedding"]
    assert runtime.units(as_dict=True)[0]["model"] == "Qwen3.5-0.8B-q4f16_1-MLC"


def test_runtime_add_remove_unit_offline() -> None:
    runtime = xlocllm.runtime([xlocllm.unit(type="LLM", model="Qwen-3.5-0.8b")])
    embedding = runtime.add_unit(xlocllm.unit(type="embedding", model="multilingual-e5-small"))

    assert [unit.type for unit in runtime.units()] == ["LLM", "embedding"]

    result = runtime.remove_unit(embedding.id)

    assert result["ok"] is True
    assert [unit.type for unit in runtime.units()] == ["LLM"]


def test_model_helpers_return_typed_catalog_items() -> None:
    qwen = model("Qwen-3.5-0.8b", unit="LLM")
    small_llms = models(unit="LLM", max_vram_mb=1500)

    assert qwen.model_id == "Qwen3.5-0.8B-q4f16_1-MLC"
    assert all(item.unit == "LLM" for item in small_llms)
    assert any(item.model_id == qwen.model_id for item in small_llms)


def test_top_level_status_is_dict() -> None:
    snapshot = xlocllm.status()

    assert "bridges" in snapshot
    assert "runtimes" in snapshot
    assert snapshot["models"]["catalog_count"] > 0
