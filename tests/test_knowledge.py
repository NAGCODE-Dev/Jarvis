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

    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        qdrant_url="http://127.0.0.1:65533",
    )
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


def test_knowledge_recreates_collection_when_force_and_dimension_mismatch(tmp_path, monkeypatch):
    import jarvis.config as config_module
    import jarvis.knowledge as knowledge_module
    from qdrant_client import QdrantClient
    from qdrant_client.http import models as qm

    local_path = tmp_path / "qdrant-local"
    test_settings = config_module.Settings(
        data_dir=tmp_path / "data",
        config_dir=config_module.settings.config_dir,
        qdrant_url="http://127.0.0.1:65533",
        qdrant_local_pathname="qdrant-local",
    )
    monkeypatch.setattr(config_module, "settings", test_settings)
    monkeypatch.setattr(knowledge_module, "settings", test_settings)

    client = QdrantClient(path=str(local_path))
    client.create_collection(
        collection_name=test_settings.qdrant_collection,
        vectors_config=qm.VectorParams(size=2, distance=qm.Distance.COSINE),
    )

    docs_dir = test_settings.knowledge_dir / "linux"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "note.md").write_text("Linux verification collection.", encoding="utf-8")

    service = knowledge_module.KnowledgeService(FakeOllama())
    result = service.index_domains(domains=["linux"], force=True)
    assert result["indexed_files"] == 1

    info = service.client.get_collection(test_settings.qdrant_collection)
    assert info.config.params.vectors.size == 3
