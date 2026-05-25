# xlocllm: готовые скрипты под популярные задачи

Этот файл - набор практических рецептов. Каждый пример поднимает runtime с
реальными моделями из каталога xlocllm и показывает, как сделать запрос.

Перед запуском:

```powershell
pip install "xlocllm[openai]"
```

Если устройство слабое или WebGPU недоступен, сначала посмотрите подбор:

```python
import xlocllm

print(xlocllm.benchmark("LLM"))
print(xlocllm.models(webgpu=False, limit_per_unit=2))
```

В примерах `IMAGE`, `AUDIO` и пути к файлам замените на свои локальные файлы или
URL, доступные браузеру.

## 1. RAG stack: embeddings + reranker

Для поиска по базе документов: сначала считаем embedding, потом reranker
пересортировывает кандидатов под конкретный запрос.

Модели:

- Embeddings: `multilingual-e5-small`
- Reranker: `bge-reranker-base`

```python
import xlocllm

documents = [
    "Лидар измеряет расстояние до объектов с помощью лазерных импульсов.",
    "Радар использует радиоволны и хорошо работает в тумане и дожде.",
    "Камера дает богатую картинку, но зависит от освещения.",
]
query = "Как лидар понимает расстояние до препятствия?"

embedding = xlocllm.unit("embedding", "multilingual-e5-small")
reranker = xlocllm.unit("reranker", "bge-reranker-base")

with xlocllm.runtime([embedding, reranker]) as rt:
    rt.run()

    vectors = rt.invoke(
        "embeddings",
        {"model": "multilingual-e5-small", "input": [query, *documents]},
    )
    ranked = rt.invoke(
        "rerank",
        {"model": "bge-reranker-base", "query": query, "documents": documents},
    )

    print("Embedding count:", len(vectors["embeddings"]))
    print("Best context:", ranked["results"][0]["document"])
```

## 2. Фото-перевод: OCR + Translator

Готовый стек для сценария "сфотографировать текст и перевести".

Модели:

- OCR: `onnx-community/trocr-base-stage1-ONNX`
- Translator: `opus-en-ru`

```python
import xlocllm

IMAGE = "menu_or_sign.jpg"

ocr = xlocllm.unit("ocr", "onnx-community/trocr-base-stage1-ONNX")
translator = xlocllm.unit("translator", "opus-en-ru")

def pick_text(value):
    if isinstance(value, dict):
        return value.get("text") or value.get("content") or str(value)
    if isinstance(value, list) and value:
        return value[0].get("generated_text") or value[0].get("text") or str(value)
    return str(value)

def pick_translation(value):
    if isinstance(value, list) and value:
        return value[0].get("translation_text") or str(value)
    if isinstance(value, dict):
        return value.get("translation_text") or value.get("text") or str(value)
    return str(value)

with xlocllm.runtime([ocr, translator]) as rt:
    rt.run()

    recognized = rt.invoke("ocr", {"model": "onnx-community/trocr-base-stage1-ONNX", "image": IMAGE})
    source_text = pick_text(recognized)
    translated = rt.invoke("translate", {"model": "opus-en-ru", "text": source_text})

    print("OCR:", source_text)
    print("RU:", pick_translation(translated))
```

## 3. Agent stack: 3 разных LLM в одном runtime

Полезно для агентных систем, где отдельные модели выполняют разные роли:
planner, worker, critic.

Модели:

- Planner: `Qwen-3.5-0.8b`
- Worker: `Qwen3-0.6B-ONNX`
- Critic: `SmolLM2-360M`

```python
from openai import OpenAI
import xlocllm

planner = xlocllm.unit("LLM", "Qwen-3.5-0.8b")
worker = xlocllm.unit("LLM", "Qwen3-0.6B-ONNX", reasoning=False)
critic = xlocllm.unit("LLM", "SmolLM2-360M")

client = OpenAI(base_url="http://127.0.0.1:1146/v1", api_key="xlocllm")

def ask(model, prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=160,
        temperature=0.2,
    )
    return response.choices[0].message.content

with xlocllm.runtime([planner, worker, critic]) as rt:
    rt.run()

    task = "Составь план маленького RAG сервиса для локальных документов."
    plan = ask("Qwen-3.5-0.8b", f"Разбей задачу на шаги:\n{task}")
    draft = ask("Qwen3-0.6B-ONNX", f"Реализуй краткий технический дизайн по плану:\n{plan}")
    review = ask("SmolLM2-360M", f"Найди слабые места в дизайне:\n{draft}")

    print("PLAN\n", plan)
    print("DRAFT\n", draft)
    print("REVIEW\n", review)
```

## 4. Meeting notes: ASR + Summarization

Для расшифровки звонка или голосовой заметки и короткого summary.

Модели:

- ASR: `whisper-tiny`
- Summarization: `Xenova/distilbart-cnn-6-6`

```python
import xlocllm

AUDIO = "meeting.wav"

asr = xlocllm.unit("asr", "whisper-tiny")
summarizer = xlocllm.unit("summarization", "Xenova/distilbart-cnn-6-6")

with xlocllm.runtime([asr, summarizer]) as rt:
    rt.run()

    transcript = rt.invoke("asr", {"model": "whisper-tiny", "audio": AUDIO})
    text = transcript["text"]
    summary = rt.invoke("summarization", {"model": "Xenova/distilbart-cnn-6-6", "text": text})

    print("TRANSCRIPT\n", text)
    print("SUMMARY\n", summary["summary"])
```

## 5. Voice assistant: ASR + LLM + TTS

Минимальный голосовой помощник: распознать речь, получить ответ LLM и озвучить.

Модели:

- ASR: `whisper-tiny`
- LLM: `Qwen-3.5-0.8b`
- TTS: `Xenova/mms-tts-rus`

```python
import json
import xlocllm

AUDIO = "question.wav"

asr = xlocllm.unit("asr", "whisper-tiny")
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b")
tts = xlocllm.unit("tts", "Xenova/mms-tts-rus")

with xlocllm.runtime([asr, llm, tts]) as rt:
    rt.run()

    speech = rt.invoke("asr", {"model": "whisper-tiny", "audio": AUDIO})["text"]
    answer = rt.chat(speech, model="Qwen-3.5-0.8b", max_tokens=120, temperature=0.3)["content"]
    audio = rt.invoke("tts", {"model": "Xenova/mms-tts-rus", "text": answer})

    print("USER:", speech)
    print("ASSISTANT:", answer)
    print("TTS payload:", json.dumps(audio)[:500])
```

## 6. Visual inspection: caption + classification + detection

Для автоописания картинки, общей классификации и поиска объектов.

Модели:

- VLM/caption: `vit-gpt2-captioning`
- Image classification: `mobilenet-v2`
- Object detection: `yolos-tiny`

```python
import xlocllm

IMAGE = "warehouse_photo.jpg"

caption = xlocllm.unit("vlm", "vit-gpt2-captioning")
classifier = xlocllm.unit("image-classification", "mobilenet-v2")
detector = xlocllm.unit("object-detection", "yolos-tiny")

with xlocllm.runtime([caption, classifier, detector]) as rt:
    rt.run()

    description = rt.invoke("image-to-text", {"model": "vit-gpt2-captioning", "image": IMAGE})
    labels = rt.invoke("image.classify", {"model": "mobilenet-v2", "image": IMAGE})
    boxes = rt.invoke("image.detect", {"model": "yolos-tiny", "image": IMAGE})

    print("Caption:", description["text"])
    print("Top labels:", labels["labels"][:3])
    print("Objects:", boxes["boxes"][:5])
```

## 7. Document intelligence: layout + tables + OCR + DocQA

Для документов, чеков, счетов, PDF-сканов и форм: найти блоки, таблицы,
распознать текст и задать вопрос по документу.

Модели:

- Layout: `Oblix/yolov10b-doclaynet_ONNX_document-layout-analysis`
- Tables: `Xenova/table-transformer-detection`
- OCR: `onnx-community/trocr-base-stage1-ONNX`
- Document QA: `Xenova/donut-base-finetuned-docvqa`

```python
import xlocllm

IMAGE = "invoice_scan.png"

layout = xlocllm.unit("document-layout", "Oblix/yolov10b-doclaynet_ONNX_document-layout-analysis")
tables = xlocllm.unit("table-detection", "Xenova/table-transformer-detection")
ocr = xlocllm.unit("ocr", "onnx-community/trocr-base-stage1-ONNX")
docqa = xlocllm.unit("document-qa", "Xenova/donut-base-finetuned-docvqa")

with xlocllm.runtime([layout, tables, ocr, docqa]) as rt:
    rt.run()

    page_blocks = rt.invoke("document-layout", {"model": layout.model, "image": IMAGE})
    table_boxes = rt.invoke("table-detection", {"model": tables.model, "image": IMAGE})
    text = rt.invoke("ocr", {"model": ocr.model, "image": IMAGE})
    answer = rt.invoke(
        "document-qa",
        {"model": docqa.model, "image": IMAGE, "question": "What is the total amount?"},
    )

    print("Layout boxes:", page_blocks["boxes"][:5])
    print("Tables:", table_boxes["boxes"][:5])
    print("OCR:", text["text"])
    print("Answer:", answer["answers"])
```

## 8. Support triage: zero-shot + sentiment + NER

Для входящих обращений: определить категорию, тональность и сущности.

Модели:

- Zero-shot: `Xenova/mobilebert-uncased-mnli`
- Sentiment: `Xenova/distilbert-base-multilingual-cased-sentiments-student`
- NER: `Xenova/bert-base-multilingual-cased-ner-hrl`

```python
import xlocllm

ticket = """
Клиент Иван Петров пишет, что заказ #A-1942 не приехал уже 5 дней.
Просит вернуть деньги и говорит, что очень недоволен поддержкой.
"""

router = xlocllm.unit("zero-shot-text", "Xenova/mobilebert-uncased-mnli")
sentiment = xlocllm.unit("text-classification", "Xenova/distilbert-base-multilingual-cased-sentiments-student")
ner = xlocllm.unit("ner", "Xenova/bert-base-multilingual-cased-ner-hrl")

with xlocllm.runtime([router, sentiment, ner]) as rt:
    rt.run()

    category = rt.invoke(
        "zero-shot-text",
        {
            "model": "Xenova/mobilebert-uncased-mnli",
            "text": ticket,
            "labels": ["delivery", "refund", "technical issue", "billing", "other"],
        },
    )
    tone = rt.invoke("text.classify", {"model": sentiment.model, "text": ticket})
    entities = rt.invoke("ner", {"model": ner.model, "text": ticket})

    print("Category:", category["labels"])
    print("Sentiment:", tone["labels"])
    print("Entities:", entities["entities"])
```

## 9. Background removal: segmentation

Для portrait matting, удаления фона и подготовки изображений для карточек
товаров.

Модель:

- Segmentation: `modnet`

```python
import xlocllm

IMAGE = "portrait.jpg"

segmenter = xlocllm.unit("image-segmentation", "modnet")

with xlocllm.runtime([segmenter]) as rt:
    rt.run()

    result = rt.invoke("image.segment", {"model": "modnet", "image": IMAGE})
    print("Segments:", result["segments"])
```

## 10. Code intelligence: CodeBERT + LLM

Для поиска по коду, похожих функций, классификации snippets и короткого review.

Модели:

- Code features: `codebert base`
- LLM: `Qwen-3.5-0.8b`

```python
import xlocllm

snippet = """
def retry(fn, attempts=3):
    for _ in range(attempts):
        try:
            return fn()
        except Exception:
            pass
    raise RuntimeError("failed")
"""

code = xlocllm.unit("code", "codebert base")
llm = xlocllm.unit("LLM", "Qwen-3.5-0.8b")

with xlocllm.runtime([code, llm]) as rt:
    rt.run()

    features = rt.invoke("code", {"model": "codebert base", "text": snippet})
    review = rt.chat(
        "Найди проблемы в этом Python коде и предложи исправление:\n\n" + snippet,
        model="Qwen-3.5-0.8b",
        max_tokens=180,
        temperature=0.2,
    )

    print("Feature payload keys:", features.keys())
    print("Review:", review["content"])
```

## Что брать за основу

- Для RAG почти всегда начинайте с `embedding + reranker`.
- Для документов добавляйте `ocr`, а для сканов с таблицами - `document-layout`
  и `table-detection`.
- Для агентных сценариев держите несколько LLM в одном runtime и выбирайте
  модель через `model=` в OpenAI-compatible запросе.
- Для слабых устройств сначала запускайте `xlocllm.benchmark("<unit>")` и
  используйте предложенные `fast` / `quality` модели.
