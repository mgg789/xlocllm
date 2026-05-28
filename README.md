# xlocllm

`xlocllm` is a local inference manager for AI/ML models from Python. The default
runtime is now `native`: it runs local engine processes, exposes an
OpenAI-compatible loopback API, and can use CUDA, DirectML, Metal/CoreML-adjacent
providers, or CPU depending on the model backend. The browser/WebGPU runtime is
still available with `mode="web"` for full backward compatibility. Created by
Droidje AI.

The native catalog starts with a stable MVP matrix across LLM, embeddings,
rerankers, vision, OCR, ASR, TTS, translation, and other task classes. The web
catalog still exposes the browser-ready `packages/catalog` model set.

Includes local RAG: persistent vector stores, embedding + optional reranker
pipelines, automatic retrieval for LLM units, and `runtime.chatui()`.

## Install

```powershell
pip install xlocllm
```

The base install stays light. In `native` mode, xlocllm downloads managed engine
dependencies and model artifacts into the xlocllm cache on the first
`runtime.run()`.

Optional OpenAI client helper:

```powershell
pip install "xlocllm[openai]"
```

## Quick Start

```python
import xlocllm

runtime = xlocllm.runtime([
    xlocllm.unit("LLM", "Qwen-3.5-0.8b"),
    xlocllm.unit("embedding", "multilingual-e5-small"),
])

runtime.run()

print(runtime.url)       # http://127.0.0.1:1146/v1
print(runtime.status())  # bridge, runtime, models, metrics
```

Use the browser/WebGPU runtime explicitly when you need the old browser-backed
behavior:

```python
xlocllm.mode = "web"
# or: runtime = xlocllm.runtime([...], mode="web")
```

In browser mode without WebGPU, ask for the CPU/WASM-compatible catalog:

```python
models = xlocllm.models(mode="web", webgpu=False)
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

## Local RAG

```python
import xlocllm

emb = xlocllm.unit("embedding", "multilingual-e5-small")
rag = xlocllm.rag(emb=emb, name="kb")
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", rag=rag)

with xlocllm.runtime([llm]) as runtime:
    runtime.run()
    rag.add(["xlocllm keeps vectors in the active runtime storage."], ids=["storage"])
    print(runtime.chat("Where does xlocllm keep vectors?"))
    runtime.chatui(session="kb-demo")
```

Native mode uses local persistent storage. Browser mode uses IndexedDB in the
paired browser runtime.

## Python SDK

The Python package lives in [`python/xlocllm`](python/xlocllm).

Core objects:

- `ModelInfo` - catalog entry with model metadata and hardware requirements.
- `Unit` - model-backed, service, or composite capability.
- `Runtime` - group of units running together.
- `Bridge` / `NativeBridge` - local HTTP control process for the selected mode.

Useful helpers:

```python
xlocllm.models(unit="LLM", max_vram_mb=1500)
xlocllm.models(mode="web", webgpu=False)
xlocllm.models(mode="native")
xlocllm.model("Qwen-3.5-0.8b", unit="LLM")
xlocllm.bridges()
xlocllm.runtimes()
xlocllm.status()
xlocllm.benchmark()
xlocllm.benchmark("LLM")
xlocllm.benchmark("LLM", mode="web")
```

`benchmark()` checks local CPU/RAM/disk, native engine availability, GPU/NPU
signals, and Hugging Face latency. In `mode="web"` it can temporarily open a
paired mini browser to detect real WebGPU/WebNN/NPU support. With a unit type,
it returns `fast` and `quality` model recommendations for the detected device.

Reasoning-capable LLM families can be configured at unit creation or while the
runtime is running:

```python
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", reasoning=False)
runtime.set_reasoning(llm.id, True)
```

CLI:

```powershell
xlocllm status
xlocllm benchmark
xlocllm benchmark LLM
xlocllm benchmark LLM --mode web
xlocllm models --unit LLM
xlocllm models --unit LLM --mode web --no-webgpu
xlocllm run --unit LLM --model "Qwen-3.5-0.8b"
xlocllm run --unit LLM --model "Qwen-3.5-0.8b" --mode web
```

## Documentation

- Repository: [`mgg789/xlocllm`](https://github.com/mgg789/xlocllm/)
- Python Unit wiki for AI/tools: [`Python-Unit`](https://github.com/mgg789/xlocllm/wiki/Python-Unit)
- Full English SDK docs: [`python/xlocllm/docs.md`](python/xlocllm/docs.md)
- Full Russian SDK docs: [`python/xlocllm/docs_ru.md`](python/xlocllm/docs_ru.md)
- Ready-to-run Russian recipes: [`python/xlocllm/recipes_ru.md`](python/xlocllm/recipes_ru.md)
- English model catalog: [`python/xlocllm/models.md`](python/xlocllm/models.md)
- Russian model catalog: [`python/xlocllm/models_ru.md`](python/xlocllm/models_ru.md)
- Publishing instructions: [`python/xlocllm/PUBLISHING.md`](python/xlocllm/PUBLISHING.md)

## Repository Layout

- `python/xlocllm` - Python SDK, bridge server, docs, and package metadata.
- `apps/web` - browser runtime UI and model host.
- `packages/catalog` - shared model catalog.
- `deploy/docker` - local Docker workflow for the web app.

## Development

```powershell
pnpm install
pnpm build
pnpm test

python -m pip install -e .\python\xlocllm[dev,openai]
python -m pytest python/xlocllm/tests
python -m ruff check python/xlocllm/src python/xlocllm/tests
python -m mypy python/xlocllm/src
```

Build the Python package:

```powershell
cd python\xlocllm
python -m build
```

## Docker Web Runtime

```powershell
docker compose -f deploy/docker/docker-compose.yml up --build
```

The web app is served on `http://127.0.0.1:8080`.

## License

BSD-3-Clause. Redistributions must retain the copyright notice:
`Copyright (c) 2026, mgg789 / Droidje AI`.
