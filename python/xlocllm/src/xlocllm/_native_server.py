from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import time
import uuid
from collections.abc import AsyncIterator, Iterable, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse

from ._paths import native_engine_dir, native_model_dir, native_store_dir
from .catalog import (
    DEFAULT_GGUF_QUANT,
    GGUF_QUANT_FALLBACK_ORDER,
    all_models,
    all_units,
    normalize_quantization,
    resolve_model,
    supports_reasoning,
)
from .registry import remove_bridge, upsert_bridge


ENGINE_IMPORTS: dict[str, dict[str, str]] = {
    "llama.cpp": {
        "llama_cpp": "llama-cpp-python>=0.3.0",
        "huggingface_hub": "huggingface-hub>=0.23.0",
    },
    "onnxruntime": {
        "numpy": "numpy>=1.26.0",
        "huggingface_hub": "huggingface-hub>=0.23.0",
        "transformers": "transformers>=4.44.0",
        "optimum": "optimum[onnxruntime]>=1.20.0",
    },
}


@dataclass
class NativeInstance:
    model: dict[str, Any]
    active: bool = True
    installed: bool = False
    status: str = "selected"
    reasoning: bool | None = None
    options: dict[str, Any] = field(default_factory=dict)
    rag_id: str | None = None
    progress: int | None = None
    error: str | None = None
    engine: Any = None


@dataclass
class CustomOnnxUnit:
    name: str
    path: Path
    options: dict[str, Any] = field(default_factory=dict)
    active: bool = True
    status: str = "selected"
    error: str | None = None
    session: Any = None


@dataclass
class VectorRecord:
    id: str
    document_id: str
    chunk_index: int
    text: str
    metadata: dict[str, Any]
    embedding: list[float]
    embedding_model: str | None = None


@dataclass
class VectorStore:
    name: str
    metric: str = "cosine"
    persist: bool = True
    namespace: str = "default"
    records: list[VectorRecord] = field(default_factory=list)

    @property
    def path(self) -> Path:
        safe = "".join(char if char.isalnum() or char in {"-", "_"} else "-" for char in f"{self.namespace}-{self.name}")
        return native_store_dir() / f"{safe}.json"

    def load(self) -> None:
        if not self.persist or not self.path.exists():
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.records = [
            VectorRecord(
                id=str(item["id"]),
                document_id=str(item["document_id"]),
                chunk_index=int(item["chunk_index"]),
                text=str(item["text"]),
                metadata=dict(item.get("metadata") or {}),
                embedding=[float(value) for value in item.get("embedding", [])],
                embedding_model=str(item["embedding_model"]) if item.get("embedding_model") else None,
            )
            for item in raw.get("records", [])
            if isinstance(item, dict)
        ]

    def save(self) -> None:
        if not self.persist:
            return
        payload = {
            "name": self.name,
            "metric": self.metric,
            "namespace": self.namespace,
            "records": [record_to_dict(record) for record in self.records],
        }
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


@dataclass
class RagPipeline:
    name: str
    emb: dict[str, Any]
    store: VectorStore
    rerank: dict[str, Any] | None = None
    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 5
    candidate_k: int = 30
    score_threshold: float | None = None
    status: str = "ready"
    active: bool = True
    error: str | None = None


class NativeRuntime:
    def __init__(self, token: str) -> None:
        self.token = token
        self.started_at = time.time()
        self.instances: dict[str, NativeInstance] = {}
        self.vector_stores: dict[str, VectorStore] = {}
        self.rags: dict[str, RagPipeline] = {}
        self.custom_onnx: dict[str, CustomOnnxUnit] = {}
        self.logs: list[dict[str, Any]] = []
        self.installing = False
        self.install_progress = 0
        self.running = False
        self.requests = {"processing": 0, "queued": 0}
        ensure_native_import_path()

    def status(self) -> dict[str, Any]:
        catalog_models = all_models(mode="native")
        return {
            "ok": True,
            "connected": True,
            "backend": "native",
            "started_at": self.started_at,
            "units": self.unit_states(),
            "models": [self.model_state(instance) for instance in self.instances.values()],
            "services": self.service_states(),
            "logs": self.logs[-200:],
            "metrics": runtime_metrics(),
            "npu": native_npu_state(),
            "capabilities": native_capabilities(len(catalog_models)),
            "requests": dict(self.requests),
            "catalogModels": catalog_models,
            "catalogModelCount": len(catalog_models),
            "installProgress": self.install_progress,
            "installing": self.installing,
            "running": self.running,
        }

    def install(self, units: list[dict[str, Any]]) -> dict[str, Any]:
        model_units = self.configure_units(units)
        if not model_units:
            return self.status()
        self.installing = True
        self.install_progress = 0
        try:
            for index, request in enumerate(model_units):
                instance = self.ensure_instance(request)
                self.log("info", f"Installing native dependencies for {instance.model['label']}")
                instance.status = "installing"
                instance.progress = 0
                self.prepare_model(instance, install_only=True)
                instance.installed = True
                instance.status = "ready"
                instance.progress = 100
                self.install_progress = round(((index + 1) / len(model_units)) * 100)
            return self.status()
        finally:
            self.installing = False

    def run(self, units: list[dict[str, Any]]) -> dict[str, Any]:
        model_units = self.configure_units(units)
        if self.installing:
            raise RuntimeError("Runtime is installing models")
        for request in model_units:
            instance = self.ensure_instance(request)
            self.log("info", f"Starting {instance.model['label']} on native backend")
            try:
                self.prepare_model(instance, install_only=False)
                instance.active = True
                instance.installed = True
                instance.status = "running"
                instance.progress = 100
                instance.error = None
            except Exception as error:  # noqa: BLE001
                instance.status = "error"
                instance.error = str(error)
                self.log("error", f"{instance.model['label']} failed: {instance.error}")
                raise
        self.running = any(instance.status == "running" for instance in self.instances.values())
        return self.status()

    def stop(self) -> dict[str, Any]:
        for instance in self.instances.values():
            if instance.status == "running":
                instance.engine = None
                instance.status = "ready" if instance.installed else "selected"
        self.running = False
        self.log("info", "Native runtime stopped")
        return self.status()

    def hibernate(self) -> dict[str, Any]:
        for instance in self.instances.values():
            if instance.active:
                instance.engine = None
                instance.status = "hibernated"
        self.running = False
        self.log("info", "Native runtime hibernated")
        return self.status()

    def heatup(self) -> dict[str, Any]:
        units = [
            {"type": instance.model["unit"], "model": instance.model["modelId"], "reasoning": instance.reasoning, "options": instance.options}
            for instance in self.instances.values()
            if instance.active
        ]
        return self.run(units)

    def set_active(self, payload: dict[str, Any]) -> dict[str, Any]:
        unit = str(payload.get("unit") or "")
        model = str(payload.get("model") or "")
        active = bool(payload.get("active", True))
        instance = self.ensure_instance({"type": unit, "model": model})
        instance.active = active
        if not active and instance.status == "running":
            instance.engine = None
            instance.status = "ready" if instance.installed else "selected"
        self.running = any(item.status == "running" for item in self.instances.values())
        return self.status()

    def configure_unit(self, payload: dict[str, Any]) -> dict[str, Any]:
        request = payload.get("unit")
        if not isinstance(request, dict):
            raise RuntimeError("configure_unit requires a unit payload")
        unit_type = normalize_unit_type(str(request.get("type") or ""))
        if unit_type == "vectorstorage":
            self.configure_store_unit(request)
            return self.status()
        if unit_type == "rag":
            self.configure_rag_unit(request)
            return self.status()
        if unit_type == "onnx":
            self.configure_onnx_unit(request)
            return self.status()
        instance = self.ensure_instance(request)
        if "reasoning" in request:
            reasoning = request.get("reasoning")
            if reasoning is not None and not supports_reasoning(instance.model):
                raise RuntimeError(f"{instance.model['label']} does not advertise reasoning control")
            instance.reasoning = reasoning if isinstance(reasoning, bool) else None
        if isinstance(request.get("options"), dict):
            instance.options.update(request["options"])
        rag_payload = request.get("rag") or instance.options.get("rag")
        if isinstance(rag_payload, dict):
            instance.rag_id = self.configure_rag_unit(rag_payload).name
        return self.status()

    def delete_model(self, payload: dict[str, Any]) -> dict[str, Any]:
        unit = str(payload.get("unit") or "")
        model = str(payload.get("model") or unit)
        deleted: list[str] = []
        try:
            resolved = resolve_model(unit, model, mode="native")
            instance = self.instances.pop(str(resolved["modelId"]), None)
            if instance is not None:
                instance.engine = None
            deleted = delete_native_model_cache(resolved)
        except Exception:
            instance = self.instances.pop(model, None)
            if instance is not None:
                instance.engine = None
        self.running = any(instance.status == "running" for instance in self.instances.values())
        result = self.status()
        result["deleted"] = deleted
        return result

    def delete_all_models(self) -> dict[str, Any]:
        for instance in self.instances.values():
            instance.engine = None
            instance.installed = False
            instance.status = "selected"
        self.running = False
        deleted = clear_native_model_cache()
        result = self.status()
        result["deleted"] = deleted
        return result

    def infer(self, endpoint: str, payload: dict[str, Any]) -> Any:
        route = normalize_endpoint(endpoint)
        self.requests["processing"] += 1
        try:
            if route in {"chat.completions", "chat"}:
                return self.chat(payload)
            if route == "responses":
                return self.chat({"messages": normalize_responses_input(payload), **payload})
            if route in {"embeddings", "embedding"}:
                return self.embeddings(payload)
            if route in {"rerank", "reranker"}:
                return self.rerank(payload)
            if route in {"vector.add", "vector.search", "vector.delete", "vector.clear", "vector.stats"}:
                return self.vector_endpoint(route, payload)
            if route in {"rag.add", "rag.search", "rag.delete", "rag.clear", "rag.reindex", "rag.stats"}:
                return self.rag_endpoint(route, payload)
            if route in {"onnx", "onnx.predict", "regression", "regression.predict"}:
                return self.onnx_predict(payload)
            return self.generic_pipeline(route, payload)
        finally:
            self.requests["processing"] = max(0, self.requests["processing"] - 1)

    async def stream_chat(self, payload: dict[str, Any]) -> AsyncIterator[str]:
        instance = self.instance_for_unit("LLM", payload.get("model"))
        self.ensure_llm_loaded(instance)
        messages = self.messages_for_chat(instance, payload)
        kwargs = chat_kwargs(payload)
        stream = instance.engine.create_chat_completion(messages=messages, stream=True, **kwargs)
        for chunk in stream:
            delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
            if delta:
                yield str(delta)
            await asyncio.sleep(0)

    def chat(self, payload: dict[str, Any]) -> dict[str, Any]:
        instance = self.instance_for_unit("LLM", payload.get("model"))
        self.ensure_llm_loaded(instance)
        rag_context = self.rag_context_for_chat(instance, payload)
        messages = self.messages_for_chat(instance, payload, rag_context=rag_context)
        result = instance.engine.create_chat_completion(messages=messages, stream=False, **chat_kwargs(payload))
        content = extract_content(result)
        return {
            "content": content,
            "raw": {**result, **({"rag": rag_context} if rag_context else {})},
            **({"rag": rag_context} if rag_context else {}),
        }

    def embeddings(self, payload: dict[str, Any]) -> dict[str, Any]:
        instance = self.instance_for_unit("embedding", payload.get("model"))
        pipe = self.ensure_pipeline_loaded(instance)
        inputs = payload.get("input")
        texts = [str(item) for item in inputs] if isinstance(inputs, list) else [str(inputs or "")]
        vectors = []
        for text in texts:
            output = pipe(text, **dict(payload.get("options") or {}))
            vectors.append(normalize_embedding_output(output))
        return {"embeddings": vectors}

    def rerank(self, payload: dict[str, Any]) -> dict[str, Any]:
        instance = self.instance_for_unit("reranker", payload.get("model"))
        pipe = self.ensure_pipeline_loaded(instance)
        query = str(payload.get("query") or "")
        documents = [str(item) for item in payload.get("documents") or []]
        results = []
        for index, document in enumerate(documents):
            output = pipe({"text": query, "text_pair": document})
            score = extract_score(output)
            results.append({"index": index, "document": document, "score": score, "raw": output})
        return {"results": sorted(results, key=lambda item: float(item["score"]), reverse=True)}

    def generic_pipeline(self, route: str, payload: dict[str, Any]) -> Any:
        unit = unit_for_endpoint(route)
        instance = self.instance_for_unit(unit, payload.get("model"))
        pipe = self.ensure_pipeline_loaded(instance)
        input_value = payload_input(payload)
        options = dict(payload.get("options") or {})
        if route in {"zero-shot-text", "zero-shot-classification", "zero.shot.text"}:
            options["candidate_labels"] = payload.get("labels") or payload.get("candidate_labels")
        return pipe(input_value, **options)

    def onnx_predict(self, payload: dict[str, Any]) -> dict[str, Any]:
        unit = self.onnx_from_payload(payload)
        session = self.ensure_custom_onnx_loaded(unit)
        try:
            import numpy as np
        except ImportError as error:
            raise RuntimeError(native_dependency_error("numpy", {"modelId": unit.name})) from error

        raw_inputs = payload.get("inputs", payload.get("input", payload.get("data")))
        if isinstance(raw_inputs, dict):
            feeds = {str(key): np.asarray(value, dtype=np.float32) for key, value in raw_inputs.items()}
        else:
            array = np.asarray(raw_inputs, dtype=np.float32)
            if array.ndim == 1:
                array = array.reshape(1, -1)
            input_name = str(unit.options.get("input_name") or session.get_inputs()[0].name)
            feeds = {input_name: array}

        raw_output_names = payload.get("output_names") or unit.options.get("output_names")
        output_names = [str(item) for item in raw_output_names] if isinstance(raw_output_names, list) else None
        outputs = session.run(output_names, feeds)
        public_outputs = [output.tolist() if hasattr(output, "tolist") else output for output in outputs]
        return {
            "ok": True,
            "model": unit.name,
            "outputs": public_outputs,
            "prediction": public_outputs[0] if public_outputs else None,
        }

    def vector_endpoint(self, route: str, payload: dict[str, Any]) -> dict[str, Any]:
        store = self.store_from_payload(payload)
        if route == "vector.add":
            records = vector_records_from_payload(payload)
            store.records.extend(records)
            store.save()
            return {"ok": True, "added": len(records), "stats": store_stats(store)}
        if route == "vector.search":
            vector = payload.get("embedding") or payload.get("vector")
            if not isinstance(vector, list):
                raise RuntimeError("vector.search requires embedding/vector")
            results = search_store(store, [float(value) for value in vector], int(payload.get("top_k") or 5))
            return {"ok": True, "results": [public_record(record, score) for record, score in results]}
        if route == "vector.delete":
            ids = set(string_list(payload.get("ids")))
            before = len(store.records)
            store.records = [record for record in store.records if record.id not in ids and record.document_id not in ids]
            store.save()
            return {"ok": True, "deleted": before - len(store.records), "stats": store_stats(store)}
        if route == "vector.clear":
            count = len(store.records)
            store.records = []
            store.save()
            return {"ok": True, "deleted": count, "stats": store_stats(store)}
        return {"ok": True, **store_stats(store)}

    def rag_endpoint(self, route: str, payload: dict[str, Any]) -> dict[str, Any]:
        rag = self.rag_from_payload(payload)
        if route == "rag.add":
            documents = rag_documents(payload)
            records: list[VectorRecord] = []
            for document in documents:
                chunks = chunk_text(document["text"], rag.chunk_size, rag.chunk_overlap)
                vectors = self.embeddings({"model": rag.emb["model"], "input": chunks})["embeddings"]
                for index, chunk in enumerate(chunks):
                    records.append(
                        VectorRecord(
                            id=f"{document['id']}:{index}",
                            document_id=document["id"],
                            chunk_index=index,
                            text=chunk,
                            metadata=document["metadata"],
                            embedding=[float(value) for value in vectors[index]],
                            embedding_model=rag.emb["model"],
                        )
                    )
            rag.store.records.extend(records)
            rag.store.save()
            return {"ok": True, "added": len(records), "stats": store_stats(rag.store)}
        if route == "rag.search":
            return self.rag_search(rag, str(payload.get("query") or ""), int(payload.get("top_k") or rag.top_k))
        if route == "rag.delete":
            return self.vector_endpoint("vector.delete", {**payload, "unit": {"type": "vectorstorage", "model": rag.store.name}})
        if route == "rag.clear":
            return self.vector_endpoint("vector.clear", {"unit": {"type": "vectorstorage", "model": rag.store.name}})
        if route == "rag.reindex":
            return {"ok": True, "reindexed": 0, "stats": store_stats(rag.store)}
        return {"ok": True, "rag": rag.name, "embedding_model": rag.emb["model"], **store_stats(rag.store)}

    def rag_search(self, rag: RagPipeline, query: str, top_k: int) -> dict[str, Any]:
        vector = self.embeddings({"model": rag.emb["model"], "input": query})["embeddings"][0]
        results = search_store(rag.store, [float(value) for value in vector], top_k)
        public = [public_record(record, score) for record, score in results]
        context = "\n\n".join(f"[{index + 1}] {item['text']}" for index, item in enumerate(public))
        return {"ok": True, "rag": rag.name, "query": query, "context": context, "results": public}

    def configure_units(self, units: list[dict[str, Any]]) -> list[dict[str, Any]]:
        model_units: list[dict[str, Any]] = []
        for request in units:
            unit_type = normalize_unit_type(str(request.get("type") or ""))
            if unit_type == "vectorstorage":
                self.configure_store_unit(request)
                continue
            if unit_type == "rag":
                self.configure_rag_unit(request)
                continue
            if unit_type == "onnx":
                self.configure_onnx_unit(request)
                continue
            instance = self.ensure_instance(request)
            self.apply_request(instance, request)
            model_units.append(request)
        return model_units

    def ensure_instance(self, request: dict[str, Any]) -> NativeInstance:
        unit_type = str(request.get("type") or "")
        model_name = str(request.get("model") or "")
        raw_quant = request.get("quant")
        if not isinstance(raw_quant, str) and isinstance(request.get("options"), dict):
            option_quant = request["options"].get("quant")
            raw_quant = option_quant if isinstance(option_quant, str) else None
        requested_quant = raw_quant if isinstance(raw_quant, str) else None
        model = resolve_model(unit_type, model_name, mode="native", quant=requested_quant)
        model_id = str(model["modelId"])
        current = self.instances.get(model_id)
        if current is not None:
            quant_changed = (
                requested_quant is not None
                and current.model.get("selectedQuantization") != model.get("selectedQuantization")
            )
            if quant_changed:
                current.model = dict(model)
                current.engine = None
                current.installed = False
                current.status = "selected"
            self.apply_request(current, request)
            return current
        instance = NativeInstance(model=dict(model))
        self.apply_request(instance, request)
        self.instances[model_id] = instance
        return instance

    def apply_request(self, instance: NativeInstance, request: dict[str, Any]) -> None:
        if isinstance(request.get("options"), dict):
            instance.options.update(request["options"])
        if "reasoning" in request:
            reasoning = request.get("reasoning")
            if reasoning is not None and not supports_reasoning(instance.model):
                raise RuntimeError(f"{instance.model['label']} does not advertise reasoning control")
            instance.reasoning = reasoning if isinstance(reasoning, bool) else None
        rag_payload = request.get("rag") or instance.options.get("rag")
        if isinstance(rag_payload, dict):
            instance.rag_id = self.configure_rag_unit(rag_payload).name

    def configure_onnx_unit(self, request: dict[str, Any]) -> CustomOnnxUnit:
        raw_options = request.get("options")
        options: dict[str, Any] = dict(raw_options) if isinstance(raw_options, dict) else {}
        name = str(request.get("model") or options.get("name") or "default")
        raw_path = options.get("model_path") or options.get("path")
        if not raw_path and name.lower().endswith(".onnx"):
            raw_path = name
        if not raw_path:
            raise RuntimeError("ONNX unit requires options.model_path")
        path = Path(str(raw_path)).expanduser()
        unit = self.custom_onnx.get(name)
        if unit is None:
            unit = CustomOnnxUnit(name=name, path=path, options=options)
            self.custom_onnx[name] = unit
        else:
            if unit.path != path:
                unit.path = path
                unit.session = None
                unit.status = "selected"
            unit.options.update(options)
        return unit

    def configure_store_unit(self, request: dict[str, Any]) -> VectorStore:
        raw_options = request.get("options")
        options: dict[str, Any] = raw_options if isinstance(raw_options, dict) else {}
        name = str(request.get("model") or options.get("name") or "default")
        store = self.vector_stores.get(name)
        if store is None:
            store = VectorStore(
                name=name,
                metric=str(options.get("metric") or "cosine"),
                persist=bool(options.get("persist", True)),
                namespace=str(options.get("namespace") or "default"),
            )
            store.load()
            self.vector_stores[name] = store
        return store

    def configure_rag_unit(self, request: dict[str, Any]) -> RagPipeline:
        raw_options = request.get("options")
        options: dict[str, Any] = raw_options if isinstance(raw_options, dict) else {}
        name = str(request.get("model") or options.get("name") or "default")
        emb = options.get("emb")
        if not isinstance(emb, dict):
            raise RuntimeError("RAG requires an embedding unit in options.emb")
        store_payload = options.get("store")
        store = self.configure_store_unit(store_payload if isinstance(store_payload, dict) else {"type": "vectorstorage", "model": f"{name}-store"})
        rerank = options.get("rerank") if isinstance(options.get("rerank"), dict) else None
        rag = RagPipeline(
            name=name,
            emb=dict(emb),
            rerank=dict(rerank) if rerank else None,
            store=store,
            chunk_size=int(options.get("chunk_size") or 800),
            chunk_overlap=int(options.get("chunk_overlap") or 120),
            top_k=int(options.get("top_k") or 5),
            candidate_k=int(options.get("candidate_k") or 30),
            score_threshold=float(options["score_threshold"]) if options.get("score_threshold") is not None else None,
        )
        self.rags[name] = rag
        return rag

    def prepare_model(self, instance: NativeInstance, *, install_only: bool) -> None:
        backend = str(instance.model.get("backend") or "onnxruntime")
        ensure_engine(backend, self.log)
        if backend == "llama.cpp":
            model_path = resolve_gguf_model_path(instance.model, self.log)
            instance.options["_resolved_model_path"] = str(model_path)
            if not install_only:
                self.ensure_llm_loaded(instance)
        elif backend == "onnxruntime" and not install_only:
            self.ensure_pipeline_loaded(instance)

    def ensure_llm_loaded(self, instance: NativeInstance) -> None:
        if instance.engine is not None:
            return
        ensure_engine("llama.cpp", self.log)
        try:
            from llama_cpp import Llama  # type: ignore[import-not-found]
        except ImportError as error:
            raise RuntimeError(native_dependency_error("llama_cpp", instance.model)) from error
        resolved_path = instance.options.get("_resolved_model_path")
        model_path = Path(str(resolved_path)) if resolved_path else resolve_gguf_model_path(instance.model, self.log)
        options = dict(instance.options)
        n_ctx = int(options.get("n_ctx") or options.get("context_window") or 4096)
        raw_gpu_layers = options.get("n_gpu_layers")
        n_gpu_layers = int(default_gpu_layers() if raw_gpu_layers is None else raw_gpu_layers)
        verbose = bool(options.get("verbose", False))
        quant = instance.model.get("selectedQuantization")
        size = format_bytes(model_path.stat().st_size) if model_path.exists() else "unknown size"
        self.log("info", f"Loading {instance.model['label']} quant={quant or 'auto'} from {model_path} ({size})")
        instance.engine = Llama(model_path=str(model_path), n_ctx=n_ctx, n_gpu_layers=n_gpu_layers, verbose=verbose)
        self.log("info", f"Loaded {instance.model['label']}")

    def ensure_pipeline_loaded(self, instance: NativeInstance) -> Any:
        if instance.engine is not None:
            return instance.engine
        ensure_engine("onnxruntime", self.log)
        try:
            from optimum.pipelines import pipeline as optimum_pipeline  # type: ignore[import-not-found]
        except ImportError as error:
            raise RuntimeError(native_dependency_error("optimum", instance.model)) from error
        task = str(instance.model["task"])
        model_id = str(instance.model.get("backendModelId") or instance.model["modelId"])
        self.log("info", f"Loading ONNX Runtime pipeline task={task} model={model_id}")
        try:
            instance.engine = optimum_pipeline(task=task, model=model_id, accelerator="ort")
        except TypeError:
            instance.engine = optimum_pipeline(task, model=model_id, accelerator="ort")
        self.log("info", f"Loaded ONNX Runtime pipeline task={task} model={model_id}")
        return instance.engine

    def instance_for_unit(self, unit: str, model_name: Any) -> NativeInstance:
        if model_name:
            return self.ensure_instance({"type": unit, "model": str(model_name)})
        for instance in self.instances.values():
            if instance.model.get("unit") == unit and instance.active:
                return instance
        raise RuntimeError(f"No active native {unit} unit")

    def messages_for_chat(
        self,
        instance: NativeInstance,
        payload: dict[str, Any],
        *,
        rag_context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        raw_messages = payload.get("messages")
        messages = raw_messages if isinstance(raw_messages, list) else [{"role": "user", "content": str(payload.get("prompt") or "")}]
        normalized = [dict(message) for message in messages if isinstance(message, dict)]
        if rag_context and rag_context.get("context"):
            normalized.insert(
                0,
                {
                    "role": "system",
                    "content": "Use this retrieved context when it is relevant. If it is not relevant, answer normally.\n\n"
                    + str(rag_context["context"]),
                },
            )
        reasoning = resolve_reasoning(instance, payload)
        if reasoning is not None and supports_reasoning(instance.model):
            normalized.insert(0, {"role": "system", "content": "/think" if reasoning else "/no_think"})
        return normalized

    def rag_context_for_chat(self, instance: NativeInstance, payload: dict[str, Any]) -> dict[str, Any] | None:
        if payload.get("use_rag") is False or not instance.rag_id:
            return None
        rag = self.rags.get(instance.rag_id)
        if rag is None:
            return None
        raw_messages = payload.get("messages")
        query = last_user_text(raw_messages if isinstance(raw_messages, list) else [])
        if not query:
            query = str(payload.get("prompt") or "")
        return self.rag_search(rag, query, int(payload.get("rag_top_k") or rag.top_k))

    def store_from_payload(self, payload: dict[str, Any]) -> VectorStore:
        unit = payload.get("unit")
        if isinstance(unit, dict):
            return self.configure_store_unit(unit)
        name = str(payload.get("store") or payload.get("name") or "default")
        return self.configure_store_unit({"type": "vectorstorage", "model": name, "options": payload.get("options") or {}})

    def onnx_from_payload(self, payload: dict[str, Any]) -> CustomOnnxUnit:
        unit = payload.get("unit")
        if isinstance(unit, dict):
            return self.configure_onnx_unit(unit)
        name = str(payload.get("model") or payload.get("name") or "default")
        if name not in self.custom_onnx:
            raise RuntimeError(f"ONNX unit not found: {name}")
        return self.custom_onnx[name]

    def ensure_custom_onnx_loaded(self, unit: CustomOnnxUnit) -> Any:
        if unit.session is not None:
            return unit.session
        ensure_engine("onnxruntime", self.log)
        try:
            import onnxruntime as ort
        except ImportError as error:
            raise RuntimeError(native_dependency_error("onnxruntime", {"modelId": unit.name})) from error
        if not unit.path.exists():
            raise RuntimeError(f"ONNX file does not exist: {unit.path}")
        providers = unit.options.get("providers")
        provider_list = [str(item) for item in providers] if isinstance(providers, list) else ort.get_available_providers()
        self.log("info", f"Loading custom ONNX unit {unit.name} from {unit.path}")
        unit.session = ort.InferenceSession(str(unit.path), providers=provider_list)
        unit.status = "running"
        unit.error = None
        self.log("info", f"Loaded custom ONNX unit {unit.name}")
        return unit.session

    def rag_from_payload(self, payload: dict[str, Any]) -> RagPipeline:
        unit = payload.get("unit")
        if isinstance(unit, dict):
            return self.configure_rag_unit(unit)
        name = str(payload.get("rag") or payload.get("name") or "default")
        if name not in self.rags:
            raise RuntimeError(f"RAG unit not found: {name}")
        return self.rags[name]

    def unit_states(self) -> list[dict[str, Any]]:
        states = []
        for unit in all_units(mode="native"):
            unit_type = str(unit["type"])
            models = [instance for instance in self.instances.values() if instance.model.get("unit") == unit_type]
            selected = next((instance for instance in models if instance.active), models[0] if models else None)
            states.append(
                {
                    "type": unit_type,
                    "selectedModelId": selected.model["modelId"] if selected else None,
                    "active": any(instance.active for instance in models),
                    "status": selected.status if selected else "off",
                    "reasoning": selected.reasoning if selected else None,
                    "quant": selected.model.get("selectedQuantization") if selected else None,
                    "supportsReasoning": supports_reasoning(selected.model) if selected else False,
                    "options": selected.options if selected else {},
                    "progress": selected.progress if selected else None,
                    "error": selected.error if selected else None,
                }
            )
        return states

    def model_state(self, instance: NativeInstance) -> dict[str, Any]:
        return {
            "runtimeId": instance.model["modelId"],
            "modelId": instance.model["modelId"],
            "unit": instance.model["unit"],
            "active": instance.active,
            "installed": instance.installed,
            "status": instance.status,
            "reasoning": instance.reasoning,
            "quant": instance.model.get("selectedQuantization"),
            "requestedQuant": instance.model.get("requestedQuantization"),
            "supportsReasoning": supports_reasoning(instance.model),
            "options": instance.options,
            "progress": instance.progress,
            "error": instance.error,
        }

    def service_states(self) -> list[dict[str, Any]]:
        stores = [
            {
                "runtimeId": f"vectorstorage:{store.name}",
                "type": "vectorstorage",
                "active": True,
                "status": "ready",
                "options": {
                    "name": store.name,
                    "metric": store.metric,
                    "persist": store.persist,
                    "namespace": store.namespace,
                    "records": len(store.records),
                },
            }
            for store in self.vector_stores.values()
        ]
        rags = [
            {
                "runtimeId": f"RAG:{rag.name}",
                "type": "RAG",
                "active": rag.active,
                "status": rag.status,
                "options": {
                    "emb": rag.emb,
                    "rerank": rag.rerank,
                    "store": rag.store.name,
                    "chunk_size": rag.chunk_size,
                    "chunk_overlap": rag.chunk_overlap,
                    "top_k": rag.top_k,
                    "candidate_k": rag.candidate_k,
                    "score_threshold": rag.score_threshold,
                },
                "error": rag.error,
            }
            for rag in self.rags.values()
        ]
        onnx_units = [
            {
                "runtimeId": f"onnx:{unit.name}",
                "type": "onnx",
                "active": unit.active,
                "status": unit.status,
                "options": {
                    **unit.options,
                    "model_path": str(unit.path),
                    "loaded": unit.session is not None,
                },
                "error": unit.error,
            }
            for unit in self.custom_onnx.values()
        ]
        return [*stores, *rags, *onnx_units]

    def log(self, level: str, message: str) -> None:
        self.logs.append({"time": time.time(), "level": level, "message": message})
        self.logs = self.logs[-500:]
        print(f"[xlocllm:{level}] {message}", file=sys.stderr, flush=True)


def create_app(port: int, token: str, live_time: float | None = None) -> FastAPI:
    runtime = NativeRuntime(token)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        if live_time is not None and live_time > 0:
            asyncio.create_task(shutdown_after(app, port, live_time))
        yield

    app = FastAPI(title="xlocllm native bridge", version="0.1.0", lifespan=lifespan)
    app.state.runtime = runtime
    app.state.live_time = live_time

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173", "https://localhost", "https://127.0.0.1"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {"name": "xlocllm native bridge", "backend": "native", "port": port, "dashboard": f"http://127.0.0.1:{port}/native-dashboard"}

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {"ok": True, "backend": "native", "port": port, "browser_connected": False}

    @app.get("/native-dashboard", response_class=HTMLResponse)
    async def native_dashboard() -> str:
        return native_dashboard_html(port)

    @app.get("/native-chat", response_class=HTMLResponse)
    async def native_chat() -> str:
        return native_chat_html(port)

    @app.get("/xlocllm/v1/status")
    async def status() -> dict[str, Any]:
        return {"ok": True, "port": port, "browser_connected": False, "backend": "native", "runtime": runtime.status(), "logs": runtime.logs[-200:]}

    @app.get("/xlocllm/v1/models")
    async def xloc_models() -> dict[str, Any]:
        return {"models": all_models(mode="native")}

    @app.get("/xlocllm/v1/units")
    async def xloc_units() -> dict[str, Any]:
        return {"units": all_units(mode="native")}

    @app.get("/xlocllm/v1/logs")
    async def logs(limit: int = 200) -> dict[str, Any]:
        return {"logs": runtime.logs[-limit:]}

    @app.post("/xlocllm/v1/runtime/install")
    async def install(payload: dict[str, Any]) -> Any:
        return safe_call(lambda: runtime.install(list(payload.get("units") or [])))

    @app.post("/xlocllm/v1/runtime/run")
    async def run(payload: dict[str, Any]) -> Any:
        return safe_call(lambda: runtime.run(list(payload.get("units") or [])))

    @app.post("/xlocllm/v1/runtime/stop")
    async def stop() -> Any:
        return runtime.stop()

    @app.post("/xlocllm/v1/runtime/hibernate")
    async def hibernate() -> Any:
        return runtime.hibernate()

    @app.post("/xlocllm/v1/runtime/heatup")
    async def heatup() -> Any:
        return safe_call(runtime.heatup)

    @app.post("/xlocllm/v1/runtime/reload")
    async def reload_runtime(payload: dict[str, Any]) -> Any:
        runtime.stop()
        return safe_call(lambda: runtime.run(list(payload.get("units") or [])))

    @app.post("/xlocllm/v1/runtime/set_active")
    async def set_active(payload: dict[str, Any]) -> Any:
        return safe_call(lambda: runtime.set_active(payload))

    @app.post("/xlocllm/v1/runtime/configure_unit")
    async def configure_unit(payload: dict[str, Any]) -> Any:
        return safe_call(lambda: runtime.configure_unit(payload))

    @app.post("/xlocllm/v1/models/delete")
    async def delete_model(payload: dict[str, Any]) -> Any:
        return safe_call(lambda: runtime.delete_model(payload))

    @app.post("/xlocllm/v1/models/delete_all")
    async def delete_all_models() -> Any:
        return runtime.delete_all_models()

    @app.post("/xlocllm/v1/invoke/{endpoint:path}")
    async def invoke(endpoint: str, payload: dict[str, Any]) -> Any:
        return safe_call(lambda: runtime.infer(endpoint.replace("/", "."), payload))

    @app.get("/v1/models")
    async def openai_models() -> dict[str, Any]:
        return {
            "object": "list",
            "data": [
                {"id": model["modelId"], "object": "model", "created": 0, "owned_by": "xlocllm"}
                for model in all_models(mode="native")
            ],
        }

    @app.post("/v1/chat/completions")
    async def chat_completions(payload: dict[str, Any]) -> Any:
        if payload.get("stream"):
            return StreamingResponse(stream_chat_response(runtime, payload), media_type="text/event-stream")
        result = safe_call(lambda: runtime.chat(payload))
        return openai_chat_response(payload, result)

    @app.post("/v1/responses")
    async def responses(payload: dict[str, Any]) -> Any:
        result = safe_call(lambda: runtime.infer("responses", payload))
        content = extract_content(result)
        return {
            "id": f"resp_{uuid.uuid4().hex}",
            "object": "response",
            "created_at": int(time.time()),
            "model": payload.get("model") or "xlocllm",
            "output": [
                {
                    "id": f"msg_{uuid.uuid4().hex}",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": content}],
                }
            ],
            "output_text": content,
        }

    @app.post("/v1/embeddings")
    async def embeddings(payload: dict[str, Any]) -> Any:
        result = safe_call(lambda: runtime.embeddings(payload))
        raw_vectors = result.get("embeddings") if isinstance(result, dict) else []
        vectors = raw_vectors if isinstance(raw_vectors, list) else []
        return {
            "object": "list",
            "model": payload.get("model") or "xlocllm-embedding",
            "data": [{"object": "embedding", "index": index, "embedding": vector} for index, vector in enumerate(vectors)],
        }

    @app.post("/xlocllm/v1/shutdown")
    async def shutdown() -> dict[str, Any]:
        remove_bridge(port)
        server = getattr(app.state, "uvicorn_server", None)
        if server is not None:
            server.should_exit = True
        return {"ok": True}

    return app


def safe_call(fn: Any) -> Any:
    try:
        return fn()
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


async def stream_chat_response(runtime: NativeRuntime, payload: dict[str, Any]) -> AsyncIterator[str]:
    chat_id = f"chatcmpl_{uuid.uuid4().hex}"
    model = str(payload.get("model") or "xlocllm")
    async for piece in runtime.stream_chat(payload):
        data = {
            "id": chat_id,
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [{"index": 0, "delta": {"content": piece}, "finish_reason": None}],
        }
        yield f"data: {json.dumps(data)}\n\n"
    done = {
        "id": chat_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
    }
    yield f"data: {json.dumps(done)}\n\n"
    yield "data: [DONE]\n\n"


def openai_chat_response(payload: dict[str, Any], result: Any) -> dict[str, Any]:
    content = extract_content(result)
    response: dict[str, Any] = {
        "id": f"chatcmpl_{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": payload.get("model") or "xlocllm",
        "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }
    rag = result.get("rag") if isinstance(result, dict) else None
    if rag is not None:
        response["xlocllm"] = {"rag": rag}
    return response


def ensure_native_import_path() -> Path:
    target = native_engine_dir() / engine_platform_key()
    target.mkdir(parents=True, exist_ok=True)
    hf_home = native_model_dir() / "hf-home"
    hf_home.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("HF_HOME", str(hf_home))
    os.environ.setdefault("HF_HUB_CACHE", str(native_model_dir()))
    target_text = str(target)
    if target_text not in sys.path:
        sys.path.insert(0, target_text)
    return target


def ensure_engine(backend: str, log: Any) -> None:
    imports = ENGINE_IMPORTS.get(backend)
    if not imports:
        return
    ensure_native_import_path()
    missing = [package for import_name, package in imports.items() if importlib.util.find_spec(import_name) is None]
    if backend == "onnxruntime" and importlib.util.find_spec("onnxruntime") is None:
        missing.append("onnxruntime-directml>=1.18.0" if sys.platform == "win32" else "onnxruntime>=1.18.0")
    if not missing:
        return
    if os.environ.get("XLOCLLM_NATIVE_DISABLE_INSTALL") == "1":
        raise RuntimeError(f"Native backend {backend} requires packages: {', '.join(missing)}")
    requirements = list(dict.fromkeys(missing))
    target = ensure_native_import_path()
    log("info", f"Installing native backend dependencies into {target}: {', '.join(requirements)}")
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "--target",
        str(target),
        "--no-warn-script-location",
        *requirements,
    ]
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "Native dependency installation failed for "
            f"{backend} on {platform.platform()} Python {platform.python_version()}. "
            f"Diagnostic command: {' '.join(command)}"
        )
    log("info", f"Installed native backend dependencies for {backend}")
    importlib.invalidate_caches()


def resolve_gguf_model_path(model: dict[str, Any], log: Any) -> Path:
    options_path = model.get("localPath")
    if options_path:
        path = Path(str(options_path)).expanduser()
        if path.exists():
            return path
    repo = str(model.get("repo") or model.get("backendModelId") or model.get("modelId"))
    patterns = [str(item) for item in model.get("files", ["*.gguf"])]
    try:
        from huggingface_hub import HfApi, hf_hub_download
    except ImportError as error:
        raise RuntimeError(native_dependency_error("huggingface_hub", model)) from error
    selected_quant = model.get("selectedQuantization")
    fallback_order = gguf_quant_fallback_order(model)
    quantizations = model.get("quantizations")
    attempts: list[tuple[str | None, list[str]]] = []
    if isinstance(quantizations, dict):
        for quant in fallback_order:
            raw_patterns = quantizations.get(quant)
            if isinstance(raw_patterns, list):
                attempts.append((quant, [str(item) for item in raw_patterns]))
    if not attempts:
        attempts.append((selected_quant if isinstance(selected_quant, str) else None, patterns))

    last_error: Exception | None = None
    for quant, quant_patterns in attempts:
        try:
            quant_label = quant or "auto"
            log(
                "info",
                f"Downloading/selecting GGUF model from {repo} quant={quant_label} patterns={quant_patterns}",
            )
            filename = select_hf_gguf_filename(repo, quant_patterns, HfApi())
            if filename is None:
                raise RuntimeError(f"No GGUF file matched {quant_patterns} in {repo}")
            local_path = Path(
                hf_hub_download(
                    repo_id=repo,
                    filename=filename,
                    cache_dir=str(native_model_dir()),
                )
            )
            candidate = local_path
            if not candidate.exists():
                raise RuntimeError(f"Downloaded GGUF file is missing: {candidate}")
            if quant and model.get("selectedQuantization") != quant:
                model["selectedQuantization"] = quant
                model["files"] = quant_patterns
            log("info", f"Selected GGUF file {candidate.name} ({format_bytes(candidate.stat().st_size)})")
            return candidate
        except Exception as error:  # noqa: BLE001
            last_error = error
            log("warning", f"GGUF quant={quant or 'auto'} unavailable for {repo}: {error}")
    raise RuntimeError(f"No GGUF file matched requested quantizations in {repo}: {last_error}")


def select_hf_gguf_filename(repo_id: str, patterns: list[str], api: Any) -> str | None:
    files = [str(item) for item in api.list_repo_files(repo_id=repo_id)]
    gguf_files = [item for item in files if item.lower().endswith(".gguf")]
    for pattern in patterns:
        matches = sorted(
            item
            for item in gguf_files
            if fnmatch(PurePosixPath(item).name, pattern) or fnmatch(item, pattern)
        )
        if matches:
            return matches[0]
    return None


def gguf_quant_fallback_order(model: dict[str, Any]) -> list[str]:
    requested = model.get("requestedQuantization") or model.get("selectedQuantization") or DEFAULT_GGUF_QUANT
    try:
        requested_quant = normalize_quantization(str(requested))
    except ValueError:
        requested_quant = DEFAULT_GGUF_QUANT
    raw_order = model.get("quantizationFallbackOrder")
    base_order = [str(item) for item in raw_order] if isinstance(raw_order, list) else GGUF_QUANT_FALLBACK_ORDER
    result = [requested_quant]
    for quant in base_order:
        normalized = normalize_quantization(str(quant))
        if normalized not in result:
            result.append(normalized)
    return result


def format_bytes(size: int | float) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} TB"


def delete_native_model_cache(model: dict[str, Any]) -> list[str]:
    repo = str(model.get("repo") or model.get("backendModelId") or model.get("modelId") or "")
    if not repo:
        return []
    cache_name = hf_cache_folder_name(repo)
    roots = [native_model_dir(), native_model_dir() / "hf-home" / "hub"]
    deleted: list[str] = []
    for root in roots:
        target = root / cache_name
        if safe_rmtree(target, root):
            deleted.append(str(target))
    return deleted


def clear_native_model_cache() -> list[str]:
    root = native_model_dir()
    root.mkdir(parents=True, exist_ok=True)
    deleted: list[str] = []
    for item in root.iterdir():
        if safe_rmtree(item, root):
            deleted.append(str(item))
    return deleted


def hf_cache_folder_name(repo_id: str) -> str:
    return "models--" + repo_id.replace("/", "--")


def safe_rmtree(path: Path, root: Path) -> bool:
    try:
        resolved = path.resolve()
        resolved_root = root.resolve()
    except OSError:
        return False
    if resolved == resolved_root or resolved_root not in resolved.parents:
        return False
    if not resolved.exists():
        return False
    if resolved.is_dir():
        shutil.rmtree(resolved)
    else:
        resolved.unlink()
    return True


def native_dependency_error(import_name: str, model: dict[str, Any]) -> str:
    return (
        f"Native dependency {import_name!r} is unavailable for model {model.get('modelId')!r}. "
        "Run runtime.run() again with network access or set mode='web' explicitly for browser runtime."
    )


def engine_platform_key() -> str:
    return f"py{sys.version_info.major}{sys.version_info.minor}-{platform.system().lower()}-{platform.machine().lower()}"


def default_gpu_layers() -> int:
    hardware = hardware_snapshot()
    if hardware.get("cuda", {}).get("available") or hardware.get("metal", {}).get("available"):
        return -1
    return 0


def hardware_snapshot() -> dict[str, Any]:
    cuda = {"available": shutil.which("nvidia-smi") is not None}
    directml = {"available": sys.platform == "win32"}
    metal = {"available": sys.platform == "darwin"}
    return {
        "cuda": cuda,
        "directml": directml,
        "metal": metal,
        "rocm": {"available": shutil.which("rocminfo") is not None, "experimental": True},
        "npu": {"available": False, "reason": "Native NPU probing is not implemented yet"},
    }


def native_capabilities(model_count: int) -> dict[str, Any]:
    hardware = hardware_snapshot()
    backend = "cuda" if hardware["cuda"]["available"] else "metal" if hardware["metal"]["available"] else "directml" if hardware["directml"]["available"] else "cpu"
    return {
        "webgpu": False,
        "webnn": False,
        "cpuFallback": True,
        "backend": f"native-{backend}",
        "modelCount": model_count,
        "catalogModelCount": model_count,
        "hardware": hardware,
    }


def native_npu_state() -> dict[str, Any]:
    return {"status": "unavailable", "reason": "Native NPU execution provider is not enabled in this MVP"}


def runtime_metrics() -> dict[str, int | None]:
    return {
        "gpu": nvidia_gpu_utilization(),
        "cpu": None,
        "ram": memory_load_percent(),
        "disk": disk_load_percent(native_model_dir()),
    }


def nvidia_gpu_utilization() -> int | None:
    if shutil.which("nvidia-smi") is None:
        return None
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    values = []
    for line in result.stdout.splitlines():
        try:
            values.append(int(line.strip()))
        except ValueError:
            continue
    return max(values) if values else None


def memory_load_percent() -> int | None:
    if sys.platform == "win32":
        import ctypes

        class MemoryStatusEx(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MemoryStatusEx()
        status.dwLength = ctypes.sizeof(MemoryStatusEx)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):  # type: ignore[attr-defined]
            return int(status.dwMemoryLoad)
        return None
    page_size = os.sysconf("SC_PAGE_SIZE") if hasattr(os, "sysconf") and "SC_PAGE_SIZE" in os.sysconf_names else None
    phys_pages = os.sysconf("SC_PHYS_PAGES") if hasattr(os, "sysconf") and "SC_PHYS_PAGES" in os.sysconf_names else None
    avail_pages = os.sysconf("SC_AVPHYS_PAGES") if hasattr(os, "sysconf") and "SC_AVPHYS_PAGES" in os.sysconf_names else None
    if not page_size or not phys_pages or avail_pages is None:
        return None
    total = page_size * phys_pages
    available = page_size * avail_pages
    return round((1 - available / total) * 100)


def disk_load_percent(path: Path) -> int:
    usage = shutil.disk_usage(path)
    return round((usage.used / usage.total) * 100)


def chat_kwargs(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {"temperature", "top_p", "top_k", "min_p", "typical_p", "repeat_penalty", "stop", "seed"}
    kwargs = {key: payload[key] for key in allowed if key in payload}
    max_tokens = payload.get("max_tokens") or payload.get("max_completion_tokens")
    if max_tokens is not None:
        kwargs["max_tokens"] = int(max_tokens)
    return kwargs


def resolve_reasoning(instance: NativeInstance, payload: dict[str, Any]) -> bool | None:
    for value in (
        payload.get("reasoning"),
        payload.get("enable_thinking"),
        payload.get("enableThinking"),
        (payload.get("chat_template_kwargs") or {}).get("enable_thinking") if isinstance(payload.get("chat_template_kwargs"), dict) else None,
        (payload.get("extra_body") or {}).get("reasoning") if isinstance(payload.get("extra_body"), dict) else None,
        instance.reasoning,
    ):
        if isinstance(value, bool):
            if not supports_reasoning(instance.model):
                raise RuntimeError(f"{instance.model['label']} does not advertise reasoning control")
            return value
        if value is None:
            continue
    return None


def normalize_embedding_output(output: Any) -> list[float]:
    if hasattr(output, "tolist"):
        output = output.tolist()
    values = flatten_numbers(output)
    if not values:
        return []
    norm = math.sqrt(sum(value * value for value in values))
    return [value / norm for value in values] if norm else values


def flatten_numbers(value: Any) -> list[float]:
    if isinstance(value, int | float):
        return [float(value)]
    if isinstance(value, dict):
        for key in ("embedding", "features", "last_hidden_state", "pooler_output"):
            if key in value:
                return flatten_numbers(value[key])
        return []
    if isinstance(value, Sequence) and not isinstance(value, str):
        if value and all(isinstance(item, int | float) for item in value):
            return [float(item) for item in value]
        rows = [flatten_numbers(item) for item in value]
        rows = [row for row in rows if row]
        if not rows:
            return []
        width = max(len(row) for row in rows)
        totals = [0.0] * width
        for row in rows:
            for index, item in enumerate(row):
                totals[index] += item
        return [item / len(rows) for item in totals]
    return []


def extract_score(output: Any) -> float:
    if isinstance(output, list) and output:
        return extract_score(output[0])
    if isinstance(output, dict):
        score = output.get("score")
        if isinstance(score, int | float):
            return float(score)
        if isinstance(output.get("logits"), Sequence):
            values = flatten_numbers(output["logits"])
            return max(values) if values else 0.0
    return 0.0


def normalize_endpoint(value: str) -> str:
    return value.strip().lower().replace("/", ".").replace("_", ".")


def normalize_unit_type(value: str) -> str:
    normalized = value.strip().lower().replace("_", "").replace("-", "")
    if normalized in {"rag"}:
        return "rag"
    if normalized in {"vectorstorage", "vectorstore", "vector"}:
        return "vectorstorage"
    if normalized in {"onnx", "onnxmodel", "onnxruntime", "regression"}:
        return "onnx"
    return value


def unit_for_endpoint(route: str) -> str:
    mapping = {
        "translate": "translator",
        "translator": "translator",
        "tts": "tts",
        "image.classify": "image-classification",
        "image-classification": "image-classification",
        "image.detect": "object-detection",
        "object-detection": "object-detection",
        "image.segment": "image-segmentation",
        "image-segmentation": "image-segmentation",
        "depth": "depth-estimation",
        "depth-estimation": "depth-estimation",
        "image-to-text": "vlm",
        "vlm": "vlm",
        "ocr": "ocr",
        "asr": "asr",
        "speech-to-text": "asr",
        "zero-shot-image": "zero-shot-image",
        "language-id": "language-id",
        "audio-classification": "audio-classification",
        "document-layout": "document-layout",
        "table-detection": "table-detection",
        "document-qa": "document-qa",
        "text-classification": "text-classification",
        "ner": "ner",
        "token-classification": "ner",
        "zero-shot-text": "zero-shot-text",
        "zero-shot-classification": "zero-shot-text",
        "summarization": "summarization",
        "summarize": "summarization",
        "text2text": "text2text",
        "text2text-generation": "text2text",
        "code": "code",
        "code.embed": "code",
    }
    if route not in mapping:
        raise RuntimeError(f"Unsupported native inference endpoint: {route}")
    return mapping[route]


def payload_input(payload: dict[str, Any]) -> Any:
    for key in ("input", "text", "image", "audio", "url", "prompt", "question"):
        if payload.get(key) is not None:
            return payload[key]
    raise RuntimeError("input/text/image/audio/url is required")


def vector_records_from_payload(payload: dict[str, Any]) -> list[VectorRecord]:
    embeddings = payload.get("embeddings") or payload.get("vectors")
    if not isinstance(embeddings, list):
        raise RuntimeError("vector.add requires embeddings or vectors")
    documents = normalize_documents(payload.get("documents") or payload.get("input") or payload.get("items"), payload.get("ids"), payload.get("metadatas"))
    records = []
    for index, document in enumerate(documents):
        records.append(
            VectorRecord(
                id=str(document.get("id") or f"{stable_id(document['text'])}:{index}"),
                document_id=str(document.get("id") or stable_id(document["text"])),
                chunk_index=0,
                text=str(document["text"]),
                metadata=dict(document.get("metadata") or {}),
                embedding=[float(value) for value in embeddings[index]],
                embedding_model=str(payload.get("embedding_model") or payload.get("embeddingModel") or "") or None,
            )
        )
    return records


def rag_documents(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return normalize_documents(payload.get("documents") or payload.get("input") or payload.get("text"), payload.get("ids"), payload.get("metadatas"))


def normalize_documents(input_value: Any, ids: Any = None, metadatas: Any = None) -> list[dict[str, Any]]:
    items = input_value if isinstance(input_value, list) else ([] if input_value is None else [input_value])
    id_list = [str(item) for item in ids] if isinstance(ids, list) else []
    metadata_list = metadatas if isinstance(metadatas, list) else []
    result = []
    for index, item in enumerate(items):
        if isinstance(item, dict):
            text = str(item.get("text") or item.get("content") or item.get("document") or "")
            raw_metadata = item.get("metadata")
            metadata: dict[str, Any] = raw_metadata if isinstance(raw_metadata, dict) else {}
            item_id_value = item.get("id") or item.get("document_id") or item.get("documentId")
            item_id = str(item_id_value or (id_list[index] if index < len(id_list) else stable_id(text)))
        else:
            text = str(item)
            raw_metadata = metadata_list[index] if index < len(metadata_list) else {}
            metadata = raw_metadata if isinstance(raw_metadata, dict) else {}
            item_id = id_list[index] if index < len(id_list) else stable_id(text)
        result.append({"id": item_id, "text": text, "metadata": dict(metadata)})
    return result


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    clean = text.strip()
    if not clean:
        return []
    step = max(1, size - overlap)
    return [clean[index : index + size] for index in range(0, len(clean), step)]


def search_store(store: VectorStore, vector: list[float], top_k: int) -> list[tuple[VectorRecord, float]]:
    scored = [(record, vector_score(store.metric, vector, record.embedding)) for record in store.records]
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:top_k]


def vector_score(metric: str, left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    width = min(len(left), len(right))
    dot = sum(left[index] * right[index] for index in range(width))
    if metric == "dot":
        return dot
    left_norm = math.sqrt(sum(left[index] * left[index] for index in range(width)))
    right_norm = math.sqrt(sum(right[index] * right[index] for index in range(width)))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def public_record(record: VectorRecord, score: float) -> dict[str, Any]:
    return {
        "id": record.id,
        "document_id": record.document_id,
        "chunk_index": record.chunk_index,
        "text": record.text,
        "metadata": record.metadata,
        "score": score,
    }


def record_to_dict(record: VectorRecord) -> dict[str, Any]:
    return {**public_record(record, 0.0), "embedding": record.embedding, "embedding_model": record.embedding_model}


def store_stats(store: VectorStore) -> dict[str, Any]:
    return {"name": store.name, "metric": store.metric, "namespace": store.namespace, "count": len(store.records), "persist": store.persist}


def string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Iterable):
        return [str(item) for item in value]
    return [str(value)]


def stable_id(value: Any) -> str:
    text = str(value)
    hash_value = 0
    for char in text:
        hash_value = (hash_value * 31 + ord(char)) & 0xFFFFFFFF
    return f"doc_{hash_value:x}"


def last_user_text(messages: list[Any]) -> str:
    for message in reversed(messages):
        if not isinstance(message, dict) or message.get("role") != "user":
            continue
        content = message.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return "\n".join(str(part.get("text") or part) for part in content)
    return ""


def normalize_responses_input(payload: dict[str, Any]) -> list[dict[str, Any]]:
    input_value = payload.get("input")
    if isinstance(input_value, list):
        return [dict(item) for item in input_value if isinstance(item, dict)]
    return [{"role": "user", "content": str(input_value or "")}]


def extract_content(result: Any) -> str:
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        if isinstance(result.get("content"), str):
            return str(result["content"])
        try:
            return str(result["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError):
            return json.dumps(result)
    return json.dumps(result)


def native_dashboard_html(port: int) -> str:
    del port
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>xlocllm native</title>
  <style>
    body {{ margin:0; font:14px system-ui,sans-serif; background:#f7faf9; color:#102027; }}
    main {{ padding:14px; display:grid; gap:12px; }}
    header {{ display:flex; justify-content:space-between; align-items:center; }}
    h1 {{ margin:0; font-size:24px; }}
    .pill {{ padding:6px 10px; border-radius:999px; background:#dff6ea; color:#135c3d; font-weight:700; }}
    .gauges {{ display:grid; grid-template-columns:repeat(3,1fr); gap:8px; }}
    .card {{ background:#edf4f4; border:1px solid #d9e5e5; border-radius:8px; padding:10px; }}
    .value {{ font-size:22px; font-weight:800; }}
    button {{ border:0; border-radius:7px; padding:10px 12px; font-weight:700; background:#102027; color:white; }}
    button.secondary {{ background:white; color:#102027; border:1px solid #d9e5e5; }}
    .actions {{ display:grid; grid-template-columns:repeat(3,1fr); gap:8px; }}
    .logs {{ max-height:96px; overflow:auto; font-size:12px; }}
  </style>
</head>
<body>
<main>
  <header><h1>xlocllm</h1><span class="pill">native</span></header>
  <section class="gauges">
    <div class="card"><span>GPU</span><div id="gpu" class="value">--</div></div>
    <div class="card"><span>CPU</span><div id="cpu" class="value">--</div></div>
    <div class="card"><span>RAM</span><div id="ram" class="value">--</div></div>
  </section>
  <section class="card"><span id="models">0 models</span> - <span id="queue">0 queue</span></section>
  <section class="actions">
    <button onclick="post('/xlocllm/v1/runtime/heatup')">Start</button>
    <button class="secondary" onclick="post('/xlocllm/v1/runtime/hibernate')">Pause</button>
    <button class="secondary" onclick="post('/xlocllm/v1/models/delete_all')">Clear</button>
  </section>
  <section id="logs" class="logs card"></section>
</main>
<script>
const fmt = (v) => v === null || v === undefined ? '--' : `${{v}}%`;
async function load() {{
  const data = await fetch('/xlocllm/v1/status').then(r => r.json());
  const rt = data.runtime || {{}};
  document.getElementById('gpu').textContent = fmt(rt.metrics?.gpu);
  document.getElementById('cpu').textContent = fmt(rt.metrics?.cpu);
  document.getElementById('ram').textContent = fmt(rt.metrics?.ram);
  document.getElementById('models').textContent = `${{(rt.models || []).filter(m => m.active).length}} models`;
  document.getElementById('queue').textContent = `${{rt.requests?.queued || 0}} queue`;
  document.getElementById('logs').innerHTML = (rt.logs || []).slice(-5).map(l => `<div>${{l.level}} - ${{l.message}}</div>`).join('');
}}
async function post(path) {{ await fetch(path, {{ method:'POST', headers:{{'content-type':'application/json'}}, body:'{{}}' }}); await load(); }}
setInterval(load, 1000); load();
</script>
</body>
</html>"""


def native_chat_html(port: int) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>xlocllm chat</title>
  <style>
    body {{ margin:0; font:14px system-ui,sans-serif; background:#f6f8fa; color:#111827; }}
    main {{ min-height:100vh; display:grid; grid-template-rows:auto 1fr auto; }}
    header {{ display:flex; gap:10px; align-items:center; padding:12px; border-bottom:1px solid #dbe3ea; background:white; }}
    h1 {{ margin:0; font-size:18px; }}
    select {{ flex:1; padding:8px; }}
    #log {{ padding:12px; overflow:auto; display:grid; align-content:start; gap:10px; }}
    .msg {{ max-width:80%; padding:10px 12px; border-radius:8px; white-space:pre-wrap; }}
    .user {{ justify-self:end; background:#111827; color:white; }}
    .assistant {{ justify-self:start; background:white; border:1px solid #dbe3ea; }}
    form {{ display:flex; gap:8px; padding:12px; border-top:1px solid #dbe3ea; background:white; }}
    textarea {{ flex:1; resize:none; padding:10px; }}
    button {{ border:0; border-radius:7px; padding:0 16px; background:#111827; color:white; font-weight:700; }}
  </style>
</head>
<body>
<main>
  <header><h1>xlocllm</h1><select id="model"></select><label><input id="rag" type="checkbox" checked> RAG</label></header>
  <section id="log"></section>
  <form id="form"><textarea id="input" rows="3" placeholder="Message"></textarea><button>Send</button></form>
</main>
<script>
const log = document.getElementById('log');
const model = document.getElementById('model');
const input = document.getElementById('input');
const rag = document.getElementById('rag');
const params = new URLSearchParams(location.search);
const session = params.get('session') || 'default';
const requestedModel = params.get('model') || '';
const storageKey = `xlocllm:native-chat:{port}:${{session}}`;
rag.checked = params.get('useRag') !== '0';
const messages = JSON.parse(localStorage.getItem(storageKey) || '[]');
function render() {{ log.innerHTML = messages.map(m => `<div class="msg ${{m.role}}">${{m.content}}</div>`).join(''); log.scrollTop = log.scrollHeight; localStorage.setItem(storageKey, JSON.stringify(messages)); }}
async function loadModels() {{
  const data = await fetch('/xlocllm/v1/status').then(r => r.json());
  const items = (data.runtime?.models || []).filter(m => m.unit === 'LLM' && m.active);
  model.innerHTML = items.length ? items.map(m => `<option value="${{m.modelId}}">${{m.modelId}}</option>`).join('') : '<option value="">LLM</option>';
  if (requestedModel) model.value = requestedModel;
}}
document.getElementById('form').addEventListener('submit', async (event) => {{
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  messages.push({{ role:'user', content:text }}); input.value = ''; render();
  const response = await fetch('/xlocllm/v1/invoke/chat.completions', {{
    method:'POST', headers:{{'content-type':'application/json'}},
    body: JSON.stringify({{ model:model.value || undefined, messages, use_rag:rag.checked, max_tokens:512 }})
  }});
  const data = await response.json();
  messages.push({{ role:'assistant', content:data.content || data.choices?.[0]?.message?.content || JSON.stringify(data) }});
  render();
}});
loadModels(); render(); setInterval(loadModels, 5000);
</script>
</body>
</html>"""


async def shutdown_after(app: FastAPI, port: int, delay: float) -> None:
    await asyncio.sleep(delay)
    remove_bridge(port)
    server = getattr(app.state, "uvicorn_server", None)
    if server is not None:
        server.should_exit = True


def run_server(port: int, token: str, live_time: float | None = None) -> None:
    app = create_app(port, token, live_time)
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level=os.environ.get("XLOCLLM_LOG_LEVEL", "warning"))
    server = uvicorn.Server(config)
    app.state.uvicorn_server = server
    upsert_bridge(port, pid=os.getpid(), token=token, backend="native")
    server.run()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=1146)
    parser.add_argument("--token", required=True)
    parser.add_argument("--live-time", type=float, default=None)
    args = parser.parse_args()
    run_server(args.port, args.token, args.live_time)


if __name__ == "__main__":
    main()
