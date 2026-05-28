# xlocllm Models Catalog

> Native-каталог v1.1: `packages/catalog/native-models.json` и packaged copy
> `xlocllm/data/native_models.json` содержат 300 native-записей. Активный каталог
> по умолчанию смотрите через `xlocllm.models(mode="native", ...)`; доступны
> фильтры `subtype=`, `modality=`, `use_case=`, `license=` и `min_context=`.
> Browser/WebGPU каталог по-прежнему описан ниже.

Источник: `packages/catalog/models.json`, schemaVersion `2`.
Всего unit-групп: `24`. Всего моделей: `217`.

Этот файл описывает browser/WebGPU каталог. В xlocllm v1.1 режим Python по
умолчанию - `native`; он использует отдельный генерируемый native registry с
GGUF LLM и ONNX Runtime task-моделями. Активный каталог лучше смотреть из Python:

```python
import xlocllm

xlocllm.models(mode="native")  # каталог runtime по умолчанию в v1.1
xlocllm.models(mode="web")     # browser/WebGPU каталог, описанный ниже
xlocllm.model("Qwen-3.5-0.8b", unit="LLM", mode="native").to_dict()
```

Каждая запись содержит точный индекс обращения: используйте строку `xlocllm.unit("<unit>", "<modelId>")`.
Внутри каждой группы модели отсортированы от более легких к более мощным по `hardwareTier`, числу параметров, VRAM и disk size.

## Группы

## LLM - LLM

Назначение: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
Catalog task: `text-generation`.
Invoke endpoint: `chat.completions`.

### 1. gemma 4 E2B it

- Индекс: `xlocllm.unit("LLM", "onnx-community/gemma-4-E2B-it-ONNX")`
- Model ID: `onnx-community/gemma-4-E2B-it-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `540 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `gemma 4 E2B it`, `gemma-4-E2B-it`, `gemma-4-E2B-it-ONNX`, `onnx-community/gemma-4-E2B-it-ONNX`
- Теги: `LLM`, `any-to-any`, `base_model:google/gemma-4-E2B-it`, `base_model:quantized:google/gemma-4-E2B-it`, `conversational`, `gemma4`, `image-text-to-text`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`

### 2. gemma 4 E4B it

- Индекс: `xlocllm.unit("LLM", "onnx-community/gemma-4-E4B-it-ONNX")`
- Model ID: `onnx-community/gemma-4-E4B-it-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `540 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `gemma 4 E4B it`, `gemma-4-E4B-it`, `gemma-4-E4B-it-ONNX`, `onnx-community/gemma-4-E4B-it-ONNX`
- Теги: `LLM`, `any-to-any`, `base_model:google/gemma-4-E2B-it`, `base_model:quantized:google/gemma-4-E2B-it`, `conversational`, `gemma4`, `image-text-to-text`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`

### 3. SmolLM 135M

- Индекс: `xlocllm.unit("LLM", "onnx-community/SmolLM-135M-ONNX")`
- Model ID: `onnx-community/SmolLM-135M-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.135B`
- Model size: `0.12 GB`
- Disk: `128 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `SmolLM 135M`, `SmolLM-135M`, `SmolLM-135M-ONNX`, `onnx-community/SmolLM-135M-ONNX`
- Теги: `LLM`, `base_model:HuggingFaceTB/SmolLM-135M`, `base_model:quantized:HuggingFaceTB/SmolLM-135M`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 4. SmolLM 135M Instruct

- Индекс: `xlocllm.unit("LLM", "onnx-community/SmolLM-135M-Instruct-ONNX")`
- Model ID: `onnx-community/SmolLM-135M-Instruct-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.135B`
- Model size: `0.12 GB`
- Disk: `128 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `SmolLM 135M Instruct`, `SmolLM-135M-Instruct`, `SmolLM-135M-Instruct-ONNX`, `onnx-community/SmolLM-135M-Instruct-ONNX`
- Теги: `LLM`, `base_model:HuggingFaceTB/SmolLM-135M-Instruct`, `base_model:quantized:HuggingFaceTB/SmolLM-135M-Instruct`, `conversational`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 5. SmolLM2 135M

- Индекс: `xlocllm.unit("LLM", "onnx-community/SmolLM2-135M-ONNX")`
- Model ID: `onnx-community/SmolLM2-135M-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.135B`
- Model size: `0.12 GB`
- Disk: `128 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `SmolLM2 135M`, `SmolLM2-135M`, `SmolLM2-135M-ONNX`, `onnx-community/SmolLM2-135M-ONNX`
- Теги: `LLM`, `base_model:HuggingFaceTB/SmolLM2-135M`, `base_model:quantized:HuggingFaceTB/SmolLM2-135M`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 6. functiongemma 270m it

- Индекс: `xlocllm.unit("LLM", "onnx-community/functiongemma-270m-it-ONNX")`
- Model ID: `onnx-community/functiongemma-270m-it-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.27B`
- Model size: `0.25 GB`
- Disk: `256 MB`
- VRAM: `460 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `gemma`
- Languages: `en`
- Алиасы: `functiongemma 270m it`, `functiongemma-270m-it`, `functiongemma-270m-it-ONNX`, `onnx-community/functiongemma-270m-it-ONNX`
- Теги: `LLM`, `base_model:google/functiongemma-270m-it`, `base_model:quantized:google/functiongemma-270m-it`, `conversational`, `gemma3_text`, `license:gemma`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 7. gemma 3 270m it

- Индекс: `xlocllm.unit("LLM", "onnx-community/gemma-3-270m-it-ONNX")`
- Model ID: `onnx-community/gemma-3-270m-it-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.27B`
- Model size: `0.25 GB`
- Disk: `256 MB`
- VRAM: `460 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `gemma`
- Languages: `en`
- Алиасы: `gemma 3 270m it`, `gemma-3-270m-it`, `gemma-3-270m-it-ONNX`, `onnx-community/gemma-3-270m-it-ONNX`
- Теги: `LLM`, `arxiv:1905.07830`, `arxiv:1905.10044`, `arxiv:1911.11641`, `arxiv:2503.19786`, `conversational`, `gemma`, `gemma3`, `gemma3_text`, `google`, `onnx`, `text-generation`, `transformers.js`

### 8. SmolLM2 360M Instruct

- Индекс: `xlocllm.unit("LLM", "SmolLM2-360M-Instruct-q4f16_1-MLC")`
- Model ID: `SmolLM2-360M-Instruct-q4f16_1-MLC`
- Для чего подходит: tiny mlc модель для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions; языки: en.
- Runtime: `mlc`
- Task: `text-generation`
- Provider: `MLC`
- Hardware tier: `tiny`
- Parameters: `0.36B`
- Model size: `0.27 GB`
- Disk: `280 MB`
- VRAM: `700 MB`
- DType: `q4f16_1`
- NPU/WebNN: `нет`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `SmolLM2-360M`, `smollm2`

### 9. SmolLM2 360M

- Индекс: `xlocllm.unit("LLM", "onnx-community/SmolLM2-360M-ONNX")`
- Model ID: `onnx-community/SmolLM2-360M-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.36B`
- Model size: `0.33 GB`
- Disk: `342 MB`
- VRAM: `615 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `SmolLM2 360M`, `SmolLM2-360M`, `SmolLM2-360M-ONNX`, `onnx-community/SmolLM2-360M-ONNX`
- Теги: `LLM`, `arxiv:2502.02737`, `base_model:HuggingFaceTB/SmolLM2-360M`, `base_model:quantized:HuggingFaceTB/SmolLM2-360M`, `en`, `license:apache-2.0`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 10. SmolLM2 360M Instruct

- Индекс: `xlocllm.unit("LLM", "HuggingFaceTB/SmolLM2-360M-Instruct")`
- Model ID: `HuggingFaceTB/SmolLM2-360M-Instruct`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `HuggingFaceTB`
- Hardware tier: `small`
- Parameters: `0.36B`
- Model size: `0.33 GB`
- Disk: `342 MB`
- VRAM: `615 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `HuggingFaceTB/SmolLM2-360M-Instruct`, `SmolLM2 360M Instruct`, `SmolLM2-360M`, `SmolLM2-360M-Instruct`
- Теги: `LLM`, `arxiv:2502.02737`, `base_model:HuggingFaceTB/SmolLM2-360M`, `base_model:quantized:HuggingFaceTB/SmolLM2-360M`, `conversational`, `en`, `llama`, `onnx`, `safetensors`, `tensorboard`, `text-generation`, `transformers`, `transformers.js`

### 11. Qwen2.5 0.5B Instruct

- Индекс: `xlocllm.unit("LLM", "asdgad/Qwen2.5-0.5B-Instruct-ONNX")`
- Model ID: `asdgad/Qwen2.5-0.5B-Instruct-ONNX`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `asdgad`
- Hardware tier: `small`
- Parameters: `0.5B`
- Model size: `0.46 GB`
- Disk: `475 MB`
- VRAM: `855 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen2.5 0.5B Instruct`, `Qwen2.5-0.5B-Instruct`, `Qwen2.5-0.5B-Instruct-ONNX`, `asdgad/Qwen2.5-0.5B-Instruct-ONNX`
- Теги: `LLM`, `arxiv:2407.10671`, `base_model:Qwen/Qwen2.5-0.5B-Instruct`, `base_model:quantized:Qwen/Qwen2.5-0.5B-Instruct`, `chat`, `conversational`, `en`, `license:apache-2.0`, `onnx`, `qwen2`, `region:us`, `text-generation`, `transformers.js`

### 12. Qwen2.5 Coder 0.5B Instruct

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen2.5-Coder-0.5B-Instruct")`
- Model ID: `onnx-community/Qwen2.5-Coder-0.5B-Instruct`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.5B`
- Model size: `0.46 GB`
- Disk: `475 MB`
- VRAM: `855 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Qwen2.5 Coder 0.5B Instruct`, `Qwen2.5-Coder-0.5B-Instruct`, `onnx-community/Qwen2.5-Coder-0.5B-Instruct`
- Теги: `LLM`, `base_model:Qwen/Qwen2.5-Coder-0.5B-Instruct`, `base_model:quantized:Qwen/Qwen2.5-Coder-0.5B-Instruct`, `conversational`, `onnx`, `qwen2`, `region:us`, `text-generation`, `transformers.js`

### 13. Qwen3 0.6B DQ

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen3-0.6B-DQ-ONNX")`
- Model ID: `onnx-community/Qwen3-0.6B-DQ-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.6B`
- Model size: `0.3 GB`
- Disk: `312 MB`
- VRAM: `561 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Qwen3 0.6B DQ`, `Qwen3-0.6B-DQ`, `Qwen3-0.6B-DQ-ONNX`, `onnx-community/Qwen3-0.6B-DQ-ONNX`
- Теги: `LLM`, `arxiv:2501.06417`, `base_model:Qwen/Qwen3-0.6B`, `base_model:quantized:Qwen/Qwen3-0.6B`, `conversational`, `onnx`, `qwen3`, `region:us`, `text-generation`, `transformers.js`

### 14. Qwen3 0.6B ONNX

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen3-0.6B-ONNX")`
- Model ID: `onnx-community/Qwen3-0.6B-ONNX`
- Для чего подходит: small transformers модель для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions; языки: multilingual.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.6B`
- Model size: `0.49 GB`
- Disk: `500 MB`
- VRAM: `1100 MB`
- DType: `q4`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen3-0.6B-ONNX`, `qwen3-0.6b-tjs`

### 15. Qwen 3.5 0.8B q4

- Индекс: `xlocllm.unit("LLM", "Qwen3.5-0.8B-q4f16_1-MLC")`
- Model ID: `Qwen3.5-0.8B-q4f16_1-MLC`
- Для чего подходит: Small multilingual chat model for low-end GPUs. Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `mlc`
- Task: `text-generation`
- Provider: `MLC`
- Hardware tier: `small`
- Parameters: `0.8B`
- Model size: `0.63 GB`
- Disk: `650 MB`
- VRAM: `1200 MB`
- DType: `q4f16_1`
- NPU/WebNN: `нет`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen-3.5-0.8b`, `qwen3.5-0.8b`, `qwen-0.8b`

### 16. Qwen3.5 0.8B

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen3.5-0.8B-ONNX")`
- Model ID: `onnx-community/Qwen3.5-0.8B-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.8B`
- Model size: `0.74 GB`
- Disk: `760 MB`
- VRAM: `1368 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen-3.5-0.8b`, `Qwen3.5 0.8B`, `Qwen3.5-0.8B`, `Qwen3.5-0.8B-ONNX`, `onnx-community/Qwen3.5-0.8B-ONNX`, `qwen3.5-0.8b`
- Теги: `LLM`, `base_model:Qwen/Qwen3.5-0.8B`, `base_model:quantized:Qwen/Qwen3.5-0.8B`, `conversational`, `image-text-to-text`, `license:apache-2.0`, `onnx`, `qwen3_5`, `region:us`

### 17. Llama 3.2 1B Instruct q4f16

- Индекс: `xlocllm.unit("LLM", "onnx-community/Llama-3.2-1B-Instruct-q4f16")`
- Model ID: `onnx-community/Llama-3.2-1B-Instruct-q4f16`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `1.0B`
- Model size: `0.51 GB`
- Disk: `520 MB`
- VRAM: `936 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `llama3.2`
- Languages: `en`
- Алиасы: `Llama 3.2 1B Instruct`, `Llama-3.2-1B-Instruct`, `Llama-3.2-1B-Instruct-q4f16`, `onnx-community/Llama-3.2-1B-Instruct-q4f16`
- Теги: `LLM`, `conversational`, `de`, `en`, `facebook`, `fr`, `llama`, `llama-3`, `meta`, `onnx`, `pytorch`, `text-generation`, `transformers.js`

### 18. gemma 3 1b it

- Индекс: `xlocllm.unit("LLM", "onnx-community/gemma-3-1b-it-ONNX")`
- Model ID: `onnx-community/gemma-3-1b-it-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `1.0B`
- Model size: `0.93 GB`
- Disk: `950 MB`
- VRAM: `1710 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `gemma`
- Languages: `en`
- Алиасы: `gemma 3 1b it`, `gemma-3-1b-it`, `gemma-3-1b-it-ONNX`, `onnx-community/gemma-3-1b-it-ONNX`
- Теги: `LLM`, `base_model:google/gemma-3-1b-it`, `base_model:quantized:google/gemma-3-1b-it`, `conversational`, `gemma3_text`, `license:gemma`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 19. gemma 3 1b it

- Индекс: `xlocllm.unit("LLM", "onnx-community/gemma-3-1b-it-ONNX-GQA")`
- Model ID: `onnx-community/gemma-3-1b-it-ONNX-GQA`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `1.0B`
- Model size: `0.93 GB`
- Disk: `950 MB`
- VRAM: `1710 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `gemma 3 1b it`, `gemma-3-1b-it`, `gemma-3-1b-it-ONNX-GQA`, `onnx-community/gemma-3-1b-it-ONNX-GQA`
- Теги: `LLM`, `base_model:google/gemma-3-1b-it`, `base_model:quantized:google/gemma-3-1b-it`, `conversational`, `gemma3_text`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 20. Llama 3.2 1B Instruct

- Индекс: `xlocllm.unit("LLM", "onnx-community/Llama-3.2-1B-Instruct-ONNX")`
- Model ID: `onnx-community/Llama-3.2-1B-Instruct-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `1.0B`
- Model size: `0.93 GB`
- Disk: `950 MB`
- VRAM: `1710 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `llama3.2`
- Languages: `en`
- Алиасы: `Llama 3.2 1B Instruct`, `Llama-3.2-1B-Instruct`, `Llama-3.2-1B-Instruct-ONNX`, `onnx-community/Llama-3.2-1B-Instruct-ONNX`
- Теги: `LLM`, `base_model:meta-llama/Llama-3.2-1B-Instruct`, `base_model:quantized:meta-llama/Llama-3.2-1B-Instruct`, `conversational`, `license:llama3.2`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 21. Llama 3.2 1B Instruct q4

- Индекс: `xlocllm.unit("LLM", "Llama-3.2-1B-Instruct-q4f16_1-MLC")`
- Model ID: `Llama-3.2-1B-Instruct-q4f16_1-MLC`
- Для чего подходит: small mlc модель для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions; языки: en, multilingual.
- Runtime: `mlc`
- Task: `text-generation`
- Provider: `MLC`
- Hardware tier: `small`
- Parameters: `1.0B`
- Model size: `0.83 GB`
- Disk: `850 MB`
- VRAM: `1800 MB`
- DType: `q4f16_1`
- NPU/WebNN: `нет`
- License: `llama3.2`
- Languages: `en, multilingual`
- Алиасы: `Llama-3.2-1b`, `llama-1b`

### 22. Phi 4 mini Instruct q4

- Индекс: `xlocllm.unit("LLM", "Phi-4-mini-instruct-q4f16_1-MLC")`
- Model ID: `Phi-4-mini-instruct-q4f16_1-MLC`
- Для чего подходит: medium mlc модель для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions; языки: en, multilingual.
- Runtime: `mlc`
- Task: `text-generation`
- Provider: `MLC`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `2.44 GB`
- Disk: `2500 MB`
- VRAM: `4200 MB`
- DType: `q4f16_1`
- NPU/WebNN: `нет`
- License: `mit`
- Languages: `en, multilingual`
- Алиасы: `Phi-4-mini`, `phi4-mini`

### 23. Qwen3.5 0.8B ONNX FP16

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen3.5-0.8B-ONNX#fp16")`
- Model ID: `onnx-community/Qwen3.5-0.8B-ONNX#fp16`
- Backend model ID: `onnx-community/Qwen3.5-0.8B-ONNX`
- Для чего подходит: Higher-quality non-q4 ONNX variant; uses FP16 files from the same HF repo. Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `0.8B`
- Model size: `1.52 GB`
- Disk: `1560 MB`
- VRAM: `2200 MB`
- DType: `fp16`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen-3.5-0.8b-fp16`, `Qwen-3.5-0.8b-no-q4`, `Qwen-3.5-0.8b-unquantized`, `Qwen3.5-0.8B-ONNX-fp16`, `qwen3.5-0.8b-fp16`
- Теги: `LLM`, `no-q4`, `fp16`, `onnx`, `qwen3_5`, `conversational`

### 24. Qwen3.5 0.8B ONNX FP32

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen3.5-0.8B-ONNX#fp32")`
- Model ID: `onnx-community/Qwen3.5-0.8B-ONNX#fp32`
- Backend model ID: `onnx-community/Qwen3.5-0.8B-ONNX`
- Для чего подходит: Full precision ONNX variant without q4/q8 quantization. Heavier than the default MLC q4 profile. Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `0.8B`
- Model size: `2.95 GB`
- Disk: `3020 MB`
- VRAM: `3600 MB`
- DType: `fp32`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen-3.5-0.8b-full`, `Qwen-3.5-0.8b-fp32`, `Qwen-3.5-0.8b-no-quant`, `Qwen3.5-0.8B-ONNX-fp32`, `qwen3.5-0.8b-full`
- Теги: `LLM`, `full`, `fp32`, `onnx`, `qwen3_5`, `conversational`

### 25. Qwen 2.5 1.5B Instruct q4

- Индекс: `xlocllm.unit("LLM", "Qwen2.5-1.5B-Instruct-q4f16_1-MLC")`
- Model ID: `Qwen2.5-1.5B-Instruct-q4f16_1-MLC`
- Для чего подходит: medium mlc модель для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions; языки: multilingual.
- Runtime: `mlc`
- Task: `text-generation`
- Provider: `MLC`
- Hardware tier: `medium`
- Parameters: `1.5B`
- Model size: `1.12 GB`
- Disk: `1150 MB`
- VRAM: `2200 MB`
- DType: `q4f16_1`
- NPU/WebNN: `нет`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen-2.5-1.5b`, `qwen2.5-1.5b`

### 26. DeepSeek R1 Distill Qwen 1.5B

- Индекс: `xlocllm.unit("LLM", "onnx-community/DeepSeek-R1-Distill-Qwen-1.5B-ONNX")`
- Model ID: `onnx-community/DeepSeek-R1-Distill-Qwen-1.5B-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `1.5B`
- Model size: `1.39 GB`
- Disk: `1425 MB`
- VRAM: `2565 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `DeepSeek R1 Distill Qwen 1.5B`, `DeepSeek-R1-Distill-Qwen-1.5B`, `DeepSeek-R1-Distill-Qwen-1.5B-ONNX`, `onnx-community/DeepSeek-R1-Distill-Qwen-1.5B-ONNX`
- Теги: `LLM`, `base_model:deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`, `base_model:quantized:deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`, `conversational`, `onnx`, `qwen2`, `region:us`, `text-generation`, `transformers.js`

### 27. Qwen2.5 Coder 1.5B Instruct

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen2.5-Coder-1.5B-Instruct")`
- Model ID: `onnx-community/Qwen2.5-Coder-1.5B-Instruct`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `1.5B`
- Model size: `1.39 GB`
- Disk: `1425 MB`
- VRAM: `2565 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen2.5 Coder 1.5B Instruct`, `Qwen2.5-Coder-1.5B-Instruct`, `onnx-community/Qwen2.5-Coder-1.5B-Instruct`
- Теги: `LLM`, `base_model:Qwen/Qwen2.5-Coder-1.5B-Instruct`, `base_model:quantized:Qwen/Qwen2.5-Coder-1.5B-Instruct`, `conversational`, `license:apache-2.0`, `onnx`, `qwen2`, `region:us`, `text-generation`, `transformers.js`

### 28. Qwen3 1.7B

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen3-1.7B-ONNX")`
- Model ID: `onnx-community/Qwen3-1.7B-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `1.7B`
- Model size: `1.58 GB`
- Disk: `1615 MB`
- VRAM: `2907 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Qwen3 1.7B`, `Qwen3-1.7B`, `Qwen3-1.7B-ONNX`, `onnx-community/Qwen3-1.7B-ONNX`
- Теги: `LLM`, `base_model:Qwen/Qwen3-1.7B`, `base_model:quantized:Qwen/Qwen3-1.7B`, `conversational`, `onnx`, `qwen3`, `region:us`, `text-generation`, `transformers.js`

### 29. SmolLM2 1.7B Instruct

- Индекс: `xlocllm.unit("LLM", "HuggingFaceTB/SmolLM2-1.7B-Instruct")`
- Model ID: `HuggingFaceTB/SmolLM2-1.7B-Instruct`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `HuggingFaceTB`
- Hardware tier: `medium`
- Parameters: `1.7B`
- Model size: `1.58 GB`
- Disk: `1615 MB`
- VRAM: `2907 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `HuggingFaceTB/SmolLM2-1.7B-Instruct`, `SmolLM2 1.7B Instruct`, `SmolLM2-1.7B-Instruct`
- Теги: `LLM`, `arxiv:2502.02737`, `base_model:HuggingFaceTB/SmolLM2-1.7B`, `base_model:quantized:HuggingFaceTB/SmolLM2-1.7B`, `conversational`, `en`, `llama`, `onnx`, `safetensors`, `tensorboard`, `text-generation`, `transformers`, `transformers.js`

### 30. Llama 3.2 3B

- Индекс: `xlocllm.unit("LLM", "onnx-community/Llama-3.2-3B")`
- Model ID: `onnx-community/Llama-3.2-3B`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `3.0B`
- Model size: `2.78 GB`
- Disk: `2850 MB`
- VRAM: `5130 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `llama3.2`
- Languages: `en`
- Алиасы: `Llama 3.2 3B`, `Llama-3.2-3B`, `onnx-community/Llama-3.2-3B`
- Теги: `LLM`, `base_model:meta-llama/Llama-3.2-3B`, `base_model:quantized:meta-llama/Llama-3.2-3B`, `license:llama3.2`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 31. Llama 3.2 3B Instruct

- Индекс: `xlocllm.unit("LLM", "onnx-community/Llama-3.2-3B-Instruct-ONNX")`
- Model ID: `onnx-community/Llama-3.2-3B-Instruct-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `3.0B`
- Model size: `2.78 GB`
- Disk: `2850 MB`
- VRAM: `5130 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `llama3.2`
- Languages: `en`
- Алиасы: `Llama 3.2 3B Instruct`, `Llama-3.2-3B-Instruct`, `Llama-3.2-3B-Instruct-ONNX`, `onnx-community/Llama-3.2-3B-Instruct-ONNX`
- Теги: `LLM`, `base_model:meta-llama/Llama-3.2-3B-Instruct`, `base_model:quantized:meta-llama/Llama-3.2-3B-Instruct`, `conversational`, `license:llama3.2`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 32. Qwen2.5 Coder 3B Instruct

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen2.5-Coder-3B-Instruct")`
- Model ID: `onnx-community/Qwen2.5-Coder-3B-Instruct`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `3.0B`
- Model size: `2.78 GB`
- Disk: `2850 MB`
- VRAM: `5130 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Qwen2.5 Coder 3B Instruct`, `Qwen2.5-Coder-3B-Instruct`, `onnx-community/Qwen2.5-Coder-3B-Instruct`
- Теги: `LLM`, `base_model:Qwen/Qwen2.5-Coder-3B-Instruct`, `base_model:quantized:Qwen/Qwen2.5-Coder-3B-Instruct`, `conversational`, `onnx`, `qwen2`, `region:us`, `text-generation`, `transformers.js`

### 33. SmolLM3 3B

- Индекс: `xlocllm.unit("LLM", "HuggingFaceTB/SmolLM3-3B-ONNX")`
- Model ID: `HuggingFaceTB/SmolLM3-3B-ONNX`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `HuggingFaceTB`
- Hardware tier: `medium`
- Parameters: `3.0B`
- Model size: `2.78 GB`
- Disk: `2850 MB`
- VRAM: `5130 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `HuggingFaceTB/SmolLM3-3B-ONNX`, `SmolLM3 3B`, `SmolLM3-3B`, `SmolLM3-3B-ONNX`
- Теги: `LLM`, `ar`, `conversational`, `en`, `es`, `fr`, `it`, `onnx`, `pt`, `smollm3`, `text-generation`, `transformers.js`, `zh`

### 34. SmolLM3 3B Base

- Индекс: `xlocllm.unit("LLM", "HuggingFaceTB/SmolLM3-3B-Base")`
- Model ID: `HuggingFaceTB/SmolLM3-3B-Base`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `HuggingFaceTB`
- Hardware tier: `medium`
- Parameters: `3.0B`
- Model size: `2.78 GB`
- Disk: `2850 MB`
- VRAM: `5130 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `HuggingFaceTB/SmolLM3-3B-Base`, `SmolLM3 3B Base`, `SmolLM3-3B-Base`
- Теги: `LLM`, `en`, `es`, `fr`, `it`, `onnx`, `pt`, `safetensors`, `smollm3`, `text-generation`, `transformers`, `transformers.js`, `zh`

### 35. Qwen3 4B

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen3-4B-ONNX")`
- Model ID: `onnx-community/Qwen3-4B-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `4.0B`
- Model size: `3.71 GB`
- Disk: `3800 MB`
- VRAM: `6840 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Qwen3 4B`, `Qwen3-4B`, `Qwen3-4B-ONNX`, `onnx-community/Qwen3-4B-ONNX`
- Теги: `LLM`, `base_model:Qwen/Qwen3-4B`, `base_model:quantized:Qwen/Qwen3-4B`, `conversational`, `onnx`, `qwen3`, `region:us`, `text-generation`, `transformers.js`

### 36. Qwen3 8B

- Индекс: `xlocllm.unit("LLM", "onnx-community/Qwen3-8B-ONNX")`
- Model ID: `onnx-community/Qwen3-8B-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `large`
- Parameters: `8.0B`
- Model size: `7.42 GB`
- Disk: `7600 MB`
- VRAM: `13680 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen3 8B`, `Qwen3-8B`, `Qwen3-8B-ONNX`, `onnx-community/Qwen3-8B-ONNX`
- Теги: `LLM`, `ONNX`, `ONNX Runtime`, `base_model:Qwen/Qwen3-8B`, `base_model:quantized:Qwen/Qwen3-8B`, `code`, `en`, `license:apache-2.0`, `nlp`, `onnx`, `qwen3`, `region:us`

### 37. gpt oss 20b

- Индекс: `xlocllm.unit("LLM", "onnx-community/gpt-oss-20b-ONNX")`
- Model ID: `onnx-community/gpt-oss-20b-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `large`
- Parameters: `20.0B`
- Model size: `18.55 GB`
- Disk: `19000 MB`
- VRAM: `34200 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `gpt oss 20b`, `gpt-oss-20b`, `gpt-oss-20b-ONNX`, `onnx-community/gpt-oss-20b-ONNX`
- Теги: `LLM`, `base_model:openai/gpt-oss-20b`, `base_model:quantized:openai/gpt-oss-20b`, `conversational`, `gpt_oss`, `license:apache-2.0`, `mxfp4`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 38. gpt oss 20b

- Индекс: `xlocllm.unit("LLM", "onnxruntime/gpt-oss-20b-onnx")`
- Model ID: `onnxruntime/gpt-oss-20b-onnx`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: чат, генерация текста, рассуждение, помощь с кодом и OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnxruntime`
- Hardware tier: `large`
- Parameters: `20.0B`
- Model size: `18.55 GB`
- Disk: `19000 MB`
- VRAM: `34200 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `gpt oss 20b`, `gpt-oss-20b`, `gpt-oss-20b-onnx`, `onnxruntime/gpt-oss-20b-onnx`
- Теги: `LLM`, `ONNX`, `ONNXRuntime`, `base_model:openai/gpt-oss-20b`, `base_model:quantized:openai/gpt-oss-20b`, `en`, `license:apache-2.0`, `onnx`, `region:us`, `safetensors`

## embedding - Embeddings

Назначение: семантический поиск, retrieval, clustering, vector databases и RAG.
Catalog task: `feature-extraction`.
Invoke endpoint: `embeddings`.

### 1. all-MiniLM-L6-v2

- Индекс: `xlocllm.unit("embedding", "Xenova/all-MiniLM-L6-v2")`
- Model ID: `Xenova/all-MiniLM-L6-v2`
- Для чего подходит: tiny transformers модель для: семантический поиск, retrieval, clustering, vector databases и RAG; языки: en.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.09 GB`
- Disk: `90 MB`
- VRAM: `250 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `all-MiniLM-L6-v2`, `minilm`

### 2. Multilingual E5 small

- Индекс: `xlocllm.unit("embedding", "Xenova/multilingual-e5-small")`
- Model ID: `Xenova/multilingual-e5-small`
- Для чего подходит: tiny transformers модель для: семантический поиск, retrieval, clustering, vector databases и RAG; языки: multilingual.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `350 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `multilingual`
- Алиасы: `multilingual-e5-small`, `e5-small`

### 3. all MiniLM L12 v2

- Индекс: `xlocllm.unit("embedding", "Xenova/all-MiniLM-L12-v2")`
- Model ID: `Xenova/all-MiniLM-L12-v2`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/all-MiniLM-L12-v2`, `all MiniLM L12 v2`, `all-MiniLM-L12-v2`
- Теги: `Embedding`, `Embeddings`, `base_model:quantized:sentence-transformers/all-MiniLM-L12-v2`, `base_model:sentence-transformers/all-MiniLM-L12-v2`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 4. all MiniLM L6 v2

- Индекс: `xlocllm.unit("embedding", "sentence-transformers/all-MiniLM-L6-v2")`
- Model ID: `sentence-transformers/all-MiniLM-L6-v2`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `sentence-transformers`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `all MiniLM L6 v2`, `all-MiniLM-L6-v2`, `sentence-transformers/all-MiniLM-L6-v2`
- Теги: `Embedding`, `Embeddings`, `bert`, `en`, `feature-extraction`, `onnx`, `openvino`, `pytorch`, `rust`, `safetensors`, `sentence-similarity`, `sentence-transformers`, `tf`, `transformers`

### 5. bge base en v1.5

- Индекс: `xlocllm.unit("embedding", "onnx-community/bge-base-en-v1.5-ONNX")`
- Model ID: `onnx-community/bge-base-en-v1.5-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `en`
- Алиасы: `bge base en v1.5`, `bge-base-en-v1.5`, `bge-base-en-v1.5-ONNX`, `onnx-community/bge-base-en-v1.5-ONNX`
- Теги: `Embedding`, `Embeddings`, `base_model:BAAI/bge-base-en-v1.5`, `base_model:quantized:BAAI/bge-base-en-v1.5`, `bert`, `en`, `endpoints_compatible`, `feature-extraction`, `license:mit`, `onnx`, `sentence-similarity`, `sentence-transformers`, `text-embeddings-inference`, `transformers.js`

### 6. bge base en v1.5

- Индекс: `xlocllm.unit("embedding", "Xenova/bge-base-en-v1.5")`
- Model ID: `Xenova/bge-base-en-v1.5`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `en`
- Алиасы: `Xenova/bge-base-en-v1.5`, `bge base en v1.5`, `bge-base-en-v1.5`
- Теги: `Embedding`, `Embeddings`, `base_model:BAAI/bge-base-en-v1.5`, `base_model:quantized:BAAI/bge-base-en-v1.5`, `bert`, `feature-extraction`, `license:mit`, `onnx`, `region:us`, `transformers.js`

### 7. bge large en v1.5

- Индекс: `xlocllm.unit("embedding", "Xenova/bge-large-en-v1.5")`
- Model ID: `Xenova/bge-large-en-v1.5`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/bge-large-en-v1.5`, `bge large en v1.5`, `bge-large-en-v1.5`
- Теги: `Embedding`, `Embeddings`, `base_model:BAAI/bge-large-en-v1.5`, `base_model:quantized:BAAI/bge-large-en-v1.5`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 8. bge large zh v1.5

- Индекс: `xlocllm.unit("embedding", "baby2008/bge-large-zh-v1.5")`
- Model ID: `baby2008/bge-large-zh-v1.5`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `baby2008`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `baby2008/bge-large-zh-v1.5`, `bge large zh v1.5`, `bge-large-zh-v1.5`
- Теги: `Embedding`, `Embeddings`, `base_model:BAAI/bge-large-zh-v1.5`, `base_model:quantized:BAAI/bge-large-zh-v1.5`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 9. bge m3

- Индекс: `xlocllm.unit("embedding", "Xenova/bge-m3")`
- Model ID: `Xenova/bge-m3`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `multilingual`
- Алиасы: `Xenova/bge-m3`, `bge m3`, `bge-m3`
- Теги: `Embedding`, `Embeddings`, `base_model:BAAI/bge-m3`, `base_model:quantized:BAAI/bge-m3`, `feature-extraction`, `license:mit`, `onnx`, `region:us`, `transformers.js`, `xlm-roberta`

### 10. bge small en v1.5

- Индекс: `xlocllm.unit("embedding", "onnx-community/bge-small-en-v1.5-ONNX")`
- Model ID: `onnx-community/bge-small-en-v1.5-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `bge small en v1.5`, `bge-small-en-v1.5`, `bge-small-en-v1.5-ONNX`, `onnx-community/bge-small-en-v1.5-ONNX`
- Теги: `Embedding`, `Embeddings`, `base_model:BAAI/bge-small-en-v1.5`, `base_model:quantized:BAAI/bge-small-en-v1.5`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 11. bge small zh v1.5

- Индекс: `xlocllm.unit("embedding", "vteaw/bge-small-zh-v1.5")`
- Model ID: `vteaw/bge-small-zh-v1.5`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `vteaw`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `bge small zh v1.5`, `bge-small-zh-v1.5`, `vteaw/bge-small-zh-v1.5`
- Теги: `Embedding`, `Embeddings`, `base_model:BAAI/bge-small-zh-v1.5`, `base_model:quantized:BAAI/bge-small-zh-v1.5`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 12. gte multilingual base

- Индекс: `xlocllm.unit("embedding", "baby2008/gte-multilingual-base")`
- Model ID: `baby2008/gte-multilingual-base`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `baby2008`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `baby2008/gte-multilingual-base`, `gte multilingual base`, `gte-multilingual-base`
- Теги: `Embedding`, `Embeddings`, `base_model:Alibaba-NLP/gte-multilingual-base`, `base_model:quantized:Alibaba-NLP/gte-multilingual-base`, `custom_code`, `feature-extraction`, `new`, `onnx`, `region:us`, `transformers.js`

### 13. jina clip v1

- Индекс: `xlocllm.unit("embedding", "jinaai/jina-clip-v1")`
- Model ID: `jinaai/jina-clip-v1`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `jinaai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `jina clip v1`, `jina-clip-v1`, `jinaai/jina-clip-v1`
- Теги: `Embedding`, `Embeddings`, `clip`, `feature-extraction`, `jina_clip`, `mteb`, `onnx`, `pytorch`, `safetensors`, `sentence-similarity`, `sentence-transformers`, `transformers`, `transformers.js`, `vision`

### 14. jina clip v2

- Индекс: `xlocllm.unit("embedding", "jinaai/jina-clip-v2")`
- Model ID: `jinaai/jina-clip-v2`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `jinaai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-nc-4.0`
- Languages: `multilingual`
- Алиасы: `jina clip v2`, `jina-clip-v2`, `jinaai/jina-clip-v2`
- Теги: `Embedding`, `Embeddings`, `clip`, `eva02`, `feature-extraction`, `jina_clip`, `multimodal`, `onnx`, `pytorch`, `retrieval`, `safetensors`, `sentence-similarity`, `transformers`, `xlm-roberta`

### 15. jina embeddings v3

- Индекс: `xlocllm.unit("embedding", "jinaai/jina-embeddings-v3")`
- Model ID: `jinaai/jina-embeddings-v3`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `jinaai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-nc-4.0`
- Languages: `multilingual`
- Алиасы: `jina embeddings v3`, `jina-embeddings-v3`, `jinaai/jina-embeddings-v3`
- Теги: `Embedding`, `Embeddings`, `af`, `am`, `custom_code`, `feature-extraction`, `mteb`, `multilingual`, `onnx`, `pytorch`, `safetensors`, `sentence-similarity`, `sentence-transformers`, `transformers`

### 16. jina embeddings v5 omni nano

- Индекс: `xlocllm.unit("embedding", "onnx-community/jina-embeddings-v5-omni-nano-ONNX")`
- Model ID: `onnx-community/jina-embeddings-v5-omni-nano-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-nc-4.0`
- Languages: `multilingual`
- Алиасы: `jina embeddings v5 omni nano`, `jina-embeddings-v5-omni-nano`, `jina-embeddings-v5-omni-nano-ONNX`, `onnx-community/jina-embeddings-v5-omni-nano-ONNX`
- Теги: `Embedding`, `Embeddings`, `cross-modal-retrieval`, `custom_code`, `embeddings`, `feature-extraction`, `jina-embeddings`, `jina_embeddings_v5_omni`, `multilingual`, `multimodal`, `onnx`, `sentence-similarity`, `transformers.js`, `webgpu`

### 17. multilingual e5 base

- Индекс: `xlocllm.unit("embedding", "Xenova/multilingual-e5-base")`
- Model ID: `Xenova/multilingual-e5-base`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/multilingual-e5-base`, `multilingual e5 base`, `multilingual-e5-base`
- Теги: `Embedding`, `Embeddings`, `base_model:intfloat/multilingual-e5-base`, `base_model:quantized:intfloat/multilingual-e5-base`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`, `xlm-roberta`

### 18. multilingual e5 large

- Индекс: `xlocllm.unit("embedding", "Xenova/multilingual-e5-large")`
- Model ID: `Xenova/multilingual-e5-large`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/multilingual-e5-large`, `multilingual e5 large`, `multilingual-e5-large`
- Теги: `Embedding`, `Embeddings`, `base_model:intfloat/multilingual-e5-large`, `base_model:quantized:intfloat/multilingual-e5-large`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`, `xlm-roberta`

### 19. mxbai embed xsmall v1

- Индекс: `xlocllm.unit("embedding", "mixedbread-ai/mxbai-embed-xsmall-v1")`
- Model ID: `mixedbread-ai/mxbai-embed-xsmall-v1`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `mixedbread-ai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `mixedbread-ai/mxbai-embed-xsmall-v1`, `mxbai embed xsmall v1`, `mxbai-embed-xsmall-v1`
- Теги: `Embedding`, `Embeddings`, `arxiv:2309.12871`, `arxiv:2402.14776`, `base_model:mixedbread-ai/mxbai-embed-xsmall-v1`, `bert`, `en`, `feature-extraction`, `gguf`, `mteb`, `onnx`, `openvino`, `safetensors`, `sentence-transformers`

### 20. nomic embed text v1

- Индекс: `xlocllm.unit("embedding", "Xenova/nomic-embed-text-v1")`
- Model ID: `Xenova/nomic-embed-text-v1`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/nomic-embed-text-v1`, `nomic embed text v1`, `nomic-embed-text-v1`
- Теги: `Embedding`, `Embeddings`, `base_model:nomic-ai/nomic-embed-text-v1`, `base_model:quantized:nomic-ai/nomic-embed-text-v1`, `custom_code`, `feature-extraction`, `nomic_bert`, `onnx`, `region:us`, `transformers.js`

### 21. nomic embed text v1.5

- Индекс: `xlocllm.unit("embedding", "nomic-ai/nomic-embed-text-v1.5")`
- Model ID: `nomic-ai/nomic-embed-text-v1.5`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `nomic-ai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `nomic embed text v1.5`, `nomic-ai/nomic-embed-text-v1.5`, `nomic-embed-text-v1.5`
- Теги: `Embedding`, `Embeddings`, `arxiv:2402.01613`, `custom_code`, `en`, `feature-extraction`, `mteb`, `nomic_bert`, `onnx`, `safetensors`, `sentence-similarity`, `sentence-transformers`, `transformers`, `transformers.js`

### 22. paraphrase MiniLM L6 v2

- Индекс: `xlocllm.unit("embedding", "Xenova/paraphrase-MiniLM-L6-v2")`
- Model ID: `Xenova/paraphrase-MiniLM-L6-v2`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/paraphrase-MiniLM-L6-v2`, `paraphrase MiniLM L6 v2`, `paraphrase-MiniLM-L6-v2`
- Теги: `Embedding`, `Embeddings`, `base_model:quantized:sentence-transformers/paraphrase-MiniLM-L6-v2`, `base_model:sentence-transformers/paraphrase-MiniLM-L6-v2`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 23. paraphrase multilingual MiniLM L12 v2

- Индекс: `xlocllm.unit("embedding", "Xenova/paraphrase-multilingual-MiniLM-L12-v2")`
- Model ID: `Xenova/paraphrase-multilingual-MiniLM-L12-v2`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/paraphrase-multilingual-MiniLM-L12-v2`, `paraphrase multilingual MiniLM L12 v2`, `paraphrase-multilingual-MiniLM-L12-v2`
- Теги: `Embedding`, `Embeddings`, `base_model:quantized:sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, `base_model:sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 24. paraphrase multilingual mpnet base v2

- Индекс: `xlocllm.unit("embedding", "Xenova/paraphrase-multilingual-mpnet-base-v2")`
- Model ID: `Xenova/paraphrase-multilingual-mpnet-base-v2`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/paraphrase-multilingual-mpnet-base-v2`, `paraphrase multilingual mpnet base v2`, `paraphrase-multilingual-mpnet-base-v2`
- Теги: `Embedding`, `Embeddings`, `base_model:quantized:sentence-transformers/paraphrase-multilingual-mpnet-base-v2`, `base_model:sentence-transformers/paraphrase-multilingual-mpnet-base-v2`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`, `xlm-roberta`

### 25. granite embedding 97m multilingual r2

- Индекс: `xlocllm.unit("embedding", "philipp-zettl/granite-embedding-97m-multilingual-r2-ONNX")`
- Model ID: `philipp-zettl/granite-embedding-97m-multilingual-r2-ONNX`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `philipp-zettl`
- Hardware tier: `tiny`
- Parameters: `0.097B`
- Model size: `0.09 GB`
- Disk: `92 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `granite embedding 97m multilingual r2`, `granite-embedding-97m-multilingual-r2`, `granite-embedding-97m-multilingual-r2-ONNX`, `philipp-zettl/granite-embedding-97m-multilingual-r2-ONNX`
- Теги: `Embedding`, `Embeddings`, `base_model:ibm-granite/granite-embedding-97m-multilingual-r2`, `base_model:quantized:ibm-granite/granite-embedding-97m-multilingual-r2`, `feature-extraction`, `modernbert`, `onnx`, `region:us`, `transformers.js`, `webgpu-export-my-repo`

### 26. granite embedding 107m multilingual

- Индекс: `xlocllm.unit("embedding", "pelagos-ai/granite-embedding-107m-multilingual-ONNX")`
- Model ID: `pelagos-ai/granite-embedding-107m-multilingual-ONNX`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `pelagos-ai`
- Hardware tier: `tiny`
- Parameters: `0.107B`
- Model size: `0.1 GB`
- Disk: `101 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `granite embedding 107m multilingual`, `granite-embedding-107m-multilingual`, `granite-embedding-107m-multilingual-ONNX`, `pelagos-ai/granite-embedding-107m-multilingual-ONNX`
- Теги: `Embedding`, `Embeddings`, `base_model:ibm-granite/granite-embedding-107m-multilingual`, `base_model:quantized:ibm-granite/granite-embedding-107m-multilingual`, `feature-extraction`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `xlm-roberta`

### 27. embeddinggemma 300m qat q8

- Индекс: `xlocllm.unit("embedding", "tooape/embeddinggemma-300m-qat-q8-ONNX")`
- Model ID: `tooape/embeddinggemma-300m-qat-q8-ONNX`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `tooape`
- Hardware tier: `tiny`
- Parameters: `0.3B`
- Model size: `0.15 GB`
- Disk: `156 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `gemma`
- Languages: `en`
- Алиасы: `embeddinggemma 300m qat q8`, `embeddinggemma-300m-qat-q8`, `embeddinggemma-300m-qat-q8-ONNX`, `tooape/embeddinggemma-300m-qat-q8-ONNX`
- Теги: `Embedding`, `Embeddings`, `base_model:google/embeddinggemma-300m`, `base_model:quantized:google/embeddinggemma-300m`, `embeddinggemma`, `feature-extraction`, `gemma3_text`, `license:gemma`, `onnx`, `quantized`, `region:us`, `sentence-similarity`, `transformers.js`

### 28. granite embedding 311m multilingual r2

- Индекс: `xlocllm.unit("embedding", "onnx-community/granite-embedding-311m-multilingual-r2-ONNX")`
- Model ID: `onnx-community/granite-embedding-311m-multilingual-r2-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.311B`
- Model size: `0.29 GB`
- Disk: `295 MB`
- VRAM: `354 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `granite embedding 311m multilingual r2`, `granite-embedding-311m-multilingual-r2`, `granite-embedding-311m-multilingual-r2-ONNX`, `onnx-community/granite-embedding-311m-multilingual-r2-ONNX`
- Теги: `Embedding`, `Embeddings`, `embeddings`, `feature-extraction`, `granite`, `matryoshka`, `modernbert`, `mteb`, `multilingual`, `onnx`, `openvino`, `sentence-similarity`, `transformers`, `transformers.js`

### 29. Qwen3 Embedding 0.6B

- Индекс: `xlocllm.unit("embedding", "onnx-community/Qwen3-Embedding-0.6B-ONNX")`
- Model ID: `onnx-community/Qwen3-Embedding-0.6B-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.6B`
- Model size: `0.56 GB`
- Disk: `570 MB`
- VRAM: `684 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Qwen3 Embedding 0.6B`, `Qwen3-Embedding-0.6B`, `Qwen3-Embedding-0.6B-ONNX`, `onnx-community/Qwen3-Embedding-0.6B-ONNX`
- Теги: `Embedding`, `Embeddings`, `base_model:Qwen/Qwen3-Embedding-0.6B`, `base_model:quantized:Qwen/Qwen3-Embedding-0.6B`, `feature-extraction`, `onnx`, `qwen3`, `region:us`, `transformers.js`

### 30. Qwen3 Embedding 0.6B

- Индекс: `xlocllm.unit("embedding", "EMA-Sakuraba-416/Qwen3-Embedding-0.6B-ONNX")`
- Model ID: `EMA-Sakuraba-416/Qwen3-Embedding-0.6B-ONNX`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: семантический поиск, retrieval, clustering, vector databases и RAG.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `EMA-Sakuraba-416`
- Hardware tier: `small`
- Parameters: `0.6B`
- Model size: `0.56 GB`
- Disk: `570 MB`
- VRAM: `684 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `EMA-Sakuraba-416/Qwen3-Embedding-0.6B-ONNX`, `Qwen3 Embedding 0.6B`, `Qwen3-Embedding-0.6B`, `Qwen3-Embedding-0.6B-ONNX`
- Теги: `Embedding`, `Embeddings`, `base_model:Qwen/Qwen3-Embedding-0.6B`, `base_model:quantized:Qwen/Qwen3-Embedding-0.6B`, `feature-extraction`, `onnx`, `qwen3`, `region:us`, `transformers.js`

### 31. Snowflake Arctic Embed L v2

- Индекс: `xlocllm.unit("embedding", "Snowflake/snowflake-arctic-embed-l-v2.0")`
- Model ID: `Snowflake/snowflake-arctic-embed-l-v2.0`
- Для чего подходит: large transformers модель для: семантический поиск, retrieval, clustering, vector databases и RAG; языки: multilingual.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Snowflake`
- Hardware tier: `large`
- Parameters: `n/a`
- Model size: `1.17 GB`
- Disk: `1200 MB`
- VRAM: `2400 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `arctic-embed-l-v2`, `snowflake-arctic-l`

### 32. Mixedbread embed large

- Индекс: `xlocllm.unit("embedding", "mixedbread-ai/mxbai-embed-large-v1")`
- Model ID: `mixedbread-ai/mxbai-embed-large-v1`
- Для чего подходит: large transformers модель для: семантический поиск, retrieval, clustering, vector databases и RAG; языки: en.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `mixedbread-ai`
- Hardware tier: `large`
- Parameters: `n/a`
- Model size: `1.32 GB`
- Disk: `1350 MB`
- VRAM: `2600 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `mxbai-embed-large`, `mixedbread-large`

## reranker - Rerankers

Назначение: переранжирование документов по релевантности запросу.
Catalog task: `text-ranking`.
Invoke endpoint: `rerank`.

### 1. bge reranker large

- Индекс: `xlocllm.unit("reranker", "Xenova/bge-reranker-large")`
- Model ID: `Xenova/bge-reranker-large`
- Для чего подходит: known browser-ready provider Подходит для: переранжирование документов по релевантности запросу.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/bge-reranker-large`, `bge reranker large`, `bge-reranker-large`
- Теги: `Reranker`, `Rerankers`, `base_model:BAAI/bge-reranker-large`, `base_model:quantized:BAAI/bge-reranker-large`, `endpoints_compatible`, `onnx`, `region:us`, `sentence-transformers`, `text-classification`, `text-embeddings-inference`, `text-ranking`, `transformers.js`, `xlm-roberta`

### 2. bge reranker v2 m3

- Индекс: `xlocllm.unit("reranker", "tss-deposium/bge-reranker-v2-m3-onnx-int8")`
- Model ID: `tss-deposium/bge-reranker-v2-m3-onnx-int8`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: переранжирование документов по релевантности запросу.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `tss-deposium`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `multilingual`
- Алиасы: `bge reranker v2 m3`, `bge-reranker-v2-m3`, `bge-reranker-v2-m3-onnx-int8`, `tss-deposium/bge-reranker-v2-m3-onnx-int8`
- Теги: `Reranker`, `Rerankers`, `base_model:BAAI/bge-reranker-v2-m3`, `base_model:quantized:BAAI/bge-reranker-v2-m3`, `cross-encoder`, `int8`, `license:mit`, `onnx`, `quantized`, `region:us`, `reranker`, `text-classification`, `transformers.js`, `xlm-roberta`

### 3. gte multilingual reranker base

- Индекс: `xlocllm.unit("reranker", "onnx-community/gte-multilingual-reranker-base")`
- Model ID: `onnx-community/gte-multilingual-reranker-base`
- Для чего подходит: known browser-ready provider Подходит для: переранжирование документов по релевантности запросу.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `gte multilingual reranker base`, `gte-multilingual-reranker-base`, `onnx-community/gte-multilingual-reranker-base`
- Теги: `Reranker`, `Rerankers`, `base_model:Alibaba-NLP/gte-multilingual-reranker-base`, `base_model:quantized:Alibaba-NLP/gte-multilingual-reranker-base`, `custom_code`, `new`, `onnx`, `region:us`, `text-classification`, `transformers.js`

### 4. jina reranker v2 base multilingual

- Индекс: `xlocllm.unit("reranker", "jinaai/jina-reranker-v2-base-multilingual")`
- Model ID: `jinaai/jina-reranker-v2-base-multilingual`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: переранжирование документов по релевантности запросу.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `jinaai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-nc-4.0`
- Languages: `multilingual`
- Алиасы: `jina reranker v2 base multilingual`, `jina-reranker-v2-base-multilingual`, `jinaai/jina-reranker-v2-base-multilingual`
- Теги: `Reranker`, `Rerankers`, `cross-encoder`, `custom_code`, `multilingual`, `onnx`, `pytorch`, `reranker`, `safetensors`, `sentence-transformers`, `text-classification`, `text-ranking`, `transformers`, `transformers.js`

### 5. ms marco TinyBERT L 2 v2

- Индекс: `xlocllm.unit("reranker", "Xenova/ms-marco-TinyBERT-L-2-v2")`
- Model ID: `Xenova/ms-marco-TinyBERT-L-2-v2`
- Для чего подходит: known browser-ready provider Подходит для: переранжирование документов по релевантности запросу.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/ms-marco-TinyBERT-L-2-v2`, `ms marco TinyBERT L 2 v2`, `ms-marco-TinyBERT-L-2-v2`
- Теги: `Reranker`, `Rerankers`, `base_model:cross-encoder/ms-marco-TinyBERT-L2-v2`, `base_model:quantized:cross-encoder/ms-marco-TinyBERT-L2-v2`, `bert`, `onnx`, `region:us`, `text-classification`, `transformers.js`

### 6. BGE Reranker base

- Индекс: `xlocllm.unit("reranker", "Xenova/bge-reranker-base")`
- Model ID: `Xenova/bge-reranker-base`
- Для чего подходит: small transformers модель для: переранжирование документов по релевантности запросу; языки: en, zh.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.42 GB`
- Disk: `430 MB`
- VRAM: `850 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `en, zh`
- Алиасы: `bge-reranker-base`

### 7. Qwen3 Reranker 0.6B

- Индекс: `xlocllm.unit("reranker", "onnx-community/Qwen3-Reranker-0.6B-ONNX")`
- Model ID: `onnx-community/Qwen3-Reranker-0.6B-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: переранжирование документов по релевантности запросу.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.6B`
- Model size: `0.56 GB`
- Disk: `570 MB`
- VRAM: `684 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen3 Reranker 0.6B`, `Qwen3-Reranker-0.6B`, `Qwen3-Reranker-0.6B-ONNX`, `onnx-community/Qwen3-Reranker-0.6B-ONNX`
- Теги: `Reranker`, `Rerankers`, `base_model:Qwen/Qwen3-Reranker-0.6B`, `base_model:quantized:Qwen/Qwen3-Reranker-0.6B`, `license:apache-2.0`, `onnx`, `qwen3`, `region:us`, `reranker`, `text-generation`, `text-ranking`, `transformers.js`

### 8. BGE Reranker v2 M3

- Индекс: `xlocllm.unit("reranker", "onnx-community/bge-reranker-v2-m3-ONNX")`
- Model ID: `onnx-community/bge-reranker-v2-m3-ONNX`
- Для чего подходит: medium transformers модель для: переранжирование документов по релевантности запросу; языки: multilingual.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.88 GB`
- Disk: `900 MB`
- VRAM: `1600 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `multilingual`
- Алиасы: `bge-reranker-v2-m3`, `reranker-m3`

## translator - Translators

Назначение: машинный перевод между поддерживаемыми языковыми парами.
Catalog task: `translation`.
Invoke endpoint: `translate`.

### 1. OPUS MT EN-RU

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-en-ru")`
- Model ID: `Xenova/opus-mt-en-ru`
- Для чего подходит: tiny transformers модель для: машинный перевод между поддерживаемыми языковыми парами; языки: en, ru.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.3 GB`
- Disk: `310 MB`
- VRAM: `650 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en, ru`
- Алиасы: `opus-en-ru`

### 2. opus mt de en

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-de-en")`
- Model ID: `Xenova/opus-mt-de-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `de, en`
- Алиасы: `Xenova/opus-mt-de-en`, `opus mt de en`, `opus-mt-de-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-de-en`, `base_model:quantized:Helsinki-NLP/opus-mt-de-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 3. opus mt de en

- Индекс: `xlocllm.unit("translator", "onnx-community/opus-mt-de-en")`
- Model ID: `onnx-community/opus-mt-de-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-4.0`
- Languages: `de, en`
- Алиасы: `onnx-community/opus-mt-de-en`, `opus mt de en`, `opus-mt-de-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-de-en`, `base_model:quantized:Helsinki-NLP/opus-mt-de-en`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 4. opus mt de fr

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-de-fr")`
- Model ID: `Xenova/opus-mt-de-fr`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `de, fr`
- Алиасы: `Xenova/opus-mt-de-fr`, `opus mt de fr`, `opus-mt-de-fr`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-de-fr`, `base_model:quantized:Helsinki-NLP/opus-mt-de-fr`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 5. opus mt en de

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-en-de")`
- Model ID: `Xenova/opus-mt-en-de`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en, de`
- Алиасы: `Xenova/opus-mt-en-de`, `opus mt en de`, `opus-mt-en-de`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-de`, `base_model:quantized:Helsinki-NLP/opus-mt-en-de`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 6. opus mt en de

- Индекс: `xlocllm.unit("translator", "onnx-community/opus-mt-en-de")`
- Model ID: `onnx-community/opus-mt-en-de`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-4.0`
- Languages: `en, de`
- Алиасы: `onnx-community/opus-mt-en-de`, `opus mt en de`, `opus-mt-en-de`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-de`, `base_model:quantized:Helsinki-NLP/opus-mt-en-de`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 7. opus mt en es

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-en-es")`
- Model ID: `Xenova/opus-mt-en-es`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en, es`
- Алиасы: `Xenova/opus-mt-en-es`, `opus mt en es`, `opus-mt-en-es`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-es`, `base_model:quantized:Helsinki-NLP/opus-mt-en-es`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 8. opus mt en es

- Индекс: `xlocllm.unit("translator", "onnx-community/opus-mt-en-es")`
- Model ID: `onnx-community/opus-mt-en-es`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-4.0`
- Languages: `en, es`
- Алиасы: `onnx-community/opus-mt-en-es`, `opus mt en es`, `opus-mt-en-es`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-es`, `base_model:quantized:Helsinki-NLP/opus-mt-en-es`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 9. opus mt en fr

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-en-fr")`
- Model ID: `Xenova/opus-mt-en-fr`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en, fr`
- Алиасы: `Xenova/opus-mt-en-fr`, `opus mt en fr`, `opus-mt-en-fr`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-fr`, `base_model:quantized:Helsinki-NLP/opus-mt-en-fr`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 10. opus mt en fr

- Индекс: `xlocllm.unit("translator", "onnx-community/opus-mt-en-fr")`
- Model ID: `onnx-community/opus-mt-en-fr`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-4.0`
- Languages: `en, fr`
- Алиасы: `onnx-community/opus-mt-en-fr`, `opus mt en fr`, `opus-mt-en-fr`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-fr`, `base_model:quantized:Helsinki-NLP/opus-mt-en-fr`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 11. opus mt en it

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-en-it")`
- Model ID: `Xenova/opus-mt-en-it`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en, it`
- Алиасы: `Xenova/opus-mt-en-it`, `opus mt en it`, `opus-mt-en-it`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-it`, `base_model:quantized:Helsinki-NLP/opus-mt-en-it`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 12. opus mt en zh

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-en-zh")`
- Model ID: `Xenova/opus-mt-en-zh`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en, zh`
- Алиасы: `Xenova/opus-mt-en-zh`, `opus mt en zh`, `opus-mt-en-zh`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-zh`, `base_model:quantized:Helsinki-NLP/opus-mt-en-zh`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 13. opus mt es en

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-es-en")`
- Model ID: `Xenova/opus-mt-es-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `es, en`
- Алиасы: `Xenova/opus-mt-es-en`, `opus mt es en`, `opus-mt-es-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-es-en`, `base_model:quantized:Helsinki-NLP/opus-mt-es-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 14. opus mt es en

- Индекс: `xlocllm.unit("translator", "onnx-community/opus-mt-es-en")`
- Model ID: `onnx-community/opus-mt-es-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-4.0`
- Languages: `es, en`
- Алиасы: `onnx-community/opus-mt-es-en`, `opus mt es en`, `opus-mt-es-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-es-en`, `base_model:quantized:Helsinki-NLP/opus-mt-es-en`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 15. opus mt fr de

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-fr-de")`
- Model ID: `Xenova/opus-mt-fr-de`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `fr, de`
- Алиасы: `Xenova/opus-mt-fr-de`, `opus mt fr de`, `opus-mt-fr-de`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-fr-de`, `base_model:quantized:Helsinki-NLP/opus-mt-fr-de`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 16. opus mt fr en

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-fr-en")`
- Model ID: `Xenova/opus-mt-fr-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `fr, en`
- Алиасы: `Xenova/opus-mt-fr-en`, `opus mt fr en`, `opus-mt-fr-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-fr-en`, `base_model:quantized:Helsinki-NLP/opus-mt-fr-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 17. opus mt fr en

- Индекс: `xlocllm.unit("translator", "onnx-community/opus-mt-fr-en")`
- Model ID: `onnx-community/opus-mt-fr-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-4.0`
- Languages: `fr, en`
- Алиасы: `onnx-community/opus-mt-fr-en`, `opus mt fr en`, `opus-mt-fr-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-fr-en`, `base_model:quantized:Helsinki-NLP/opus-mt-fr-en`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 18. opus mt it en

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-it-en")`
- Model ID: `Xenova/opus-mt-it-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `it, en`
- Алиасы: `Xenova/opus-mt-it-en`, `opus mt it en`, `opus-mt-it-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-it-en`, `base_model:quantized:Helsinki-NLP/opus-mt-it-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 19. opus mt ja en

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-ja-en")`
- Model ID: `Xenova/opus-mt-ja-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `ja, en`
- Алиасы: `Xenova/opus-mt-ja-en`, `opus mt ja en`, `opus-mt-ja-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-ja-en`, `base_model:quantized:Helsinki-NLP/opus-mt-ja-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 20. opus mt ko en

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-ko-en")`
- Model ID: `Xenova/opus-mt-ko-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `ko, en`
- Алиасы: `Xenova/opus-mt-ko-en`, `opus mt ko en`, `opus-mt-ko-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-ko-en`, `base_model:quantized:Helsinki-NLP/opus-mt-ko-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 21. opus mt ru en

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-ru-en")`
- Model ID: `Xenova/opus-mt-ru-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `ru, en`
- Алиасы: `Xenova/opus-mt-ru-en`, `opus mt ru en`, `opus-mt-ru-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-ru-en`, `base_model:quantized:Helsinki-NLP/opus-mt-ru-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 22. opus mt zh en

- Индекс: `xlocllm.unit("translator", "Xenova/opus-mt-zh-en")`
- Model ID: `Xenova/opus-mt-zh-en`
- Для чего подходит: known browser-ready provider Подходит для: машинный перевод между поддерживаемыми языковыми парами.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `zh, en`
- Алиасы: `Xenova/opus-mt-zh-en`, `opus mt zh en`, `opus-mt-zh-en`
- Теги: `Translation`, `base_model:Helsinki-NLP/opus-mt-zh-en`, `base_model:quantized:Helsinki-NLP/opus-mt-zh-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 23. M2M100 418M

- Индекс: `xlocllm.unit("translator", "Xenova/m2m100_418M")`
- Model ID: `Xenova/m2m100_418M`
- Для чего подходит: medium transformers модель для: машинный перевод между поддерживаемыми языковыми парами; языки: multilingual.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `medium`
- Parameters: `0.418B`
- Model size: `0.88 GB`
- Disk: `900 MB`
- VRAM: `1900 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `multilingual`
- Алиасы: `m2m100`, `m2m100-418m`

### 24. NLLB 200 distilled 600M

- Индекс: `xlocllm.unit("translator", "Xenova/nllb-200-distilled-600M")`
- Model ID: `Xenova/nllb-200-distilled-600M`
- Для чего подходит: medium transformers модель для: машинный перевод между поддерживаемыми языковыми парами; языки: multilingual.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `medium`
- Parameters: `0.6B`
- Model size: `1.17 GB`
- Disk: `1200 MB`
- VRAM: `2300 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `cc-by-nc-4.0`
- Languages: `multilingual`
- Алиасы: `nllb-200`, `nllb`

## tts - TTS

Назначение: синтез речи из текста в браузере.
Catalog task: `text-to-speech`.
Invoke endpoint: `tts`.

### 1. mms tts deu

- Индекс: `xlocllm.unit("tts", "Xenova/mms-tts-deu")`
- Model ID: `Xenova/mms-tts-deu`
- Для чего подходит: known browser-ready provider Подходит для: синтез речи из текста в браузере.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/mms-tts-deu`, `mms tts deu`, `mms-tts-deu`
- Теги: `Audio`, `TTS`, `base_model:facebook/mms-tts-deu`, `base_model:quantized:facebook/mms-tts-deu`, `onnx`, `region:us`, `text-to-audio`, `text-to-speech`, `transformers.js`, `vits`

### 2. mms tts eng

- Индекс: `xlocllm.unit("tts", "Xenova/mms-tts-eng")`
- Model ID: `Xenova/mms-tts-eng`
- Для чего подходит: known browser-ready provider Подходит для: синтез речи из текста в браузере.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/mms-tts-eng`, `mms tts eng`, `mms-tts-eng`
- Теги: `Audio`, `TTS`, `base_model:facebook/mms-tts-eng`, `base_model:quantized:facebook/mms-tts-eng`, `onnx`, `region:us`, `text-to-audio`, `text-to-speech`, `transformers.js`, `vits`

### 3. mms tts fra

- Индекс: `xlocllm.unit("tts", "Xenova/mms-tts-fra")`
- Model ID: `Xenova/mms-tts-fra`
- Для чего подходит: known browser-ready provider Подходит для: синтез речи из текста в браузере.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/mms-tts-fra`, `mms tts fra`, `mms-tts-fra`
- Теги: `Audio`, `TTS`, `base_model:facebook/mms-tts-fra`, `base_model:quantized:facebook/mms-tts-fra`, `onnx`, `region:us`, `text-to-audio`, `text-to-speech`, `transformers.js`, `vits`

### 4. mms tts rus

- Индекс: `xlocllm.unit("tts", "Xenova/mms-tts-rus")`
- Model ID: `Xenova/mms-tts-rus`
- Для чего подходит: known browser-ready provider Подходит для: синтез речи из текста в браузере.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/mms-tts-rus`, `mms tts rus`, `mms-tts-rus`
- Теги: `Audio`, `TTS`, `base_model:facebook/mms-tts-rus`, `base_model:quantized:facebook/mms-tts-rus`, `onnx`, `region:us`, `text-to-audio`, `text-to-speech`, `transformers.js`, `vits`

### 5. mms tts spa

- Индекс: `xlocllm.unit("tts", "Xenova/mms-tts-spa")`
- Model ID: `Xenova/mms-tts-spa`
- Для чего подходит: known browser-ready provider Подходит для: синтез речи из текста в браузере.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/mms-tts-spa`, `mms tts spa`, `mms-tts-spa`
- Теги: `Audio`, `TTS`, `base_model:facebook/mms-tts-spa`, `base_model:quantized:facebook/mms-tts-spa`, `onnx`, `region:us`, `text-to-audio`, `text-to-speech`, `transformers.js`, `vits`

### 6. Kokoro 82M

- Индекс: `xlocllm.unit("tts", "onnx-community/Kokoro-82M-v1.0-ONNX")`
- Model ID: `onnx-community/Kokoro-82M-v1.0-ONNX`
- Для чего подходит: tiny transformers модель для: синтез речи из текста в браузере; языки: en.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.082B`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `450 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `kokoro`, `kokoro-82m`

### 7. SpeechT5 TTS

- Индекс: `xlocllm.unit("tts", "Xenova/speecht5_tts")`
- Model ID: `Xenova/speecht5_tts`
- Для чего подходит: small transformers модель для: синтез речи из текста в браузере; языки: en.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `900 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `en`
- Алиасы: `speecht5`

## image-classification - Image Classification

Назначение: классификация изображений и визуальные теги.
Catalog task: `image-classification`.
Invoke endpoint: `image.classify`.

### 1. MobileNet V2

- Индекс: `xlocllm.unit("image-classification", "onnx-community/mobilenet_v2_1.0_224")`
- Model ID: `onnx-community/mobilenet_v2_1.0_224`
- Для чего подходит: tiny transformers модель для: классификация изображений и визуальные теги; языки: n/a.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.02 GB`
- Disk: `25 MB`
- VRAM: `160 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `n/a`
- Алиасы: `mobilenet-v2`, `mobilenet`

### 2. convnext tiny 224

- Индекс: `xlocllm.unit("image-classification", "Xenova/convnext-tiny-224")`
- Model ID: `Xenova/convnext-tiny-224`
- Для чего подходит: known browser-ready provider Подходит для: классификация изображений и визуальные теги.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.09 GB`
- Disk: `90 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/convnext-tiny-224`, `convnext tiny 224`, `convnext-tiny-224`
- Теги: `Image`, `Image Classification`, `base_model:facebook/convnext-tiny-224`, `base_model:quantized:facebook/convnext-tiny-224`, `convnext`, `image-classification`, `onnx`, `region:us`, `transformers.js`

### 3. mobilenetv4 conv small.e2400 r224 in1k

- Индекс: `xlocllm.unit("image-classification", "onnx-community/mobilenetv4_conv_small.e2400_r224_in1k")`
- Model ID: `onnx-community/mobilenetv4_conv_small.e2400_r224_in1k`
- Для чего подходит: known browser-ready provider Подходит для: классификация изображений и визуальные теги.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.09 GB`
- Disk: `90 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `mobilenetv4-conv-small.e2400-r224-in1k`, `mobilenetv4_conv_small.e2400_r224_in1k`, `onnx-community/mobilenetv4_conv_small.e2400_r224_in1k`
- Теги: `Image`, `Image Classification`, `base_model:quantized:timm/mobilenetv4_conv_small.e2400_r224_in1k`, `base_model:timm/mobilenetv4_conv_small.e2400_r224_in1k`, `mobilenet_v4`, `onnx`, `region:us`, `transformers.js`

### 4. swin tiny patch4 window7 224

- Индекс: `xlocllm.unit("image-classification", "Xenova/swin-tiny-patch4-window7-224")`
- Model ID: `Xenova/swin-tiny-patch4-window7-224`
- Для чего подходит: known browser-ready provider Подходит для: классификация изображений и визуальные теги.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.09 GB`
- Disk: `90 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/swin-tiny-patch4-window7-224`, `swin tiny patch4 window7 224`, `swin-tiny-patch4-window7-224`
- Теги: `Image`, `Image Classification`, `base_model:microsoft/swin-tiny-patch4-window7-224`, `base_model:quantized:microsoft/swin-tiny-patch4-window7-224`, `image-classification`, `onnx`, `region:us`, `swin`, `transformers.js`

### 5. vit base patch16 224 in21k

- Индекс: `xlocllm.unit("image-classification", "Xenova/vit-base-patch16-224-in21k")`
- Model ID: `Xenova/vit-base-patch16-224-in21k`
- Для чего подходит: known browser-ready provider Подходит для: классификация изображений и визуальные теги.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.09 GB`
- Disk: `90 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/vit-base-patch16-224-in21k`, `vit base patch16 224 in21k`, `vit-base-patch16-224-in21k`
- Теги: `Image`, `Image Classification`, `base_model:google/vit-base-patch16-224-in21k`, `base_model:quantized:google/vit-base-patch16-224-in21k`, `image-feature-extraction`, `onnx`, `region:us`, `transformers.js`, `vit`

### 6. ViT base 224

- Индекс: `xlocllm.unit("image-classification", "Xenova/vit-base-patch16-224")`
- Model ID: `Xenova/vit-base-patch16-224`
- Для чего подходит: small transformers модель для: классификация изображений и визуальные теги; языки: n/a.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.32 GB`
- Disk: `330 MB`
- VRAM: `700 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `n/a`
- Алиасы: `vit-base-224`

## object-detection - Object Detection

Назначение: детекция объектов, bounding boxes и layout detection на detection-моделях.
Catalog task: `object-detection`.
Invoke endpoint: `image.detect`.

### 1. detr resnet 50 panoptic

- Индекс: `xlocllm.unit("object-detection", "Xenova/detr-resnet-50-panoptic")`
- Model ID: `Xenova/detr-resnet-50-panoptic`
- Для чего подходит: known browser-ready provider Подходит для: детекция объектов, bounding boxes и layout detection на detection-моделях.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/detr-resnet-50-panoptic`, `detr resnet 50 panoptic`, `detr-resnet-50-panoptic`
- Теги: `Image`, `Object Detection`, `base_model:facebook/detr-resnet-50-panoptic`, `base_model:quantized:facebook/detr-resnet-50-panoptic`, `detr`, `image-segmentation`, `onnx`, `region:us`, `transformers.js`

### 2. rfdetr base

- Индекс: `xlocllm.unit("object-detection", "onnx-community/rfdetr_base-ONNX")`
- Model ID: `onnx-community/rfdetr_base-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: детекция объектов, bounding boxes и layout detection на detection-моделях.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `onnx-community/rfdetr_base-ONNX`, `rfdetr-base`, `rfdetr_base`, `rfdetr_base-ONNX`
- Теги: `Image`, `Object Detection`, `license:apache-2.0`, `object-detection`, `onnx`, `region:us`, `rf_detr`, `transformers.js`

### 3. rtdetr r18vd

- Индекс: `xlocllm.unit("object-detection", "onnx-community/rtdetr_r18vd")`
- Model ID: `onnx-community/rtdetr_r18vd`
- Для чего подходит: known browser-ready provider Подходит для: детекция объектов, bounding boxes и layout detection на detection-моделях.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `onnx-community/rtdetr_r18vd`, `rtdetr-r18vd`, `rtdetr_r18vd`
- Теги: `Image`, `Object Detection`, `base_model:PekingU/rtdetr_r18vd`, `base_model:quantized:PekingU/rtdetr_r18vd`, `object-detection`, `onnx`, `region:us`, `rt_detr`, `transformers.js`

### 4. rtdetr r50vd coco o365

- Индекс: `xlocllm.unit("object-detection", "onnx-community/rtdetr_r50vd_coco_o365")`
- Model ID: `onnx-community/rtdetr_r50vd_coco_o365`
- Для чего подходит: known browser-ready provider Подходит для: детекция объектов, bounding boxes и layout detection на detection-моделях.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `onnx-community/rtdetr_r50vd_coco_o365`, `rtdetr-r50vd-coco-o365`, `rtdetr_r50vd_coco_o365`
- Теги: `Image`, `Object Detection`, `base_model:PekingU/rtdetr_r50vd_coco_o365`, `base_model:quantized:PekingU/rtdetr_r50vd_coco_o365`, `object-detection`, `onnx`, `region:us`, `rt_detr`, `transformers.js`

### 5. rtdetr v2 r18vd

- Индекс: `xlocllm.unit("object-detection", "onnx-community/rtdetr_v2_r18vd-ONNX")`
- Model ID: `onnx-community/rtdetr_v2_r18vd-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: детекция объектов, bounding boxes и layout detection на detection-моделях.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `onnx-community/rtdetr_v2_r18vd-ONNX`, `rtdetr-v2-r18vd`, `rtdetr_v2_r18vd`, `rtdetr_v2_r18vd-ONNX`
- Теги: `Image`, `Object Detection`, `base_model:PekingU/rtdetr_v2_r18vd`, `base_model:quantized:PekingU/rtdetr_v2_r18vd`, `license:apache-2.0`, `object-detection`, `onnx`, `region:us`, `rt_detr_v2`, `transformers.js`

### 6. yolo realtime

- Индекс: `xlocllm.unit("object-detection", "kurnie/yolo-realtime")`
- Model ID: `kurnie/yolo-realtime`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: детекция объектов, bounding boxes и layout detection на detection-моделях.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `kurnie`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `gpl-3.0`
- Languages: `universal`
- Алиасы: `kurnie/yolo-realtime`, `yolo realtime`, `yolo-realtime`
- Теги: `Image`, `Object Detection`, `license:gpl-3.0`, `object-detection`, `onnx`, `region:us`, `transformers.js`, `yolov8`

### 7. yolov10m doclaynet

- Индекс: `xlocllm.unit("object-detection", "Oblix/yolov10m-doclaynet_ONNX_document-layout-analysis")`
- Model ID: `Oblix/yolov10m-doclaynet_ONNX_document-layout-analysis`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: детекция объектов, bounding boxes и layout detection на detection-моделях.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Oblix`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Oblix/yolov10m-doclaynet_ONNX_document-layout-analysis`, `yolov10m doclaynet`, `yolov10m-doclaynet`, `yolov10m-doclaynet_ONNX_document-layout-analysis`
- Теги: `Image`, `Object Detection`, `object-detection`, `onnx`, `region:us`, `transformers.js`, `yolov10`

### 8. YOLOS tiny

- Индекс: `xlocllm.unit("object-detection", "Xenova/yolos-tiny")`
- Model ID: `Xenova/yolos-tiny`
- Для чего подходит: tiny transformers модель для: детекция объектов, bounding boxes и layout detection на detection-моделях; языки: n/a.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.11 GB`
- Disk: `110 MB`
- VRAM: `350 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `n/a`
- Алиасы: `yolos-tiny`

### 9. DETR ResNet 50

- Индекс: `xlocllm.unit("object-detection", "Xenova/detr-resnet-50")`
- Model ID: `Xenova/detr-resnet-50`
- Для чего подходит: medium transformers модель для: детекция объектов, bounding boxes и layout detection на detection-моделях; языки: n/a.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Xenova`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.17 GB`
- Disk: `170 MB`
- VRAM: `900 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `n/a`
- Алиасы: `detr-resnet-50`, `detr`

## image-segmentation - Image segmentation/background removing

Назначение: сегментация, portrait matting и удаление фона.
Catalog task: `image-segmentation`.
Invoke endpoint: `image.segment`.

### 1. MODNet portrait matting

- Индекс: `xlocllm.unit("image-segmentation", "Xenova/modnet")`
- Model ID: `Xenova/modnet`
- Для чего подходит: tiny transformers модель для: сегментация, portrait matting и удаление фона; языки: n/a.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.03 GB`
- Disk: `30 MB`
- VRAM: `180 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `n/a`
- Алиасы: `modnet`

### 2. BiRefNet

- Индекс: `xlocllm.unit("image-segmentation", "onnx-community/BiRefNet-ONNX")`
- Model ID: `onnx-community/BiRefNet-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: сегментация, portrait matting и удаление фона.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `universal`
- Алиасы: `BiRefNet`, `BiRefNet-ONNX`, `onnx-community/BiRefNet-ONNX`
- Теги: `Camouflaged Object Detection`, `Dichotomous Image Segmentation`, `Image`, `Image Segmentation`, `Salient Object Detection`, `background-removal`, `base_model:ZhengPeng7/BiRefNet`, `base_model:quantized:ZhengPeng7/BiRefNet`, `birefnet`, `image-segmentation`, `license:mit`, `mask-generation`, `onnx`, `transformers.js`

### 3. birefnet lite 512

- Индекс: `xlocllm.unit("image-segmentation", "studioludens/birefnet-lite-512")`
- Model ID: `studioludens/birefnet-lite-512`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: сегментация, portrait matting и удаление фона.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `studioludens`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `universal`
- Алиасы: `birefnet lite 512`, `birefnet-lite-512`, `studioludens/birefnet-lite-512`
- Теги: `Image`, `Image Segmentation`, `alpha-matting`, `background-removal`, `birefnet`, `dichotomous-image-segmentation`, `foreground-extraction`, `image-matting`, `matting`, `onnx`, `salient-object-detection`, `swin`, `transformers.js`, `webgpu`

### 4. BiRefNet portrait

- Индекс: `xlocllm.unit("image-segmentation", "onnx-community/BiRefNet-portrait-ONNX")`
- Model ID: `onnx-community/BiRefNet-portrait-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: сегментация, portrait matting и удаление фона.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `universal`
- Алиасы: `BiRefNet portrait`, `BiRefNet-portrait`, `BiRefNet-portrait-ONNX`, `onnx-community/BiRefNet-portrait-ONNX`
- Теги: `Camouflaged Object Detection`, `Dichotomous Image Segmentation`, `Image`, `Image Segmentation`, `Salient Object Detection`, `background-removal`, `base_model:ZhengPeng7/BiRefNet-portrait`, `base_model:quantized:ZhengPeng7/BiRefNet-portrait`, `birefnet`, `image-segmentation`, `license:mit`, `mask-generation`, `onnx`, `transformers.js`

### 5. ormbg

- Индекс: `xlocllm.unit("image-segmentation", "onnx-community/ormbg-ONNX")`
- Model ID: `onnx-community/ormbg-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: сегментация, portrait matting и удаление фона.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `onnx-community/ormbg-ONNX`, `ormbg`, `ormbg-ONNX`
- Теги: `Image`, `Image Segmentation`, `background-removal`, `base_model:quantized:schirrmacher/ormbg`, `base_model:schirrmacher/ormbg`, `image-segmentation`, `isnet`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`

### 6. RMBG 1.4

- Индекс: `xlocllm.unit("image-segmentation", "SolonD/RMBG-1.4")`
- Model ID: `SolonD/RMBG-1.4`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: сегментация, portrait matting и удаление фона.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `SolonD`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `other`
- Languages: `universal`
- Алиасы: `RMBG 1.4`, `RMBG-1.4`, `SolonD/RMBG-1.4`
- Теги: `Image`, `Image Segmentation`, `Pytorch`, `SegformerForSemanticSegmentation`, `background`, `background-removal`, `image-segmentation`, `legal liability`, `onnx`, `pytorch`, `remove background`, `safetensors`, `transformers`, `vision`

### 7. U 2 Net

- Индекс: `xlocllm.unit("image-segmentation", "BritishWerewolf/U-2-Net")`
- Model ID: `BritishWerewolf/U-2-Net`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: сегментация, portrait matting и удаление фона.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `BritishWerewolf`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `BritishWerewolf/U-2-Net`, `U 2 Net`, `U-2-Net`
- Теги: `Image`, `Image Segmentation`, `background-removal`, `en`, `endpoints_compatible`, `image-segmentation`, `license:apache-2.0`, `mask-generation`, `onnx`, `portrait-matting`, `transformers`, `transformers.js`, `u2net`, `vision`

### 8. U 2 Netp

- Индекс: `xlocllm.unit("image-segmentation", "BritishWerewolf/U-2-Netp")`
- Model ID: `BritishWerewolf/U-2-Netp`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: сегментация, portrait matting и удаление фона.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `BritishWerewolf`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `BritishWerewolf/U-2-Netp`, `U 2 Netp`, `U-2-Netp`
- Теги: `Image`, `Image Segmentation`, `background-removal`, `en`, `endpoints_compatible`, `image-segmentation`, `license:apache-2.0`, `mask-generation`, `onnx`, `portrait-matting`, `transformers`, `transformers.js`, `u2net`, `vision`

### 9. BEN2 background removal

- Индекс: `xlocllm.unit("image-segmentation", "onnx-community/BEN2-ONNX")`
- Model ID: `onnx-community/BEN2-ONNX`
- Для чего подходит: medium transformers модель для: сегментация, portrait matting и удаление фона; языки: n/a.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.66 GB`
- Disk: `680 MB`
- VRAM: `1300 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `n/a`
- Алиасы: `ben2`, `background-removal`

## depth-estimation - Depth estimator

Назначение: карты глубины и оценка относительной глубины сцены.
Catalog task: `depth-estimation`.
Invoke endpoint: `depth`.

### 1. depth anything base hf

- Индекс: `xlocllm.unit("depth-estimation", "Xenova/depth-anything-base-hf")`
- Model ID: `Xenova/depth-anything-base-hf`
- Для чего подходит: known browser-ready provider Подходит для: карты глубины и оценка относительной глубины сцены.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/depth-anything-base-hf`, `depth anything base hf`, `depth-anything-base-hf`
- Теги: `Depth`, `Image`, `base_model:LiheYoung/depth-anything-base-hf`, `base_model:quantized:LiheYoung/depth-anything-base-hf`, `depth-estimation`, `depth_anything`, `onnx`, `region:us`, `transformers.js`

### 2. depth anything large hf

- Индекс: `xlocllm.unit("depth-estimation", "Xenova/depth-anything-large-hf")`
- Model ID: `Xenova/depth-anything-large-hf`
- Для чего подходит: known browser-ready provider Подходит для: карты глубины и оценка относительной глубины сцены.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/depth-anything-large-hf`, `depth anything large hf`, `depth-anything-large-hf`
- Теги: `Depth`, `Image`, `base_model:LiheYoung/depth-anything-large-hf`, `base_model:quantized:LiheYoung/depth-anything-large-hf`, `depth-estimation`, `depth_anything`, `onnx`, `region:us`, `transformers.js`

### 3. depth anything small hf

- Индекс: `xlocllm.unit("depth-estimation", "Xenova/depth-anything-small-hf")`
- Model ID: `Xenova/depth-anything-small-hf`
- Для чего подходит: known browser-ready provider Подходит для: карты глубины и оценка относительной глубины сцены.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/depth-anything-small-hf`, `depth anything small hf`, `depth-anything-small-hf`
- Теги: `Depth`, `Image`, `base_model:LiheYoung/depth-anything-small-hf`, `base_model:quantized:LiheYoung/depth-anything-small-hf`, `depth-estimation`, `depth_anything`, `onnx`, `region:us`, `transformers.js`

### 4. depth anything v2 base

- Индекс: `xlocllm.unit("depth-estimation", "onnx-community/depth-anything-v2-base")`
- Model ID: `onnx-community/depth-anything-v2-base`
- Для чего подходит: known browser-ready provider Подходит для: карты глубины и оценка относительной глубины сцены.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-nc-4.0`
- Languages: `universal`
- Алиасы: `depth anything v2 base`, `depth-anything-v2-base`, `onnx-community/depth-anything-v2-base`
- Теги: `Depth`, `Image`, `base_model:depth-anything/Depth-Anything-V2-Base`, `base_model:quantized:depth-anything/Depth-Anything-V2-Base`, `depth-estimation`, `depth_anything`, `license:cc-by-nc-4.0`, `onnx`, `region:us`, `transformers.js`

### 5. depth anything v2 large

- Индекс: `xlocllm.unit("depth-estimation", "onnx-community/depth-anything-v2-large-ONNX")`
- Model ID: `onnx-community/depth-anything-v2-large-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: карты глубины и оценка относительной глубины сцены.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `cc-by-nc-4.0`
- Languages: `universal`
- Алиасы: `depth anything v2 large`, `depth-anything-v2-large`, `depth-anything-v2-large-ONNX`, `onnx-community/depth-anything-v2-large-ONNX`
- Теги: `Depth`, `Image`, `base_model:depth-anything/Depth-Anything-V2-Large`, `base_model:quantized:depth-anything/Depth-Anything-V2-Large`, `depth-estimation`, `depth_anything`, `license:cc-by-nc-4.0`, `onnx`, `region:us`, `transformers.js`

### 6. depth anything v2 small

- Индекс: `xlocllm.unit("depth-estimation", "onnx-community/depth-anything-v2-small-ONNX")`
- Model ID: `onnx-community/depth-anything-v2-small-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: карты глубины и оценка относительной глубины сцены.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `depth anything v2 small`, `depth-anything-v2-small`, `depth-anything-v2-small-ONNX`, `onnx-community/depth-anything-v2-small-ONNX`
- Теги: `Depth`, `Image`, `base_model:depth-anything/Depth-Anything-V2-Small`, `base_model:quantized:depth-anything/Depth-Anything-V2-Small`, `depth-estimation`, `depth_anything`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`

### 7. Depth Anything V2 small

- Индекс: `xlocllm.unit("depth-estimation", "onnx-community/depth-anything-v2-small")`
- Model ID: `onnx-community/depth-anything-v2-small`
- Для чего подходит: small transformers модель для: карты глубины и оценка относительной глубины сцены; языки: n/a.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.3 GB`
- Disk: `310 MB`
- VRAM: `700 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `n/a`
- Алиасы: `depth-anything-v2-small`, `depth-anything-small`

### 8. DPT hybrid MiDaS

- Индекс: `xlocllm.unit("depth-estimation", "Xenova/dpt-hybrid-midas")`
- Model ID: `Xenova/dpt-hybrid-midas`
- Для чего подходит: medium transformers модель для: карты глубины и оценка относительной глубины сцены; языки: n/a.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `Xenova`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.47 GB`
- Disk: `480 MB`
- VRAM: `950 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `n/a`
- Алиасы: `dpt-hybrid-midas`, `midas`

## vlm - VLM/image-to-text

Назначение: image captioning и image-to-text задачи.
Catalog task: `image-to-text`.
Invoke endpoint: `image-to-text`.

### 1. SmolVLM 256M Instruct

- Индекс: `xlocllm.unit("vlm", "HuggingFaceTB/SmolVLM-256M-Instruct")`
- Model ID: `HuggingFaceTB/SmolVLM-256M-Instruct`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: image captioning и image-to-text задачи.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `HuggingFaceTB`
- Hardware tier: `tiny`
- Parameters: `0.256B`
- Model size: `0.24 GB`
- Disk: `243 MB`
- VRAM: `291 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `HuggingFaceTB/SmolVLM-256M-Instruct`, `SmolVLM 256M Instruct`, `SmolVLM-256M-Instruct`
- Теги: `VLM`, `arxiv:2504.05299`, `base_model:HuggingFaceTB/SmolLM2-135M-Instruct`, `base_model:quantized:HuggingFaceTB/SmolLM2-135M-Instruct`, `conversational`, `dataset:HuggingFaceM4/Docmatix`, `dataset:HuggingFaceM4/the_cauldron`, `en`, `idefics3`, `image-text-to-text`, `onnx`, `safetensors`, `transformers`

### 2. Florence 2 base

- Индекс: `xlocllm.unit("vlm", "onnx-community/Florence-2-base")`
- Model ID: `onnx-community/Florence-2-base`
- Для чего подходит: known browser-ready provider Подходит для: image captioning и image-to-text задачи.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.63 GB`
- Disk: `650 MB`
- VRAM: `780 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `en`
- Алиасы: `Florence 2 base`, `Florence-2-base`, `onnx-community/Florence-2-base`
- Теги: `VLM`, `base_model:microsoft/Florence-2-base`, `base_model:quantized:microsoft/Florence-2-base`, `florence2`, `image-text-to-text`, `image-to-text`, `license:mit`, `onnx`, `region:us`, `text-generation`, `text2text-generation`, `transformers.js`, `vision`

### 3. Florence 2 large

- Индекс: `xlocllm.unit("vlm", "onnx-community/Florence-2-large")`
- Model ID: `onnx-community/Florence-2-large`
- Для чего подходит: known browser-ready provider Подходит для: image captioning и image-to-text задачи.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.63 GB`
- Disk: `650 MB`
- VRAM: `780 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `en`
- Алиасы: `Florence 2 large`, `Florence-2-large`, `onnx-community/Florence-2-large`
- Теги: `VLM`, `base_model:microsoft/Florence-2-large`, `base_model:quantized:microsoft/Florence-2-large`, `florence2`, `image-text-to-text`, `image-to-text`, `license:mit`, `onnx`, `region:us`, `text-generation`, `text2text-generation`, `transformers.js`, `vision`

### 4. Florence 2 large ft

- Индекс: `xlocllm.unit("vlm", "onnx-community/Florence-2-large-ft")`
- Model ID: `onnx-community/Florence-2-large-ft`
- Для чего подходит: known browser-ready provider Подходит для: image captioning и image-to-text задачи.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.63 GB`
- Disk: `650 MB`
- VRAM: `780 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `en`
- Алиасы: `Florence 2 large ft`, `Florence-2-large-ft`, `onnx-community/Florence-2-large-ft`
- Теги: `VLM`, `base_model:microsoft/Florence-2-large-ft`, `base_model:quantized:microsoft/Florence-2-large-ft`, `florence2`, `image-text-to-text`, `image-to-text`, `license:mit`, `onnx`, `region:us`, `text-generation`, `text2text-generation`, `transformers.js`, `vision`

### 5. ViT GPT-2 image captioning

- Индекс: `xlocllm.unit("vlm", "Xenova/vit-gpt2-image-captioning")`
- Model ID: `Xenova/vit-gpt2-image-captioning`
- Для чего подходит: small transformers модель для: image captioning и image-to-text задачи; языки: en.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.45 GB`
- Disk: `460 MB`
- VRAM: `950 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `vit-gpt2-captioning`, `image-captioning`

### 6. FastVLM 0.5B

- Индекс: `xlocllm.unit("vlm", "onnx-community/FastVLM-0.5B-ONNX")`
- Model ID: `onnx-community/FastVLM-0.5B-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: image captioning и image-to-text задачи.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.5B`
- Model size: `0.46 GB`
- Disk: `475 MB`
- VRAM: `570 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apple-amlr`
- Languages: `en`
- Алиасы: `FastVLM 0.5B`, `FastVLM-0.5B`, `FastVLM-0.5B-ONNX`, `onnx-community/FastVLM-0.5B-ONNX`
- Теги: `VLM`, `arxiv:2412.13303`, `base_model:apple/FastVLM-0.5B`, `base_model:quantized:apple/FastVLM-0.5B`, `conversational`, `fastvlm`, `image-text-to-text`, `license:apple-amlr`, `llava_qwen2`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 7. Florence 2 base finetuned

- Индекс: `xlocllm.unit("vlm", "onnx-community/Florence-2-base-ft")`
- Model ID: `onnx-community/Florence-2-base-ft`
- Для чего подходит: medium transformers модель для: image captioning и image-to-text задачи; языки: en.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.76 GB`
- Disk: `780 MB`
- VRAM: `1500 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `en`
- Алиасы: `florence-2-base-ft`, `florence-base`

### 8. Qwen2 VL 2B Instruct

- Индекс: `xlocllm.unit("vlm", "onnx-community/Qwen2-VL-2B-Instruct")`
- Model ID: `onnx-community/Qwen2-VL-2B-Instruct`
- Для чего подходит: known browser-ready provider Подходит для: image captioning и image-to-text задачи.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `2.0B`
- Model size: `1.86 GB`
- Disk: `1900 MB`
- VRAM: `2280 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `Qwen2 VL 2B Instruct`, `Qwen2-VL-2B-Instruct`, `onnx-community/Qwen2-VL-2B-Instruct`
- Теги: `VLM`, `base_model:Qwen/Qwen2-VL-2B-Instruct`, `base_model:quantized:Qwen/Qwen2-VL-2B-Instruct`, `conversational`, `image-text-to-text`, `license:apache-2.0`, `onnx`, `qwen2_vl`, `region:us`, `transformers.js`

## asr - ASR

Назначение: speech-to-text транскрибация.
Catalog task: `automatic-speech-recognition`.
Invoke endpoint: `asr`.

### 1. Whisper tiny multilingual

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-tiny")`
- Model ID: `Xenova/whisper-tiny`
- Для чего подходит: tiny transformers модель для: speech-to-text транскрибация; языки: multilingual.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.08 GB`
- Disk: `80 MB`
- VRAM: `250 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `multilingual`
- Алиасы: `whisper-tiny`

### 2. whisper base

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-base")`
- Model ID: `Xenova/whisper-base`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `Xenova/whisper-base`, `whisper base`, `whisper-base`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-base`, `base_model:quantized:openai/whisper-base`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 3. whisper base.en

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-base.en")`
- Model ID: `Xenova/whisper-base.en`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `Xenova/whisper-base.en`, `whisper base.en`, `whisper-base.en`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-base.en`, `base_model:quantized:openai/whisper-base.en`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 4. whisper large

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-large")`
- Model ID: `Xenova/whisper-large`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `Xenova/whisper-large`, `whisper large`, `whisper-large`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-large`, `base_model:quantized:openai/whisper-large`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 5. whisper large v2

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-large-v2")`
- Model ID: `Xenova/whisper-large-v2`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/whisper-large-v2`, `whisper large v2`, `whisper-large-v2`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-large-v2`, `base_model:quantized:openai/whisper-large-v2`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 6. whisper large v3

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-large-v3")`
- Model ID: `Xenova/whisper-large-v3`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `Xenova/whisper-large-v3`, `whisper large v3`, `whisper-large-v3`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-large-v3`, `base_model:quantized:openai/whisper-large-v3`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 7. whisper medium

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-medium")`
- Model ID: `Xenova/whisper-medium`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `Xenova/whisper-medium`, `whisper medium`, `whisper-medium`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-medium`, `base_model:quantized:openai/whisper-medium`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 8. whisper medium.en

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-medium.en")`
- Model ID: `Xenova/whisper-medium.en`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `Xenova/whisper-medium.en`, `whisper medium.en`, `whisper-medium.en`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-medium.en`, `base_model:quantized:openai/whisper-medium.en`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 9. whisper small

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-small")`
- Model ID: `Xenova/whisper-small`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `Xenova/whisper-small`, `whisper small`, `whisper-small`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-small`, `base_model:quantized:openai/whisper-small`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 10. whisper small.en

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-small.en")`
- Model ID: `Xenova/whisper-small.en`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `Xenova/whisper-small.en`, `whisper small.en`, `whisper-small.en`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-small.en`, `base_model:quantized:openai/whisper-small.en`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 11. whisper tiny

- Индекс: `xlocllm.unit("asr", "onnx-community/whisper-tiny")`
- Model ID: `onnx-community/whisper-tiny`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `onnx-community/whisper-tiny`, `whisper tiny`, `whisper-tiny`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-tiny`, `base_model:quantized:openai/whisper-tiny`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 12. whisper tiny.en

- Индекс: `xlocllm.unit("asr", "onnx-community/whisper-tiny.en")`
- Model ID: `onnx-community/whisper-tiny.en`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `onnx-community/whisper-tiny.en`, `whisper tiny.en`, `whisper-tiny.en`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-tiny.en`, `base_model:quantized:openai/whisper-tiny.en`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 13. whisper tiny.en

- Индекс: `xlocllm.unit("asr", "Xenova/whisper-tiny.en")`
- Model ID: `Xenova/whisper-tiny.en`
- Для чего подходит: known browser-ready provider Подходит для: speech-to-text транскрибация.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `Xenova/whisper-tiny.en`, `whisper tiny.en`, `whisper-tiny.en`
- Теги: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-tiny.en`, `base_model:quantized:openai/whisper-tiny.en`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 14. Whisper base multilingual

- Индекс: `xlocllm.unit("asr", "onnx-community/whisper-base")`
- Model ID: `onnx-community/whisper-base`
- Для чего подходит: small transformers модель для: speech-to-text транскрибация; языки: multilingual.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.14 GB`
- Disk: `145 MB`
- VRAM: `550 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `multilingual`
- Алиасы: `whisper-base`

### 15. Whisper large v3 turbo

- Индекс: `xlocllm.unit("asr", "onnx-community/whisper-large-v3-turbo")`
- Model ID: `onnx-community/whisper-large-v3-turbo`
- Для чего подходит: large transformers модель для: speech-to-text транскрибация; языки: multilingual.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `onnx-community`
- Hardware tier: `large`
- Parameters: `n/a`
- Model size: `1.56 GB`
- Disk: `1600 MB`
- VRAM: `3600 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `multilingual`
- Алиасы: `whisper-large-v3-turbo`

## zero-shot-image - Zero-shot-image

Назначение: zero-shot классификация изображений по пользовательским labels.
Catalog task: `zero-shot-image-classification`.
Invoke endpoint: `zero-shot-image`.

### 1. CLIP ViT base patch32

- Индекс: `xlocllm.unit("zero-shot-image", "Xenova/clip-vit-base-patch32")`
- Model ID: `Xenova/clip-vit-base-patch32`
- Для чего подходит: small transformers модель для: zero-shot классификация изображений по пользовательским labels; языки: en.
- Runtime: `transformers`
- Task: `zero-shot-image-classification`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.33 GB`
- Disk: `340 MB`
- VRAM: `750 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `en`
- Алиасы: `clip-vit-base-patch32`, `clip-base`

### 2. SigLIP base 224

- Индекс: `xlocllm.unit("zero-shot-image", "Xenova/siglip-base-patch16-224")`
- Model ID: `Xenova/siglip-base-patch16-224`
- Для чего подходит: medium transformers модель для: zero-shot классификация изображений по пользовательским labels; языки: en.
- Runtime: `transformers`
- Task: `zero-shot-image-classification`
- Provider: `Xenova`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.51 GB`
- Disk: `520 MB`
- VRAM: `1100 MB`
- DType: `q8`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `siglip-base-224`, `siglip`

## language-id - Language identification

Назначение: определение языка речи по аудио.
Catalog task: `audio-classification`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. mms lid 126

- Индекс: `xlocllm.unit("language-id", "Xenova/mms-lid-126")`
- Model ID: `Xenova/mms-lid-126`
- Для чего подходит: known browser-ready provider Подходит для: определение языка речи по аудио.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/mms-lid-126`, `mms lid 126`, `mms-lid-126`
- Теги: `Audio`, `Language ID`, `audio-classification`, `base_model:facebook/mms-lid-126`, `base_model:quantized:facebook/mms-lid-126`, `mms`, `onnx`, `region:us`, `transformers.js`, `wav2vec2`

### 2. mms lid 256

- Индекс: `xlocllm.unit("language-id", "Xenova/mms-lid-256")`
- Model ID: `Xenova/mms-lid-256`
- Для чего подходит: known browser-ready provider Подходит для: определение языка речи по аудио.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/mms-lid-256`, `mms lid 256`, `mms-lid-256`
- Теги: `Audio`, `Language ID`, `audio-classification`, `base_model:facebook/mms-lid-256`, `base_model:quantized:facebook/mms-lid-256`, `mms`, `onnx`, `region:us`, `transformers.js`, `wav2vec2`

### 3. mms lid 4017

- Индекс: `xlocllm.unit("language-id", "Xenova/mms-lid-4017")`
- Model ID: `Xenova/mms-lid-4017`
- Для чего подходит: known browser-ready provider Подходит для: определение языка речи по аудио.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/mms-lid-4017`, `mms lid 4017`, `mms-lid-4017`
- Теги: `Audio`, `Language ID`, `audio-classification`, `base_model:facebook/mms-lid-4017`, `base_model:quantized:facebook/mms-lid-4017`, `mms`, `onnx`, `region:us`, `transformers.js`, `wav2vec2`

## audio-classification - Audio classification

Назначение: классификация аудио и звуковые теги.
Catalog task: `audio-classification`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. ast finetuned audioset 10 10 0.4593

- Индекс: `xlocllm.unit("audio-classification", "Xenova/ast-finetuned-audioset-10-10-0.4593")`
- Model ID: `Xenova/ast-finetuned-audioset-10-10-0.4593`
- Для чего подходит: known browser-ready provider Подходит для: классификация аудио и звуковые теги.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/ast-finetuned-audioset-10-10-0.4593`, `ast finetuned audioset 10 10 0.4593`, `ast-finetuned-audioset-10-10-0.4593`
- Теги: `Audio`, `Audio Classification`, `audio-classification`, `audio-spectrogram-transformer`, `base_model:MIT/ast-finetuned-audioset-10-10-0.4593`, `base_model:quantized:MIT/ast-finetuned-audioset-10-10-0.4593`, `onnx`, `region:us`, `transformers.js`

### 2. clap htsat unfused

- Индекс: `xlocllm.unit("audio-classification", "Xenova/clap-htsat-unfused")`
- Model ID: `Xenova/clap-htsat-unfused`
- Для чего подходит: known browser-ready provider Подходит для: классификация аудио и звуковые теги.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/clap-htsat-unfused`, `clap htsat unfused`, `clap-htsat-unfused`
- Теги: `Audio`, `Audio Classification`, `base_model:laion/clap-htsat-unfused`, `base_model:quantized:laion/clap-htsat-unfused`, `clap`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`, `zero-shot-audio-classification`

### 3. wav2vec2 large xlsr 53 gender recognition librispeech

- Индекс: `xlocllm.unit("audio-classification", "Xenova/wav2vec2-large-xlsr-53-gender-recognition-librispeech")`
- Model ID: `Xenova/wav2vec2-large-xlsr-53-gender-recognition-librispeech`
- Для чего подходит: known browser-ready provider Подходит для: классификация аудио и звуковые теги.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/wav2vec2-large-xlsr-53-gender-recognition-librispeech`, `wav2vec2 large xlsr 53 gender recognition librispeech`, `wav2vec2-large-xlsr-53-gender-recognition-librispeech`
- Теги: `Audio`, `Audio Classification`, `audio-classification`, `base_model:alefiury/wav2vec2-large-xlsr-53-gender-recognition-librispeech`, `base_model:quantized:alefiury/wav2vec2-large-xlsr-53-gender-recognition-librispeech`, `onnx`, `region:us`, `transformers.js`, `wav2vec2`

## ocr - OCR/text recognition

Назначение: OCR и распознавание текста на изображениях.
Catalog task: `image-to-text`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. manga ocr base

- Индекс: `xlocllm.unit("ocr", "onnx-community/manga-ocr-base-ONNX")`
- Model ID: `onnx-community/manga-ocr-base-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: OCR и распознавание текста на изображениях.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `manga ocr base`, `manga-ocr-base`, `manga-ocr-base-ONNX`, `onnx-community/manga-ocr-base-ONNX`
- Теги: `OCR`, `base_model:kha-white/manga-ocr-base`, `base_model:quantized:kha-white/manga-ocr-base`, `dataset:manga109s`, `image-text-to-text`, `image-to-text`, `ja`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `vision-encoder-decoder`

### 2. mgp str base

- Индекс: `xlocllm.unit("ocr", "onnx-community/mgp-str-base")`
- Model ID: `onnx-community/mgp-str-base`
- Для чего подходит: known browser-ready provider Подходит для: OCR и распознавание текста на изображениях.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `mgp str base`, `mgp-str-base`, `onnx-community/mgp-str-base`
- Теги: `OCR`, `base_model:alibaba-damo/mgp-str-base`, `base_model:quantized:alibaba-damo/mgp-str-base`, `image-to-text`, `mgp-str`, `ocr`, `onnx`, `region:us`, `transformers.js`

### 3. TexTeller

- Индекс: `xlocllm.unit("ocr", "onnx-community/TexTeller-ONNX")`
- Model ID: `onnx-community/TexTeller-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: OCR и распознавание текста на изображениях.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `TexTeller`, `TexTeller-ONNX`, `onnx-community/TexTeller-ONNX`
- Теги: `OCR`, `base_model:OleehyO/TexTeller`, `base_model:quantized:OleehyO/TexTeller`, `dataset:OleehyO/latex-formulas`, `image to latex`, `image-text-to-text`, `image-to-text`, `license:apache-2.0`, `ocr`, `onnx`, `region:us`, `transformers.js`, `vision-encoder-decoder`

### 4. trocr base stage1

- Индекс: `xlocllm.unit("ocr", "onnx-community/trocr-base-stage1-ONNX")`
- Model ID: `onnx-community/trocr-base-stage1-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: OCR и распознавание текста на изображениях.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `onnx-community/trocr-base-stage1-ONNX`, `trocr base stage1`, `trocr-base-stage1`, `trocr-base-stage1-ONNX`
- Теги: `OCR`, `base_model:microsoft/trocr-base-stage1`, `base_model:quantized:microsoft/trocr-base-stage1`, `image-text-to-text`, `onnx`, `region:us`, `transformers.js`, `vision-encoder-decoder`

## document-layout - Document layout

Назначение: анализ layout документов и детекция элементов страницы.
Catalog task: `object-detection`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. yolov10b doclaynet

- Индекс: `xlocllm.unit("document-layout", "Oblix/yolov10b-doclaynet_ONNX_document-layout-analysis")`
- Model ID: `Oblix/yolov10b-doclaynet_ONNX_document-layout-analysis`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: анализ layout документов и детекция элементов страницы.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Oblix`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Oblix/yolov10b-doclaynet_ONNX_document-layout-analysis`, `yolov10b doclaynet`, `yolov10b-doclaynet`, `yolov10b-doclaynet_ONNX_document-layout-analysis`
- Теги: `Document Layout`, `OCR`, `object-detection`, `onnx`, `region:us`, `transformers.js`, `yolov10`

## table-detection - Table detection/structure

Назначение: детекция таблиц и распознавание структуры таблиц.
Catalog task: `object-detection`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. table transformer detection

- Индекс: `xlocllm.unit("table-detection", "Xenova/table-transformer-detection")`
- Model ID: `Xenova/table-transformer-detection`
- Для чего подходит: known browser-ready provider Подходит для: детекция таблиц и распознавание структуры таблиц.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/table-transformer-detection`, `table transformer detection`, `table-transformer-detection`
- Теги: `OCR`, `Table`, `base_model:microsoft/table-transformer-detection`, `base_model:quantized:microsoft/table-transformer-detection`, `object-detection`, `onnx`, `region:us`, `table-transformer`, `transformers.js`

### 2. table transformer structure recognition v1.1 all

- Индекс: `xlocllm.unit("table-detection", "Xenova/table-transformer-structure-recognition-v1.1-all")`
- Model ID: `Xenova/table-transformer-structure-recognition-v1.1-all`
- Для чего подходит: known browser-ready provider Подходит для: детекция таблиц и распознавание структуры таблиц.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/table-transformer-structure-recognition-v1.1-all`, `table transformer structure recognition v1.1 all`, `table-transformer-structure-recognition-v1.1-all`
- Теги: `OCR`, `Table`, `base_model:microsoft/table-transformer-structure-recognition-v1.1-all`, `base_model:quantized:microsoft/table-transformer-structure-recognition-v1.1-all`, `object-detection`, `onnx`, `region:us`, `table-transformer`, `transformers.js`

## document-qa - Document QA

Назначение: document question answering и извлечение данных из документов.
Catalog task: `document-question-answering`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. donut base finetuned cord v2

- Индекс: `xlocllm.unit("document-qa", "Xenova/donut-base-finetuned-cord-v2")`
- Model ID: `Xenova/donut-base-finetuned-cord-v2`
- Для чего подходит: known browser-ready provider Подходит для: document question answering и извлечение данных из документов.
- Runtime: `transformers`
- Task: `document-question-answering`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/donut-base-finetuned-cord-v2`, `donut base finetuned cord v2`, `donut-base-finetuned-cord-v2`
- Теги: `Document QA`, `OCR`, `base_model:naver-clova-ix/donut-base-finetuned-cord-v2`, `base_model:quantized:naver-clova-ix/donut-base-finetuned-cord-v2`, `donut`, `donut-swin`, `image-text-to-text`, `image-to-text`, `onnx`, `region:us`, `transformers.js`, `vision`, `vision-encoder-decoder`

### 2. donut base finetuned docvqa

- Индекс: `xlocllm.unit("document-qa", "Xenova/donut-base-finetuned-docvqa")`
- Model ID: `Xenova/donut-base-finetuned-docvqa`
- Для чего подходит: known browser-ready provider Подходит для: document question answering и извлечение данных из документов.
- Runtime: `transformers`
- Task: `document-question-answering`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `Xenova/donut-base-finetuned-docvqa`, `donut base finetuned docvqa`, `donut-base-finetuned-docvqa`
- Теги: `Document QA`, `OCR`, `base_model:naver-clova-ix/donut-base-finetuned-docvqa`, `base_model:quantized:naver-clova-ix/donut-base-finetuned-docvqa`, `document-question-answering`, `donut`, `donut-swin`, `image-text-to-text`, `image-to-text`, `onnx`, `region:us`, `transformers.js`, `vision`, `vision-encoder-decoder`

## text-classification - Text classification

Назначение: sentiment, toxicity и общая классификация текста.
Catalog task: `text-classification`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. bert base multilingual uncased sentiment

- Индекс: `xlocllm.unit("text-classification", "Xenova/bert-base-multilingual-uncased-sentiment")`
- Model ID: `Xenova/bert-base-multilingual-uncased-sentiment`
- Для чего подходит: known browser-ready provider Подходит для: sentiment, toxicity и общая классификация текста.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/bert-base-multilingual-uncased-sentiment`, `bert base multilingual uncased sentiment`, `bert-base-multilingual-uncased-sentiment`
- Теги: `Text`, `Text Classification`, `base_model:nlptown/bert-base-multilingual-uncased-sentiment`, `base_model:quantized:nlptown/bert-base-multilingual-uncased-sentiment`, `bert`, `onnx`, `region:us`, `text-classification`, `transformers.js`

### 2. distilbert base multilingual cased sentiments student

- Индекс: `xlocllm.unit("text-classification", "Xenova/distilbert-base-multilingual-cased-sentiments-student")`
- Model ID: `Xenova/distilbert-base-multilingual-cased-sentiments-student`
- Для чего подходит: known browser-ready provider Подходит для: sentiment, toxicity и общая классификация текста.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/distilbert-base-multilingual-cased-sentiments-student`, `distilbert base multilingual cased sentiments student`, `distilbert-base-multilingual-cased-sentiments-student`
- Теги: `Text`, `Text Classification`, `base_model:lxyuan/distilbert-base-multilingual-cased-sentiments-student`, `base_model:quantized:lxyuan/distilbert-base-multilingual-cased-sentiments-student`, `distilbert`, `onnx`, `region:us`, `text-classification`, `transformers.js`

### 3. distilbert base uncased finetuned sst 2 english

- Индекс: `xlocllm.unit("text-classification", "Xenova/distilbert-base-uncased-finetuned-sst-2-english")`
- Model ID: `Xenova/distilbert-base-uncased-finetuned-sst-2-english`
- Для чего подходит: known browser-ready provider Подходит для: sentiment, toxicity и общая классификация текста.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/distilbert-base-uncased-finetuned-sst-2-english`, `distilbert base uncased finetuned sst 2 english`, `distilbert-base-uncased-finetuned-sst-2-english`
- Теги: `Text`, `Text Classification`, `base_model:distilbert/distilbert-base-uncased-finetuned-sst-2-english`, `base_model:quantized:distilbert/distilbert-base-uncased-finetuned-sst-2-english`, `distilbert`, `onnx`, `region:us`, `text-classification`, `transformers.js`

### 4. toxic bert

- Индекс: `xlocllm.unit("text-classification", "Xenova/toxic-bert")`
- Model ID: `Xenova/toxic-bert`
- Для чего подходит: known browser-ready provider Подходит для: sentiment, toxicity и общая классификация текста.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/toxic-bert`, `toxic bert`, `toxic-bert`
- Теги: `Text`, `Text Classification`, `base_model:quantized:unitary/toxic-bert`, `base_model:unitary/toxic-bert`, `bert`, `onnx`, `region:us`, `text-classification`, `transformers.js`

## ner - NER/entity extraction

Назначение: named entity recognition и token classification.
Catalog task: `token-classification`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. bert base multilingual cased ner hrl

- Индекс: `xlocllm.unit("ner", "Xenova/bert-base-multilingual-cased-ner-hrl")`
- Model ID: `Xenova/bert-base-multilingual-cased-ner-hrl`
- Для чего подходит: known browser-ready provider Подходит для: named entity recognition и token classification.
- Runtime: `transformers`
- Task: `token-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `multilingual`
- Алиасы: `Xenova/bert-base-multilingual-cased-ner-hrl`, `bert base multilingual cased ner hrl`, `bert-base-multilingual-cased-ner-hrl`
- Теги: `NER`, `Text`, `base_model:Davlan/bert-base-multilingual-cased-ner-hrl`, `base_model:quantized:Davlan/bert-base-multilingual-cased-ner-hrl`, `bert`, `onnx`, `region:us`, `token-classification`, `transformers.js`

### 2. bert base NER

- Индекс: `xlocllm.unit("ner", "Xenova/bert-base-NER")`
- Model ID: `Xenova/bert-base-NER`
- Для чего подходит: known browser-ready provider Подходит для: named entity recognition и token classification.
- Runtime: `transformers`
- Task: `token-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/bert-base-NER`, `bert base NER`, `bert-base-NER`
- Теги: `NER`, `Text`, `base_model:dslim/bert-base-NER`, `base_model:quantized:dslim/bert-base-NER`, `bert`, `onnx`, `region:us`, `token-classification`, `transformers.js`

### 3. bert base NER uncased

- Индекс: `xlocllm.unit("ner", "Xenova/bert-base-NER-uncased")`
- Model ID: `Xenova/bert-base-NER-uncased`
- Для чего подходит: known browser-ready provider Подходит для: named entity recognition и token classification.
- Runtime: `transformers`
- Task: `token-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/bert-base-NER-uncased`, `bert base NER uncased`, `bert-base-NER-uncased`
- Теги: `NER`, `Text`, `base_model:dslim/bert-base-NER-uncased`, `base_model:quantized:dslim/bert-base-NER-uncased`, `bert`, `onnx`, `region:us`, `token-classification`, `transformers.js`

## zero-shot-text - Zero-shot text

Назначение: zero-shot классификация текста с пользовательскими candidate labels.
Catalog task: `zero-shot-classification`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. bart large mnli

- Индекс: `xlocllm.unit("zero-shot-text", "Xenova/bart-large-mnli")`
- Model ID: `Xenova/bart-large-mnli`
- Для чего подходит: known browser-ready provider Подходит для: zero-shot классификация текста с пользовательскими candidate labels.
- Runtime: `transformers`
- Task: `zero-shot-classification`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.32 GB`
- Disk: `330 MB`
- VRAM: `396 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/bart-large-mnli`, `bart large mnli`, `bart-large-mnli`
- Теги: `Text`, `Zero-shot Text`, `bart`, `base_model:facebook/bart-large-mnli`, `base_model:quantized:facebook/bart-large-mnli`, `onnx`, `region:us`, `text-classification`, `transformers.js`, `zero-shot-classification`

### 2. mobilebert uncased mnli

- Индекс: `xlocllm.unit("zero-shot-text", "Xenova/mobilebert-uncased-mnli")`
- Model ID: `Xenova/mobilebert-uncased-mnli`
- Для чего подходит: known browser-ready provider Подходит для: zero-shot классификация текста с пользовательскими candidate labels.
- Runtime: `transformers`
- Task: `zero-shot-classification`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.32 GB`
- Disk: `330 MB`
- VRAM: `396 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/mobilebert-uncased-mnli`, `mobilebert uncased mnli`, `mobilebert-uncased-mnli`
- Теги: `Text`, `Zero-shot Text`, `base_model:quantized:typeform/mobilebert-uncased-mnli`, `base_model:typeform/mobilebert-uncased-mnli`, `mobilebert`, `onnx`, `region:us`, `text-classification`, `transformers.js`, `zero-shot-classification`

## summarization - Summarization

Назначение: суммаризация текста.
Catalog task: `summarization`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. bart large cnn

- Индекс: `xlocllm.unit("summarization", "Xenova/bart-large-cnn")`
- Model ID: `Xenova/bart-large-cnn`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/bart-large-cnn`, `bart large cnn`, `bart-large-cnn`
- Теги: `Summarization`, `Text`, `bart`, `base_model:facebook/bart-large-cnn`, `base_model:quantized:facebook/bart-large-cnn`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 2. Bart Large CNN

- Индекс: `xlocllm.unit("summarization", "c2p-cmd/Bart-Large-CNN-Onnx")`
- Model ID: `c2p-cmd/Bart-Large-CNN-Onnx`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `c2p-cmd`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Bart Large CNN`, `Bart-Large-CNN`, `Bart-Large-CNN-Onnx`, `c2p-cmd/Bart-Large-CNN-Onnx`
- Теги: `Summarization`, `Text`, `bart`, `base_model:facebook/bart-large-cnn`, `base_model:quantized:facebook/bart-large-cnn`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 3. bart large cnn

- Индекс: `xlocllm.unit("summarization", "omoral02/bart-large-cnn-ONNX")`
- Model ID: `omoral02/bart-large-cnn-ONNX`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `omoral02`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `mit`
- Languages: `en`
- Алиасы: `bart large cnn`, `bart-large-cnn`, `bart-large-cnn-ONNX`, `omoral02/bart-large-cnn-ONNX`
- Теги: `Summarization`, `Text`, `arxiv:1910.13461`, `bart`, `base_model:facebook/bart-large-cnn`, `base_model:quantized:facebook/bart-large-cnn`, `dataset:cnn_dailymail`, `en`, `license:mit`, `model-index`, `onnx`, `summarization`, `text2text-generation`, `transformers.js`

### 4. bart large xsum

- Индекс: `xlocllm.unit("summarization", "Xenova/bart-large-xsum")`
- Model ID: `Xenova/bart-large-xsum`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/bart-large-xsum`, `bart large xsum`, `bart-large-xsum`
- Теги: `Summarization`, `Text`, `bart`, `base_model:facebook/bart-large-xsum`, `base_model:quantized:facebook/bart-large-xsum`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 5. distilbart cnn 12 3

- Индекс: `xlocllm.unit("summarization", "Xenova/distilbart-cnn-12-3")`
- Model ID: `Xenova/distilbart-cnn-12-3`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/distilbart-cnn-12-3`, `distilbart cnn 12 3`, `distilbart-cnn-12-3`
- Теги: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-cnn-12-3`, `base_model:sshleifer/distilbart-cnn-12-3`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 6. distilbart cnn 12 6

- Индекс: `xlocllm.unit("summarization", "Xenova/distilbart-cnn-12-6")`
- Model ID: `Xenova/distilbart-cnn-12-6`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/distilbart-cnn-12-6`, `distilbart cnn 12 6`, `distilbart-cnn-12-6`
- Теги: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-cnn-12-6`, `base_model:sshleifer/distilbart-cnn-12-6`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 7. distilbart cnn 12 6

- Индекс: `xlocllm.unit("summarization", "Mozilla/distilbart-cnn-12-6")`
- Model ID: `Mozilla/distilbart-cnn-12-6`
- Для чего подходит: ONNX/WebGPU artifact marker Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Mozilla`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Mozilla/distilbart-cnn-12-6`, `distilbart cnn 12 6`, `distilbart-cnn-12-6`
- Теги: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-cnn-12-6`, `base_model:sshleifer/distilbart-cnn-12-6`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 8. distilbart cnn 6 6

- Индекс: `xlocllm.unit("summarization", "Xenova/distilbart-cnn-6-6")`
- Model ID: `Xenova/distilbart-cnn-6-6`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `Xenova/distilbart-cnn-6-6`, `distilbart cnn 6 6`, `distilbart-cnn-6-6`
- Теги: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-cnn-6-6`, `base_model:sshleifer/distilbart-cnn-6-6`, `license:apache-2.0`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 9. distilbart xsum 12 1

- Индекс: `xlocllm.unit("summarization", "Xenova/distilbart-xsum-12-1")`
- Model ID: `Xenova/distilbart-xsum-12-1`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/distilbart-xsum-12-1`, `distilbart xsum 12 1`, `distilbart-xsum-12-1`
- Теги: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-xsum-12-1`, `base_model:sshleifer/distilbart-xsum-12-1`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 10. distilbart xsum 12 3

- Индекс: `xlocllm.unit("summarization", "Xenova/distilbart-xsum-12-3")`
- Model ID: `Xenova/distilbart-xsum-12-3`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/distilbart-xsum-12-3`, `distilbart xsum 12 3`, `distilbart-xsum-12-3`
- Теги: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-xsum-12-3`, `base_model:sshleifer/distilbart-xsum-12-3`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 11. distilbart xsum 12 6

- Индекс: `xlocllm.unit("summarization", "Xenova/distilbart-xsum-12-6")`
- Model ID: `Xenova/distilbart-xsum-12-6`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/distilbart-xsum-12-6`, `distilbart xsum 12 6`, `distilbart-xsum-12-6`
- Теги: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-xsum-12-6`, `base_model:sshleifer/distilbart-xsum-12-6`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 12. distilbart xsum 6 6

- Индекс: `xlocllm.unit("summarization", "Xenova/distilbart-xsum-6-6")`
- Model ID: `Xenova/distilbart-xsum-6-6`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/distilbart-xsum-6-6`, `distilbart xsum 6 6`, `distilbart-xsum-6-6`
- Теги: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-xsum-6-6`, `base_model:sshleifer/distilbart-xsum-6-6`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 13. distilbart xsum 9 6

- Индекс: `xlocllm.unit("summarization", "Xenova/distilbart-xsum-9-6")`
- Model ID: `Xenova/distilbart-xsum-9-6`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/distilbart-xsum-9-6`, `distilbart xsum 9 6`, `distilbart-xsum-9-6`
- Теги: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-xsum-9-6`, `base_model:sshleifer/distilbart-xsum-9-6`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 14. rut5 base sum gazeta

- Индекс: `xlocllm.unit("summarization", "onnx-community/rut5_base_sum_gazeta-ONNX")`
- Model ID: `onnx-community/rut5_base_sum_gazeta-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `['apache-2.0']`
- Languages: `ru`
- Алиасы: `onnx-community/rut5_base_sum_gazeta-ONNX`, `rut5-base-sum-gazeta`, `rut5_base_sum_gazeta`, `rut5_base_sum_gazeta-ONNX`
- Теги: `Summarization`, `Text`, `base_model:IlyaGusev/rut5_base_sum_gazeta`, `base_model:quantized:IlyaGusev/rut5_base_sum_gazeta`, `dataset:IlyaGusev/gazeta`, `license:apache-2.0`, `onnx`, `region:us`, `ru`, `summarization`, `t5`, `text2text-generation`, `transformers.js`

### 15. text summarization

- Индекс: `xlocllm.unit("summarization", "onnx-community/text_summarization-ONNX")`
- Model ID: `onnx-community/text_summarization-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: суммаризация текста.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `onnx-community/text_summarization-ONNX`, `text-summarization`, `text_summarization`, `text_summarization-ONNX`
- Теги: `Summarization`, `Text`, `base_model:Falconsai/text_summarization`, `base_model:quantized:Falconsai/text_summarization`, `en`, `license:apache-2.0`, `onnx`, `region:us`, `summarization`, `t5`, `text2text-generation`, `transformers.js`

## text2text - Text2Text utilities

Назначение: универсальные text-to-text generation задачи.
Catalog task: `text2text-generation`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. flan t5 small

- Индекс: `xlocllm.unit("text2text", "Xenova/flan-t5-small")`
- Model ID: `Xenova/flan-t5-small`
- Для чего подходит: known browser-ready provider Подходит для: универсальные text-to-text generation задачи.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `en`
- Алиасы: `Xenova/flan-t5-small`, `flan t5 small`, `flan-t5-small`
- Теги: `Text`, `Text2Text`, `dataset:djaym7/wiki_dialog`, `dataset:svakulenk0/qrecc`, `dataset:taskmaster2`, `de`, `en`, `fr`, `multilingual`, `onnx`, `ro`, `t5`, `text2text-generation`, `transformers.js`

### 2. t5 small

- Индекс: `xlocllm.unit("text2text", "Xenova/t5-small")`
- Model ID: `Xenova/t5-small`
- Для чего подходит: known browser-ready provider Подходит для: универсальные text-to-text generation задачи.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `Xenova/t5-small`, `t5 small`, `t5-small`
- Теги: `Text`, `Text2Text`, `base_model:google-t5/t5-small`, `base_model:quantized:google-t5/t5-small`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 3. LaMini T5 61M

- Индекс: `xlocllm.unit("text2text", "Xenova/LaMini-T5-61M")`
- Model ID: `Xenova/LaMini-T5-61M`
- Для чего подходит: known browser-ready provider Подходит для: универсальные text-to-text generation задачи.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `0.061B`
- Model size: `0.06 GB`
- Disk: `57 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `LaMini T5 61M`, `LaMini-T5-61M`, `Xenova/LaMini-T5-61M`
- Теги: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-T5-61M`, `base_model:quantized:MBZUAI/LaMini-T5-61M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 4. LaMini Flan T5 77M

- Индекс: `xlocllm.unit("text2text", "Xenova/LaMini-Flan-T5-77M")`
- Model ID: `Xenova/LaMini-Flan-T5-77M`
- Для чего подходит: known browser-ready provider Подходит для: универсальные text-to-text generation задачи.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `0.077B`
- Model size: `0.07 GB`
- Disk: `73 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `LaMini Flan T5 77M`, `LaMini-Flan-T5-77M`, `Xenova/LaMini-Flan-T5-77M`
- Теги: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-Flan-T5-77M`, `base_model:quantized:MBZUAI/LaMini-Flan-T5-77M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 5. LaMini T5 223M

- Индекс: `xlocllm.unit("text2text", "Xenova/LaMini-T5-223M")`
- Model ID: `Xenova/LaMini-T5-223M`
- Для чего подходит: known browser-ready provider Подходит для: универсальные text-to-text generation задачи.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `0.223B`
- Model size: `0.21 GB`
- Disk: `211 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `LaMini T5 223M`, `LaMini-T5-223M`, `Xenova/LaMini-T5-223M`
- Теги: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-T5-223M`, `base_model:quantized:MBZUAI/LaMini-T5-223M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 6. LaMini Flan T5 248M

- Индекс: `xlocllm.unit("text2text", "Xenova/LaMini-Flan-T5-248M")`
- Model ID: `Xenova/LaMini-Flan-T5-248M`
- Для чего подходит: known browser-ready provider Подходит для: универсальные text-to-text generation задачи.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `0.248B`
- Model size: `0.23 GB`
- Disk: `235 MB`
- VRAM: `282 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `LaMini Flan T5 248M`, `LaMini-Flan-T5-248M`, `Xenova/LaMini-Flan-T5-248M`
- Теги: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-Flan-T5-248M`, `base_model:quantized:MBZUAI/LaMini-Flan-T5-248M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 7. LaMini T5 738M

- Индекс: `xlocllm.unit("text2text", "Xenova/LaMini-T5-738M")`
- Model ID: `Xenova/LaMini-T5-738M`
- Для чего подходит: known browser-ready provider Подходит для: универсальные text-to-text generation задачи.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `0.738B`
- Model size: `0.68 GB`
- Disk: `701 MB`
- VRAM: `841 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `LaMini T5 738M`, `LaMini-T5-738M`, `Xenova/LaMini-T5-738M`
- Теги: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-T5-738M`, `base_model:quantized:MBZUAI/LaMini-T5-738M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 8. LaMini Flan T5 783M

- Индекс: `xlocllm.unit("text2text", "Xenova/LaMini-Flan-T5-783M")`
- Model ID: `Xenova/LaMini-Flan-T5-783M`
- Для чего подходит: known browser-ready provider Подходит для: универсальные text-to-text generation задачи.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `0.783B`
- Model size: `0.73 GB`
- Disk: `743 MB`
- VRAM: `891 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `en`
- Алиасы: `LaMini Flan T5 783M`, `LaMini-Flan-T5-783M`, `Xenova/LaMini-Flan-T5-783M`
- Теги: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-Flan-T5-783M`, `base_model:quantized:MBZUAI/LaMini-Flan-T5-783M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

## code - Code understanding

Назначение: code embeddings, определение языка кода и code understanding.
Catalog task: `feature-extraction`.
Invoke endpoint: прямой endpoint пока не реализован в Python/browser bridge routing.

### 1. codebert base

- Индекс: `xlocllm.unit("code", "onnx-community/codebert-base-ONNX")`
- Model ID: `onnx-community/codebert-base-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: code embeddings, определение языка кода и code understanding.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.16 GB`
- Disk: `160 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `codebert base`, `codebert-base`, `codebert-base-ONNX`, `onnx-community/codebert-base-ONNX`
- Теги: `Code`, `arxiv:2002.08155`, `base_model:microsoft/codebert-base`, `base_model:quantized:microsoft/codebert-base`, `feature-extraction`, `onnx`, `region:us`, `roberta`, `transformers.js`

### 2. codebert javascript

- Индекс: `xlocllm.unit("code", "onnx-community/codebert-javascript-ONNX")`
- Model ID: `onnx-community/codebert-javascript-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: code embeddings, определение языка кода и code understanding.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.16 GB`
- Disk: `160 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `codebert javascript`, `codebert-javascript`, `codebert-javascript-ONNX`, `onnx-community/codebert-javascript-ONNX`
- Теги: `Code`, `arxiv:2302.05527`, `base_model:neulab/codebert-javascript`, `base_model:quantized:neulab/codebert-javascript`, `fill-mask`, `onnx`, `region:us`, `roberta`, `transformers.js`

### 3. CodeBERTa language id

- Индекс: `xlocllm.unit("code", "onnx-community/CodeBERTa-language-id-ONNX")`
- Model ID: `onnx-community/CodeBERTa-language-id-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: code embeddings, определение языка кода и code understanding.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.16 GB`
- Disk: `160 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `apache-2.0`
- Languages: `universal`
- Алиасы: `CodeBERTa language id`, `CodeBERTa-language-id`, `CodeBERTa-language-id-ONNX`, `onnx-community/CodeBERTa-language-id-ONNX`
- Теги: `Code`, `arxiv:1909.09436`, `base_model:huggingface/CodeBERTa-language-id`, `base_model:quantized:huggingface/CodeBERTa-language-id`, `code`, `dataset:code_search_net`, `license:apache-2.0`, `onnx`, `region:us`, `roberta`, `text-classification`, `transformers.js`

### 4. CodeBERTa small v1

- Индекс: `xlocllm.unit("code", "onnx-community/CodeBERTa-small-v1-ONNX")`
- Model ID: `onnx-community/CodeBERTa-small-v1-ONNX`
- Для чего подходит: known browser-ready provider Подходит для: code embeddings, определение языка кода и code understanding.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.16 GB`
- Disk: `160 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `да`
- License: `unknown`
- Languages: `universal`
- Алиасы: `CodeBERTa small v1`, `CodeBERTa-small-v1`, `CodeBERTa-small-v1-ONNX`, `onnx-community/CodeBERTa-small-v1-ONNX`
- Теги: `Code`, `arxiv:1909.09436`, `base_model:huggingface/CodeBERTa-small-v1`, `base_model:quantized:huggingface/CodeBERTa-small-v1`, `code`, `dataset:code_search_net`, `fill-mask`, `onnx`, `region:us`, `roberta`, `transformers.js`
