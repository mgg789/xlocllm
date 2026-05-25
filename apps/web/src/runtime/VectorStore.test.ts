import { describe, expect, it } from "vitest";
import { chunkText, metadataMatches, vectorScore, type VectorRecord } from "./VectorStore";

describe("VectorStore helpers", () => {
  it("chunks text with overlap", () => {
    const chunks = chunkText("alpha beta gamma delta epsilon zeta eta theta ".repeat(8), 90, 10);

    expect(chunks.length).toBeGreaterThan(1);
    expect(chunks.every((chunk) => chunk.length > 0)).toBe(true);
  });

  it("scores vectors by cosine similarity", () => {
    expect(vectorScore("cosine", [1, 0], [1, 0])).toBeCloseTo(1);
    expect(vectorScore("cosine", [1, 0], [0, 1])).toBeCloseTo(0);
  });

  it("matches metadata and record fields", () => {
    const record: VectorRecord = {
      key: "k",
      store: "s",
      namespace: "n",
      id: "a",
      documentId: "doc",
      chunkIndex: 0,
      text: "hello",
      metadata: { source: "manual" },
      embedding: [1],
      createdAt: "now",
      updatedAt: "now",
    };

    expect(metadataMatches(record, { source: "manual", documentId: "doc" })).toBe(true);
    expect(metadataMatches(record, { source: "other" })).toBe(false);
  });
});
