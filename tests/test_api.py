from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from jarvis.api import create_api_router
from jarvis.memory import MemoryAction, MemoryManager
from jarvis.router import JarvisRouter
from jarvis.schemas import ChatMessage
from jarvis.sessions import SessionStore


class FakeOllama:
    def health(self):
        return {"status": "ok", "models": ["qwen3:4b"]}

    def list_models(self):
        return {"models": [{"name": "qwen3:4b"}, {"name": "gemma4:e2b"}]}

    def embed(self, text, model=None):
        if isinstance(text, list):
            return [[0.1, 0.2] for _ in text]
        return [[0.1, 0.2]]

    def chat(self, model, messages, temperature=None):
        return "ok"

    def chat_stream(self, model, messages, temperature=None):
        yield "o"
        yield "k"


class FakeKnowledge:
    def health(self):
        return {"status": "ok", "collections": 1}

    def search(self, query, top_k=4, domain=None, score_threshold=None):
        return []

    def index_domains(self, domains=None, force=False):
        return {"indexed_files": 0, "indexed_chunks": 0}

    def ingest_note(self, *, domain, title, content, source_path=None, force=False):
        return {
            "stored_path": f"knowledge/{domain}/obsidian/{title}.md",
            "indexed_chunks": 1,
            "domain": domain,
        }


def test_router_exposes_models_and_streams(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module
    import jarvis.sessions as sessions_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)

    memory = MemoryManager()
    router = JarvisRouter(FakeOllama(), memory, FakeKnowledge())

    models = router.list_models()
    assert any(model["id"] == "jarvis-programador" for model in models)
    assert any(model["id"] == "jarvis-programador-safe" for model in models)

    chunks = list(router.complete_stream("jarvis-safe", [ChatMessage(role="user", content="oi")]))
    assert "".join(chunks) == "ok"


def test_memory_and_workspace_context(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)
    monkeypatch.setattr(registry_module, "settings", test_settings)

    memory = MemoryManager()
    memory.apply(MemoryAction(action="update_state", field="weight.current_kg", value=72, source="test"))
    memory.apply(MemoryAction(action="append_workspace_note", field="topic", value="context selection", source="test", workspace="jarvis"))

    context = memory.resolve_context(workspace="jarvis")
    assert context["state"]["weight.current_kg"] == 72
    assert context["workspace"]["name"] == "jarvis"
    assert context["workspace"]["facts"]["topic"] == "context selection"


def test_session_store_persists_messages_and_metadata(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.sessions as sessions_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)

    store = SessionStore()
    session = store.create_session(model="jarvis-safe", workspace="jarvis")
    updated = store.append_exchange(
        session["id"],
        user_content="oi",
        user_display_content="Oi limpo",
        assistant_content="ok",
        model="jarvis-safe",
        workspace="jarvis",
    )

    assert updated["messages"][0]["display_content"] == "Oi limpo"
    assert updated["messages"][1]["content"] == "ok"
    assert updated["workspace"] == "jarvis"
    assert updated["title"] == "Oi limpo"
    assert Path(test_settings.sessions_dir / f"{session['id']}.json").exists()


def test_session_store_ignores_workspace_prefix_in_generated_title(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.sessions as sessions_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)

    store = SessionStore()
    session = store.create_session(model="jarvis-safe", workspace="jarvis")
    updated = store.append_exchange(
        session["id"],
        user_content="[WORKSPACE: jarvis]\nResponda ao projeto atual",
        user_display_content=None,
        assistant_content="ok",
        model="jarvis-safe",
        workspace="jarvis",
    )

    assert updated["title"] == "Responda ao projeto atual"


def test_api_updates_can_clear_workspace_and_missing_session_returns_404(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module
    import jarvis.sessions as sessions_module
    from fastapi import FastAPI

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)

    app = FastAPI()
    app.include_router(create_api_router(ollama=FakeOllama(), memory=MemoryManager(), knowledge=FakeKnowledge()))
    client = TestClient(app)

    created = client.post("/api/chat/sessions", json={"model": "jarvis-safe", "workspace": "jarvis"})
    assert created.status_code == 200
    session_id = created.json()["session"]["id"]

    cleared = client.put(f"/api/chat/sessions/{session_id}", json={"workspace": None})
    assert cleared.status_code == 200
    assert cleared.json()["session"]["workspace"] is None

    missing = client.get("/api/chat/sessions/does-not-exist")
    assert missing.status_code == 404


def test_api_session_message_updates_hierarchical_memory(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module
    import jarvis.sessions as sessions_module
    from fastapi import FastAPI

    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        semantic_memory_enabled=False,
    )
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)
    monkeypatch.setattr(sessions_module, "settings", test_settings)

    memory = MemoryManager()
    app = FastAPI()
    app.include_router(create_api_router(ollama=FakeOllama(), memory=memory, knowledge=FakeKnowledge()))
    client = TestClient(app)

    created = client.post("/api/chat/sessions", json={"model": "jarvis-safe", "workspace": "jarvis"})
    session_id = created.json()["session"]["id"]

    response = client.post(
        f"/api/chat/sessions/{session_id}/message",
        json={"model": "jarvis-safe", "content": "continuar o projeto jarvis", "display_content": "Continuar o projeto Jarvis", "workspace": "jarvis"},
    )

    assert response.status_code == 200
    payload = test_settings.current_context_path.read_text(encoding="utf-8")
    assert "Continuar o projeto Jarvis" in payload
    assert '"topic": "jarvis"' in payload

    status = client.get("/api/status")
    assert status.status_code == 200
    assert status.json()["memory"]["hierarchical"]["working_memory_messages"] == 2

    context = client.get("/api/memory/context", params={"workspace": "jarvis"})
    assert context.status_code == 200
    assert context.json()["hierarchical"]["active_topics"] >= 1


def test_hierarchical_memory_compacts_important_history(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module

    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        working_memory_limit=3,
        working_memory_preserve_recent=2,
    )
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "OllamaClient", FakeOllama)

    memory = MemoryManager()
    memory.record_exchange(
        user_content="Decidi usar Kotlin no app Android do projeto.",
        user_display_content="Decidi usar Kotlin no app Android do projeto.",
        assistant_content="Vamos manter Kotlin como base.",
        workspace=None,
        model="jarvis-codex",
    )
    memory.record_exchange(
        user_content="oi",
        user_display_content="oi",
        assistant_content="ok",
        workspace=None,
        model="jarvis-codex",
    )

    summary_path = test_settings.memory_dir / "summaries" / "programming.json"
    topic_path = test_settings.topic_memory_dir / "programming.md"
    active_path = test_settings.active_memory_dir / "programming.json"

    assert summary_path.exists()
    assert topic_path.exists()
    assert active_path.exists()
    assert "Kotlin" in summary_path.read_text(encoding="utf-8")
    assert "Kotlin" in topic_path.read_text(encoding="utf-8")
    assert "Kotlin" in active_path.read_text(encoding="utf-8")
