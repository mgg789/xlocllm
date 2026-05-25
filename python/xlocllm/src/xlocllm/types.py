from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

UnitType = Literal[
    "LLM",
    "embedding",
    "reranker",
    "translator",
    "tts",
    "image-classification",
    "object-detection",
    "image-segmentation",
    "depth-estimation",
    "vlm",
    "asr",
    "zero-shot-image",
    "language-id",
    "audio-classification",
    "ocr",
    "document-layout",
    "table-detection",
    "document-qa",
    "text-classification",
    "ner",
    "zero-shot-text",
    "summarization",
    "text2text",
    "code",
]


@dataclass(frozen=True)
class UnitRequest:
    type: str
    model: str

    def to_payload(self) -> dict[str, str]:
        return {"type": self.type, "model": self.model}


Json = dict[str, Any]
