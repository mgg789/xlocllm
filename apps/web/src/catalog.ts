import catalogJson from "../../../packages/catalog/models.json";
import type { Catalog, ModelSpec, UnitDefinition, UnitType } from "./types";

export const catalog = catalogJson as Catalog;

export const unitDefinitions: UnitDefinition[] = catalog.units;

export function modelsForUnit(unit: UnitType): ModelSpec[] {
  return catalog.models.filter((model) => model.unit === unit);
}

export function resolveModel(unit: string, modelName: string): ModelSpec | undefined {
  const normalizedUnit = normalizeUnit(unit);
  const normalizedModel = normalize(modelName);
  return catalog.models.find((model) => {
    if (model.unit !== normalizedUnit) return false;
    return (
      normalize(model.modelId) === normalizedModel ||
      normalize(model.label) === normalizedModel ||
      model.aliases.some((alias) => normalize(alias) === normalizedModel)
    );
  });
}

export function normalizeUnit(unit: string): UnitType {
  const value = normalize(unit);
  if (value === "embeddings") return "embedding";
  if (value === "translator" || value === "translation") return "translator";
  if (value === "image-to-text" || value === "vlm") return "vlm";
  if (value === "background-removing" || value === "segmentation") return "image-segmentation";
  if (value === "zero-shot-image-classification") return "zero-shot-image";
  if (value === "language-identification") return "language-id";
  if (value === "speech-to-text") return "asr";
  if (value === "text-generation" || value === "chat") return "LLM";
  if (value === "text2text-generation" || value === "text-to-text") return "text2text";
  if (value === "text-ranking") return "reranker";
  const found = catalog.units.find((candidate) => normalize(candidate.type) === value || normalize(candidate.label) === value);
  if (!found) {
    throw new Error(`Unknown xlocllm unit type: ${unit}`);
  }
  return found.type;
}

export function modelSummary(model: ModelSpec): string {
  const languages = model.languages.join(", ");
  const params = typeof model.parameterB === "number" ? `${model.parameterB}B params` : "params n/a";
  return `${model.hardwareTier} | ${params} | ${model.modelSizeGb} GB disk | ${languages}`;
}

function normalize(value: string): string {
  return value.trim().toLowerCase().replace(/[_\s]+/g, "-");
}
