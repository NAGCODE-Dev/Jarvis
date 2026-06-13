from __future__ import annotations

import difflib
import json
import time
from pathlib import PurePosixPath
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from jarvis.benchmark import BenchmarkService
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
    SessionApprovalRequest,
    SessionCreateRequest,
    SessionMessageRequest,
    SessionOperationRequest,
    SessionUpdateRequest,
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
    def create_workspace_file(request: WorkspaceFileWriteRequest):
        return {"status": "ok", **workspace_call(workspace.write_file, request.path, request.content, create=True)}

    @router.post("/api/workspace/directory")
    def create_workspace_directory(request: WorkspaceDirectoryCreateRequest):
        return {"status": "ok", **workspace_call(workspace.create_directory, request.path)}

    @router.put("/api/workspace/file")
    def update_workspace_file(request: WorkspaceFileWriteRequest):
        return {"status": "ok", **workspace_call(workspace.write_file, request.path, request.content, create=False)}

    @router.post("/api/workspace/rename")
    def rename_workspace_path(request: WorkspaceRenameRequest):
        return {"status": "ok", **workspace_call(workspace.rename_path, request.source_path, request.target_path)}

    @router.delete("/api/workspace/path")
    def delete_workspace_path(path: str):
        return {"status": "ok", **workspace_call(workspace.delete_path, path)}

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
    def run_terminal_command(request: TerminalRunRequest):
        return {"status": "ok", "result": workspace_call(terminal.run, request.command, cwd=request.cwd)}

    @router.get("/api/terminal/sessions")
    def list_terminal_sessions():
        return {"status": "ok", "sessions": terminal.list_sessions()}

    @router.post("/api/terminal/sessions")
    def create_terminal_session(request: TerminalSessionCreateRequest):
        return {"status": "ok", "session": workspace_call(terminal.create_session, cwd=request.cwd, cols=request.cols, rows=request.rows)}

    @router.get("/api/terminal/sessions/{session_id}/read")
    def read_terminal_session(session_id: str, wait_ms: int = 0):
        return {"status": "ok", "result": workspace_call(terminal.read, session_id, wait_ms=wait_ms)}

    @router.post("/api/terminal/sessions/{session_id}/write")
    def write_terminal_session(session_id: str, request: TerminalSessionWriteRequest):
        return {"status": "ok", "result": workspace_call(terminal.write, session_id, request.data, wait_ms=request.wait_ms)}

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
        session = sessions.create_session(title=request.title, model=request.model, workspace=request.workspace)
        return {"status": "ok", "session": session}

    @router.get("/api/chat/sessions/{session_id}")
    def get_chat_session(session_id: str):
        return {"status": "ok", "session": require_session(session_id)}

    @router.put("/api/chat/sessions/{session_id}")
    def update_chat_session(session_id: str, request: SessionUpdateRequest):
        session = require_session(session_id)
        if "title" in request.model_fields_set:
            session["title"] = request.title
        if "model" in request.model_fields_set and request.model is not None:
            session["model"] = request.model
        if "workspace" in request.model_fields_set:
            session["workspace"] = request.workspace
        if "messages" in request.model_fields_set:
            session["messages"] = [message.model_dump() for message in (request.messages or [])]
        return {"status": "ok", "session": sessions.save_session(session_id, session)}

    @router.delete("/api/chat/sessions/{session_id}")
    def delete_chat_session(session_id: str):
        require_session(session_id)
        sessions.delete_session(session_id)
        return {"status": "ok"}

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
        return {"status": "ok", "session": session}

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
        return {"status": "ok", "session": session, "approval": session.get("approvals", [])[-1]}

    @router.post("/api/chat/sessions/{session_id}/approvals/{approval_id}")
    def apply_chat_session_approval(session_id: str, approval_id: str, request: SessionApprovalActionRequest):
        require_session(session_id)
        approval = sessions.get_approval(session_id, approval_id)

        if request.action == "reject":
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
            return {"status": "ok", "session": session, "approval": updated_approval, "result": None}

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
        return {"status": "ok", "session": session, "approval": updated_approval, "result": result}

    @router.post("/api/chat/sessions/{session_id}/message")
    def create_chat_session_message(session_id: str, request: SessionMessageRequest):
        session = require_session(session_id)
        user_content = request.content
        if request.workspace:
            user_content = f"[WORKSPACE: {request.workspace}]\n{user_content}"
        existing_messages = session.get("messages", [])
        messages = [ChatMessage.model_validate(message) for message in existing_messages]
        messages.append(ChatMessage(role="user", content=user_content))
        content = jarvis.complete(request.model, messages, temperature=request.temperature)
        updated = sessions.append_exchange(
            session_id,
            user_content=user_content,
            user_display_content=request.display_content,
            assistant_content=content,
            model=request.model,
            workspace=request.workspace,
        )
        memory.record_exchange(
            user_content=user_content,
            user_display_content=request.display_content,
            assistant_content=content,
            model=request.model,
            workspace=request.workspace,
        )
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

        def event_stream():
            assistant_parts: list[str] = []
            try:
                start_payload = {"type": "start", "session_id": session_id, "model": request.model}
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
                )
                memory.record_exchange(
                    user_content=user_content,
                    user_display_content=request.display_content,
                    assistant_content=assistant_content,
                    model=request.model,
                    workspace=request.workspace,
                )
                done_payload = {"type": "done", "session": updated, "message": assistant_content}
                yield f"data: {json.dumps(done_payload)}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as exc:
                error_payload = {"type": "error", "detail": str(exc)}
                yield f"data: {json.dumps(error_payload)}\n\n"
                yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    return router
