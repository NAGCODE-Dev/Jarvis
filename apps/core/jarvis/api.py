from __future__ import annotations

import json
import time
from uuid import uuid4

from fastapi import APIRouter
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
    ChatCompletionRequest,
    EmbeddingRequest,
    KnowledgeIndexRequest,
    KnowledgeSearchRequest,
    MemoryFactRequest,
    StateUpdateRequest,
    SummarizeMemoryRequest,
    TimelineEntryRequest,
    WorkspaceMemoryRequest,
)


def create_api_router(ollama: OllamaClient, memory: MemoryService, knowledge: KnowledgeService) -> APIRouter:
    router = APIRouter()
    jarvis = JarvisRouter(ollama=ollama, memory=memory, knowledge=knowledge)
    benchmarks = BenchmarkService(ollama=ollama)
    registry = ModelRegistry()

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

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
            }
        except Exception as exc:
            service_status["memory"] = {"status": "error", "detail": str(exc)}
        service_status["models"] = registry.get_rankings()
        return service_status

    @router.get("/v1/models")
    def list_models() -> dict[str, list[dict[str, str]]]:
        return {"data": jarvis.list_models()}

    @router.post("/v1/chat/completions")
    def create_chat_completion(request: ChatCompletionRequest):
        content = jarvis.complete(request.model, request.messages, temperature=request.temperature)
        created = int(time.time())
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
        if not request.stream:
            return response

        def event_stream():
            chunk = {
                "id": response["id"],
                "object": "chat.completion.chunk",
                "created": created,
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {"role": "assistant", "content": content},
                        "finish_reason": "stop",
                    }
                ],
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

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
        return {"status": "ok", "context": memory.resolve_context(workspace=workspace)}

    @router.post("/api/knowledge/index")
    def index_knowledge(request: KnowledgeIndexRequest):
        result = knowledge.index_domains(domains=request.domains, force=request.force)
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

    return router
