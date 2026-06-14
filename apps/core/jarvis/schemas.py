from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    stream: bool = False
    temperature: float | None = None
    max_tokens: int | None = None


class EmbeddingRequest(BaseModel):
    model: str | None = None
    input: str | list[str]


class MemoryFactRequest(BaseModel):
    section: str = Field(description="Logical namespace, e.g. profile, preferences, goals or constraints.")
    key: str
    value: Any
    source: str | None = None


class StateUpdateRequest(BaseModel):
    field: str
    value: Any
    source: str | None = None


class WorkspaceMemoryRequest(BaseModel):
    workspace: str
    field: str
    value: Any
    source: str | None = None


class TimelineEntryRequest(BaseModel):
    event: str
    happened_at: datetime | None = None


class SummarizeMemoryRequest(BaseModel):
    scope: Literal["current", "all"] = "current"
    label: str | None = None


class KnowledgeIndexRequest(BaseModel):
    domains: list[str] | None = None
    force: bool = False


class KnowledgeIngestNoteRequest(BaseModel):
    domain: str
    title: str
    content: str
    source_path: str | None = None
    force: bool = False


class KnowledgeSearchRequest(BaseModel):
    query: str
    domain: str | None = None
    top_k: int = 5
    score_threshold: float | None = None


class SearchResult(BaseModel):
    score: float
    text: str
    metadata: dict[str, Any]


class BenchmarkRequest(BaseModel):
    models: list[str] | None = None


class SessionMissionRequest(BaseModel):
    objective: str | None = None
    status: str | None = None
    next_steps: list[str] = Field(default_factory=list)


class SessionUiStateRequest(BaseModel):
    active_file: str | None = None
    open_files: list[str] = Field(default_factory=list)
    quick_flow_mode: str | None = None
    quick_target_path: str | None = None
    quick_goal: str | None = None
    draft_prompt: str | None = None
    editor_instruction: str | None = None
    terminal_command: str | None = None
    workbench_mode: str | None = None
    terminal_tail: str | None = None
    pending_attachments: list[SessionAttachmentRequest] = Field(default_factory=list)
    pending_edit_proposal: dict[str, Any] | None = None
    pending_batch_proposal: dict[str, Any] | None = None
    pending_task_assist: dict[str, Any] | None = None


class SessionMetaRequest(BaseModel):
    pinned: bool | None = None
    archived: bool | None = None


class SessionTaskCreateRequest(BaseModel):
    title: str
    objective: str | None = None
    phase: Literal["planner", "executor", "verifier", "memory"] = "planner"
    status: Literal["todo", "in_progress", "done", "blocked"] = "todo"
    workspace: str | None = None
    notes: str | None = None


class SessionTaskUpdateRequest(BaseModel):
    title: str | None = None
    objective: str | None = None
    phase: Literal["planner", "executor", "verifier", "memory"] | None = None
    status: Literal["todo", "in_progress", "done", "blocked"] | None = None
    workspace: str | None = None
    notes: str | None = None


class SessionCreateRequest(BaseModel):
    title: str | None = None
    model: str = "jarvis-safe"
    workspace: str | None = None
    mission: SessionMissionRequest | None = None
    ui_state: SessionUiStateRequest | None = None
    meta: SessionMetaRequest | None = None


class SessionUpdateRequest(BaseModel):
    title: str | None = None
    model: str | None = None
    workspace: str | None = None
    messages: list[ChatMessage] | None = None
    mission: SessionMissionRequest | None = None
    ui_state: SessionUiStateRequest | None = None
    meta: SessionMetaRequest | None = None


class SessionAttachmentRequest(BaseModel):
    id: str | None = None
    name: str
    content: str
    size: int | None = None


class SessionMessageRequest(BaseModel):
    model: str
    content: str
    display_content: str | None = None
    workspace: str | None = None
    temperature: float | None = None
    attachments: list[SessionAttachmentRequest] | None = None


class SessionWorkspaceTurnRequest(BaseModel):
    model: str
    content: str
    display_content: str | None = None
    workspace: str | None = None
    path: str | None = None
    file_content: str | None = None
    terminal_output: str | None = None
    queue_command: bool = True
    queue_edit: bool = True
    attachments: list[SessionAttachmentRequest] | None = None


class SessionOperationRequest(BaseModel):
    kind: str
    title: str
    path: str | None = None
    command: str | None = None
    detail: str | None = None
    metadata: dict[str, Any] | None = None


class SessionCheckpointCreateRequest(BaseModel):
    title: str | None = None
    summary: str | None = None


class SessionApprovalRequest(BaseModel):
    kind: str
    title: str
    path: str | None = None
    command: str | None = None
    detail: str | None = None
    metadata: dict[str, Any] | None = None
    payload: dict[str, Any] | None = None


class SessionApprovalActionRequest(BaseModel):
    action: Literal["apply", "reject"] = "apply"


class SessionApprovalBatchActionRequest(BaseModel):
    action: Literal["apply", "reject"] = "apply"
    approval_ids: list[str] | None = None
    pending_only: bool = True


class SessionNoteSyncRequest(BaseModel):
    workspace: str | None = None
    remember: bool = True
    index: bool = True
    force: bool = True


class WorkspaceFileRequest(BaseModel):
    path: str


class WorkspaceFileWriteRequest(BaseModel):
    path: str
    content: str = ""


class WorkspaceFileSnapshot(BaseModel):
    path: str
    content: str


class WorkspaceDirectoryCreateRequest(BaseModel):
    path: str


class WorkspaceRenameRequest(BaseModel):
    source_path: str
    target_path: str


class WorkspaceEditAssistRequest(BaseModel):
    path: str
    instruction: str
    model: str = "jarvis-programador-safe"
    content: str | None = None
    workspace: str | None = None


class WorkspaceTaskAssistRequest(BaseModel):
    instruction: str
    model: str = "jarvis-programador-safe"
    path: str | None = None
    content: str | None = None
    workspace: str | None = None
    terminal_output: str | None = None
    execute_command: bool = False


class WorkspaceBatchEditRequest(BaseModel):
    instruction: str
    model: str = "jarvis-programador-safe"
    files: list[WorkspaceFileSnapshot]
    workspace: str | None = None


class WorkspaceTreeRequest(BaseModel):
    path: str | None = None


class TerminalRunRequest(BaseModel):
    command: str
    cwd: str | None = None


class TerminalNativeOpenRequest(BaseModel):
    cwd: str | None = None


class TerminalSessionCreateRequest(BaseModel):
    cwd: str | None = None
    cols: int = 120
    rows: int = 32


class TerminalSessionWriteRequest(BaseModel):
    data: str
    wait_ms: int = 120


class TerminalSessionResizeRequest(BaseModel):
    cols: int = 120
    rows: int = 32


class TerminalSignalRequest(BaseModel):
    signal: Literal["int", "term", "kill"] = "int"
