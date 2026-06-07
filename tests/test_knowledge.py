from __future__ import annotations

from pathlib import Path

from jarvis.knowledge import KnowledgeService


class FakeOllama:
    def embed(self, text, model=None):
        if isinstance(text, list):
            return [[0.1, 0.2, 0.3] for _ in text]
        return [[0.1, 0.2, 0.3]]


def test_knowledge_uses_local_qdrant_when_remote_unavailable(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.knowledge as knowledge_module

    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=config_module.settings.config_dir)
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(knowledge_module, "settings", test_settings)

    docs_dir = test_settings.knowledge_dir / "programacao"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "note.md").write_text("FastAPI routers can orchestrate local assistants.", encoding="utf-8")

    service = knowledge_module.KnowledgeService(FakeOllama())
    result = service.index_domains(domains=["programacao"])
    assert result["indexed_files"] == 1

    search_results = service.search("FastAPI local assistants", domain="programacao", top_k=1)
    assert len(search_results) == 1
    assert service.mode == "local"
