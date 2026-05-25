from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

UnitType = Literal[
    "LLM",
    "vectorstorage",
    "RAG",
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
    reasoning: bool | None = None
    options: dict[str, Any] | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"type": self.type, "model": self.model}
        if self.reasoning is not None:
            payload["reasoning"] = self.reasoning
        if self.options:
            payload["options"] = dict(self.options)
        return payload


Json = dict[str, Any]
