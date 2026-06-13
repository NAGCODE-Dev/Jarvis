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


def test_linux_app_files_exist():
    linux_dir = ROOT / "apps" / "linux"
    desktop_template = linux_dir / "jarvis-local.desktop.in"
    launcher = ROOT / "scripts" / "run_linux_app.sh"
    installer = ROOT / "scripts" / "install_linux_app.sh"

    assert desktop_template.exists()
    assert launcher.exists()
    assert installer.exists()

    desktop_text = desktop_template.read_text(encoding="utf-8")
    launcher_text = launcher.read_text(encoding="utf-8")
    installer_text = installer.read_text(encoding="utf-8")

    assert "Name=Jarvis Local" in desktop_text
    assert "scripts/run_linux_app.sh" in desktop_text
    assert '--app="$APP_URL"' in launcher_text
    assert "boot_local.sh" in launcher_text
    assert "jarvis-local.desktop" in installer_text
    assert "Jarvis Local" in installer_text


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
    css = (web_dir / "styles.css").read_text(encoding="utf-8")

    assert 'id="attach-file"' in html
    assert 'id="ctx-active-file"' in html
    assert 'id="ctx-open-tabs"' in html
    assert 'id="ctx-terminal"' in html
    assert 'id="ctx-search"' in html
    assert 'id="composer-context-preview"' in html
    assert 'id="file-input"' in html
    assert 'class="secondary quick-action"' in html
    assert "/message/stream" in js
    assert "buildAttachmentPrompt" in js
    assert "buildOperationalContextBlock" in js
    assert "renderComposerContextPreview" in js
    assert "CONTEXT_PREFS_KEY" in js
    assert 'id="session-search"' in html
    assert 'id="export-chat"' in html
    assert "exportCurrentSessionMarkdown" in js
    assert 'data-dropzone="idle"' in html
    assert "dragenter" in js
    assert "setDropzoneState" in js
    assert 'id="workspace-files"' in html
    assert 'id="workspace-search"' in html
    assert 'id="run-workspace-search"' in html
    assert 'id="clear-workspace-search"' in html
    assert 'id="workspace-search-results"' in html
    assert 'id="new-folder"' in html
    assert 'id="open-path"' in html
    assert 'id="file-editor"' in html
    assert 'id="refresh-operations"' in html
    assert 'id="session-operations"' in html
    assert 'id="editor-tabs"' in html
    assert 'id="editor-instruction"' in html
    assert 'id="editor-selection"' in html
    assert 'id="ask-jarvis-batch-edit"' in html
    assert 'id="apply-batch-proposal"' in html
    assert 'id="save-all-files"' in html
    assert 'id="attach-open-tabs"' in html
    assert 'id="run-selection"' in html
    assert 'id="editor-batch-output"' in html
    assert 'id="editor-batch-proposals"' in html
    assert 'id="run-task-assist"' in html
    assert 'id="run-task-cycle"' in html
    assert 'id="run-suggested-command"' in html
    assert 'id="editor-task-output"' in html
    assert 'id="editor-diff"' in html
    assert 'id="editor-hunks"' in html
    assert 'id="ask-jarvis-edit"' in html
    assert 'id="apply-proposal"' in html
    assert 'id="rename-file"' in html
    assert 'id="delete-file"' in html
    assert 'id="restart-terminal"' in html
    assert 'id="new-terminal"' in html
    assert 'id="close-terminal"' in html
    assert 'id="terminal-sessions"' in html
    assert 'id="interrupt-terminal"' in html
    assert 'id="terminal-command"' in html
    assert 'id="run-terminal-command"' in html
    assert 'id="send-terminal-command"' in html
    assert 'id="cd-file-dir"' in html
    assert 'id="command-history"' in html
    assert 'id="clear-command-history"' in html
    assert 'id="git-status"' in html
    assert 'id="git-diff"' in html
    assert 'id="git-log"' in html
    assert 'id="git-github"' in html
    assert 'id="git-attach"' in html
    assert 'id="git-output"' in html
    assert 'id="refresh-approvals"' in html
    assert 'id="self-improve-active"' in html
    assert 'id="queue-suggested-command"' in html
    assert 'id="queue-edit-proposal"' in html
    assert 'id="approvals"' in html
    assert 'id="remember-note"' in html
    assert 'id="index-note"' in html
    assert 'id="chat-about-note"' in html
    assert 'id="obsidian-auto-remember"' in html
    assert 'id="obsidian-auto-index"' in html
    assert 'id="recent-files"' in html
    assert 'id="clear-recent-files"' in html
    assert 'id="slash-commands"' in html
    assert "/api/workspace/search" in js
    assert "/api/workspace/tree" in js
    assert "/api/workspace/file" in js
    assert "/api/workspace/directory" in js
    assert "/api/workspace/rename" in js
    assert "/api/workspace/edit-proposal" in js
    assert "/api/workspace/batch-edit-proposal" in js
    assert "/api/workspace/task-assist" in js
    assert "/api/workspace/task-cycle" in js
    assert "/api/workspace/path?path=" in js
    assert "/api/terminal/sessions" in js
    assert "openWorkspaceFile" in js
    assert "mapTerminalKey" in js
    assert "renderEditorTabs" in js
    assert "renderTerminalSessions" in js
    assert "appendSessionOperation" in js
    assert "renderSessionOperations" in js
    assert "renderWorkspaceSearchResults" in js
    assert "renderTaskAssist" in js
    assert "renderBatchProposal" in js
    assert "handleSlashCommand" in js
    assert "rememberCurrentNote" in js
    assert "indexCurrentNote" in js
    assert "prepareChatFromCurrentNote" in js
    assert "runTerminalCommandFromInput" in js
    assert "renderRecentFiles" in js
    assert "renderSlashCommands" in js
    assert "renderCommandHistory" in js
    assert "trackCommandHistory" in js
    assert "renderGitOutput" in js
    assert "runGitCommand" in js
    assert "attachGitContextToChat" in js
    assert "latestGitContext" in js
    assert "renderApprovals" in js
    assert "queueApproval" in js
    assert "actOnApproval" in js
    assert "runSelfImproveActive" in js
    assert "queueSuggestedCommandApproval" in js
    assert "queueEditProposalApproval" in js
    assert "/api/terminal/run" in js
    assert '"/git-status"' in js
    assert '"/git-diff"' in js
    assert '"/git-log"' in js
    assert '"/git-attach"' in js
    assert '"/queue-command"' in js
    assert '"/queue-edit"' in js
    assert '"/self-review"' in js
    assert "/api/chat/sessions/${currentSessionId}/approvals" in js
    assert "saveAllEditors" in js
    assert "attachOpenTabsToChat" in js
    assert "runEditorSelectionInTerminal" in js
    assert '"/save-all"' in js
    assert '"/attach-tabs"' in js
    assert '"/run-selection"' in js
    assert "runObsidianAssistOnSave" in js
    assert "buildHelpGuide" in js
    assert "loadObsidianPrefs" in js
    assert "persistObsidianPrefs" in js
    assert '"/help"' in js
    assert "applyBatchProposalFile" in js
    assert "applyBatchProposalHunk" in js
    assert "renderEditProposal" in js
    assert "applyProposalHunk" in js
    assert "mergeInstructionWithSelection" in js
    assert "workspace-search-row" in css
    assert "terminal-session-chip" in css
    assert "composer-context-preview" in css
    assert "editor-selection" in css
    assert "workspace-history-shell" in css
    assert "session-operation-card" in css
    assert "workspace-codex-grid" in css
    assert "workspace-obsidian-shell" in css
    assert "obsidian-status" in css
    assert "obsidian-automation-row" in css
    assert "recent-files" in css
    assert "terminal-command-row" in css
    assert "terminal-help-shell" in css
    assert "command-history" in css
    assert "command-history-chip" in css
    assert "git-shell" in css
    assert "git-header" in css
    assert "git-actions" in css
    assert "git-output" in css
    assert "approval-shell" in css
    assert "approval-header" in css
    assert "approvals-list" in css
    assert "approval-card" in css
    assert "approval-card-preview" in css
    assert "slash-command-shell" in css
    assert "slash-commands" in css
    assert "slash-command-chip" in css
    assert "editor-batch-card" in css
    assert "editor-batch-card-actions" in css
    assert "editor-batch-hunk-button" in css
    assert "editor-tab" in css
    assert "editor-task-output" in css
    assert "editor-diff" in css
    assert "editor-hunk-card" in css
