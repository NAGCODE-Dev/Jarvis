from __future__ import annotations

import difflib
import json
import time
from pathlib import PurePosixPath
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from jarvis.benchmark import BenchmarkService
from jarvis.events import EventBus
from jarvis.config import settings
from jarvis.knowledge import KnowledgeService
from jarvis.memory import MemoryAction, MemoryService
from jarvis.model_registry import ModelRegistry
from jarvis.ollama_client import OllamaClient
from jarvis.router import JarvisRouter
from jarvis.schemas import (
    BenchmarkRequest,
    ChatMessage,
    ChatCompletionRequest,
    EmbeddingRequest,
    KnowledgeIngestNoteRequest,
    KnowledgeIndexRequest,
    KnowledgeSearchRequest,
    MemoryFactRequest,
    StateUpdateRequest,
    SummarizeMemoryRequest,
    SessionApprovalActionRequest,
    SessionApprovalBatchActionRequest,
    SessionApprovalRequest,
    SessionCheckpointCreateRequest,
    SessionCreateRequest,
    SessionMessageRequest,
    SessionNoteSyncRequest,
    SessionWorkspaceTurnRequest,
    SessionOperationRequest,
    SessionTaskCreateRequest,
    SessionTaskUpdateRequest,
    SessionUpdateRequest,
    TerminalNativeOpenRequest,
    TerminalRunRequest,
    TerminalSessionCreateRequest,
    TerminalSessionResizeRequest,
    TerminalSessionWriteRequest,
    TerminalSignalRequest,
    TimelineEntryRequest,
    WorkspaceBatchEditRequest,
    WorkspaceDirectoryCreateRequest,
    WorkspaceEditAssistRequest,
    WorkspaceFileWriteRequest,
    WorkspaceRenameRequest,
    WorkspaceTaskAssistRequest,
    WorkspaceMemoryRequest,
)
from jarvis.sessions import SessionStore
from jarvis.terminal import TerminalService
from jarvis.workspace import WorkspaceService


def create_api_router(ollama: OllamaClient, memory: MemoryService, knowledge: KnowledgeService) -> APIRouter:
    router = APIRouter()
    jarvis = JarvisRouter(ollama=ollama, memory=memory, knowledge=knowledge)
    benchmarks = BenchmarkService(ollama=ollama)
    registry = ModelRegistry()
    sessions = SessionStore()
    workspace = WorkspaceService()
    terminal = TerminalService()
    events = EventBus()

    def _persist_session_event(event):
        session_id = event.payload.get("session_id")
        if not session_id:
            return
        payload = {key: value for key, value in event.payload.items() if key != "session_id"}
        try:
            sessions.append_event(session_id, event_type=event.type, payload=payload, source=payload.get("source") or "event_bus")
        except FileNotFoundError:
            return

    events.subscribe("*", _persist_session_event)

    def emit_session_event(session_id: str, event_type: str, payload: dict | None = None, source: str = "jarvis") -> None:
        enriched = {"session_id": session_id, **(payload or {}), "source": source}
        events.emit(event_type, enriched)

    def _maybe_create_automatic_checkpoint(event) -> None:
        session_id = event.payload.get("session_id")
        if not session_id:
            return
        event_type = event.type
        title = None
        summary = None

        if event_type == "task_completed":
            title = "Checkpoint automático: tarefa concluída"
            summary = f"task_id={event.payload.get('task_id')} fase={event.payload.get('phase')}"
        elif event_type == "approval_applied":
            title = "Checkpoint automático: ação aplicada"
            summary = f"approval_id={event.payload.get('approval_id')} tipo={event.payload.get('kind')}"
        elif event_type == "workspace_changed":
            action = str(event.payload.get("action") or "").strip()
            if action not in {"rename_path", "delete_path"}:
                return
            title = "Checkpoint automático: mudança estrutural no workspace"
            summary = f"action={action} path={event.payload.get('path')}"
        elif event_type == "command_executed":
            exit_code = event.payload.get("exit_code")
            if exit_code in (None, 0):
                return
            title = "Checkpoint automático: comando com falha"
            summary = f"exit_code={exit_code} command={event.payload.get('command')}"
        else:
            return

        try:
            session, checkpoint = sessions.create_checkpoint(
                session_id,
                title=title,
                summary=summary,
                source="auto",
                trigger_event=event_type,
            )
            sessions.append_operation(
                session_id,
                kind="checkpoint_auto",
                title=f"Gerou checkpoint automático {checkpoint.get('title') or checkpoint.get('id')}",
                path=checkpoint.get("active_file"),
                detail=checkpoint.get("summary"),
                metadata={"checkpoint_id": checkpoint.get("id"), "trigger_event": event_type},
            )
            events.emit(
                "checkpoint_created",
                {
                    "session_id": session_id,
                    "checkpoint_id": checkpoint.get("id"),
                    "title": checkpoint.get("title"),
                    "source": "auto",
                    "trigger_event": event_type,
                },
            )
        except FileNotFoundError:
            return

    for auto_event in ("task_completed", "approval_applied", "workspace_changed", "command_executed"):
        events.subscribe(auto_event, _maybe_create_automatic_checkpoint)

    def require_session(session_id: str) -> dict[str, object]:
        try:
            return sessions.get_session(session_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=f"Session not found: {session_id}") from exc

    def workspace_call(fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    def strip_code_fences(content: str) -> str:
        text = content.strip()
        if text.startswith("```") and text.endswith("```"):
            lines = text.splitlines()
            if len(lines) >= 3:
                return "\n".join(lines[1:-1]).strip()
        return text

    def parse_json_object(content: str) -> dict[str, object] | None:
        text = strip_code_fences(content)
        candidates = [text]
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidates.append(text[start : end + 1])
        for candidate in candidates:
            try:
                parsed = json.loads(candidate)
            except Exception:
                continue
            if isinstance(parsed, dict):
                return parsed
        return None

    def build_diff_hunks(original_content: str, proposed_content: str) -> list[dict[str, object]]:
        original_lines = original_content.splitlines()
        proposed_lines = proposed_content.splitlines()
        matcher = difflib.SequenceMatcher(a=original_lines, b=proposed_lines)
        hunks: list[dict[str, object]] = []
        for index, (tag, i1, i2, j1, j2) in enumerate(matcher.get_opcodes()):
            if tag == "equal":
                continue
            preview = "\n".join(
                difflib.unified_diff(
                    original_lines[i1:i2],
                    proposed_lines[j1:j2],
                    fromfile="before",
                    tofile="after",
                    lineterm="",
                )
            )
            hunks.append(
                {
                    "index": index,
                    "tag": tag,
                    "original_start": i1,
                    "original_end": i2,
                    "proposed_start": j1,
                    "proposed_end": j2,
                    "original_lines": original_lines[i1:i2],
                    "proposed_lines": proposed_lines[j1:j2],
                    "preview": preview,
                }
            )
        return hunks

    def make_edit_proposal(
        *,
        path: str,
        instruction: str,
        model: str,
        source_content: str,
        workspace_name: str | None,
    ) -> dict[str, object]:
        messages = [
            ChatMessage(
                role="system",
                content=(
                    "You are editing a local workspace file. "
                    "Return only the fully revised file content. "
                    "Do not explain, do not wrap in markdown fences, do not omit unchanged sections."
                ),
            ),
            ChatMessage(
                role="user",
                content=(
                    f"File path: {path}\n"
                    f"Workspace: {workspace_name or 'none'}\n"
                    f"Instruction: {instruction}\n\n"
                    f"Current file content:\n{source_content}"
                ),
            ),
        ]
        proposed_content = strip_code_fences(jarvis.complete(model, messages, temperature=0.1))
        diff = "\n".join(
            difflib.unified_diff(
                source_content.splitlines(),
                proposed_content.splitlines(),
                fromfile=f"a/{path}",
                tofile=f"b/{path}",
                lineterm="",
            )
        )
        hunks = build_diff_hunks(source_content, proposed_content)
        return {
            "path": path,
            "instruction": instruction,
            "original_content": source_content,
            "proposed_content": proposed_content,
            "diff": diff,
            "hunks": hunks,
        }

    def make_task_assist(
        *,
        instruction: str,
        model: str,
        path: str | None,
        content: str | None,
        workspace_name: str | None,
        terminal_output: str | None,
    ) -> dict[str, object]:
        task_messages = [
            ChatMessage(
                role="system",
                content=(
                    "You are helping inside a local coding workspace. "
                    "Return a JSON object with keys summary, suggested_command, edit_instruction. "
                    "summary must be short. suggested_command can be empty if not needed. "
                    "edit_instruction can be empty if no file edit is needed."
                ),
            ),
            ChatMessage(
                role="user",
                content=(
                    f"Instruction: {instruction}\n"
                    f"Workspace: {workspace_name or 'none'}\n"
                    f"Active file path: {path or 'none'}\n\n"
                    f"Active file content:\n{content or '[none]'}\n\n"
                    f"Recent terminal output:\n{terminal_output or '[none]'}"
                ),
            ),
        ]
        raw_response = jarvis.complete(model, task_messages, temperature=0.1)
        parsed = parse_json_object(raw_response) or {}
        summary = str(parsed.get("summary") or raw_response).strip()
        suggested_command = str(parsed.get("suggested_command") or "").strip()
        edit_instruction = str(parsed.get("edit_instruction") or instruction).strip()

        edit_proposal: dict[str, object] | None = None
        if path and content is not None and edit_instruction:
            edit_proposal = make_edit_proposal(
                path=path,
                instruction=edit_instruction,
                model=model,
                source_content=content,
                workspace_name=workspace_name,
            )

        return {
            "summary": summary,
            "suggested_command": suggested_command,
            "edit_instruction": edit_instruction,
            "edit_proposal": edit_proposal,
        }

    def make_batch_edit_proposal(
        *,
        instruction: str,
        model: str,
        files: list[dict[str, str]],
        workspace_name: str | None,
    ) -> dict[str, object]:
        messages = [
            ChatMessage(
                role="system",
                content=(
                    "You are editing multiple local workspace files. "
                    "Return a JSON object with keys summary and files. "
                    "files must be an array of objects with path and content. "
                    "Only include files that should change. "
                    "Each content value must contain the full revised file content."
                ),
            ),
            ChatMessage(
                role="user",
                content=json.dumps(
                    {
                        "workspace": workspace_name or "none",
                        "instruction": instruction,
                        "files": files,
                    },
                    ensure_ascii=False,
                ),
            ),
        ]
        raw_response = jarvis.complete(model, messages, temperature=0.1)
        parsed = parse_json_object(raw_response) or {}
        proposed_files = parsed.get("files")
        if not isinstance(proposed_files, list):
            proposed_files = []

        original_by_path = {file["path"]: file["content"] for file in files}
        proposals: list[dict[str, object]] = []
        for item in proposed_files:
            if not isinstance(item, dict):
                continue
            path = str(item.get("path") or "").strip()
            proposed_content = str(item.get("content") or "")
            original_content = original_by_path.get(path)
            if not path or original_content is None:
                continue
            diff = "\n".join(
                difflib.unified_diff(
                    original_content.splitlines(),
                    proposed_content.splitlines(),
                    fromfile=f"a/{path}",
                    tofile=f"b/{path}",
                    lineterm="",
                )
            )
            proposals.append(
                {
                    "path": path,
                    "original_content": original_content,
                    "proposed_content": proposed_content,
                    "diff": diff,
                    "hunks": build_diff_hunks(original_content, proposed_content),
                }
            )

        return {
            "summary": str(parsed.get("summary") or "").strip(),
            "proposals": proposals,
        }

    def resolve_workspace_content(path: str | None, content: str | None) -> tuple[str | None, str | None]:
        if path is None:
            return None, content
        if content is not None:
            return path, content
        file_payload = workspace_call(workspace.read_file, path)
        return path, str(file_payload["content"])

    def build_workspace_turn_message(task_assist: dict[str, object], *, path: str | None, queued_approvals: list[dict[str, object]]) -> str:
        lines: list[str] = []
        summary = str(task_assist.get("summary") or "").strip()
        if summary:
            lines.append(summary)
        if path:
            lines.append(f"Arquivo alvo: {path}")
        suggested_command = str(task_assist.get("suggested_command") or "").strip()
        if suggested_command:
            lines.append(f"Comando sugerido: {suggested_command}")
        if queued_approvals:
            approval_kinds = ", ".join(str(item.get("kind") or "acao") for item in queued_approvals)
            lines.append(f"Ações enfileiradas: {len(queued_approvals)} ({approval_kinds})")
        if task_assist.get("edit_proposal") and not queued_approvals:
            lines.append("Uma proposta de edição foi preparada para revisão.")
        if not lines:
            lines.append("Jarvis analisou o contexto operacional e não encontrou ações imediatas.")
        return "\n".join(lines)

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/v1")
    @router.get("/v1/")
    def openai_root() -> dict[str, object]:
        return {
            "object": "service",
            "service": "jarvis-openai-compatible",
            "status": "ok",
            "models_url": "/v1/models",
            "chat_completions_url": "/v1/chat/completions",
            "embeddings_url": "/v1/embeddings",
        }

    @router.get("/api/status")
    def status() -> dict[str, object]:
        service_status: dict[str, object] = {
            "core": {
                "status": "ok",
                "app_name": settings.app_name,
                "model_selection_strategy": settings.model_selection_strategy,
            },
        }
        try:
            service_status["ollama"] = ollama.health()
        except Exception as exc:
            service_status["ollama"] = {"status": "error", "detail": str(exc)}
        try:
            service_status["qdrant"] = knowledge.health()
        except Exception as exc:
            service_status["qdrant"] = {"status": "error", "detail": str(exc)}
        try:
            context = memory.resolve_context()
            service_status["memory"] = {
                "status": "ok",
                "identity_facts": len(context["identity"]),
                "state_facts": len(context["state"]),
                "hierarchical": memory.hierarchical_status(),
            }
        except Exception as exc:
            service_status["memory"] = {"status": "error", "detail": str(exc)}
        service_status["models"] = registry.get_rankings()
        return service_status

    @router.get("/v1/models")
    def list_models() -> dict[str, object]:
        return {"object": "list", "data": jarvis.list_models()}

    @router.post("/v1/chat/completions")
    def create_chat_completion(request: ChatCompletionRequest):
        created = int(time.time())
        if request.stream:
            def event_stream():
                response_id = f"chatcmpl-{uuid4().hex}"
                try:
                    for chunk_text in jarvis.complete_stream(request.model, request.messages, temperature=request.temperature):
                        chunk = {
                            "id": response_id,
                            "object": "chat.completion.chunk",
                            "created": created,
                            "model": request.model,
                            "choices": [
                                {
                                    "index": 0,
                                    "delta": {"content": chunk_text},
                                    "finish_reason": None,
                                }
                            ],
                        }
                        yield f"data: {json.dumps(chunk)}\n\n"
                    chunk = {
                        "id": response_id,
                        "object": "chat.completion.chunk",
                        "created": created,
                        "model": request.model,
                        "choices": [
                            {
                                "index": 0,
                                "delta": {},
                                "finish_reason": "stop",
                            }
                        ],
                    }
                    yield f"data: {json.dumps(chunk)}\n\n"
                    yield "data: [DONE]\n\n"
                except Exception as exc:
                    error_chunk = {
                        "id": response_id,
                        "object": "error",
                        "created": created,
                        "model": request.model,
                        "error": {"message": str(exc)},
                    }
                    yield f"data: {json.dumps(error_chunk)}\n\n"
                    yield "data: [DONE]\n\n"

            return StreamingResponse(event_stream(), media_type="text/event-stream")

        content = jarvis.complete(request.model, request.messages, temperature=request.temperature)
        response = {
            "id": f"chatcmpl-{uuid4().hex}",
            "object": "chat.completion",
            "created": created,
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
        }
        return response

    @router.post("/v1/embeddings")
    def create_embeddings(request: EmbeddingRequest):
        embeddings = ollama.embed(request.input, model=request.model)
        data = [
            {"object": "embedding", "index": index, "embedding": embedding}
            for index, embedding in enumerate(embeddings)
        ]
        return {"object": "list", "data": data, "model": request.model}

    @router.post("/api/memory/fact")
    def remember_fact(request: MemoryFactRequest):
        result = memory.apply(
            MemoryAction(
                action="set_identity_fact",
                field=f"{request.section}.{request.key}" if "." not in request.key else request.key,
                value=request.value,
                source=request.source or "api",
            )
        )
        return {"status": "ok", **result}

    @router.post("/api/memory/action")
    def apply_memory_action(request: MemoryAction):
        result = memory.apply(request)
        return {"status": "ok", **result}

    @router.post("/api/memory/state")
    def update_state(request: StateUpdateRequest):
        result = memory.apply(
            MemoryAction(
                action="update_state",
                field=request.field,
                value=request.value,
                source=request.source or "api",
            )
        )
        return {"status": "ok", **result}

    @router.post("/api/memory/timeline")
    def append_timeline(request: TimelineEntryRequest):
        result = memory.apply(
            MemoryAction(
                action="append_timeline_event",
                field="timeline.event",
                value=request.event,
                source="api",
                timestamp=request.happened_at.isoformat() if request.happened_at else None,
            )
        )
        return {"status": "ok", **result}

    @router.post("/api/memory/workspace")
    def append_workspace_memory(request: WorkspaceMemoryRequest):
        result = memory.apply(
            MemoryAction(
                action="append_workspace_note",
                field=request.field,
                value=request.value,
                workspace=request.workspace,
                source=request.source or "api",
            )
        )
        return {"status": "ok", **result}

    @router.post("/api/memory/summarize")
    def summarize_memory(request: SummarizeMemoryRequest):
        summary_path = memory.summarize_memory(label=request.label, scope=request.scope)
        archived = memory.archive_old_memory()
        return {"status": "ok", "summary_path": str(summary_path), "archived": [str(path) for path in archived]}

    @router.get("/api/memory/context")
    def get_context(workspace: str | None = None):
        return {
            "status": "ok",
            "context": memory.resolve_context(workspace=workspace),
            "hierarchical": memory.hierarchical_status(),
        }

    @router.post("/api/knowledge/index")
    def index_knowledge(request: KnowledgeIndexRequest):
        result = knowledge.index_domains(domains=request.domains, force=request.force)
        return {"status": "ok", **result}

    @router.post("/api/knowledge/ingest-note")
    def ingest_knowledge_note(request: KnowledgeIngestNoteRequest):
        result = knowledge.ingest_note(
            domain=request.domain,
            title=request.title,
            content=request.content,
            source_path=request.source_path,
            force=request.force,
        )
        return {"status": "ok", **result}

    @router.post("/api/knowledge/search")
    def search_knowledge(request: KnowledgeSearchRequest):
        results = knowledge.search(
            query=request.query,
            domain=request.domain,
            top_k=request.top_k,
            score_threshold=request.score_threshold,
        )
        return {"status": "ok", "results": [result.model_dump() for result in results]}

    @router.post("/api/benchmark/run")
    def run_benchmark(request: BenchmarkRequest):
        results = benchmarks.run(request.models)
        registry.save_benchmark(results)
        events.emit("benchmark_finished", {"models": request.models or [], "source": "api"})
        return {"status": "ok", "results": results}

    @router.get("/api/models/rankings")
    def get_model_rankings():
        return {"status": "ok", "rankings": registry.get_rankings()}

    @router.get("/api/workspace/tree")
    def get_workspace_tree(path: str | None = None):
        return {"status": "ok", "tree": workspace_call(workspace.list_tree, path)}

    @router.get("/api/workspace/file")
    def get_workspace_file(path: str):
        return {"status": "ok", **workspace_call(workspace.read_file, path)}

    @router.post("/api/workspace/file")
    def create_workspace_file(request: WorkspaceFileWriteRequest, session_id: str | None = None):
        result = workspace_call(workspace.write_file, request.path, request.content, create=True)
        if session_id:
            emit_session_event(session_id, "workspace_changed", {"path": request.path, "action": "create_file"}, source="workspace")
        return {"status": "ok", **result}

    @router.post("/api/workspace/directory")
    def create_workspace_directory(request: WorkspaceDirectoryCreateRequest, session_id: str | None = None):
        result = workspace_call(workspace.create_directory, request.path)
        if session_id:
            emit_session_event(session_id, "workspace_changed", {"path": request.path, "action": "create_directory"}, source="workspace")
        return {"status": "ok", **result}

    @router.put("/api/workspace/file")
    def update_workspace_file(request: WorkspaceFileWriteRequest, session_id: str | None = None):
        result = workspace_call(workspace.write_file, request.path, request.content, create=False)
        if session_id:
            emit_session_event(session_id, "workspace_changed", {"path": request.path, "action": "update_file"}, source="workspace")
        return {"status": "ok", **result}

    @router.post("/api/workspace/rename")
    def rename_workspace_path(request: WorkspaceRenameRequest, session_id: str | None = None):
        result = workspace_call(workspace.rename_path, request.source_path, request.target_path)
        if session_id:
            emit_session_event(session_id, "workspace_changed", {"path": request.target_path, "from_path": request.source_path, "action": "rename_path"}, source="workspace")
        return {"status": "ok", **result}

    @router.delete("/api/workspace/path")
    def delete_workspace_path(path: str, session_id: str | None = None):
        result = workspace_call(workspace.delete_path, path)
        if session_id:
            emit_session_event(session_id, "workspace_changed", {"path": path, "action": "delete_path"}, source="workspace")
        return {"status": "ok", **result}

    @router.get("/api/workspace/search")
    def search_workspace(q: str, limit: int = 30):
        return {"status": "ok", **workspace_call(workspace.search, q, limit=limit)}

    @router.post("/api/workspace/edit-proposal")
    def create_workspace_edit_proposal(request: WorkspaceEditAssistRequest):
        _, source_content = resolve_workspace_content(request.path, request.content)
        return {
            "status": "ok",
            **make_edit_proposal(
                path=request.path,
                instruction=request.instruction,
                model=request.model,
                source_content=source_content,
                workspace_name=request.workspace,
            ),
        }

    @router.post("/api/workspace/batch-edit-proposal")
    def create_workspace_batch_edit_proposal(request: WorkspaceBatchEditRequest):
        files = [{"path": file.path, "content": file.content} for file in request.files]
        return {
            "status": "ok",
            **make_batch_edit_proposal(
                instruction=request.instruction,
                model=request.model,
                files=files,
                workspace_name=request.workspace,
            ),
        }

    @router.post("/api/workspace/task-assist")
    def create_workspace_task_assist(request: WorkspaceTaskAssistRequest):
        path, content = resolve_workspace_content(request.path, request.content)
        return {
            "status": "ok",
            **make_task_assist(
                instruction=request.instruction,
                model=request.model,
                path=path,
                content=content,
                workspace_name=request.workspace,
                terminal_output=request.terminal_output,
            ),
        }

    @router.post("/api/workspace/task-cycle")
    def create_workspace_task_cycle(request: WorkspaceTaskAssistRequest):
        path, content = resolve_workspace_content(request.path, request.content)
        initial = make_task_assist(
            instruction=request.instruction,
            model=request.model,
            path=path,
            content=content,
            workspace_name=request.workspace,
            terminal_output=request.terminal_output,
        )

        command_result: dict[str, object] | None = None
        final = initial
        if request.execute_command and initial.get("suggested_command"):
            command_cwd = "."
            if path:
                parent = PurePosixPath(path).parent.as_posix()
                command_cwd = "." if parent in {"", "."} else parent
            command_result = workspace_call(terminal.run, str(initial["suggested_command"]), cwd=command_cwd)
            refreshed_content = content
            if path is not None:
                _, refreshed_content = resolve_workspace_content(path, None)
            combined_terminal_output = "\n".join(
                part for part in [request.terminal_output or "", str(command_result.get("output") or "")] if part
            )
            final = make_task_assist(
                instruction=request.instruction,
                model=request.model,
                path=path,
                content=refreshed_content,
                workspace_name=request.workspace,
                terminal_output=combined_terminal_output,
            )

        return {
            "status": "ok",
            "initial": initial,
            "command_result": command_result,
            "final": final,
        }

    @router.post("/api/terminal/run")
    def run_terminal_command(request: TerminalRunRequest, session_id: str | None = None):
        result = workspace_call(terminal.run, request.command, cwd=request.cwd)
        if session_id:
            emit_session_event(session_id, "command_executed", {"command": request.command, "cwd": request.cwd, "exit_code": result.get("exit_code")}, source="terminal")
        return {"status": "ok", "result": result}

    @router.post("/api/terminal/native")
    def open_native_terminal(request: TerminalNativeOpenRequest):
        return {"status": "ok", "result": workspace_call(terminal.open_native, cwd=request.cwd)}

    @router.get("/api/terminal/sessions")
    def list_terminal_sessions():
        return {"status": "ok", "sessions": terminal.list_sessions()}

    @router.post("/api/terminal/sessions")
    def create_terminal_session(request: TerminalSessionCreateRequest, session_id: str | None = None):
        created = workspace_call(terminal.create_session, cwd=request.cwd, cols=request.cols, rows=request.rows)
        if session_id:
            emit_session_event(session_id, "terminal_session_created", {"terminal_session_id": created.get("session_id"), "cwd": created.get("cwd")}, source="terminal")
        return {"status": "ok", "session": created}

    @router.get("/api/terminal/sessions/{session_id}/read")
    def read_terminal_session(session_id: str, wait_ms: int = 0):
        return {"status": "ok", "result": workspace_call(terminal.read, session_id, wait_ms=wait_ms)}

    @router.post("/api/terminal/sessions/{session_id}/write")
    def write_terminal_session(session_id: str, request: TerminalSessionWriteRequest, chat_session_id: str | None = None):
        result = workspace_call(terminal.write, session_id, request.data, wait_ms=request.wait_ms)
        if chat_session_id:
            emit_session_event(chat_session_id, "command_executed", {"terminal_session_id": session_id, "command": request.data.strip(), "exit_code": result.get("exit_code")}, source="terminal")
        return {"status": "ok", "result": result}

    @router.post("/api/terminal/sessions/{session_id}/resize")
    def resize_terminal_session(session_id: str, request: TerminalSessionResizeRequest):
        return {"status": "ok", "result": workspace_call(terminal.resize, session_id, request.cols, request.rows)}

    @router.post("/api/terminal/sessions/{session_id}/signal")
    def signal_terminal_session(session_id: str, request: TerminalSignalRequest):
        return {"status": "ok", "result": workspace_call(terminal.send_signal, session_id, request.signal)}

    @router.delete("/api/terminal/sessions/{session_id}")
    def close_terminal_session(session_id: str):
        workspace_call(terminal.close, session_id)
        return {"status": "ok"}

    @router.get("/api/chat/sessions")
    def list_chat_sessions():
        return {"status": "ok", "sessions": sessions.list_sessions()}

    @router.post("/api/chat/sessions")
    def create_chat_session(request: SessionCreateRequest):
        session = sessions.create_session(
            title=request.title,
            model=request.model,
            workspace=request.workspace,
            mission=request.mission.model_dump() if request.mission else None,
            ui_state=request.ui_state.model_dump() if request.ui_state else None,
            meta=request.meta.model_dump() if request.meta else None,
        )
        return {"status": "ok", "session": session}

    @router.get("/api/chat/sessions/{session_id}")
    def get_chat_session(session_id: str):
        return {"status": "ok", "session": require_session(session_id)}

    @router.get("/api/chat/sessions/{session_id}/note")
    def get_chat_session_note(session_id: str):
        require_session(session_id)
        note = sessions.get_session_note(session_id)
        return {"status": "ok", **note}

    @router.post("/api/chat/sessions/{session_id}/note/sync")
    def sync_chat_session_note(session_id: str, request: SessionNoteSyncRequest):
        session = require_session(session_id)
        note = sessions.get_session_note(session_id)
        workspace_name = (
            request.workspace
            or session.get("workspace")
            or ((session.get("mission") or {}).get("objective") and "jarvis")
            or "jarvis"
        )
        safe_title = (session.get("title") or f"session-{session_id}")[:80]
        sync_result: dict[str, object] = {
            "path": note["path"],
            "remembered": False,
            "indexed": False,
            "workspace": workspace_name,
        }
        if request.remember:
            field = f"session.{session_id[:12]}"
            memory.apply(
                MemoryAction(
                    action="append_workspace_note",
                    field=field,
                    value=f"Sessao: {safe_title}\nPath: {note['path']}\n\n{note['content'][:4000]}",
                    workspace=workspace_name,
                    source="api-session-note-sync",
                )
            )
            sync_result["remembered"] = True
            sync_result["memory_field"] = field
        if request.index:
            indexed = knowledge.ingest_note(
                domain=workspace_name,
                title=safe_title,
                content=note["content"],
                source_path=note["path"],
                force=request.force,
            )
            sync_result["indexed"] = True
            sync_result["knowledge"] = indexed
        emit_session_event(
            session_id,
            "session_note_synced",
            {"workspace": workspace_name, "remembered": sync_result["remembered"], "indexed": sync_result["indexed"]},
            source="api",
        )
        sessions.append_operation(
            session_id,
            kind="session_note_sync",
            title="Sincronizou nota da sessão",
            path=note["path"],
            detail=f"workspace {workspace_name} · memoria={sync_result['remembered']} · rag={sync_result['indexed']}",
        )
        return {"status": "ok", **sync_result, "session": sessions.get_session(session_id)}

    @router.put("/api/chat/sessions/{session_id}")
    def update_chat_session(session_id: str, request: SessionUpdateRequest):
        session = require_session(session_id)
        workspace_changed = False
        session_context_changed = False
        if "title" in request.model_fields_set:
            session["title"] = request.title
        if "model" in request.model_fields_set and request.model is not None:
            session["model"] = request.model
        if "workspace" in request.model_fields_set:
            session["workspace"] = request.workspace
            workspace_changed = True
        if "messages" in request.model_fields_set:
            session["messages"] = [message.model_dump() for message in (request.messages or [])]
        if "mission" in request.model_fields_set:
            session["mission"] = sessions._normalize_mission(request.mission.model_dump() if request.mission else None)
        if "ui_state" in request.model_fields_set:
            session["ui_state"] = sessions._normalize_ui_state(request.ui_state.model_dump() if request.ui_state else None)
            session_context_changed = True
        if "meta" in request.model_fields_set:
            session["meta"] = sessions._normalize_meta(request.meta.model_dump() if request.meta else None)
        updated = sessions.save_session(session_id, session)
        if workspace_changed:
            emit_session_event(session_id, "workspace_changed", {"workspace": request.workspace}, source="api")
        if session_context_changed:
            emit_session_event(
                session_id,
                "session_context_updated",
                {
                    "active_file": (updated.get("ui_state") or {}).get("active_file"),
                    "open_files": len((updated.get("ui_state") or {}).get("open_files") or []),
                },
                source="api",
            )
        return {"status": "ok", "session": sessions.get_session(session_id)}

    @router.delete("/api/chat/sessions/{session_id}")
    def delete_chat_session(session_id: str):
        require_session(session_id)
        sessions.delete_session(session_id)
        return {"status": "ok"}

    @router.post("/api/chat/sessions/{session_id}/tasks")
    def create_chat_session_task(session_id: str, request: SessionTaskCreateRequest):
        require_session(session_id)
        session, task = sessions.create_task(
            session_id,
            title=request.title,
            objective=request.objective,
            phase=request.phase,
            status=request.status,
            workspace=request.workspace,
            notes=request.notes,
        )
        emit_session_event(session_id, "task_created", {"task_id": task["id"], "phase": task["phase"], "status": task["status"]}, source="api")
        return {"status": "ok", "session": sessions.get_session(session_id), "task": task}

    @router.put("/api/chat/sessions/{session_id}/tasks/{task_id}")
    def update_chat_session_task(session_id: str, task_id: str, request: SessionTaskUpdateRequest):
        require_session(session_id)
        session, task = sessions.update_task(session_id, task_id, request.model_dump(exclude_none=True))
        emit_session_event(session_id, "task_updated", {"task_id": task["id"], "phase": task["phase"], "status": task["status"]}, source="api")
        if task.get("status") == "done":
            emit_session_event(session_id, "task_completed", {"task_id": task["id"], "phase": task["phase"], "status": task["status"]}, source="api")
        return {"status": "ok", "session": sessions.get_session(session_id), "task": task}

    @router.post("/api/chat/sessions/{session_id}/operations")
    def append_chat_session_operation(session_id: str, request: SessionOperationRequest):
        require_session(session_id)
        session = sessions.append_operation(
            session_id,
            kind=request.kind,
            title=request.title,
            path=request.path,
            command=request.command,
            detail=request.detail,
            metadata=request.metadata,
        )
        emit_session_event(session_id, "operation_logged", {"kind": request.kind, "title": request.title, "path": request.path, "command": request.command}, source="api")
        return {"status": "ok", "session": session}

    @router.post("/api/chat/sessions/{session_id}/checkpoints")
    def create_chat_session_checkpoint(session_id: str, request: SessionCheckpointCreateRequest):
        require_session(session_id)
        session, checkpoint = sessions.create_checkpoint(
            session_id,
            title=request.title,
            summary=request.summary,
            source="manual",
            trigger_event="manual",
        )
        session = sessions.append_operation(
            session_id,
            kind="checkpoint_create",
            title=f"Criou checkpoint {checkpoint.get('title') or checkpoint.get('id')}",
            path=checkpoint.get("active_file"),
            detail=checkpoint.get("summary"),
            metadata={"checkpoint_id": checkpoint.get("id")},
        )
        emit_session_event(session_id, "checkpoint_created", {"checkpoint_id": checkpoint.get("id"), "title": checkpoint.get("title")}, source="api")
        return {"status": "ok", "session": sessions.get_session(session_id), "checkpoint": checkpoint}

    @router.post("/api/chat/sessions/{session_id}/checkpoints/{checkpoint_id}/restore")
    def restore_chat_session_checkpoint(session_id: str, checkpoint_id: str):
        require_session(session_id)
        session, checkpoint = sessions.restore_checkpoint(session_id, checkpoint_id)
        session = sessions.append_operation(
            session_id,
            kind="checkpoint_restore",
            title=f"Restaurou checkpoint {checkpoint.get('title') or checkpoint.get('id')}",
            path=checkpoint.get("active_file"),
            detail=checkpoint.get("summary"),
            metadata={"checkpoint_id": checkpoint.get("id")},
        )
        emit_session_event(session_id, "checkpoint_restored", {"checkpoint_id": checkpoint.get("id"), "title": checkpoint.get("title")}, source="api")
        return {"status": "ok", "session": sessions.get_session(session_id), "checkpoint": checkpoint}

    @router.post("/api/chat/sessions/{session_id}/approvals")
    def append_chat_session_approval(session_id: str, request: SessionApprovalRequest):
        require_session(session_id)
        session = sessions.append_approval(
            session_id,
            kind=request.kind,
            title=request.title,
            path=request.path,
            command=request.command,
            detail=request.detail,
            metadata=request.metadata,
            payload=request.payload,
        )
        emit_session_event(session_id, "approval_created", {"kind": request.kind, "title": request.title, "path": request.path, "command": request.command}, source="api")
        return {"status": "ok", "session": session, "approval": session.get("approvals", [])[-1]}

    def execute_approval_action(session_id: str, approval_id: str, action: str) -> tuple[dict, dict, dict | None]:
        require_session(session_id)
        approval = sessions.get_approval(session_id, approval_id)

        if action == "reject":
            session, updated_approval = sessions.update_approval(session_id, approval_id, status="rejected")
            session = sessions.append_operation(
                session_id,
                kind="approval_rejected",
                title=f"Rejeitou ação {approval.get('title') or approval.get('kind') or approval_id}",
                path=approval.get("path"),
                command=approval.get("command"),
                detail=approval.get("detail"),
                metadata={"approval_id": approval_id, "kind": approval.get("kind")},
            )
            emit_session_event(session_id, "approval_rejected", {"approval_id": approval_id, "kind": approval.get("kind")}, source="api")
            return sessions.get_session(session_id), updated_approval, None

        result: dict[str, object] | None = None
        approval_kind = str(approval.get("kind") or "").strip()
        payload = approval.get("payload") or {}

        if approval_kind == "terminal_command":
            command = str(approval.get("command") or payload.get("command") or "").strip()
            if not command:
                raise HTTPException(status_code=400, detail="Approval command missing")
            result = workspace_call(terminal.run, command, cwd=payload.get("cwd"))
        elif approval_kind == "file_edit":
            target_path = str(approval.get("path") or payload.get("path") or "").strip()
            proposed_content = payload.get("proposed_content")
            if not target_path or not isinstance(proposed_content, str):
                raise HTTPException(status_code=400, detail="Approval file payload missing")
            result = workspace_call(workspace.write_file, target_path, proposed_content, False)
        elif approval_kind == "batch_edit":
            files = payload.get("files")
            if not isinstance(files, list) or not files:
                raise HTTPException(status_code=400, detail="Approval batch payload missing")
            applied = []
            for item in files:
                if not isinstance(item, dict):
                    continue
                target_path = str(item.get("path") or "").strip()
                proposed_content = item.get("proposed_content")
                if not target_path or not isinstance(proposed_content, str):
                    continue
                workspace_call(workspace.write_file, target_path, proposed_content, False)
                applied.append(target_path)
            result = {"applied_files": applied, "count": len(applied)}
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported approval kind: {approval_kind}")

        session, updated_approval = sessions.update_approval(session_id, approval_id, status="applied", result=result)
        session = sessions.append_operation(
            session_id,
            kind="approval_applied",
            title=f"Aplicou ação {approval.get('title') or approval_kind}",
            path=approval.get("path"),
            command=approval.get("command"),
            detail=approval.get("detail"),
            metadata={"approval_id": approval_id, "kind": approval_kind, "result": result},
        )
        emit_session_event(session_id, "approval_applied", {"approval_id": approval_id, "kind": approval_kind}, source="api")
        return sessions.get_session(session_id), updated_approval, result

    @router.post("/api/chat/sessions/{session_id}/approvals/batch")
    def apply_chat_session_approvals_batch(session_id: str, request: SessionApprovalBatchActionRequest):
        session = require_session(session_id)
        approvals = session.get("approvals", [])
        selected_ids = {item for item in (request.approval_ids or []) if item}
        target_ids: list[str] = []
        for approval in approvals:
            approval_id = str(approval.get("id") or "").strip()
            if not approval_id:
                continue
            if selected_ids and approval_id not in selected_ids:
                continue
            if request.pending_only and approval.get("status") != "pending":
                continue
            target_ids.append(approval_id)

        results: list[dict[str, object]] = []
        for approval_id in target_ids:
            _, updated_approval, result = execute_approval_action(session_id, approval_id, request.action)
            results.append({"approval": updated_approval, "result": result})

        return {
            "status": "ok",
            "session": sessions.get_session(session_id),
            "action": request.action,
            "count": len(results),
            "results": results,
        }

    @router.post("/api/chat/sessions/{session_id}/approvals/{approval_id}")
    def apply_chat_session_approval(session_id: str, approval_id: str, request: SessionApprovalActionRequest):
        session, updated_approval, result = execute_approval_action(session_id, approval_id, request.action)
        return {"status": "ok", "session": session, "approval": updated_approval, "result": result}

    def execute_workspace_turn(session_id: str, request: SessionWorkspaceTurnRequest) -> dict[str, object]:
        session = require_session(session_id)
        user_content = request.content
        if request.workspace:
            user_content = f"[WORKSPACE: {request.workspace}]\n{user_content}"
        existing_messages = session.get("messages", [])
        messages = [ChatMessage.model_validate(message) for message in existing_messages]
        messages.append(ChatMessage(role="user", content=user_content))
        assistant_metadata = jarvis.describe_request(request.model, messages)

        path, content = resolve_workspace_content(request.path, request.file_content)
        task_assist = make_task_assist(
            instruction=user_content,
            model=request.model,
            path=path,
            content=content,
            workspace_name=request.workspace,
            terminal_output=request.terminal_output,
        )

        queued_approvals: list[dict[str, object]] = []
        if request.queue_edit and isinstance(task_assist.get("edit_proposal"), dict) and path:
            approval_session = sessions.append_approval(
                session_id,
                kind="file_edit",
                title=f"Diff proposto para {path}",
                path=path,
                detail=str(task_assist.get("edit_instruction") or task_assist.get("summary") or "Aplicar edição proposta"),
                payload={
                    "path": path,
                    "proposed_content": task_assist["edit_proposal"].get("proposed_content"),
                    "diff": task_assist["edit_proposal"].get("diff"),
                    "instruction": task_assist.get("edit_instruction"),
                },
            )
            approval = dict((approval_session.get("approvals") or [])[-1])
            queued_approvals.append(approval)
            emit_session_event(session_id, "approval_created", {"kind": approval.get("kind"), "title": approval.get("title"), "path": approval.get("path")}, source="workspace_turn")

        suggested_command = str(task_assist.get("suggested_command") or "").strip()
        if request.queue_command and suggested_command:
            command_cwd = "."
            if path:
                parent = PurePosixPath(path).parent.as_posix()
                command_cwd = "." if parent in {"", "."} else parent
            approval_session = sessions.append_approval(
                session_id,
                kind="terminal_command",
                title="Comando sugerido pelo Jarvis",
                path=path,
                command=suggested_command,
                detail=str(task_assist.get("summary") or "Comando operacional sugerido"),
                payload={"command": suggested_command, "cwd": command_cwd},
            )
            approval = dict((approval_session.get("approvals") or [])[-1])
            queued_approvals.append(approval)
            emit_session_event(session_id, "approval_created", {"kind": approval.get("kind"), "title": approval.get("title"), "command": approval.get("command")}, source="workspace_turn")

        assistant_content = build_workspace_turn_message(task_assist, path=path, queued_approvals=queued_approvals)
        assistant_metadata = {
            **assistant_metadata,
            "workspace_turn": True,
            "target_path": path,
            "queued_approvals": len(queued_approvals),
            "suggested_command": suggested_command or None,
        }
        turn_snapshot = {
            "workspace": request.workspace,
            "mission": session.get("mission") or None,
            "ui_state": {
                **(session.get("ui_state") or {}),
                "active_file": path,
                "pending_attachments": [attachment.model_dump() for attachment in (request.attachments or [])],
                "pending_edit_proposal": task_assist.get("edit_proposal"),
                "pending_task_assist": task_assist,
                "terminal_tail": request.terminal_output,
                "workbench_mode": "review" if queued_approvals else "build",
            },
        }
        sessions.append_exchange(
            session_id,
            user_content=user_content,
            user_display_content=request.display_content,
            assistant_content=assistant_content,
            model=request.model,
            workspace=request.workspace,
            assistant_metadata=assistant_metadata,
            user_attachments=[attachment.model_dump() for attachment in (request.attachments or [])],
        )
        sessions.append_operation(
            session_id,
            kind="workspace_turn",
            title="Executou turno operacional do Jarvis",
            path=path,
            command=suggested_command or None,
            detail=str(task_assist.get("summary") or request.content)[:240],
            metadata={"queued_approvals": len(queued_approvals), "workspace_turn": True},
        )
        updated_session, turn = sessions.append_turn(
            session_id,
            kind="workspace_turn",
            title="Turno operacional do Jarvis",
            summary=str(task_assist.get("summary") or "")[:4000] or None,
            path=path,
            workspace=request.workspace,
            model=request.model,
            user_prompt=request.display_content or request.content,
            suggested_command=suggested_command or None,
            edit_instruction=str(task_assist.get("edit_instruction") or "")[:4000] or None,
            approvals=queued_approvals,
            task_assist=task_assist,
            snapshot=turn_snapshot,
            metadata=assistant_metadata,
        )
        memory.record_exchange(
            user_content=user_content,
            user_display_content=request.display_content,
            assistant_content=assistant_content,
            model=request.model,
            workspace=request.workspace,
        )
        emit_session_event(session_id, "workspace_turn_created", {"workspace": request.workspace, "path": path, "queued_approvals": len(queued_approvals), "turn_id": turn.get("id")}, source="workspace_turn")
        emit_session_event(session_id, "memory_updated", {"workspace": request.workspace, "model": request.model}, source="memory")
        return {
            "status": "ok",
            "session": sessions.get_session(session_id),
            "message": assistant_content,
            "task_assist": task_assist,
            "approvals": queued_approvals,
            "turn": turn,
            "assistant_metadata": assistant_metadata,
            "target_path": path,
        }

    @router.post("/api/chat/sessions/{session_id}/workspace-turn")
    def create_chat_session_workspace_turn(session_id: str, request: SessionWorkspaceTurnRequest):
        return execute_workspace_turn(session_id, request)

    @router.post("/api/chat/sessions/{session_id}/workspace-turn/stream")
    def create_chat_session_workspace_turn_stream(session_id: str, request: SessionWorkspaceTurnRequest):
        def chunk_text(text: str, size: int = 160):
            for index in range(0, len(text), size):
                yield text[index:index + size]

        def event_stream():
            try:
                session = require_session(session_id)
                user_content = request.content
                if request.workspace:
                    user_content = f"[WORKSPACE: {request.workspace}]\n{user_content}"
                existing_messages = session.get("messages", [])
                messages = [ChatMessage.model_validate(message) for message in existing_messages]
                messages.append(ChatMessage(role="user", content=user_content))
                assistant_metadata = jarvis.describe_request(request.model, messages)
                start_payload = {"type": "start", "session_id": session_id, "model": request.model, "assistant_metadata": assistant_metadata}
                yield f"data: {json.dumps(start_payload)}\n\n"
                yield f"data: {json.dumps({'type': 'phase', 'phase': 'analyzing', 'label': 'Jarvis analisando workspace, arquivo ativo e terminal'})}\n\n"
                payload = execute_workspace_turn(session_id, request)
                phase_payload = {
                    "type": "phase",
                    "phase": "planning",
                    "label": "Plano operacional pronto",
                    "summary": payload["task_assist"].get("summary"),
                    "queued_approvals": len(payload["approvals"]),
                }
                yield f"data: {json.dumps(phase_payload)}\n\n"
                for chunk in chunk_text(str(payload["message"] or "")):
                    yield f"data: {json.dumps({'type': 'chunk', 'delta': chunk})}\n\n"
                yield f"data: {json.dumps({'type': 'done', **payload})}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as exc:
                yield f"data: {json.dumps({'type': 'error', 'detail': str(exc)})}\n\n"
                yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    @router.post("/api/chat/sessions/{session_id}/turns/{turn_id}/restore")
    def restore_chat_session_turn(session_id: str, turn_id: str):
        require_session(session_id)
        session, turn = sessions.restore_turn(session_id, turn_id)
        session = sessions.append_operation(
            session_id,
            kind="turn_restore",
            title=f"Restaurou turno {turn.get('title') or turn.get('id')}",
            path=turn.get("path"),
            command=turn.get("suggested_command"),
            detail=turn.get("summary"),
            metadata={"turn_id": turn.get("id")},
        )
        emit_session_event(session_id, "workspace_turn_restored", {"turn_id": turn.get("id"), "path": turn.get("path")}, source="api")
        return {"status": "ok", "session": sessions.get_session(session_id), "turn": turn}

    @router.post("/api/chat/sessions/{session_id}/message")
    def create_chat_session_message(session_id: str, request: SessionMessageRequest):
        session = require_session(session_id)
        user_content = request.content
        if request.workspace:
            user_content = f"[WORKSPACE: {request.workspace}]\n{user_content}"
        existing_messages = session.get("messages", [])
        messages = [ChatMessage.model_validate(message) for message in existing_messages]
        messages.append(ChatMessage(role="user", content=user_content))
        assistant_metadata = jarvis.describe_request(request.model, messages)
        content = jarvis.complete(request.model, messages, temperature=request.temperature)
        updated = sessions.append_exchange(
            session_id,
            user_content=user_content,
            user_display_content=request.display_content,
            assistant_content=content,
            model=request.model,
            workspace=request.workspace,
            assistant_metadata=assistant_metadata,
            user_attachments=[attachment.model_dump() for attachment in (request.attachments or [])],
        )
        memory.record_exchange(
            user_content=user_content,
            user_display_content=request.display_content,
            assistant_content=content,
            model=request.model,
            workspace=request.workspace,
        )
        emit_session_event(session_id, "memory_updated", {"workspace": request.workspace, "model": request.model}, source="memory")
        return {"status": "ok", "session": updated, "message": content}

    @router.post("/api/chat/sessions/{session_id}/message/stream")
    def create_chat_session_message_stream(session_id: str, request: SessionMessageRequest):
        session = require_session(session_id)
        user_content = request.content
        if request.workspace:
            user_content = f"[WORKSPACE: {request.workspace}]\n{user_content}"
        existing_messages = session.get("messages", [])
        messages = [ChatMessage.model_validate(message) for message in existing_messages]
        messages.append(ChatMessage(role="user", content=user_content))

        assistant_metadata = jarvis.describe_request(request.model, messages)

        def event_stream():
            assistant_parts: list[str] = []
            try:
                start_payload = {"type": "start", "session_id": session_id, "model": request.model, "assistant_metadata": assistant_metadata}
                yield f"data: {json.dumps(start_payload)}\n\n"
                for chunk in jarvis.complete_stream(request.model, messages, temperature=request.temperature):
                    assistant_parts.append(chunk)
                    payload = {"type": "chunk", "delta": chunk}
                    yield f"data: {json.dumps(payload)}\n\n"
                assistant_content = "".join(assistant_parts)
                updated = sessions.append_exchange(
                    session_id,
                    user_content=user_content,
                    user_display_content=request.display_content,
                    assistant_content=assistant_content,
                    model=request.model,
                    workspace=request.workspace,
                    assistant_metadata=assistant_metadata,
                    user_attachments=[attachment.model_dump() for attachment in (request.attachments or [])],
                )
                memory.record_exchange(
                    user_content=user_content,
                    user_display_content=request.display_content,
                    assistant_content=assistant_content,
                    model=request.model,
                    workspace=request.workspace,
                )
                emit_session_event(session_id, "memory_updated", {"workspace": request.workspace, "model": request.model}, source="memory")
                done_payload = {"type": "done", "session": updated, "message": assistant_content}
                yield f"data: {json.dumps(done_payload)}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as exc:
                error_payload = {"type": "error", "detail": str(exc)}
                yield f"data: {json.dumps(error_payload)}\n\n"
                yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    return router
