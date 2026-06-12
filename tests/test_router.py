from __future__ import annotations

from jarvis.memory import MemoryManager
from jarvis.router import JarvisRouter
from jarvis.schemas import ChatMessage


class FakeOllama:
    def list_models(self):
        return {"models": [{"name": "qwen2.5-coder:1.5b"}, {"name": "qwen2.5:3b"}, {"name": "qwen3:1.7b"}]}

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
        return {"models": [{"name": "qwen2.5-coder:1.5b"}, {"name": "qwen2.5:3b"}]}

    def chat(self, model, messages, temperature=None):
        if model == "qwen2.5-coder:1.5b":
            raise RuntimeError("model not installed")
        return f"{model}:{messages[-1].content}"


class CapturingOllama(FakeOllama):
    def __init__(self):
        self.last_messages = []

    def chat(self, model, messages, temperature=None):
        self.last_messages = list(messages)
        return f"{model}:{messages[-1].content}"


def test_router_prefers_coder_for_code_query(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)

    router = JarvisRouter(FakeOllama(), MemoryManager(), FakeKnowledge())
    response = router.complete("jarvis", [ChatMessage(role="user", content="Analise este código Python")])

    assert test_settings.coder_model in response


def test_safe_router_uses_lighter_coder_profile(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)

    router = JarvisRouter(FakeOllama(), MemoryManager(), FakeKnowledge())
    response = router.complete("jarvis-programador-safe", [ChatMessage(role="user", content="Analise este código Python")])

    assert test_settings.safe_coder_model in response


def test_explicit_quality_coder_uses_configured_coder_model(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)

    router = JarvisRouter(FakeOllama(), MemoryManager(), FakeKnowledge())
    response = router.complete("jarvis-programador", [ChatMessage(role="user", content="Analise este código Python")])

    assert test_settings.coder_model in response


def test_router_falls_back_to_installed_ollama_model(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)

    router = JarvisRouter(FallbackOllama(), MemoryManager(), FakeKnowledge())
    response = router.complete("jarvis", [ChatMessage(role="user", content="Analise este código Python")])

    assert "qwen2.5:3b" in response


def test_router_compacts_long_conversations(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.memory as memory_module
    import jarvis.model_registry as registry_module
    import jarvis.router as router_module

    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        history_char_budget=1000,
        history_preserve_messages=2,
    )
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(memory_module, "settings", test_settings)
    monkeypatch.setattr(registry_module, "settings", test_settings)
    monkeypatch.setattr(router_module, "settings", test_settings)

    ollama = CapturingOllama()
    router = JarvisRouter(ollama, MemoryManager(), FakeKnowledge())
    messages = [
        ChatMessage(role="user", content="A" * 320),
        ChatMessage(role="assistant", content="B" * 320),
        ChatMessage(role="user", content="C" * 320),
        ChatMessage(role="assistant", content="D" * 320),
        ChatMessage(role="user", content="E" * 80),
    ]

    router.complete("jarvis-codex", messages)

    contents = [message.content for message in ollama.last_messages if message.role != "system"]
    assert contents == ["D" * 320, "E" * 80]
    assert any("Conversation context compacted" in message.content for message in ollama.last_messages if message.role == "system")
