# xlocllm

`xlocllm` is a local browser inference manager for AI/ML models, runnig from python or typescript (soon). xlocllm uses WebGPU and NPU to run models. This is one of the easiest ways to run LLM on your PC. Created by Droidje AI.

`217 models are available now! (LLM, emeddings, rerankers, VLM, OCR, TTS and more)`

## Install

```powershell
pip install xlocllm
```

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

Without WebGPU, ask for the CPU/WASM-compatible catalog:

```python
models = xlocllm.models(webgpu=False)
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

## Python SDK

The Python package lives in [`python/xlocllm`](python/xlocllm).

Core objects:

- `ModelInfo` - catalog entry with model metadata and hardware requirements.
- `Unit` - one capability/model pair.
- `Runtime` - group of units running together.
- `Bridge` - local HTTP/WebSocket process.

Useful helpers:

```python
xlocllm.models(unit="LLM", max_vram_mb=1500)
xlocllm.models(webgpu=False)
xlocllm.model("Qwen-3.5-0.8b", unit="LLM")
xlocllm.bridges()
xlocllm.runtimes()
xlocllm.status()
xlocllm.benchmark()
xlocllm.benchmark("LLM")
```

`benchmark()` temporarily opens a paired mini browser by default to detect real
WebGPU/WebNN/NPU support, then closes it. With a unit type, it returns `fast`
and `quality` model recommendations for the detected device.

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
xlocllm models --unit LLM --no-webgpu
xlocllm run --unit LLM --model "Qwen-3.5-0.8b"
```

## Documentation

- Full English SDK docs: [`python/xlocllm/docs.md`](python/xlocllm/docs.md)
- Full Russian SDK docs: [`python/xlocllm/docs_ru.md`](python/xlocllm/docs_ru.md)
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

MIT
