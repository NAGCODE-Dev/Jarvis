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


def test_obsidian_plugin_contains_session_search_and_rename_controls():
    plugin_dir = ROOT / "apps" / "obsidian-plugin" / "jarvis-local"
    js = (plugin_dir / "main.js").read_text(encoding="utf-8")
    css = (plugin_dir / "styles.css").read_text(encoding="utf-8")

    assert "jarvis-chat-session-search" in js
    assert 'text: "Renomear"' in js
    assert "updateSession(sessionId, payload)" in js
    assert "jarvis-chat-session-meta" in css
    assert "sendCurrentNoteToChatView" in js
    assert 'text: "Pesquisa"' in js
    assert "jarvis-chat-quick-actions" in css
    assert 'text: "Salvar resposta"' in js
    assert 'text: "Inserir na nota"' in js
    assert "exportChatMessageToNote" in js
    assert "appendChatMessageToActiveNote" in js
    assert "jarvis-chat-message-actions" in css
    assert 'text: "Anexar nota"' in js
    assert 'text: "Anexar seleção"' in js
    assert "buildCurrentNoteAttachment" in js
    assert "buildCurrentSelectionAttachment" in js
    assert "jarvis-chat-attachment-chip" in css


def test_pwa_files_exist():
    web_dir = ROOT / "apps" / "web"
    assert (web_dir / "index.html").exists()
    assert (web_dir / "app.js").exists()
    assert (web_dir / "styles.css").exists()
    assert (web_dir / "manifest.webmanifest").exists()
    assert (web_dir / "sw.js").exists()
    assert (ROOT / "scripts" / "pwa_smoke.sh").exists()
    assert (ROOT / "MANUAL_VALIDATION.md").exists()


def test_pwa_contains_session_management_controls():
    web_dir = ROOT / "apps" / "web"
    html = (web_dir / "index.html").read_text(encoding="utf-8")
    js = (web_dir / "app.js").read_text(encoding="utf-8")

    assert 'id="delete-chat"' in html
    assert 'id="session-title"' in html
    assert "STORAGE_KEY" in js
    assert 'method: "DELETE"' in js


def test_pwa_contains_streaming_attachments_and_quick_actions():
    web_dir = ROOT / "apps" / "web"
    html = (web_dir / "index.html").read_text(encoding="utf-8")
    js = (web_dir / "app.js").read_text(encoding="utf-8")

    assert 'id="attach-file"' in html
    assert 'id="file-input"' in html
    assert 'class="secondary quick-action"' in html
    assert "/message/stream" in js
    assert "buildAttachmentPrompt" in js
    assert 'id="session-search"' in html
    assert 'id="export-chat"' in html
    assert "exportCurrentSessionMarkdown" in js
    assert 'data-dropzone="idle"' in html
    assert "dragenter" in js
    assert "setDropzoneState" in js
