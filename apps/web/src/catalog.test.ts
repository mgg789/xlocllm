import { describe, expect, it } from "vitest";
import { resolveModel, unitDefinitions } from "./catalog";

describe("catalog", () => {
  it("contains every requested unit", () => {
    expect(unitDefinitions.map((unit) => unit.type)).toEqual([
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
    ]);
  });

  it("resolves user-facing aliases", () => {
    expect(resolveModel("LLM", "Qwen-3.5-0.8b")?.modelId).toBe("Qwen3.5-0.8B-q4f16_1-MLC");
    expect(resolveModel("embedding", "multilingual-e5-small")?.modelId).toBe("Xenova/multilingual-e5-small");
  });

  it("contains expanded browser catalog metadata", () => {
    const qwenOnnx = resolveModel("LLM", "onnx-community/Qwen3.5-0.8B-ONNX");
    const qwenFull = resolveModel("LLM", "Qwen-3.5-0.8b-full");

    expect(qwenOnnx?.runtime).toBe("transformers");
    expect(qwenOnnx?.taskGroup).toBe("LLM");
    expect(qwenOnnx?.modelSizeGb).toBeGreaterThan(0);
    expect(qwenOnnx?.npuEligible).toBe(true);
    expect(qwenFull?.backendModelId).toBe("onnx-community/Qwen3.5-0.8B-ONNX");
    expect(qwenFull?.dtype).toBe("fp32");
  });
});
