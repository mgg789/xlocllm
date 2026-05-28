# xlocllm Python SDK

`xlocllm` - локальный Python SDK для запуска AI/ML моделей с единым API и двумя
режимами runtime. По умолчанию используется `native`: Python поднимает локальный
supervisor, отдает OpenAI-compatible API на `127.0.0.1` и запускает локальные
engine вроде llama.cpp/GGUF для LLM и ONNX Runtime для embeddings, rerank,
vision, audio, OCR и других task-моделей.

Старый browser/WebGPU runtime сохранен как `mode="web"`. Он по-прежнему запускает
модели в связанном окне браузера через WebGPU/WebNN, MLC WebLLM или
Transformers.js.

Ссылки на проект и документацию доступны прямо из Python-пакета, чтобы агенты и
инструменты могли сами находить актуальные docs:

```python
import xlocllm

print(xlocllm.PROJECT_URLS)
print(xlocllm.DOCUMENTATION_URL)  # https://github.com/mgg789/xlocllm/wiki/Python-Unit
```

- Repository: <https://github.com/mgg789/xlocllm/>
- Python Unit wiki: <https://github.com/mgg789/xlocllm/wiki/Python-Unit>

## Установка

```powershell
python -m pip install -e .\python\xlocllm
```

Метаданные пакета:

- Python: `>=3.10`
- базовые runtime-зависимости: `fastapi`, `uvicorn[standard]`, `pydantic`
- CLI entry points: `xlocllm`, `xlocllm-bridge`

Базовая установка остается легкой. В `native` режиме недостающие engine
зависимости и model artifacts скачиваются в cache xlocllm при первом
`runtime.run()`. Чтобы запретить автоустановку native engine и получать явную
диагностическую ошибку, установите `XLOCLLM_NATIVE_DISABLE_INSTALL=1`.

## Основные сущности

В новой схеме SDK есть четыре основные сущности:

- `ModelInfo` - запись каталога модели с runtime и hardware-характеристиками.
- `Unit` - пара capability/model, например `LLM + Qwen`.
- `Runtime` - набор units, которые надо держать вместе в выбранном runtime.
- `Bridge` / `NativeBridge` - локальный HTTP процесс управления для выбранного режима.

Глобальный режим:

```python
import xlocllm

print(xlocllm.mode)  # native
xlocllm.mode = "web"  # явно включить старый browser/WebGPU runtime
```

Scoped-режимы можно задавать декораторами или context manager'ами. Они временно
меняют default для создаваемых внутри `unit(...)`, а после выхода восстанавливают
предыдущее состояние:

```python
@xlocllm.webgpu
def run_webgpu():
    llm = xlocllm.unit("LLM", "SmolLM2-360M-Instruct-q4f16_1-MLC")

with xlocllm.web:
    clf = xlocllm.unit("text-classification", "Xenova/distilbert-base-uncased-finetuned-sst-2-english")

with xlocllm.native:
    llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b")
```

`xlocllm.webgpu` означает `mode="web"` и default `options.device="webgpu"`.
`xlocllm.web` означает `mode="web"` и default `options.device="wasm"`.
`xlocllm.native` возвращает запуск к локальному native runtime.

## Быстрый старт

```python
import xlocllm

llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b")
emb = xlocllm.unit("embedding", "multilingual-e5-small")

runtime = xlocllm.runtime([llm, emb], port=1146)
runtime.install()
runtime.run()

print(runtime.url)       # http://127.0.0.1:1146/v1
print(runtime.status())  # полный словарь состояния bridge/runtime
```

Одиночный unit тоже можно запускать напрямую:

```python
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b")
llm.install()
llm.run()
```

Поддерживается context manager с автоматической очисткой:

```python
with xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b")]) as runtime:
    runtime.run()
    print(runtime.chat("Привет", temperature=0))
```

## OpenAI-compatible API

```python
import xlocllm
from openai import OpenAI

llm = xlocllm.unit(type="LLM", model="Qwen-3.5-0.8b-fp32")
client = OpenAI(base_url="http://127.0.0.1:1146/v1", api_key="xlocllm")

with xlocllm.runtime([llm]) as runtime:
    runtime.run()
    response = client.chat.completions.create(
        model="Qwen-3.5-0.8b-fp32",
        messages=[{"role": "user", "content": "Что такое лидар"}],
        max_tokens=64,
    )
    print(response.choices[0].message.content)
```

Поддерживаемые OpenAI-like endpoints:

- `GET /v1/models`
- `POST /v1/chat/completions`
- `POST /v1/chat/completions` с `stream=True`
- `POST /v1/responses`
- `POST /v1/embeddings`

## Top-Level API

### `xlocllm.unit(type, model, quant=None, reasoning=None, options=None, rag=None, mode=None)`

Создает `Unit`, нормализуя тип и имя модели через каталог. `quant` работает для
native GGUF LLM и принимает значения вроде `"q2"`, `"q4"`, `"q8"`, `"fp16"`,
`"fp32"`. Если параметр не указан, xlocllm сначала просит `q4`, затем откатывается
к `q8`, `fp16`, `fp32` и другим доступным GGUF-квантованиям, не меняя публичное
имя модели. `reasoning` включает или выключает thinking/reasoning для
LLM-семейств, которые это поддерживают. `options` передается в выбранный runtime
как настройки unit. `mode=None` берет `xlocllm.mode`; по умолчанию это
`"native"`. Для LLM можно передать `rag=<RAG unit>`, тогда chat-запросы будут
автоматически делать retrieval перед генерацией.

```python
unit = xlocllm.unit("chat", "qwen-0.8b")
q8 = xlocllm.unit("LLM", "Qwen-3.5-0.8b", quant="q8")
print(unit.type)   # LLM
print(unit.mode)   # native
```

Модель можно указывать через точный `modelId`, `label` или любой alias из
каталога.

Service units не требуют модели из каталога. Например,
`xlocllm.unit("regression", "...", options={"model_path": "model.onnx"})`
создает native ONNX unit; после подключения к запущенному runtime его можно
вызывать через `unit.predict([[...]])`.

Дополнительные формы:

```python
info = xlocllm.model("Qwen-3.5-0.8b", unit="LLM")
llm = xlocllm.unit(info)

clf = xlocllm.unit(
    sklearn_model,
    type="text-classification",
    name="clf",
    labels=["no", "yes"],
)
reg = xlocllm.unit("model.onnx", type="regression", name="reg", input_name="float_input")

with xlocllm.unit(info) as unit:
    ...
```

Custom sklearn и torch модели экспортируются в ONNX. В `native` режиме они
запускаются через ONNX Runtime. В `web` режиме SDK регистрирует ONNX artifact на
локальном bridge, а связанное browser-окно выполняет модель через ONNX Runtime
Web/WASM.

### `xlocllm.vectorstorage(name="default", backend="indexeddb", metric="cosine", persist=True, namespace="default", options=None, mode=None)`

Создает сервисный unit для локального vector storage. В `native` режиме дефолтный
backend автоматически становится native persistent store. В `web` режиме дефолт
остается browser IndexedDB. Для временного индекса используйте `persist=False`
или `backend="memory"`. `metric`: `cosine`, `dot`, `euclidean`.

```python
store = xlocllm.vectorstorage(name="docs", namespace="kb")
```

Низкоуровневый `vectorstorage` требует готовые embeddings. Обычно удобнее
использовать `xlocllm.rag(...)`: он сам чанкует текст, вызывает embedding model
и пишет векторные записи.

### `xlocllm.rag(emb, rerank=None, store=None, name="default", chunk_size=800, chunk_overlap=120, top_k=5, candidate_k=30, score_threshold=None, options=None, mode=None)`

Создает высокоуровневый RAG unit. `emb` должен быть embedding unit. `rerank`
опционален и должен быть reranker unit. Если `store` не указан, xlocllm создаст
vector store `<name>-store` в выбранном режиме.

```python
emb = xlocllm.unit("embedding", "multilingual-e5-small")
rerank = xlocllm.unit("reranker", "bge-reranker-base")
rag = xlocllm.rag(emb=emb, rerank=rerank, name="kb")
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", rag=rag)
```

### `xlocllm.runtime(units, port=1146, bridge=None, runtime_id=None, mode=None)`

Создает `Runtime` из объектов `Unit` или `UnitRequest`. `mode=None` берет
`xlocllm.mode`; передайте `mode="web"`, чтобы явно использовать
browser/WebGPU backend только для этого runtime.

```python
runtime = xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b")], port=12000)
web_runtime = xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b", mode="web")], mode="web")
```

### `xlocllm.models(..., mode=None, installed=None, hardware=None, include_unavailable=False, quant=None, subtype=None, modality=None, use_case=None, license=None, min_context=None)`

Возвращает модели каталога как `ModelInfo`.

Фильтры:

- `unit`
- `runtime`
- `task`
- `task_group`
- `hardware_tier`
- `language`
- `provider`
- `availability`
- `npu`
- `webgpu` - `False` возвращает только модели, доступные без WebGPU через CPU/WASM
- `cpu` - алиас для CPU/WASM fallback
- `available_without_webgpu`
- `search`
- `max_vram_mb`
- `max_disk_mb`
- `max_size_gb`
- `max_parameters_b`
- `subtype` - подтип внутри класса, например `reasoning`, `chat`,
  `multilingual-retrieval`, `cross-encoder`, `caption-vqa`
- `modality` - входная/выходная модальность из `modalities`, например `text`,
  `image`, `audio`, `speech`
- `use_case` - сценарий из `useCases`, например `rag`, `agent`, `captioning`,
  `translation`, `classification`
- `license` - точное имя лицензии в metadata
- `min_context` - минимальная длина контекста для LLM/VLM/code моделей
- `limit_per_unit`
- `mode` - `"native"` или `"web"`; по умолчанию `xlocllm.mode`
- `installed` - фильтр по установленным artifacts, если доступны bridge/status данные
- `hardware` - опциональный снимок железа для native-фильтрации
- `include_unavailable` - показать native-записи даже если engine/hardware policy
  считает их недоступными
- `quant` - выбрать GGUF-квантование в metadata для native LLM

Пример:

```python
small_llms = xlocllm.models(unit="LLM", max_vram_mb=1500, search="qwen")
native_llms = xlocllm.models(unit="LLM", mode="native")
cpu_web_models = xlocllm.models(unit="LLM", mode="web", webgpu=False)
rag_embeddings = xlocllm.models(unit="embedding", mode="native", use_case="rag", modality="text")
reasoning_llms = xlocllm.models(unit="LLM", mode="native", subtype="reasoning", min_context=8192)
```

Native-каталог вынесен в `packages/catalog/native-models.json` и packaged copy
`xlocllm/data/native_models.json`. Сейчас он содержит 300 записей в разных
классах: LLM, embeddings, rerankers, VLM, translation, ASR, TTS, OCR, vision,
classification, summarization, code и другие task-модели. LLM, embeddings,
reranker и VLM расширены сильнее остальных, чтобы покрыть разные размеры,
языки, архитектуры и сценарии.

В `web` режиме при `webgpu=False` исключаются MLC/WebLLM модели и тяжелые Transformers.js
модели. В fallback-каталоге остается минимум одна usable-модель для каждого
типа unit, если в каталоге есть подходящий Transformers.js кандидат.

### `xlocllm.model(name, unit=None, mode=None, quant=None)`

Возвращает одну модель как `ModelInfo`.

```python
info = xlocllm.model("Qwen-3.5-0.8b", unit="LLM")
q8 = xlocllm.model("Qwen-3.5-0.8b", unit="LLM", quant="q8")
print(info.model_id)
print(info.to_dict())
```

У native-записей в `to_dict()` есть backend-поля вроде `backend`, `format`,
`repo`, `files`, `quantization`, `providers`, `ram_mb`, `vram_mb`, `disk_mb`,
`verified`, если они известны.

### `xlocllm.bridges(active_only=True)`

Возвращает известные `Bridge` из локального registry.

### `xlocllm.runtimes(active_only=True)`

Возвращает известные `Runtime` из локального registry.

### `xlocllm.status()`

Возвращает словарь, где собраны:

- известные bridges;
- известные runtimes;
- установленные и запущенные модели, если runtime отдает такие данные;
- resource metrics, которые отдает backend;
- количество моделей в каталоге.

### `xlocllm.benchmark(type=None, mode=None, ping_hf=True, timeout=2.0, browser=True, browser_timeout=15.0, port=None)`

Возвращает словарь с параметрами системы, RAM, свободным местом на диске,
native hardware/engine availability, optional browser capabilities и latency до
Hugging Face. В native режиме браузер для запуска моделей не нужен. В web режиме
`browser=True` поднимает временный local bridge и mini browser window, получает
реальные `webgpu`/`webnn`/`npu` capability и закрывает временные процессы после
замера.

Если передать `type`, benchmark дополнительно вернет две рекомендации для этого
unit type:

- `fast` - легкая модель, которая должна работать быстро и стабильно.
- `quality` - самая сильная модель, которая выглядит посильной для устройства.

```python
system = xlocllm.benchmark()
llm_fit = xlocllm.benchmark("LLM")
```

Для CI/headless-сценариев используйте `browser=False`, чтобы не открывать окно.

## Unit API

Свойства:

- `unit.id` - локальный id вида `<type>:<modelId>`
- `unit.type`
- `unit.model`
- `unit.label`
- `unit.model_info`
- `unit.mode`
- `unit.quant` - выбранное GGUF-квантование для native LLM, если применимо
- `unit.reasoning`
- `unit.options`
- `unit.rag` - подключенный RAG unit для LLM, если настроен
- `unit.supports_reasoning`

Методы:

- `unit.to_payload()` - `{"type": ..., "model": ...}`
- `unit.to_dict()` - payload, label и metadata модели
- `unit.status()` - состояние unit в attached runtime
- `unit.remove()` - убрать из attached runtime без удаления cache
- `unit.delete_cache(bridge=None)` - удалить cache модели в выбранном backend
- `unit.delete(delete_cache=True, bridge=None)` - убрать из runtime и при необходимости удалить model cache
- `unit.set_reasoning(enabled)` - горячо поменять reasoning-настройку для unit
- `unit.as_runtime(port=1146)` - создать или переиспользовать runtime для одного unit
- `unit.install(port=1146)`
- `unit.run(port=1146)`
- `unit.stop()`
- `unit.hibernate()`
- `unit.heatup()`
- `unit.invoke(endpoint, payload, timeout=None)`
- `unit.add(documents, ids=None, metadatas=None, embeddings=None, **params)` - для `RAG` и `vectorstorage`
- `unit.search(query=None, embedding=None, top_k=None, filter=None, **params)` - для `RAG` и `vectorstorage`
- `unit.delete(ids=None, filter=None, **params)` - удалить документы RAG или vector records
- `unit.clear(**params)` - очистить namespace RAG/vector store
- `unit.stats()` - статистика RAG/vector storage
- `unit.reindex(**params)` - переэмбеддить существующие RAG chunks
- `unit.predict(inputs, **params)` - выполнить custom native ONNX/regression unit

## Runtime API

Свойства:

- `runtime.id`
- `runtime.mode`
- `runtime.port`
- `runtime.base_url` - `http://127.0.0.1:<port>`
- `runtime.url` - `http://127.0.0.1:<port>/v1`
- `runtime.bridge`
- `runtime.installed`
- `runtime.running`
- `runtime.unit_requests`

Методы:

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

`runtime.remove_unit()` принимает `unit.id`, `modelId` или тип unit. Если runtime
запущен и `delete_cache=False`, SDK попросит выбранный backend деактивировать
модель. Если `delete_cache=True`, SDK дополнительно запросит очистку cache
модели.

`runtime.open()` открывает dashboard. В web mode это остается paired browser
mini-window, в котором живет browser runtime. В native mode открывается
небраузерное desktop-окно со статусом, метриками, логами и кнопками
Start/Pause/Clear; сами native-модели выполняются в локальных Python/native
engine, а не внутри этого окна.

## RAG и Vector Storage

RAG исполняется внутри активного runtime:

1. `rag.add(...)` чанкует документы.
2. Настроенный embedding unit считает embedding для каждого chunk.
3. Векторы и metadata сохраняются в backend storage выбранного режима.
4. `rag.search(...)` эмбеддит query, ищет кандидаты, опционально rerank-ит их и
   возвращает `results` плюс собранный `context`.

В native режиме storage локальный и persistent внутри cache xlocllm. В web режиме
storage хранится в IndexedDB связанного браузерного runtime.

```python
emb = xlocllm.unit("embedding", "multilingual-e5-small")
store = xlocllm.vectorstorage("support-kb")
rag = xlocllm.rag(emb=emb, store=store, name="support")
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", rag=rag)

with xlocllm.runtime([llm]) as rt:
    rt.run()
    rag.add(["Возврат обрабатывается в течение 5 рабочих дней."], ids=["refunds"])
    print(rag.search("Сколько занимает возврат?", top_k=3))
    print(rt.chat("Сколько занимает возврат?"))
    print(rt.chat("Ответь без локальных документов", use_rag=False))
```

Если LLM создан с `rag=...`, `runtime.chat(...)`,
`/xlocllm/v1/invoke/chat.completions` и OpenAI-compatible
`/v1/chat/completions` автоматически делают retrieval, пока не передан
`use_rag=False`. SDK-ответ содержит `raw["rag"]` и `rag`, если retrieval
использовался. OpenAI-compatible ответ кладет эти данные в extension field
`xlocllm.rag`.

Низкоуровневые endpoints через `runtime.invoke(...)`:

- `vector.add`, `vector.search`, `vector.delete`, `vector.clear`, `vector.stats`
- `rag.add`, `rag.search`, `rag.delete`, `rag.clear`, `rag.reindex`, `rag.stats`

## Chat UI

`runtime.chatui()` запускает runtime при необходимости и открывает отдельное
окно чата, которое ходит в bridge по HTTP. По умолчанию метод блокирует скрипт,
чтобы `with xlocllm.runtime(...)` не закрыл bridge сразу после открытия чата.
Если нужен только `WindowHandle`, передайте `block=False`.

```python
with xlocllm.runtime([llm]) as rt:
    rt.run()
    rt.chatui(session="demo", use_rag=True)
```

## Bridge API

Свойства:

- `bridge.port`
- `bridge.base_url`
- `bridge.url` - OpenAI-compatible `/v1` URL

Методы:

- `bridge.activate(daemon=False)`
- `bridge.close()`
- `bridge.status()`
- `bridge.health()`
- `bridge.models()`
- `bridge.units()`
- `bridge.logs(limit=200)`
- `bridge.wait_ready(timeout=None, require_browser=False)`
- `bridge.reload(units=None)`
- `bridge.set_active(unit, active=True, model=None)`
- `bridge.delete_model(unit_or_model, model=None)`
- `bridge.delete_all_models(confirm=True)`
- `bridge.invoke(endpoint, payload, timeout=None)`
- `bridge.processes()`

## Direct Invoke Endpoints

Используйте `runtime.invoke(endpoint, payload)` или
`bridge.invoke(endpoint, payload)`.

Поддерживаемые endpoints:

| Endpoint | Unit | Обязательный input | Возвращает |
| --- | --- | --- | --- |
| `chat.completions`, `chat` | `LLM` | `messages` или `prompt` | `{content, raw?}` |
| `responses` | `LLM` | `input` | response-like text |
| `embeddings`, `embedding` | `embedding` | `input` строка или список | `{embeddings}` |
| `rerank`, `reranker` | `reranker` | `query`, `documents` | `{results}` по score |
| `translate`, `translator` | `translator` | `text`/`input`, опц. `src_lang`, `tgt_lang` | output backend |
| `tts` | `tts` | `text`/`input` | audio-like result |
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
| `vector.delete`, `vector.clear`, `vector.stats` | `vectorstorage` | `unit` | mutation/stats result |
| `rag.add` | `RAG` | `unit`, `documents` | `{ok, rag, store, ids}` |
| `rag.search` | `RAG` | `unit`, `query` | `{ok, results, context}` |
| `rag.delete`, `rag.clear`, `rag.reindex`, `rag.stats` | `RAG` | `unit` | mutation/stats result |

Примеры:

```python
runtime.invoke("embeddings", {"model": "Xenova/multilingual-e5-small", "input": ["hello"]})
runtime.invoke("translate", {"model": "Xenova/opus-mt-en-ru", "text": "hello"})
runtime.invoke("rerank", {"query": "local llm", "documents": ["browser", "server"]})
runtime.invoke("zero-shot-text", {"text": "local inference", "labels": ["AI", "finance"]})
```

Короткие wrappers:

```python
runtime.chat("hello", temperature=0)
vectors = runtime.embed(["hello", "world"])
client = runtime.client()  # требует optional package openai
```

## Переменные окружения

- `XLOCLLM_HOME` - переопределяет папку состояния.
- `XLOCLLM_WEB_URL` - URL web runtime вместо autodiscovery.
- `XLOCLLM_LOG_LEVEL` - уровень логов uvicorn, по умолчанию `warning`.
- `XLOCLLM_NATIVE_DISABLE_INSTALL=1` - отключает managed установку native
  зависимостей и вместо этого возвращает диагностическую ошибку.

Папки состояния по умолчанию:

- Windows: `%LOCALAPPDATA%\xlocllm`
- Unix-like: `$XDG_STATE_HOME/xlocllm` или `~/.local/state/xlocllm`

Native engines, скачанные model artifacts и native vector storage живут внутри
этой же папки `XLOCLLM_HOME`.

CLI для cache:

```powershell
xlocllm cache delete --mode native --unit LLM --model "Qwen-3.5-0.8b" --yes
xlocllm cache clear --mode native --yes
xlocllm cache clear --mode web --yes
```

`cache delete` удаляет одну модель из cache. `cache clear` удаляет все model
artifacts выбранного backend. Native engine packages при этом сохраняются,
удаляются только модели.

## Особенности native runtime

Native mode - режим по умолчанию. Dashboard window в native режиме только
показывает состояние и дает управление: процессы, downloads, queue, loaded units
и resource metrics. Это небраузерное desktop-окно. Модели не исполняются внутри
dashboard; в web mode сохраняется старое browser mini-window поведение.

LLM в native режиме используют GGUF через llama.cpp-compatible loading. Остальные
task-модели используют ONNX Runtime pipelines там, где это возможно. Перед
запуском install planner проверяет выбранную модель, OS, Python version, hardware
signals, engine cache и model cache. Если engine или artifact не удалось
установить/загрузить, ошибка явно показывает backend, model id, OS, Python
version и cache/diagnostic context. Автоматического fallback в web mode нет.

## Особенности браузерного runtime

Bridge слушает только `127.0.0.1`. В `mode="web"` окно браузера должно
оставаться открытым, пока работают browser-модели. Python bridge - это локальный
слой управления и OpenAI-compatible API; веса моделей, cache и inference
исполняются в браузере.

Если mini browser runtime отключился во время RPC, bridge ждет reconnect до 30
секунд и повторяет RPC. Если mini-окно не возвращается за 30 секунд, bridge сам
закрывается, чтобы не оставлять orphan local processes.

Если WebGPU недоступен, браузерный runtime переключает подходящие
Transformers.js модели на WASM и заранее отклоняет MLC/WebLLM или слишком
тяжелые модели. `runtime.status()["runtime"]["capabilities"]` показывает
`webgpu`, `webnn`, `cpuFallback` и количество видимых моделей.

## Управление reasoning

Reasoning/thinking control доступен для LLM-семейств, которые это явно
поддерживают. Сейчас это определяется для Qwen3/Qwen3.5, DeepSeek-R1, gpt-oss и
QwQ-подобных моделей.

```python
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b-fp32", reasoning=False)
runtime = xlocllm.runtime([llm])
runtime.set_reasoning(llm.id, True)
llm.set_reasoning(False)
```

На уровне запроса значения `reasoning`, `enable_thinking` или
`chat_template_kwargs={"enable_thinking": ...}` переопределяют настройку unit.
Web runtime передает `chat_template_kwargs.enable_thinking` в
Transformers.js и добавляет Qwen-маркер `/think` или `/no_think` для MLC/WebLLM
chat, где это нужно. Native runtime сохраняет тот же SDK-флаг и применяет его в
native chat-template path, если выбранная модель заявляет reasoning support.

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
xlocllm cache delete --mode native --unit LLM --model "Qwen-3.5-0.8b" --yes
xlocllm cache clear --mode native --yes
xlocllm bridge --port 1146
xlocllm bridge --mode web --port 1146
```

## Готовые рецепты

Практические end-to-end скрипты для RAG, фото-перевода, агентных LLM-стеков,
voice assistant, OCR/document intelligence и других частых задач вынесены в
[`recipes_ru.md`](recipes_ru.md).

## Полный API Reference

### Top-Level Exports

Доступно напрямую из `xlocllm`:

- `xlocllm.mode` - глобальный runtime mode, по умолчанию `"native"`
- `xlocllm.unit(type, model, quant=None, reasoning=None, options=None, rag=None, mode=None) -> Unit`
- `xlocllm.vectorstorage(name="default", ..., mode=None) -> Unit`
- `xlocllm.rag(emb, rerank=None, store=None, ..., mode=None) -> Unit`
- `xlocllm.runtime(units, port=1146, bridge=None, runtime_id=None, mode=None) -> Runtime`
- `xlocllm.model(name, unit=None, mode=None, quant=None) -> ModelInfo`
- `xlocllm.models(..., mode=None, installed=None, hardware=None, include_unavailable=False, quant=None) -> list[ModelInfo]`
- `xlocllm.bridges(active_only=True) -> list[Bridge | NativeBridge]`
- `xlocllm.runtimes(active_only=True) -> list[Runtime]`
- `xlocllm.status() -> dict`
- `xlocllm.benchmark(type=None, mode=None, ...) -> dict`
- `xlocllm.cpu_fallback_model_ids() -> set[str]`
- `xlocllm.supports_cpu_fallback(model_dict) -> bool`
- `xlocllm.supports_reasoning(model_dict) -> bool`
- `xlocllm.window(...) -> WindowHandle`
- `xlocllm.GetBridge(port=None) -> Bridge | BridgeGroup`
- классы: `Bridge`, `NativeBridge`, `BridgeGroup`, `ModelInfo`, `Runtime`, `Unit`, `UnitRequest`
- исключения: `XlocLLMError`, `BridgeNotReady`, `BrowserNotConnected`,
  `ModelNotFound`, `RuntimeNotFound`, `UnitNotFound`

### `ModelInfo`

`ModelInfo` - типизированное read-only представление одной записи каталога.

Свойства:

- `data: dict[str, Any]` - исходный объект каталога.
- `unit: str` - тип unit, например `LLM` или `embedding`.
- `runtime: str` - backend family: `native`, `mlc` или `transformers`.
- `mode: str | None` - режим каталога, если поле задано.
- `task: str` - backend task.
- `model_id: str` - точный id модели для `unit()`.
- `label: str` - человекочитаемое имя.
- `aliases: list[str]` - допустимые алиасы для поиска.
- `hardware_tier: str` - `tiny`, `small`, `medium` или `large`.
- `disk_mb: int` - примерный размер cache/disk.
- `vram_mb: int` - примерная потребность в GPU memory.
- `npu_eligible: bool` - предпочтителен ли WebNN/NPU при наличии.
- `cpu_fallback: bool` - может ли модель работать без WebGPU через CPU/WASM.
- `supports_reasoning: bool` - есть ли advertised reasoning-control.

Методы:

- `get(key, default=None) -> Any` - безопасный dictionary-style lookup.
- `__getitem__(key) -> Any` - обязательный dictionary-style lookup.
- `to_dict() -> dict[str, Any]` - копия исходной записи каталога.

### `Unit`

`Unit` описывает model-backed capability, сервисный unit или composite unit.

Обычно создается так:

```python
unit = xlocllm.unit("LLM", "Qwen-3.5-0.8b", quant=None, reasoning=None, options=None, rag=None, mode=None)
```

Свойства:

- `type: str` - нормализованный тип unit.
- `model: str` - точный resolved model id.
- `model_info: ModelInfo | None` - запись каталога.
- `mode: str | None` - выбранный runtime mode.
- `quant: str | None` - выбранное GGUF-квантование для native LLM.
- `reasoning: bool | None` - настройка reasoning для поддерживающих LLM.
- `options: dict[str, Any]` - runtime options для unit.
- `rag: Unit | None` - подключенный RAG service для LLM units.
- `id: str` - локальный стабильный id вида `<type>:<modelId>`.
- `label: str` - label из каталога или model id.
- `supports_reasoning: bool` - capability из каталога.

Методы:

- `to_payload() -> dict[str, Any]`
  Возвращает payload для bridge: `{"type": type, "model": model, ...}`.
- `to_dict() -> dict[str, Any]`
  Возвращает id, type, model, label и metadata модели.
- `status() -> dict[str, Any]`
  Возвращает состояние attached runtime; если unit не attached, возвращает
  offline selected-state.
- `remove() -> dict[str, Any]`
  Убирает unit из attached runtime без удаления model cache.
- `delete(delete_cache=True, bridge=None) -> dict[str, Any]`
  Если unit attached, убирает его из runtime. Если `delete_cache=True`, просит
  выбранный bridge удалить model cache. Для `RAG` и `vectorstorage`
  `delete(ids=None, filter=None)` удаляет документы или vector records.
- `delete_cache(bridge=None) -> dict[str, Any]`
  Удаляет cache модели в выбранном backend через bridge.
- `set_reasoning(enabled) -> dict[str, Any]`
  Меняет local setting и пушит изменение в running runtime, если unit attached.
- `as_runtime(port=1146) -> Runtime`
  Создает или переиспользует single-unit runtime.
- `install(port=1146) -> dict[str, Any]`
  Shortcut для `unit.as_runtime(port).install()`.
- `run(port=1146) -> dict[str, Any]`
  Shortcut для `unit.as_runtime(port).run()`.
- `stop() -> dict[str, Any]`
  Останавливает single-unit runtime.
- `hibernate() -> dict[str, Any]`
  Переводит single-unit runtime в hibernate.
- `heatup() -> dict[str, Any]`
  Запускает и прогревает single-unit runtime.
- `invoke(endpoint, payload, timeout=None) -> dict[str, Any]`
  Вызывает endpoint через single-unit runtime.
- `add(documents, ids=None, metadatas=None, embeddings=None, **params) -> dict[str, Any]`
  Добавляет документы в `RAG` или явные text+embedding records в `vectorstorage`.
- `search(query=None, embedding=None, top_k=None, filter=None, **params) -> dict[str, Any]`
  Ищет в `RAG` по текстовому query или в `vectorstorage` по готовому embedding.
- `clear(**params) -> dict[str, Any]`
  Очищает namespace RAG/vector store.
- `stats() -> dict[str, Any]`
  Возвращает статистику vector/RAG storage из активного runtime.
- `reindex(**params) -> dict[str, Any]`
  Переэмбеддит существующие RAG chunks текущей embedding model.

### `Runtime`

`Runtime` - Python-side описание и контроллер набора units.

Конструктор:

```python
Runtime(units, *, port=1146, bridge=None, runtime_id=None, mode=None)
```

Обычно используйте `xlocllm.runtime(...)`.

Свойства:

- `id: str` - runtime registry id.
- `mode: str` - выбранный runtime mode: `"native"` или `"web"`.
- `port: int` - порт bridge.
- `bridge: Bridge | NativeBridge | None` - связанный bridge.
- `window_handle: WindowHandle | None` - dashboard/browser window, если его открыл SDK.
- `installed: bool` - Python-side флаг установки.
- `running: bool` - Python-side флаг запуска.
- `base_url: str` - base URL bridge, например `http://127.0.0.1:1146`.
- `url: str` - OpenAI-compatible URL, например `http://127.0.0.1:1146/v1`.
- `unit_requests: list[dict[str, Any]]` - payload objects для всех units.

Методы:

- `add_unit(unit, activate=True) -> Unit`
  Добавляет `Unit` или `UnitRequest`. Если runtime уже работает и bridge
  attached, `activate=True` попросит выбранный backend запустить модель.
- `remove_unit(unit_id, delete_cache=False) -> dict[str, Any]`
  Удаляет unit по `unit.id`, model id или типу unit. С `delete_cache=True`
  просит bridge удалить cache модели.
- `configure_unit(unit_id, reasoning=None, options=None) -> dict[str, Any]`
  Меняет options unit. Если runtime запущен, отправляет hot update в активный backend.
- `set_reasoning(unit_id, enabled) -> dict[str, Any]`
  Shortcut для `configure_unit(..., reasoning=enabled)`.
- `unit_status(unit_id) -> dict[str, Any]`
  Возвращает лучшее доступное состояние unit из активного backend.
- `units(as_dict=False, state=False) -> list[Any]`
  Возвращает configured `Unit`, dict-представления или backend-reported states.
- `models() -> list[dict[str, Any]]`
  Возвращает backend model states, если доступны, иначе configured units.
- `install(port=None) -> dict[str, Any]`
  Запускает bridge daemon и просит установить engines/models. В web режиме
  открывает browser window и ждет pairing; в native режиме открывает dashboard.
- `run(port=None) -> dict[str, Any]`
  Гарантирует install и запускает все configured units.
- `stop() -> dict[str, Any]`
  Останавливает модели и закрывает owned dashboard/browser window.
- `hibernate() -> dict[str, Any]`
  Выгружает active models, оставляя их selected.
- `heatup() -> dict[str, Any]`
  Запускает active models и делает warmup для поддерживаемых units.
- `status() -> dict[str, Any]`
  Возвращает runtime id, URL, configured units, bridge process info и backend
  status snapshot, если bridge reachable.
- `health() -> dict[str, Any]`
  Возвращает bridge health.
- `logs(limit=200) -> list[dict[str, Any]]`
  Возвращает логи bridge/backend runtime.
- `invoke(endpoint, payload, timeout=None) -> dict[str, Any]`
  Вызывает `/xlocllm/v1/invoke/{endpoint}`.
- `client(api_key="xlocllm", **kwargs) -> Any`
  Создает `openai.OpenAI` client с `base_url=runtime.url`. Требует optional
  package `openai`.
- `chat(prompt=None, messages=None, model=None, use_rag=None, **params) -> dict[str, Any]`
  Shortcut для `chat.completions`. Если selected LLM имеет `rag`, retrieval
  запускается автоматически, пока не передан `use_rag=False`.
- `embed(input, model=None) -> list[Any]`
  Shortcut для `embeddings`.
- `open() -> WindowHandle`
  Открывает или переоткрывает native dashboard или browser UI для attached bridge.
- `chatui(model=None, session="default", use_rag=True, open_browser=True, width=760, height=860) -> WindowHandle`
  Открывает chat window, привязанный к running runtime.
- `close() -> dict[str, Any]`
  Останавливает bridge и удаляет runtime registry state.
- `wait_ready(timeout=None, require_browser=False) -> Runtime`
  Ждет доступности bridge и опционально browser pairing в web mode.
- `__enter__() -> Runtime`, `__exit__(...) -> False`
  Поддержка `with` для cleanup bridge/window.

### `Bridge` / `NativeBridge`

`Bridge` - локальный HTTP/WebSocket control plane для web mode. `NativeBridge` -
локальный control plane для native mode с тем же основным API.

Конструктор:

```python
Bridge(port=1146, ttl=None, live_time=None)
```

Свойства:

- `port: int`
- `ttl: float | None` - зарезервировано, сейчас не применяется.
- `live_time: float | None` - optional lifetime server process в секундах.
- `token: str` - browser pairing token.
- `base_url: str` - `http://127.0.0.1:<port>`.
- `url: str` - `http://127.0.0.1:<port>/v1`.

Методы:

- `activate(daemon=False) -> Bridge`
  Запускает bridge, если он еще не healthy. С `daemon=True` стартует отдельный
  Python process, иначе daemon thread.
- `close() -> dict[str, Any]`
  Просит bridge shutdown и удаляет запись registry.
- `status() -> dict[str, Any]`
  Вызывает `/xlocllm/v1/status`.
- `health() -> dict[str, Any]`
  Вызывает `/health`.
- `models() -> list[dict[str, Any]]`
  Возвращает видимый backend каталог моделей из bridge или local fallback.
- `units() -> list[dict[str, Any]]`
  Возвращает unit definitions из bridge или local fallback.
- `logs(limit=200) -> list[dict[str, Any]]`
  Возвращает bridge/backend logs.
- `wait_ready(timeout=None, require_browser=False) -> Bridge`
  Ждет health bridge и опционально pairing браузера.
- `reload(units=None) -> dict[str, Any]`
  Останавливает и перезапускает backend runtime с переданными units.
- `set_active(unit, active=True, model=None) -> dict[str, Any]`
  При `active=True` запускает модель; при `active=False` деактивирует модель
  через `runtime/set_active`.
- `delete_model(unit_or_model, model=None) -> dict[str, Any]`
  Запрашивает удаление model cache.
- `delete_all_models(confirm=True) -> dict[str, Any]`
  Удаляет все известные model cache entries. При `confirm=False` кидает
  исключение.
- `invoke(endpoint, payload, timeout=None) -> dict[str, Any]`
  Вызывает `/xlocllm/v1/invoke/{endpoint}`.
- `processes() -> dict[str, Any]`
  Возвращает PID bridge и window/dashboard, а также alive flags.

### `BridgeGroup`

`BridgeGroup` возвращается из `GetBridge()`, когда порт не передан.

Свойства:

- `bridges: list[Bridge]`

Методы:

- `__iter__()`
- `__len__()`
- `activate(daemon=False) -> list[Bridge]`
- `close() -> list[dict[str, Any]]`
- `status() -> list[dict[str, Any]]`
- `health() -> list[dict[str, Any]]`

### `WindowHandle`

Возвращается из `xlocllm.window(...)` и `Runtime.open()`.

Свойства:

- `port: int`
- `url: str`
- `pid: int | None`
- `owned: bool`

Методы:

- `close() -> None`
  Закрывает owned browser process tree, если это возможно.

### `UnitRequest`

Низкоуровневая dataclass для bridge payload.

Свойства:

- `type: str`
- `model: str`
- `reasoning: bool | None`
- `options: dict[str, Any] | None`

Методы:

- `to_payload() -> dict[str, Any]`

### Исключения

- `XlocLLMError` - базовое исключение SDK.
- `BridgeNotReady` - bridge недоступен.
- `BrowserNotConnected` - bridge запущен, но browser runtime не paired.
- `ModelNotFound` - модель или alias не найден.
- `UnitNotFound` - unit type не найден.
- `RuntimeNotFound` - runtime id неизвестен.
