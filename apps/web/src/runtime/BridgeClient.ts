import type { BrowserRpcRequest } from "../types";
import { RuntimeHost } from "./RuntimeHost";

type BridgeState = "disabled" | "connecting" | "connected" | "error";

export class BridgeClient {
  private ws?: WebSocket;
  private reconnectTimer?: number;
  private stopped = false;
  private mode = "full";
  private unsubscribeHost?: () => void;
  private stateListeners = new Set<(state: BridgeState) => void>();

  constructor(private readonly host: RuntimeHost) {
    this.unsubscribeHost = this.host.subscribe(() => {
      this.send({ type: "browser_status", payload: this.host.status() });
    });
  }

  subscribe(listener: (state: BridgeState) => void): () => void {
    this.stateListeners.add(listener);
    return () => this.stateListeners.delete(listener);
  }

  startFromLocation(location: Location): void {
    const params = new URLSearchParams(location.search);
    const port = params.get("bridgePort");
    const token = params.get("pairingToken");
    this.mode = params.get("mode") ?? params.get("uiMode") ?? "full";
    if (!port || !token) {
      this.setState("disabled");
      return;
    }
    this.connect(Number(port), token);
  }

  stop(): void {
    this.stopped = true;
    if (this.reconnectTimer) window.clearTimeout(this.reconnectTimer);
    this.unsubscribeHost?.();
    this.ws?.close();
  }

  private connect(port: number, token: string): void {
    this.setState("connecting");
    const ws = new WebSocket(
      `ws://127.0.0.1:${port}/xlocllm/ws?token=${encodeURIComponent(token)}&mode=${encodeURIComponent(this.mode)}`,
    );
    this.ws = ws;

    ws.onopen = () => {
      this.setState("connected");
      this.send({ type: "browser_status", payload: this.host.status() });
    };

    ws.onmessage = (event) => {
      void this.handleMessage(event.data);
    };

    ws.onclose = () => {
      if (this.stopped) return;
      this.setState("connecting");
      this.reconnectTimer = window.setTimeout(() => this.connect(port, token), 1000);
    };

    ws.onerror = () => {
      this.setState("error");
    };
  }

  private async handleMessage(data: string): Promise<void> {
    const request = JSON.parse(data) as BrowserRpcRequest;
    const emitStream = (chunk: string) => {
      this.send({ type: "rpc_chunk", id: request.id, payload: { chunk } });
    };
    try {
      const result = await this.host.handleRpc(request, emitStream);
      this.send({ type: "rpc_result", id: request.id, payload: result });
      this.send({ type: "browser_status", payload: this.host.status() });
    } catch (error) {
      this.send({ type: "rpc_error", id: request.id, error: String(error instanceof Error ? error.message : error) });
      this.send({ type: "browser_status", payload: this.host.status() });
    } finally {
      if (request.type === "infer_stream") {
        this.send({ type: "rpc_complete", id: request.id });
      }
    }
  }

  private send(message: Record<string, unknown>): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  private setState(state: BridgeState): void {
    for (const listener of this.stateListeners) listener(state);
  }
}
