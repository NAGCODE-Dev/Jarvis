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


class SessionCreateRequest(BaseModel):
    title: str | None = None
    model: str = "jarvis-safe"
    workspace: str | None = None


class SessionUpdateRequest(BaseModel):
    title: str | None = None
    model: str | None = None
    workspace: str | None = None
    messages: list[ChatMessage] | None = None


class SessionMessageRequest(BaseModel):
    model: str
    content: str
    display_content: str | None = None
    workspace: str | None = None
    temperature: float | None = None


class SessionOperationRequest(BaseModel):
    kind: str
    title: str
    path: str | None = None
    command: str | None = None
    detail: str | None = None
    metadata: dict[str, Any] | None = None


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
