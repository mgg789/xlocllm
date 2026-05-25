export type UnitType =
  | "LLM"
  | "embedding"
  | "reranker"
  | "translator"
  | "tts"
  | "image-classification"
  | "object-detection"
  | "image-segmentation"
  | "depth-estimation"
  | "vlm"
  | "asr"
  | "zero-shot-image"
  | "language-id"
  | "audio-classification"
  | "ocr"
  | "document-layout"
  | "table-detection"
  | "document-qa"
  | "text-classification"
  | "ner"
  | "zero-shot-text"
  | "summarization"
  | "text2text"
  | "code";

export type RuntimeKind = "mlc" | "transformers";

export type HardwareTier = "tiny" | "small" | "medium" | "large";

export type UnitStatus =
  | "off"
  | "selected"
  | "installing"
  | "ready"
  | "active"
  | "running"
  | "hibernated"
  | "error";

export interface UnitDefinition {
  type: UnitType;
  label: string;
  task: string;
}

export interface ModelSpec {
  unit: UnitType;
  runtime: RuntimeKind;
  task: string;
  taskGroup: string;
  modelId: string;
  backendModelId?: string;
  aliases: string[];
  label: string;
  provider: string;
  logoKey: string;
  languages: string[];
  license: string;
  hardwareTier: HardwareTier;
  parameterB?: number | null;
  modelSizeGb: number;
  diskMB: number;
  vramMB: number;
  dtype?: string;
  tags?: string[];
  npuEligible?: boolean;
  availability?: "verified" | "candidate" | "unsupported";
  notes?: string;
}

export interface Catalog {
  schemaVersion: number;
  units: UnitDefinition[];
  models: ModelSpec[];
}

export interface UnitState {
  type: UnitType;
  selectedModelId?: string;
  active: boolean;
  status: UnitStatus;
  progress?: number;
  error?: string;
}

export interface RuntimeMetrics {
  gpu: number | null;
  cpu: number | null;
  ram: number | null;
  disk: number | null;
}

export interface NpuState {
  status: "active" | "unavailable" | "fallback";
  reason?: string;
  backend?: string;
}

export interface LogEntry {
  time: string;
  level: "info" | "warn" | "error";
  message: string;
}

export interface RuntimeUnitRequest {
  type: UnitType | string;
  model: string;
}

export interface RuntimeModelState {
  runtimeId: string;
  modelId: string;
  unit: UnitType;
  active: boolean;
  installed: boolean;
  status: UnitStatus;
  progress?: number;
  error?: string;
}

export interface RuntimeRequestState {
  processing: number;
  queued: number;
}

export interface RuntimeSnapshot {
  units: UnitState[];
  models: RuntimeModelState[];
  logs: LogEntry[];
  metrics: RuntimeMetrics;
  npu: NpuState;
  requests: RuntimeRequestState;
  installProgress: number;
  installing: boolean;
  running: boolean;
}

export interface BrowserRpcRequest {
  id: string;
  type:
    | "install"
    | "run"
    | "stop"
    | "hibernate"
    | "heatup"
    | "status"
    | "set_active"
    | "delete_model"
    | "delete_all_models"
    | "infer"
    | "infer_stream";
  units?: RuntimeUnitRequest[];
  payload?: any;
  endpoint?: string;
}
