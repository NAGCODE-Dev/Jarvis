from __future__ import annotations

from pathlib import Path

from jarvis import config as config_module
from jarvis.memory import MemoryAction, MemoryManager


def test_memory_writes_files(tmp_path: Path, monkeypatch):
    test_settings = config_module.Settings(data_dir=tmp_path / "data", config_dir=tmp_path / "config")
    monkeypatch.setattr(config_module, "settings", test_settings)

    import jarvis.memory as memory_module

    monkeypatch.setattr(memory_module, "settings", test_settings)
    manager = memory_module.MemoryManager()

    manager.apply(MemoryAction(action="set_identity_fact", field="preferences.editor", value="VS Code", source="test"))
    manager.apply(MemoryAction(action="update_state", field="project.current", value="working on Jarvis", source="test"))
    manager.apply(MemoryAction(action="append_timeline_event", field="timeline.event", value="Initialized tests", source="test"))
    manager.apply(MemoryAction(action="append_workspace_note", field="topic", value="router refactor", source="test", workspace="jarvis"))
    summary = manager.summarize_memory(label="unit-test")

    assert "VS Code" in test_settings.preferences_path.read_text(encoding="utf-8")
    assert "working on Jarvis" in test_settings.state_path.read_text(encoding="utf-8")
    assert "Initialized tests" in test_settings.timeline_path.read_text(encoding="utf-8")
    assert (test_settings.workspace_memory_dir / "jarvis" / "current.md").exists()
    assert test_settings.memory_catalog_path.exists()
    assert summary.exists()
