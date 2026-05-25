# xlocllm Python SDK

`xlocllm` is a local browser-backed inference SDK. Python code talks to a
loopback FastAPI bridge, while the actual model runtime lives in a paired
browser window using WebGPU/WebNN through MLC WebLLM or Transformers.js.

## Install

```powershell
python -m pip install -e .\python\xlocllm
```

Package metadata:

- Python: `>=3.10`
- Runtime dependencies: `fastapi`, `uvicorn[standard]`, `pydantic`
- CLI entry point: `xlocllm-bridge`

## Core Objects

The v1-style SDK schema has four main concepts:

- `ModelInfo` - immutable model catalog entry with hardware and runtime metadata.
- `Unit` - one capability/model pair, for example `LLM + Qwen`.
- `Runtime` - a group of units that should run together.
- `Bridge` - local HTTP/WebSocket process used by Python and the browser runtime.

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

## OpenAI-Compatible Usage

```python
import xlocllm
from openai import OpenAI

runtime = xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b")])
runtime.run()

client = OpenAI(base_url=runtime.url, api_key="xlocllm")
response = client.chat.completions.create(
    model="Qwen3.5-0.8B-q4f16_1-MLC",
    messages=[{"role": "user", "content": "Say hello"}],
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

### `xlocllm.unit(type, model)`

Creates a `Unit` by resolving the requested unit type and model name against the
catalog.

```python
unit = xlocllm.unit("chat", "qwen-0.8b")
print(unit.type)   # LLM
print(unit.model)  # Qwen3.5-0.8B-q4f16_1-MLC
```

Accepted model names include exact `modelId`, `label`, and catalog aliases.

### `xlocllm.runtime(units, port=1146, bridge=None, runtime_id=None)`

Creates a `Runtime` from `Unit` or `UnitRequest` objects.

```python
runtime = xlocllm.runtime([xlocllm.unit("LLM", "Qwen-3.5-0.8b")], port=12000)
```

### `xlocllm.models(...)`

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
- `search`
- `max_vram_mb`
- `max_disk_mb`
- `max_size_gb`
- `max_parameters_b`

Example:

```python
small_llms = xlocllm.models(unit="LLM", max_vram_mb=1500, search="qwen")
```

### `xlocllm.model(name, unit=None)`

Returns one `ModelInfo`.

```python
info = xlocllm.model("Qwen-3.5-0.8b", unit="LLM")
print(info.model_id)
print(info.to_dict())
```

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

## Unit API

Properties:

- `unit.id` - stable local id in the form `<type>:<modelId>`
- `unit.type`
- `unit.model`
- `unit.label`
- `unit.model_info`

Methods:

- `unit.to_payload()` - `{"type": ..., "model": ...}`
- `unit.to_dict()` - payload plus label and model metadata
- `unit.status()` - attached runtime state if available
- `unit.remove()` - remove from attached runtime without deleting cache
- `unit.delete(delete_cache=True, bridge=None)` - remove from runtime and optionally delete browser cache
- `unit.as_runtime(port=1146)` - create or reuse a single-unit runtime
- `unit.install(port=1146)`
- `unit.run(port=1146)`
- `unit.stop()`
- `unit.hibernate()`
- `unit.heatup()`
- `unit.invoke(endpoint, payload, timeout=None)`

## Runtime API

Properties:

- `runtime.id`
- `runtime.port`
- `runtime.base_url` - `http://127.0.0.1:<port>`
- `runtime.url` - `http://127.0.0.1:<port>/v1`
- `runtime.bridge`
- `runtime.installed`
- `runtime.running`
- `runtime.unit_requests`

Methods:

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

`runtime.remove_unit()` accepts the unit id, model id, or unit type. If the
runtime is running and `delete_cache=False`, the SDK asks the browser runtime to
deactivate that specific model. If `delete_cache=True`, it requests model cache
cleanup through the bridge.

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
- `bridge.models()` - full catalog as dictionaries
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

Examples:

```python
runtime.invoke("embeddings", {"model": "Xenova/multilingual-e5-small", "input": ["hello"]})
runtime.invoke("translate", {"model": "Xenova/opus-mt-en-ru", "text": "hello"})
runtime.invoke("rerank", {"query": "local llm", "documents": ["browser", "server"]})
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

Default state locations:

- Windows: `%LOCALAPPDATA%\xlocllm`
- Unix-like: `$XDG_STATE_HOME/xlocllm` or `~/.local/state/xlocllm`

## Browser Runtime Notes

The bridge binds to `127.0.0.1`. The browser window must stay open while browser
models are running. The Python bridge is only a local control and API layer; the
model weights and inference execution live in browser storage and browser GPU
runtime.

Some catalog units already exist for future use, but direct invoke routing is
currently implemented only for the endpoints listed above.

## Complete API Reference

### Top-Level Exports

Imported directly from `xlocllm`:

- `xlocllm.unit(type, model) -> Unit`
- `xlocllm.runtime(units, port=1146, bridge=None, runtime_id=None) -> Runtime`
- `xlocllm.model(name, unit=None) -> ModelInfo`
- `xlocllm.models(...) -> list[ModelInfo]`
- `xlocllm.bridges(active_only=True) -> list[Bridge]`
- `xlocllm.runtimes(active_only=True) -> list[Runtime]`
- `xlocllm.status() -> dict`
- `xlocllm.window(...) -> WindowHandle`
- `xlocllm.GetBridge(port=None) -> Bridge | BridgeGroup`
- classes: `Bridge`, `BridgeGroup`, `ModelInfo`, `Runtime`, `Unit`
- exceptions: `XlocLLMError`, `BridgeNotReady`, `BrowserNotConnected`,
  `ModelNotFound`, `RuntimeNotFound`, `UnitNotFound`

### `ModelInfo`

`ModelInfo` wraps one catalog record. It behaves like a typed read-only view over
the underlying model dictionary.

Properties:

- `data: dict[str, Any]` - raw catalog object.
- `unit: str` - unit type, for example `LLM` or `embedding`.
- `runtime: str` - backend family, currently `mlc` or `transformers`.
- `task: str` - backend task string.
- `model_id: str` - exact model id to pass to `unit()`.
- `label: str` - human-readable model name.
- `aliases: list[str]` - accepted lookup aliases.
- `hardware_tier: str` - `tiny`, `small`, `medium`, or `large`.
- `disk_mb: int` - approximate disk/cache size.
- `vram_mb: int` - approximate GPU memory requirement.
- `npu_eligible: bool` - whether WebNN/NPU is preferred when available.

Methods:

- `get(key, default=None) -> Any` - dictionary-style optional lookup.
- `__getitem__(key) -> Any` - dictionary-style required lookup.
- `to_dict() -> dict[str, Any]` - copy of the raw catalog object.

### `Unit`

`Unit` represents one capability/model pair.

Constructor is normally not called directly. Prefer:

```python
unit = xlocllm.unit("LLM", "Qwen-3.5-0.8b")
```

Properties:

- `type: str` - normalized unit type.
- `model: str` - resolved exact model id.
- `model_info: ModelInfo | None` - catalog entry.
- `id: str` - local stable id in the form `<type>:<modelId>`.
- `label: str` - catalog label, or model id if metadata is absent.

Methods:

- `to_payload() -> dict[str, str]`
  Returns the bridge payload: `{"type": type, "model": model}`.
- `to_dict() -> dict[str, Any]`
  Returns id, type, model, label, and model metadata.
- `status() -> dict[str, Any]`
  Returns attached runtime status when the unit belongs to a runtime; otherwise
  returns an offline selected-state dictionary.
- `remove() -> dict[str, Any]`
  Removes the unit from its attached runtime without deleting browser cache.
- `delete(delete_cache=True, bridge=None) -> dict[str, Any]`
  If attached to a runtime, removes it from that runtime. If `delete_cache=True`,
  asks the bridge to delete the browser cache for this model.
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

### `Runtime`

`Runtime` is a Python-side runtime definition and controller. It owns a set of
units and communicates through one bridge.

Constructor:

```python
Runtime(units, *, port=1146, bridge=None, runtime_id=None)
```

Use `xlocllm.runtime(...)` unless you need direct class construction.

Properties:

- `id: str` - runtime registry id.
- `port: int` - bridge port.
- `bridge: Bridge | None` - attached bridge object.
- `window_handle: WindowHandle | None` - browser window handle if opened by SDK.
- `installed: bool` - Python-side install state flag.
- `running: bool` - Python-side run state flag.
- `base_url: str` - bridge base URL, for example `http://127.0.0.1:1146`.
- `url: str` - OpenAI-compatible URL, for example `http://127.0.0.1:1146/v1`.
- `unit_requests: list[UnitRequest]` - bridge payload objects for all units.

Methods:

- `add_unit(unit, activate=True) -> Unit`
  Adds a `Unit` or `UnitRequest`. If runtime is already running and a bridge is
  attached, `activate=True` asks the browser runtime to start that model.
- `remove_unit(unit_id, delete_cache=False) -> dict[str, Any]`
  Removes a unit by `unit.id`, model id, or unit type. With `delete_cache=True`,
  asks the bridge to delete model cache.
- `unit_status(unit_id) -> dict[str, Any]`
  Returns the best available browser state for a unit.
- `units(as_dict=False, state=False) -> list[Any]`
  Returns configured `Unit` objects, dictionaries, or browser-reported unit
  states when `state=True`.
- `models() -> list[dict[str, Any]]`
  Returns browser runtime model states if available; otherwise returns configured
  unit dictionaries.
- `install(port=None) -> dict[str, Any]`
  Starts bridge daemon, opens browser window, waits for pairing, and requests
  model installation.
- `run(port=None) -> dict[str, Any]`
  Ensures install has happened and starts all configured units.
- `stop() -> dict[str, Any]`
  Stops running browser models and closes the owned browser window.
- `hibernate() -> dict[str, Any]`
  Unloads active models but keeps them selected.
- `heatup() -> dict[str, Any]`
  Starts active models and performs a small warmup for supported units.
- `status() -> dict[str, Any]`
  Returns runtime id, URL, configured units, bridge process info, and browser
  status snapshot when reachable.
- `health() -> dict[str, Any]`
  Returns bridge health.
- `logs(limit=200) -> list[dict[str, Any]]`
  Returns bridge/browser runtime logs.
- `invoke(endpoint, payload, timeout=None) -> dict[str, Any]`
  Calls `/xlocllm/v1/invoke/{endpoint}`.
- `client(api_key="xlocllm", **kwargs) -> Any`
  Creates an `openai.OpenAI` client bound to `runtime.url`. Requires optional
  `openai` package.
- `chat(prompt=None, messages=None, model=None, **params) -> dict[str, Any]`
  Convenience wrapper for `chat.completions`.
- `embed(input, model=None) -> list[Any]`
  Convenience wrapper for `embeddings`.
- `open() -> WindowHandle`
  Opens or reopens the browser UI for the attached bridge.
- `close() -> dict[str, Any]`
  Shuts down the bridge and removes runtime registry state.
- `wait_ready(timeout=None, require_browser=False) -> Runtime`
  Waits until the bridge is reachable, and optionally until the browser is paired.

### `Bridge`

`Bridge` is the local HTTP/WebSocket control plane.

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
  Returns bridge/browser logs.
- `wait_ready(timeout=None, require_browser=False) -> Bridge`
  Waits for bridge health and optionally browser pairing.
- `reload(units=None) -> dict[str, Any]`
  Stops and reruns the browser runtime with supplied units.
- `set_active(unit, active=True, model=None) -> dict[str, Any]`
  Starts a model for `active=True`; deactivates a model through `runtime/set_active`
  for `active=False`.
- `delete_model(unit_or_model, model=None) -> dict[str, Any]`
  Requests browser-side model cache deletion.
- `delete_all_models(confirm=True) -> dict[str, Any]`
  Deletes all known browser-side model cache entries. Raises if `confirm=False`.
- `invoke(endpoint, payload, timeout=None) -> dict[str, Any]`
  Calls `/xlocllm/v1/invoke/{endpoint}`.
- `processes() -> dict[str, Any]`
  Returns bridge and browser window PIDs with alive flags.

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

Methods:

- `to_payload() -> dict[str, str]`

### Exceptions

- `XlocLLMError` - base SDK exception.
- `BridgeNotReady` - bridge cannot be reached.
- `BrowserNotConnected` - bridge is up but browser runtime is not paired.
- `ModelNotFound` - model name/alias does not resolve.
- `UnitNotFound` - unit type does not resolve.
- `RuntimeNotFound` - runtime id is unknown.
