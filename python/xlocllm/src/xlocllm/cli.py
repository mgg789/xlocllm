from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from typing import Any

from .benchmark import benchmark as run_benchmark
from ._mode import current_mode
from .bridge import Bridge
from .catalog import model as catalog_model
from .catalog import models as catalog_models
from .native_bridge import NativeBridge
from .runtime import runtime as create_runtime
from .runtime import status as runtime_status
from .runtime import unit as create_unit


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    command = str(args.command)
    try:
        if command == "status":
            return _print_json(runtime_status())
        if command == "benchmark":
            return _print_json(
                run_benchmark(
                    args.type,
                    mode=args.mode,
                    ping_hf=args.hf,
                    timeout=args.timeout,
                    browser=args.browser,
                    browser_timeout=args.browser_timeout,
                    port=args.port,
                )
            )
        if command == "models":
            items = catalog_models(
                unit=args.unit,
                mode=args.mode,
                runtime=args.runtime,
                task=args.task,
                task_group=args.task_group,
                hardware_tier=args.hardware_tier,
                language=args.language,
                provider=args.provider,
                availability=args.availability,
                npu=args.npu,
                webgpu=args.webgpu,
                cpu=args.cpu,
                search=args.search,
                max_vram_mb=args.max_vram_mb,
                max_disk_mb=args.max_disk_mb,
                max_size_gb=args.max_size_gb,
                max_parameters_b=args.max_parameters_b,
                limit_per_unit=args.limit_per_unit,
            )
            return _print_json([item.to_dict() for item in items])
        if command == "model":
            return _print_json(catalog_model(args.name, unit=args.unit, mode=args.mode).to_dict())
        if command == "run":
            rt = create_runtime(
                [create_unit(args.unit, args.model, mode=args.mode, reasoning=args.reasoning)],
                port=args.port,
                mode=args.mode,
            )
            result = rt.run()
            return _print_json({"runtime": rt.status(), "run": result})
        if command == "bridge":
            selected_mode = current_mode(args.mode)
            bridge = (
                NativeBridge(port=args.port) if selected_mode == "native" else Bridge(port=args.port)
            ).activate(daemon=True)
            return _print_json(
                {"ok": True, "mode": selected_mode, "port": bridge.port, "url": bridge.url}
            )
    except Exception as error:  # noqa: BLE001
        print(f"xlocllm: {error}", file=sys.stderr)
        return 1
    parser.print_help()
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="xlocllm", description="xlocllm local runtime CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Print bridges, runtimes, models, and resource status")

    benchmark_parser = subparsers.add_parser("benchmark", help="Inspect local capabilities and recommend models")
    benchmark_parser.add_argument("type", nargs="?", help="Optional unit type, for example LLM or embedding")
    benchmark_parser.add_argument("--mode", choices=["native", "web"], default=None, help="Runtime mode")
    benchmark_parser.add_argument("--hf", action=argparse.BooleanOptionalAction, default=True, help="Ping Hugging Face")
    benchmark_parser.add_argument("--timeout", type=float, default=2.0, help="Network timeout in seconds")
    benchmark_parser.add_argument(
        "--browser",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Temporarily launch a paired browser to detect WebGPU/WebNN/NPU",
    )
    benchmark_parser.add_argument("--browser-timeout", type=float, default=15.0, help="Browser probing timeout")
    benchmark_parser.add_argument("--port", type=int, default=None, help="Temporary bridge port")

    models_parser = subparsers.add_parser("models", help="List catalog models")
    _add_model_filters(models_parser)

    model_parser = subparsers.add_parser("model", help="Show one catalog model")
    model_parser.add_argument("name", help="Model id, label, or alias")
    model_parser.add_argument("--unit", help="Unit type, for example LLM or embedding")
    model_parser.add_argument("--mode", choices=["native", "web"], default=None, help="Catalog mode")

    run_parser = subparsers.add_parser("run", help="Start one unit and expose the OpenAI-compatible API")
    run_parser.add_argument("--unit", required=True, help="Unit type, for example LLM or embedding")
    run_parser.add_argument("--model", required=True, help="Model id, label, or alias")
    run_parser.add_argument("--reasoning", action=argparse.BooleanOptionalAction, default=None, help="Enable or disable reasoning when supported")
    run_parser.add_argument("--mode", choices=["native", "web"], default=None, help="Runtime mode")
    run_parser.add_argument("--port", type=int, default=1146, help="Bridge port")

    bridge_parser = subparsers.add_parser("bridge", help="Start the bridge daemon")
    bridge_parser.add_argument("--mode", choices=["native", "web"], default=None, help="Bridge mode")
    bridge_parser.add_argument("--port", type=int, default=1146, help="Bridge port")

    return parser


def _add_model_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--unit", help="Filter by unit type")
    parser.add_argument("--mode", choices=["native", "web"], default=None, help="Catalog mode")
    parser.add_argument("--runtime", help="Filter by runtime backend")
    parser.add_argument("--task", help="Filter by Transformers.js task")
    parser.add_argument("--task-group", help="Filter by high-level task group")
    parser.add_argument("--hardware-tier", choices=["tiny", "small", "medium", "large"])
    parser.add_argument("--language", help="Filter by language code")
    parser.add_argument("--provider", help="Filter by model provider")
    parser.add_argument("--availability", help="Filter by availability status")
    parser.add_argument("--npu", action=argparse.BooleanOptionalAction, default=None, help="Filter NPU-eligible models")
    parser.add_argument(
        "--webgpu",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Use --no-webgpu to list only CPU/WASM fallback-capable models",
    )
    parser.add_argument("--cpu", action="store_true", help="Alias for --no-webgpu")
    parser.add_argument("--search", help="Search ids, labels, aliases, providers, units, and tags")
    parser.add_argument("--max-vram-mb", type=int, help="Maximum estimated VRAM")
    parser.add_argument("--max-disk-mb", type=int, help="Maximum estimated download/cache size")
    parser.add_argument("--max-size-gb", type=float, help="Maximum model size in GB")
    parser.add_argument("--max-parameters-b", type=float, help="Maximum parameter count in billions")
    parser.add_argument("--limit-per-unit", type=int, help="Limit returned rows per unit")


def _print_json(value: Any) -> int:
    print(json.dumps(value, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
