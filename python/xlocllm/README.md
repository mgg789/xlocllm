# xlocllm

`xlocllm` is a Python SDK for local browser-backed AI inference. It exposes an
OpenAI-compatible loopback API from Python while running model weights in a
paired browser window through WebGPU/WebNN with MLC WebLLM and Transformers.js.

The goal is simple:

```powershell
pip install xlocllm
```

Then:

```python
import xlocllm

llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b")
runtime = xlocllm.runtime([llm])
runtime.run()

print(runtime.url)  # http://127.0.0.1:1146/v1
print(runtime.chat("Say hello", temperature=0))
```

## What It Does

- Starts a local FastAPI bridge on `127.0.0.1`.
- Opens a paired browser app window.
- Runs models inside the browser runtime.
- Provides OpenAI-compatible `/v1` endpoints for local clients.
- Supports LLMs, embeddings, rerankers, translation, TTS, vision, ASR, and more
  through a shared catalog.
- Provides browser-local RAG with IndexedDB vector storage, embeddings,
  optional reranking, automatic LLM retrieval, and `runtime.chatui()`.
- Keeps Python-side objects for models, units, runtimes, and bridges.

## Install

```powershell
pip install xlocllm
```

Optional OpenAI client helper:

```powershell
pip install "xlocllm[openai]"
```

Development install from this repository:

```powershell
python -m pip install -e .\python\xlocllm[dev,openai]
```

## Quick Start

```python
import xlocllm

runtime = xlocllm.runtime(
    [
        xlocllm.unit("LLM", "Qwen-3.5-0.8b"),
        xlocllm.unit("embedding", "multilingual-e5-small"),
    ]
)

runtime.install()
runtime.run()

print(runtime.status())
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

With the optional helper:

```python
client = runtime.client()
```

## Browser-Local RAG

```python
import xlocllm

emb = xlocllm.unit("embedding", "multilingual-e5-small")
rag = xlocllm.rag(emb=emb, name="kb")
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", rag=rag)

with xlocllm.runtime([llm]) as runtime:
    runtime.run()
    rag.add(["xlocllm keeps vector stores in browser IndexedDB."], ids=["storage"])
    print(runtime.chat("Where does xlocllm keep vectors?"))
    runtime.chatui(session="kb-demo")
```

## Core API

```python
model = xlocllm.model("Qwen-3.5-0.8b", unit="LLM")
models = xlocllm.models(unit="LLM", max_vram_mb=1500)
cpu_models = xlocllm.models(webgpu=False)

unit = xlocllm.unit("LLM", "Qwen-3.5-0.8b", reasoning=None)
store = xlocllm.vectorstorage("kb")
rag = xlocllm.rag(emb=xlocllm.unit("embedding", "multilingual-e5-small"), store=store)
runtime = xlocllm.runtime([unit], port=1146)
bridge = xlocllm.Bridge(port=1146)

print(runtime.url)
print(bridge.url)
print(xlocllm.bridges())
print(xlocllm.runtimes())
print(xlocllm.status())
print(xlocllm.benchmark())
print(xlocllm.benchmark("LLM"))
```

`benchmark()` temporarily opens a paired mini browser by default to detect real
WebGPU/WebNN/NPU support, then closes it. With a unit type, it returns `fast`
and `quality` recommendations.

Reasoning-capable LLMs can be configured at creation and updated hot:

```python
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", reasoning=False)
runtime.set_reasoning(llm.id, True)
```

CLI:

```powershell
xlocllm status
xlocllm benchmark
xlocllm benchmark LLM
xlocllm models --unit LLM --no-webgpu
xlocllm run --unit LLM --model "Qwen-3.5-0.8b"
```

## Documentation

- Full English SDK docs: [`docs.md`](https://github.com/mgg789/xlocllm/blob/main/python/xlocllm/docs.md)
- Full Russian SDK docs: [`docs_ru.md`](https://github.com/mgg789/xlocllm/blob/main/python/xlocllm/docs_ru.md)
- Ready-to-run Russian recipes: [`recipes_ru.md`](https://github.com/mgg789/xlocllm/blob/main/python/xlocllm/recipes_ru.md)
- English model catalog: [`models.md`](https://github.com/mgg789/xlocllm/blob/main/python/xlocllm/models.md)
- Russian model catalog: [`models_ru.md`](https://github.com/mgg789/xlocllm/blob/main/python/xlocllm/models_ru.md)

## Model Lookup

Use exact `modelId`, `label`, or aliases:

```python
xlocllm.unit("LLM", "Qwen-3.5-0.8b")
xlocllm.unit("LLM", "Qwen3.5-0.8B-q4f16_1-MLC")
xlocllm.unit("embedding", "multilingual-e5-small")
```

Browse the complete catalog in [`models.md`](https://github.com/mgg789/xlocllm/blob/main/python/xlocllm/models.md).

## Local State

By default, xlocllm stores bridge metadata and browser profiles under:

- Windows: `%LOCALAPPDATA%\xlocllm`
- Linux/macOS: `$XDG_STATE_HOME/xlocllm` or `~/.local/state/xlocllm`

Environment variables:

- `XLOCLLM_HOME` - override local state directory.
- `XLOCLLM_WEB_URL` - use a custom web runtime URL.
- `XLOCLLM_LOG_LEVEL` - uvicorn log level.

## Development Checks

```powershell
python -m pytest python/xlocllm/tests
python -m ruff check python/xlocllm/src python/xlocllm/tests
python -m mypy python/xlocllm/src
```

Build the Python package:

```powershell
cd python\xlocllm
python -m build
```

## Notes

The bridge binds to loopback only. The browser window must remain open while
browser-backed models are running. Without WebGPU, xlocllm exposes only the
CPU/WASM-compatible Transformers.js subset and rejects heavier models before
loading.

## License

MIT
