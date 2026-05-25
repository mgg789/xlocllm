import type {
  BrowserRpcRequest,
  LogEntry,
  ModelSpec,
  NpuState,
  RuntimeMetrics,
  RuntimeModelState,
  RuntimeRequestState,
  RuntimeSnapshot,
  RuntimeUnitRequest,
  UnitState,
  UnitType,
} from "../types";
import { catalog, resolveModel, unitDefinitions } from "../catalog";

type RuntimeInstance = {
  model: ModelSpec;
  engine?: any;
  pipeline?: any;
  active: boolean;
  installed: boolean;
  status: UnitState["status"];
  progress?: number;
  error?: string;
};

type Listener = () => void;
type InstallBatch = {
  completed: number;
  total: number;
};

export class RuntimeHost {
  private instances = new Map<string, RuntimeInstance>();
  private logs: LogEntry[] = [];
  private listeners = new Set<Listener>();
  private installing = false;
  private installProgress = 0;
  private running = false;
  private npuAvailable = false;
  private npu: NpuState = { status: "unavailable", reason: "WebNN probe has not completed" };
  private requests: RuntimeRequestState = { processing: 0, queued: 0 };

  constructor() {
    void this.probeNpu();
  }

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  snapshot(): RuntimeSnapshot {
    const models = [...this.instances.values()].map((instance) => this.toRuntimeModelState(instance));
    return {
      units: unitDefinitions.map((unit) => this.unitState(unit.type)),
      models,
      logs: this.logs.slice(-200),
      metrics: this.metrics(),
      npu: this.npu,
      requests: { ...this.requests },
      installProgress: this.installProgress,
      installing: this.installing,
      running: this.running,
    };
  }

  addModel(model: ModelSpec, active = true): RuntimeModelState {
    const current = this.instances.get(model.modelId);
    if (current) {
      current.active = active;
      if (current.status === "off") current.status = "selected";
      this.emit();
      return this.toRuntimeModelState(current);
    }
    const instance: RuntimeInstance = {
      model,
      active,
      installed: false,
      status: "selected",
    };
    this.instances.set(model.modelId, instance);
    this.log("info", `Added ${model.label} to runtime`);
    this.emit();
    return this.toRuntimeModelState(instance);
  }

  addModelById(modelId: string, active = true): RuntimeModelState {
    return this.addModel(this.requireAnyModel(modelId), active);
  }

  setModelActive(modelId: string, active: boolean): RuntimeModelState {
    const instance = this.instances.get(modelId) ?? this.addMissingModel(modelId);
    instance.active = active;
    if (!active && instance.status === "running") {
      void this.dispose(instance).then(() => {
        instance.status = instance.installed ? "ready" : "selected";
        this.running = this.anyRunning();
        this.emit();
      });
    } else {
      this.emit();
    }
    return this.toRuntimeModelState(instance);
  }

  async handleRpc(request: BrowserRpcRequest, emitStream?: (chunk: string) => void): Promise<any> {
    switch (request.type) {
      case "install":
        return this.install(request.units ?? []);
      case "run":
        return this.run(request.units ?? []);
      case "stop":
        return this.stop();
      case "hibernate":
        return this.hibernate();
      case "heatup":
        return this.heatup();
      case "status":
        return this.status();
      case "set_active":
        return this.setActiveFromRpc(request.payload ?? {});
      case "delete_model":
        return this.deleteModel(request.payload?.unit, request.payload?.model);
      case "delete_all_models":
        return this.deleteAllModels();
      case "infer":
        return this.infer(request.endpoint ?? "", request.payload ?? {});
      case "infer_stream":
        return this.inferStream(request.endpoint ?? "", request.payload ?? {}, emitStream);
      default:
        throw new Error(`Unsupported RPC type: ${(request as BrowserRpcRequest).type}`);
    }
  }

  async install(units: RuntimeUnitRequest[]): Promise<any> {
    const models = this.modelsFromRequests(units);
    if (models.length === 0) return this.status();
    this.installing = true;
    this.installProgress = 0;
    this.emit();
    try {
      for (const [index, model] of models.entries()) {
        const batch = { completed: index, total: models.length };
        const instance = this.ensureRuntimeModel(model, true);
        this.log("info", `Installing ${model.label}`);
        instance.status = "installing";
        instance.progress = 0;
        instance.error = undefined;
        this.installProgress = this.batchProgress(batch, 0);
        this.emit();
        try {
          await this.loadModel(model, true, instance, batch);
          instance.installed = true;
          instance.status = "ready";
          instance.progress = 100;
          this.installProgress = this.batchProgress({ completed: index + 1, total: models.length }, 0);
          this.log("info", `${model.label} is ready`);
        } catch (error) {
          instance.status = "error";
          instance.error = String(error instanceof Error ? error.message : error);
          this.log("error", `${model.label} install failed: ${instance.error}`);
          throw error;
        } finally {
          this.emit();
        }
      }
      this.installProgress = 100;
      return this.status();
    } finally {
      this.installing = false;
      this.emit();
    }
  }

  async run(units: RuntimeUnitRequest[]): Promise<any> {
    if (this.installing) {
      throw new Error("Runtime is installing models");
    }
    const models = this.modelsFromRequests(units);
    for (const model of models) {
      const instance = this.ensureRuntimeModel(model, true);
      this.log("info", `Starting ${model.label}`);
      try {
        const loaded = await this.loadModel(model, false, instance);
        this.instances.set(model.modelId, {
          ...loaded,
          active: true,
          installed: true,
          status: "running",
        });
        this.log("info", `${model.label} is running`);
      } catch (error) {
        instance.status = "error";
        instance.error = String(error instanceof Error ? error.message : error);
        this.log("error", `${model.label} run failed: ${instance.error}`);
        throw error;
      } finally {
        this.emit();
      }
    }
    this.running = this.anyRunning();
    this.emit();
    return this.status();
  }

  async stop(): Promise<any> {
    for (const instance of this.instances.values()) {
      if (instance.status === "running") {
        await this.dispose(instance);
        instance.status = instance.installed ? "ready" : "selected";
      }
    }
    this.running = false;
    this.log("info", "Runtime stopped");
    this.emit();
    return this.status();
  }

  async hibernate(): Promise<any> {
    for (const instance of this.instances.values()) {
      if (!instance.active) continue;
      if (instance.status === "running") await this.dispose(instance);
      if (instance.installed || instance.status === "ready") {
        instance.status = "hibernated";
      }
    }
    this.running = false;
    this.log("info", "Runtime hibernated");
    this.emit();
    return this.status();
  }

  async heatup(): Promise<any> {
    const active = [...this.instances.values()]
      .filter((instance) => instance.active)
      .map((instance) => ({ type: instance.model.unit, model: instance.model.modelId }));
    await this.run(active);
    await Promise.all(
      [...this.instances.values()]
        .filter((instance) => instance.active && instance.status === "running")
        .map((instance) =>
          this.warmup(instance).catch((error) => {
            this.log("warn", `${instance.model.label} warmup skipped: ${String(error)}`);
          }),
        ),
    );
    this.log("info", "Runtime heatup completed");
    this.emit();
    return this.status();
  }

  status(): any {
    const snapshot = this.snapshot();
    return {
      ok: true,
      connected: true,
      ...snapshot,
      catalogModels: catalog.models,
      catalogModelCount: catalog.models.length,
    };
  }

  async deleteModel(unit?: string, modelName?: string): Promise<any> {
    const model = this.modelFromDeletePayload(unit, modelName);
    const instance = this.instances.get(model.modelId);
    if (instance) {
      await this.dispose(instance);
      this.instances.delete(model.modelId);
    }
    const hf = await this.tryTransformers();
    if (hf?.ModelRegistry?.clear_pipeline_cache) {
      await hf.ModelRegistry.clear_pipeline_cache(model.task, this.backendModelId(model), this.modelOptions(model, false));
    }
    this.running = this.anyRunning();
    this.log("info", `Deleted ${model.label} from runtime and requested cache cleanup`);
    this.emit();
    return this.status();
  }

  async deleteAllModels(): Promise<any> {
    for (const instance of this.instances.values()) {
      await this.dispose(instance);
      instance.installed = false;
      instance.status = "selected";
      instance.progress = undefined;
      instance.error = undefined;
    }
    const hf = await this.tryTransformers();
    if (hf?.env) {
      try {
        const cacheName = hf.env.cacheKey ?? "transformers-cache";
        await caches.delete(cacheName);
      } catch (error) {
        this.log("warn", `Browser cache cleanup failed: ${String(error)}`);
      }
    }
    this.running = false;
    this.log("info", "All known model cache entries were cleared");
    this.emit();
    return this.status();
  }

  async infer(endpoint: string, payload: any): Promise<any> {
    return this.trackRequest(() => this.inferImpl(endpoint, payload));
  }

  async inferStream(endpoint: string, payload: any, emitStream?: (chunk: string) => void): Promise<any> {
    return this.trackRequest(async () => {
      if (endpoint !== "chat.completions") {
        const result = await this.inferImpl(endpoint, payload);
        emitStream?.(JSON.stringify(result));
        return result;
      }
      const instance = await this.getInstanceOrLoad("LLM", payload.model);
      const messages = payload.messages ?? [{ role: "user", content: payload.prompt ?? "" }];
      if (instance.model.runtime === "mlc" && instance.engine?.chat?.completions?.create) {
        const stream = await instance.engine.chat.completions.create({
        ...payload,
        model: this.backendModelId(instance.model),
        messages,
        stream: true,
        });
        let content = "";
        for await (const chunk of stream) {
          const delta = chunk?.choices?.[0]?.delta?.content ?? "";
          if (delta) {
            content += delta;
            emitStream?.(delta);
          }
        }
        return { content };
      }
      const result = await this.chat({ ...payload, messages, stream: false });
      const content = result.content ?? result.choices?.[0]?.message?.content ?? "";
      for (const piece of splitText(content)) emitStream?.(piece);
      return { content };
    });
  }

  private async inferImpl(endpoint: string, payload: any): Promise<any> {
    if (endpoint === "chat.completions") return this.chat(payload);
    if (endpoint === "responses") return this.responses(payload);
    if (endpoint === "embeddings") return this.embeddings(payload);
    if (endpoint === "rerank") return this.rerank(payload);
    if (endpoint === "translate") return this.translate(payload);
    if (endpoint === "tts") return this.tts(payload);
    if (endpoint === "image.classify") return this.runPipeline("image-classification", payload.image, payload.options);
    if (endpoint === "image.detect") return this.runPipeline("object-detection", payload.image, payload.options);
    if (endpoint === "image.segment") return this.runPipeline("image-segmentation", payload.image, payload.options);
    if (endpoint === "depth") return this.runPipeline("depth-estimation", payload.image, payload.options);
    if (endpoint === "image-to-text") return this.runPipeline("vlm", payload.image, payload.options);
    if (endpoint === "asr") return this.runPipeline("asr", payload.audio, payload.options);
    if (endpoint === "zero-shot-image") {
      const instance = this.requireInstance("zero-shot-image");
      return instance.pipeline(payload.image, payload.labels ?? payload.candidate_labels ?? []);
    }
    throw new Error(`Unsupported inference endpoint: ${endpoint}`);
  }

  private async chat(payload: any): Promise<any> {
    const instance = await this.getInstanceOrLoad("LLM", payload.model);
    const messages = payload.messages ?? [{ role: "user", content: payload.prompt ?? "" }];
    if (instance.model.runtime === "mlc" && instance.engine?.chat?.completions?.create) {
      const result = await instance.engine.chat.completions.create({
        ...payload,
        model: this.backendModelId(instance.model),
        messages,
        stream: false,
      });
      return { content: result?.choices?.[0]?.message?.content ?? "", raw: result };
    }
    if (!instance.pipeline) throw new Error("LLM pipeline is not loaded");
    const output = await instance.pipeline(messages, {
      max_new_tokens: payload.max_tokens ?? payload.max_completion_tokens ?? 256,
      temperature: payload.temperature ?? 0.7,
      do_sample: (payload.temperature ?? 0.7) > 0,
    });
    return { content: extractGeneratedText(output) };
  }

  private async responses(payload: any): Promise<any> {
    const input = Array.isArray(payload.input) ? payload.input : [{ role: "user", content: String(payload.input ?? "") }];
    return this.chat({ ...payload, messages: input });
  }

  private async embeddings(payload: any): Promise<any> {
    const instance = await this.getInstanceOrLoad("embedding", payload.model);
    const input = Array.isArray(payload.input) ? payload.input : [payload.input ?? ""];
    const tensor = await instance.pipeline(input, { pooling: "mean", normalize: true });
    return { embeddings: typeof tensor.tolist === "function" ? tensor.tolist() : tensor };
  }

  private async rerank(payload: any): Promise<any> {
    const instance = await this.getInstanceOrLoad("reranker", payload.model);
    const query = payload.query ?? "";
    const documents = payload.documents ?? [];
    const scores = [];
    for (const [index, document] of documents.entries()) {
      const output = await instance.pipeline(`${query} [SEP] ${document}`);
      const first = Array.isArray(output) ? output[0] : output;
      scores.push({ index, document, score: first?.score ?? 0, raw: output });
    }
    return { results: scores.sort((a, b) => b.score - a.score) };
  }

  private async translate(payload: any): Promise<any> {
    const instance = await this.getInstanceOrLoad("translator", payload.model);
    return instance.pipeline(payload.text ?? payload.input ?? "", {
      src_lang: payload.src_lang,
      tgt_lang: payload.tgt_lang,
      ...payload.options,
    });
  }

  private async tts(payload: any): Promise<any> {
    const instance = await this.getInstanceOrLoad("tts", payload.model);
    const result = await instance.pipeline(payload.text ?? payload.input ?? "", payload.options ?? {});
    return serializeBinaryLike(result);
  }

  private async runPipeline(unit: UnitType, input: any, options?: any): Promise<any> {
    const instance = await this.getInstanceOrLoad(unit, options?.model);
    return instance.pipeline(input, options ?? {});
  }

  private async loadModel(model: ModelSpec, installOnly: boolean, target?: RuntimeInstance, batch?: InstallBatch): Promise<RuntimeInstance> {
    if (model.runtime === "mlc") {
      const mlc = await import("@mlc-ai/web-llm");
      const backendModelId = this.backendModelId(model);
      const engine = await mlc.CreateMLCEngine(backendModelId, {
        appConfig: mlc.prebuiltAppConfig,
        initProgressCallback: (progress: any) => {
          const text = progress?.text ?? progress?.status ?? "loading";
          if (typeof progress?.progress === "number") {
            this.updateInstallProgress(target, progress.progress, batch);
          }
          this.log("info", `${model.label}: ${text}`);
        },
      });
      if (installOnly && engine?.unload) {
        await engine.unload();
        return { model, active: target?.active ?? true, installed: true, status: "ready" };
      }
      return { model, engine, active: target?.active ?? true, installed: true, status: "running" };
    }

    const hf = await import("@huggingface/transformers");
    const preferNpu = Boolean(model.npuEligible && this.npuAvailable);
    try {
      const pipe = await hf.pipeline(model.task as any, this.backendModelId(model), this.pipelineOptions(model, preferNpu, target, batch) as any);
      if (preferNpu) {
        this.npu = { status: "active", backend: "webnn-npu", reason: "WebNN pipeline loaded" };
      }
      if (installOnly && pipe?.dispose) {
        await pipe.dispose();
        return { model, active: target?.active ?? true, installed: true, status: "ready" };
      }
      return { model, pipeline: pipe, active: target?.active ?? true, installed: true, status: "running" };
    } catch (error) {
      if (!preferNpu) throw error;
      this.npu = { status: "fallback", backend: "webgpu", reason: String(error instanceof Error ? error.message : error) };
      this.log("warn", `${model.label}: WebNN/NPU load failed, falling back to WebGPU`);
      const pipe = await hf.pipeline(model.task as any, this.backendModelId(model), this.pipelineOptions(model, false, target, batch) as any);
      if (installOnly && pipe?.dispose) {
        await pipe.dispose();
        return { model, active: target?.active ?? true, installed: true, status: "ready" };
      }
      return { model, pipeline: pipe, active: target?.active ?? true, installed: true, status: "running" };
    }
  }

  private async warmup(instance: RuntimeInstance): Promise<void> {
    if (instance.model.unit === "LLM") {
      await this.chat({ model: instance.model.modelId, messages: [{ role: "user", content: "Hi" }], max_tokens: 1, temperature: 0 });
    } else if (instance.model.unit === "embedding") {
      await this.embeddings({ model: instance.model.modelId, input: "warmup" });
    }
  }

  private async dispose(instance: RuntimeInstance): Promise<void> {
    if (instance.engine?.unload) await instance.engine.unload();
    if (instance.engine?.dispose) await instance.engine.dispose();
    if (instance.pipeline?.dispose) await instance.pipeline.dispose();
    instance.engine = undefined;
    instance.pipeline = undefined;
  }

  private modelsFromRequests(units: RuntimeUnitRequest[]): ModelSpec[] {
    if (units.length === 0) {
      return [...this.instances.values()]
        .filter((instance) => instance.active)
        .map((instance) => instance.model);
    }
    return units.map((unit) => {
      const model = this.requireModel(unit.type, unit.model);
      this.ensureRuntimeModel(model, true);
      return model;
    });
  }

  private ensureRuntimeModel(model: ModelSpec, active: boolean): RuntimeInstance {
    const current = this.instances.get(model.modelId);
    if (current) {
      current.active = active || current.active;
      return current;
    }
    const instance: RuntimeInstance = {
      model,
      active,
      installed: false,
      status: "selected",
    };
    this.instances.set(model.modelId, instance);
    return instance;
  }

  private addMissingModel(modelId: string): RuntimeInstance {
    const model = this.requireAnyModel(modelId);
    return this.ensureRuntimeModel(model, true);
  }

  private requireModel(unit: string, modelName: string): ModelSpec {
    const model = resolveModel(unit, modelName);
    if (!model) throw new Error(`Model not found for unit=${unit} model=${modelName}`);
    return model;
  }

  private requireAnyModel(modelName: string): ModelSpec {
    const normalized = normalize(modelName);
    const model = catalog.models.find((candidate) => {
      return (
        normalize(candidate.modelId) === normalized ||
        normalize(candidate.label) === normalized ||
        candidate.aliases.some((alias) => normalize(alias) === normalized)
      );
    });
    if (!model) throw new Error(`Model not found: ${modelName}`);
    return model;
  }

  private requireInstance(unit: UnitType): RuntimeInstance {
    const instance = [...this.instances.values()].find(
      (candidate) => candidate.model.unit === unit && candidate.active && candidate.status === "running",
    );
    if (!instance) {
      throw new Error(`${unit} unit is not running. Add a model, activate it, and press Run.`);
    }
    return instance;
  }

  private async getInstanceOrLoad(unit: UnitType, modelName?: string): Promise<RuntimeInstance> {
    if (modelName) {
      const model = resolveModel(unit, modelName);
      if (model) {
        const current = this.instances.get(model.modelId);
        if (current?.status === "running") return current;
        this.log("info", `Auto-loading ${model.label} for ${unit}`);
        const target = this.ensureRuntimeModel(model, true);
        const loaded = await this.loadModel(model, false, target);
        const running = { ...loaded, active: true, installed: true, status: "running" as const };
        this.instances.set(model.modelId, running);
        this.running = true;
        this.emit();
        return running;
      }
    }

    const running = [...this.instances.values()].find(
      (instance) => instance.model.unit === unit && instance.active && instance.status === "running",
    );
    if (running) return running;

    const active = [...this.instances.values()].find((instance) => instance.model.unit === unit && instance.active);
    if (!active) return this.requireInstance(unit);
    const loaded = await this.loadModel(active.model, false, active);
    const next = { ...loaded, active: true, installed: true, status: "running" as const };
    this.instances.set(active.model.modelId, next);
    this.running = true;
    this.emit();
    return next;
  }

  private modelFromDeletePayload(unit?: string, modelName?: string): ModelSpec {
    if (unit && modelName) return this.requireModel(unit, modelName);
    if (modelName) return this.requireAnyModel(modelName);
    if (unit) return this.requireAnyModel(unit);
    throw new Error("unit/model is required");
  }

  private setActiveFromRpc(payload: { model?: string; active?: boolean; unit?: string }): any {
    const model = payload.unit && payload.model ? this.requireModel(payload.unit, payload.model) : this.requireAnyModel(payload.model ?? "");
    this.setModelActive(model.modelId, payload.active ?? true);
    return this.status();
  }

  private pipelineOptions(model: ModelSpec, preferNpu: boolean, target?: RuntimeInstance, batch?: InstallBatch): Record<string, unknown> {
    const options: Record<string, unknown> = {
      ...this.modelOptions(model, preferNpu),
      progress_callback: (progress: any) => {
        if (progress?.status === "progress" && typeof progress.progress === "number") {
          this.updateInstallProgress(target, progress.progress, batch);
          this.log("info", `${model.label}: ${Math.round(progress.progress)}% ${progress.file ?? ""}`);
          this.emit();
        }
      },
    };
    return options;
  }

  private modelOptions(model: ModelSpec, preferNpu: boolean): Record<string, unknown> {
    const options: Record<string, unknown> = {
      device: preferNpu ? "webnn-npu" : "webgpu",
    };
    if (model.dtype && model.dtype !== "auto") {
      options.dtype = model.dtype;
    }
    return options;
  }

  private backendModelId(model: ModelSpec): string {
    return model.backendModelId ?? model.modelId;
  }

  private updateInstallProgress(target: RuntimeInstance | undefined, rawProgress: number, batch?: InstallBatch): void {
    const normalized = rawProgress <= 1 ? rawProgress * 100 : rawProgress;
    const capped = Math.min(95, Math.max(0, Math.round(normalized)));
    if (target) {
      target.progress = Math.max(target.progress ?? 0, capped);
    }
    if (batch) {
      this.installProgress = this.batchProgress(batch, target?.progress ?? capped);
    }
  }

  private batchProgress(batch: InstallBatch, currentModelProgress: number): number {
    if (batch.total <= 0) return 0;
    return Math.max(0, Math.min(100, Math.round(((batch.completed * 100) + currentModelProgress) / batch.total)));
  }

  private async tryTransformers(): Promise<any | undefined> {
    try {
      return await import("@huggingface/transformers");
    } catch {
      return undefined;
    }
  }

  private async probeNpu(): Promise<void> {
    const nav = navigator as Navigator & { ml?: { createContext?: (options?: Record<string, unknown>) => Promise<unknown> } };
    if (!nav.ml?.createContext) {
      this.npu = { status: "unavailable", reason: "WebNN API is not exposed by this browser" };
      this.emit();
      return;
    }
    try {
      await nav.ml.createContext({ deviceType: "npu" });
      this.npuAvailable = true;
      this.npu = { status: "active", backend: "webnn-npu", reason: "WebNN NPU context is available" };
    } catch (error) {
      this.npuAvailable = false;
      this.npu = { status: "fallback", backend: "webgpu", reason: String(error instanceof Error ? error.message : error) };
    }
    this.emit();
  }

  private metrics(): RuntimeMetrics {
    const running = [...this.instances.values()].filter((instance) => instance.status === "running");
    const installed = [...this.instances.values()].filter((instance) => instance.installed || instance.status === "running");
    const vram = running.reduce((sum, instance) => sum + instance.model.vramMB, 0);
    const disk = installed.reduce((sum, instance) => sum + instance.model.diskMB, 0);
    const memory = (performance as any).memory;
    return {
      gpu: running.length ? Math.min(100, Math.round(vram / 80)) : 0,
      cpu: running.length ? Math.min(100, running.length * 12) : 0,
      ram: memory?.usedJSHeapSize && memory?.jsHeapSizeLimit ? Math.round((memory.usedJSHeapSize / memory.jsHeapSizeLimit) * 100) : null,
      disk: disk ? Math.min(100, Math.round(disk / 100)) : 0,
    };
  }

  private unitState(unit: UnitType): UnitState {
    const models = [...this.instances.values()].filter((instance) => instance.model.unit === unit);
    const selected = models.find((instance) => instance.active) ?? models[0];
    const statuses = models.map((instance) => instance.status);
    const priority: UnitState["status"][] = ["error", "installing", "running", "hibernated", "ready", "selected"];
    const status = priority.find((candidate) => statuses.includes(candidate)) ?? "off";
    return {
      type: unit,
      selectedModelId: selected?.model.modelId,
      active: models.some((instance) => instance.active),
      status,
      progress: selected?.progress,
      error: selected?.error,
    };
  }

  private toRuntimeModelState(instance: RuntimeInstance): RuntimeModelState {
    return {
      runtimeId: instance.model.modelId,
      modelId: instance.model.modelId,
      unit: instance.model.unit,
      active: instance.active,
      installed: instance.installed,
      status: instance.status,
      progress: instance.progress,
      error: instance.error,
    };
  }

  private anyRunning(): boolean {
    return [...this.instances.values()].some((instance) => instance.status === "running");
  }

  private async trackRequest<T>(fn: () => Promise<T>): Promise<T> {
    this.requests.processing += 1;
    this.emit();
    try {
      return await fn();
    } finally {
      this.requests.processing = Math.max(0, this.requests.processing - 1);
      this.emit();
    }
  }

  private log(level: LogEntry["level"], message: string): void {
    this.logs.push({ time: new Date().toISOString(), level, message });
    this.logs = this.logs.slice(-300);
    this.emit();
  }

  private emit(): void {
    for (const listener of this.listeners) listener();
  }
}

function normalize(value: string): string {
  return value.trim().toLowerCase().replace(/[_\s]+/g, "-");
}

function extractGeneratedText(output: any): string {
  if (typeof output === "string") return output;
  if (Array.isArray(output)) {
    const first = output[0];
    if (typeof first?.generated_text === "string") return first.generated_text;
    if (Array.isArray(first?.generated_text)) return first.generated_text.at(-1)?.content ?? JSON.stringify(output);
  }
  return JSON.stringify(output);
}

function serializeBinaryLike(result: any): any {
  if (result?.audio instanceof Float32Array) {
    return { audio: Array.from(result.audio), sampling_rate: result.sampling_rate };
  }
  return result;
}

function splitText(text: string): string[] {
  const chunks = [];
  for (let index = 0; index < text.length; index += 24) {
    chunks.push(text.slice(index, index + 24));
  }
  return chunks.length ? chunks : [""];
}
