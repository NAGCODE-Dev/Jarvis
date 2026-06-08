from __future__ import annotations

import argparse
from pathlib import Path

from jarvis import cli


def test_obsidian_note_uses_frontmatter_and_appends(tmp_path: Path, monkeypatch):
    note = tmp_path / "faculdade" / "aula.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text(
        "---\nworkspace: faculdade\njarvis_mode: research\n---\n# Aula\n\nResumo da matéria.\n",
        encoding="utf-8",
    )

    captured: dict[str, object] = {}

    def fake_chat_request(*, model: str, messages: list[dict[str, str]], temperature: float | None, timeout: float) -> str:
        captured["model"] = model
        captured["prompt"] = messages[0]["content"]
        return "## Resposta\n\nConteúdo útil."

    monkeypatch.setattr(cli, "_chat_request", fake_chat_request)

    args = argparse.Namespace(
        note=note,
        instruction="Complete esta nota.",
        model=None,
        workspace=None,
        append=True,
        title="Jarvis Research",
        temperature=None,
        timeout=30.0,
    )

    rc = cli.cmd_obsidian_note(args)
    assert rc == 0
    assert captured["model"] == "jarvis-pesquisador-safe"
    assert "Workspace inferido: faculdade" in str(captured["prompt"])
    updated = note.read_text(encoding="utf-8")
    assert "## Jarvis Research" in updated
    assert "Conteúdo útil." in updated


def test_infer_workspace_from_note_path():
    note = Path("/vault/programacao/jarvis/nota.md")
    workspace = cli._infer_workspace_from_note_path(note, {})
    assert workspace == "jarvis"


def test_obsidian_sync_uses_knowledge_service(tmp_path: Path, monkeypatch):
    note = tmp_path / "crossfit" / "wod.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text("# WOD\n\nTreino do dia.\n", encoding="utf-8")

    captured: dict[str, object] = {}

    class FakeKnowledgeService:
        def __init__(self, _ollama):
            pass

        def ingest_note(self, *, domain, title, content, source_path=None, force=False):
            captured["domain"] = domain
            captured["title"] = title
            captured["content"] = content
            captured["source_path"] = source_path
            return {"stored_path": "knowledge/crossfit/obsidian/wod.md", "indexed_chunks": 1, "domain": domain}

    monkeypatch.setattr(cli, "KnowledgeService", FakeKnowledgeService)
    monkeypatch.setattr(cli, "OllamaClient", lambda: object())

    args = argparse.Namespace(note=note, workspace=None, title=None, force=False)
    rc = cli.cmd_obsidian_sync(args)

    assert rc == 0
    assert captured["domain"] == "crossfit"
    assert captured["title"] == "wod"
    assert "Treino do dia." in str(captured["content"])


def test_obsidian_remember_uses_memory_service(tmp_path: Path, monkeypatch):
    note = tmp_path / "jarvis" / "roadmap.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text("# Roadmap\n\nPlanejar plugin do Obsidian.\n", encoding="utf-8")

    captured: dict[str, object] = {}

    class FakeMemoryManager:
        def apply(self, action):
            captured["action"] = action
            return {"path": "data/memory/workspaces/jarvis/current.md"}

    monkeypatch.setattr(cli, "MemoryManager", FakeMemoryManager)

    args = argparse.Namespace(note=note, workspace=None, field=None, max_chars=200)
    rc = cli.cmd_obsidian_remember(args)

    assert rc == 0
    action = captured["action"]
    assert action.workspace == "jarvis"
    assert action.field == "obsidian.roadmap"
    assert "Planejar plugin do Obsidian." in str(action.value)


def test_obsidian_sync_dir_syncs_all_markdown_files(tmp_path: Path, monkeypatch):
    folder = tmp_path / "faculdade"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "a.md").write_text("# A\n\nConteúdo A\n", encoding="utf-8")
    (folder / "b.md").write_text("---\nworkspace: faculdade\n---\n# B\n\nConteúdo B\n", encoding="utf-8")
    (folder / "ignore.txt").write_text("x", encoding="utf-8")

    captured: list[tuple[str, str, str]] = []

    class FakeKnowledgeService:
        def __init__(self, _ollama):
            pass

        def ingest_note(self, *, domain, title, content, source_path=None, force=False):
            captured.append((domain, title, source_path or ""))
            return {"stored_path": f"knowledge/{domain}/obsidian/{title}.md", "indexed_chunks": 1, "domain": domain}

    monkeypatch.setattr(cli, "KnowledgeService", FakeKnowledgeService)
    monkeypatch.setattr(cli, "OllamaClient", lambda: object())

    args = argparse.Namespace(directory=folder, workspace=None, force=False, non_recursive=False)
    rc = cli.cmd_obsidian_sync_dir(args)

    assert rc == 0
    assert len(captured) == 2
    assert captured[0][0] == "faculdade"
    assert {item[1] for item in captured} == {"a", "b"}
