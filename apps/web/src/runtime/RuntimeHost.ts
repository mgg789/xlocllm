import type {
  BrowserRpcRequest,
  LogEntry,
  ModelSpec,
  NpuState,
  RuntimeMetrics,
  RuntimeModelState,
  RuntimeRequestState,
  RuntimeServiceState,
  RuntimeSnapshot,
  RuntimeUnitRequest,
  UnitState,
  UnitType,
} from "../types";
import {
  catalog,
  resolveModel,
  supportedModelsForCapabilities,
  supportsCpuFallback,
  supportsReasoning,
  unitDefinitions,
} from "../catalog";
import {
  VectorStorageRegistry,
  chunkText,
  type VectorAddItem,
  type VectorMetric,
  type VectorSearchResult,
  type VectorStoreConfig,
} from "./VectorStore";

type RuntimeInstance = {
  model: ModelSpec;
  engine?: any;
  pipeline?: any;
  active: boolean;
  installed: boolean;
  status: UnitState["status"];
  reasoning?: boolean | null;
  options?: Record<string, unknown>;
  ragId?: string;
  progress?: number;
  error?: string;
};

type RagConfig = {
  name: string;
  emb: RuntimeUnitRequest;
  rerank?: RuntimeUnitRequest | null;
  store: VectorStoreConfig;
  chunkSize: number;
  chunkOverlap: number;
  topK: number;
  candidateK: number;
  scoreThreshold?: number | null;
  options?: Record<string, unknown>;
  active: boolean;
  status: UnitState["status"];
  error?: string;
};

type Listener = () => void;
type InstallBatch = {
  completed: number;
  total: number;
};

export class RuntimeHost {
  private instances = new Map<string, RuntimeInstance>();
  private vectorStores = new VectorStorageRegistry();
  private rags = new Map<string, RagConfig>();
  private logs: LogEntry[] = [];
  private listeners = new Set<Listener>();
  private installing = false;
  private installProgress = 0;
  private running = false;
  private webgpuAvailable = Boolean((navigator as Navigator & { gpu?: unknown }).gpu);
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
    const catalogModels = this.supportedCatalogModels();
    return {
      units: unitDefinitions.map((unit) => this.unitState(unit.type)),
      models,
      services: this.serviceStates(),
      logs: this.logs.slice(-200),
      metrics: this.metrics(),
      npu: this.npu,
      capabilities: this.capabilities(catalogModels.length),
      requests: { ...this.requests },
      catalogModels,
      catalogModelCount: catalog.models.length,
      installProgress: this.installProgress,
      installing: this.installing,
      running: this.running,
    };
  }

  addModel(model: ModelSpec, active = true): RuntimeModelState {
    this.assertModelSupported(model);
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
      case "configure_unit":
        return this.configureUnitFromRpc(request.payload ?? {});
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
      catalogModels: snapshot.catalogModels,
      catalogModelCount: snapshot.catalogModelCount,
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
      const reasoning = this.resolveReasoning(instance, payload);
      if (instance.model.runtime === "mlc" && instance.engine?.chat?.completions?.create) {
        const stream = await instance.engine.chat.completions.create({
          ...payload,
          ...instance.options,
          model: this.backendModelId(instance.model),
          messages: this.messagesWithReasoningMarker(instance.model, messages, reasoning),
          extra_body: this.extraBodyWithReasoning(payload.extra_body, reasoning),
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
    const route = normalizeEndpoint(endpoint);
    switch (route) {
      case "chat.completions":
      case "chat":
        return this.chat(payload);
      case "responses":
        return this.responses(payload);
      case "embeddings":
      case "embedding":
        return this.embeddings(payload);
      case "rerank":
      case "reranker":
        return this.rerank(payload);
      case "translate":
      case "translator":
        return this.translate(payload);
      case "tts":
        return this.tts(payload);
      case "image.classify":
      case "image-classification":
        return this.classification("image-classification", imageInput(payload), payload);
      case "image.detect":
      case "object-detection":
        return this.detection("object-detection", imageInput(payload), payload);
      case "image.segment":
      case "image-segmentation":
        return this.runPipelineResult("image-segmentation", imageInput(payload), payload, "segments");
      case "depth":
      case "depth-estimation":
        return this.runPipelineResult("depth-estimation", imageInput(payload), payload, "depth");
      case "image-to-text":
      case "vlm":
      case "ocr":
        return this.generatedText(payload, route === "ocr" ? "ocr" : "vlm", imageInput(payload));
      case "asr":
      case "speech-to-text":
        return this.speechToText(payload);
      case "zero-shot-image":
        return this.zeroShotImage(payload);
      case "language-id":
        return this.classification("language-id", audioInput(payload), payload);
      case "audio-classification":
      case "audio.classify":
        return this.classification("audio-classification", audioInput(payload), payload);
      case "document-layout":
        return this.detection("document-layout", imageInput(payload), payload);
      case "table-detection":
        return this.detection("table-detection", imageInput(payload), payload);
      case "document-qa":
        return this.documentQuestionAnswering(payload);
      case "text-classification":
      case "text.classify":
        return this.classification("text-classification", textInput(payload), payload);
      case "ner":
      case "token-classification":
        return this.runPipelineResult("ner", textInput(payload), payload, "entities");
      case "zero-shot-text":
      case "zero-shot-classification":
        return this.zeroShotText(payload);
      case "summarization":
      case "summarize":
        return this.generatedText(payload, "summarization", textInput(payload), "summary");
      case "text2text":
      case "text2text-generation":
        return this.generatedText(payload, "text2text", textInput(payload), "text");
      case "code":
      case "code.embed":
        return this.code(payload);
      case "vector.add":
        return this.vectorAdd(payload);
      case "vector.search":
        return this.vectorSearch(payload);
      case "vector.delete":
        return this.vectorDelete(payload);
      case "vector.clear":
        return this.vectorClear(payload);
      case "vector.stats":
        return this.vectorStats(payload);
      case "rag.add":
        return this.ragAdd(payload);
      case "rag.search":
        return this.ragSearch(payload);
      case "rag.delete":
        return this.ragDelete(payload);
      case "rag.clear":
        return this.ragClear(payload);
      case "rag.reindex":
        return this.ragReindex(payload);
      case "rag.stats":
        return this.ragStats(payload);
      default:
        throw new Error(`Unsupported inference endpoint: ${endpoint}`);
    }
  }

  private async chat(payload: any): Promise<any> {
    const instance = await this.getInstanceOrLoad("LLM", payload.model);
    const baseMessages = payload.messages ?? [{ role: "user", content: payload.prompt ?? "" }];
    const ragContext = await this.ragContextForChat(instance, payload, baseMessages);
    const messages = ragContext ? messagesWithRagContext(baseMessages, ragContext) : baseMessages;
    const reasoning = this.resolveReasoning(instance, payload);
    if (instance.model.runtime === "mlc" && instance.engine?.chat?.completions?.create) {
      const result = await instance.engine.chat.completions.create({
        ...payload,
        ...instance.options,
        model: this.backendModelId(instance.model),
        messages: this.messagesWithReasoningMarker(instance.model, messages, reasoning),
        extra_body: this.extraBodyWithReasoning(payload.extra_body, reasoning),
        stream: false,
      });
      return {
        content: result?.choices?.[0]?.message?.content ?? "",
        raw: ragContext ? { ...result, rag: ragContext } : result,
        ...(ragContext ? { rag: ragContext } : {}),
      };
    }
    if (!instance.pipeline) throw new Error("LLM pipeline is not loaded");
    const output = await instance.pipeline(messages, this.generationOptions(instance, payload, reasoning));
    return { content: extractGeneratedText(output), raw: ragContext ? { rag: ragContext } : output, ...(ragContext ? { rag: ragContext } : {}) };
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
    return instance.pipeline(input, this.pipelineCallOptions(instance, options));
  }

  private async runPipelineResult(unit: UnitType, input: any, payload: any, key: string): Promise<any> {
    const result = await this.runPipeline(unit, input, pipelinePayloadOptions(payload));
    return { [key]: normalizeArrayResult(result), raw: result };
  }

  private async classification(unit: UnitType, input: any, payload: any): Promise<any> {
    const result = await this.runPipeline(unit, input, pipelinePayloadOptions(payload));
    return { labels: normalizeArrayResult(result), raw: result };
  }

  private async detection(unit: UnitType, input: any, payload: any): Promise<any> {
    const result = await this.runPipeline(unit, input, pipelinePayloadOptions(payload));
    return { boxes: normalizeArrayResult(result), raw: result };
  }

  private async generatedText(payload: any, unit: UnitType, input: any, key = "text"): Promise<any> {
    const result = await this.runPipeline(unit, input, pipelinePayloadOptions(payload));
    return { [key]: extractGeneratedText(result), raw: result };
  }

  private async speechToText(payload: any): Promise<any> {
    const result = await this.runPipeline("asr", audioInput(payload), pipelinePayloadOptions(payload));
    return { text: extractGeneratedText(result), chunks: Array.isArray(result?.chunks) ? result.chunks : undefined, raw: result };
  }

  private async zeroShotImage(payload: any): Promise<any> {
    const instance = await this.getInstanceOrLoad("zero-shot-image", payload.model);
    const labels = labelsInput(payload);
    const result = await instance.pipeline(imageInput(payload), labels, this.pipelineCallOptions(instance, payload.options));
    return { labels: normalizeArrayResult(result), raw: result };
  }

  private async zeroShotText(payload: any): Promise<any> {
    const instance = await this.getInstanceOrLoad("zero-shot-text", payload.model);
    const result = await instance.pipeline(textInput(payload), labelsInput(payload), this.pipelineCallOptions(instance, payload.options));
    return { labels: normalizeArrayResult(result), raw: result };
  }

  private async documentQuestionAnswering(payload: any): Promise<any> {
    const instance = await this.getInstanceOrLoad("document-qa", payload.model);
    const options = this.pipelineCallOptions(instance, payload.options);
    const image = imageInput(payload);
    const question = String(payload.question ?? payload.query ?? "");
    if (!question) throw new Error("document-qa requires question or query");
    let result: any;
    try {
      result = await instance.pipeline(image, question, options);
    } catch {
      result = await instance.pipeline({ image, question }, options);
    }
    return { answers: normalizeArrayResult(result), raw: result };
  }

  private async code(payload: any): Promise<any> {
    const result = await this.runPipeline("code", textInput(payload), pipelinePayloadOptions(payload));
    return { features: typeof result?.tolist === "function" ? result.tolist() : result, raw: result };
  }

  private async vectorAdd(payload: any): Promise<any> {
    const config = this.vectorConfigFromPayload(payload);
    const items = vectorItemsFromPayload(payload);
    if (items.some((item) => !Array.isArray(item.embedding))) {
      throw new Error("vector.add requires embeddings for every item");
    }
    return this.vectorStores.add(config, items);
  }

  private async vectorSearch(payload: any): Promise<any> {
    const config = this.vectorConfigFromPayload(payload);
    const embedding = payload.embedding ?? payload.queryEmbedding;
    if (!Array.isArray(embedding)) {
      throw new Error("vector.search requires embedding or queryEmbedding");
    }
    return this.vectorStores.search(config, embedding.map(Number), numberOrDefault(payload.top_k ?? payload.topK, 5), payload.filter);
  }

  private async vectorDelete(payload: any): Promise<any> {
    const config = this.vectorConfigFromPayload(payload);
    return this.vectorStores.delete(config, stringArray(payload.ids), payload.filter);
  }

  private async vectorClear(payload: any): Promise<any> {
    const config = this.vectorConfigFromPayload(payload);
    return this.vectorStores.clear(config);
  }

  private async vectorStats(payload: any): Promise<any> {
    const config = this.vectorConfigFromPayload(payload);
    return this.vectorStores.stats(config);
  }

  private async ragAdd(payload: any): Promise<any> {
    const rag = this.ragFromPayload(payload);
    const documents = ragDocumentsFromPayload(payload);
    const chunks = documents.flatMap((document) =>
      chunkText(document.text, rag.chunkSize, rag.chunkOverlap).map((text, index) => ({
        document,
        text,
        index,
      })),
    );
    if (chunks.length === 0) return { ok: true, rag: rag.name, store: rag.store.name, count: 0, ids: [] };
    const embeddings = await this.embeddingVectors(rag.emb, chunks.map((chunk) => chunk.text));
    const items: VectorAddItem[] = chunks.map((chunk, index) => ({
      id: `${chunk.document.id}:${chunk.index}`,
      documentId: chunk.document.id,
      chunkIndex: chunk.index,
      text: chunk.text,
      metadata: { ...(chunk.document.metadata ?? {}), documentId: chunk.document.id },
      embedding: embeddings[index],
      embeddingModel: rag.emb.model,
    }));
    const result = await this.vectorStores.add(rag.store, items);
    return { ...result, rag: rag.name, documents: documents.length };
  }

  private async ragSearch(payload: any): Promise<any> {
    const rag = this.ragFromPayload(payload);
    const query = String(payload.query ?? payload.input ?? payload.prompt ?? "");
    if (!query) throw new Error("rag.search requires query");
    const topK = numberOrDefault(payload.top_k ?? payload.topK, rag.topK);
    const candidateK = Math.max(topK, numberOrDefault(payload.candidate_k ?? payload.candidateK, rag.candidateK));
    const [embedding] = await this.embeddingVectors(rag.emb, [query]);
    const vectorResult = await this.vectorStores.search(rag.store, embedding, candidateK, payload.filter);
    let results = vectorResult.results;
    if (rag.scoreThreshold !== null && rag.scoreThreshold !== undefined) {
      results = results.filter((result) => result.score >= Number(rag.scoreThreshold));
    }
    if (rag.rerank && results.length > 0) {
      results = await this.rerankVectorResults(rag, query, results);
    }
    const finalResults = results.slice(0, topK);
    return {
      ok: true,
      rag: rag.name,
      store: rag.store.name,
      query,
      results: finalResults.map(publicVectorResult),
      context: contextFromResults(finalResults),
    };
  }

  private async ragDelete(payload: any): Promise<any> {
    const rag = this.ragFromPayload(payload);
    const result = await this.vectorStores.delete(rag.store, stringArray(payload.ids), payload.filter);
    return { ...result, rag: rag.name };
  }

  private async ragClear(payload: any): Promise<any> {
    const rag = this.ragFromPayload(payload);
    const result = await this.vectorStores.clear(rag.store);
    return { ...result, rag: rag.name };
  }

  private async ragReindex(payload: any): Promise<any> {
    const rag = this.ragFromPayload(payload);
    const records = await this.vectorStores.records(rag.store);
    if (records.length === 0) return { ok: true, rag: rag.name, store: rag.store.name, count: 0 };
    const embeddings = await this.embeddingVectors(rag.emb, records.map((record) => record.text));
    const items: VectorAddItem[] = records.map((record, index) => ({
      id: record.id,
      documentId: record.documentId,
      chunkIndex: record.chunkIndex,
      text: record.text,
      metadata: record.metadata,
      embedding: embeddings[index],
      embeddingModel: rag.emb.model,
    }));
    const result = await this.vectorStores.add(rag.store, items);
    return { ...result, rag: rag.name, reindexed: result.count };
  }

  private async ragStats(payload: any): Promise<any> {
    const rag = this.ragFromPayload(payload);
    const stats = await this.vectorStores.stats(rag.store);
    return { ...stats, rag: rag.name, embedding_model: rag.emb.model, reranker_model: rag.rerank?.model ?? null };
  }

  private async ragContextForChat(instance: RuntimeInstance, payload: any, messages: any[]): Promise<any | null> {
    const useRag = payload.use_rag ?? payload.useRag ?? payload.extra_body?.use_rag ?? payload.extra_body?.useRag;
    if (useRag === false) return null;
    const ragPayload = payload.rag ?? payload.extra_body?.rag;
    const ragId = ragPayload ? this.configureRagUnit(ragPayload).name : instance.ragId;
    if (!ragId) return null;
    const query = lastUserText(messages);
    if (!query) return null;
    const result = await this.ragSearch({
      rag: ragId,
      query,
      top_k: payload.rag_top_k ?? payload.extra_body?.rag_top_k,
      filter: payload.rag_filter ?? payload.extra_body?.rag_filter,
    });
    return result.results.length > 0 ? result : null;
  }

  private async embeddingVectors(unit: RuntimeUnitRequest, input: string[]): Promise<number[][]> {
    const result = await this.embeddings({ model: unit.model, input });
    const vectors = result.embeddings;
    if (!Array.isArray(vectors) || vectors.length !== input.length) {
      throw new Error(`Embedding model ${unit.model} returned invalid vectors`);
    }
    return vectors.map((vector: unknown) => {
      if (!Array.isArray(vector)) throw new Error(`Embedding model ${unit.model} returned a non-array vector`);
      return vector.map(Number);
    });
  }

  private async rerankVectorResults(rag: RagConfig, query: string, results: VectorSearchResult[]): Promise<VectorSearchResult[]> {
    if (!rag.rerank) return results;
    const reranked = await this.rerank({ model: rag.rerank.model, query, documents: results.map((result) => result.text) });
    const byIndex = new Map<number, number>();
    for (const item of reranked.results ?? []) {
      if (typeof item.index === "number" && typeof item.score === "number") byIndex.set(item.index, item.score);
    }
    return results
      .map((result, index) => ({ ...result, score: byIndex.get(index) ?? result.score, metadata: { ...result.metadata, vectorScore: result.score } }))
      .sort((left, right) => right.score - left.score);
  }

  private generationOptions(instance: RuntimeInstance, payload: any, reasoning: boolean | null): Record<string, unknown> {
    const options: Record<string, unknown> = {
      ...(instance.options ?? {}),
      ...(payload.options ?? {}),
      max_new_tokens: payload.max_tokens ?? payload.max_completion_tokens ?? 256,
      temperature: payload.temperature ?? 0.7,
      do_sample: (payload.temperature ?? 0.7) > 0,
    };
    if (reasoning !== null) {
      options.chat_template_kwargs = {
        ...((instance.options?.chat_template_kwargs as Record<string, unknown> | undefined) ?? {}),
        ...((payload.options?.chat_template_kwargs as Record<string, unknown> | undefined) ?? {}),
        ...(payload.chat_template_kwargs ?? {}),
        ...(payload.extra_body?.chat_template_kwargs ?? {}),
        enable_thinking: reasoning,
      };
    }
    return options;
  }

  private pipelineCallOptions(instance: RuntimeInstance, options?: any): Record<string, unknown> {
    const result: Record<string, unknown> = { ...(instance.options ?? {}), ...(options ?? {}) };
    delete result.model;
    return result;
  }

  private loadedInstance(
    model: ModelSpec,
    target: RuntimeInstance | undefined,
    values: Partial<RuntimeInstance>,
  ): RuntimeInstance {
    return {
      model,
      active: target?.active ?? true,
      installed: values.installed ?? true,
      status: values.status ?? "running",
      reasoning: target?.reasoning,
      options: target?.options ?? {},
      ragId: target?.ragId,
      engine: values.engine,
      pipeline: values.pipeline,
      progress: target?.progress,
      error: target?.error,
    };
  }

  private async loadModel(model: ModelSpec, installOnly: boolean, target?: RuntimeInstance, batch?: InstallBatch): Promise<RuntimeInstance> {
    this.assertModelSupported(model);
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
        return this.loadedInstance(model, target, { installed: true, status: "ready" });
      }
      return this.loadedInstance(model, target, { engine, installed: true, status: "running" });
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
        return this.loadedInstance(model, target, { installed: true, status: "ready" });
      }
      return this.loadedInstance(model, target, { pipeline: pipe, installed: true, status: "running" });
    } catch (error) {
      if (!preferNpu) throw error;
      this.npu = {
        status: "fallback",
        backend: this.webgpuAvailable ? "webgpu" : "wasm",
        reason: String(error instanceof Error ? error.message : error),
      };
      this.log("warn", `${model.label}: WebNN/NPU load failed, falling back to ${this.webgpuAvailable ? "WebGPU" : "WASM"}`);
      const pipe = await hf.pipeline(model.task as any, this.backendModelId(model), this.pipelineOptions(model, false, target, batch) as any);
      if (installOnly && pipe?.dispose) {
        await pipe.dispose();
        return this.loadedInstance(model, target, { installed: true, status: "ready" });
      }
      return this.loadedInstance(model, target, { pipeline: pipe, installed: true, status: "running" });
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
    const modelRequests = this.modelRequestsFromUnits(units);
    return modelRequests.map((unit) => {
      const model = this.requireModel(unit.type, unit.model);
      this.ensureRuntimeModel(model, true, unit);
      return model;
    });
  }

  private modelRequestsFromUnits(units: RuntimeUnitRequest[]): RuntimeUnitRequest[] {
    const requests: RuntimeUnitRequest[] = [];
    for (const unit of units) {
      if (isVectorUnit(unit)) {
        this.configureVectorUnit(unit);
        continue;
      }
      if (isRagUnit(unit)) {
        const rag = this.configureRagUnit(unit);
        requests.push(rag.emb);
        if (rag.rerank) requests.push(rag.rerank);
        continue;
      }
      requests.push(unit);
      const ragPayload = unit.rag ?? (unit.options?.rag as RuntimeUnitRequest | undefined);
      if (ragPayload) {
        const rag = this.configureRagUnit(ragPayload);
        requests.push(rag.emb);
        if (rag.rerank) requests.push(rag.rerank);
      }
    }
    return dedupeModelRequests(requests);
  }

  private ensureRuntimeModel(model: ModelSpec, active: boolean, request?: RuntimeUnitRequest): RuntimeInstance {
    const current = this.instances.get(model.modelId);
    if (current) {
      current.active = active || current.active;
      this.applyUnitRequest(current, request);
      return current;
    }
    const instance: RuntimeInstance = {
      model,
      active,
      installed: false,
      status: "selected",
      options: {},
    };
    this.applyUnitRequest(instance, request);
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
    this.assertModelSupported(model);
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
    this.assertModelSupported(model);
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
        this.assertModelSupported(model);
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

  private configureUnitFromRpc(payload: { unit?: RuntimeUnitRequest; unit_id?: string; reasoning?: boolean | null; options?: Record<string, unknown> }): any {
    const request = payload.unit;
    if (request && isVectorUnit(request)) {
      this.configureVectorUnit(request);
      this.emit();
      return this.status();
    }
    if (request && isRagUnit(request)) {
      this.configureRagUnit(request);
      this.emit();
      return this.status();
    }
    const reasoning = request && "reasoning" in request ? request.reasoning : payload.reasoning;
    let instance: RuntimeInstance | undefined;
    if (request?.type && request.model) {
      const model = this.requireModel(request.type, request.model);
      instance = this.ensureRuntimeModel(model, true, {
        ...request,
        reasoning,
        options: { ...(request.options ?? {}), ...(payload.options ?? {}) },
      });
    } else if (payload.unit_id) {
      const modelId = payload.unit_id.includes(":") ? payload.unit_id.split(":").slice(1).join(":") : payload.unit_id;
      instance = this.instances.get(modelId) ?? [...this.instances.values()].find((candidate) => candidate.model.unit === payload.unit_id);
    }
    if (!instance) throw new Error("Unit is not present in runtime");
    this.applyUnitRequest(instance, {
      type: instance.model.unit,
      model: instance.model.modelId,
      reasoning,
      options: { ...(request?.options ?? {}), ...(payload.options ?? {}) },
    });
    this.log("info", `${instance.model.label} runtime options updated`);
    this.emit();
    return this.status();
  }

  private configureVectorUnit(unit: RuntimeUnitRequest): VectorStoreConfig {
    const options = unit.options ?? {};
    return this.vectorStores.configure({
      name: unit.model || String(options.name ?? "default"),
      backend: String(options.backend ?? "indexeddb"),
      metric: String(options.metric ?? "cosine") as VectorMetric,
      persist: options.persist !== false,
      namespace: String(options.namespace ?? "default"),
      options,
    });
  }

  private configureRagUnit(unit: RuntimeUnitRequest | Record<string, unknown> | string): RagConfig {
    if (typeof unit === "string") {
      const existing = this.rags.get(unit);
      if (!existing) throw new Error(`RAG unit not found: ${unit}`);
      return existing;
    }
    const request = unit as RuntimeUnitRequest;
    if (!isRagUnit(request)) throw new Error("RAG unit payload is required");
    const options = request.options ?? {};
    const emb = normalizeNestedRequest(options.emb);
    if (!emb) throw new Error("RAG unit requires options.emb");
    const rerank = normalizeNestedRequest(options.rerank);
    const storeRequest = normalizeNestedRequest(options.store);
    const store = storeRequest ? this.configureVectorUnit(storeRequest) : this.configureVectorUnit(defaultVectorUnit(`${request.model}-store`));
    const rag: RagConfig = {
      name: request.model || "default",
      emb,
      rerank,
      store,
      chunkSize: numberOrDefault(options.chunk_size ?? options.chunkSize, 800),
      chunkOverlap: numberOrDefault(options.chunk_overlap ?? options.chunkOverlap, 120),
      topK: numberOrDefault(options.top_k ?? options.topK, 5),
      candidateK: numberOrDefault(options.candidate_k ?? options.candidateK, 30),
      scoreThreshold: typeof options.score_threshold === "number" ? options.score_threshold : typeof options.scoreThreshold === "number" ? options.scoreThreshold : null,
      options,
      active: true,
      status: "selected",
    };
    this.rags.set(rag.name, rag);
    return rag;
  }

  private vectorConfigFromPayload(payload: any): VectorStoreConfig {
    if (payload.unit && isVectorUnit(payload.unit)) return this.configureVectorUnit(payload.unit);
    const name = String(payload.store ?? payload.name ?? payload.model ?? "default");
    const existing = this.vectorStores.get(name);
    if (existing) return existing;
    return this.vectorStores.configure({
      name,
      backend: String(payload.backend ?? "indexeddb"),
      metric: String(payload.metric ?? "cosine") as VectorMetric,
      persist: payload.persist !== false,
      namespace: String(payload.namespace ?? "default"),
      options: payload.options ?? {},
    });
  }

  private ragFromPayload(payload: any): RagConfig {
    if (payload.unit && isRagUnit(payload.unit)) return this.configureRagUnit(payload.unit);
    if (payload.rag && typeof payload.rag !== "string") return this.configureRagUnit(payload.rag);
    const name = String(payload.rag ?? payload.name ?? payload.model ?? "default");
    const existing = this.rags.get(name);
    if (!existing) throw new Error(`RAG unit not found: ${name}`);
    return existing;
  }

  private applyUnitRequest(instance: RuntimeInstance, request?: RuntimeUnitRequest): void {
    if (!request) return;
    if (request.reasoning !== undefined) {
      this.setInstanceReasoning(instance, request.reasoning);
    }
    if (request.options) {
      instance.options = { ...(instance.options ?? {}), ...request.options };
    }
    const ragPayload = request.rag ?? (request.options?.rag as RuntimeUnitRequest | undefined);
    if (ragPayload) {
      instance.ragId = this.configureRagUnit(ragPayload).name;
    }
  }

  private setInstanceReasoning(instance: RuntimeInstance, reasoning: boolean | null): void {
    if (reasoning !== null && !supportsReasoning(instance.model)) {
      throw new Error(`${instance.model.label} does not advertise reasoning control`);
    }
    instance.reasoning = reasoning;
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
      device: preferNpu ? "webnn-npu" : this.runtimeBackend(model),
    };
    if (model.dtype && model.dtype !== "auto") {
      options.dtype = model.dtype;
    }
    return options;
  }

  private backendModelId(model: ModelSpec): string {
    return model.backendModelId ?? model.modelId;
  }

  private resolveReasoning(instance: RuntimeInstance, payload: any): boolean | null {
    const candidates = [
      payload.reasoning,
      payload.enable_thinking,
      payload.enableThinking,
      payload.chat_template_kwargs?.enable_thinking,
      payload.extra_body?.reasoning,
      payload.extra_body?.enable_thinking,
      payload.extra_body?.chat_template_kwargs?.enable_thinking,
      instance.reasoning,
    ];
    for (const candidate of candidates) {
      if (typeof candidate === "boolean") {
        if (!supportsReasoning(instance.model)) {
          throw new Error(`${instance.model.label} does not advertise reasoning control`);
        }
        return candidate;
      }
      if (candidate === null) return null;
    }
    return null;
  }

  private extraBodyWithReasoning(extraBody: any, reasoning: boolean | null): Record<string, unknown> | undefined {
    if (reasoning === null) return extraBody;
    return {
      ...(extraBody ?? {}),
      reasoning,
      chat_template_kwargs: {
        ...(extraBody?.chat_template_kwargs ?? {}),
        enable_thinking: reasoning,
      },
    };
  }

  private messagesWithReasoningMarker(model: ModelSpec, messages: any[], reasoning: boolean | null): any[] {
    if (reasoning === null || !isQwenReasoningModel(model)) return messages;
    const marker = reasoning ? "/think" : "/no_think";
    if (messages.length === 0) return [{ role: "user", content: marker }];
    const index = messages.findIndex((message) => message.role === "system");
    if (index >= 0) {
      return messages.map((message, current) =>
        current === index ? { ...message, content: `${String(message.content ?? "")}\n${marker}` } : message,
      );
    }
    return [{ role: "system", content: marker }, ...messages];
  }

  private runtimeBackend(model: ModelSpec): "webgpu" | "wasm" {
    if (this.webgpuAvailable) return "webgpu";
    if (model.runtime === "transformers" && supportsCpuFallback(model)) return "wasm";
    throw new Error(`${model.label} requires WebGPU. Use xlocllm.models(webgpu=False) to list CPU/WASM-capable models.`);
  }

  private assertModelSupported(model: ModelSpec): void {
    if (model.runtime === "mlc" && !this.webgpuAvailable) {
      throw new Error(`${model.label} uses WebLLM/MLC and requires WebGPU`);
    }
    if (!this.webgpuAvailable && !supportsCpuFallback(model)) {
      throw new Error(`${model.label} is not available without WebGPU`);
    }
  }

  private supportedCatalogModels(): ModelSpec[] {
    return supportedModelsForCapabilities(this.webgpuAvailable);
  }

  private capabilities(modelCount: number): RuntimeSnapshot["capabilities"] {
    return {
      webgpu: this.webgpuAvailable,
      webnn: this.npuAvailable,
      cpuFallback: !this.webgpuAvailable,
      backend: this.webgpuAvailable ? "webgpu" : "wasm",
      modelCount,
      catalogModelCount: catalog.models.length,
    };
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
      this.npu = {
        status: "fallback",
        backend: this.webgpuAvailable ? "webgpu" : "wasm",
        reason: String(error instanceof Error ? error.message : error),
      };
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
      reasoning: selected?.reasoning,
      supportsReasoning: selected ? supportsReasoning(selected.model) : false,
      options: selected?.options,
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
      reasoning: instance.reasoning,
      supportsReasoning: supportsReasoning(instance.model),
      options: instance.options,
      progress: instance.progress,
      error: instance.error,
    };
  }

  private serviceStates(): RuntimeServiceState[] {
    const stores = this.vectorStores.allConfigs().map((store) => ({
      runtimeId: `vectorstorage:${store.name}`,
      type: "vectorstorage",
      active: true,
      status: "ready" as const,
      options: { ...store },
    }));
    const rags = [...this.rags.values()].map((rag) => ({
      runtimeId: `RAG:${rag.name}`,
      type: "RAG",
      active: rag.active,
      status: rag.status,
      options: {
        emb: rag.emb,
        rerank: rag.rerank,
        store: rag.store,
        chunkSize: rag.chunkSize,
        chunkOverlap: rag.chunkOverlap,
        topK: rag.topK,
        candidateK: rag.candidateK,
        scoreThreshold: rag.scoreThreshold,
      },
      error: rag.error,
    }));
    return [...stores, ...rags];
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

function normalizeEndpoint(value: string): string {
  return value.trim().toLowerCase().replace(/[/_]/g, ".");
}

function isVectorUnit(unit: RuntimeUnitRequest | Record<string, unknown> | undefined): boolean {
  return normalizeUnitType(String(unit?.type ?? "")) === "vectorstorage";
}

function isRagUnit(unit: RuntimeUnitRequest | Record<string, unknown> | undefined): boolean {
  return normalizeUnitType(String(unit?.type ?? "")) === "rag";
}

function normalizeUnitType(value: string): string {
  return value.trim().toLowerCase().replace(/[\s_-]+/g, "");
}

function normalizeNestedRequest(value: unknown): RuntimeUnitRequest | null {
  if (!value || typeof value !== "object") return null;
  const item = value as RuntimeUnitRequest;
  if (!item.type || !item.model) return null;
  return item;
}

function defaultVectorUnit(name: string): RuntimeUnitRequest {
  return {
    type: "vectorstorage",
    model: name,
    options: { backend: "indexeddb", metric: "cosine", persist: true, namespace: "default" },
  };
}

function dedupeModelRequests(requests: RuntimeUnitRequest[]): RuntimeUnitRequest[] {
  const seen = new Set<string>();
  const result: RuntimeUnitRequest[] = [];
  for (const request of requests) {
    if (isVectorUnit(request) || isRagUnit(request)) continue;
    const key = `${request.type}:${request.model}`;
    if (seen.has(key)) continue;
    seen.add(key);
    result.push(request);
  }
  return result;
}

function numberOrDefault(value: unknown, fallback: number): number {
  const numberValue = Number(value);
  return Number.isFinite(numberValue) && numberValue > 0 ? numberValue : fallback;
}

function stringArray(value: unknown): string[] | null {
  if (value === undefined || value === null) return null;
  if (Array.isArray(value)) return value.map(String);
  return [String(value)];
}

function vectorItemsFromPayload(payload: any): VectorAddItem[] {
  const documents = normalizeDocumentInputs(payload.documents ?? payload.items ?? payload.input, payload.ids, payload.metadatas);
  const embeddings = payload.embeddings ?? payload.vectors;
  if (!Array.isArray(embeddings)) {
    if (Array.isArray(payload.items)) {
      return payload.items.map((item: any, index: number) => ({
        id: item.id,
        documentId: item.documentId ?? item.document_id,
        chunkIndex: item.chunkIndex ?? item.chunk_index ?? index,
        text: String(item.text ?? item.content ?? item.document ?? ""),
        metadata: item.metadata ?? {},
        embedding: item.embedding ?? item.vector,
        embeddingModel: item.embeddingModel ?? item.embedding_model,
      }));
    }
    throw new Error("vector.add requires embeddings or vectors");
  }
  return documents.map((document, index) => ({
    id: document.id,
    documentId: document.id,
    chunkIndex: 0,
    text: document.text,
    metadata: document.metadata,
    embedding: embeddings[index],
    embeddingModel: payload.embedding_model ?? payload.embeddingModel,
  }));
}

function ragDocumentsFromPayload(payload: any): Array<{ id: string; text: string; metadata: Record<string, unknown> }> {
  return normalizeDocumentInputs(payload.documents ?? payload.input ?? payload.text, payload.ids, payload.metadatas);
}

function normalizeDocumentInputs(
  input: unknown,
  ids?: unknown,
  metadatas?: unknown,
): Array<{ id: string; text: string; metadata: Record<string, unknown> }> {
  const rawItems = Array.isArray(input) ? input : input === undefined || input === null ? [] : [input];
  const idList = Array.isArray(ids) ? ids.map(String) : [];
  const metadataList = Array.isArray(metadatas) ? metadatas : [];
  return rawItems.map((item, index) => {
    if (item && typeof item === "object") {
      const object = item as Record<string, unknown>;
      return {
        id: String(object.id ?? object.documentId ?? object.document_id ?? idList[index] ?? stableDocumentId(object.text ?? object.content ?? index)),
        text: String(object.text ?? object.content ?? object.document ?? ""),
        metadata: metadataObject(object.metadata ?? metadataList[index]),
      };
    }
    return {
      id: String(idList[index] ?? stableDocumentId(item ?? index)),
      text: String(item ?? ""),
      metadata: metadataObject(metadataList[index]),
    };
  });
}

function metadataObject(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value) ? (value as Record<string, unknown>) : {};
}

function stableDocumentId(value: unknown): string {
  const text = String(value ?? "");
  let hash = 0;
  for (let index = 0; index < text.length; index += 1) {
    hash = Math.imul(31, hash) + text.charCodeAt(index);
  }
  return `doc_${Math.abs(hash).toString(36)}`;
}

function publicVectorResult(result: VectorSearchResult): Record<string, unknown> {
  return {
    id: result.id,
    document_id: result.documentId,
    chunk_index: result.chunkIndex,
    text: result.text,
    metadata: result.metadata,
    score: result.score,
  };
}

function contextFromResults(results: VectorSearchResult[]): string {
  return results.map((result, index) => `[${index + 1}] ${result.text}`).join("\n\n");
}

function lastUserText(messages: any[]): string {
  for (let index = messages.length - 1; index >= 0; index -= 1) {
    const message = messages[index];
    if (message?.role !== "user") continue;
    const content = message.content;
    if (typeof content === "string") return content;
    if (Array.isArray(content)) {
      return content
        .map((part) => (typeof part === "string" ? part : typeof part?.text === "string" ? part.text : ""))
        .filter(Boolean)
        .join("\n");
    }
  }
  return "";
}

function messagesWithRagContext(messages: any[], rag: any): any[] {
  const context = String(rag.context ?? "").trim();
  if (!context) return messages;
  const systemMessage = {
    role: "system",
    content: `Use this retrieved context when it is relevant. If the context is not relevant, answer normally.\n\n${context}`,
  };
  return [systemMessage, ...messages];
}

function pipelinePayloadOptions(payload: any): Record<string, unknown> {
  return {
    ...(payload.options ?? {}),
    ...(payload.model ? { model: payload.model } : {}),
  };
}

function imageInput(payload: any): any {
  const value = payload.image ?? payload.input ?? payload.url;
  if (value === undefined || value === null || value === "") throw new Error("image input is required");
  return value;
}

function audioInput(payload: any): any {
  const value = payload.audio ?? payload.input ?? payload.url;
  if (value === undefined || value === null || value === "") throw new Error("audio input is required");
  return value;
}

function textInput(payload: any): string {
  const value = payload.text ?? payload.input ?? payload.prompt ?? payload.query;
  if (value === undefined || value === null) throw new Error("text input is required");
  return String(value);
}

function labelsInput(payload: any): string[] {
  const labels = payload.labels ?? payload.candidate_labels ?? payload.candidateLabels;
  if (!Array.isArray(labels) || labels.length === 0) throw new Error("labels or candidate_labels are required");
  return labels.map((label) => String(label));
}

function normalizeArrayResult(result: any): any[] {
  if (Array.isArray(result)) return result;
  if (Array.isArray(result?.data)) return result.data;
  if (Array.isArray(result?.labels)) return result.labels;
  if (Array.isArray(result?.entities)) return result.entities;
  return result === undefined || result === null ? [] : [result];
}

function extractGeneratedText(output: any): string {
  if (typeof output === "string") return output;
  if (Array.isArray(output)) {
    const first = output[0];
    if (typeof first?.generated_text === "string") return first.generated_text;
    if (typeof first?.summary_text === "string") return first.summary_text;
    if (typeof first?.translation_text === "string") return first.translation_text;
    if (typeof first?.text === "string") return first.text;
    if (Array.isArray(first?.generated_text)) return first.generated_text.at(-1)?.content ?? JSON.stringify(output);
  }
  if (typeof output?.generated_text === "string") return output.generated_text;
  if (typeof output?.summary_text === "string") return output.summary_text;
  if (typeof output?.translation_text === "string") return output.translation_text;
  if (typeof output?.text === "string") return output.text;
  return JSON.stringify(output);
}

function serializeBinaryLike(result: any): any {
  if (result?.audio instanceof Float32Array) {
    return { audio: Array.from(result.audio), sampling_rate: result.sampling_rate };
  }
  return result;
}

function isQwenReasoningModel(model: ModelSpec): boolean {
  const haystack = [model.modelId, model.label, ...(model.aliases ?? []), ...(model.tags ?? [])].join(" ").toLowerCase();
  return haystack.includes("qwen3") || haystack.includes("qwen3.5") || haystack.includes("qwen3_5");
}

function splitText(text: string): string[] {
  const chunks = [];
  for (let index = 0; index < text.length; index += 24) {
    chunks.push(text.slice(index, index + 24));
  }
  return chunks.length ? chunks : [""];
}
