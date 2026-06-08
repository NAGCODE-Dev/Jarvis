from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime
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


def _read_prompt(args: argparse.Namespace) -> str:
    prompt = args.prompt or ""
    if args.stdin:
        stdin_text = input_stream_read()
        if stdin_text:
            prompt = f"{prompt}\n\n{stdin_text}".strip()
    for path in args.file or []:
        file_content = path.read_text(encoding="utf-8")
        prompt = f"{prompt}\n\n[FILE: {path}]\n{file_content}".strip()
    return prompt


def _parse_frontmatter(note_text: str) -> tuple[dict[str, str], str]:
    if not note_text.startswith("---\n"):
        return {}, note_text
    end = note_text.find("\n---\n", 4)
    if end == -1:
        return {}, note_text
    block = note_text[4:end]
    body = note_text[end + 5 :]
    parsed: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        parsed[key.strip()] = value.strip().strip("'\"")
    return parsed, body


def _infer_workspace_from_note_path(note_path: Path, frontmatter: dict[str, str]) -> str | None:
    if frontmatter.get("workspace"):
        return frontmatter["workspace"]
    path_parts = [part.lower() for part in note_path.parts]
    for candidate in ("jarvis", "faculdade", "crossfit", "programacao", "minecraft", "linux", "musculacao", "pessoal"):
        if candidate.lower() in path_parts:
            return candidate
    return None


def _resolve_note_model(frontmatter: dict[str, str], explicit_model: str | None) -> str:
    if explicit_model:
        return explicit_model
    mode = frontmatter.get("jarvis_mode", "").lower()
    if mode in {"research", "pesquisa", "study"}:
        return "jarvis-pesquisador-safe"
    if mode in {"code", "coding", "programming", "programacao"}:
        return "jarvis-programador-safe"
    return "jarvis-safe"


def _build_note_prompt(note_path: Path, note_body: str, instruction: str, workspace: str | None) -> str:
    workspace_line = workspace or "none"
    task = instruction or "Leia a nota e responda em Markdown útil e objetivo."
    return (
        "Você está ajudando com uma nota do Obsidian.\n"
        f"Path da nota: {note_path}\n"
        f"Workspace inferido: {workspace_line}\n"
        f"Tarefa: {task}\n\n"
        "Conteúdo atual da nota:\n"
        f"{note_body.strip()}\n"
    )


def _append_obsidian_response(note_path: Path, title: str, response: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    block = f"\n\n## {title} ({timestamp})\n\n{response.strip()}\n"
    note_path.write_text(note_path.read_text(encoding="utf-8") + block, encoding="utf-8")


def _resolve_note_path(note_path: Path) -> Path:
    note_path = note_path.expanduser()
    if not note_path.is_absolute():
        note_path = Path.cwd() / note_path
    return note_path


def _list_markdown_files(root: Path, recursive: bool = True) -> list[Path]:
    pattern = "**/*.md" if recursive else "*.md"
    return sorted(path for path in root.glob(pattern) if path.is_file())


def input_stream_read() -> str:
    try:
        import sys

        if sys.stdin.isatty():
            return ""
        return sys.stdin.read()
    except Exception:
        return ""


def _chat_request(*, model: str, messages: list[dict[str, str]], temperature: float | None, timeout: float) -> str:
    payload: dict[str, Any] = {"model": model, "messages": messages}
    if temperature is not None:
        payload["temperature"] = temperature
    response = httpx.post(
        f"http://{settings.host}:{settings.port}/v1/chat/completions",
        headers={"Authorization": "Bearer local"},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    body = response.json()
    return body["choices"][0]["message"]["content"]


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


def cmd_chat(args: argparse.Namespace) -> int:
    prompt = _read_prompt(args)
    if not prompt:
        print(json.dumps({"status": "error", "detail": "No prompt provided."}, indent=2, ensure_ascii=False))
        return 1

    try:
        print(
            _chat_request(
                model=args.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=args.temperature,
                timeout=args.timeout,
            )
        )
        return 0
    except Exception as exc:
        print(json.dumps({"status": "error", "detail": str(exc)}, indent=2, ensure_ascii=False))
        return 1


def cmd_repl(args: argparse.Namespace) -> int:
    model = args.model
    history: list[dict[str, str]] = []
    max_turns = max(1, args.max_turns)

    print(f"Jarvis chat on {model}")
    print("Commands: /exit, /clear, /model <name>, /file <path>")

    while True:
        try:
            prompt = input("\nVocê> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[jarvis] bye")
            return 0

        if not prompt:
            continue
        if prompt in {"/exit", "/quit"}:
            print("[jarvis] bye")
            return 0
        if prompt == "/clear":
            history.clear()
            print("[jarvis] contexto limpo")
            continue
        if prompt.startswith("/model "):
            model = prompt.split(" ", 1)[1].strip()
            print(f"[jarvis] model = {model}")
            continue
        if prompt.startswith("/file "):
            raw_path = prompt.split(" ", 1)[1].strip()
            path = Path(raw_path).expanduser()
            if not path.is_absolute():
                path = Path.cwd() / path
            try:
                file_content = path.read_text(encoding="utf-8")
            except Exception as exc:
                print(f"[jarvis] erro lendo arquivo: {exc}")
                continue
            prompt = f"[FILE: {path}]\n{file_content}"

        user_message = {"role": "user", "content": prompt}
        messages = history + [user_message]
        try:
            answer = _chat_request(
                model=model,
                messages=messages,
                temperature=args.temperature,
                timeout=args.timeout,
            )
        except Exception as exc:
            print(json.dumps({"status": "error", "detail": str(exc)}, indent=2, ensure_ascii=False))
            continue

        print(f"\nJarvis> {answer}")
        history.extend([user_message, {"role": "assistant", "content": answer}])
        history = history[-(max_turns * 2) :]


def cmd_obsidian_note(args: argparse.Namespace) -> int:
    note_path = _resolve_note_path(args.note)
    if not note_path.exists():
        print(json.dumps({"status": "error", "detail": f"Note not found: {note_path}"}, indent=2, ensure_ascii=False))
        return 1

    raw = note_path.read_text(encoding="utf-8")
    frontmatter, body = _parse_frontmatter(raw)
    workspace = args.workspace or _infer_workspace_from_note_path(note_path, frontmatter)
    model = _resolve_note_model(frontmatter, args.model)
    prompt = _build_note_prompt(note_path, body, args.instruction or "", workspace)

    try:
        answer = _chat_request(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=args.temperature,
            timeout=args.timeout,
        )
    except Exception as exc:
        print(json.dumps({"status": "error", "detail": str(exc)}, indent=2, ensure_ascii=False))
        return 1

    if args.append:
        title = args.title or "Jarvis"
        _append_obsidian_response(note_path, title, answer)

    print(answer)
    return 0


def cmd_obsidian_sync(args: argparse.Namespace) -> int:
    note_path = _resolve_note_path(args.note)
    if not note_path.exists():
        print(json.dumps({"status": "error", "detail": f"Note not found: {note_path}"}, indent=2, ensure_ascii=False))
        return 1

    raw = note_path.read_text(encoding="utf-8")
    frontmatter, body = _parse_frontmatter(raw)
    workspace = args.workspace or _infer_workspace_from_note_path(note_path, frontmatter) or "pessoal"
    service = KnowledgeService(OllamaClient())
    result = service.ingest_note(
        domain=workspace,
        title=args.title or note_path.stem,
        content=body.strip(),
        source_path=str(note_path),
        force=args.force,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_obsidian_sync_dir(args: argparse.Namespace) -> int:
    directory = args.directory.expanduser()
    if not directory.is_absolute():
        directory = Path.cwd() / directory
    if not directory.exists() or not directory.is_dir():
        print(json.dumps({"status": "error", "detail": f"Directory not found: {directory}"}, indent=2, ensure_ascii=False))
        return 1

    files = _list_markdown_files(directory, recursive=not args.non_recursive)
    if not files:
        print(json.dumps({"status": "ok", "synced_files": 0, "results": []}, indent=2, ensure_ascii=False))
        return 0

    service = KnowledgeService(OllamaClient())
    results: list[dict[str, Any]] = []
    for note_path in files:
        raw = note_path.read_text(encoding="utf-8")
        frontmatter, body = _parse_frontmatter(raw)
        workspace = args.workspace or _infer_workspace_from_note_path(note_path, frontmatter) or "pessoal"
        result = service.ingest_note(
            domain=workspace,
            title=note_path.stem,
            content=body.strip(),
            source_path=str(note_path),
            force=args.force,
        )
        results.append({"file": str(note_path), **result})

    print(json.dumps({"status": "ok", "synced_files": len(results), "results": results}, indent=2, ensure_ascii=False))
    return 0


def cmd_obsidian_remember(args: argparse.Namespace) -> int:
    note_path = _resolve_note_path(args.note)
    if not note_path.exists():
        print(json.dumps({"status": "error", "detail": f"Note not found: {note_path}"}, indent=2, ensure_ascii=False))
        return 1

    raw = note_path.read_text(encoding="utf-8")
    frontmatter, body = _parse_frontmatter(raw)
    workspace = args.workspace or _infer_workspace_from_note_path(note_path, frontmatter) or "jarvis"
    memory = MemoryManager()
    field = args.field or f"obsidian.{note_path.stem.lower().replace(' ', '-')}"
    excerpt = body.strip()[: args.max_chars]
    result = memory.apply(
        MemoryAction(
            action="append_workspace_note",
            field=field,
            value=f"Nota: {note_path.stem}\nPath: {note_path}\n\n{excerpt}",
            source="obsidian-cli",
            workspace=workspace,
        )
    )
    print(json.dumps({"workspace": workspace, **result}, indent=2, ensure_ascii=False))
    return 0


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

    chat_parser = subparsers.add_parser("chat")
    chat_parser.add_argument("prompt", nargs="?")
    chat_parser.add_argument("--model", default="jarvis-safe")
    chat_parser.add_argument("--file", type=Path, action="append")
    chat_parser.add_argument("--stdin", action="store_true")
    chat_parser.add_argument("--temperature", type=float)
    chat_parser.add_argument("--timeout", type=float, default=300.0)
    chat_parser.set_defaults(func=cmd_chat)

    repl_parser = subparsers.add_parser("repl")
    repl_parser.add_argument("--model", default="jarvis-safe")
    repl_parser.add_argument("--temperature", type=float)
    repl_parser.add_argument("--timeout", type=float, default=300.0)
    repl_parser.add_argument("--max-turns", type=int, default=6)
    repl_parser.set_defaults(func=cmd_repl)

    obsidian_parser = subparsers.add_parser("obsidian-note")
    obsidian_parser.add_argument("note", type=Path)
    obsidian_parser.add_argument("instruction", nargs="?")
    obsidian_parser.add_argument("--model")
    obsidian_parser.add_argument("--workspace")
    obsidian_parser.add_argument("--append", action="store_true")
    obsidian_parser.add_argument("--title")
    obsidian_parser.add_argument("--temperature", type=float)
    obsidian_parser.add_argument("--timeout", type=float, default=300.0)
    obsidian_parser.set_defaults(func=cmd_obsidian_note)

    obsidian_sync_parser = subparsers.add_parser("obsidian-sync")
    obsidian_sync_parser.add_argument("note", type=Path)
    obsidian_sync_parser.add_argument("--workspace")
    obsidian_sync_parser.add_argument("--title")
    obsidian_sync_parser.add_argument("--force", action="store_true")
    obsidian_sync_parser.set_defaults(func=cmd_obsidian_sync)

    obsidian_sync_dir_parser = subparsers.add_parser("obsidian-sync-dir")
    obsidian_sync_dir_parser.add_argument("directory", type=Path)
    obsidian_sync_dir_parser.add_argument("--workspace")
    obsidian_sync_dir_parser.add_argument("--force", action="store_true")
    obsidian_sync_dir_parser.add_argument("--non-recursive", action="store_true")
    obsidian_sync_dir_parser.set_defaults(func=cmd_obsidian_sync_dir)

    obsidian_remember_parser = subparsers.add_parser("obsidian-remember")
    obsidian_remember_parser.add_argument("note", type=Path)
    obsidian_remember_parser.add_argument("--workspace")
    obsidian_remember_parser.add_argument("--field")
    obsidian_remember_parser.add_argument("--max-chars", type=int, default=1600)
    obsidian_remember_parser.set_defaults(func=cmd_obsidian_remember)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
