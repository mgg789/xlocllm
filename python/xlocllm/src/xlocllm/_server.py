from __future__ import annotations

import argparse
import asyncio
import json
import os
import time
import uuid
from collections.abc import AsyncIterator
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from ._paths import web_dist_dir
from .catalog import all_models, all_units
from .registry import remove_bridge, upsert_bridge


class BrowserHub:
    def __init__(self, token: str) -> None:
        self.token = token
        self.websocket: WebSocket | None = None
        self.pending: dict[str, asyncio.Future[Any]] = {}
        self.streams: dict[str, asyncio.Queue[dict[str, Any]]] = {}
        self.status: dict[str, Any] = {"connected": False}
        self.logs: list[dict[str, Any]] = []

    async def connect(self, websocket: WebSocket, token: str | None) -> None:
        if token != self.token:
            await websocket.close(code=4401)
            return
        await websocket.accept()
        self.websocket = websocket
        self.status["connected"] = True
        self.log("info", "Browser runtime connected")
        try:
            while True:
                message = await websocket.receive_json()
                self.handle_browser_message(message)
        except WebSocketDisconnect:
            self.log("warn", "Browser runtime disconnected")
        finally:
            if self.websocket is websocket:
                self.websocket = None
                self.status["connected"] = False
                for future in self.pending.values():
                    if not future.done():
                        future.set_exception(RuntimeError("Browser runtime disconnected"))
                self.pending.clear()

    def handle_browser_message(self, message: dict[str, Any]) -> None:
        message_type = message.get("type")
        request_id = str(message.get("id", ""))
        if message_type == "browser_status":
            payload = message.get("payload") or {}
            if isinstance(payload, dict):
                self.status.update(payload)
            return
        if message_type == "rpc_chunk" and request_id in self.streams:
            self.streams[request_id].put_nowait({"type": "chunk", "payload": message.get("payload") or {}})
            return
        if message_type == "rpc_complete" and request_id in self.streams:
            self.streams[request_id].put_nowait({"type": "complete"})
            return
        future = self.pending.get(request_id)
        if not future:
            return
        if message_type == "rpc_result":
            payload = message.get("payload")
            if isinstance(payload, dict):
                self.status.update(payload)
            future.set_result(payload)
        elif message_type == "rpc_error":
            error = str(message.get("error") or "Browser RPC failed")
            self.log("error", error)
            future.set_exception(RuntimeError(error))

    async def rpc(
        self,
        request_type: str,
        *,
        endpoint: str | None = None,
        units: list[dict[str, Any]] | None = None,
        payload: dict[str, Any] | None = None,
        timeout: float = 900.0,
    ) -> Any:
        if not self.websocket:
            raise HTTPException(status_code=503, detail="Browser runtime is not connected")
        request_id = uuid.uuid4().hex
        loop = asyncio.get_running_loop()
        future: asyncio.Future[Any] = loop.create_future()
        self.pending[request_id] = future
        await self.websocket.send_json(
            {
                "id": request_id,
                "type": request_type,
                "endpoint": endpoint,
                "units": units,
                "payload": payload,
            }
        )
        try:
            return await asyncio.wait_for(future, timeout=timeout)
        finally:
            self.pending.pop(request_id, None)

    async def stream_rpc(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float = 900.0,
    ) -> AsyncIterator[str]:
        if not self.websocket:
            raise HTTPException(status_code=503, detail="Browser runtime is not connected")
        request_id = uuid.uuid4().hex
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        self.streams[request_id] = queue
        loop = asyncio.get_running_loop()
        future: asyncio.Future[Any] = loop.create_future()
        self.pending[request_id] = future
        await self.websocket.send_json(
            {
                "id": request_id,
                "type": "infer_stream",
                "endpoint": endpoint,
                "payload": payload,
            }
        )
        deadline = loop.time() + timeout
        try:
            while True:
                remaining = max(0.1, deadline - loop.time())
                item = await asyncio.wait_for(queue.get(), timeout=remaining)
                if item["type"] == "complete":
                    break
                chunk = item.get("payload", {}).get("chunk", "")
                if chunk:
                    yield str(chunk)
            await asyncio.wait_for(future, timeout=5)
        finally:
            self.streams.pop(request_id, None)
            self.pending.pop(request_id, None)

    def log(self, level: str, message: str) -> None:
        self.logs.append({"time": time.time(), "level": level, "message": message})
        self.logs = self.logs[-500:]


def create_app(port: int, token: str, live_time: float | None = None) -> FastAPI:
    hub = BrowserHub(token)
    app = FastAPI(title="xlocllm bridge", version="0.1.0")
    app.state.hub = hub
    app.state.started_at = time.time()
    app.state.live_time = live_time

    @app.on_event("startup")
    async def schedule_live_time_shutdown() -> None:
        if live_time is not None and live_time > 0:
            asyncio.create_task(shutdown_after(app, port, live_time))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "https://localhost",
            "https://127.0.0.1",
        ],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    dist = web_dist_dir()
    if dist is not None:
        app.mount("/ui", StaticFiles(directory=dist, html=True), name="ui")

    @app.get("/")
    async def root() -> dict[str, Any]:
        ui = f"http://127.0.0.1:{port}/ui/" if dist is not None else "http://127.0.0.1:5173"
        return {"name": "xlocllm bridge", "port": port, "ui": ui}

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {"ok": True, "port": port, "browser_connected": bool(hub.websocket)}

    @app.websocket("/xlocllm/ws")
    async def websocket_endpoint(websocket: WebSocket) -> None:
        mode = websocket.query_params.get("mode")
        await hub.connect(websocket, websocket.query_params.get("token"))
        if mode == "mini":
            hub.log("info", "Mini browser window closed; shutting down bridge daemon")
            remove_bridge(port)
            server = getattr(app.state, "uvicorn_server", None)
            if server is not None:
                server.should_exit = True

    @app.get("/xlocllm/v1/status")
    async def status() -> dict[str, Any]:
        return bridge_status(port, hub)

    @app.get("/xlocllm/v1/models")
    async def xloc_models() -> dict[str, Any]:
        return {"models": all_models()}

    @app.get("/xlocllm/v1/units")
    async def xloc_units() -> dict[str, Any]:
        return {"units": all_units()}

    @app.get("/xlocllm/v1/logs")
    async def logs(limit: int = 200) -> dict[str, Any]:
        return {"logs": hub.logs[-limit:]}

    @app.post("/xlocllm/v1/runtime/install")
    async def install(payload: dict[str, Any]) -> Any:
        return await safe_rpc(hub, "install", units=list(payload.get("units") or []), timeout=3600)

    @app.post("/xlocllm/v1/runtime/run")
    async def run(payload: dict[str, Any]) -> Any:
        return await safe_rpc(hub, "run", units=list(payload.get("units") or []), timeout=1800)

    @app.post("/xlocllm/v1/runtime/stop")
    async def stop() -> Any:
        return await safe_rpc(hub, "stop", timeout=60)

    @app.post("/xlocllm/v1/runtime/hibernate")
    async def hibernate() -> Any:
        return await safe_rpc(hub, "hibernate", timeout=300)

    @app.post("/xlocllm/v1/runtime/heatup")
    async def heatup() -> Any:
        return await safe_rpc(hub, "heatup", timeout=1800)

    @app.post("/xlocllm/v1/runtime/reload")
    async def reload_runtime(payload: dict[str, Any]) -> Any:
        await safe_rpc(hub, "stop", timeout=60)
        return await safe_rpc(hub, "run", units=list(payload.get("units") or []), timeout=1800)

    @app.post("/xlocllm/v1/runtime/set_active")
    async def set_active(payload: dict[str, Any]) -> Any:
        return await safe_rpc(hub, "set_active", payload=payload, timeout=300)

    @app.post("/xlocllm/v1/models/delete")
    async def delete_model(payload: dict[str, Any]) -> Any:
        return await safe_rpc(hub, "delete_model", payload=payload, timeout=300)

    @app.post("/xlocllm/v1/models/delete_all")
    async def delete_all_models() -> Any:
        return await safe_rpc(hub, "delete_all_models", timeout=600)

    @app.post("/xlocllm/v1/invoke/{endpoint:path}")
    async def invoke(endpoint: str, payload: dict[str, Any]) -> Any:
        return await safe_rpc(hub, "infer", endpoint=endpoint.replace("/", "."), payload=payload, timeout=1800)

    @app.get("/v1/models")
    async def openai_models() -> dict[str, Any]:
        return {
            "object": "list",
            "data": [
                {
                    "id": model["modelId"],
                    "object": "model",
                    "created": 0,
                    "owned_by": "xlocllm",
                }
                for model in all_models()
            ],
        }

    @app.post("/v1/chat/completions")
    async def chat_completions(payload: dict[str, Any]) -> Any:
        if payload.get("stream"):
            return StreamingResponse(stream_chat(hub, payload), media_type="text/event-stream")
        result = await safe_rpc(hub, "infer", endpoint="chat.completions", payload=payload, timeout=1800)
        return openai_chat_response(payload, result)

    @app.post("/v1/responses")
    async def responses(payload: dict[str, Any]) -> Any:
        result = await safe_rpc(hub, "infer", endpoint="responses", payload=payload, timeout=1800)
        content = extract_content(result)
        response_id = f"resp_{uuid.uuid4().hex}"
        return {
            "id": response_id,
            "object": "response",
            "created_at": int(time.time()),
            "model": payload.get("model") or "xlocllm",
            "output": [
                {
                    "id": f"msg_{uuid.uuid4().hex}",
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": content}],
                }
            ],
            "output_text": content,
        }

    @app.post("/v1/embeddings")
    async def embeddings(payload: dict[str, Any]) -> Any:
        result = await safe_rpc(hub, "infer", endpoint="embeddings", payload=payload, timeout=1800)
        vectors = result.get("embeddings") if isinstance(result, dict) else result
        return {
            "object": "list",
            "model": payload.get("model") or "xlocllm-embedding",
            "data": [
                {"object": "embedding", "index": index, "embedding": vector}
                for index, vector in enumerate(vectors or [])
            ],
        }

    @app.post("/xlocllm/v1/shutdown")
    async def shutdown() -> dict[str, Any]:
        remove_bridge(port)
        server = getattr(app.state, "uvicorn_server", None)
        if server is not None:
            server.should_exit = True
        return {"ok": True}

    return app


async def safe_rpc(
    hub: BrowserHub,
    request_type: str,
    *,
    endpoint: str | None = None,
    units: list[dict[str, Any]] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: float = 900.0,
) -> Any:
    try:
        return await hub.rpc(
            request_type,
            endpoint=endpoint,
            units=units,
            payload=payload,
            timeout=timeout,
        )
    except HTTPException:
        raise
    except RuntimeError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


async def stream_chat(hub: BrowserHub, payload: dict[str, Any]) -> AsyncIterator[str]:
    chat_id = f"chatcmpl_{uuid.uuid4().hex}"
    model = str(payload.get("model") or "xlocllm")
    async for chunk in hub.stream_rpc("chat.completions", payload):
        data = {
            "id": chat_id,
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": model,
            "choices": [{"index": 0, "delta": {"content": chunk}, "finish_reason": None}],
        }
        yield f"data: {json.dumps(data)}\n\n"
    done = {
        "id": chat_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
    }
    yield f"data: {json.dumps(done)}\n\n"
    yield "data: [DONE]\n\n"


def openai_chat_response(payload: dict[str, Any], result: Any) -> dict[str, Any]:
    content = extract_content(result)
    return {
        "id": f"chatcmpl_{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": payload.get("model") or "xlocllm",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
    }


def extract_content(result: Any) -> str:
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        if isinstance(result.get("content"), str):
            return str(result["content"])
        raw = result.get("raw")
        if isinstance(raw, dict):
            try:
                return str(raw["choices"][0]["message"]["content"])
            except (KeyError, IndexError, TypeError):
                pass
        try:
            return str(result["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError):
            return json.dumps(result)
    return json.dumps(result)


def bridge_status(port: int, hub: BrowserHub) -> dict[str, Any]:
    return {
        "ok": True,
        "port": port,
        "browser_connected": bool(hub.websocket),
        "started_at": getattr(hub, "started_at", None),
        "runtime": hub.status,
        "logs": hub.logs[-200:],
    }


async def shutdown_after(app: FastAPI, port: int, delay: float) -> None:
    await asyncio.sleep(delay)
    remove_bridge(port)
    server = getattr(app.state, "uvicorn_server", None)
    if server is not None:
        server.should_exit = True


def run_server(port: int, token: str, live_time: float | None = None) -> None:
    app = create_app(port, token, live_time)
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level=os.environ.get("XLOCLLM_LOG_LEVEL", "warning"))
    server = uvicorn.Server(config)
    app.state.uvicorn_server = server
    upsert_bridge(port, pid=os.getpid(), token=token)
    server.run()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=1146)
    parser.add_argument("--token", required=True)
    parser.add_argument("--live-time", type=float, default=None)
    args = parser.parse_args()
    run_server(args.port, args.token, args.live_time)


if __name__ == "__main__":
    main()
