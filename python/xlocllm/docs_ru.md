# xlocllm Python SDK

`xlocllm` - локальный Python SDK для запуска моделей в браузере. Python-код
общается с локальным FastAPI bridge на `127.0.0.1`, а сами модели загружаются и
исполняются в связанном окне браузера через WebGPU/WebNN, MLC WebLLM или
Transformers.js.

## Установка

```powershell
python -m pip install -e .\python\xlocllm
```

Метаданные пакета:

- Python: `>=3.10`
- runtime-зависимости: `fastapi`, `uvicorn[standard]`, `pydantic`
- CLI entry point: `xlocllm-bridge`

## Основные сущности

В новой схеме SDK есть четыре основные сущности:

- `ModelInfo` - запись каталога модели с runtime и hardware-характеристиками.
- `Unit` - пара capability/model, например `LLM + Qwen`.
- `Runtime` - набор units, которые надо держать вместе в браузерном runtime.
- `Bridge` - локальный HTTP/WebSocket процесс между Python и браузером.

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

## OpenAI-compatible API

```python
import xlocllm
from openai import OpenAI

runtime = xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b")])
runtime.run()

client = OpenAI(base_url=runtime.url, api_key="xlocllm")
response = client.chat.completions.create(
    model="Qwen3.5-0.8B-q4f16_1-MLC",
    messages=[{"role": "user", "content": "Привет"}],
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

### `xlocllm.unit(type, model)`

Создает `Unit`, нормализуя тип и имя модели через каталог.

```python
unit = xlocllm.unit("chat", "qwen-0.8b")
print(unit.type)   # LLM
print(unit.model)  # Qwen3.5-0.8B-q4f16_1-MLC
```

Модель можно указывать через точный `modelId`, `label` или любой alias из
каталога.

### `xlocllm.runtime(units, port=1146, bridge=None, runtime_id=None)`

Создает `Runtime` из объектов `Unit` или `UnitRequest`.

```python
runtime = xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b")], port=12000)
```

### `xlocllm.models(...)`

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
- `search`
- `max_vram_mb`
- `max_disk_mb`
- `max_size_gb`
- `max_parameters_b`

Пример:

```python
small_llms = xlocllm.models(unit="LLM", max_vram_mb=1500, search="qwen")
```

### `xlocllm.model(name, unit=None)`

Возвращает одну модель как `ModelInfo`.

```python
info = xlocllm.model("Qwen-3.5-0.8b", unit="LLM")
print(info.model_id)
print(info.to_dict())
```

### `xlocllm.bridges(active_only=True)`

Возвращает известные `Bridge` из локального registry.

### `xlocllm.runtimes(active_only=True)`

Возвращает известные `Runtime` из локального registry.

### `xlocllm.status()`

Возвращает словарь, где собраны:

- известные bridges;
- известные runtimes;
- установленные и запущенные модели, если browser runtime доступен;
- resource metrics, которые отдает браузер;
- количество моделей в каталоге.

## Unit API

Свойства:

- `unit.id` - локальный id вида `<type>:<modelId>`
- `unit.type`
- `unit.model`
- `unit.label`
- `unit.model_info`

Методы:

- `unit.to_payload()` - `{"type": ..., "model": ...}`
- `unit.to_dict()` - payload, label и metadata модели
- `unit.status()` - состояние unit в attached runtime
- `unit.remove()` - убрать из attached runtime без удаления cache
- `unit.delete(delete_cache=True, bridge=None)` - убрать из runtime и при необходимости удалить browser cache
- `unit.as_runtime(port=1146)` - создать или переиспользовать runtime для одного unit
- `unit.install(port=1146)`
- `unit.run(port=1146)`
- `unit.stop()`
- `unit.hibernate()`
- `unit.heatup()`
- `unit.invoke(endpoint, payload, timeout=None)`

## Runtime API

Свойства:

- `runtime.id`
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
- `runtime.chat(prompt=None, messages=None, model=None, **params)`
- `runtime.embed(input, model=None)`
- `runtime.open()`
- `runtime.close()`
- `runtime.wait_ready(timeout=None, require_browser=False)`

`runtime.remove_unit()` принимает `unit.id`, `modelId` или тип unit. Если runtime
запущен и `delete_cache=False`, SDK попросит браузер деактивировать модель. Если
`delete_cache=True`, SDK дополнительно запросит очистку cache модели.

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

- `chat.completions`
- `responses`
- `embeddings`
- `rerank`
- `translate`
- `tts`
- `image.classify`
- `image.detect`
- `image.segment`
- `depth`
- `image-to-text`
- `asr`
- `zero-shot-image`

Примеры:

```python
runtime.invoke("embeddings", {"model": "Xenova/multilingual-e5-small", "input": ["hello"]})
runtime.invoke("translate", {"model": "Xenova/opus-mt-en-ru", "text": "hello"})
runtime.invoke("rerank", {"query": "local llm", "documents": ["browser", "server"]})
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

Папки состояния по умолчанию:

- Windows: `%LOCALAPPDATA%\xlocllm`
- Unix-like: `$XDG_STATE_HOME/xlocllm` или `~/.local/state/xlocllm`

## Особенности браузерного runtime

Bridge слушает только `127.0.0.1`. Окно браузера должно оставаться открытым,
пока работают browser-модели. Python bridge - это локальный слой управления и
OpenAI-compatible API; веса моделей, cache и inference исполняются в браузере.

Часть unit-типов уже есть в каталоге как основа для расширения, но прямой
`invoke` routing сейчас реализован только для endpoints, перечисленных выше.

## Полный API Reference

### Top-Level Exports

Доступно напрямую из `xlocllm`:

- `xlocllm.unit(type, model) -> Unit`
- `xlocllm.runtime(units, port=1146, bridge=None, runtime_id=None) -> Runtime`
- `xlocllm.model(name, unit=None) -> ModelInfo`
- `xlocllm.models(...) -> list[ModelInfo]`
- `xlocllm.bridges(active_only=True) -> list[Bridge]`
- `xlocllm.runtimes(active_only=True) -> list[Runtime]`
- `xlocllm.status() -> dict`
- `xlocllm.window(...) -> WindowHandle`
- `xlocllm.GetBridge(port=None) -> Bridge | BridgeGroup`
- классы: `Bridge`, `BridgeGroup`, `ModelInfo`, `Runtime`, `Unit`
- исключения: `XlocLLMError`, `BridgeNotReady`, `BrowserNotConnected`,
  `ModelNotFound`, `RuntimeNotFound`, `UnitNotFound`

### `ModelInfo`

`ModelInfo` - типизированное read-only представление одной записи каталога.

Свойства:

- `data: dict[str, Any]` - исходный объект каталога.
- `unit: str` - тип unit, например `LLM` или `embedding`.
- `runtime: str` - backend family: `mlc` или `transformers`.
- `task: str` - backend task.
- `model_id: str` - точный id модели для `unit()`.
- `label: str` - человекочитаемое имя.
- `aliases: list[str]` - допустимые алиасы для поиска.
- `hardware_tier: str` - `tiny`, `small`, `medium` или `large`.
- `disk_mb: int` - примерный размер cache/disk.
- `vram_mb: int` - примерная потребность в GPU memory.
- `npu_eligible: bool` - предпочтителен ли WebNN/NPU при наличии.

Методы:

- `get(key, default=None) -> Any` - безопасный dictionary-style lookup.
- `__getitem__(key) -> Any` - обязательный dictionary-style lookup.
- `to_dict() -> dict[str, Any]` - копия исходной записи каталога.

### `Unit`

`Unit` описывает одну пару capability/model.

Обычно создается так:

```python
unit = xlocllm.unit("LLM", "Qwen-3.5-0.8b")
```

Свойства:

- `type: str` - нормализованный тип unit.
- `model: str` - точный resolved model id.
- `model_info: ModelInfo | None` - запись каталога.
- `id: str` - локальный стабильный id вида `<type>:<modelId>`.
- `label: str` - label из каталога или model id.

Методы:

- `to_payload() -> dict[str, str]`
  Возвращает payload для bridge: `{"type": type, "model": model}`.
- `to_dict() -> dict[str, Any]`
  Возвращает id, type, model, label и metadata модели.
- `status() -> dict[str, Any]`
  Возвращает состояние attached runtime; если unit не attached, возвращает
  offline selected-state.
- `remove() -> dict[str, Any]`
  Убирает unit из attached runtime без удаления browser cache.
- `delete(delete_cache=True, bridge=None) -> dict[str, Any]`
  Если unit attached, убирает его из runtime. Если `delete_cache=True`, просит
  bridge удалить browser cache модели.
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

### `Runtime`

`Runtime` - Python-side описание и контроллер набора units.

Конструктор:

```python
Runtime(units, *, port=1146, bridge=None, runtime_id=None)
```

Обычно используйте `xlocllm.runtime(...)`.

Свойства:

- `id: str` - runtime registry id.
- `port: int` - порт bridge.
- `bridge: Bridge | None` - связанный bridge.
- `window_handle: WindowHandle | None` - окно браузера, если его открыл SDK.
- `installed: bool` - Python-side флаг установки.
- `running: bool` - Python-side флаг запуска.
- `base_url: str` - base URL bridge, например `http://127.0.0.1:1146`.
- `url: str` - OpenAI-compatible URL, например `http://127.0.0.1:1146/v1`.
- `unit_requests: list[UnitRequest]` - payload objects для всех units.

Методы:

- `add_unit(unit, activate=True) -> Unit`
  Добавляет `Unit` или `UnitRequest`. Если runtime уже работает и bridge
  attached, `activate=True` попросит браузер запустить модель.
- `remove_unit(unit_id, delete_cache=False) -> dict[str, Any]`
  Удаляет unit по `unit.id`, model id или типу unit. С `delete_cache=True`
  просит bridge удалить cache модели.
- `unit_status(unit_id) -> dict[str, Any]`
  Возвращает лучшее доступное состояние unit из browser runtime.
- `units(as_dict=False, state=False) -> list[Any]`
  Возвращает configured `Unit`, dict-представления или browser-reported states.
- `models() -> list[dict[str, Any]]`
  Возвращает browser runtime model states, если доступны, иначе configured units.
- `install(port=None) -> dict[str, Any]`
  Запускает bridge daemon, открывает browser window, ждет pairing и просит
  установить модели.
- `run(port=None) -> dict[str, Any]`
  Гарантирует install и запускает все configured units.
- `stop() -> dict[str, Any]`
  Останавливает browser models и закрывает owned browser window.
- `hibernate() -> dict[str, Any]`
  Выгружает active models, оставляя их selected.
- `heatup() -> dict[str, Any]`
  Запускает active models и делает warmup для поддерживаемых units.
- `status() -> dict[str, Any]`
  Возвращает runtime id, URL, configured units, bridge process info и browser
  status snapshot, если bridge reachable.
- `health() -> dict[str, Any]`
  Возвращает bridge health.
- `logs(limit=200) -> list[dict[str, Any]]`
  Возвращает логи bridge/browser runtime.
- `invoke(endpoint, payload, timeout=None) -> dict[str, Any]`
  Вызывает `/xlocllm/v1/invoke/{endpoint}`.
- `client(api_key="xlocllm", **kwargs) -> Any`
  Создает `openai.OpenAI` client с `base_url=runtime.url`. Требует optional
  package `openai`.
- `chat(prompt=None, messages=None, model=None, **params) -> dict[str, Any]`
  Shortcut для `chat.completions`.
- `embed(input, model=None) -> list[Any]`
  Shortcut для `embeddings`.
- `open() -> WindowHandle`
  Открывает или переоткрывает browser UI для attached bridge.
- `close() -> dict[str, Any]`
  Останавливает bridge и удаляет runtime registry state.
- `wait_ready(timeout=None, require_browser=False) -> Runtime`
  Ждет доступности bridge и опционально browser pairing.

### `Bridge`

`Bridge` - локальный HTTP/WebSocket control plane.

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
  Возвращает каталог моделей из bridge или local fallback.
- `units() -> list[dict[str, Any]]`
  Возвращает unit definitions из bridge или local fallback.
- `logs(limit=200) -> list[dict[str, Any]]`
  Возвращает bridge/browser logs.
- `wait_ready(timeout=None, require_browser=False) -> Bridge`
  Ждет health bridge и опционально pairing браузера.
- `reload(units=None) -> dict[str, Any]`
  Останавливает и перезапускает browser runtime с переданными units.
- `set_active(unit, active=True, model=None) -> dict[str, Any]`
  При `active=True` запускает модель; при `active=False` деактивирует модель
  через `runtime/set_active`.
- `delete_model(unit_or_model, model=None) -> dict[str, Any]`
  Запрашивает удаление browser-side cache модели.
- `delete_all_models(confirm=True) -> dict[str, Any]`
  Удаляет все известные browser-side cache entries. При `confirm=False` кидает
  исключение.
- `invoke(endpoint, payload, timeout=None) -> dict[str, Any]`
  Вызывает `/xlocllm/v1/invoke/{endpoint}`.
- `processes() -> dict[str, Any]`
  Возвращает PID bridge и browser window, а также alive flags.

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

Методы:

- `to_payload() -> dict[str, str]`

### Исключения

- `XlocLLMError` - базовое исключение SDK.
- `BridgeNotReady` - bridge недоступен.
- `BrowserNotConnected` - bridge запущен, но browser runtime не paired.
- `ModelNotFound` - модель или alias не найден.
- `UnitNotFound` - unit type не найден.
- `RuntimeNotFound` - runtime id неизвестен.
