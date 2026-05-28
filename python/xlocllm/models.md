# xlocllm Models Catalog

Source: `packages/catalog/models.json`, schemaVersion `2`.
Unit groups: `24`. Models: `217`.

This file documents the browser/WebGPU catalog source. In xlocllm v1.1 the
default Python mode is `native`, which uses a separate generated native registry
with GGUF LLM entries and ONNX Runtime task-model entries. Inspect the active
catalog from Python:

```python
import xlocllm

xlocllm.models(mode="native")  # default v1.1 runtime catalog
xlocllm.models(mode="web")     # browser/WebGPU catalog documented below
xlocllm.model("Qwen-3.5-0.8b", unit="LLM", mode="native").to_dict()
```

Every entry contains the exact lookup index: use `xlocllm.unit("<unit>", "<modelId>")`.
Inside each group, models are ordered from lighter/weaker to stronger/heavier by `hardwareTier`, parameter count, VRAM, and disk size.

## Groups

## LLM - LLM

Purpose: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
Catalog task: `text-generation`.
Invoke endpoint: `chat.completions`.

### 1. gemma 4 E2B it

- Index: `xlocllm.unit("LLM", "onnx-community/gemma-4-E2B-it-ONNX")`
- Model ID: `onnx-community/gemma-4-E2B-it-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `540 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `gemma 4 E2B it`, `gemma-4-E2B-it`, `gemma-4-E2B-it-ONNX`, `onnx-community/gemma-4-E2B-it-ONNX`
- Tags: `LLM`, `any-to-any`, `base_model:google/gemma-4-E2B-it`, `base_model:quantized:google/gemma-4-E2B-it`, `conversational`, `gemma4`, `image-text-to-text`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`

### 2. gemma 4 E4B it

- Index: `xlocllm.unit("LLM", "onnx-community/gemma-4-E4B-it-ONNX")`
- Model ID: `onnx-community/gemma-4-E4B-it-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `540 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `gemma 4 E4B it`, `gemma-4-E4B-it`, `gemma-4-E4B-it-ONNX`, `onnx-community/gemma-4-E4B-it-ONNX`
- Tags: `LLM`, `any-to-any`, `base_model:google/gemma-4-E2B-it`, `base_model:quantized:google/gemma-4-E2B-it`, `conversational`, `gemma4`, `image-text-to-text`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`

### 3. SmolLM 135M

- Index: `xlocllm.unit("LLM", "onnx-community/SmolLM-135M-ONNX")`
- Model ID: `onnx-community/SmolLM-135M-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.135B`
- Model size: `0.12 GB`
- Disk: `128 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `SmolLM 135M`, `SmolLM-135M`, `SmolLM-135M-ONNX`, `onnx-community/SmolLM-135M-ONNX`
- Tags: `LLM`, `base_model:HuggingFaceTB/SmolLM-135M`, `base_model:quantized:HuggingFaceTB/SmolLM-135M`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 4. SmolLM 135M Instruct

- Index: `xlocllm.unit("LLM", "onnx-community/SmolLM-135M-Instruct-ONNX")`
- Model ID: `onnx-community/SmolLM-135M-Instruct-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.135B`
- Model size: `0.12 GB`
- Disk: `128 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `SmolLM 135M Instruct`, `SmolLM-135M-Instruct`, `SmolLM-135M-Instruct-ONNX`, `onnx-community/SmolLM-135M-Instruct-ONNX`
- Tags: `LLM`, `base_model:HuggingFaceTB/SmolLM-135M-Instruct`, `base_model:quantized:HuggingFaceTB/SmolLM-135M-Instruct`, `conversational`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 5. SmolLM2 135M

- Index: `xlocllm.unit("LLM", "onnx-community/SmolLM2-135M-ONNX")`
- Model ID: `onnx-community/SmolLM2-135M-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.135B`
- Model size: `0.12 GB`
- Disk: `128 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `SmolLM2 135M`, `SmolLM2-135M`, `SmolLM2-135M-ONNX`, `onnx-community/SmolLM2-135M-ONNX`
- Tags: `LLM`, `base_model:HuggingFaceTB/SmolLM2-135M`, `base_model:quantized:HuggingFaceTB/SmolLM2-135M`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 6. functiongemma 270m it

- Index: `xlocllm.unit("LLM", "onnx-community/functiongemma-270m-it-ONNX")`
- Model ID: `onnx-community/functiongemma-270m-it-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.27B`
- Model size: `0.25 GB`
- Disk: `256 MB`
- VRAM: `460 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `gemma`
- Languages: `en`
- Aliases: `functiongemma 270m it`, `functiongemma-270m-it`, `functiongemma-270m-it-ONNX`, `onnx-community/functiongemma-270m-it-ONNX`
- Tags: `LLM`, `base_model:google/functiongemma-270m-it`, `base_model:quantized:google/functiongemma-270m-it`, `conversational`, `gemma3_text`, `license:gemma`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 7. gemma 3 270m it

- Index: `xlocllm.unit("LLM", "onnx-community/gemma-3-270m-it-ONNX")`
- Model ID: `onnx-community/gemma-3-270m-it-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.27B`
- Model size: `0.25 GB`
- Disk: `256 MB`
- VRAM: `460 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `gemma`
- Languages: `en`
- Aliases: `gemma 3 270m it`, `gemma-3-270m-it`, `gemma-3-270m-it-ONNX`, `onnx-community/gemma-3-270m-it-ONNX`
- Tags: `LLM`, `arxiv:1905.07830`, `arxiv:1905.10044`, `arxiv:1911.11641`, `arxiv:2503.19786`, `conversational`, `gemma`, `gemma3`, `gemma3_text`, `google`, `onnx`, `text-generation`, `transformers.js`

### 8. SmolLM2 360M Instruct

- Index: `xlocllm.unit("LLM", "SmolLM2-360M-Instruct-q4f16_1-MLC")`
- Model ID: `SmolLM2-360M-Instruct-q4f16_1-MLC`
- Best for: tiny mlc model for chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions; languages: en.
- Runtime: `mlc`
- Task: `text-generation`
- Provider: `MLC`
- Hardware tier: `tiny`
- Parameters: `0.36B`
- Model size: `0.27 GB`
- Disk: `280 MB`
- VRAM: `700 MB`
- DType: `q4f16_1`
- NPU/WebNN: `no`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `SmolLM2-360M`, `smollm2`

### 9. SmolLM2 360M

- Index: `xlocllm.unit("LLM", "onnx-community/SmolLM2-360M-ONNX")`
- Model ID: `onnx-community/SmolLM2-360M-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.36B`
- Model size: `0.33 GB`
- Disk: `342 MB`
- VRAM: `615 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `SmolLM2 360M`, `SmolLM2-360M`, `SmolLM2-360M-ONNX`, `onnx-community/SmolLM2-360M-ONNX`
- Tags: `LLM`, `arxiv:2502.02737`, `base_model:HuggingFaceTB/SmolLM2-360M`, `base_model:quantized:HuggingFaceTB/SmolLM2-360M`, `en`, `license:apache-2.0`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 10. SmolLM2 360M Instruct

- Index: `xlocllm.unit("LLM", "HuggingFaceTB/SmolLM2-360M-Instruct")`
- Model ID: `HuggingFaceTB/SmolLM2-360M-Instruct`
- Best for: ONNX/WebGPU artifact marker Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `HuggingFaceTB`
- Hardware tier: `small`
- Parameters: `0.36B`
- Model size: `0.33 GB`
- Disk: `342 MB`
- VRAM: `615 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `HuggingFaceTB/SmolLM2-360M-Instruct`, `SmolLM2 360M Instruct`, `SmolLM2-360M`, `SmolLM2-360M-Instruct`
- Tags: `LLM`, `arxiv:2502.02737`, `base_model:HuggingFaceTB/SmolLM2-360M`, `base_model:quantized:HuggingFaceTB/SmolLM2-360M`, `conversational`, `en`, `llama`, `onnx`, `safetensors`, `tensorboard`, `text-generation`, `transformers`, `transformers.js`

### 11. Qwen2.5 0.5B Instruct

- Index: `xlocllm.unit("LLM", "asdgad/Qwen2.5-0.5B-Instruct-ONNX")`
- Model ID: `asdgad/Qwen2.5-0.5B-Instruct-ONNX`
- Best for: ONNX/WebGPU artifact marker Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `asdgad`
- Hardware tier: `small`
- Parameters: `0.5B`
- Model size: `0.46 GB`
- Disk: `475 MB`
- VRAM: `855 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen2.5 0.5B Instruct`, `Qwen2.5-0.5B-Instruct`, `Qwen2.5-0.5B-Instruct-ONNX`, `asdgad/Qwen2.5-0.5B-Instruct-ONNX`
- Tags: `LLM`, `arxiv:2407.10671`, `base_model:Qwen/Qwen2.5-0.5B-Instruct`, `base_model:quantized:Qwen/Qwen2.5-0.5B-Instruct`, `chat`, `conversational`, `en`, `license:apache-2.0`, `onnx`, `qwen2`, `region:us`, `text-generation`, `transformers.js`

### 12. Qwen2.5 Coder 0.5B Instruct

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen2.5-Coder-0.5B-Instruct")`
- Model ID: `onnx-community/Qwen2.5-Coder-0.5B-Instruct`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.5B`
- Model size: `0.46 GB`
- Disk: `475 MB`
- VRAM: `855 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Qwen2.5 Coder 0.5B Instruct`, `Qwen2.5-Coder-0.5B-Instruct`, `onnx-community/Qwen2.5-Coder-0.5B-Instruct`
- Tags: `LLM`, `base_model:Qwen/Qwen2.5-Coder-0.5B-Instruct`, `base_model:quantized:Qwen/Qwen2.5-Coder-0.5B-Instruct`, `conversational`, `onnx`, `qwen2`, `region:us`, `text-generation`, `transformers.js`

### 13. Qwen3 0.6B DQ

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen3-0.6B-DQ-ONNX")`
- Model ID: `onnx-community/Qwen3-0.6B-DQ-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.6B`
- Model size: `0.3 GB`
- Disk: `312 MB`
- VRAM: `561 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Qwen3 0.6B DQ`, `Qwen3-0.6B-DQ`, `Qwen3-0.6B-DQ-ONNX`, `onnx-community/Qwen3-0.6B-DQ-ONNX`
- Tags: `LLM`, `arxiv:2501.06417`, `base_model:Qwen/Qwen3-0.6B`, `base_model:quantized:Qwen/Qwen3-0.6B`, `conversational`, `onnx`, `qwen3`, `region:us`, `text-generation`, `transformers.js`

### 14. Qwen3 0.6B ONNX

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen3-0.6B-ONNX")`
- Model ID: `onnx-community/Qwen3-0.6B-ONNX`
- Best for: small transformers model for chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions; languages: multilingual.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.6B`
- Model size: `0.49 GB`
- Disk: `500 MB`
- VRAM: `1100 MB`
- DType: `q4`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen3-0.6B-ONNX`, `qwen3-0.6b-tjs`

### 15. Qwen 3.5 0.8B q4

- Index: `xlocllm.unit("LLM", "Qwen3.5-0.8B-q4f16_1-MLC")`
- Model ID: `Qwen3.5-0.8B-q4f16_1-MLC`
- Best for: Small multilingual chat model for low-end GPUs. Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `mlc`
- Task: `text-generation`
- Provider: `MLC`
- Hardware tier: `small`
- Parameters: `0.8B`
- Model size: `0.63 GB`
- Disk: `650 MB`
- VRAM: `1200 MB`
- DType: `q4f16_1`
- NPU/WebNN: `no`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen-3.5-0.8b`, `qwen3.5-0.8b`, `qwen-0.8b`

### 16. Qwen3.5 0.8B

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen3.5-0.8B-ONNX")`
- Model ID: `onnx-community/Qwen3.5-0.8B-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.8B`
- Model size: `0.74 GB`
- Disk: `760 MB`
- VRAM: `1368 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen-3.5-0.8b`, `Qwen3.5 0.8B`, `Qwen3.5-0.8B`, `Qwen3.5-0.8B-ONNX`, `onnx-community/Qwen3.5-0.8B-ONNX`, `qwen3.5-0.8b`
- Tags: `LLM`, `base_model:Qwen/Qwen3.5-0.8B`, `base_model:quantized:Qwen/Qwen3.5-0.8B`, `conversational`, `image-text-to-text`, `license:apache-2.0`, `onnx`, `qwen3_5`, `region:us`

### 17. Llama 3.2 1B Instruct q4f16

- Index: `xlocllm.unit("LLM", "onnx-community/Llama-3.2-1B-Instruct-q4f16")`
- Model ID: `onnx-community/Llama-3.2-1B-Instruct-q4f16`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `1.0B`
- Model size: `0.51 GB`
- Disk: `520 MB`
- VRAM: `936 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `llama3.2`
- Languages: `en`
- Aliases: `Llama 3.2 1B Instruct`, `Llama-3.2-1B-Instruct`, `Llama-3.2-1B-Instruct-q4f16`, `onnx-community/Llama-3.2-1B-Instruct-q4f16`
- Tags: `LLM`, `conversational`, `de`, `en`, `facebook`, `fr`, `llama`, `llama-3`, `meta`, `onnx`, `pytorch`, `text-generation`, `transformers.js`

### 18. gemma 3 1b it

- Index: `xlocllm.unit("LLM", "onnx-community/gemma-3-1b-it-ONNX")`
- Model ID: `onnx-community/gemma-3-1b-it-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `1.0B`
- Model size: `0.93 GB`
- Disk: `950 MB`
- VRAM: `1710 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `gemma`
- Languages: `en`
- Aliases: `gemma 3 1b it`, `gemma-3-1b-it`, `gemma-3-1b-it-ONNX`, `onnx-community/gemma-3-1b-it-ONNX`
- Tags: `LLM`, `base_model:google/gemma-3-1b-it`, `base_model:quantized:google/gemma-3-1b-it`, `conversational`, `gemma3_text`, `license:gemma`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 19. gemma 3 1b it

- Index: `xlocllm.unit("LLM", "onnx-community/gemma-3-1b-it-ONNX-GQA")`
- Model ID: `onnx-community/gemma-3-1b-it-ONNX-GQA`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `1.0B`
- Model size: `0.93 GB`
- Disk: `950 MB`
- VRAM: `1710 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `gemma 3 1b it`, `gemma-3-1b-it`, `gemma-3-1b-it-ONNX-GQA`, `onnx-community/gemma-3-1b-it-ONNX-GQA`
- Tags: `LLM`, `base_model:google/gemma-3-1b-it`, `base_model:quantized:google/gemma-3-1b-it`, `conversational`, `gemma3_text`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 20. Llama 3.2 1B Instruct

- Index: `xlocllm.unit("LLM", "onnx-community/Llama-3.2-1B-Instruct-ONNX")`
- Model ID: `onnx-community/Llama-3.2-1B-Instruct-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `1.0B`
- Model size: `0.93 GB`
- Disk: `950 MB`
- VRAM: `1710 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `llama3.2`
- Languages: `en`
- Aliases: `Llama 3.2 1B Instruct`, `Llama-3.2-1B-Instruct`, `Llama-3.2-1B-Instruct-ONNX`, `onnx-community/Llama-3.2-1B-Instruct-ONNX`
- Tags: `LLM`, `base_model:meta-llama/Llama-3.2-1B-Instruct`, `base_model:quantized:meta-llama/Llama-3.2-1B-Instruct`, `conversational`, `license:llama3.2`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 21. Llama 3.2 1B Instruct q4

- Index: `xlocllm.unit("LLM", "Llama-3.2-1B-Instruct-q4f16_1-MLC")`
- Model ID: `Llama-3.2-1B-Instruct-q4f16_1-MLC`
- Best for: small mlc model for chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions; languages: en, multilingual.
- Runtime: `mlc`
- Task: `text-generation`
- Provider: `MLC`
- Hardware tier: `small`
- Parameters: `1.0B`
- Model size: `0.83 GB`
- Disk: `850 MB`
- VRAM: `1800 MB`
- DType: `q4f16_1`
- NPU/WebNN: `no`
- License: `llama3.2`
- Languages: `en, multilingual`
- Aliases: `Llama-3.2-1b`, `llama-1b`

### 22. Phi 4 mini Instruct q4

- Index: `xlocllm.unit("LLM", "Phi-4-mini-instruct-q4f16_1-MLC")`
- Model ID: `Phi-4-mini-instruct-q4f16_1-MLC`
- Best for: medium mlc model for chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions; languages: en, multilingual.
- Runtime: `mlc`
- Task: `text-generation`
- Provider: `MLC`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `2.44 GB`
- Disk: `2500 MB`
- VRAM: `4200 MB`
- DType: `q4f16_1`
- NPU/WebNN: `no`
- License: `mit`
- Languages: `en, multilingual`
- Aliases: `Phi-4-mini`, `phi4-mini`

### 23. Qwen3.5 0.8B ONNX FP16

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen3.5-0.8B-ONNX#fp16")`
- Model ID: `onnx-community/Qwen3.5-0.8B-ONNX#fp16`
- Backend model ID: `onnx-community/Qwen3.5-0.8B-ONNX`
- Best for: Higher-quality non-q4 ONNX variant; uses FP16 files from the same HF repo. Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `0.8B`
- Model size: `1.52 GB`
- Disk: `1560 MB`
- VRAM: `2200 MB`
- DType: `fp16`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen-3.5-0.8b-fp16`, `Qwen-3.5-0.8b-no-q4`, `Qwen-3.5-0.8b-unquantized`, `Qwen3.5-0.8B-ONNX-fp16`, `qwen3.5-0.8b-fp16`
- Tags: `LLM`, `no-q4`, `fp16`, `onnx`, `qwen3_5`, `conversational`

### 24. Qwen3.5 0.8B ONNX FP32

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen3.5-0.8B-ONNX#fp32")`
- Model ID: `onnx-community/Qwen3.5-0.8B-ONNX#fp32`
- Backend model ID: `onnx-community/Qwen3.5-0.8B-ONNX`
- Best for: Full precision ONNX variant without q4/q8 quantization. Heavier than the default MLC q4 profile. Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `0.8B`
- Model size: `2.95 GB`
- Disk: `3020 MB`
- VRAM: `3600 MB`
- DType: `fp32`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen-3.5-0.8b-full`, `Qwen-3.5-0.8b-fp32`, `Qwen-3.5-0.8b-no-quant`, `Qwen3.5-0.8B-ONNX-fp32`, `qwen3.5-0.8b-full`
- Tags: `LLM`, `full`, `fp32`, `onnx`, `qwen3_5`, `conversational`

### 25. Qwen 2.5 1.5B Instruct q4

- Index: `xlocllm.unit("LLM", "Qwen2.5-1.5B-Instruct-q4f16_1-MLC")`
- Model ID: `Qwen2.5-1.5B-Instruct-q4f16_1-MLC`
- Best for: medium mlc model for chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions; languages: multilingual.
- Runtime: `mlc`
- Task: `text-generation`
- Provider: `MLC`
- Hardware tier: `medium`
- Parameters: `1.5B`
- Model size: `1.12 GB`
- Disk: `1150 MB`
- VRAM: `2200 MB`
- DType: `q4f16_1`
- NPU/WebNN: `no`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen-2.5-1.5b`, `qwen2.5-1.5b`

### 26. DeepSeek R1 Distill Qwen 1.5B

- Index: `xlocllm.unit("LLM", "onnx-community/DeepSeek-R1-Distill-Qwen-1.5B-ONNX")`
- Model ID: `onnx-community/DeepSeek-R1-Distill-Qwen-1.5B-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `1.5B`
- Model size: `1.39 GB`
- Disk: `1425 MB`
- VRAM: `2565 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `DeepSeek R1 Distill Qwen 1.5B`, `DeepSeek-R1-Distill-Qwen-1.5B`, `DeepSeek-R1-Distill-Qwen-1.5B-ONNX`, `onnx-community/DeepSeek-R1-Distill-Qwen-1.5B-ONNX`
- Tags: `LLM`, `base_model:deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`, `base_model:quantized:deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`, `conversational`, `onnx`, `qwen2`, `region:us`, `text-generation`, `transformers.js`

### 27. Qwen2.5 Coder 1.5B Instruct

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen2.5-Coder-1.5B-Instruct")`
- Model ID: `onnx-community/Qwen2.5-Coder-1.5B-Instruct`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `1.5B`
- Model size: `1.39 GB`
- Disk: `1425 MB`
- VRAM: `2565 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen2.5 Coder 1.5B Instruct`, `Qwen2.5-Coder-1.5B-Instruct`, `onnx-community/Qwen2.5-Coder-1.5B-Instruct`
- Tags: `LLM`, `base_model:Qwen/Qwen2.5-Coder-1.5B-Instruct`, `base_model:quantized:Qwen/Qwen2.5-Coder-1.5B-Instruct`, `conversational`, `license:apache-2.0`, `onnx`, `qwen2`, `region:us`, `text-generation`, `transformers.js`

### 28. Qwen3 1.7B

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen3-1.7B-ONNX")`
- Model ID: `onnx-community/Qwen3-1.7B-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `1.7B`
- Model size: `1.58 GB`
- Disk: `1615 MB`
- VRAM: `2907 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Qwen3 1.7B`, `Qwen3-1.7B`, `Qwen3-1.7B-ONNX`, `onnx-community/Qwen3-1.7B-ONNX`
- Tags: `LLM`, `base_model:Qwen/Qwen3-1.7B`, `base_model:quantized:Qwen/Qwen3-1.7B`, `conversational`, `onnx`, `qwen3`, `region:us`, `text-generation`, `transformers.js`

### 29. SmolLM2 1.7B Instruct

- Index: `xlocllm.unit("LLM", "HuggingFaceTB/SmolLM2-1.7B-Instruct")`
- Model ID: `HuggingFaceTB/SmolLM2-1.7B-Instruct`
- Best for: ONNX/WebGPU artifact marker Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `HuggingFaceTB`
- Hardware tier: `medium`
- Parameters: `1.7B`
- Model size: `1.58 GB`
- Disk: `1615 MB`
- VRAM: `2907 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `HuggingFaceTB/SmolLM2-1.7B-Instruct`, `SmolLM2 1.7B Instruct`, `SmolLM2-1.7B-Instruct`
- Tags: `LLM`, `arxiv:2502.02737`, `base_model:HuggingFaceTB/SmolLM2-1.7B`, `base_model:quantized:HuggingFaceTB/SmolLM2-1.7B`, `conversational`, `en`, `llama`, `onnx`, `safetensors`, `tensorboard`, `text-generation`, `transformers`, `transformers.js`

### 30. Llama 3.2 3B

- Index: `xlocllm.unit("LLM", "onnx-community/Llama-3.2-3B")`
- Model ID: `onnx-community/Llama-3.2-3B`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `3.0B`
- Model size: `2.78 GB`
- Disk: `2850 MB`
- VRAM: `5130 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `llama3.2`
- Languages: `en`
- Aliases: `Llama 3.2 3B`, `Llama-3.2-3B`, `onnx-community/Llama-3.2-3B`
- Tags: `LLM`, `base_model:meta-llama/Llama-3.2-3B`, `base_model:quantized:meta-llama/Llama-3.2-3B`, `license:llama3.2`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 31. Llama 3.2 3B Instruct

- Index: `xlocllm.unit("LLM", "onnx-community/Llama-3.2-3B-Instruct-ONNX")`
- Model ID: `onnx-community/Llama-3.2-3B-Instruct-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `3.0B`
- Model size: `2.78 GB`
- Disk: `2850 MB`
- VRAM: `5130 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `llama3.2`
- Languages: `en`
- Aliases: `Llama 3.2 3B Instruct`, `Llama-3.2-3B-Instruct`, `Llama-3.2-3B-Instruct-ONNX`, `onnx-community/Llama-3.2-3B-Instruct-ONNX`
- Tags: `LLM`, `base_model:meta-llama/Llama-3.2-3B-Instruct`, `base_model:quantized:meta-llama/Llama-3.2-3B-Instruct`, `conversational`, `license:llama3.2`, `llama`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 32. Qwen2.5 Coder 3B Instruct

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen2.5-Coder-3B-Instruct")`
- Model ID: `onnx-community/Qwen2.5-Coder-3B-Instruct`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `3.0B`
- Model size: `2.78 GB`
- Disk: `2850 MB`
- VRAM: `5130 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Qwen2.5 Coder 3B Instruct`, `Qwen2.5-Coder-3B-Instruct`, `onnx-community/Qwen2.5-Coder-3B-Instruct`
- Tags: `LLM`, `base_model:Qwen/Qwen2.5-Coder-3B-Instruct`, `base_model:quantized:Qwen/Qwen2.5-Coder-3B-Instruct`, `conversational`, `onnx`, `qwen2`, `region:us`, `text-generation`, `transformers.js`

### 33. SmolLM3 3B

- Index: `xlocllm.unit("LLM", "HuggingFaceTB/SmolLM3-3B-ONNX")`
- Model ID: `HuggingFaceTB/SmolLM3-3B-ONNX`
- Best for: ONNX/WebGPU artifact marker Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `HuggingFaceTB`
- Hardware tier: `medium`
- Parameters: `3.0B`
- Model size: `2.78 GB`
- Disk: `2850 MB`
- VRAM: `5130 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `HuggingFaceTB/SmolLM3-3B-ONNX`, `SmolLM3 3B`, `SmolLM3-3B`, `SmolLM3-3B-ONNX`
- Tags: `LLM`, `ar`, `conversational`, `en`, `es`, `fr`, `it`, `onnx`, `pt`, `smollm3`, `text-generation`, `transformers.js`, `zh`

### 34. SmolLM3 3B Base

- Index: `xlocllm.unit("LLM", "HuggingFaceTB/SmolLM3-3B-Base")`
- Model ID: `HuggingFaceTB/SmolLM3-3B-Base`
- Best for: ONNX/WebGPU artifact marker Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `HuggingFaceTB`
- Hardware tier: `medium`
- Parameters: `3.0B`
- Model size: `2.78 GB`
- Disk: `2850 MB`
- VRAM: `5130 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `HuggingFaceTB/SmolLM3-3B-Base`, `SmolLM3 3B Base`, `SmolLM3-3B-Base`
- Tags: `LLM`, `en`, `es`, `fr`, `it`, `onnx`, `pt`, `safetensors`, `smollm3`, `text-generation`, `transformers`, `transformers.js`, `zh`

### 35. Qwen3 4B

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen3-4B-ONNX")`
- Model ID: `onnx-community/Qwen3-4B-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `4.0B`
- Model size: `3.71 GB`
- Disk: `3800 MB`
- VRAM: `6840 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Qwen3 4B`, `Qwen3-4B`, `Qwen3-4B-ONNX`, `onnx-community/Qwen3-4B-ONNX`
- Tags: `LLM`, `base_model:Qwen/Qwen3-4B`, `base_model:quantized:Qwen/Qwen3-4B`, `conversational`, `onnx`, `qwen3`, `region:us`, `text-generation`, `transformers.js`

### 36. Qwen3 8B

- Index: `xlocllm.unit("LLM", "onnx-community/Qwen3-8B-ONNX")`
- Model ID: `onnx-community/Qwen3-8B-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `large`
- Parameters: `8.0B`
- Model size: `7.42 GB`
- Disk: `7600 MB`
- VRAM: `13680 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen3 8B`, `Qwen3-8B`, `Qwen3-8B-ONNX`, `onnx-community/Qwen3-8B-ONNX`
- Tags: `LLM`, `ONNX`, `ONNX Runtime`, `base_model:Qwen/Qwen3-8B`, `base_model:quantized:Qwen/Qwen3-8B`, `code`, `en`, `license:apache-2.0`, `nlp`, `onnx`, `qwen3`, `region:us`

### 37. gpt oss 20b

- Index: `xlocllm.unit("LLM", "onnx-community/gpt-oss-20b-ONNX")`
- Model ID: `onnx-community/gpt-oss-20b-ONNX`
- Best for: known browser-ready provider Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnx-community`
- Hardware tier: `large`
- Parameters: `20.0B`
- Model size: `18.55 GB`
- Disk: `19000 MB`
- VRAM: `34200 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `gpt oss 20b`, `gpt-oss-20b`, `gpt-oss-20b-ONNX`, `onnx-community/gpt-oss-20b-ONNX`
- Tags: `LLM`, `base_model:openai/gpt-oss-20b`, `base_model:quantized:openai/gpt-oss-20b`, `conversational`, `gpt_oss`, `license:apache-2.0`, `mxfp4`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 38. gpt oss 20b

- Index: `xlocllm.unit("LLM", "onnxruntime/gpt-oss-20b-onnx")`
- Model ID: `onnxruntime/gpt-oss-20b-onnx`
- Best for: ONNX/WebGPU artifact marker Best for: chat, text generation, reasoning, coding assistance, and OpenAI-compatible chat completions.
- Runtime: `transformers`
- Task: `text-generation`
- Provider: `onnxruntime`
- Hardware tier: `large`
- Parameters: `20.0B`
- Model size: `18.55 GB`
- Disk: `19000 MB`
- VRAM: `34200 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `gpt oss 20b`, `gpt-oss-20b`, `gpt-oss-20b-onnx`, `onnxruntime/gpt-oss-20b-onnx`
- Tags: `LLM`, `ONNX`, `ONNXRuntime`, `base_model:openai/gpt-oss-20b`, `base_model:quantized:openai/gpt-oss-20b`, `en`, `license:apache-2.0`, `onnx`, `region:us`, `safetensors`

## embedding - Embeddings

Purpose: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
Catalog task: `feature-extraction`.
Invoke endpoint: `embeddings`.

### 1. all-MiniLM-L6-v2

- Index: `xlocllm.unit("embedding", "Xenova/all-MiniLM-L6-v2")`
- Model ID: `Xenova/all-MiniLM-L6-v2`
- Best for: tiny transformers model for semantic search, retrieval, clustering, vector databases, and RAG pipelines; languages: en.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.09 GB`
- Disk: `90 MB`
- VRAM: `250 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `all-MiniLM-L6-v2`, `minilm`

### 2. Multilingual E5 small

- Index: `xlocllm.unit("embedding", "Xenova/multilingual-e5-small")`
- Model ID: `Xenova/multilingual-e5-small`
- Best for: tiny transformers model for semantic search, retrieval, clustering, vector databases, and RAG pipelines; languages: multilingual.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `350 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `multilingual`
- Aliases: `multilingual-e5-small`, `e5-small`

### 3. all MiniLM L12 v2

- Index: `xlocllm.unit("embedding", "Xenova/all-MiniLM-L12-v2")`
- Model ID: `Xenova/all-MiniLM-L12-v2`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/all-MiniLM-L12-v2`, `all MiniLM L12 v2`, `all-MiniLM-L12-v2`
- Tags: `Embedding`, `Embeddings`, `base_model:quantized:sentence-transformers/all-MiniLM-L12-v2`, `base_model:sentence-transformers/all-MiniLM-L12-v2`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 4. all MiniLM L6 v2

- Index: `xlocllm.unit("embedding", "sentence-transformers/all-MiniLM-L6-v2")`
- Model ID: `sentence-transformers/all-MiniLM-L6-v2`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `sentence-transformers`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `all MiniLM L6 v2`, `all-MiniLM-L6-v2`, `sentence-transformers/all-MiniLM-L6-v2`
- Tags: `Embedding`, `Embeddings`, `bert`, `en`, `feature-extraction`, `onnx`, `openvino`, `pytorch`, `rust`, `safetensors`, `sentence-similarity`, `sentence-transformers`, `tf`, `transformers`

### 5. bge base en v1.5

- Index: `xlocllm.unit("embedding", "onnx-community/bge-base-en-v1.5-ONNX")`
- Model ID: `onnx-community/bge-base-en-v1.5-ONNX`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `en`
- Aliases: `bge base en v1.5`, `bge-base-en-v1.5`, `bge-base-en-v1.5-ONNX`, `onnx-community/bge-base-en-v1.5-ONNX`
- Tags: `Embedding`, `Embeddings`, `base_model:BAAI/bge-base-en-v1.5`, `base_model:quantized:BAAI/bge-base-en-v1.5`, `bert`, `en`, `endpoints_compatible`, `feature-extraction`, `license:mit`, `onnx`, `sentence-similarity`, `sentence-transformers`, `text-embeddings-inference`, `transformers.js`

### 6. bge base en v1.5

- Index: `xlocllm.unit("embedding", "Xenova/bge-base-en-v1.5")`
- Model ID: `Xenova/bge-base-en-v1.5`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `en`
- Aliases: `Xenova/bge-base-en-v1.5`, `bge base en v1.5`, `bge-base-en-v1.5`
- Tags: `Embedding`, `Embeddings`, `base_model:BAAI/bge-base-en-v1.5`, `base_model:quantized:BAAI/bge-base-en-v1.5`, `bert`, `feature-extraction`, `license:mit`, `onnx`, `region:us`, `transformers.js`

### 7. bge large en v1.5

- Index: `xlocllm.unit("embedding", "Xenova/bge-large-en-v1.5")`
- Model ID: `Xenova/bge-large-en-v1.5`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/bge-large-en-v1.5`, `bge large en v1.5`, `bge-large-en-v1.5`
- Tags: `Embedding`, `Embeddings`, `base_model:BAAI/bge-large-en-v1.5`, `base_model:quantized:BAAI/bge-large-en-v1.5`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 8. bge large zh v1.5

- Index: `xlocllm.unit("embedding", "baby2008/bge-large-zh-v1.5")`
- Model ID: `baby2008/bge-large-zh-v1.5`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `baby2008`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `baby2008/bge-large-zh-v1.5`, `bge large zh v1.5`, `bge-large-zh-v1.5`
- Tags: `Embedding`, `Embeddings`, `base_model:BAAI/bge-large-zh-v1.5`, `base_model:quantized:BAAI/bge-large-zh-v1.5`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 9. bge m3

- Index: `xlocllm.unit("embedding", "Xenova/bge-m3")`
- Model ID: `Xenova/bge-m3`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `multilingual`
- Aliases: `Xenova/bge-m3`, `bge m3`, `bge-m3`
- Tags: `Embedding`, `Embeddings`, `base_model:BAAI/bge-m3`, `base_model:quantized:BAAI/bge-m3`, `feature-extraction`, `license:mit`, `onnx`, `region:us`, `transformers.js`, `xlm-roberta`

### 10. bge small en v1.5

- Index: `xlocllm.unit("embedding", "onnx-community/bge-small-en-v1.5-ONNX")`
- Model ID: `onnx-community/bge-small-en-v1.5-ONNX`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `bge small en v1.5`, `bge-small-en-v1.5`, `bge-small-en-v1.5-ONNX`, `onnx-community/bge-small-en-v1.5-ONNX`
- Tags: `Embedding`, `Embeddings`, `base_model:BAAI/bge-small-en-v1.5`, `base_model:quantized:BAAI/bge-small-en-v1.5`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 11. bge small zh v1.5

- Index: `xlocllm.unit("embedding", "vteaw/bge-small-zh-v1.5")`
- Model ID: `vteaw/bge-small-zh-v1.5`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `vteaw`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `bge small zh v1.5`, `bge-small-zh-v1.5`, `vteaw/bge-small-zh-v1.5`
- Tags: `Embedding`, `Embeddings`, `base_model:BAAI/bge-small-zh-v1.5`, `base_model:quantized:BAAI/bge-small-zh-v1.5`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 12. gte multilingual base

- Index: `xlocllm.unit("embedding", "baby2008/gte-multilingual-base")`
- Model ID: `baby2008/gte-multilingual-base`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `baby2008`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `baby2008/gte-multilingual-base`, `gte multilingual base`, `gte-multilingual-base`
- Tags: `Embedding`, `Embeddings`, `base_model:Alibaba-NLP/gte-multilingual-base`, `base_model:quantized:Alibaba-NLP/gte-multilingual-base`, `custom_code`, `feature-extraction`, `new`, `onnx`, `region:us`, `transformers.js`

### 13. jina clip v1

- Index: `xlocllm.unit("embedding", "jinaai/jina-clip-v1")`
- Model ID: `jinaai/jina-clip-v1`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `jinaai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `jina clip v1`, `jina-clip-v1`, `jinaai/jina-clip-v1`
- Tags: `Embedding`, `Embeddings`, `clip`, `feature-extraction`, `jina_clip`, `mteb`, `onnx`, `pytorch`, `safetensors`, `sentence-similarity`, `sentence-transformers`, `transformers`, `transformers.js`, `vision`

### 14. jina clip v2

- Index: `xlocllm.unit("embedding", "jinaai/jina-clip-v2")`
- Model ID: `jinaai/jina-clip-v2`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `jinaai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-nc-4.0`
- Languages: `multilingual`
- Aliases: `jina clip v2`, `jina-clip-v2`, `jinaai/jina-clip-v2`
- Tags: `Embedding`, `Embeddings`, `clip`, `eva02`, `feature-extraction`, `jina_clip`, `multimodal`, `onnx`, `pytorch`, `retrieval`, `safetensors`, `sentence-similarity`, `transformers`, `xlm-roberta`

### 15. jina embeddings v3

- Index: `xlocllm.unit("embedding", "jinaai/jina-embeddings-v3")`
- Model ID: `jinaai/jina-embeddings-v3`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `jinaai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-nc-4.0`
- Languages: `multilingual`
- Aliases: `jina embeddings v3`, `jina-embeddings-v3`, `jinaai/jina-embeddings-v3`
- Tags: `Embedding`, `Embeddings`, `af`, `am`, `custom_code`, `feature-extraction`, `mteb`, `multilingual`, `onnx`, `pytorch`, `safetensors`, `sentence-similarity`, `sentence-transformers`, `transformers`

### 16. jina embeddings v5 omni nano

- Index: `xlocllm.unit("embedding", "onnx-community/jina-embeddings-v5-omni-nano-ONNX")`
- Model ID: `onnx-community/jina-embeddings-v5-omni-nano-ONNX`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-nc-4.0`
- Languages: `multilingual`
- Aliases: `jina embeddings v5 omni nano`, `jina-embeddings-v5-omni-nano`, `jina-embeddings-v5-omni-nano-ONNX`, `onnx-community/jina-embeddings-v5-omni-nano-ONNX`
- Tags: `Embedding`, `Embeddings`, `cross-modal-retrieval`, `custom_code`, `embeddings`, `feature-extraction`, `jina-embeddings`, `jina_embeddings_v5_omni`, `multilingual`, `multimodal`, `onnx`, `sentence-similarity`, `transformers.js`, `webgpu`

### 17. multilingual e5 base

- Index: `xlocllm.unit("embedding", "Xenova/multilingual-e5-base")`
- Model ID: `Xenova/multilingual-e5-base`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/multilingual-e5-base`, `multilingual e5 base`, `multilingual-e5-base`
- Tags: `Embedding`, `Embeddings`, `base_model:intfloat/multilingual-e5-base`, `base_model:quantized:intfloat/multilingual-e5-base`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`, `xlm-roberta`

### 18. multilingual e5 large

- Index: `xlocllm.unit("embedding", "Xenova/multilingual-e5-large")`
- Model ID: `Xenova/multilingual-e5-large`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/multilingual-e5-large`, `multilingual e5 large`, `multilingual-e5-large`
- Tags: `Embedding`, `Embeddings`, `base_model:intfloat/multilingual-e5-large`, `base_model:quantized:intfloat/multilingual-e5-large`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`, `xlm-roberta`

### 19. mxbai embed xsmall v1

- Index: `xlocllm.unit("embedding", "mixedbread-ai/mxbai-embed-xsmall-v1")`
- Model ID: `mixedbread-ai/mxbai-embed-xsmall-v1`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `mixedbread-ai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `mixedbread-ai/mxbai-embed-xsmall-v1`, `mxbai embed xsmall v1`, `mxbai-embed-xsmall-v1`
- Tags: `Embedding`, `Embeddings`, `arxiv:2309.12871`, `arxiv:2402.14776`, `base_model:mixedbread-ai/mxbai-embed-xsmall-v1`, `bert`, `en`, `feature-extraction`, `gguf`, `mteb`, `onnx`, `openvino`, `safetensors`, `sentence-transformers`

### 20. nomic embed text v1

- Index: `xlocllm.unit("embedding", "Xenova/nomic-embed-text-v1")`
- Model ID: `Xenova/nomic-embed-text-v1`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/nomic-embed-text-v1`, `nomic embed text v1`, `nomic-embed-text-v1`
- Tags: `Embedding`, `Embeddings`, `base_model:nomic-ai/nomic-embed-text-v1`, `base_model:quantized:nomic-ai/nomic-embed-text-v1`, `custom_code`, `feature-extraction`, `nomic_bert`, `onnx`, `region:us`, `transformers.js`

### 21. nomic embed text v1.5

- Index: `xlocllm.unit("embedding", "nomic-ai/nomic-embed-text-v1.5")`
- Model ID: `nomic-ai/nomic-embed-text-v1.5`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `nomic-ai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `nomic embed text v1.5`, `nomic-ai/nomic-embed-text-v1.5`, `nomic-embed-text-v1.5`
- Tags: `Embedding`, `Embeddings`, `arxiv:2402.01613`, `custom_code`, `en`, `feature-extraction`, `mteb`, `nomic_bert`, `onnx`, `safetensors`, `sentence-similarity`, `sentence-transformers`, `transformers`, `transformers.js`

### 22. paraphrase MiniLM L6 v2

- Index: `xlocllm.unit("embedding", "Xenova/paraphrase-MiniLM-L6-v2")`
- Model ID: `Xenova/paraphrase-MiniLM-L6-v2`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/paraphrase-MiniLM-L6-v2`, `paraphrase MiniLM L6 v2`, `paraphrase-MiniLM-L6-v2`
- Tags: `Embedding`, `Embeddings`, `base_model:quantized:sentence-transformers/paraphrase-MiniLM-L6-v2`, `base_model:sentence-transformers/paraphrase-MiniLM-L6-v2`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 23. paraphrase multilingual MiniLM L12 v2

- Index: `xlocllm.unit("embedding", "Xenova/paraphrase-multilingual-MiniLM-L12-v2")`
- Model ID: `Xenova/paraphrase-multilingual-MiniLM-L12-v2`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/paraphrase-multilingual-MiniLM-L12-v2`, `paraphrase multilingual MiniLM L12 v2`, `paraphrase-multilingual-MiniLM-L12-v2`
- Tags: `Embedding`, `Embeddings`, `base_model:quantized:sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, `base_model:sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, `bert`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`

### 24. paraphrase multilingual mpnet base v2

- Index: `xlocllm.unit("embedding", "Xenova/paraphrase-multilingual-mpnet-base-v2")`
- Model ID: `Xenova/paraphrase-multilingual-mpnet-base-v2`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/paraphrase-multilingual-mpnet-base-v2`, `paraphrase multilingual mpnet base v2`, `paraphrase-multilingual-mpnet-base-v2`
- Tags: `Embedding`, `Embeddings`, `base_model:quantized:sentence-transformers/paraphrase-multilingual-mpnet-base-v2`, `base_model:sentence-transformers/paraphrase-multilingual-mpnet-base-v2`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`, `xlm-roberta`

### 25. granite embedding 97m multilingual r2

- Index: `xlocllm.unit("embedding", "philipp-zettl/granite-embedding-97m-multilingual-r2-ONNX")`
- Model ID: `philipp-zettl/granite-embedding-97m-multilingual-r2-ONNX`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `philipp-zettl`
- Hardware tier: `tiny`
- Parameters: `0.097B`
- Model size: `0.09 GB`
- Disk: `92 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `granite embedding 97m multilingual r2`, `granite-embedding-97m-multilingual-r2`, `granite-embedding-97m-multilingual-r2-ONNX`, `philipp-zettl/granite-embedding-97m-multilingual-r2-ONNX`
- Tags: `Embedding`, `Embeddings`, `base_model:ibm-granite/granite-embedding-97m-multilingual-r2`, `base_model:quantized:ibm-granite/granite-embedding-97m-multilingual-r2`, `feature-extraction`, `modernbert`, `onnx`, `region:us`, `transformers.js`, `webgpu-export-my-repo`

### 26. granite embedding 107m multilingual

- Index: `xlocllm.unit("embedding", "pelagos-ai/granite-embedding-107m-multilingual-ONNX")`
- Model ID: `pelagos-ai/granite-embedding-107m-multilingual-ONNX`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `pelagos-ai`
- Hardware tier: `tiny`
- Parameters: `0.107B`
- Model size: `0.1 GB`
- Disk: `101 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `granite embedding 107m multilingual`, `granite-embedding-107m-multilingual`, `granite-embedding-107m-multilingual-ONNX`, `pelagos-ai/granite-embedding-107m-multilingual-ONNX`
- Tags: `Embedding`, `Embeddings`, `base_model:ibm-granite/granite-embedding-107m-multilingual`, `base_model:quantized:ibm-granite/granite-embedding-107m-multilingual`, `feature-extraction`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `xlm-roberta`

### 27. embeddinggemma 300m qat q8

- Index: `xlocllm.unit("embedding", "tooape/embeddinggemma-300m-qat-q8-ONNX")`
- Model ID: `tooape/embeddinggemma-300m-qat-q8-ONNX`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `tooape`
- Hardware tier: `tiny`
- Parameters: `0.3B`
- Model size: `0.15 GB`
- Disk: `156 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `gemma`
- Languages: `en`
- Aliases: `embeddinggemma 300m qat q8`, `embeddinggemma-300m-qat-q8`, `embeddinggemma-300m-qat-q8-ONNX`, `tooape/embeddinggemma-300m-qat-q8-ONNX`
- Tags: `Embedding`, `Embeddings`, `base_model:google/embeddinggemma-300m`, `base_model:quantized:google/embeddinggemma-300m`, `embeddinggemma`, `feature-extraction`, `gemma3_text`, `license:gemma`, `onnx`, `quantized`, `region:us`, `sentence-similarity`, `transformers.js`

### 28. granite embedding 311m multilingual r2

- Index: `xlocllm.unit("embedding", "onnx-community/granite-embedding-311m-multilingual-r2-ONNX")`
- Model ID: `onnx-community/granite-embedding-311m-multilingual-r2-ONNX`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.311B`
- Model size: `0.29 GB`
- Disk: `295 MB`
- VRAM: `354 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `granite embedding 311m multilingual r2`, `granite-embedding-311m-multilingual-r2`, `granite-embedding-311m-multilingual-r2-ONNX`, `onnx-community/granite-embedding-311m-multilingual-r2-ONNX`
- Tags: `Embedding`, `Embeddings`, `embeddings`, `feature-extraction`, `granite`, `matryoshka`, `modernbert`, `mteb`, `multilingual`, `onnx`, `openvino`, `sentence-similarity`, `transformers`, `transformers.js`

### 29. Qwen3 Embedding 0.6B

- Index: `xlocllm.unit("embedding", "onnx-community/Qwen3-Embedding-0.6B-ONNX")`
- Model ID: `onnx-community/Qwen3-Embedding-0.6B-ONNX`
- Best for: known browser-ready provider Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.6B`
- Model size: `0.56 GB`
- Disk: `570 MB`
- VRAM: `684 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Qwen3 Embedding 0.6B`, `Qwen3-Embedding-0.6B`, `Qwen3-Embedding-0.6B-ONNX`, `onnx-community/Qwen3-Embedding-0.6B-ONNX`
- Tags: `Embedding`, `Embeddings`, `base_model:Qwen/Qwen3-Embedding-0.6B`, `base_model:quantized:Qwen/Qwen3-Embedding-0.6B`, `feature-extraction`, `onnx`, `qwen3`, `region:us`, `transformers.js`

### 30. Qwen3 Embedding 0.6B

- Index: `xlocllm.unit("embedding", "EMA-Sakuraba-416/Qwen3-Embedding-0.6B-ONNX")`
- Model ID: `EMA-Sakuraba-416/Qwen3-Embedding-0.6B-ONNX`
- Best for: ONNX/WebGPU artifact marker Best for: semantic search, retrieval, clustering, vector databases, and RAG pipelines.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `EMA-Sakuraba-416`
- Hardware tier: `small`
- Parameters: `0.6B`
- Model size: `0.56 GB`
- Disk: `570 MB`
- VRAM: `684 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `EMA-Sakuraba-416/Qwen3-Embedding-0.6B-ONNX`, `Qwen3 Embedding 0.6B`, `Qwen3-Embedding-0.6B`, `Qwen3-Embedding-0.6B-ONNX`
- Tags: `Embedding`, `Embeddings`, `base_model:Qwen/Qwen3-Embedding-0.6B`, `base_model:quantized:Qwen/Qwen3-Embedding-0.6B`, `feature-extraction`, `onnx`, `qwen3`, `region:us`, `transformers.js`

### 31. Snowflake Arctic Embed L v2

- Index: `xlocllm.unit("embedding", "Snowflake/snowflake-arctic-embed-l-v2.0")`
- Model ID: `Snowflake/snowflake-arctic-embed-l-v2.0`
- Best for: large transformers model for semantic search, retrieval, clustering, vector databases, and RAG pipelines; languages: multilingual.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `Snowflake`
- Hardware tier: `large`
- Parameters: `n/a`
- Model size: `1.17 GB`
- Disk: `1200 MB`
- VRAM: `2400 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `arctic-embed-l-v2`, `snowflake-arctic-l`

### 32. Mixedbread embed large

- Index: `xlocllm.unit("embedding", "mixedbread-ai/mxbai-embed-large-v1")`
- Model ID: `mixedbread-ai/mxbai-embed-large-v1`
- Best for: large transformers model for semantic search, retrieval, clustering, vector databases, and RAG pipelines; languages: en.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `mixedbread-ai`
- Hardware tier: `large`
- Parameters: `n/a`
- Model size: `1.32 GB`
- Disk: `1350 MB`
- VRAM: `2600 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `mxbai-embed-large`, `mixedbread-large`

## reranker - Rerankers

Purpose: reranking retrieved documents by relevance to a query.
Catalog task: `text-ranking`.
Invoke endpoint: `rerank`.

### 1. bge reranker large

- Index: `xlocllm.unit("reranker", "Xenova/bge-reranker-large")`
- Model ID: `Xenova/bge-reranker-large`
- Best for: known browser-ready provider Best for: reranking retrieved documents by relevance to a query.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/bge-reranker-large`, `bge reranker large`, `bge-reranker-large`
- Tags: `Reranker`, `Rerankers`, `base_model:BAAI/bge-reranker-large`, `base_model:quantized:BAAI/bge-reranker-large`, `endpoints_compatible`, `onnx`, `region:us`, `sentence-transformers`, `text-classification`, `text-embeddings-inference`, `text-ranking`, `transformers.js`, `xlm-roberta`

### 2. bge reranker v2 m3

- Index: `xlocllm.unit("reranker", "tss-deposium/bge-reranker-v2-m3-onnx-int8")`
- Model ID: `tss-deposium/bge-reranker-v2-m3-onnx-int8`
- Best for: ONNX/WebGPU artifact marker Best for: reranking retrieved documents by relevance to a query.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `tss-deposium`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `multilingual`
- Aliases: `bge reranker v2 m3`, `bge-reranker-v2-m3`, `bge-reranker-v2-m3-onnx-int8`, `tss-deposium/bge-reranker-v2-m3-onnx-int8`
- Tags: `Reranker`, `Rerankers`, `base_model:BAAI/bge-reranker-v2-m3`, `base_model:quantized:BAAI/bge-reranker-v2-m3`, `cross-encoder`, `int8`, `license:mit`, `onnx`, `quantized`, `region:us`, `reranker`, `text-classification`, `transformers.js`, `xlm-roberta`

### 3. gte multilingual reranker base

- Index: `xlocllm.unit("reranker", "onnx-community/gte-multilingual-reranker-base")`
- Model ID: `onnx-community/gte-multilingual-reranker-base`
- Best for: known browser-ready provider Best for: reranking retrieved documents by relevance to a query.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `gte multilingual reranker base`, `gte-multilingual-reranker-base`, `onnx-community/gte-multilingual-reranker-base`
- Tags: `Reranker`, `Rerankers`, `base_model:Alibaba-NLP/gte-multilingual-reranker-base`, `base_model:quantized:Alibaba-NLP/gte-multilingual-reranker-base`, `custom_code`, `new`, `onnx`, `region:us`, `text-classification`, `transformers.js`

### 4. jina reranker v2 base multilingual

- Index: `xlocllm.unit("reranker", "jinaai/jina-reranker-v2-base-multilingual")`
- Model ID: `jinaai/jina-reranker-v2-base-multilingual`
- Best for: ONNX/WebGPU artifact marker Best for: reranking retrieved documents by relevance to a query.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `jinaai`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-nc-4.0`
- Languages: `multilingual`
- Aliases: `jina reranker v2 base multilingual`, `jina-reranker-v2-base-multilingual`, `jinaai/jina-reranker-v2-base-multilingual`
- Tags: `Reranker`, `Rerankers`, `cross-encoder`, `custom_code`, `multilingual`, `onnx`, `pytorch`, `reranker`, `safetensors`, `sentence-transformers`, `text-classification`, `text-ranking`, `transformers`, `transformers.js`

### 5. ms marco TinyBERT L 2 v2

- Index: `xlocllm.unit("reranker", "Xenova/ms-marco-TinyBERT-L-2-v2")`
- Model ID: `Xenova/ms-marco-TinyBERT-L-2-v2`
- Best for: known browser-ready provider Best for: reranking retrieved documents by relevance to a query.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.29 GB`
- Disk: `300 MB`
- VRAM: `360 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/ms-marco-TinyBERT-L-2-v2`, `ms marco TinyBERT L 2 v2`, `ms-marco-TinyBERT-L-2-v2`
- Tags: `Reranker`, `Rerankers`, `base_model:cross-encoder/ms-marco-TinyBERT-L2-v2`, `base_model:quantized:cross-encoder/ms-marco-TinyBERT-L2-v2`, `bert`, `onnx`, `region:us`, `text-classification`, `transformers.js`

### 6. BGE Reranker base

- Index: `xlocllm.unit("reranker", "Xenova/bge-reranker-base")`
- Model ID: `Xenova/bge-reranker-base`
- Best for: small transformers model for reranking retrieved documents by relevance to a query; languages: en, zh.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.42 GB`
- Disk: `430 MB`
- VRAM: `850 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `en, zh`
- Aliases: `bge-reranker-base`

### 7. Qwen3 Reranker 0.6B

- Index: `xlocllm.unit("reranker", "onnx-community/Qwen3-Reranker-0.6B-ONNX")`
- Model ID: `onnx-community/Qwen3-Reranker-0.6B-ONNX`
- Best for: known browser-ready provider Best for: reranking retrieved documents by relevance to a query.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.6B`
- Model size: `0.56 GB`
- Disk: `570 MB`
- VRAM: `684 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen3 Reranker 0.6B`, `Qwen3-Reranker-0.6B`, `Qwen3-Reranker-0.6B-ONNX`, `onnx-community/Qwen3-Reranker-0.6B-ONNX`
- Tags: `Reranker`, `Rerankers`, `base_model:Qwen/Qwen3-Reranker-0.6B`, `base_model:quantized:Qwen/Qwen3-Reranker-0.6B`, `license:apache-2.0`, `onnx`, `qwen3`, `region:us`, `reranker`, `text-generation`, `text-ranking`, `transformers.js`

### 8. BGE Reranker v2 M3

- Index: `xlocllm.unit("reranker", "onnx-community/bge-reranker-v2-m3-ONNX")`
- Model ID: `onnx-community/bge-reranker-v2-m3-ONNX`
- Best for: medium transformers model for reranking retrieved documents by relevance to a query; languages: multilingual.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.88 GB`
- Disk: `900 MB`
- VRAM: `1600 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `multilingual`
- Aliases: `bge-reranker-v2-m3`, `reranker-m3`

## translator - Translators

Purpose: machine translation between supported language pairs.
Catalog task: `translation`.
Invoke endpoint: `translate`.

### 1. OPUS MT EN-RU

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-en-ru")`
- Model ID: `Xenova/opus-mt-en-ru`
- Best for: tiny transformers model for machine translation between supported language pairs; languages: en, ru.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.3 GB`
- Disk: `310 MB`
- VRAM: `650 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en, ru`
- Aliases: `opus-en-ru`

### 2. opus mt de en

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-de-en")`
- Model ID: `Xenova/opus-mt-de-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `de, en`
- Aliases: `Xenova/opus-mt-de-en`, `opus mt de en`, `opus-mt-de-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-de-en`, `base_model:quantized:Helsinki-NLP/opus-mt-de-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 3. opus mt de en

- Index: `xlocllm.unit("translator", "onnx-community/opus-mt-de-en")`
- Model ID: `onnx-community/opus-mt-de-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-4.0`
- Languages: `de, en`
- Aliases: `onnx-community/opus-mt-de-en`, `opus mt de en`, `opus-mt-de-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-de-en`, `base_model:quantized:Helsinki-NLP/opus-mt-de-en`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 4. opus mt de fr

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-de-fr")`
- Model ID: `Xenova/opus-mt-de-fr`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `de, fr`
- Aliases: `Xenova/opus-mt-de-fr`, `opus mt de fr`, `opus-mt-de-fr`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-de-fr`, `base_model:quantized:Helsinki-NLP/opus-mt-de-fr`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 5. opus mt en de

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-en-de")`
- Model ID: `Xenova/opus-mt-en-de`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en, de`
- Aliases: `Xenova/opus-mt-en-de`, `opus mt en de`, `opus-mt-en-de`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-de`, `base_model:quantized:Helsinki-NLP/opus-mt-en-de`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 6. opus mt en de

- Index: `xlocllm.unit("translator", "onnx-community/opus-mt-en-de")`
- Model ID: `onnx-community/opus-mt-en-de`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-4.0`
- Languages: `en, de`
- Aliases: `onnx-community/opus-mt-en-de`, `opus mt en de`, `opus-mt-en-de`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-de`, `base_model:quantized:Helsinki-NLP/opus-mt-en-de`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 7. opus mt en es

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-en-es")`
- Model ID: `Xenova/opus-mt-en-es`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en, es`
- Aliases: `Xenova/opus-mt-en-es`, `opus mt en es`, `opus-mt-en-es`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-es`, `base_model:quantized:Helsinki-NLP/opus-mt-en-es`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 8. opus mt en es

- Index: `xlocllm.unit("translator", "onnx-community/opus-mt-en-es")`
- Model ID: `onnx-community/opus-mt-en-es`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-4.0`
- Languages: `en, es`
- Aliases: `onnx-community/opus-mt-en-es`, `opus mt en es`, `opus-mt-en-es`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-es`, `base_model:quantized:Helsinki-NLP/opus-mt-en-es`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 9. opus mt en fr

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-en-fr")`
- Model ID: `Xenova/opus-mt-en-fr`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en, fr`
- Aliases: `Xenova/opus-mt-en-fr`, `opus mt en fr`, `opus-mt-en-fr`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-fr`, `base_model:quantized:Helsinki-NLP/opus-mt-en-fr`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 10. opus mt en fr

- Index: `xlocllm.unit("translator", "onnx-community/opus-mt-en-fr")`
- Model ID: `onnx-community/opus-mt-en-fr`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-4.0`
- Languages: `en, fr`
- Aliases: `onnx-community/opus-mt-en-fr`, `opus mt en fr`, `opus-mt-en-fr`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-fr`, `base_model:quantized:Helsinki-NLP/opus-mt-en-fr`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 11. opus mt en it

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-en-it")`
- Model ID: `Xenova/opus-mt-en-it`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en, it`
- Aliases: `Xenova/opus-mt-en-it`, `opus mt en it`, `opus-mt-en-it`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-it`, `base_model:quantized:Helsinki-NLP/opus-mt-en-it`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 12. opus mt en zh

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-en-zh")`
- Model ID: `Xenova/opus-mt-en-zh`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en, zh`
- Aliases: `Xenova/opus-mt-en-zh`, `opus mt en zh`, `opus-mt-en-zh`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-en-zh`, `base_model:quantized:Helsinki-NLP/opus-mt-en-zh`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 13. opus mt es en

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-es-en")`
- Model ID: `Xenova/opus-mt-es-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `es, en`
- Aliases: `Xenova/opus-mt-es-en`, `opus mt es en`, `opus-mt-es-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-es-en`, `base_model:quantized:Helsinki-NLP/opus-mt-es-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 14. opus mt es en

- Index: `xlocllm.unit("translator", "onnx-community/opus-mt-es-en")`
- Model ID: `onnx-community/opus-mt-es-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-4.0`
- Languages: `es, en`
- Aliases: `onnx-community/opus-mt-es-en`, `opus mt es en`, `opus-mt-es-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-es-en`, `base_model:quantized:Helsinki-NLP/opus-mt-es-en`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 15. opus mt fr de

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-fr-de")`
- Model ID: `Xenova/opus-mt-fr-de`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `fr, de`
- Aliases: `Xenova/opus-mt-fr-de`, `opus mt fr de`, `opus-mt-fr-de`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-fr-de`, `base_model:quantized:Helsinki-NLP/opus-mt-fr-de`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 16. opus mt fr en

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-fr-en")`
- Model ID: `Xenova/opus-mt-fr-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `fr, en`
- Aliases: `Xenova/opus-mt-fr-en`, `opus mt fr en`, `opus-mt-fr-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-fr-en`, `base_model:quantized:Helsinki-NLP/opus-mt-fr-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 17. opus mt fr en

- Index: `xlocllm.unit("translator", "onnx-community/opus-mt-fr-en")`
- Model ID: `onnx-community/opus-mt-fr-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-4.0`
- Languages: `fr, en`
- Aliases: `onnx-community/opus-mt-fr-en`, `opus mt fr en`, `opus-mt-fr-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-fr-en`, `base_model:quantized:Helsinki-NLP/opus-mt-fr-en`, `license:cc-by-4.0`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 18. opus mt it en

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-it-en")`
- Model ID: `Xenova/opus-mt-it-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `it, en`
- Aliases: `Xenova/opus-mt-it-en`, `opus mt it en`, `opus-mt-it-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-it-en`, `base_model:quantized:Helsinki-NLP/opus-mt-it-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 19. opus mt ja en

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-ja-en")`
- Model ID: `Xenova/opus-mt-ja-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `ja, en`
- Aliases: `Xenova/opus-mt-ja-en`, `opus mt ja en`, `opus-mt-ja-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-ja-en`, `base_model:quantized:Helsinki-NLP/opus-mt-ja-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 20. opus mt ko en

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-ko-en")`
- Model ID: `Xenova/opus-mt-ko-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `ko, en`
- Aliases: `Xenova/opus-mt-ko-en`, `opus mt ko en`, `opus-mt-ko-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-ko-en`, `base_model:quantized:Helsinki-NLP/opus-mt-ko-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 21. opus mt ru en

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-ru-en")`
- Model ID: `Xenova/opus-mt-ru-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `ru, en`
- Aliases: `Xenova/opus-mt-ru-en`, `opus mt ru en`, `opus-mt-ru-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-ru-en`, `base_model:quantized:Helsinki-NLP/opus-mt-ru-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 22. opus mt zh en

- Index: `xlocllm.unit("translator", "Xenova/opus-mt-zh-en")`
- Model ID: `Xenova/opus-mt-zh-en`
- Best for: known browser-ready provider Best for: machine translation between supported language pairs.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.31 GB`
- Disk: `320 MB`
- VRAM: `384 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `zh, en`
- Aliases: `Xenova/opus-mt-zh-en`, `opus mt zh en`, `opus-mt-zh-en`
- Tags: `Translation`, `base_model:Helsinki-NLP/opus-mt-zh-en`, `base_model:quantized:Helsinki-NLP/opus-mt-zh-en`, `marian`, `onnx`, `region:us`, `text2text-generation`, `transformers.js`, `translation`

### 23. M2M100 418M

- Index: `xlocllm.unit("translator", "Xenova/m2m100_418M")`
- Model ID: `Xenova/m2m100_418M`
- Best for: medium transformers model for machine translation between supported language pairs; languages: multilingual.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `medium`
- Parameters: `0.418B`
- Model size: `0.88 GB`
- Disk: `900 MB`
- VRAM: `1900 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `multilingual`
- Aliases: `m2m100`, `m2m100-418m`

### 24. NLLB 200 distilled 600M

- Index: `xlocllm.unit("translator", "Xenova/nllb-200-distilled-600M")`
- Model ID: `Xenova/nllb-200-distilled-600M`
- Best for: medium transformers model for machine translation between supported language pairs; languages: multilingual.
- Runtime: `transformers`
- Task: `translation`
- Provider: `Xenova`
- Hardware tier: `medium`
- Parameters: `0.6B`
- Model size: `1.17 GB`
- Disk: `1200 MB`
- VRAM: `2300 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `cc-by-nc-4.0`
- Languages: `multilingual`
- Aliases: `nllb-200`, `nllb`

## tts - TTS

Purpose: text-to-speech synthesis and browser-side voice generation.
Catalog task: `text-to-speech`.
Invoke endpoint: `tts`.

### 1. mms tts deu

- Index: `xlocllm.unit("tts", "Xenova/mms-tts-deu")`
- Model ID: `Xenova/mms-tts-deu`
- Best for: known browser-ready provider Best for: text-to-speech synthesis and browser-side voice generation.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/mms-tts-deu`, `mms tts deu`, `mms-tts-deu`
- Tags: `Audio`, `TTS`, `base_model:facebook/mms-tts-deu`, `base_model:quantized:facebook/mms-tts-deu`, `onnx`, `region:us`, `text-to-audio`, `text-to-speech`, `transformers.js`, `vits`

### 2. mms tts eng

- Index: `xlocllm.unit("tts", "Xenova/mms-tts-eng")`
- Model ID: `Xenova/mms-tts-eng`
- Best for: known browser-ready provider Best for: text-to-speech synthesis and browser-side voice generation.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/mms-tts-eng`, `mms tts eng`, `mms-tts-eng`
- Tags: `Audio`, `TTS`, `base_model:facebook/mms-tts-eng`, `base_model:quantized:facebook/mms-tts-eng`, `onnx`, `region:us`, `text-to-audio`, `text-to-speech`, `transformers.js`, `vits`

### 3. mms tts fra

- Index: `xlocllm.unit("tts", "Xenova/mms-tts-fra")`
- Model ID: `Xenova/mms-tts-fra`
- Best for: known browser-ready provider Best for: text-to-speech synthesis and browser-side voice generation.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/mms-tts-fra`, `mms tts fra`, `mms-tts-fra`
- Tags: `Audio`, `TTS`, `base_model:facebook/mms-tts-fra`, `base_model:quantized:facebook/mms-tts-fra`, `onnx`, `region:us`, `text-to-audio`, `text-to-speech`, `transformers.js`, `vits`

### 4. mms tts rus

- Index: `xlocllm.unit("tts", "Xenova/mms-tts-rus")`
- Model ID: `Xenova/mms-tts-rus`
- Best for: known browser-ready provider Best for: text-to-speech synthesis and browser-side voice generation.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/mms-tts-rus`, `mms tts rus`, `mms-tts-rus`
- Tags: `Audio`, `TTS`, `base_model:facebook/mms-tts-rus`, `base_model:quantized:facebook/mms-tts-rus`, `onnx`, `region:us`, `text-to-audio`, `text-to-speech`, `transformers.js`, `vits`

### 5. mms tts spa

- Index: `xlocllm.unit("tts", "Xenova/mms-tts-spa")`
- Model ID: `Xenova/mms-tts-spa`
- Best for: known browser-ready provider Best for: text-to-speech synthesis and browser-side voice generation.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/mms-tts-spa`, `mms tts spa`, `mms-tts-spa`
- Tags: `Audio`, `TTS`, `base_model:facebook/mms-tts-spa`, `base_model:quantized:facebook/mms-tts-spa`, `onnx`, `region:us`, `text-to-audio`, `text-to-speech`, `transformers.js`, `vits`

### 6. Kokoro 82M

- Index: `xlocllm.unit("tts", "onnx-community/Kokoro-82M-v1.0-ONNX")`
- Model ID: `onnx-community/Kokoro-82M-v1.0-ONNX`
- Best for: tiny transformers model for text-to-speech synthesis and browser-side voice generation; languages: en.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `0.082B`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `450 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `kokoro`, `kokoro-82m`

### 7. SpeechT5 TTS

- Index: `xlocllm.unit("tts", "Xenova/speecht5_tts")`
- Model ID: `Xenova/speecht5_tts`
- Best for: small transformers model for text-to-speech synthesis and browser-side voice generation; languages: en.
- Runtime: `transformers`
- Task: `text-to-speech`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `900 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `en`
- Aliases: `speecht5`

## image-classification - Image Classification

Purpose: image classification and visual tagging.
Catalog task: `image-classification`.
Invoke endpoint: `image.classify`.

### 1. MobileNet V2

- Index: `xlocllm.unit("image-classification", "onnx-community/mobilenet_v2_1.0_224")`
- Model ID: `onnx-community/mobilenet_v2_1.0_224`
- Best for: tiny transformers model for image classification and visual tagging; languages: n/a.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.02 GB`
- Disk: `25 MB`
- VRAM: `160 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `n/a`
- Aliases: `mobilenet-v2`, `mobilenet`

### 2. convnext tiny 224

- Index: `xlocllm.unit("image-classification", "Xenova/convnext-tiny-224")`
- Model ID: `Xenova/convnext-tiny-224`
- Best for: known browser-ready provider Best for: image classification and visual tagging.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.09 GB`
- Disk: `90 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/convnext-tiny-224`, `convnext tiny 224`, `convnext-tiny-224`
- Tags: `Image`, `Image Classification`, `base_model:facebook/convnext-tiny-224`, `base_model:quantized:facebook/convnext-tiny-224`, `convnext`, `image-classification`, `onnx`, `region:us`, `transformers.js`

### 3. mobilenetv4 conv small.e2400 r224 in1k

- Index: `xlocllm.unit("image-classification", "onnx-community/mobilenetv4_conv_small.e2400_r224_in1k")`
- Model ID: `onnx-community/mobilenetv4_conv_small.e2400_r224_in1k`
- Best for: known browser-ready provider Best for: image classification and visual tagging.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.09 GB`
- Disk: `90 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `mobilenetv4-conv-small.e2400-r224-in1k`, `mobilenetv4_conv_small.e2400_r224_in1k`, `onnx-community/mobilenetv4_conv_small.e2400_r224_in1k`
- Tags: `Image`, `Image Classification`, `base_model:quantized:timm/mobilenetv4_conv_small.e2400_r224_in1k`, `base_model:timm/mobilenetv4_conv_small.e2400_r224_in1k`, `mobilenet_v4`, `onnx`, `region:us`, `transformers.js`

### 4. swin tiny patch4 window7 224

- Index: `xlocllm.unit("image-classification", "Xenova/swin-tiny-patch4-window7-224")`
- Model ID: `Xenova/swin-tiny-patch4-window7-224`
- Best for: known browser-ready provider Best for: image classification and visual tagging.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.09 GB`
- Disk: `90 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/swin-tiny-patch4-window7-224`, `swin tiny patch4 window7 224`, `swin-tiny-patch4-window7-224`
- Tags: `Image`, `Image Classification`, `base_model:microsoft/swin-tiny-patch4-window7-224`, `base_model:quantized:microsoft/swin-tiny-patch4-window7-224`, `image-classification`, `onnx`, `region:us`, `swin`, `transformers.js`

### 5. vit base patch16 224 in21k

- Index: `xlocllm.unit("image-classification", "Xenova/vit-base-patch16-224-in21k")`
- Model ID: `Xenova/vit-base-patch16-224-in21k`
- Best for: known browser-ready provider Best for: image classification and visual tagging.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.09 GB`
- Disk: `90 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/vit-base-patch16-224-in21k`, `vit base patch16 224 in21k`, `vit-base-patch16-224-in21k`
- Tags: `Image`, `Image Classification`, `base_model:google/vit-base-patch16-224-in21k`, `base_model:quantized:google/vit-base-patch16-224-in21k`, `image-feature-extraction`, `onnx`, `region:us`, `transformers.js`, `vit`

### 6. ViT base 224

- Index: `xlocllm.unit("image-classification", "Xenova/vit-base-patch16-224")`
- Model ID: `Xenova/vit-base-patch16-224`
- Best for: small transformers model for image classification and visual tagging; languages: n/a.
- Runtime: `transformers`
- Task: `image-classification`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.32 GB`
- Disk: `330 MB`
- VRAM: `700 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `n/a`
- Aliases: `vit-base-224`

## object-detection - Object Detection

Purpose: object detection, bounding boxes, and layout detection models that use detection tasks.
Catalog task: `object-detection`.
Invoke endpoint: `image.detect`.

### 1. detr resnet 50 panoptic

- Index: `xlocllm.unit("object-detection", "Xenova/detr-resnet-50-panoptic")`
- Model ID: `Xenova/detr-resnet-50-panoptic`
- Best for: known browser-ready provider Best for: object detection, bounding boxes, and layout detection models that use detection tasks.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/detr-resnet-50-panoptic`, `detr resnet 50 panoptic`, `detr-resnet-50-panoptic`
- Tags: `Image`, `Object Detection`, `base_model:facebook/detr-resnet-50-panoptic`, `base_model:quantized:facebook/detr-resnet-50-panoptic`, `detr`, `image-segmentation`, `onnx`, `region:us`, `transformers.js`

### 2. rfdetr base

- Index: `xlocllm.unit("object-detection", "onnx-community/rfdetr_base-ONNX")`
- Model ID: `onnx-community/rfdetr_base-ONNX`
- Best for: known browser-ready provider Best for: object detection, bounding boxes, and layout detection models that use detection tasks.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `onnx-community/rfdetr_base-ONNX`, `rfdetr-base`, `rfdetr_base`, `rfdetr_base-ONNX`
- Tags: `Image`, `Object Detection`, `license:apache-2.0`, `object-detection`, `onnx`, `region:us`, `rf_detr`, `transformers.js`

### 3. rtdetr r18vd

- Index: `xlocllm.unit("object-detection", "onnx-community/rtdetr_r18vd")`
- Model ID: `onnx-community/rtdetr_r18vd`
- Best for: known browser-ready provider Best for: object detection, bounding boxes, and layout detection models that use detection tasks.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `onnx-community/rtdetr_r18vd`, `rtdetr-r18vd`, `rtdetr_r18vd`
- Tags: `Image`, `Object Detection`, `base_model:PekingU/rtdetr_r18vd`, `base_model:quantized:PekingU/rtdetr_r18vd`, `object-detection`, `onnx`, `region:us`, `rt_detr`, `transformers.js`

### 4. rtdetr r50vd coco o365

- Index: `xlocllm.unit("object-detection", "onnx-community/rtdetr_r50vd_coco_o365")`
- Model ID: `onnx-community/rtdetr_r50vd_coco_o365`
- Best for: known browser-ready provider Best for: object detection, bounding boxes, and layout detection models that use detection tasks.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `onnx-community/rtdetr_r50vd_coco_o365`, `rtdetr-r50vd-coco-o365`, `rtdetr_r50vd_coco_o365`
- Tags: `Image`, `Object Detection`, `base_model:PekingU/rtdetr_r50vd_coco_o365`, `base_model:quantized:PekingU/rtdetr_r50vd_coco_o365`, `object-detection`, `onnx`, `region:us`, `rt_detr`, `transformers.js`

### 5. rtdetr v2 r18vd

- Index: `xlocllm.unit("object-detection", "onnx-community/rtdetr_v2_r18vd-ONNX")`
- Model ID: `onnx-community/rtdetr_v2_r18vd-ONNX`
- Best for: known browser-ready provider Best for: object detection, bounding boxes, and layout detection models that use detection tasks.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `onnx-community/rtdetr_v2_r18vd-ONNX`, `rtdetr-v2-r18vd`, `rtdetr_v2_r18vd`, `rtdetr_v2_r18vd-ONNX`
- Tags: `Image`, `Object Detection`, `base_model:PekingU/rtdetr_v2_r18vd`, `base_model:quantized:PekingU/rtdetr_v2_r18vd`, `license:apache-2.0`, `object-detection`, `onnx`, `region:us`, `rt_detr_v2`, `transformers.js`

### 6. yolo realtime

- Index: `xlocllm.unit("object-detection", "kurnie/yolo-realtime")`
- Model ID: `kurnie/yolo-realtime`
- Best for: ONNX/WebGPU artifact marker Best for: object detection, bounding boxes, and layout detection models that use detection tasks.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `kurnie`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `gpl-3.0`
- Languages: `universal`
- Aliases: `kurnie/yolo-realtime`, `yolo realtime`, `yolo-realtime`
- Tags: `Image`, `Object Detection`, `license:gpl-3.0`, `object-detection`, `onnx`, `region:us`, `transformers.js`, `yolov8`

### 7. yolov10m doclaynet

- Index: `xlocllm.unit("object-detection", "Oblix/yolov10m-doclaynet_ONNX_document-layout-analysis")`
- Model ID: `Oblix/yolov10m-doclaynet_ONNX_document-layout-analysis`
- Best for: ONNX/WebGPU artifact marker Best for: object detection, bounding boxes, and layout detection models that use detection tasks.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Oblix`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Oblix/yolov10m-doclaynet_ONNX_document-layout-analysis`, `yolov10m doclaynet`, `yolov10m-doclaynet`, `yolov10m-doclaynet_ONNX_document-layout-analysis`
- Tags: `Image`, `Object Detection`, `object-detection`, `onnx`, `region:us`, `transformers.js`, `yolov10`

### 8. YOLOS tiny

- Index: `xlocllm.unit("object-detection", "Xenova/yolos-tiny")`
- Model ID: `Xenova/yolos-tiny`
- Best for: tiny transformers model for object detection, bounding boxes, and layout detection models that use detection tasks; languages: n/a.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.11 GB`
- Disk: `110 MB`
- VRAM: `350 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `n/a`
- Aliases: `yolos-tiny`

### 9. DETR ResNet 50

- Index: `xlocllm.unit("object-detection", "Xenova/detr-resnet-50")`
- Model ID: `Xenova/detr-resnet-50`
- Best for: medium transformers model for object detection, bounding boxes, and layout detection models that use detection tasks; languages: n/a.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Xenova`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.17 GB`
- Disk: `170 MB`
- VRAM: `900 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `n/a`
- Aliases: `detr-resnet-50`, `detr`

## image-segmentation - Image segmentation/background removing

Purpose: image segmentation, portrait matting, and background removal.
Catalog task: `image-segmentation`.
Invoke endpoint: `image.segment`.

### 1. MODNet portrait matting

- Index: `xlocllm.unit("image-segmentation", "Xenova/modnet")`
- Model ID: `Xenova/modnet`
- Best for: tiny transformers model for image segmentation, portrait matting, and background removal; languages: n/a.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.03 GB`
- Disk: `30 MB`
- VRAM: `180 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `n/a`
- Aliases: `modnet`

### 2. BiRefNet

- Index: `xlocllm.unit("image-segmentation", "onnx-community/BiRefNet-ONNX")`
- Model ID: `onnx-community/BiRefNet-ONNX`
- Best for: known browser-ready provider Best for: image segmentation, portrait matting, and background removal.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `universal`
- Aliases: `BiRefNet`, `BiRefNet-ONNX`, `onnx-community/BiRefNet-ONNX`
- Tags: `Camouflaged Object Detection`, `Dichotomous Image Segmentation`, `Image`, `Image Segmentation`, `Salient Object Detection`, `background-removal`, `base_model:ZhengPeng7/BiRefNet`, `base_model:quantized:ZhengPeng7/BiRefNet`, `birefnet`, `image-segmentation`, `license:mit`, `mask-generation`, `onnx`, `transformers.js`

### 3. birefnet lite 512

- Index: `xlocllm.unit("image-segmentation", "studioludens/birefnet-lite-512")`
- Model ID: `studioludens/birefnet-lite-512`
- Best for: ONNX/WebGPU artifact marker Best for: image segmentation, portrait matting, and background removal.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `studioludens`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `universal`
- Aliases: `birefnet lite 512`, `birefnet-lite-512`, `studioludens/birefnet-lite-512`
- Tags: `Image`, `Image Segmentation`, `alpha-matting`, `background-removal`, `birefnet`, `dichotomous-image-segmentation`, `foreground-extraction`, `image-matting`, `matting`, `onnx`, `salient-object-detection`, `swin`, `transformers.js`, `webgpu`

### 4. BiRefNet portrait

- Index: `xlocllm.unit("image-segmentation", "onnx-community/BiRefNet-portrait-ONNX")`
- Model ID: `onnx-community/BiRefNet-portrait-ONNX`
- Best for: known browser-ready provider Best for: image segmentation, portrait matting, and background removal.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `universal`
- Aliases: `BiRefNet portrait`, `BiRefNet-portrait`, `BiRefNet-portrait-ONNX`, `onnx-community/BiRefNet-portrait-ONNX`
- Tags: `Camouflaged Object Detection`, `Dichotomous Image Segmentation`, `Image`, `Image Segmentation`, `Salient Object Detection`, `background-removal`, `base_model:ZhengPeng7/BiRefNet-portrait`, `base_model:quantized:ZhengPeng7/BiRefNet-portrait`, `birefnet`, `image-segmentation`, `license:mit`, `mask-generation`, `onnx`, `transformers.js`

### 5. ormbg

- Index: `xlocllm.unit("image-segmentation", "onnx-community/ormbg-ONNX")`
- Model ID: `onnx-community/ormbg-ONNX`
- Best for: known browser-ready provider Best for: image segmentation, portrait matting, and background removal.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `onnx-community/ormbg-ONNX`, `ormbg`, `ormbg-ONNX`
- Tags: `Image`, `Image Segmentation`, `background-removal`, `base_model:quantized:schirrmacher/ormbg`, `base_model:schirrmacher/ormbg`, `image-segmentation`, `isnet`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`

### 6. RMBG 1.4

- Index: `xlocllm.unit("image-segmentation", "SolonD/RMBG-1.4")`
- Model ID: `SolonD/RMBG-1.4`
- Best for: ONNX/WebGPU artifact marker Best for: image segmentation, portrait matting, and background removal.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `SolonD`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `other`
- Languages: `universal`
- Aliases: `RMBG 1.4`, `RMBG-1.4`, `SolonD/RMBG-1.4`
- Tags: `Image`, `Image Segmentation`, `Pytorch`, `SegformerForSemanticSegmentation`, `background`, `background-removal`, `image-segmentation`, `legal liability`, `onnx`, `pytorch`, `remove background`, `safetensors`, `transformers`, `vision`

### 7. U 2 Net

- Index: `xlocllm.unit("image-segmentation", "BritishWerewolf/U-2-Net")`
- Model ID: `BritishWerewolf/U-2-Net`
- Best for: ONNX/WebGPU artifact marker Best for: image segmentation, portrait matting, and background removal.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `BritishWerewolf`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `BritishWerewolf/U-2-Net`, `U 2 Net`, `U-2-Net`
- Tags: `Image`, `Image Segmentation`, `background-removal`, `en`, `endpoints_compatible`, `image-segmentation`, `license:apache-2.0`, `mask-generation`, `onnx`, `portrait-matting`, `transformers`, `transformers.js`, `u2net`, `vision`

### 8. U 2 Netp

- Index: `xlocllm.unit("image-segmentation", "BritishWerewolf/U-2-Netp")`
- Model ID: `BritishWerewolf/U-2-Netp`
- Best for: ONNX/WebGPU artifact marker Best for: image segmentation, portrait matting, and background removal.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `BritishWerewolf`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `BritishWerewolf/U-2-Netp`, `U 2 Netp`, `U-2-Netp`
- Tags: `Image`, `Image Segmentation`, `background-removal`, `en`, `endpoints_compatible`, `image-segmentation`, `license:apache-2.0`, `mask-generation`, `onnx`, `portrait-matting`, `transformers`, `transformers.js`, `u2net`, `vision`

### 9. BEN2 background removal

- Index: `xlocllm.unit("image-segmentation", "onnx-community/BEN2-ONNX")`
- Model ID: `onnx-community/BEN2-ONNX`
- Best for: medium transformers model for image segmentation, portrait matting, and background removal; languages: n/a.
- Runtime: `transformers`
- Task: `image-segmentation`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.66 GB`
- Disk: `680 MB`
- VRAM: `1300 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `n/a`
- Aliases: `ben2`, `background-removal`

## depth-estimation - Depth estimator

Purpose: monocular depth maps and relative scene depth estimation.
Catalog task: `depth-estimation`.
Invoke endpoint: `depth`.

### 1. depth anything base hf

- Index: `xlocllm.unit("depth-estimation", "Xenova/depth-anything-base-hf")`
- Model ID: `Xenova/depth-anything-base-hf`
- Best for: known browser-ready provider Best for: monocular depth maps and relative scene depth estimation.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/depth-anything-base-hf`, `depth anything base hf`, `depth-anything-base-hf`
- Tags: `Depth`, `Image`, `base_model:LiheYoung/depth-anything-base-hf`, `base_model:quantized:LiheYoung/depth-anything-base-hf`, `depth-estimation`, `depth_anything`, `onnx`, `region:us`, `transformers.js`

### 2. depth anything large hf

- Index: `xlocllm.unit("depth-estimation", "Xenova/depth-anything-large-hf")`
- Model ID: `Xenova/depth-anything-large-hf`
- Best for: known browser-ready provider Best for: monocular depth maps and relative scene depth estimation.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/depth-anything-large-hf`, `depth anything large hf`, `depth-anything-large-hf`
- Tags: `Depth`, `Image`, `base_model:LiheYoung/depth-anything-large-hf`, `base_model:quantized:LiheYoung/depth-anything-large-hf`, `depth-estimation`, `depth_anything`, `onnx`, `region:us`, `transformers.js`

### 3. depth anything small hf

- Index: `xlocllm.unit("depth-estimation", "Xenova/depth-anything-small-hf")`
- Model ID: `Xenova/depth-anything-small-hf`
- Best for: known browser-ready provider Best for: monocular depth maps and relative scene depth estimation.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/depth-anything-small-hf`, `depth anything small hf`, `depth-anything-small-hf`
- Tags: `Depth`, `Image`, `base_model:LiheYoung/depth-anything-small-hf`, `base_model:quantized:LiheYoung/depth-anything-small-hf`, `depth-estimation`, `depth_anything`, `onnx`, `region:us`, `transformers.js`

### 4. depth anything v2 base

- Index: `xlocllm.unit("depth-estimation", "onnx-community/depth-anything-v2-base")`
- Model ID: `onnx-community/depth-anything-v2-base`
- Best for: known browser-ready provider Best for: monocular depth maps and relative scene depth estimation.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-nc-4.0`
- Languages: `universal`
- Aliases: `depth anything v2 base`, `depth-anything-v2-base`, `onnx-community/depth-anything-v2-base`
- Tags: `Depth`, `Image`, `base_model:depth-anything/Depth-Anything-V2-Base`, `base_model:quantized:depth-anything/Depth-Anything-V2-Base`, `depth-estimation`, `depth_anything`, `license:cc-by-nc-4.0`, `onnx`, `region:us`, `transformers.js`

### 5. depth anything v2 large

- Index: `xlocllm.unit("depth-estimation", "onnx-community/depth-anything-v2-large-ONNX")`
- Model ID: `onnx-community/depth-anything-v2-large-ONNX`
- Best for: known browser-ready provider Best for: monocular depth maps and relative scene depth estimation.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `cc-by-nc-4.0`
- Languages: `universal`
- Aliases: `depth anything v2 large`, `depth-anything-v2-large`, `depth-anything-v2-large-ONNX`, `onnx-community/depth-anything-v2-large-ONNX`
- Tags: `Depth`, `Image`, `base_model:depth-anything/Depth-Anything-V2-Large`, `base_model:quantized:depth-anything/Depth-Anything-V2-Large`, `depth-estimation`, `depth_anything`, `license:cc-by-nc-4.0`, `onnx`, `region:us`, `transformers.js`

### 6. depth anything v2 small

- Index: `xlocllm.unit("depth-estimation", "onnx-community/depth-anything-v2-small-ONNX")`
- Model ID: `onnx-community/depth-anything-v2-small-ONNX`
- Best for: known browser-ready provider Best for: monocular depth maps and relative scene depth estimation.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.21 GB`
- Disk: `220 MB`
- VRAM: `264 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `depth anything v2 small`, `depth-anything-v2-small`, `depth-anything-v2-small-ONNX`, `onnx-community/depth-anything-v2-small-ONNX`
- Tags: `Depth`, `Image`, `base_model:depth-anything/Depth-Anything-V2-Small`, `base_model:quantized:depth-anything/Depth-Anything-V2-Small`, `depth-estimation`, `depth_anything`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`

### 7. Depth Anything V2 small

- Index: `xlocllm.unit("depth-estimation", "onnx-community/depth-anything-v2-small")`
- Model ID: `onnx-community/depth-anything-v2-small`
- Best for: small transformers model for monocular depth maps and relative scene depth estimation; languages: n/a.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.3 GB`
- Disk: `310 MB`
- VRAM: `700 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `n/a`
- Aliases: `depth-anything-v2-small`, `depth-anything-small`

### 8. DPT hybrid MiDaS

- Index: `xlocllm.unit("depth-estimation", "Xenova/dpt-hybrid-midas")`
- Model ID: `Xenova/dpt-hybrid-midas`
- Best for: medium transformers model for monocular depth maps and relative scene depth estimation; languages: n/a.
- Runtime: `transformers`
- Task: `depth-estimation`
- Provider: `Xenova`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.47 GB`
- Disk: `480 MB`
- VRAM: `950 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `n/a`
- Aliases: `dpt-hybrid-midas`, `midas`

## vlm - VLM/image-to-text

Purpose: image captioning and image-to-text style vision-language tasks.
Catalog task: `image-to-text`.
Invoke endpoint: `image-to-text`.

### 1. SmolVLM 256M Instruct

- Index: `xlocllm.unit("vlm", "HuggingFaceTB/SmolVLM-256M-Instruct")`
- Model ID: `HuggingFaceTB/SmolVLM-256M-Instruct`
- Best for: ONNX/WebGPU artifact marker Best for: image captioning and image-to-text style vision-language tasks.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `HuggingFaceTB`
- Hardware tier: `tiny`
- Parameters: `0.256B`
- Model size: `0.24 GB`
- Disk: `243 MB`
- VRAM: `291 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `HuggingFaceTB/SmolVLM-256M-Instruct`, `SmolVLM 256M Instruct`, `SmolVLM-256M-Instruct`
- Tags: `VLM`, `arxiv:2504.05299`, `base_model:HuggingFaceTB/SmolLM2-135M-Instruct`, `base_model:quantized:HuggingFaceTB/SmolLM2-135M-Instruct`, `conversational`, `dataset:HuggingFaceM4/Docmatix`, `dataset:HuggingFaceM4/the_cauldron`, `en`, `idefics3`, `image-text-to-text`, `onnx`, `safetensors`, `transformers`

### 2. Florence 2 base

- Index: `xlocllm.unit("vlm", "onnx-community/Florence-2-base")`
- Model ID: `onnx-community/Florence-2-base`
- Best for: known browser-ready provider Best for: image captioning and image-to-text style vision-language tasks.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.63 GB`
- Disk: `650 MB`
- VRAM: `780 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `en`
- Aliases: `Florence 2 base`, `Florence-2-base`, `onnx-community/Florence-2-base`
- Tags: `VLM`, `base_model:microsoft/Florence-2-base`, `base_model:quantized:microsoft/Florence-2-base`, `florence2`, `image-text-to-text`, `image-to-text`, `license:mit`, `onnx`, `region:us`, `text-generation`, `text2text-generation`, `transformers.js`, `vision`

### 3. Florence 2 large

- Index: `xlocllm.unit("vlm", "onnx-community/Florence-2-large")`
- Model ID: `onnx-community/Florence-2-large`
- Best for: known browser-ready provider Best for: image captioning and image-to-text style vision-language tasks.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.63 GB`
- Disk: `650 MB`
- VRAM: `780 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `en`
- Aliases: `Florence 2 large`, `Florence-2-large`, `onnx-community/Florence-2-large`
- Tags: `VLM`, `base_model:microsoft/Florence-2-large`, `base_model:quantized:microsoft/Florence-2-large`, `florence2`, `image-text-to-text`, `image-to-text`, `license:mit`, `onnx`, `region:us`, `text-generation`, `text2text-generation`, `transformers.js`, `vision`

### 4. Florence 2 large ft

- Index: `xlocllm.unit("vlm", "onnx-community/Florence-2-large-ft")`
- Model ID: `onnx-community/Florence-2-large-ft`
- Best for: known browser-ready provider Best for: image captioning and image-to-text style vision-language tasks.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.63 GB`
- Disk: `650 MB`
- VRAM: `780 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `en`
- Aliases: `Florence 2 large ft`, `Florence-2-large-ft`, `onnx-community/Florence-2-large-ft`
- Tags: `VLM`, `base_model:microsoft/Florence-2-large-ft`, `base_model:quantized:microsoft/Florence-2-large-ft`, `florence2`, `image-text-to-text`, `image-to-text`, `license:mit`, `onnx`, `region:us`, `text-generation`, `text2text-generation`, `transformers.js`, `vision`

### 5. ViT GPT-2 image captioning

- Index: `xlocllm.unit("vlm", "Xenova/vit-gpt2-image-captioning")`
- Model ID: `Xenova/vit-gpt2-image-captioning`
- Best for: small transformers model for image captioning and image-to-text style vision-language tasks; languages: en.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.45 GB`
- Disk: `460 MB`
- VRAM: `950 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `vit-gpt2-captioning`, `image-captioning`

### 6. FastVLM 0.5B

- Index: `xlocllm.unit("vlm", "onnx-community/FastVLM-0.5B-ONNX")`
- Model ID: `onnx-community/FastVLM-0.5B-ONNX`
- Best for: known browser-ready provider Best for: image captioning and image-to-text style vision-language tasks.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `0.5B`
- Model size: `0.46 GB`
- Disk: `475 MB`
- VRAM: `570 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apple-amlr`
- Languages: `en`
- Aliases: `FastVLM 0.5B`, `FastVLM-0.5B`, `FastVLM-0.5B-ONNX`, `onnx-community/FastVLM-0.5B-ONNX`
- Tags: `VLM`, `arxiv:2412.13303`, `base_model:apple/FastVLM-0.5B`, `base_model:quantized:apple/FastVLM-0.5B`, `conversational`, `fastvlm`, `image-text-to-text`, `license:apple-amlr`, `llava_qwen2`, `onnx`, `region:us`, `text-generation`, `transformers.js`

### 7. Florence 2 base finetuned

- Index: `xlocllm.unit("vlm", "onnx-community/Florence-2-base-ft")`
- Model ID: `onnx-community/Florence-2-base-ft`
- Best for: medium transformers model for image captioning and image-to-text style vision-language tasks; languages: en.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.76 GB`
- Disk: `780 MB`
- VRAM: `1500 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `en`
- Aliases: `florence-2-base-ft`, `florence-base`

### 8. Qwen2 VL 2B Instruct

- Index: `xlocllm.unit("vlm", "onnx-community/Qwen2-VL-2B-Instruct")`
- Model ID: `onnx-community/Qwen2-VL-2B-Instruct`
- Best for: known browser-ready provider Best for: image captioning and image-to-text style vision-language tasks.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `medium`
- Parameters: `2.0B`
- Model size: `1.86 GB`
- Disk: `1900 MB`
- VRAM: `2280 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `Qwen2 VL 2B Instruct`, `Qwen2-VL-2B-Instruct`, `onnx-community/Qwen2-VL-2B-Instruct`
- Tags: `VLM`, `base_model:Qwen/Qwen2-VL-2B-Instruct`, `base_model:quantized:Qwen/Qwen2-VL-2B-Instruct`, `conversational`, `image-text-to-text`, `license:apache-2.0`, `onnx`, `qwen2_vl`, `region:us`, `transformers.js`

## asr - ASR

Purpose: speech-to-text transcription.
Catalog task: `automatic-speech-recognition`.
Invoke endpoint: `asr`.

### 1. Whisper tiny multilingual

- Index: `xlocllm.unit("asr", "Xenova/whisper-tiny")`
- Model ID: `Xenova/whisper-tiny`
- Best for: tiny transformers model for speech-to-text transcription; languages: multilingual.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.08 GB`
- Disk: `80 MB`
- VRAM: `250 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `multilingual`
- Aliases: `whisper-tiny`

### 2. whisper base

- Index: `xlocllm.unit("asr", "Xenova/whisper-base")`
- Model ID: `Xenova/whisper-base`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `Xenova/whisper-base`, `whisper base`, `whisper-base`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-base`, `base_model:quantized:openai/whisper-base`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 3. whisper base.en

- Index: `xlocllm.unit("asr", "Xenova/whisper-base.en")`
- Model ID: `Xenova/whisper-base.en`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `Xenova/whisper-base.en`, `whisper base.en`, `whisper-base.en`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-base.en`, `base_model:quantized:openai/whisper-base.en`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 4. whisper large

- Index: `xlocllm.unit("asr", "Xenova/whisper-large")`
- Model ID: `Xenova/whisper-large`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `Xenova/whisper-large`, `whisper large`, `whisper-large`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-large`, `base_model:quantized:openai/whisper-large`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 5. whisper large v2

- Index: `xlocllm.unit("asr", "Xenova/whisper-large-v2")`
- Model ID: `Xenova/whisper-large-v2`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/whisper-large-v2`, `whisper large v2`, `whisper-large-v2`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-large-v2`, `base_model:quantized:openai/whisper-large-v2`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 6. whisper large v3

- Index: `xlocllm.unit("asr", "Xenova/whisper-large-v3")`
- Model ID: `Xenova/whisper-large-v3`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `Xenova/whisper-large-v3`, `whisper large v3`, `whisper-large-v3`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-large-v3`, `base_model:quantized:openai/whisper-large-v3`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 7. whisper medium

- Index: `xlocllm.unit("asr", "Xenova/whisper-medium")`
- Model ID: `Xenova/whisper-medium`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `Xenova/whisper-medium`, `whisper medium`, `whisper-medium`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-medium`, `base_model:quantized:openai/whisper-medium`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 8. whisper medium.en

- Index: `xlocllm.unit("asr", "Xenova/whisper-medium.en")`
- Model ID: `Xenova/whisper-medium.en`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `Xenova/whisper-medium.en`, `whisper medium.en`, `whisper-medium.en`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-medium.en`, `base_model:quantized:openai/whisper-medium.en`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 9. whisper small

- Index: `xlocllm.unit("asr", "Xenova/whisper-small")`
- Model ID: `Xenova/whisper-small`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `Xenova/whisper-small`, `whisper small`, `whisper-small`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-small`, `base_model:quantized:openai/whisper-small`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 10. whisper small.en

- Index: `xlocllm.unit("asr", "Xenova/whisper-small.en")`
- Model ID: `Xenova/whisper-small.en`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `Xenova/whisper-small.en`, `whisper small.en`, `whisper-small.en`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-small.en`, `base_model:quantized:openai/whisper-small.en`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 11. whisper tiny

- Index: `xlocllm.unit("asr", "onnx-community/whisper-tiny")`
- Model ID: `onnx-community/whisper-tiny`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `onnx-community/whisper-tiny`, `whisper tiny`, `whisper-tiny`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-tiny`, `base_model:quantized:openai/whisper-tiny`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 12. whisper tiny.en

- Index: `xlocllm.unit("asr", "onnx-community/whisper-tiny.en")`
- Model ID: `onnx-community/whisper-tiny.en`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `onnx-community/whisper-tiny.en`, `whisper tiny.en`, `whisper-tiny.en`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-tiny.en`, `base_model:quantized:openai/whisper-tiny.en`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 13. whisper tiny.en

- Index: `xlocllm.unit("asr", "Xenova/whisper-tiny.en")`
- Model ID: `Xenova/whisper-tiny.en`
- Best for: known browser-ready provider Best for: speech-to-text transcription.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.34 GB`
- Disk: `350 MB`
- VRAM: `420 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `Xenova/whisper-tiny.en`, `whisper tiny.en`, `whisper-tiny.en`
- Tags: `ASR`, `Audio`, `automatic-speech-recognition`, `base_model:openai/whisper-tiny.en`, `base_model:quantized:openai/whisper-tiny.en`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `whisper`

### 14. Whisper base multilingual

- Index: `xlocllm.unit("asr", "onnx-community/whisper-base")`
- Model ID: `onnx-community/whisper-base`
- Best for: small transformers model for speech-to-text transcription; languages: multilingual.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.14 GB`
- Disk: `145 MB`
- VRAM: `550 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `multilingual`
- Aliases: `whisper-base`

### 15. Whisper large v3 turbo

- Index: `xlocllm.unit("asr", "onnx-community/whisper-large-v3-turbo")`
- Model ID: `onnx-community/whisper-large-v3-turbo`
- Best for: large transformers model for speech-to-text transcription; languages: multilingual.
- Runtime: `transformers`
- Task: `automatic-speech-recognition`
- Provider: `onnx-community`
- Hardware tier: `large`
- Parameters: `n/a`
- Model size: `1.56 GB`
- Disk: `1600 MB`
- VRAM: `3600 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `multilingual`
- Aliases: `whisper-large-v3-turbo`

## zero-shot-image - Zero-shot-image

Purpose: zero-shot image classification against user-provided labels.
Catalog task: `zero-shot-image-classification`.
Invoke endpoint: `zero-shot-image`.

### 1. CLIP ViT base patch32

- Index: `xlocllm.unit("zero-shot-image", "Xenova/clip-vit-base-patch32")`
- Model ID: `Xenova/clip-vit-base-patch32`
- Best for: small transformers model for zero-shot image classification against user-provided labels; languages: en.
- Runtime: `transformers`
- Task: `zero-shot-image-classification`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.33 GB`
- Disk: `340 MB`
- VRAM: `750 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `en`
- Aliases: `clip-vit-base-patch32`, `clip-base`

### 2. SigLIP base 224

- Index: `xlocllm.unit("zero-shot-image", "Xenova/siglip-base-patch16-224")`
- Model ID: `Xenova/siglip-base-patch16-224`
- Best for: medium transformers model for zero-shot image classification against user-provided labels; languages: en.
- Runtime: `transformers`
- Task: `zero-shot-image-classification`
- Provider: `Xenova`
- Hardware tier: `medium`
- Parameters: `n/a`
- Model size: `0.51 GB`
- Disk: `520 MB`
- VRAM: `1100 MB`
- DType: `q8`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `siglip-base-224`, `siglip`

## language-id - Language identification

Purpose: spoken language identification from audio.
Catalog task: `audio-classification`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. mms lid 126

- Index: `xlocllm.unit("language-id", "Xenova/mms-lid-126")`
- Model ID: `Xenova/mms-lid-126`
- Best for: known browser-ready provider Best for: spoken language identification from audio.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/mms-lid-126`, `mms lid 126`, `mms-lid-126`
- Tags: `Audio`, `Language ID`, `audio-classification`, `base_model:facebook/mms-lid-126`, `base_model:quantized:facebook/mms-lid-126`, `mms`, `onnx`, `region:us`, `transformers.js`, `wav2vec2`

### 2. mms lid 256

- Index: `xlocllm.unit("language-id", "Xenova/mms-lid-256")`
- Model ID: `Xenova/mms-lid-256`
- Best for: known browser-ready provider Best for: spoken language identification from audio.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/mms-lid-256`, `mms lid 256`, `mms-lid-256`
- Tags: `Audio`, `Language ID`, `audio-classification`, `base_model:facebook/mms-lid-256`, `base_model:quantized:facebook/mms-lid-256`, `mms`, `onnx`, `region:us`, `transformers.js`, `wav2vec2`

### 3. mms lid 4017

- Index: `xlocllm.unit("language-id", "Xenova/mms-lid-4017")`
- Model ID: `Xenova/mms-lid-4017`
- Best for: known browser-ready provider Best for: spoken language identification from audio.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/mms-lid-4017`, `mms lid 4017`, `mms-lid-4017`
- Tags: `Audio`, `Language ID`, `audio-classification`, `base_model:facebook/mms-lid-4017`, `base_model:quantized:facebook/mms-lid-4017`, `mms`, `onnx`, `region:us`, `transformers.js`, `wav2vec2`

## audio-classification - Audio classification

Purpose: audio tagging and sound classification.
Catalog task: `audio-classification`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. ast finetuned audioset 10 10 0.4593

- Index: `xlocllm.unit("audio-classification", "Xenova/ast-finetuned-audioset-10-10-0.4593")`
- Model ID: `Xenova/ast-finetuned-audioset-10-10-0.4593`
- Best for: known browser-ready provider Best for: audio tagging and sound classification.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/ast-finetuned-audioset-10-10-0.4593`, `ast finetuned audioset 10 10 0.4593`, `ast-finetuned-audioset-10-10-0.4593`
- Tags: `Audio`, `Audio Classification`, `audio-classification`, `audio-spectrogram-transformer`, `base_model:MIT/ast-finetuned-audioset-10-10-0.4593`, `base_model:quantized:MIT/ast-finetuned-audioset-10-10-0.4593`, `onnx`, `region:us`, `transformers.js`

### 2. clap htsat unfused

- Index: `xlocllm.unit("audio-classification", "Xenova/clap-htsat-unfused")`
- Model ID: `Xenova/clap-htsat-unfused`
- Best for: known browser-ready provider Best for: audio tagging and sound classification.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/clap-htsat-unfused`, `clap htsat unfused`, `clap-htsat-unfused`
- Tags: `Audio`, `Audio Classification`, `base_model:laion/clap-htsat-unfused`, `base_model:quantized:laion/clap-htsat-unfused`, `clap`, `feature-extraction`, `onnx`, `region:us`, `transformers.js`, `zero-shot-audio-classification`

### 3. wav2vec2 large xlsr 53 gender recognition librispeech

- Index: `xlocllm.unit("audio-classification", "Xenova/wav2vec2-large-xlsr-53-gender-recognition-librispeech")`
- Model ID: `Xenova/wav2vec2-large-xlsr-53-gender-recognition-librispeech`
- Best for: known browser-ready provider Best for: audio tagging and sound classification.
- Runtime: `transformers`
- Task: `audio-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/wav2vec2-large-xlsr-53-gender-recognition-librispeech`, `wav2vec2 large xlsr 53 gender recognition librispeech`, `wav2vec2-large-xlsr-53-gender-recognition-librispeech`
- Tags: `Audio`, `Audio Classification`, `audio-classification`, `base_model:alefiury/wav2vec2-large-xlsr-53-gender-recognition-librispeech`, `base_model:quantized:alefiury/wav2vec2-large-xlsr-53-gender-recognition-librispeech`, `onnx`, `region:us`, `transformers.js`, `wav2vec2`

## ocr - OCR/text recognition

Purpose: OCR and image-to-text recognition models.
Catalog task: `image-to-text`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. manga ocr base

- Index: `xlocllm.unit("ocr", "onnx-community/manga-ocr-base-ONNX")`
- Model ID: `onnx-community/manga-ocr-base-ONNX`
- Best for: known browser-ready provider Best for: OCR and image-to-text recognition models.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `manga ocr base`, `manga-ocr-base`, `manga-ocr-base-ONNX`, `onnx-community/manga-ocr-base-ONNX`
- Tags: `OCR`, `base_model:kha-white/manga-ocr-base`, `base_model:quantized:kha-white/manga-ocr-base`, `dataset:manga109s`, `image-text-to-text`, `image-to-text`, `ja`, `license:apache-2.0`, `onnx`, `region:us`, `transformers.js`, `vision-encoder-decoder`

### 2. mgp str base

- Index: `xlocllm.unit("ocr", "onnx-community/mgp-str-base")`
- Model ID: `onnx-community/mgp-str-base`
- Best for: known browser-ready provider Best for: OCR and image-to-text recognition models.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `mgp str base`, `mgp-str-base`, `onnx-community/mgp-str-base`
- Tags: `OCR`, `base_model:alibaba-damo/mgp-str-base`, `base_model:quantized:alibaba-damo/mgp-str-base`, `image-to-text`, `mgp-str`, `ocr`, `onnx`, `region:us`, `transformers.js`

### 3. TexTeller

- Index: `xlocllm.unit("ocr", "onnx-community/TexTeller-ONNX")`
- Model ID: `onnx-community/TexTeller-ONNX`
- Best for: known browser-ready provider Best for: OCR and image-to-text recognition models.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `TexTeller`, `TexTeller-ONNX`, `onnx-community/TexTeller-ONNX`
- Tags: `OCR`, `base_model:OleehyO/TexTeller`, `base_model:quantized:OleehyO/TexTeller`, `dataset:OleehyO/latex-formulas`, `image to latex`, `image-text-to-text`, `image-to-text`, `license:apache-2.0`, `ocr`, `onnx`, `region:us`, `transformers.js`, `vision-encoder-decoder`

### 4. trocr base stage1

- Index: `xlocllm.unit("ocr", "onnx-community/trocr-base-stage1-ONNX")`
- Model ID: `onnx-community/trocr-base-stage1-ONNX`
- Best for: known browser-ready provider Best for: OCR and image-to-text recognition models.
- Runtime: `transformers`
- Task: `image-to-text`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `onnx-community/trocr-base-stage1-ONNX`, `trocr base stage1`, `trocr-base-stage1`, `trocr-base-stage1-ONNX`
- Tags: `OCR`, `base_model:microsoft/trocr-base-stage1`, `base_model:quantized:microsoft/trocr-base-stage1`, `image-text-to-text`, `onnx`, `region:us`, `transformers.js`, `vision-encoder-decoder`

## document-layout - Document layout

Purpose: document layout analysis and page element detection.
Catalog task: `object-detection`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. yolov10b doclaynet

- Index: `xlocllm.unit("document-layout", "Oblix/yolov10b-doclaynet_ONNX_document-layout-analysis")`
- Model ID: `Oblix/yolov10b-doclaynet_ONNX_document-layout-analysis`
- Best for: ONNX/WebGPU artifact marker Best for: document layout analysis and page element detection.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Oblix`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Oblix/yolov10b-doclaynet_ONNX_document-layout-analysis`, `yolov10b doclaynet`, `yolov10b-doclaynet`, `yolov10b-doclaynet_ONNX_document-layout-analysis`
- Tags: `Document Layout`, `OCR`, `object-detection`, `onnx`, `region:us`, `transformers.js`, `yolov10`

## table-detection - Table detection/structure

Purpose: table detection and table structure recognition.
Catalog task: `object-detection`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. table transformer detection

- Index: `xlocllm.unit("table-detection", "Xenova/table-transformer-detection")`
- Model ID: `Xenova/table-transformer-detection`
- Best for: known browser-ready provider Best for: table detection and table structure recognition.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/table-transformer-detection`, `table transformer detection`, `table-transformer-detection`
- Tags: `OCR`, `Table`, `base_model:microsoft/table-transformer-detection`, `base_model:quantized:microsoft/table-transformer-detection`, `object-detection`, `onnx`, `region:us`, `table-transformer`, `transformers.js`

### 2. table transformer structure recognition v1.1 all

- Index: `xlocllm.unit("table-detection", "Xenova/table-transformer-structure-recognition-v1.1-all")`
- Model ID: `Xenova/table-transformer-structure-recognition-v1.1-all`
- Best for: known browser-ready provider Best for: table detection and table structure recognition.
- Runtime: `transformers`
- Task: `object-detection`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.18 GB`
- Disk: `180 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/table-transformer-structure-recognition-v1.1-all`, `table transformer structure recognition v1.1 all`, `table-transformer-structure-recognition-v1.1-all`
- Tags: `OCR`, `Table`, `base_model:microsoft/table-transformer-structure-recognition-v1.1-all`, `base_model:quantized:microsoft/table-transformer-structure-recognition-v1.1-all`, `object-detection`, `onnx`, `region:us`, `table-transformer`, `transformers.js`

## document-qa - Document QA

Purpose: document question answering and form-like document extraction.
Catalog task: `document-question-answering`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. donut base finetuned cord v2

- Index: `xlocllm.unit("document-qa", "Xenova/donut-base-finetuned-cord-v2")`
- Model ID: `Xenova/donut-base-finetuned-cord-v2`
- Best for: known browser-ready provider Best for: document question answering and form-like document extraction.
- Runtime: `transformers`
- Task: `document-question-answering`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/donut-base-finetuned-cord-v2`, `donut base finetuned cord v2`, `donut-base-finetuned-cord-v2`
- Tags: `Document QA`, `OCR`, `base_model:naver-clova-ix/donut-base-finetuned-cord-v2`, `base_model:quantized:naver-clova-ix/donut-base-finetuned-cord-v2`, `donut`, `donut-swin`, `image-text-to-text`, `image-to-text`, `onnx`, `region:us`, `transformers.js`, `vision`, `vision-encoder-decoder`

### 2. donut base finetuned docvqa

- Index: `xlocllm.unit("document-qa", "Xenova/donut-base-finetuned-docvqa")`
- Model ID: `Xenova/donut-base-finetuned-docvqa`
- Best for: known browser-ready provider Best for: document question answering and form-like document extraction.
- Runtime: `transformers`
- Task: `document-question-answering`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `Xenova/donut-base-finetuned-docvqa`, `donut base finetuned docvqa`, `donut-base-finetuned-docvqa`
- Tags: `Document QA`, `OCR`, `base_model:naver-clova-ix/donut-base-finetuned-docvqa`, `base_model:quantized:naver-clova-ix/donut-base-finetuned-docvqa`, `document-question-answering`, `donut`, `donut-swin`, `image-text-to-text`, `image-to-text`, `onnx`, `region:us`, `transformers.js`, `vision`, `vision-encoder-decoder`

## text-classification - Text classification

Purpose: sentiment, toxicity, and general text classification.
Catalog task: `text-classification`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. bert base multilingual uncased sentiment

- Index: `xlocllm.unit("text-classification", "Xenova/bert-base-multilingual-uncased-sentiment")`
- Model ID: `Xenova/bert-base-multilingual-uncased-sentiment`
- Best for: known browser-ready provider Best for: sentiment, toxicity, and general text classification.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/bert-base-multilingual-uncased-sentiment`, `bert base multilingual uncased sentiment`, `bert-base-multilingual-uncased-sentiment`
- Tags: `Text`, `Text Classification`, `base_model:nlptown/bert-base-multilingual-uncased-sentiment`, `base_model:quantized:nlptown/bert-base-multilingual-uncased-sentiment`, `bert`, `onnx`, `region:us`, `text-classification`, `transformers.js`

### 2. distilbert base multilingual cased sentiments student

- Index: `xlocllm.unit("text-classification", "Xenova/distilbert-base-multilingual-cased-sentiments-student")`
- Model ID: `Xenova/distilbert-base-multilingual-cased-sentiments-student`
- Best for: known browser-ready provider Best for: sentiment, toxicity, and general text classification.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/distilbert-base-multilingual-cased-sentiments-student`, `distilbert base multilingual cased sentiments student`, `distilbert-base-multilingual-cased-sentiments-student`
- Tags: `Text`, `Text Classification`, `base_model:lxyuan/distilbert-base-multilingual-cased-sentiments-student`, `base_model:quantized:lxyuan/distilbert-base-multilingual-cased-sentiments-student`, `distilbert`, `onnx`, `region:us`, `text-classification`, `transformers.js`

### 3. distilbert base uncased finetuned sst 2 english

- Index: `xlocllm.unit("text-classification", "Xenova/distilbert-base-uncased-finetuned-sst-2-english")`
- Model ID: `Xenova/distilbert-base-uncased-finetuned-sst-2-english`
- Best for: known browser-ready provider Best for: sentiment, toxicity, and general text classification.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/distilbert-base-uncased-finetuned-sst-2-english`, `distilbert base uncased finetuned sst 2 english`, `distilbert-base-uncased-finetuned-sst-2-english`
- Tags: `Text`, `Text Classification`, `base_model:distilbert/distilbert-base-uncased-finetuned-sst-2-english`, `base_model:quantized:distilbert/distilbert-base-uncased-finetuned-sst-2-english`, `distilbert`, `onnx`, `region:us`, `text-classification`, `transformers.js`

### 4. toxic bert

- Index: `xlocllm.unit("text-classification", "Xenova/toxic-bert")`
- Model ID: `Xenova/toxic-bert`
- Best for: known browser-ready provider Best for: sentiment, toxicity, and general text classification.
- Runtime: `transformers`
- Task: `text-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/toxic-bert`, `toxic bert`, `toxic-bert`
- Tags: `Text`, `Text Classification`, `base_model:quantized:unitary/toxic-bert`, `base_model:unitary/toxic-bert`, `bert`, `onnx`, `region:us`, `text-classification`, `transformers.js`

## ner - NER/entity extraction

Purpose: named entity recognition and token classification.
Catalog task: `token-classification`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. bert base multilingual cased ner hrl

- Index: `xlocllm.unit("ner", "Xenova/bert-base-multilingual-cased-ner-hrl")`
- Model ID: `Xenova/bert-base-multilingual-cased-ner-hrl`
- Best for: known browser-ready provider Best for: named entity recognition and token classification.
- Runtime: `transformers`
- Task: `token-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `multilingual`
- Aliases: `Xenova/bert-base-multilingual-cased-ner-hrl`, `bert base multilingual cased ner hrl`, `bert-base-multilingual-cased-ner-hrl`
- Tags: `NER`, `Text`, `base_model:Davlan/bert-base-multilingual-cased-ner-hrl`, `base_model:quantized:Davlan/bert-base-multilingual-cased-ner-hrl`, `bert`, `onnx`, `region:us`, `token-classification`, `transformers.js`

### 2. bert base NER

- Index: `xlocllm.unit("ner", "Xenova/bert-base-NER")`
- Model ID: `Xenova/bert-base-NER`
- Best for: known browser-ready provider Best for: named entity recognition and token classification.
- Runtime: `transformers`
- Task: `token-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/bert-base-NER`, `bert base NER`, `bert-base-NER`
- Tags: `NER`, `Text`, `base_model:dslim/bert-base-NER`, `base_model:quantized:dslim/bert-base-NER`, `bert`, `onnx`, `region:us`, `token-classification`, `transformers.js`

### 3. bert base NER uncased

- Index: `xlocllm.unit("ner", "Xenova/bert-base-NER-uncased")`
- Model ID: `Xenova/bert-base-NER-uncased`
- Best for: known browser-ready provider Best for: named entity recognition and token classification.
- Runtime: `transformers`
- Task: `token-classification`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.12 GB`
- Disk: `120 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/bert-base-NER-uncased`, `bert base NER uncased`, `bert-base-NER-uncased`
- Tags: `NER`, `Text`, `base_model:dslim/bert-base-NER-uncased`, `base_model:quantized:dslim/bert-base-NER-uncased`, `bert`, `onnx`, `region:us`, `token-classification`, `transformers.js`

## zero-shot-text - Zero-shot text

Purpose: zero-shot text classification with custom candidate labels.
Catalog task: `zero-shot-classification`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. bart large mnli

- Index: `xlocllm.unit("zero-shot-text", "Xenova/bart-large-mnli")`
- Model ID: `Xenova/bart-large-mnli`
- Best for: known browser-ready provider Best for: zero-shot text classification with custom candidate labels.
- Runtime: `transformers`
- Task: `zero-shot-classification`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.32 GB`
- Disk: `330 MB`
- VRAM: `396 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/bart-large-mnli`, `bart large mnli`, `bart-large-mnli`
- Tags: `Text`, `Zero-shot Text`, `bart`, `base_model:facebook/bart-large-mnli`, `base_model:quantized:facebook/bart-large-mnli`, `onnx`, `region:us`, `text-classification`, `transformers.js`, `zero-shot-classification`

### 2. mobilebert uncased mnli

- Index: `xlocllm.unit("zero-shot-text", "Xenova/mobilebert-uncased-mnli")`
- Model ID: `Xenova/mobilebert-uncased-mnli`
- Best for: known browser-ready provider Best for: zero-shot text classification with custom candidate labels.
- Runtime: `transformers`
- Task: `zero-shot-classification`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.32 GB`
- Disk: `330 MB`
- VRAM: `396 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/mobilebert-uncased-mnli`, `mobilebert uncased mnli`, `mobilebert-uncased-mnli`
- Tags: `Text`, `Zero-shot Text`, `base_model:quantized:typeform/mobilebert-uncased-mnli`, `base_model:typeform/mobilebert-uncased-mnli`, `mobilebert`, `onnx`, `region:us`, `text-classification`, `transformers.js`, `zero-shot-classification`

## summarization - Summarization

Purpose: text summarization.
Catalog task: `summarization`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. bart large cnn

- Index: `xlocllm.unit("summarization", "Xenova/bart-large-cnn")`
- Model ID: `Xenova/bart-large-cnn`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/bart-large-cnn`, `bart large cnn`, `bart-large-cnn`
- Tags: `Summarization`, `Text`, `bart`, `base_model:facebook/bart-large-cnn`, `base_model:quantized:facebook/bart-large-cnn`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 2. Bart Large CNN

- Index: `xlocllm.unit("summarization", "c2p-cmd/Bart-Large-CNN-Onnx")`
- Model ID: `c2p-cmd/Bart-Large-CNN-Onnx`
- Best for: ONNX/WebGPU artifact marker Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `c2p-cmd`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Bart Large CNN`, `Bart-Large-CNN`, `Bart-Large-CNN-Onnx`, `c2p-cmd/Bart-Large-CNN-Onnx`
- Tags: `Summarization`, `Text`, `bart`, `base_model:facebook/bart-large-cnn`, `base_model:quantized:facebook/bart-large-cnn`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 3. bart large cnn

- Index: `xlocllm.unit("summarization", "omoral02/bart-large-cnn-ONNX")`
- Model ID: `omoral02/bart-large-cnn-ONNX`
- Best for: ONNX/WebGPU artifact marker Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `omoral02`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `mit`
- Languages: `en`
- Aliases: `bart large cnn`, `bart-large-cnn`, `bart-large-cnn-ONNX`, `omoral02/bart-large-cnn-ONNX`
- Tags: `Summarization`, `Text`, `arxiv:1910.13461`, `bart`, `base_model:facebook/bart-large-cnn`, `base_model:quantized:facebook/bart-large-cnn`, `dataset:cnn_dailymail`, `en`, `license:mit`, `model-index`, `onnx`, `summarization`, `text2text-generation`, `transformers.js`

### 4. bart large xsum

- Index: `xlocllm.unit("summarization", "Xenova/bart-large-xsum")`
- Model ID: `Xenova/bart-large-xsum`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/bart-large-xsum`, `bart large xsum`, `bart-large-xsum`
- Tags: `Summarization`, `Text`, `bart`, `base_model:facebook/bart-large-xsum`, `base_model:quantized:facebook/bart-large-xsum`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 5. distilbart cnn 12 3

- Index: `xlocllm.unit("summarization", "Xenova/distilbart-cnn-12-3")`
- Model ID: `Xenova/distilbart-cnn-12-3`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/distilbart-cnn-12-3`, `distilbart cnn 12 3`, `distilbart-cnn-12-3`
- Tags: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-cnn-12-3`, `base_model:sshleifer/distilbart-cnn-12-3`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 6. distilbart cnn 12 6

- Index: `xlocllm.unit("summarization", "Xenova/distilbart-cnn-12-6")`
- Model ID: `Xenova/distilbart-cnn-12-6`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/distilbart-cnn-12-6`, `distilbart cnn 12 6`, `distilbart-cnn-12-6`
- Tags: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-cnn-12-6`, `base_model:sshleifer/distilbart-cnn-12-6`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 7. distilbart cnn 12 6

- Index: `xlocllm.unit("summarization", "Mozilla/distilbart-cnn-12-6")`
- Model ID: `Mozilla/distilbart-cnn-12-6`
- Best for: ONNX/WebGPU artifact marker Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Mozilla`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Mozilla/distilbart-cnn-12-6`, `distilbart cnn 12 6`, `distilbart-cnn-12-6`
- Tags: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-cnn-12-6`, `base_model:sshleifer/distilbart-cnn-12-6`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 8. distilbart cnn 6 6

- Index: `xlocllm.unit("summarization", "Xenova/distilbart-cnn-6-6")`
- Model ID: `Xenova/distilbart-cnn-6-6`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `Xenova/distilbart-cnn-6-6`, `distilbart cnn 6 6`, `distilbart-cnn-6-6`
- Tags: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-cnn-6-6`, `base_model:sshleifer/distilbart-cnn-6-6`, `license:apache-2.0`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 9. distilbart xsum 12 1

- Index: `xlocllm.unit("summarization", "Xenova/distilbart-xsum-12-1")`
- Model ID: `Xenova/distilbart-xsum-12-1`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/distilbart-xsum-12-1`, `distilbart xsum 12 1`, `distilbart-xsum-12-1`
- Tags: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-xsum-12-1`, `base_model:sshleifer/distilbart-xsum-12-1`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 10. distilbart xsum 12 3

- Index: `xlocllm.unit("summarization", "Xenova/distilbart-xsum-12-3")`
- Model ID: `Xenova/distilbart-xsum-12-3`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/distilbart-xsum-12-3`, `distilbart xsum 12 3`, `distilbart-xsum-12-3`
- Tags: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-xsum-12-3`, `base_model:sshleifer/distilbart-xsum-12-3`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 11. distilbart xsum 12 6

- Index: `xlocllm.unit("summarization", "Xenova/distilbart-xsum-12-6")`
- Model ID: `Xenova/distilbart-xsum-12-6`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/distilbart-xsum-12-6`, `distilbart xsum 12 6`, `distilbart-xsum-12-6`
- Tags: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-xsum-12-6`, `base_model:sshleifer/distilbart-xsum-12-6`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 12. distilbart xsum 6 6

- Index: `xlocllm.unit("summarization", "Xenova/distilbart-xsum-6-6")`
- Model ID: `Xenova/distilbart-xsum-6-6`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/distilbart-xsum-6-6`, `distilbart xsum 6 6`, `distilbart-xsum-6-6`
- Tags: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-xsum-6-6`, `base_model:sshleifer/distilbart-xsum-6-6`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 13. distilbart xsum 9 6

- Index: `xlocllm.unit("summarization", "Xenova/distilbart-xsum-9-6")`
- Model ID: `Xenova/distilbart-xsum-9-6`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/distilbart-xsum-9-6`, `distilbart xsum 9 6`, `distilbart-xsum-9-6`
- Tags: `Summarization`, `Text`, `bart`, `base_model:quantized:sshleifer/distilbart-xsum-9-6`, `base_model:sshleifer/distilbart-xsum-9-6`, `onnx`, `region:us`, `summarization`, `text2text-generation`, `transformers.js`

### 14. rut5 base sum gazeta

- Index: `xlocllm.unit("summarization", "onnx-community/rut5_base_sum_gazeta-ONNX")`
- Model ID: `onnx-community/rut5_base_sum_gazeta-ONNX`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `['apache-2.0']`
- Languages: `ru`
- Aliases: `onnx-community/rut5_base_sum_gazeta-ONNX`, `rut5-base-sum-gazeta`, `rut5_base_sum_gazeta`, `rut5_base_sum_gazeta-ONNX`
- Tags: `Summarization`, `Text`, `base_model:IlyaGusev/rut5_base_sum_gazeta`, `base_model:quantized:IlyaGusev/rut5_base_sum_gazeta`, `dataset:IlyaGusev/gazeta`, `license:apache-2.0`, `onnx`, `region:us`, `ru`, `summarization`, `t5`, `text2text-generation`, `transformers.js`

### 15. text summarization

- Index: `xlocllm.unit("summarization", "onnx-community/text_summarization-ONNX")`
- Model ID: `onnx-community/text_summarization-ONNX`
- Best for: known browser-ready provider Best for: text summarization.
- Runtime: `transformers`
- Task: `summarization`
- Provider: `onnx-community`
- Hardware tier: `small`
- Parameters: `n/a`
- Model size: `0.41 GB`
- Disk: `420 MB`
- VRAM: `504 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `onnx-community/text_summarization-ONNX`, `text-summarization`, `text_summarization`, `text_summarization-ONNX`
- Tags: `Summarization`, `Text`, `base_model:Falconsai/text_summarization`, `base_model:quantized:Falconsai/text_summarization`, `en`, `license:apache-2.0`, `onnx`, `region:us`, `summarization`, `t5`, `text2text-generation`, `transformers.js`

## text2text - Text2Text utilities

Purpose: general text-to-text generation utilities.
Catalog task: `text2text-generation`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. flan t5 small

- Index: `xlocllm.unit("text2text", "Xenova/flan-t5-small")`
- Model ID: `Xenova/flan-t5-small`
- Best for: known browser-ready provider Best for: general text-to-text generation utilities.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `en`
- Aliases: `Xenova/flan-t5-small`, `flan t5 small`, `flan-t5-small`
- Tags: `Text`, `Text2Text`, `dataset:djaym7/wiki_dialog`, `dataset:svakulenk0/qrecc`, `dataset:taskmaster2`, `de`, `en`, `fr`, `multilingual`, `onnx`, `ro`, `t5`, `text2text-generation`, `transformers.js`

### 2. t5 small

- Index: `xlocllm.unit("text2text", "Xenova/t5-small")`
- Model ID: `Xenova/t5-small`
- Best for: known browser-ready provider Best for: general text-to-text generation utilities.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.25 GB`
- Disk: `260 MB`
- VRAM: `312 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `Xenova/t5-small`, `t5 small`, `t5-small`
- Tags: `Text`, `Text2Text`, `base_model:google-t5/t5-small`, `base_model:quantized:google-t5/t5-small`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 3. LaMini T5 61M

- Index: `xlocllm.unit("text2text", "Xenova/LaMini-T5-61M")`
- Model ID: `Xenova/LaMini-T5-61M`
- Best for: known browser-ready provider Best for: general text-to-text generation utilities.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `0.061B`
- Model size: `0.06 GB`
- Disk: `57 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `LaMini T5 61M`, `LaMini-T5-61M`, `Xenova/LaMini-T5-61M`
- Tags: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-T5-61M`, `base_model:quantized:MBZUAI/LaMini-T5-61M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 4. LaMini Flan T5 77M

- Index: `xlocllm.unit("text2text", "Xenova/LaMini-Flan-T5-77M")`
- Model ID: `Xenova/LaMini-Flan-T5-77M`
- Best for: known browser-ready provider Best for: general text-to-text generation utilities.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `0.077B`
- Model size: `0.07 GB`
- Disk: `73 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `LaMini Flan T5 77M`, `LaMini-Flan-T5-77M`, `Xenova/LaMini-Flan-T5-77M`
- Tags: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-Flan-T5-77M`, `base_model:quantized:MBZUAI/LaMini-Flan-T5-77M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 5. LaMini T5 223M

- Index: `xlocllm.unit("text2text", "Xenova/LaMini-T5-223M")`
- Model ID: `Xenova/LaMini-T5-223M`
- Best for: known browser-ready provider Best for: general text-to-text generation utilities.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `0.223B`
- Model size: `0.21 GB`
- Disk: `211 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `LaMini T5 223M`, `LaMini-T5-223M`, `Xenova/LaMini-T5-223M`
- Tags: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-T5-223M`, `base_model:quantized:MBZUAI/LaMini-T5-223M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 6. LaMini Flan T5 248M

- Index: `xlocllm.unit("text2text", "Xenova/LaMini-Flan-T5-248M")`
- Model ID: `Xenova/LaMini-Flan-T5-248M`
- Best for: known browser-ready provider Best for: general text-to-text generation utilities.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `tiny`
- Parameters: `0.248B`
- Model size: `0.23 GB`
- Disk: `235 MB`
- VRAM: `282 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `LaMini Flan T5 248M`, `LaMini-Flan-T5-248M`, `Xenova/LaMini-Flan-T5-248M`
- Tags: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-Flan-T5-248M`, `base_model:quantized:MBZUAI/LaMini-Flan-T5-248M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 7. LaMini T5 738M

- Index: `xlocllm.unit("text2text", "Xenova/LaMini-T5-738M")`
- Model ID: `Xenova/LaMini-T5-738M`
- Best for: known browser-ready provider Best for: general text-to-text generation utilities.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `0.738B`
- Model size: `0.68 GB`
- Disk: `701 MB`
- VRAM: `841 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `LaMini T5 738M`, `LaMini-T5-738M`, `Xenova/LaMini-T5-738M`
- Tags: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-T5-738M`, `base_model:quantized:MBZUAI/LaMini-T5-738M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

### 8. LaMini Flan T5 783M

- Index: `xlocllm.unit("text2text", "Xenova/LaMini-Flan-T5-783M")`
- Model ID: `Xenova/LaMini-Flan-T5-783M`
- Best for: known browser-ready provider Best for: general text-to-text generation utilities.
- Runtime: `transformers`
- Task: `text2text-generation`
- Provider: `Xenova`
- Hardware tier: `small`
- Parameters: `0.783B`
- Model size: `0.73 GB`
- Disk: `743 MB`
- VRAM: `891 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `en`
- Aliases: `LaMini Flan T5 783M`, `LaMini-Flan-T5-783M`, `Xenova/LaMini-Flan-T5-783M`
- Tags: `Text`, `Text2Text`, `base_model:MBZUAI/LaMini-Flan-T5-783M`, `base_model:quantized:MBZUAI/LaMini-Flan-T5-783M`, `onnx`, `region:us`, `t5`, `text2text-generation`, `transformers.js`

## code - Code understanding

Purpose: code embeddings, code language identification, and code understanding features.
Catalog task: `feature-extraction`.
Invoke endpoint: no direct Python/browser bridge route is implemented yet.

### 1. codebert base

- Index: `xlocllm.unit("code", "onnx-community/codebert-base-ONNX")`
- Model ID: `onnx-community/codebert-base-ONNX`
- Best for: known browser-ready provider Best for: code embeddings, code language identification, and code understanding features.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.16 GB`
- Disk: `160 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `codebert base`, `codebert-base`, `codebert-base-ONNX`, `onnx-community/codebert-base-ONNX`
- Tags: `Code`, `arxiv:2002.08155`, `base_model:microsoft/codebert-base`, `base_model:quantized:microsoft/codebert-base`, `feature-extraction`, `onnx`, `region:us`, `roberta`, `transformers.js`

### 2. codebert javascript

- Index: `xlocllm.unit("code", "onnx-community/codebert-javascript-ONNX")`
- Model ID: `onnx-community/codebert-javascript-ONNX`
- Best for: known browser-ready provider Best for: code embeddings, code language identification, and code understanding features.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.16 GB`
- Disk: `160 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `codebert javascript`, `codebert-javascript`, `codebert-javascript-ONNX`, `onnx-community/codebert-javascript-ONNX`
- Tags: `Code`, `arxiv:2302.05527`, `base_model:neulab/codebert-javascript`, `base_model:quantized:neulab/codebert-javascript`, `fill-mask`, `onnx`, `region:us`, `roberta`, `transformers.js`

### 3. CodeBERTa language id

- Index: `xlocllm.unit("code", "onnx-community/CodeBERTa-language-id-ONNX")`
- Model ID: `onnx-community/CodeBERTa-language-id-ONNX`
- Best for: known browser-ready provider Best for: code embeddings, code language identification, and code understanding features.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.16 GB`
- Disk: `160 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `apache-2.0`
- Languages: `universal`
- Aliases: `CodeBERTa language id`, `CodeBERTa-language-id`, `CodeBERTa-language-id-ONNX`, `onnx-community/CodeBERTa-language-id-ONNX`
- Tags: `Code`, `arxiv:1909.09436`, `base_model:huggingface/CodeBERTa-language-id`, `base_model:quantized:huggingface/CodeBERTa-language-id`, `code`, `dataset:code_search_net`, `license:apache-2.0`, `onnx`, `region:us`, `roberta`, `text-classification`, `transformers.js`

### 4. CodeBERTa small v1

- Index: `xlocllm.unit("code", "onnx-community/CodeBERTa-small-v1-ONNX")`
- Model ID: `onnx-community/CodeBERTa-small-v1-ONNX`
- Best for: known browser-ready provider Best for: code embeddings, code language identification, and code understanding features.
- Runtime: `transformers`
- Task: `feature-extraction`
- Provider: `onnx-community`
- Hardware tier: `tiny`
- Parameters: `n/a`
- Model size: `0.16 GB`
- Disk: `160 MB`
- VRAM: `256 MB`
- DType: `auto`
- NPU/WebNN: `yes`
- License: `unknown`
- Languages: `universal`
- Aliases: `CodeBERTa small v1`, `CodeBERTa-small-v1`, `CodeBERTa-small-v1-ONNX`, `onnx-community/CodeBERTa-small-v1-ONNX`
- Tags: `Code`, `arxiv:1909.09436`, `base_model:huggingface/CodeBERTa-small-v1`, `base_model:quantized:huggingface/CodeBERTa-small-v1`, `code`, `dataset:code_search_net`, `fill-mask`, `onnx`, `region:us`, `roberta`, `transformers.js`
