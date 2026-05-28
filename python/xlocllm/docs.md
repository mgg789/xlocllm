# xlocllm Python SDK

`xlocllm` is a local inference SDK with one Python-facing API and two runtime
modes. The default is `native`: Python starts a local supervisor, exposes an
OpenAI-compatible loopback API, and runs local engines such as llama.cpp/GGUF
for LLMs and ONNX Runtime for embeddings, rerankers, vision, audio, OCR, and
other task models.

The existing browser/WebGPU runtime remains available with `mode="web"`. It
keeps the old paired-browser behavior through MLC WebLLM and Transformers.js.

## Install

```powershell
python -m pip install -e .\python\xlocllm
```

Package metadata:

- Python: `>=3.10`
- Base runtime dependencies: `fastapi`, `uvicorn[standard]`, `pydantic`
- CLI entry points: `xlocllm`, `xlocllm-bridge`

The base install is intentionally light. In `native` mode, managed engine
dependencies and model artifacts are downloaded into the xlocllm cache during
the first `runtime.run()` that needs them. Set `XLOCLLM_NATIVE_DISABLE_INSTALL=1`
to make missing native dependencies fail fast instead of being installed.

## Core Objects

The v1-style SDK schema has four main concepts:

- `ModelInfo` - immutable model catalog entry with hardware and runtime metadata.
- `Unit` - one capability/model pair, for example `LLM + Qwen`.
- `Runtime` - a group of units that should run together.
- `Bridge` / `NativeBridge` - local HTTP control process for the selected mode.

The global default mode is:

```python
import xlocllm

print(xlocllm.mode)  # native
xlocllm.mode = "web"  # opt into browser/WebGPU mode globally
```

## Quick Start

```python
import xlocllm

llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b")
emb = xlocllm.unit("embedding", "multilingual-e5-small")

runtime = xlocllm.runtime([llm, emb], port=1146)
runtime.install()
runtime.run()

print(runtime.url)       # http://127.0.0.1:1146/v1
print(runtime.status())  # Full bridge/runtime status dictionary
```

Single-unit compatibility is supported:

```python
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b")
llm.install()
llm.run()
```

Context-manager cleanup is supported:

```python
with xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b")]) as runtime:
    runtime.run()
    print(runtime.chat("Say hello", temperature=0))
```

## OpenAI-Compatible Usage

```python
import xlocllm
from openai import OpenAI

llm = xlocllm.unit(type="LLM", model="Qwen-3.5-0.8b-fp32")
client = OpenAI(base_url="http://127.0.0.1:1146/v1", api_key="xlocllm")

with xlocllm.runtime([llm]) as runtime:
    runtime.run()
    response = client.chat.completions.create(
        model="Qwen-3.5-0.8b-fp32",
        messages=[{"role": "user", "content": "What is lidar?"}],
        max_tokens=64,
    )
    print(response.choices[0].message.content)
```

Supported OpenAI-like endpoints:

- `GET /v1/models`
- `POST /v1/chat/completions`
- `POST /v1/chat/completions` with `stream=True`
- `POST /v1/responses`
- `POST /v1/embeddings`

## Top-Level API

### `xlocllm.unit(type, model, reasoning=None, options=None, rag=None, mode=None)`

Creates a `Unit` by resolving the requested unit type and model name against the
catalog. `reasoning` may be `True`, `False`, or `None` for LLM families that
advertise thinking/reasoning control. `options` is a dictionary passed to the
selected runtime for that unit. `mode` defaults to `xlocllm.mode`, which is
`"native"` unless changed. For LLM units, pass `rag=<RAG unit>` to enable
automatic retrieval before chat calls.

```python
unit = xlocllm.unit("chat", "qwen-0.8b")
print(unit.type)   # LLM
print(unit.mode)   # native
```

Accepted model names include exact `modelId`, `label`, and catalog aliases.

### `xlocllm.vectorstorage(name="default", backend="indexeddb", metric="cosine", persist=True, namespace="default", options=None, mode=None)`

Creates a local service unit for vector storage. In native mode, the default
backend is rewritten to the native persistent store. In web mode, the default
backend remains browser IndexedDB. Use `persist=False` or `backend="memory"` for
temporary stores. `metric` accepts `cosine`, `dot`, or `euclidean`.

```python
store = xlocllm.vectorstorage(name="docs", namespace="kb")
```

Direct vector storage calls require explicit embeddings. Most users should use
`xlocllm.rag(...)`, which chunks text, embeds it, and writes vectors for you.

### `xlocllm.rag(emb, rerank=None, store=None, name="default", chunk_size=800, chunk_overlap=120, top_k=5, candidate_k=30, score_threshold=None, options=None, mode=None)`

Creates a high-level RAG service unit. `emb` must be an embedding unit. `rerank`
is optional and must be a reranker unit. If `store` is omitted, xlocllm creates
a vector store named `<name>-store` in the selected mode.

```python
emb = xlocllm.unit("embedding", "multilingual-e5-small")
rerank = xlocllm.unit("reranker", "bge-reranker-base")
rag = xlocllm.rag(emb=emb, rerank=rerank, name="kb")
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", rag=rag)
```

### `xlocllm.runtime(units, port=1146, bridge=None, runtime_id=None, mode=None)`

Creates a `Runtime` from `Unit` or `UnitRequest` objects. `mode=None` uses
`xlocllm.mode`; pass `mode="web"` to force the browser/WebGPU backend for this
runtime only.

```python
runtime = xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b")], port=12000)
web_runtime = xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b", mode="web")], mode="web")
```

### `xlocllm.models(..., mode=None, installed=None, hardware=None, include_unavailable=False)`

Returns filtered catalog entries as `ModelInfo` objects.

Filters:

- `unit`
- `runtime`
- `task`
- `task_group`
- `hardware_tier`
- `language`
- `provider`
- `availability`
- `npu`
- `webgpu` - pass `False` to list only CPU/WASM fallback-capable models
- `cpu` - alias for CPU/WASM fallback mode
- `available_without_webgpu` - explicit CPU/WASM fallback filter
- `search`
- `max_vram_mb`
- `max_disk_mb`
- `max_size_gb`
- `max_parameters_b`
- `limit_per_unit`
- `mode` - `"native"` or `"web"`; defaults to `xlocllm.mode`
- `installed` - filter installed model artifacts when bridge/status data is available
- `hardware` - optional hardware snapshot used for native availability filtering
- `include_unavailable` - include native catalog entries even when local engine
  or hardware policy says they are unavailable

Example:

```python
small_llms = xlocllm.models(unit="LLM", max_vram_mb=1500, search="qwen")
native_llms = xlocllm.models(unit="LLM", mode="native")
cpu_web_models = xlocllm.models(unit="LLM", mode="web", webgpu=False)
```

In web mode, `webgpu=False` excludes MLC/WebLLM models and heavy
Transformers.js models. The fallback catalog keeps at least one usable model for
every unit class whenever the catalog contains a Transformers.js candidate for
that class.

### `xlocllm.model(name, unit=None, mode=None)`

Returns one `ModelInfo`.

```python
info = xlocllm.model("Qwen-3.5-0.8b", unit="LLM")
print(info.model_id)
print(info.to_dict())
```

Native entries include backend fields such as `backend`, `format`, `repo`,
`files`, `quantization`, `providers`, `ram_mb`, `vram_mb`, `disk_mb`, and
`verified` when known.

### `xlocllm.bridges(active_only=True)`

Returns known `Bridge` objects from the local bridge registry.

### `xlocllm.runtimes(active_only=True)`

Returns known `Runtime` objects from the local runtime registry.

### `xlocllm.status()`

Returns a dictionary with:

- known bridges
- known runtimes
- installed/running model snapshots when available
- browser-reported resource metrics when available
- catalog model count

### `xlocllm.benchmark(type=None, mode=None, ping_hf=True, timeout=2.0, browser=True, browser_timeout=15.0, port=None)`

Returns a dictionary with local system parameters, RAM, free disk space, native
hardware/engine availability, optional browser capabilities, and Hugging Face
latency. In native mode, no model-hosting browser is required. In web mode,
`browser=True` starts a temporary local bridge and mini browser window to detect
real WebGPU/WebNN/NPU availability, then closes them after the probe.

When `type` is provided, benchmark also returns two recommendations for that
unit type:

- `fast` - a smaller model expected to run quickly and stably.
- `quality` - the strongest model that appears to fit the detected/estimated
  device limits.

```python
system = xlocllm.benchmark()
llm_fit = xlocllm.benchmark("LLM")
```

Use `browser=False` for CI/headless checks that must not open a browser window.

## Unit API

Properties:

- `unit.id` - stable local id in the form `<type>:<modelId>`
- `unit.type`
- `unit.model`
- `unit.label`
- `unit.model_info`
- `unit.mode`
- `unit.reasoning`
- `unit.options`
- `unit.rag` - attached RAG unit for LLM units, when configured
- `unit.supports_reasoning`

Methods:

- `unit.to_payload()` - `{"type": ..., "model": ...}`
- `unit.to_dict()` - payload plus label and model metadata
- `unit.status()` - attached runtime state if available
- `unit.remove()` - remove from attached runtime without deleting cache
- `unit.delete_cache(bridge=None)` - delete selected-mode cache for the model
- `unit.delete(delete_cache=True, bridge=None)` - remove from runtime and optionally delete model cache
- `unit.set_reasoning(enabled)` - hot-update reasoning control when attached to a running runtime
- `unit.as_runtime(port=1146)` - create or reuse a single-unit runtime
- `unit.install(port=1146)`
- `unit.run(port=1146)`
- `unit.stop()`
- `unit.hibernate()`
- `unit.heatup()`
- `unit.invoke(endpoint, payload, timeout=None)`
- `unit.add(documents, ids=None, metadatas=None, embeddings=None, **params)` - for `RAG` and `vectorstorage`
- `unit.search(query=None, embedding=None, top_k=None, filter=None, **params)` - for `RAG` and `vectorstorage`
- `unit.delete(ids=None, filter=None, **params)` - delete RAG documents or vector records
- `unit.clear(**params)` - clear a RAG/vector store namespace
- `unit.stats()` - return RAG/vector store stats
- `unit.reindex(**params)` - re-embed existing RAG chunks

## Runtime API

Properties:

- `runtime.id`
- `runtime.port`
- `runtime.base_url` - `http://127.0.0.1:<port>`
- `runtime.url` - `http://127.0.0.1:<port>/v1`
- `runtime.bridge`
- `runtime.mode`
- `runtime.installed`
- `runtime.running`
- `runtime.unit_requests`

Methods:

- `runtime.add_unit(unit)`
- `runtime.remove_unit(unit_id, delete_cache=False)`
- `runtime.configure_unit(unit_id, reasoning=None, options=None)`
- `runtime.set_reasoning(unit_id, enabled)`
- `runtime.unit_status(unit_id)`
- `runtime.units(as_dict=False, state=False)`
- `runtime.models()`
- `runtime.install(port=None)`
- `runtime.run(port=None)`
- `runtime.stop()`
- `runtime.hibernate()`
- `runtime.heatup()`
- `runtime.status()`
- `runtime.health()`
- `runtime.logs(limit=200)`
- `runtime.invoke(endpoint, payload, timeout=None)`
- `runtime.client(api_key="xlocllm", **kwargs)`
- `runtime.chat(prompt=None, messages=None, model=None, use_rag=None, **params)`
- `runtime.embed(input, model=None)`
- `runtime.open()`
- `runtime.chatui(model=None, session="default", use_rag=True, open_browser=True, block=True, width=760, height=860)`
- `runtime.close()`
- `runtime.wait_ready(timeout=None, require_browser=False)`

`Runtime` implements `with` cleanup. Exiting the context closes the owned bridge
and any owned dashboard/browser window when they were started by that runtime.

`runtime.remove_unit()` accepts the unit id, model id, or unit type. If the
runtime is running and `delete_cache=False`, the SDK asks the selected backend
to deactivate that specific model. If `delete_cache=True`, it requests model
cache cleanup through the bridge.

## RAG and Vector Storage

RAG runs in the active runtime mode:

1. `rag.add(...)` chunks documents.
2. The configured embedding unit embeds every chunk.
3. Vectors and metadata are persisted in the selected backend store.
4. `rag.search(...)` embeds the query, vector-searches candidates, optionally
   reranks them, and returns `results` plus an assembled `context` string.

Native mode uses local persistent storage under the xlocllm cache. Web mode uses
IndexedDB in the paired browser runtime.

```python
emb = xlocllm.unit("embedding", "multilingual-e5-small")
store = xlocllm.vectorstorage("support-kb")
rag = xlocllm.rag(emb=emb, store=store, name="support")
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", rag=rag)

with xlocllm.runtime([llm]) as rt:
    rt.run()
    rag.add(["Refunds are processed within 5 business days."], ids=["refunds"])
    print(rag.search("How long does a refund take?", top_k=3))
    print(rt.chat("How long does a refund take?"))
    print(rt.chat("Ignore local docs and answer generally", use_rag=False))
```

When an LLM has `rag=...`, `runtime.chat(...)`, `/xlocllm/v1/invoke/chat.completions`,
and OpenAI-compatible `/v1/chat/completions` perform retrieval automatically
unless `use_rag=False` is passed. The SDK response includes `raw["rag"]` and
`rag` metadata when retrieval was used. OpenAI-compatible responses expose the
same data under the extension field `xlocllm.rag`.

Low-level vector endpoints are available through `runtime.invoke(...)`:

- `vector.add`, `vector.search`, `vector.delete`, `vector.clear`, `vector.stats`
- `rag.add`, `rag.search`, `rag.delete`, `rag.clear`, `rag.reindex`, `rag.stats`

## Chat UI

`runtime.chatui()` starts the runtime if needed and opens a separate chat window
that talks to the existing bridge over HTTP. It blocks by default so scripts that
use `with xlocllm.runtime(...)` keep the runtime alive until the chat window is
closed. Pass `block=False` if you want just the `WindowHandle`.

```python
with xlocllm.runtime([llm]) as rt:
    rt.run()
    rt.chatui(session="demo", use_rag=True)
```

## Bridge API

Properties:

- `bridge.port`
- `bridge.base_url`
- `bridge.url` - OpenAI-compatible `/v1` URL

Methods:

- `bridge.activate(daemon=False)`
- `bridge.close()`
- `bridge.status()`
- `bridge.health()`
- `bridge.models()` - browser-visible catalog as dictionaries when paired; local catalog fallback otherwise
- `bridge.units()` - unit definitions as dictionaries
- `bridge.logs(limit=200)`
- `bridge.wait_ready(timeout=None, require_browser=False)`
- `bridge.reload(units=None)`
- `bridge.set_active(unit, active=True, model=None)`
- `bridge.delete_model(unit_or_model, model=None)`
- `bridge.delete_all_models(confirm=True)`
- `bridge.invoke(endpoint, payload, timeout=None)`
- `bridge.processes()`

## Direct Invoke Endpoints

Use `runtime.invoke(endpoint, payload)` or `bridge.invoke(endpoint, payload)`.

Supported endpoints:

| Endpoint | Unit | Required input | Return shape |
| --- | --- | --- | --- |
| `chat.completions`, `chat` | `LLM` | `messages` or `prompt` | `{content, raw?}` |
| `responses` | `LLM` | `input` | response-like text content |
| `embeddings`, `embedding` | `embedding` | `input` string or list | `{embeddings}` |
| `rerank`, `reranker` | `reranker` | `query`, `documents` | `{results}` sorted by score |
| `translate`, `translator` | `translator` | `text`/`input`, optional `src_lang`, `tgt_lang` | backend translation output |
| `tts` | `tts` | `text`/`input` | audio-like result, serialized when possible |
| `image.classify`, `image-classification` | `image-classification` | `image`/`input`/`url` | `{labels, raw}` |
| `image.detect`, `object-detection` | `object-detection` | `image`/`input`/`url` | `{boxes, raw}` |
| `image.segment`, `image-segmentation` | `image-segmentation` | `image`/`input`/`url` | `{segments, raw}` |
| `depth`, `depth-estimation` | `depth-estimation` | `image`/`input`/`url` | `{depth, raw}` |
| `image-to-text`, `vlm` | `vlm` | `image`/`input`/`url` | `{text, raw}` |
| `asr`, `speech-to-text` | `asr` | `audio`/`input`/`url` | `{text, chunks?, raw}` |
| `zero-shot-image` | `zero-shot-image` | `image`, `labels`/`candidate_labels` | `{labels, raw}` |
| `language-id` | `language-id` | `audio`/`input`/`url` | `{labels, raw}` |
| `audio.classify`, `audio-classification` | `audio-classification` | `audio`/`input`/`url` | `{labels, raw}` |
| `ocr` | `ocr` | `image`/`input`/`url` | `{text, raw}` |
| `document-layout` | `document-layout` | `image`/`input`/`url` | `{boxes, raw}` |
| `table-detection` | `table-detection` | `image`/`input`/`url` | `{boxes, raw}` |
| `document-qa` | `document-qa` | `image`, `question`/`query` | `{answers, raw}` |
| `text.classify`, `text-classification` | `text-classification` | `text`/`input` | `{labels, raw}` |
| `ner`, `token-classification` | `ner` | `text`/`input` | `{entities, raw}` |
| `zero-shot-text`, `zero-shot-classification` | `zero-shot-text` | `text`, `labels`/`candidate_labels` | `{labels, raw}` |
| `summarization`, `summarize` | `summarization` | `text`/`input` | `{summary, raw}` |
| `text2text`, `text2text-generation` | `text2text` | `text`/`input` | `{text, raw}` |
| `code`, `code.embed` | `code` | `text`/`input` | `{features, raw}` |
| `vector.add` | `vectorstorage` | `unit`, `documents`, `embeddings` | `{ok, store, namespace, ids}` |
| `vector.search` | `vectorstorage` | `unit`, `embedding` | `{ok, results}` |
| `vector.delete`, `vector.clear`, `vector.stats` | `vectorstorage` | `unit` | storage mutation/stats result |
| `rag.add` | `RAG` | `unit`, `documents` | `{ok, rag, store, ids}` |
| `rag.search` | `RAG` | `unit`, `query` | `{ok, results, context}` |
| `rag.delete`, `rag.clear`, `rag.reindex`, `rag.stats` | `RAG` | `unit` | RAG mutation/stats result |

Examples:

```python
runtime.invoke("embeddings", {"model": "Xenova/multilingual-e5-small", "input": ["hello"]})
runtime.invoke("translate", {"model": "Xenova/opus-mt-en-ru", "text": "hello"})
runtime.invoke("rerank", {"query": "local llm", "documents": ["browser", "server"]})
runtime.invoke("zero-shot-text", {"text": "Fast local inference", "labels": ["AI", "finance"]})
```

Convenience wrappers:

```python
runtime.chat("hello", temperature=0)
vectors = runtime.embed(["hello", "world"])
client = runtime.client()  # requires the optional openai package
```

## Environment Variables

- `XLOCLLM_HOME` - override state directory.
- `XLOCLLM_WEB_URL` - use a custom web runtime URL instead of autodiscovery.
- `XLOCLLM_LOG_LEVEL` - uvicorn log level, default `warning`.
- `XLOCLLM_NATIVE_DISABLE_INSTALL=1` - disable managed native dependency
  installation and fail with a diagnostic error when an engine is missing.

Default state locations:

- Windows: `%LOCALAPPDATA%\xlocllm`
- Unix-like: `$XDG_STATE_HOME/xlocllm` or `~/.local/state/xlocllm`

Native engines, downloaded model artifacts, and native vector storage live under
the same `XLOCLLM_HOME` tree.

## Native Runtime Notes

Native mode is the default. The dashboard window is a monitor/control surface:
it shows process, download, queue, loaded-unit, and resource status, but model
weights are not executed in that browser window.

Native LLMs use GGUF through llama.cpp-compatible loading. Non-LLM tasks use
ONNX Runtime pipelines where available. The install planner checks the selected
model, OS, Python version, hardware signals, engine cache, and model cache before
starting. If a native engine or artifact cannot be installed or loaded, the
error includes the backend, model id, OS, Python version, and cache/diagnostic
context instead of silently falling back to web mode.

## Browser Runtime Notes

The bridge binds to `127.0.0.1`. In `mode="web"`, the browser window must stay
open while browser models are running. The Python bridge is only a local control
and API layer; the model weights and inference execution live in browser storage
and browser GPU runtime.

If a mini browser runtime disconnects while an RPC is in progress, the bridge
waits up to 30 seconds for the browser to reconnect and retries the RPC. If the
mini window stays disconnected for 30 seconds, the bridge shuts itself down to
avoid orphan local processes.

When WebGPU is unavailable, the browser runtime switches supported
Transformers.js models to WASM and rejects MLC/WebLLM or heavy model requests
before loading. `runtime.status()["runtime"]["capabilities"]` reports
`webgpu`, `webnn`, `cpuFallback`, and the number of visible catalog models.

## Reasoning Control

Reasoning control is available for LLM families that advertise thinking mode,
currently detected for Qwen3/Qwen3.5, DeepSeek-R1, gpt-oss, and QwQ-style model
names. Set it when creating the unit:

```python
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", reasoning=False)
```

Change it while a runtime is already running:

```python
runtime.set_reasoning(llm.id, True)
llm.set_reasoning(False)
```

Per-request values such as `reasoning`, `enable_thinking`, or
`chat_template_kwargs={"enable_thinking": ...}` override the unit default. Web
mode passes `chat_template_kwargs.enable_thinking` for Transformers.js pipelines
and adds Qwen's `/think` or `/no_think` marker for MLC/WebLLM-style chat when
needed. Native mode keeps the same SDK flag and applies it through the native
chat template path when the selected model advertises reasoning support.

## CLI

```powershell
xlocllm status
xlocllm benchmark
xlocllm benchmark LLM
xlocllm benchmark LLM --mode web
xlocllm benchmark embedding --no-browser --no-hf
xlocllm models --unit LLM
xlocllm models --unit LLM --mode web --no-webgpu
xlocllm model "Qwen-3.5-0.8b-fp32" --unit LLM
xlocllm run --unit LLM --model "Qwen-3.5-0.8b" --port 1146
xlocllm run --unit LLM --model "Qwen-3.5-0.8b" --mode web
xlocllm run --unit LLM --model "Qwen-3.5-0.8b-fp32" --no-reasoning
xlocllm bridge --port 1146
xlocllm bridge --mode web --port 1146
```

## Ready Recipes

Russian end-to-end scripts for RAG, photo translation, agentic LLM stacks, voice
assistant, OCR/document intelligence, and other common tasks live in
[`recipes_ru.md`](recipes_ru.md).

## Complete API Reference

### Top-Level Exports

Imported directly from `xlocllm`:

- `xlocllm.mode` - global runtime mode, `"native"` by default; set to `"web"` for browser mode
- `xlocllm.unit(type, model, reasoning=None, options=None, rag=None, mode=None) -> Unit`
- `xlocllm.vectorstorage(name="default", ..., mode=None) -> Unit`
- `xlocllm.rag(emb, rerank=None, store=None, ..., mode=None) -> Unit`
- `xlocllm.runtime(units, port=1146, bridge=None, runtime_id=None, mode=None) -> Runtime`
- `xlocllm.model(name, unit=None, mode=None) -> ModelInfo`
- `xlocllm.models(..., mode=None, installed=None, hardware=None, include_unavailable=False) -> list[ModelInfo]`
- `xlocllm.cpu_fallback_model_ids() -> set[str]`
- `xlocllm.supports_cpu_fallback(model_dict) -> bool`
- `xlocllm.supports_reasoning(model_dict) -> bool`
- `xlocllm.bridges(active_only=True) -> list[Bridge | NativeBridge]`
- `xlocllm.runtimes(active_only=True) -> list[Runtime]`
- `xlocllm.status() -> dict`
- `xlocllm.benchmark(type=None, mode=None, ...) -> dict`
- `xlocllm.window(...) -> WindowHandle`
- `xlocllm.GetBridge(port=None) -> Bridge | BridgeGroup`
- classes: `Bridge`, `NativeBridge`, `BridgeGroup`, `ModelInfo`, `Runtime`, `Unit`, `UnitRequest`
- exceptions: `XlocLLMError`, `BridgeNotReady`, `BrowserNotConnected`,
  `ModelNotFound`, `RuntimeNotFound`, `UnitNotFound`

### `ModelInfo`

`ModelInfo` wraps one catalog record. It behaves like a typed read-only view over
the underlying model dictionary.

Properties:

- `data: dict[str, Any]` - raw catalog object.
- `unit: str` - unit type, for example `LLM` or `embedding`.
- `runtime: str` - backend family, for example `native`, `mlc`, or `transformers`.
- `mode: str | None` - catalog mode when present.
- `task: str` - backend task string.
- `model_id: str` - exact model id to pass to `unit()`.
- `label: str` - human-readable model name.
- `aliases: list[str]` - accepted lookup aliases.
- `hardware_tier: str` - `tiny`, `small`, `medium`, or `large`.
- `disk_mb: int` - approximate disk/cache size.
- `vram_mb: int` - approximate GPU memory requirement.
- `npu_eligible: bool` - whether WebNN/NPU is preferred when available.
- `cpu_fallback: bool` - whether the model can run in CPU/WASM fallback mode.
- `supports_reasoning: bool` - whether the model advertises reasoning control.

Methods:

- `get(key, default=None) -> Any` - dictionary-style optional lookup.
- `__getitem__(key) -> Any` - dictionary-style required lookup.
- `to_dict() -> dict[str, Any]` - copy of the raw catalog object.

### `Unit`

`Unit` represents one model-backed capability, service unit, or composite unit.

Constructor is normally not called directly. Prefer:

```python
unit = xlocllm.unit("LLM", "Qwen-3.5-0.8b", reasoning=None, options=None, rag=None, mode=None)
```

Properties:

- `type: str` - normalized unit type.
- `model: str` - resolved exact model id.
- `model_info: ModelInfo | None` - catalog entry.
- `mode: str | None` - selected runtime mode for this unit.
- `reasoning: bool | None` - unit default for reasoning-capable LLMs.
- `options: dict[str, Any]` - runtime options attached to the unit.
- `rag: Unit | None` - attached RAG service for LLM units.
- `id: str` - local stable id in the form `<type>:<modelId>`.
- `label: str` - catalog label, or model id if metadata is absent.
- `supports_reasoning: bool` - catalog-derived reasoning capability.

Methods:

- `to_payload() -> dict[str, Any]`
  Returns the bridge payload: `{"type": type, "model": model, ...}`.
- `to_dict() -> dict[str, Any]`
  Returns id, type, model, label, and model metadata.
- `status() -> dict[str, Any]`
  Returns attached runtime status when the unit belongs to a runtime; otherwise
  returns an offline selected-state dictionary.
- `remove() -> dict[str, Any]`
  Removes the unit from its attached runtime without deleting model cache.
- `delete(delete_cache=True, bridge=None) -> dict[str, Any]`
  If attached to a runtime, removes it from that runtime. If `delete_cache=True`,
  asks the selected bridge to delete the model cache. For `RAG` and
  `vectorstorage`, `delete(ids=None, filter=None)` deletes documents or vector
  records instead.
- `delete_cache(bridge=None) -> dict[str, Any]`
  Deletes selected-mode cache for this model through a bridge.
- `set_reasoning(enabled) -> dict[str, Any]`
  Updates local reasoning setting and pushes the change into the running runtime
  when attached.
- `as_runtime(port=1146) -> Runtime`
  Creates or reuses a single-unit runtime.
- `install(port=1146) -> dict[str, Any]`
  Convenience wrapper for `unit.as_runtime(port).install()`.
- `run(port=1146) -> dict[str, Any]`
  Convenience wrapper for `unit.as_runtime(port).run()`.
- `stop() -> dict[str, Any]`
  Stops the single-unit runtime.
- `hibernate() -> dict[str, Any]`
  Hibernates the single-unit runtime.
- `heatup() -> dict[str, Any]`
  Heats up the single-unit runtime.
- `invoke(endpoint, payload, timeout=None) -> dict[str, Any]`
  Invokes an endpoint through the single-unit runtime.
- `add(documents, ids=None, metadatas=None, embeddings=None, **params) -> dict[str, Any]`
  Adds documents to a `RAG` unit, or explicit text+embedding records to a
  `vectorstorage` unit.
- `search(query=None, embedding=None, top_k=None, filter=None, **params) -> dict[str, Any]`
  Searches a `RAG` unit by text query, or a `vectorstorage` unit by explicit
  embedding.
- `clear(**params) -> dict[str, Any]`
  Clears the configured RAG/vector namespace.
- `stats() -> dict[str, Any]`
  Returns vector/RAG storage stats from the active runtime.
- `reindex(**params) -> dict[str, Any]`
  Re-embeds existing RAG chunks with the current embedding model.

### `Runtime`

`Runtime` is a Python-side runtime definition and controller. It owns a set of
units and communicates through one bridge.

Constructor:

```python
Runtime(units, *, port=1146, bridge=None, runtime_id=None, mode=None)
```

Use `xlocllm.runtime(...)` unless you need direct class construction.

Properties:

- `id: str` - runtime registry id.
- `mode: str` - selected runtime mode, `"native"` or `"web"`.
- `port: int` - bridge port.
- `bridge: Bridge | NativeBridge | None` - attached bridge object.
- `window_handle: WindowHandle | None` - dashboard/browser window handle if opened by SDK.
- `installed: bool` - Python-side install state flag.
- `running: bool` - Python-side run state flag.
- `base_url: str` - bridge base URL, for example `http://127.0.0.1:1146`.
- `url: str` - OpenAI-compatible URL, for example `http://127.0.0.1:1146/v1`.
- `unit_requests: list[dict[str, Any]]` - bridge payload objects for all units.

Methods:

- `add_unit(unit, activate=True) -> Unit`
  Adds a `Unit` or `UnitRequest`. If runtime is already running and a bridge is
  attached, `activate=True` asks the selected backend to start that model.
- `remove_unit(unit_id, delete_cache=False) -> dict[str, Any]`
  Removes a unit by `unit.id`, model id, or unit type. With `delete_cache=True`,
  asks the bridge to delete model cache.
- `unit_status(unit_id) -> dict[str, Any]`
  Returns the best available backend state for a unit.
- `configure_unit(unit_id, reasoning=None, options=None) -> dict[str, Any]`
  Updates unit options. If runtime is running, sends the update to the active
  backend without recreating the Python object.
- `set_reasoning(unit_id, enabled) -> dict[str, Any]`
  Convenience wrapper for `configure_unit(..., reasoning=enabled)`.
- `units(as_dict=False, state=False) -> list[Any]`
  Returns configured `Unit` objects, dictionaries, or backend-reported unit
  states when `state=True`.
- `models() -> list[dict[str, Any]]`
  Returns backend model states if available; otherwise returns configured
  unit dictionaries.
- `install(port=None) -> dict[str, Any]`
  Starts the selected bridge daemon and requests engine/model installation. Web
  mode opens the paired browser and waits for pairing; native mode starts the
  local supervisor and opens the dashboard.
- `run(port=None) -> dict[str, Any]`
  Ensures install has happened and starts all configured units.
- `stop() -> dict[str, Any]`
  Stops running models and closes the owned dashboard/browser window.
- `hibernate() -> dict[str, Any]`
  Unloads active models but keeps them selected.
- `heatup() -> dict[str, Any]`
  Starts active models and performs a small warmup for supported units.
- `status() -> dict[str, Any]`
  Returns runtime id, URL, mode, configured units, bridge process info, and backend
  status snapshot when reachable.
- `health() -> dict[str, Any]`
  Returns bridge health.
- `logs(limit=200) -> list[dict[str, Any]]`
  Returns bridge/backend runtime logs.
- `invoke(endpoint, payload, timeout=None) -> dict[str, Any]`
  Calls `/xlocllm/v1/invoke/{endpoint}`.
- `client(api_key="xlocllm", **kwargs) -> Any`
  Creates an `openai.OpenAI` client bound to `runtime.url`. Requires optional
  `openai` package.
- `chat(prompt=None, messages=None, model=None, use_rag=None, **params) -> dict[str, Any]`
  Convenience wrapper for `chat.completions`. When the selected LLM has `rag`,
  retrieval runs automatically unless `use_rag=False`.
- `embed(input, model=None) -> list[Any]`
  Convenience wrapper for `embeddings`.
- `open() -> WindowHandle`
  Opens or reopens the native dashboard or browser UI for the attached bridge.
- `chatui(model=None, session="default", use_rag=True, open_browser=True, width=760, height=860) -> WindowHandle`
  Opens a chat window backed by the running runtime.
- `close() -> dict[str, Any]`
  Shuts down the bridge and removes runtime registry state.
- `wait_ready(timeout=None, require_browser=False) -> Runtime`
  Waits until the bridge is reachable, and optionally until the web browser is paired.
- `__enter__() -> Runtime`, `__exit__(...) -> False`
  Context-manager support for cleanup.

### `Bridge` / `NativeBridge`

`Bridge` is the local HTTP/WebSocket control plane for web mode. `NativeBridge`
is the local control plane for native mode and exposes the same main SDK-facing
methods.

Constructor:

```python
Bridge(port=1146, ttl=None, live_time=None)
```

Properties:

- `port: int`
- `ttl: float | None` - reserved field; currently not enforced.
- `live_time: float | None` - optional server lifetime in seconds.
- `token: str` - browser pairing token.
- `base_url: str` - `http://127.0.0.1:<port>`.
- `url: str` - `http://127.0.0.1:<port>/v1`.

Methods:

- `activate(daemon=False) -> Bridge`
  Starts the bridge if it is not already healthy. With `daemon=True`, starts a
  detached Python process. Otherwise starts a daemon thread.
- `close() -> dict[str, Any]`
  Requests bridge shutdown and removes bridge registry entry.
- `status() -> dict[str, Any]`
  Calls `/xlocllm/v1/status`.
- `health() -> dict[str, Any]`
  Calls `/health`.
- `models() -> list[dict[str, Any]]`
  Returns catalog models from bridge or local fallback.
- `units() -> list[dict[str, Any]]`
  Returns unit definitions from bridge or local fallback.
- `logs(limit=200) -> list[dict[str, Any]]`
  Returns bridge/backend logs.
- `wait_ready(timeout=None, require_browser=False) -> Bridge`
  Waits for bridge health and optionally browser pairing.
- `reload(units=None) -> dict[str, Any]`
  Stops and reruns the backend runtime with supplied units.
- `set_active(unit, active=True, model=None) -> dict[str, Any]`
  Starts a model for `active=True`; deactivates a model through `runtime/set_active`
  for `active=False`.
- `delete_model(unit_or_model, model=None) -> dict[str, Any]`
  Requests model cache deletion.
- `delete_all_models(confirm=True) -> dict[str, Any]`
  Deletes all known model cache entries. Raises if `confirm=False`.
- `invoke(endpoint, payload, timeout=None) -> dict[str, Any]`
  Calls `/xlocllm/v1/invoke/{endpoint}`.
- `processes() -> dict[str, Any]`
  Returns bridge and window/dashboard PIDs with alive flags.

### `BridgeGroup`

`BridgeGroup` is returned by `GetBridge()` when no port is provided.

Properties:

- `bridges: list[Bridge]`

Methods:

- `__iter__()`
- `__len__()`
- `activate(daemon=False) -> list[Bridge]`
- `close() -> list[dict[str, Any]]`
- `status() -> list[dict[str, Any]]`
- `health() -> list[dict[str, Any]]`

### `WindowHandle`

Returned by `xlocllm.window(...)` and `Runtime.open()`.

Properties:

- `port: int`
- `url: str`
- `pid: int | None`
- `owned: bool`

Methods:

- `close() -> None`
  Closes the owned browser process tree when possible.

### `UnitRequest`

Low-level dataclass used for bridge payloads.

Properties:

- `type: str`
- `model: str`
- `reasoning: bool | None`
- `options: dict[str, Any] | None`

Methods:

- `to_payload() -> dict[str, Any]`

### Exceptions

- `XlocLLMError` - base SDK exception.
- `BridgeNotReady` - bridge cannot be reached.
- `BrowserNotConnected` - bridge is up but browser runtime is not paired.
- `ModelNotFound` - model name/alias does not resolve.
- `UnitNotFound` - unit type does not resolve.
- `RuntimeNotFound` - runtime id is unknown.
