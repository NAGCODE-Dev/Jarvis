from __future__ import annotations

import argparse
import json
from typing import Any

import httpx

from jarvis.benchmark import BenchmarkService
from jarvis.config import settings
from jarvis.knowledge import KnowledgeService
from jarvis.memory import MemoryAction, MemoryManager
from jarvis.model_registry import ModelRegistry
from jarvis.ollama_client import OllamaClient


def _coerce_value(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        lowered = raw.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if lowered == "null":
            return None
        return raw


def cmd_index_knowledge(args: argparse.Namespace) -> int:
    service = KnowledgeService(OllamaClient())
    result = service.index_domains(domains=args.domains, force=args.force)
    print(json.dumps(result, indent=2))
    return 0


def cmd_search_knowledge(args: argparse.Namespace) -> int:
    service = KnowledgeService(OllamaClient())
    results = service.search(args.query, domain=args.domain, top_k=args.top_k)
    print(json.dumps([result.model_dump() for result in results], indent=2, ensure_ascii=False))
    return 0


def cmd_smoke(args: argparse.Namespace) -> int:
    checks: dict[str, object] = {}
    failures = 0

    try:
        response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=5.0)
        response.raise_for_status()
        checks["ollama"] = {"status": "ok"}
    except Exception as exc:
        checks["ollama"] = {"status": "error", "detail": str(exc)}
        failures += 1

    try:
        response = httpx.get(f"{settings.qdrant_url}/collections", timeout=5.0)
        response.raise_for_status()
        checks["qdrant"] = {"status": "ok"}
    except Exception as exc:
        checks["qdrant"] = {"status": "error", "detail": str(exc)}
        failures += 1

    try:
        response = httpx.get(f"http://{settings.host}:{settings.port}/api/status", timeout=5.0)
        response.raise_for_status()
        checks["jarvis-core"] = response.json()
    except Exception as exc:
        checks["jarvis-core"] = {"status": "error", "detail": str(exc)}
        failures += 1

    if failures:
        print(json.dumps({"status": "failed", "checks": checks}, indent=2, ensure_ascii=False))
        return 1

    print(json.dumps({"status": "ok", "checks": checks}, indent=2, ensure_ascii=False))
    return 0


def cmd_benchmark(args: argparse.Namespace) -> int:
    ollama = OllamaClient()
    service = BenchmarkService(ollama)
    registry = ModelRegistry()
    results = service.run(args.models)
    registry.save_benchmark(results)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


def cmd_memory_action(args: argparse.Namespace) -> int:
    memory = MemoryManager()
    action = MemoryAction(
        action=args.action,
        field=args.field,
        value=_coerce_value(args.value),
        source=args.source,
        workspace=args.workspace,
    )
    result = memory.apply(action)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_show_context(args: argparse.Namespace) -> int:
    memory = MemoryManager()
    fields = args.field or None
    context = memory.resolve_context(fields=fields, workspace=args.workspace, include_archive=args.include_archive)
    print(json.dumps(context, indent=2, ensure_ascii=False))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    try:
        response = httpx.get(f"http://{settings.host}:{settings.port}/api/status", timeout=5.0)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "error", "detail": str(exc)}, indent=2, ensure_ascii=False))
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="jarvis")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index-knowledge")
    index_parser.add_argument("--domain", dest="domains", action="append")
    index_parser.add_argument("--force", action="store_true")
    index_parser.set_defaults(func=cmd_index_knowledge)

    search_parser = subparsers.add_parser("search-knowledge")
    search_parser.add_argument("query")
    search_parser.add_argument("--domain")
    search_parser.add_argument("--top-k", type=int, default=5)
    search_parser.set_defaults(func=cmd_search_knowledge)

    smoke_parser = subparsers.add_parser("smoke")
    smoke_parser.set_defaults(func=cmd_smoke)

    benchmark_parser = subparsers.add_parser("benchmark")
    benchmark_parser.add_argument("--model", dest="models", action="append")
    benchmark_parser.set_defaults(func=cmd_benchmark)

    memory_parser = subparsers.add_parser("memory-action")
    memory_parser.add_argument("action")
    memory_parser.add_argument("field")
    memory_parser.add_argument("value")
    memory_parser.add_argument("--source", default="cli")
    memory_parser.add_argument("--workspace")
    memory_parser.set_defaults(func=cmd_memory_action)

    context_parser = subparsers.add_parser("show-context")
    context_parser.add_argument("--workspace")
    context_parser.add_argument("--field", action="append")
    context_parser.add_argument("--include-archive", action="store_true")
    context_parser.set_defaults(func=cmd_show_context)

    status_parser = subparsers.add_parser("status")
    status_parser.set_defaults(func=cmd_status)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
