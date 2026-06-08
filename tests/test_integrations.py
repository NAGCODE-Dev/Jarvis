from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_obsidian_plugin_manifest_and_files_exist():
    plugin_dir = ROOT / "apps" / "obsidian-plugin" / "jarvis-local"
    manifest = json.loads((plugin_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["id"] == "jarvis-local"
    assert (plugin_dir / "main.js").exists()
    assert (plugin_dir / "styles.css").exists()
    assert (plugin_dir / "README.md").exists()


def test_pwa_files_exist():
    web_dir = ROOT / "apps" / "web"
    assert (web_dir / "index.html").exists()
    assert (web_dir / "app.js").exists()
    assert (web_dir / "styles.css").exists()
    assert (web_dir / "manifest.webmanifest").exists()
    assert (web_dir / "sw.js").exists()


def test_pwa_contains_session_management_controls():
    web_dir = ROOT / "apps" / "web"
    html = (web_dir / "index.html").read_text(encoding="utf-8")
    js = (web_dir / "app.js").read_text(encoding="utf-8")

    assert 'id="delete-chat"' in html
    assert 'id="session-title"' in html
    assert "STORAGE_KEY" in js
    assert 'method: "DELETE"' in js
