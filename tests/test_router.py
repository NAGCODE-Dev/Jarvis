from __future__ import annotations

from jarvis.memory import MemoryManager
from jarvis.router import JarvisRouter
from jarvis.schemas import ChatMessage


class FakeOllama:
    def list_models(self):
        return {"models": [{"name": "qwen3:8b"}]}

    def chat(self, model, messages, temperature=None):
        return f"{model}:{messages[-1].content}"

    def embed(self, text, model=None):
        if isinstance(text, list):
            return [[0.1, 0.2] for _ in text]
        return [[0.1, 0.2]]


class FakeKnowledge:
    def search(self, query, top_k=4, domain=None, score_threshold=None):
        return []


class FallbackOllama(FakeOllama):
    def list_models(self):
        return {"models": [{"name": "qwen2.5:3b"}]}

    def chat(self, model, messages, temperature=None):
        if model in {"qwen3:8b", "qwen3:4b"}:
            raise RuntimeError("model not installed")
        return f"{model}:{messages[-1].content}"


def test_router_prefers_coder_for_code_query(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)

    router = JarvisRouter(FakeOllama(), MemoryManager(), FakeKnowledge())
    response = router.complete("jarvis", [ChatMessage(role="user", content="Analise este código Python")])

    assert "qwen3:8b" in response


def test_router_falls_back_to_installed_ollama_model(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)

    router = JarvisRouter(FallbackOllama(), MemoryManager(), FakeKnowledge())
    response = router.complete("jarvis", [ChatMessage(role="user", content="Analise este código Python")])

    assert "qwen2.5:3b" in response
