import catalogJson from "../../../packages/catalog/models.json";
import type { Catalog, HardwareTier, ModelSpec, UnitDefinition, UnitType } from "./types";

export const catalog = catalogJson as Catalog;

export const unitDefinitions: UnitDefinition[] = catalog.units;

const CPU_FALLBACK_TIERS = new Set<HardwareTier>(["tiny", "small"]);
const CPU_FALLBACK_MAX_VRAM_MB = 1500;
const CPU_FALLBACK_MAX_DISK_MB = 1600;

export function modelsForUnit(unit: UnitType): ModelSpec[] {
  return catalog.models.filter((model) => model.unit === unit);
}

export function supportedModelsForCapabilities(webgpuAvailable: boolean): ModelSpec[] {
  if (webgpuAvailable) return catalog.models;
  const ids = cpuFallbackModelIds();
  return catalog.models.filter((model) => ids.has(model.modelId));
}

export function supportsCpuFallback(model: ModelSpec): boolean {
  if (model.runtime !== "transformers") return false;
  if (model.availability === "unsupported") return false;
  if (CPU_FALLBACK_TIERS.has(model.hardwareTier)) return true;
  return model.vramMB <= CPU_FALLBACK_MAX_VRAM_MB && model.diskMB <= CPU_FALLBACK_MAX_DISK_MB;
}

export function supportsReasoning(model: ModelSpec): boolean {
  if (model.unit !== "LLM") return false;
  const haystack = [
    model.modelId,
    model.label,
    model.notes ?? "",
    ...model.aliases,
    ...(model.tags ?? []),
  ]
    .join(" ")
    .toLowerCase();
  return ["qwen3", "qwen3.5", "qwen3_5", "deepseek-r1", "gpt-oss", "qwq"].some((marker) => haystack.includes(marker));
}

export function cpuFallbackModelIds(minPerUnit = 2): Set<string> {
  const result = new Set(catalog.models.filter(supportsCpuFallback).map((model) => model.modelId));
  for (const unit of unitDefinitions) {
    const current = catalog.models.filter((model) => model.unit === unit.type && result.has(model.modelId));
    if (current.length >= minPerUnit) continue;
    const fallback = catalog.models
      .filter((model) => model.unit === unit.type && model.runtime === "transformers" && model.availability !== "unsupported")
      .sort(compareModelWeight)
      .slice(0, minPerUnit);
    for (const model of fallback) result.add(model.modelId);
  }
  return result;
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

function compareModelWeight(left: ModelSpec, right: ModelSpec): number {
  const leftWeight = modelWeight(left);
  const rightWeight = modelWeight(right);
  for (let index = 0; index < leftWeight.length; index += 1) {
    const delta = leftWeight[index] - rightWeight[index];
    if (delta !== 0) return delta;
  }
  return left.label.localeCompare(right.label);
}

function modelWeight(model: ModelSpec): [number, number, number, number] {
  const tierOrder: Record<HardwareTier, number> = { tiny: 0, small: 1, medium: 2, large: 3 };
  return [tierOrder[model.hardwareTier] ?? 99, model.vramMB, model.diskMB, model.parameterB ?? 0];
}

function normalize(value: string): string {
  return value.trim().toLowerCase().replace(/[_\s]+/g, "-");
}
