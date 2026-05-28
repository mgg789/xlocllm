from pathlib import Path

import pytest

import xlocllm


def test_vectorstorage_payload() -> None:
    store = xlocllm.vectorstorage(name="docs", namespace="kb", metric="dot", persist=False)

    assert store.type == "vectorstorage"
    assert store.model == "docs"
    assert store.to_payload() == {
        "type": "vectorstorage",
        "model": "docs",
        "options": {
            "backend": "native",
            "metric": "dot",
            "persist": False,
            "namespace": "kb",
        },
    }


def test_rag_payload_and_llm_attachment() -> None:
    emb = xlocllm.unit("embedding", "multilingual-e5-small")
    store = xlocllm.vectorstorage(name="docs")
    rag = xlocllm.rag(emb=emb, store=store, name="kb", chunk_size=400, top_k=3)
    llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", rag=rag)

    payload = llm.to_payload()

    assert payload["rag"]["type"] == "RAG"
    assert payload["rag"]["model"] == "kb"
    assert payload["rag"]["options"]["emb"]["type"] == "embedding"
    assert payload["rag"]["options"]["store"]["type"] == "vectorstorage"
    assert payload["rag"]["options"]["chunk_size"] == 400
    assert payload["rag"]["options"]["top_k"] == 3


def test_rag_methods_require_runtime() -> None:
    emb = xlocllm.unit("embedding", "multilingual-e5-small")
    rag = xlocllm.rag(emb=emb)

    with pytest.raises(RuntimeError, match="not attached"):
        rag.search("hello")


def test_onnx_service_unit_payload_and_predict_guard() -> None:
    regression = xlocllm.unit(
        "regression",
        "demo-regressor",
        options={"model_path": "model.onnx", "input_name": "float_input"},
    )

    assert regression.type == "onnx"
    assert regression.to_payload()["options"]["model_path"] == "model.onnx"
    with pytest.raises(RuntimeError, match="not attached"):
        regression.predict([[1.0, 2.0]])


def test_modelinfo_unit_and_custom_onnx_path_payload(tmp_path: Path) -> None:
    info = xlocllm.model("Qwen-3.5-0.8b", unit="LLM")
    llm = xlocllm.unit(info)
    onnx_path = tmp_path / "classifier.onnx"
    onnx_path.write_bytes(b"fake")
    classifier = xlocllm.unit(
        onnx_path,
        type="text-classification",
        name="demo-classifier",
        labels=["negative", "positive"],
    )

    assert llm.model == info.model_id
    assert classifier.type == "text-classification"
    assert classifier.to_payload()["options"]["custom"] is True
    assert classifier.to_payload()["options"]["labels"] == ["negative", "positive"]
    with pytest.raises(RuntimeError, match="not attached"):
        classifier.predict([[0.1, 0.9]])


def test_runtime_attaches_nested_rag() -> None:
    emb = xlocllm.unit("embedding", "multilingual-e5-small")
    rag = xlocllm.rag(emb=emb)
    llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", rag=rag)
    rt = xlocllm.runtime([llm])

    assert rag._runtime is rt
    assert rt.units(as_dict=True)[0]["rag"]["type"] == "RAG"
