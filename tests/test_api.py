from __future__ import annotations

from fastapi.testclient import TestClient

from jarvis.api import create_api_router
from jarvis.memory import MemoryManager


class FakeOllama:
    def health(self):
        return {"status": "ok", "models": ["qwen3:4b"]}

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

    response = client.get("/v1/models")
    assert response.status_code == 200
    assert any(model["id"] == "jarvis-programador" for model in response.json()["data"])

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
