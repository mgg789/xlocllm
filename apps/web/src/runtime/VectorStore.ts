export type VectorMetric = "cosine" | "dot" | "euclidean";

export interface VectorStoreConfig {
  name: string;
  backend: "indexeddb" | "memory" | string;
  metric: VectorMetric;
  persist: boolean;
  namespace: string;
  options?: Record<string, unknown>;
}

export interface VectorRecord {
  key: string;
  store: string;
  namespace: string;
  id: string;
  documentId: string;
  chunkIndex: number;
  text: string;
  metadata: Record<string, unknown>;
  embedding: number[];
  embeddingModel?: string;
  createdAt: string;
  updatedAt: string;
}

export interface VectorSearchResult extends VectorRecord {
  score: number;
}

export interface VectorAddItem {
  id?: string;
  documentId?: string;
  chunkIndex?: number;
  text: string;
  metadata?: Record<string, unknown>;
  embedding: number[];
  embeddingModel?: string;
}

export interface VectorAddResult {
  ok: true;
  store: string;
  namespace: string;
  count: number;
  ids: string[];
}

export interface VectorSearchResultSet {
  ok: true;
  store: string;
  namespace: string;
  results: VectorSearchResult[];
}

const dbName = "xlocllm-vectorstores";
const dbVersion = 1;
const vectorStoreName = "vectors";

export class VectorStorageRegistry {
  private configs = new Map<string, VectorStoreConfig>();
  private memory = new Map<string, VectorRecord>();
  private db?: Promise<IDBDatabase | undefined>;

  configure(config: VectorStoreConfig): VectorStoreConfig {
    const normalized = normalizeConfig(config);
    this.configs.set(normalized.name, normalized);
    return normalized;
  }

  get(name: string): VectorStoreConfig | undefined {
    return this.configs.get(name);
  }

  allConfigs(): VectorStoreConfig[] {
    return [...this.configs.values()];
  }

  ensure(config: VectorStoreConfig): VectorStoreConfig {
    return this.configure(config);
  }

  async add(config: VectorStoreConfig, items: VectorAddItem[]): Promise<VectorAddResult> {
    const normalized = this.ensure(config);
    const now = new Date().toISOString();
    const records = items.map((item, index) => {
      const documentId = item.documentId ?? item.id ?? randomId();
      const id = item.id ?? `${documentId}:${item.chunkIndex ?? index}`;
      const record: VectorRecord = {
        key: recordKey(normalized.name, normalized.namespace, id),
        store: normalized.name,
        namespace: normalized.namespace,
        id,
        documentId,
        chunkIndex: item.chunkIndex ?? index,
        text: item.text,
        metadata: item.metadata ?? {},
        embedding: item.embedding.map(Number),
        embeddingModel: item.embeddingModel,
        createdAt: now,
        updatedAt: now,
      };
      return record;
    });
    if (normalized.persist && normalized.backend === "indexeddb") {
      const db = await this.openDb();
      if (db) {
        await putRecords(db, records);
      } else {
        for (const record of records) this.memory.set(record.key, record);
      }
    } else {
      for (const record of records) this.memory.set(record.key, record);
    }
    return {
      ok: true,
      store: normalized.name,
      namespace: normalized.namespace,
      count: records.length,
      ids: records.map((record) => record.id),
    };
  }

  async search(
    config: VectorStoreConfig,
    embedding: number[],
    topK: number,
    filter?: Record<string, unknown> | null,
  ): Promise<VectorSearchResultSet> {
    const normalized = this.ensure(config);
    const records = await this.records(normalized);
    const results = records
      .filter((record) => metadataMatches(record, filter))
      .map((record) => ({ ...record, score: vectorScore(normalized.metric, embedding, record.embedding) }))
      .sort((left, right) => right.score - left.score)
      .slice(0, Math.max(1, topK));
    return { ok: true, store: normalized.name, namespace: normalized.namespace, results };
  }

  async delete(
    config: VectorStoreConfig,
    ids?: string[] | null,
    filter?: Record<string, unknown> | null,
  ): Promise<{ ok: true; store: string; namespace: string; deleted: number }> {
    const normalized = this.ensure(config);
    const idSet = new Set((ids ?? []).map(String));
    if (idSet.size === 0 && !filter) {
      return { ok: true, store: normalized.name, namespace: normalized.namespace, deleted: 0 };
    }
    const records = await this.records(normalized);
    const doomed = records.filter((record) => {
      const byId = idSet.has(record.id) || idSet.has(record.documentId);
      return (idSet.size === 0 || byId) && metadataMatches(record, filter);
    });
    await this.deleteKeys(normalized, doomed.map((record) => record.key));
    return { ok: true, store: normalized.name, namespace: normalized.namespace, deleted: doomed.length };
  }

  async clear(config: VectorStoreConfig): Promise<{ ok: true; store: string; namespace: string; deleted: number }> {
    const normalized = this.ensure(config);
    const records = await this.records(normalized);
    await this.deleteKeys(normalized, records.map((record) => record.key));
    return { ok: true, store: normalized.name, namespace: normalized.namespace, deleted: records.length };
  }

  async stats(config: VectorStoreConfig): Promise<Record<string, unknown>> {
    const normalized = this.ensure(config);
    const records = await this.records(normalized);
    const documentIds = new Set(records.map((record) => record.documentId));
    const dimensions = records[0]?.embedding.length ?? null;
    return {
      ok: true,
      store: normalized.name,
      namespace: normalized.namespace,
      backend: normalized.backend,
      persist: normalized.persist,
      metric: normalized.metric,
      chunks: records.length,
      documents: documentIds.size,
      dimensions,
    };
  }

  async records(config: VectorStoreConfig): Promise<VectorRecord[]> {
    const normalized = this.ensure(config);
    if (normalized.persist && normalized.backend === "indexeddb") {
      const db = await this.openDb();
      if (db) return getRecords(db, normalized);
    }
    return [...this.memory.values()].filter((record) => record.store === normalized.name && record.namespace === normalized.namespace);
  }

  private async deleteKeys(config: VectorStoreConfig, keys: string[]): Promise<void> {
    if (keys.length === 0) return;
    if (config.persist && config.backend === "indexeddb") {
      const db = await this.openDb();
      if (db) {
        await deleteRecords(db, keys);
        return;
      }
    }
    for (const key of keys) this.memory.delete(key);
  }

  private openDb(): Promise<IDBDatabase | undefined> {
    if (!this.db) {
      this.db = openVectorDb();
    }
    return this.db;
  }
}

export function normalizeConfig(config: VectorStoreConfig): VectorStoreConfig {
  const metric = ["cosine", "dot", "euclidean"].includes(config.metric) ? config.metric : "cosine";
  const backend = config.backend || "indexeddb";
  return {
    ...config,
    name: config.name || "default",
    backend,
    metric,
    persist: config.persist !== false,
    namespace: config.namespace || "default",
  };
}

export function chunkText(text: string, chunkSize: number, chunkOverlap: number): string[] {
  const clean = text.replace(/\s+/g, " ").trim();
  if (!clean) return [];
  const size = Math.max(80, chunkSize || 800);
  const overlap = Math.max(0, Math.min(chunkOverlap || 0, size - 1));
  const chunks: string[] = [];
  let start = 0;
  while (start < clean.length) {
    let end = Math.min(clean.length, start + size);
    if (end < clean.length) {
      const boundary = clean.lastIndexOf(" ", end);
      if (boundary > start + Math.floor(size * 0.6)) end = boundary;
    }
    chunks.push(clean.slice(start, end).trim());
    if (end >= clean.length) break;
    start = Math.max(0, end - overlap);
  }
  return chunks.filter(Boolean);
}

export function vectorScore(metric: VectorMetric, query: number[], candidate: number[]): number {
  if (query.length !== candidate.length || query.length === 0) return Number.NEGATIVE_INFINITY;
  if (metric === "dot") return dot(query, candidate);
  if (metric === "euclidean") return -Math.sqrt(query.reduce((sum, value, index) => sum + (value - candidate[index]) ** 2, 0));
  const denominator = magnitude(query) * magnitude(candidate);
  return denominator === 0 ? Number.NEGATIVE_INFINITY : dot(query, candidate) / denominator;
}

export function metadataMatches(record: VectorRecord, filter?: Record<string, unknown> | null): boolean {
  if (!filter || Object.keys(filter).length === 0) return true;
  return Object.entries(filter).every(([key, expected]) => {
    const actual = key in record ? (record as unknown as Record<string, unknown>)[key] : record.metadata[key];
    if (Array.isArray(expected)) return expected.includes(actual);
    return actual === expected;
  });
}

function dot(left: number[], right: number[]): number {
  return left.reduce((sum, value, index) => sum + value * right[index], 0);
}

function magnitude(values: number[]): number {
  return Math.sqrt(values.reduce((sum, value) => sum + value * value, 0));
}

function recordKey(store: string, namespace: string, id: string): string {
  return `${store}\u0000${namespace}\u0000${id}`;
}

function randomId(): string {
  return globalThis.crypto?.randomUUID?.() ?? `vec_${Math.random().toString(36).slice(2)}`;
}

function openVectorDb(): Promise<IDBDatabase | undefined> {
  if (typeof indexedDB === "undefined") return Promise.resolve(undefined);
  return new Promise((resolve) => {
    const request = indexedDB.open(dbName, dbVersion);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(vectorStoreName)) {
        const store = db.createObjectStore(vectorStoreName, { keyPath: "key" });
        store.createIndex("store", "store", { unique: false });
        store.createIndex("namespace", "namespace", { unique: false });
        store.createIndex("documentId", "documentId", { unique: false });
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => resolve(undefined);
    request.onblocked = () => resolve(undefined);
  });
}

function putRecords(db: IDBDatabase, records: VectorRecord[]): Promise<void> {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(vectorStoreName, "readwrite");
    const store = tx.objectStore(vectorStoreName);
    for (const record of records) store.put(record);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error ?? new Error("IndexedDB put failed"));
  });
}

function getRecords(db: IDBDatabase, config: VectorStoreConfig): Promise<VectorRecord[]> {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(vectorStoreName, "readonly");
    const store = tx.objectStore(vectorStoreName);
    const request = store.index("store").getAll(config.name);
    request.onsuccess = () => {
      const records = (request.result as VectorRecord[]).filter((record) => record.namespace === config.namespace);
      resolve(records);
    };
    request.onerror = () => reject(request.error ?? new Error("IndexedDB read failed"));
  });
}

function deleteRecords(db: IDBDatabase, keys: string[]): Promise<void> {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(vectorStoreName, "readwrite");
    const store = tx.objectStore(vectorStoreName);
    for (const key of keys) store.delete(key);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error ?? new Error("IndexedDB delete failed"));
  });
}
