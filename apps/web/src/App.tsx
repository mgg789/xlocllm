import {
  Activity,
  ArrowLeft,
  BookOpen,
  CheckCircle2,
  Download,
  Flame,
  Gauge,
  HardDrive,
  MemoryStick,
  Moon,
  Pause,
  Play,
  PlugZap,
  Plus,
  Power,
  RefreshCw,
  Search,
  SlidersHorizontal,
  Square,
  Star,
  Sun,
  Trash2,
  Wifi,
  WifiOff,
  ZapOff,
} from "lucide-react";
import { useEffect, useMemo, useRef, useState, type CSSProperties, type ReactNode } from "react";
import { catalog, modelSummary, unitDefinitions } from "./catalog";
import { BridgeClient } from "./runtime/BridgeClient";
import { RuntimeHost } from "./runtime/RuntimeHost";
import type { HardwareTier, LogEntry, ModelSpec, NpuState, RuntimeMetrics, RuntimeModelState, RuntimeSnapshot, RuntimeUnitRequest, UnitType } from "./types";
import "./styles.css";

const defaultPort = 1146;
const favoriteStorageKey = "xlocllm:favorites";

type BridgeState = "disabled" | "connecting" | "connected" | "error";
type Theme = "light" | "dark";
type View = "dashboard" | "catalog";
type SortMode = "recommended" | "name" | "size-asc" | "size-desc" | "params-asc" | "params-desc";

interface Filters {
  unit: "all" | UnitType;
  taskGroup: "all" | string;
  runtime: "all" | string;
  hardwareTier: "all" | HardwareTier;
  language: "all" | string;
  status: "all" | "active" | "installed" | "favorites" | "npu";
  paramMin: number;
  paramMax: number;
  sizeMin: number;
  sizeMax: number;
}

const catalogRanges = {
  paramMax: Math.ceil(Math.max(1, ...catalog.models.map((model) => model.parameterB ?? 0))),
  sizeMax: Math.ceil(Math.max(1, ...catalog.models.map((model) => model.modelSizeGb ?? 0))),
};

const defaultFilters: Filters = {
  unit: "all",
  taskGroup: "all",
  runtime: "all",
  hardwareTier: "all",
  language: "all",
  status: "all",
  paramMin: 0,
  paramMax: catalogRanges.paramMax,
  sizeMin: 0,
  sizeMax: catalogRanges.sizeMax,
};

export default function App() {
  const host = useMemo(() => new RuntimeHost(), []);
  const bridge = useMemo(() => new BridgeClient(host), [host]);
  const [snapshot, setSnapshot] = useState<RuntimeSnapshot>(host.snapshot());
  const [bridgeState, setBridgeState] = useState<BridgeState>("disabled");
  const [port, setPort] = useState(initialPort);
  const [theme, setTheme] = useState<Theme>(() => readTheme());
  const [view, setView] = useState<View>("dashboard");
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [favorites, setFavorites] = useState<Set<string>>(() => readFavorites());
  const [filters, setFilters] = useState<Filters>(defaultFilters);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<SortMode>("recommended");

  useEffect(() => host.subscribe(() => setSnapshot(host.snapshot())), [host]);
  useEffect(() => bridge.subscribe((state) => setBridgeState(state as BridgeState)), [bridge]);
  useEffect(() => {
    bridge.startFromLocation(window.location);
    return () => bridge.stop();
  }, [bridge]);
  useEffect(() => {
    if (!isMiniMode()) return undefined;
    const shutdownBridge = () => {
      const bridgePort = new URLSearchParams(window.location.search).get("bridgePort");
      if (!bridgePort) return;
      const url = `http://127.0.0.1:${bridgePort}/xlocllm/v1/shutdown`;
      if (!navigator.sendBeacon(url, new Blob())) {
        void fetch(url, { method: "POST", keepalive: true }).catch(() => undefined);
      }
    };
    window.addEventListener("pagehide", shutdownBridge);
    return () => window.removeEventListener("pagehide", shutdownBridge);
  }, []);
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    window.localStorage.setItem("xlocllm:theme", theme);
  }, [theme]);
  useEffect(() => {
    window.sessionStorage.setItem(favoriteStorageKey, JSON.stringify([...favorites]));
  }, [favorites]);

  const activeUnits = runtimeUnits(snapshot.models.filter((model) => model.active));
  const miniMode = isMiniMode();

  const actions = {
    install: () => host.install(activeUnits).catch(console.error),
    run: () => host.run(activeUnits).catch(console.error),
    stop: () => host.stop().catch(console.error),
    hibernate: () => host.hibernate().catch(console.error),
    heatup: () => host.heatup().catch(console.error),
    deleteAll: () => setConfirmDelete(true),
    addModel: (model: ModelSpec) => host.addModel(model, true),
    deleteModel: (model: ModelSpec) => host.deleteModel(model.unit, model.modelId).catch(console.error),
    installModel: (model: ModelSpec) => host.install([{ type: model.unit, model: model.modelId }]).catch(console.error),
    toggleActive: (modelId: string, active: boolean) => host.setModelActive(modelId, active),
  };

  const toggleFavorite = (modelId: string) => {
    setFavorites((current) => {
      const next = new Set(current);
      if (next.has(modelId)) next.delete(modelId);
      else next.add(modelId);
      return next;
    });
  };

  if (miniMode) {
    return (
      <MiniRuntime
        bridgeState={bridgeState}
        port={port}
        snapshot={snapshot}
        onRun={actions.run}
        onStop={actions.stop}
        onHibernate={actions.hibernate}
        onHeatup={actions.heatup}
        onDeleteAll={actions.deleteAll}
      />
    );
  }

  return (
    <main className="app-shell">
      {view === "dashboard" ? (
        <>
          <section className="dashboard-hero">
            <ControlPanel
              bridgeState={bridgeState}
              port={port}
              setPort={setPort}
              snapshot={snapshot}
              theme={theme}
              setTheme={setTheme}
              onInstall={actions.install}
              onRun={actions.run}
              onStop={actions.stop}
              onHibernate={actions.hibernate}
              onHeatup={actions.heatup}
              onDeleteAll={actions.deleteAll}
            />
            <MetricsPanel metrics={snapshot.metrics} />
          </section>

          <RuntimeModelsPanel
            snapshot={snapshot}
            onAdd={() => setView("catalog")}
            onInstall={actions.installModel}
            onDelete={actions.deleteModel}
            onToggleActive={actions.toggleActive}
          />

          <Logs entries={snapshot.logs} />
        </>
      ) : (
        <CatalogScreen
          snapshot={snapshot}
          bridgeState={bridgeState}
          favorites={favorites}
          filters={filters}
          search={search}
          sort={sort}
          onBack={() => setView("dashboard")}
          onFiltersChange={setFilters}
          onSearchChange={setSearch}
          onSortChange={setSort}
          onAdd={actions.addModel}
          onDelete={actions.deleteModel}
          onToggleFavorite={toggleFavorite}
        />
      )}

      {confirmDelete && (
        <div className="modal-backdrop" role="presentation">
          <div className="modal" role="dialog" aria-modal="true" aria-labelledby="delete-all-title">
            <h2 id="delete-all-title">Delete all models</h2>
            <p>Cached model files known to xlocllm will be removed from browser storage. Runtime rows will stay, but become not installed.</p>
            <div className="modal-actions">
              <button type="button" className="ghost" onClick={() => setConfirmDelete(false)}>
                Cancel
              </button>
              <button
                type="button"
                className="danger"
                onClick={() => {
                  setConfirmDelete(false);
                  void host.deleteAllModels().catch(console.error);
                }}
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

function ControlPanel({
  bridgeState,
  port,
  setPort,
  snapshot,
  theme,
  setTheme,
  onInstall,
  onRun,
  onStop,
  onHibernate,
  onHeatup,
  onDeleteAll,
}: {
  bridgeState: BridgeState;
  port: number;
  setPort: (port: number) => void;
  snapshot: RuntimeSnapshot;
  theme: Theme;
  setTheme: (theme: Theme) => void;
  onInstall: () => void;
  onRun: () => void;
  onStop: () => void;
  onHibernate: () => void;
  onHeatup: () => void;
  onDeleteAll: () => void;
}) {
  const activeCount = snapshot.models.filter((model) => model.active).length;
  const hibernated = snapshot.models.some((model) => model.status === "hibernated");
  return (
    <section className="control-stack">
      <header className="brand-panel">
        <div>
          <h1>xlocllm</h1>
          <p>v0.1.0 · {catalog.models.length} models in catalog</p>
        </div>
        <button className="icon-button" type="button" onClick={() => setTheme(theme === "dark" ? "light" : "dark")} title="Switch theme">
          {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <BridgeBadge state={bridgeState} />
      </header>

      <div className="control-panel">
        <button type="button" disabled={snapshot.installing || activeCount === 0} onClick={snapshot.running ? onStop : onRun}>
          {snapshot.running ? <Square size={18} /> : <Power size={18} />}
          {snapshot.running ? "Stop" : "Run"}
        </button>
        <button type="button" disabled={snapshot.installing || activeCount === 0} onClick={onInstall}>
          <Download size={18} />
          {snapshot.installing ? "Installing" : "Install"}
        </button>
        <StatCard label="Active models" value={String(activeCount)} tone="neutral" />
        <NpuCard npu={snapshot.npu} />
        <button type="button" className="secondary" onClick={hibernated ? onHeatup : onHibernate} disabled={activeCount === 0}>
          {hibernated ? <Flame size={18} /> : <Pause size={18} />}
          {hibernated ? "Heatup" : "Hibernate"}
        </button>
        <button type="button" className="danger" onClick={onDeleteAll}>
          <Trash2 size={18} />
          Delete all models
        </button>
        <button type="button" className="danger" onClick={onStop}>
          <ZapOff size={18} />
          Kill switch
        </button>
        <a className="button secondary" href="docs.html" target="_blank" rel="noreferrer">
          <BookOpen size={18} />
          Docs
        </a>
        <label className="port-control">
          <span>Port</span>
          <input value={port} onChange={(event) => setPort(Number(event.target.value) || defaultPort)} inputMode="numeric" />
        </label>
        <button type="button" className="secondary" onClick={() => updateQueryPort(port)}>
          <PlugZap size={18} />
          Set port
        </button>
      </div>
    </section>
  );
}

function BridgeBadge({ state }: { state: BridgeState }) {
  const connected = state === "connected";
  return (
    <div className={`bridge-badge ${connected ? "connected" : "disconnected"}`}>
      {connected ? <Wifi size={16} /> : <WifiOff size={16} />}
      <span>{connected ? "connected" : state}</span>
    </div>
  );
}

function StatCard({ label, value, tone = "neutral" }: { label: string; value: string; tone?: "neutral" | "good" | "warn" }) {
  return (
    <div className={`stat-card tone-${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function NpuCard({ npu }: { npu: NpuState }) {
  const value = npu.status === "active" ? "NPU on" : npu.status === "fallback" ? "fallback" : "off";
  return <StatCard label="NPU" value={value} tone={npu.status === "active" ? "good" : npu.status === "fallback" ? "warn" : "neutral"} />;
}

function MetricsPanel({ metrics }: { metrics: RuntimeMetrics }) {
  return (
    <section className="metrics-grid" aria-label="Runtime metrics">
      <Metric title="GPU" value={metrics.gpu} icon={<Gauge size={18} />} />
      <Metric title="CPU" value={metrics.cpu} icon={<Activity size={18} />} />
      <Metric title="RAM" value={metrics.ram} icon={<MemoryStick size={18} />} />
      <Metric title="DISK" value={metrics.disk} icon={<HardDrive size={18} />} />
    </section>
  );
}

function Metric({ title, value, icon }: { title: string; value: number | null; icon: ReactNode }) {
  const bounded = value === null ? 0 : Math.max(0, Math.min(100, value));
  return (
    <div className="metric">
      <div className="metric-title">
        {icon}
        <span>{title}</span>
      </div>
      <div className="metric-chart" aria-hidden="true">
        {Array.from({ length: 18 }, (_, index) => (
          <span key={index} className={index * 6 <= bounded ? levelClass(bounded) : ""} />
        ))}
        <i style={{ transform: `translateY(${100 - bounded}%)` }} />
      </div>
      <div className="metric-value">{value === null ? "--" : `${bounded}%`}</div>
    </div>
  );
}

function RuntimeModelsPanel({
  snapshot,
  onAdd,
  onInstall,
  onDelete,
  onToggleActive,
}: {
  snapshot: RuntimeSnapshot;
  onAdd: () => void;
  onInstall: (model: ModelSpec) => void;
  onDelete: (model: ModelSpec) => void;
  onToggleActive: (modelId: string, active: boolean) => void;
}) {
  return (
    <section className="runtime-panel">
      <div className="section-header">
        <div>
          <h2>Runtime models</h2>
          <p>{snapshot.models.length} added · {snapshot.models.filter((model) => model.active).length} active</p>
        </div>
        <button type="button" className="icon-button primary" onClick={onAdd} title="Add model">
          <Plus size={20} />
        </button>
      </div>
      <div className="runtime-list">
        {snapshot.models.length === 0 ? (
          <div className="empty-state">
            <p>No models in runtime</p>
            <button type="button" onClick={onAdd}>
              <Plus size={18} />
              Add model
            </button>
          </div>
        ) : (
          snapshot.models.map((state) => {
            const model = catalog.models.find((candidate) => candidate.modelId === state.modelId);
            if (!model) return null;
            return (
              <RuntimeModelRow
                key={state.runtimeId}
                model={model}
                state={state}
                onInstall={onInstall}
                onDelete={onDelete}
                onToggleActive={onToggleActive}
              />
            );
          })
        )}
      </div>
    </section>
  );
}

function RuntimeModelRow({
  model,
  state,
  onInstall,
  onDelete,
  onToggleActive,
}: {
  model: ModelSpec;
  state: RuntimeModelState;
  onInstall: (model: ModelSpec) => void;
  onDelete: (model: ModelSpec) => void;
  onToggleActive: (modelId: string, active: boolean) => void;
}) {
  return (
    <article className={`runtime-row status-${state.status}`}>
      <ProviderLogo logoKey={model.logoKey} />
      <div className="runtime-main">
        <div className="runtime-title">
          <h3>{model.label}</h3>
          <span>{model.unit}</span>
        </div>
        <p>{modelSummary(model)}</p>
        <div className="tag-row">
          <span>{model.runtime}</span>
          <span>{model.hardwareTier}</span>
          <span>{state.status}</span>
          {state.progress ? <span>{state.progress}%</span> : null}
        </div>
      </div>
      <label className="switch">
        <input type="checkbox" checked={state.active} onChange={(event) => onToggleActive(model.modelId, event.target.checked)} />
        <span>active</span>
      </label>
      <button type="button" className="secondary" onClick={() => onInstall(model)} disabled={state.status === "installing"}>
        <Download size={16} />
        {state.installed ? "Ready" : "Install"}
      </button>
      <button type="button" className="danger icon-button" onClick={() => onDelete(model)} title="Delete model">
        <Trash2 size={16} />
      </button>
    </article>
  );
}

function CatalogScreen({
  snapshot,
  bridgeState,
  favorites,
  filters,
  search,
  sort,
  onBack,
  onFiltersChange,
  onSearchChange,
  onSortChange,
  onAdd,
  onDelete,
  onToggleFavorite,
}: {
  snapshot: RuntimeSnapshot;
  bridgeState: BridgeState;
  favorites: Set<string>;
  filters: Filters;
  search: string;
  sort: SortMode;
  onBack: () => void;
  onFiltersChange: (filters: Filters) => void;
  onSearchChange: (search: string) => void;
  onSortChange: (sort: SortMode) => void;
  onAdd: (model: ModelSpec) => void;
  onDelete: (model: ModelSpec) => void;
  onToggleFavorite: (modelId: string) => void;
}) {
  const runtimeIds = new Set(snapshot.models.map((model) => model.modelId));
  const installedIds = new Set(snapshot.models.filter((model) => model.installed).map((model) => model.modelId));
  const activeIds = new Set(snapshot.models.filter((model) => model.active).map((model) => model.modelId));
  const filtered = useMemo(
    () => filterModels(catalog.models, filters, search, sort, { runtimeIds, installedIds, activeIds, favorites }),
    [activeIds, favorites, filters, installedIds, runtimeIds, search, sort],
  );

  return (
    <section className="catalog-screen">
      <aside className="filters-panel">
        <button type="button" className="secondary back-button" onClick={onBack}>
          <ArrowLeft size={18} />
          To dashboard
        </button>
        <div className="filters-title">
          <SlidersHorizontal size={18} />
          <h2>Filters</h2>
        </div>
        <FilterControls filters={filters} onChange={onFiltersChange} />
      </aside>
      <div className="catalog-workspace">
        <header className="catalog-toolbar">
          <BridgeBadge state={bridgeState} />
          <label className="search-box">
            <Search size={18} />
            <input value={search} onChange={(event) => onSearchChange(event.target.value)} placeholder="Search models" />
          </label>
          <select value={sort} onChange={(event) => onSortChange(event.target.value as SortMode)}>
            <option value="recommended">recommended</option>
            <option value="name">name</option>
            <option value="size-asc">size: low to high</option>
            <option value="size-desc">size: high to low</option>
            <option value="params-asc">params: low to high</option>
            <option value="params-desc">params: high to low</option>
          </select>
        </header>
        <div className="catalog-count">{filtered.length} of {catalog.models.length} models</div>
        <div className="model-grid">
          {filtered.map((model) => {
            const added = runtimeIds.has(model.modelId);
            return (
              <ModelCard
                key={model.modelId}
                model={model}
                added={added}
                favorite={favorites.has(model.modelId)}
                onAdd={() => onAdd(model)}
                onDelete={() => onDelete(model)}
                onToggleFavorite={() => onToggleFavorite(model.modelId)}
              />
            );
          })}
        </div>
      </div>
    </section>
  );
}

function FilterControls({ filters, onChange }: { filters: Filters; onChange: (filters: Filters) => void }) {
  const taskGroups = unique(catalog.models.map((model) => model.taskGroup));
  const runtimes = unique(catalog.models.map((model) => model.runtime));
  const languages = unique(catalog.models.flatMap((model) => model.languages));
  const update = <K extends keyof Filters>(key: K, value: Filters[K]) => onChange({ ...filters, [key]: value });
  return (
    <div className="filter-controls">
      <Select label="Type" value={filters.unit} onChange={(value) => update("unit", value as Filters["unit"])}>
        <option value="all">all</option>
        {unitDefinitions.map((unit) => (
          <option key={unit.type} value={unit.type}>{unit.label}</option>
        ))}
      </Select>
      <Select label="Profile" value={filters.taskGroup} onChange={(value) => update("taskGroup", value)}>
        <option value="all">all</option>
        {taskGroups.map((group) => (
          <option key={group} value={group}>{group}</option>
        ))}
      </Select>
      <Select label="Protocol" value={filters.runtime} onChange={(value) => update("runtime", value)}>
        <option value="all">all</option>
        {runtimes.map((runtime) => (
          <option key={runtime} value={runtime}>{runtime}</option>
        ))}
      </Select>
      <Select label="Hardware" value={filters.hardwareTier} onChange={(value) => update("hardwareTier", value as Filters["hardwareTier"])}>
        <option value="all">all</option>
        <option value="tiny">tiny</option>
        <option value="small">small</option>
        <option value="medium">medium</option>
        <option value="large">large</option>
      </Select>
      <Select label="Language" value={filters.language} onChange={(value) => update("language", value)}>
        <option value="all">all</option>
        {languages.map((language) => (
          <option key={language} value={language}>{language}</option>
        ))}
      </Select>
      <Select label="Status" value={filters.status} onChange={(value) => update("status", value as Filters["status"])}>
        <option value="all">all</option>
        <option value="active">active</option>
        <option value="installed">installed</option>
        <option value="favorites">favorites</option>
        <option value="npu">NPU/WebNN</option>
      </Select>
      <RangePair
        label="Parameters, B"
        min={0}
        max={catalogRanges.paramMax}
        lower={filters.paramMin}
        upper={filters.paramMax}
        onLower={(value) => update("paramMin", Math.min(value, filters.paramMax))}
        onUpper={(value) => update("paramMax", Math.max(value, filters.paramMin))}
      />
      <RangePair
        label="Model size, GB"
        min={0}
        max={catalogRanges.sizeMax}
        lower={filters.sizeMin}
        upper={filters.sizeMax}
        onLower={(value) => update("sizeMin", Math.min(value, filters.sizeMax))}
        onUpper={(value) => update("sizeMax", Math.max(value, filters.sizeMin))}
      />
      <div className="filter-actions">
        <button type="button" className="ghost" onClick={() => onChange(defaultFilters)}>
          Clear all
        </button>
        <button type="button" className="secondary">
          <CheckCircle2 size={16} />
          Submit
        </button>
      </div>
    </div>
  );
}

function Select({ label, value, onChange, children }: { label: string; value: string; onChange: (value: string) => void; children: ReactNode }) {
  return (
    <label className="field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {children}
      </select>
    </label>
  );
}

function RangePair({
  label,
  min,
  max,
  lower,
  upper,
  onLower,
  onUpper,
}: {
  label: string;
  min: number;
  max: number;
  lower: number;
  upper: number;
  onLower: (value: number) => void;
  onUpper: (value: number) => void;
}) {
  return (
    <div className="range-pair">
      <span>{label}</span>
      <div className="range-values">
        <b>{lower}</b>
        <b>{upper}</b>
      </div>
      <input type="range" min={min} max={max} step="0.1" value={lower} onChange={(event) => onLower(Number(event.target.value))} />
      <input type="range" min={min} max={max} step="0.1" value={upper} onChange={(event) => onUpper(Number(event.target.value))} />
    </div>
  );
}

function ModelCard({
  model,
  added,
  favorite,
  onAdd,
  onDelete,
  onToggleFavorite,
}: {
  model: ModelSpec;
  added: boolean;
  favorite: boolean;
  onAdd: () => void;
  onDelete: () => void;
  onToggleFavorite: () => void;
}) {
  return (
    <article className="model-card">
      <ProviderLogo logoKey={model.logoKey} />
      <div className="model-card-main">
        <div className="model-card-title">
          <h3>{model.label}</h3>
          <span>{model.unit}</span>
        </div>
        <p>{model.modelId}</p>
        <div className="model-facts">
          <span>{model.parameterB ? `${model.parameterB}B` : "n/a"}</span>
          <span>{model.modelSizeGb} GB</span>
          <span>{model.runtime}</span>
          <span>{model.hardwareTier}</span>
        </div>
        <div className="tag-row">
          {model.languages.slice(0, 3).map((language) => <span key={language}>{language}</span>)}
          {model.npuEligible ? <span>NPU ready</span> : null}
        </div>
      </div>
      <button type="button" className={`favorite ${favorite ? "active" : ""}`} onClick={onToggleFavorite} title="Favorite">
        <Star size={18} />
      </button>
      <button type="button" className={added ? "danger" : ""} onClick={added ? onDelete : onAdd}>
        {added ? <Trash2 size={16} /> : <Plus size={16} />}
        {added ? "Delete" : "ADD"}
      </button>
    </article>
  );
}

function ProviderLogo({ logoKey }: { logoKey?: string }) {
  const label = logoKeyLabel(logoKey);
  return <span className={`provider-logo logo-${logoKey ?? "model"}`}>{label}</span>;
}

function MiniRuntime({
  bridgeState,
  port,
  snapshot,
  onRun,
  onStop,
  onHibernate,
  onHeatup,
  onDeleteAll,
}: {
  bridgeState: BridgeState;
  port: number;
  snapshot: RuntimeSnapshot;
  onRun: () => void;
  onStop: () => void;
  onHibernate: () => void;
  onHeatup: () => void;
  onDeleteAll: () => void;
}) {
  const activeCount = snapshot.models.filter((model) => model.active).length;
  const hibernated = snapshot.models.some((model) => model.status === "hibernated");
  const installValue = Math.max(0, Math.min(100, snapshot.installProgress));
  const diskValue = snapshot.installing ? installValue : boundedMetric(snapshot.metrics.disk);
  return (
    <main className="mini-shell">
      <header className="mini-header">
        <h1>xlocllm</h1>
        <div className={`mini-port ${bridgeState === "connected" ? "connected" : "disconnected"}`}>
          <span>{port}</span>
          {bridgeState === "connected" ? <Wifi size={14} /> : <WifiOff size={14} />}
        </div>
        <span className="mini-version">v0.1.0</span>
      </header>

      <section className="mini-gauges">
        <GaugeDial label="GPU" value={snapshot.metrics.gpu} />
        <GaugeDial label="CPU" value={snapshot.metrics.cpu} />
        <GaugeDial label="RAM" value={snapshot.metrics.ram} />
      </section>

      <section className="mini-disk">
        <div>
          <span>{snapshot.installing ? `INSTALLATION ${installValue}%` : "DISK"}</span>
          <div className={`meter ${snapshot.installing ? "installing" : ""}`}><span style={{ width: `${diskValue}%` }} /></div>
        </div>
        <div className="mini-requests">
          <b>{snapshot.requests.processing}</b>
          <span>processing</span>
          <b>{snapshot.requests.queued}</b>
          <span>queue</span>
        </div>
      </section>

      <section className="mini-actions">
        <button
          type="button"
          className={snapshot.running ? "danger" : ""}
          disabled={snapshot.installing || (!snapshot.running && activeCount === 0)}
          onClick={snapshot.running ? onStop : onRun}
        >
          {snapshot.running ? <Square size={16} /> : <Play size={16} />}
          {snapshot.installing ? "Installing" : snapshot.running ? "Stop" : "Start"}
        </button>
        <button type="button" className="secondary" disabled={snapshot.installing || activeCount === 0} onClick={hibernated ? onHeatup : onHibernate}>
          {hibernated ? <RefreshCw size={16} /> : <Pause size={16} />}
          {hibernated ? "Continue" : "Pause"}
        </button>
        <button type="button" className="secondary" disabled={snapshot.running || snapshot.installing} onClick={onDeleteAll}>
          <Trash2 size={16} />
          Clear
        </button>
      </section>

      <section className="mini-status-row">
        <StatCard label="models" value={String(activeCount)} />
        <NpuCard npu={snapshot.npu} />
      </section>

      <p className="mini-note">This window must stay open and visible while browser models are working.</p>
    </main>
  );
}

function GaugeDial({ label, value }: { label: string; value: number | null }) {
  const bounded = boundedMetric(value);
  const arcLength = 157;
  const progress = arcLength - (arcLength * bounded) / 100;
  return (
    <div className={`gauge-dial ${gaugeLevel(bounded)}`}>
      <svg className="dial" viewBox="0 0 120 70" aria-hidden="true">
        <path className="dial-track" d="M 15 60 A 45 45 0 0 1 105 60" pathLength={arcLength} />
        <path
          className="dial-progress"
          d="M 15 60 A 45 45 0 0 1 105 60"
          pathLength={arcLength}
          style={{ strokeDasharray: arcLength, strokeDashoffset: progress } as CSSProperties}
        />
      </svg>
      <div className="dial-value">
        <span>{bounded}%</span>
      </div>
      <b>{label}</b>
    </div>
  );
}

function Logs({ entries }: { entries: LogEntry[] }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    ref.current?.scrollTo({ top: ref.current.scrollHeight });
  }, [entries]);
  return (
    <section className="logs">
      <h2>Logs</h2>
      <div ref={ref} className="log-list">
        {entries.length === 0 ? (
          <div className="log muted">No logs yet</div>
        ) : (
          entries.map((entry, index) => (
            <div key={`${entry.time}-${index}`} className={`log ${entry.level}`}>
              <time>{new Date(entry.time).toLocaleTimeString()}</time>
              <span>{entry.level}</span>
              <p>{entry.message}</p>
            </div>
          ))
        )}
      </div>
    </section>
  );
}

function filterModels(
  models: ModelSpec[],
  filters: Filters,
  search: string,
  sort: SortMode,
  state: {
    runtimeIds: Set<string>;
    installedIds: Set<string>;
    activeIds: Set<string>;
    favorites: Set<string>;
  },
): ModelSpec[] {
  const query = normalize(search);
  const filtered = models.filter((model) => {
    if (filters.unit !== "all" && model.unit !== filters.unit) return false;
    if (filters.taskGroup !== "all" && model.taskGroup !== filters.taskGroup) return false;
    if (filters.runtime !== "all" && model.runtime !== filters.runtime) return false;
    if (filters.hardwareTier !== "all" && model.hardwareTier !== filters.hardwareTier) return false;
    if (filters.language !== "all" && !model.languages.includes(filters.language)) return false;
    if ((model.parameterB ?? 0) < filters.paramMin || (model.parameterB ?? 0) > filters.paramMax) return false;
    if (model.modelSizeGb < filters.sizeMin || model.modelSizeGb > filters.sizeMax) return false;
    if (filters.status === "active" && !state.activeIds.has(model.modelId)) return false;
    if (filters.status === "installed" && !state.installedIds.has(model.modelId)) return false;
    if (filters.status === "favorites" && !state.favorites.has(model.modelId)) return false;
    if (filters.status === "npu" && !model.npuEligible) return false;
    if (!query) return true;
    const haystack = normalize([model.label, model.modelId, model.provider, model.unit, model.taskGroup, ...(model.tags ?? [])].join(" "));
    return haystack.includes(query);
  });

  return filtered.sort((left, right) => {
    if (sort === "name") return left.label.localeCompare(right.label);
    if (sort === "size-asc") return left.modelSizeGb - right.modelSizeGb;
    if (sort === "size-desc") return right.modelSizeGb - left.modelSizeGb;
    if (sort === "params-asc") return (left.parameterB ?? 0) - (right.parameterB ?? 0);
    if (sort === "params-desc") return (right.parameterB ?? 0) - (left.parameterB ?? 0);
    return recommendationRank(left) - recommendationRank(right) || left.label.localeCompare(right.label);
  });
}

function recommendationRank(model: ModelSpec): number {
  const tierRank: Record<HardwareTier, number> = { tiny: 0, small: 1, medium: 2, large: 3 };
  return tierRank[model.hardwareTier] * 10 + (model.availability === "verified" ? 0 : 2) + (model.npuEligible ? 0 : 1);
}

function runtimeUnits(models: RuntimeModelState[]): RuntimeUnitRequest[] {
  return models.map((model) => ({ type: model.unit, model: model.modelId }));
}

function unique(values: string[]): string[] {
  return [...new Set(values.filter(Boolean))].sort((left, right) => left.localeCompare(right));
}

function initialPort(): number {
  const value = Number(new URLSearchParams(window.location.search).get("bridgePort"));
  return Number.isFinite(value) && value > 0 ? value : defaultPort;
}

function isMiniMode(): boolean {
  const params = new URLSearchParams(window.location.search);
  return params.get("mode") === "mini" || params.get("uiMode") === "mini";
}

function updateQueryPort(port: number) {
  const url = new URL(window.location.href);
  url.searchParams.set("bridgePort", String(port));
  window.history.replaceState(null, "", url);
}

function readTheme(): Theme {
  return window.localStorage.getItem("xlocllm:theme") === "dark" ? "dark" : "light";
}

function readFavorites(): Set<string> {
  try {
    const value = JSON.parse(window.sessionStorage.getItem(favoriteStorageKey) ?? "[]");
    return new Set(Array.isArray(value) ? value.filter((item) => typeof item === "string") : []);
  } catch {
    return new Set();
  }
}

function boundedMetric(value: number | null): number {
  return value === null ? 0 : Math.max(0, Math.min(100, value));
}

function levelClass(value: number): string {
  if (value > 75) return "hot";
  if (value > 45) return "warm";
  return "cool";
}

function gaugeLevel(value: number): string {
  if (value > 80) return "level-hot";
  if (value > 55) return "level-warm";
  return "level-cool";
}

function logoKeyLabel(logoKey?: string): string {
  const labels: Record<string, string> = {
    xenova: "Xe",
    onnx: "ON",
    huggingface: "HF",
    jina: "Ji",
    mixedbread: "Mb",
    nomic: "No",
    microsoft: "MS",
    mozilla: "Mz",
    model: "AI",
  };
  return labels[logoKey ?? "model"] ?? "AI";
}

function normalize(value: string): string {
  return value.trim().toLowerCase();
}
