from __future__ import annotations

from fastapi.testclient import TestClient

from jarvis.api import create_api_router
from jarvis.memory import MemoryManager


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


def test_models_endpoint(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    from fastapi import FastAPI

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)

    app = FastAPI()
    app.include_router(create_api_router(FakeOllama(), MemoryManager(), FakeKnowledge()))
    client = TestClient(app)

    response = client.get("/v1")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    response = client.get("/v1/models")
    assert response.status_code == 200
    assert response.json()["object"] == "list"
    assert any(model["id"] == "jarvis-programador" for model in response.json()["data"])
    assert any(model["id"] == "jarvis-programador-safe" for model in response.json()["data"])

    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["core"]["status"] == "ok"

    response = client.post(
        "/api/memory/workspace",
        json={"workspace": "jarvis", "field": "topic", "value": "context selection", "source": "test"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/memory/action",
        json={"action": "update_state", "field": "weight.current_kg", "value": 72, "source": "test"},
    )
    assert response.status_code == 200

    response = client.get("/api/memory/context", params={"workspace": "jarvis"})
    assert response.status_code == 200
    assert response.json()["context"]["workspace"]["name"] == "jarvis"

    response = client.post(
        "/api/knowledge/ingest-note",
        json={
            "domain": "jarvis",
            "title": "Arquitetura Jarvis",
            "content": "# Arquitetura\n\nNotas do Obsidian.",
            "source_path": "Jarvis/Arquitetura.md",
        },
    )
    assert response.status_code == 200
    assert response.json()["domain"] == "jarvis"


def test_web_app_shell(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.knowledge as knowledge_module
    import jarvis.main as main_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.ollama_client as ollama_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(main_module, "settings", test_settings)
    monkeypatch.setattr(knowledge_module, "settings", test_settings)
    monkeypatch.setattr(ollama_module, "settings", test_settings)
    monkeypatch.setattr(main_module, "OllamaClient", FakeOllama)
    monkeypatch.setattr(main_module, "KnowledgeService", lambda ollama: FakeKnowledge())

    app = main_module.create_app()
    client = TestClient(app)

    response = client.get("/", follow_redirects=False)
    assert response.status_code in {302, 307}
    assert response.headers["location"] == "/app/"

    response = client.get("/app/")
    assert response.status_code == 200
    assert "Jarvis Local" in response.text

    response = client.get("/app/manifest.webmanifest")
    assert response.status_code == 200


def test_chat_sessions_api(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    from fastapi import FastAPI

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)

    app = FastAPI()
    app.include_router(create_api_router(FakeOllama(), MemoryManager(), FakeKnowledge()))
    client = TestClient(app)

    response = client.post("/api/chat/sessions", json={"model": "jarvis-safe", "workspace": "jarvis"})
    assert response.status_code == 200
    session = response.json()["session"]
    session_id = session["id"]

    response = client.post(
        f"/api/chat/sessions/{session_id}/message",
        json={"model": "jarvis-safe", "content": "oi", "display_content": "Oi limpo", "workspace": "jarvis"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "ok"
    assert len(response.json()["session"]["messages"]) == 2
    assert response.json()["session"]["messages"][0]["display_content"] == "Oi limpo"

    response = client.get("/api/chat/sessions")
    assert response.status_code == 200
    assert response.json()["sessions"][0]["id"] == session_id
