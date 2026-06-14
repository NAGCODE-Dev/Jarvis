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
    canonical_launcher = ROOT / "scripts" / "jarvis.sh"
    launcher = ROOT / "scripts" / "run_linux_app.sh"
    installer = ROOT / "scripts" / "install_linux_app.sh"
    deb_builder = ROOT / "scripts" / "build_deb.sh"
    deb_smoke = ROOT / "scripts" / "deb_smoke.sh"
    deb_installer = ROOT / "scripts" / "install_deb_local.sh"
    package_doctor = ROOT / "scripts" / "package_doctor.sh"
    package_setup = ROOT / "scripts" / "package_setup.sh"
    runtime_env = ROOT / "scripts" / "_runtime_env.sh"
    package_help = ROOT / "apps" / "linux" / "package_help.html"
    debian_dir = ROOT / "packaging" / "debian"
    debian_control = debian_dir / "control.in"
    debian_postinst = debian_dir / "postinst"
    debian_prerm = debian_dir / "prerm"
    debian_desktop = debian_dir / "jarvis-local.desktop.in"

    assert desktop_template.exists()
    assert canonical_launcher.exists()
    assert launcher.exists()
    assert installer.exists()
    assert deb_builder.exists()
    assert deb_smoke.exists()
    assert deb_installer.exists()
    assert package_doctor.exists()
    assert package_setup.exists()
    assert runtime_env.exists()
    assert package_help.exists()
    assert debian_control.exists()
    assert debian_postinst.exists()
    assert debian_prerm.exists()
    assert debian_desktop.exists()

    desktop_text = desktop_template.read_text(encoding="utf-8")
    canonical_launcher_text = canonical_launcher.read_text(encoding="utf-8")
    launcher_text = launcher.read_text(encoding="utf-8")
    installer_text = installer.read_text(encoding="utf-8")
    deb_builder_text = deb_builder.read_text(encoding="utf-8")
    deb_installer_text = deb_installer.read_text(encoding="utf-8")
    package_doctor_text = package_doctor.read_text(encoding="utf-8")
    package_setup_text = package_setup.read_text(encoding="utf-8")
    runtime_env_text = runtime_env.read_text(encoding="utf-8")
    package_help_text = package_help.read_text(encoding="utf-8")
    debian_control_text = debian_control.read_text(encoding="utf-8")
    debian_postinst_text = debian_postinst.read_text(encoding="utf-8")
    debian_prerm_text = debian_prerm.read_text(encoding="utf-8")
    debian_desktop_text = debian_desktop.read_text(encoding="utf-8")

    assert "Name=Jarvis Local" in desktop_text
    assert "scripts/run_linux_app.sh" in desktop_text
    assert "scripts/jarvis.sh" in launcher_text
    assert "package_doctor.sh" in launcher_text
    assert "package_help.html" in launcher_text
    assert '--app="$APP_URL"' in launcher_text
    assert "scripts/jarvis.sh" in canonical_launcher_text
    assert "scripts/package_doctor.sh" in canonical_launcher_text
    assert "scripts/package_setup.sh" in canonical_launcher_text
    assert "run_cli_chat chat jarvis-safe" in canonical_launcher_text

    continue_preflight_text = (ROOT / "scripts" / "continue_preflight.sh").read_text(encoding="utf-8")
    continue_smoke_text = (ROOT / "scripts" / "continue_smoke.sh").read_text(encoding="utf-8")
    assert "jarvis-local.desktop" in installer_text
    assert "Jarvis Local" in installer_text
    assert "/opt/jarvis-local/app" in deb_builder_text
    assert "DEBIAN" in deb_builder_text
    assert "packaging/debian" in deb_builder_text
    assert "scripts/jarvis.sh app" in deb_builder_text
    assert "OUTPUT_PATH" in deb_builder_text
    assert "postinst" in deb_builder_text
    assert "prerm" in deb_builder_text
    assert "dpkg -i" in deb_installer_text
    assert "Package: @PACKAGE_NAME@" in debian_control_text
    assert "Architecture: @ARCH@" in debian_control_text
    assert "update-desktop-database" in debian_postinst_text
    assert "update-desktop-database" in debian_prerm_text
    assert "Exec=/usr/bin/jarvis-local" in debian_desktop_text
    assert "python operacional" in package_doctor_text
    assert "JARVIS_VENV_DIR" in package_doctor_text
    assert "setup-local" in package_setup_text
    assert "JARVIS_RUNTIME_HOME/continue" in continue_preflight_text
    assert "JARVIS_RUNTIME_HOME/continue-smoke" in continue_smoke_text
    assert "JARVIS_ENV_FILE" in runtime_env_text
    assert "JARVIS_DATA_DIR" in runtime_env_text
    assert "Jarvis Local não conseguiu iniciar automaticamente" in package_help_text
    assert "setup-local" in package_help_text


def test_canonical_chat_wrappers_delegate_to_jarvis_launcher():
    chat_wrapper = (ROOT / "scripts" / "chat.sh").read_text(encoding="utf-8")
    code_wrapper = (ROOT / "scripts" / "code_chat.sh").read_text(encoding="utf-8")
    research_wrapper = (ROOT / "scripts" / "research_chat.sh").read_text(encoding="utf-8")

    assert 'scripts/jarvis.sh" chat' in chat_wrapper
    assert 'scripts/jarvis.sh" code' in code_wrapper
    assert 'scripts/jarvis.sh" research' in research_wrapper

    chat_repl_wrapper = (ROOT / "scripts" / "chat_repl.sh").read_text(encoding="utf-8")
    code_repl_wrapper = (ROOT / "scripts" / "code_chat_repl.sh").read_text(encoding="utf-8")
    research_repl_wrapper = (ROOT / "scripts" / "research_chat_repl.sh").read_text(encoding="utf-8")

    assert 'scripts/jarvis.sh" repl' in chat_repl_wrapper
    assert 'scripts/jarvis.sh" code-repl' in code_repl_wrapper
    assert 'scripts/jarvis.sh" research-repl' in research_repl_wrapper


def test_cli_wrappers_use_runtime_aware_python_resolution():
    wrapper_paths = [
        ROOT / "scripts" / "index_knowledge.sh",
        ROOT / "scripts" / "benchmark_models.sh",
        ROOT / "scripts" / "memory_action.sh",
        ROOT / "scripts" / "show_context.sh",
        ROOT / "scripts" / "smoke_test.sh",
        ROOT / "scripts" / "obsidian_sync_dir.sh",
        ROOT / "scripts" / "obsidian_sync_note.sh",
        ROOT / "scripts" / "obsidian_remember_note.sh",
    ]

    for wrapper in wrapper_paths:
        content = wrapper.read_text(encoding="utf-8")
        assert 'scripts/_ensure_python_env.sh' in content
        assert 'scripts/_resolve_python.sh' in content
        assert 'PYTHONPATH="$ROOT_DIR/apps/core"' in content


def test_pwa_contains_session_management_controls():
    web_dir = ROOT / "apps" / "web"
    html = (web_dir / "index.html").read_text(encoding="utf-8")
    js = (web_dir / "app.js").read_text(encoding="utf-8")

    assert 'id="delete-chat"' in html
    assert 'id="session-title"' in html
    assert 'id="pin-session"' in html
    assert 'id="archive-session"' in html
    assert 'id="open-session-note"' in html
    assert 'id="attach-session-note"' in html
    assert 'id="session-filters"' in html
    assert 'data-session-filter="active"' in html
    assert 'data-session-filter="archived"' in html
    assert 'id="replay-session"' in html
    assert 'id="replay-toggle"' in html
    assert 'id="replay-next"' in html
    assert 'id="replay-stop"' in html
    assert 'id="replay-status"' in html
    assert 'id="mode-chat"' in html
    assert 'id="mode-build"' in html
    assert 'id="mode-review"' in html
    assert 'id="mode-focus"' in html
    assert 'id="workbench-status"' in html
    assert 'id="prompt-active-file"' in html
    assert 'id="prompt-terminal-debug"' in html
    assert 'id="prompt-create-file"' in html
    assert 'id="prompt-next-step"' in html
    assert 'id="refresh-mission-control"' in html
    assert 'id="mission-briefing"' in html
    assert 'id="mission-status"' in html
    assert 'id="mission-next-actions"' in html
    assert 'id="mission-objective"' in html
    assert 'id="mission-status-input"' in html
    assert 'id="mission-next-steps-input"' in html
    assert 'id="save-mission"' in html
    assert 'id="starter-inspect-project"' in html
    assert 'id="starter-fix-error"' in html
    assert 'id="starter-create-file"' in html
    assert 'id="starter-next-step"' in html
    assert 'id="starter-guided"' in html
    assert 'id="starter-readiness"' in html
    assert 'id="starter-context"' in html
    assert 'id="workspace-quality-first"' in html
    assert 'id="workspace-auto-profile"' in html
    assert 'id="apply-workspace-preset"' in html
    assert 'id="save-workspace-preset"' in html
    assert 'id="workspace-preset-status"' in html
    assert 'id="onboarding-wizard"' in html
    assert 'id="onboarding-wizard-form"' in html
    assert 'id="onboarding-mode"' in html
    assert 'id="onboarding-workspace"' in html
    assert 'id="onboarding-goal"' in html
    assert 'id="onboarding-target-path"' in html
    assert 'id="task-title"' in html
    assert 'id="task-phase"' in html
    assert 'id="create-task"' in html
    assert 'id="task-board"' in html
    assert 'id="open-command-palette"' in html
    assert 'id="command-palette"' in html
    assert 'id="command-palette-backdrop"' in html
    assert 'id="command-palette-input"' in html
    assert 'id="command-palette-results"' in html
    assert 'id="close-command-palette"' in html
    assert "STORAGE_KEY" in js
    assert "WORKBENCH_MODE_KEY" in js
    assert "WORKSPACE_PRESETS_KEY" in js
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
    assert "message-attachments" in js
    assert "message-attachment-preview" in js
    assert "CONTEXT_PREFS_KEY" in js
    assert 'id="session-search"' in html
    assert 'id="export-chat"' in html
    assert 'id="send-codex"' in html
    assert "normalizeSessionMeta" in js
    assert "setSessionFilter" in js
    assert "toggleCurrentSessionMeta" in js
    assert "openCurrentSessionNote" in js
    assert "attachCurrentSessionNote" in js
    assert "compareSessionsForSidebar" in js
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
    assert 'id="create-checkpoint"' in html
    assert 'id="session-checkpoints"' in html
    assert 'id="session-turns"' in html
    assert 'id="session-timeline"' in html
    assert 'id="timeline-filters"' in html
    assert 'id="session-operations"' in html
    assert 'id="session-events"' in html
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
    assert 'id="native-terminal"' in html
    assert 'id="native-terminal-file"' in html
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
    assert 'id="git-prs"' in html
    assert 'id="git-issues"' in html
    assert 'id="git-pr-view"' in html
    assert 'id="git-pr-checkout"' in html
    assert 'id="git-pr-diff"' in html
    assert 'id="git-pr-create"' in html
    assert 'id="git-issue-view"' in html
    assert 'id="git-issue-create"' in html
    assert 'id="git-attach"' in html
    assert 'id="github-target"' in html
    assert 'id="github-title"' in html
    assert 'id="git-output"' in html
    assert 'id="refresh-approvals"' in html
    assert 'id="apply-pending-approvals"' in html
    assert 'id="reject-pending-approvals"' in html
    assert 'id="self-improve-active"' in html
    assert 'id="queue-suggested-command"' in html
    assert 'id="queue-edit-proposal"' in html
    assert 'id="approvals"' in html
    assert 'id="remember-note"' in html
    assert 'id="index-note"' in html
    assert 'id="chat-about-note"' in html
    assert 'id="obsidian-auto-remember"' in html
    assert 'id="obsidian-auto-index"' in html
    assert 'id="sync-session-note"' in html
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
    assert "/api/terminal/native" in js
    assert "openWorkspaceFile" in js
    assert "mapTerminalKey" in js
    assert "renderEditorTabs" in js
    assert "renderTerminalSessions" in js
    assert "appendSessionOperation" in js
    assert "renderSessionOperations" in js
    assert "renderSessionCheckpoints" in js
    assert "renderSessionTimeline" in js
    assert "renderSessionTurns" in js
    assert "restoreSessionTurn" in js
    assert "setTimelineFilter" in js
    assert "classifyTimelineItem" in js
    assert "createSessionCheckpoint" in js
    assert "restoreSessionCheckpoint" in js
    assert "renderWorkspaceSearchResults" in js
    assert "renderTaskAssist" in js
    assert "renderBatchProposal" in js
    assert "handleSlashCommand" in js
    assert "submitWorkspaceChatPrompt" in js
    assert "scheduleTerminalSnapshotSave" in js
    assert "pending_attachments" in js
    assert "pending_task_assist" in js
    assert "terminal_tail" in js
    assert "rememberCurrentNote" in js
    assert "indexCurrentNote" in js
    assert "prepareChatFromCurrentNote" in js
    assert "syncCurrentSessionNoteToObsidian" in js
    assert "openNativeLinuxTerminal" in js
    assert "openNativeLinuxTerminalForActiveFile" in js
    assert "runTerminalCommandFromInput" in js
    assert "renderRecentFiles" in js
    assert "renderSlashCommands" in js
    assert "loadWorkbenchMode" in js
    assert "loadWorkspacePresets" in js
    assert "applyWorkspacePresetForCurrent" in js
    assert "saveWorkspacePreset" in js
    assert "resolveAdaptiveModel" in js
    assert "syncAdaptiveModel" in js
    assert "QUALITY_MODEL_MAP" in js
    assert "setWorkbenchMode" in js
    assert "preparePromptForActiveFile" in js
    assert "preparePromptForTerminalDebug" in js
    assert "preparePromptForCreateFile" in js
    assert "preparePromptForNextStep" in js
    assert "startGettingStartedFlow" in js
    assert "ensureStarterTerminalReady" in js
    assert "persistMission(" in js
    assert "buildEmptySessionBriefing" in js
    assert "Comece de um destes jeitos:" in js
    assert "openOnboardingWizard" in js
    assert "submitOnboardingWizard" in js
    assert "shouldOpenOnboardingWizard" in js
    assert "Assistente guiado de inicio" in js
    assert "renderStarterReadiness" in js
    assert "loadStarterContext" in js
    assert "renderStarterContext" in js
    assert "Ultimo comando" in js
    assert "Ultimo erro" in js
    assert "Diagnosticar erro" in js
    assert "Retomar trabalho" in js
    assert "buildStarterResumeAction" in js
    assert "executeStarterResumeAction" in js
    assert "/delegate -> usa o prompt atual para gerar diff/comando e enfileirar acoes" in js
    assert "buildMissionModel" in js
    assert "buildMissionActions" in js
    assert "buildMissionBriefingText" in js
    assert "buildMissionPrompt" in js
    assert "renderMissionControl" in js
    assert "normalizeMissionPayload" in js
    assert "syncMissionInputs" in js
    assert "persistMissionFromInputs" in js
    assert "currentMission" in js
    assert "currentTasks" in js
    assert "currentEvents" in js
    assert "createSessionTaskFromInputs" in js
    assert "updateSessionTask" in js
    assert "renderTaskBoard" in js
    assert "renderEventStream" in js
    assert "nextTaskPhase" in js
    assert "buildCommandPaletteItems" in js
    assert "getFilteredCommandPaletteItems" in js
    assert "openCommandPalette" in js
    assert "closeCommandPalette" in js
    assert "moveCommandPaletteSelection" in js
    assert "executeSelectedCommandPaletteItem" in js
    assert "renderCommandPaletteResults" in js
    assert "renderWorkbenchStatus" in js
    assert "renderCommandHistory" in js
    assert "trackCommandHistory" in js
    assert "renderGitOutput" in js
    assert "startSessionReplay" in js
    assert "toggleReplayPlayback" in js
    assert "replayNextMessage" in js
    assert "renderReplayStatus" in js
    assert "runGitCommand" in js
    assert "attachGitContextToChat" in js
    assert "formatMessageMetadata" in js
    assert "latestGitContext" in js
    assert "renderApprovals" in js
    assert "queueApproval" in js
    assert "queueGitHubApproval" in js
    assert "readGitHubTarget" in js
    assert "readGitHubTitle" in js
    assert "buildGitHubBody" in js
    assert "promptGitHubAction" in js
    assert "actOnApproval" in js
    assert "runSelfImproveActive" in js
    assert "queueSuggestedCommandApproval" in js
    assert "queueEditProposalApproval" in js
    assert "/api/terminal/run" in js
    assert '"/git-status"' in js
    assert '"/git-diff"' in js
    assert '"/git-log"' in js
    assert '"/git-prs"' in js
    assert '"/git-issues"' in js
    assert '"/gh-pr-view"' in js
    assert '"/gh-pr-checkout"' in js
    assert '"/gh-pr-diff"' in js
    assert '"/gh-pr-create"' in js
    assert '"/gh-issue-view"' in js
    assert '"/gh-issue-create"' in js
    assert '"/linux-terminal"' in js
    assert '"/linux-terminal-file"' in js
    assert '"/git-attach"' in js
    assert '"/mode build"' in js
    assert '"/explain-file"' in js
    assert '"/debug-terminal"' in js
    assert 'commandPaletteOpen' in js
    assert '"/queue-command"' in js
    assert '"/queue-edit"' in js
    assert '"/self-review"' in js
    assert "/api/chat/sessions/${currentSessionId}/approvals" in js
    assert "/api/chat/sessions/${currentSessionId}/approvals/batch" in js
    assert "/api/chat/sessions/${currentSessionId}/note" in js
    assert "/api/chat/sessions/${currentSessionId}/note/sync" in js
    assert "/api/chat/sessions/${sessionId}/workspace-turn" in js
    assert "/api/chat/sessions/${sessionId}/workspace-turn/stream" in js
    assert "/api/chat/sessions/${currentSessionId}/turns/${turnId}/restore" in js
    assert "actOnPendingApprovals" in js
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
    assert "session-checkpoint-card" in css
    assert "session-timeline-card" in css
    assert "session-turn-card" in css
    assert "session-turn-actions" in css
    assert "session-item-actions" in css
    assert "session-item-action" in css
    assert "timeline-filters" in css
    assert "timeline-filter.active" in css
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
    assert "git-form" in css
    assert "git-output" in css
    assert "message-meta" in css
    assert "replay-toolbar" in css
    assert "replay-status" in css
    assert "approval-shell" in css
    assert "approval-header" in css
    assert "approvals-list" in css
    assert "approval-card" in css
    assert "approval-card-preview" in css
    assert "workbench-topbar" in css
    assert "workbench-mode-shell" in css
    assert "workbench-modes" in css
    assert "workbench-status" in css
    assert "mission-control-shell" in css
    assert ".starter-shell" in css
    assert ".panel-workspace-preset" in css
    assert ".workspace-preset-row" in css
    assert ".workspace-preset-actions" in css
    assert ".starter-actions" in css
    assert ".starter-readiness" in css
    assert ".starter-readiness-card" in css
    assert ".starter-context" in css
    assert ".starter-context-card" in css
    assert ".onboarding-wizard-dialog" in css
    assert ".onboarding-wizard-form" in css
    assert "mission-control-header" in css
    assert "mission-status" in css
    assert "mission-card" in css
    assert "mission-next-actions" in css
    assert "mission-action" in css
    assert "mission-editor-shell" in css
    assert "mission-editor-row" in css
    assert "#mission-next-steps-input" in css
    assert "task-board-shell" in css
    assert "task-board-creator" in css
    assert "task-board" in css
    assert "task-card" in css
    assert "task-card-actions" in css
    assert "event-stream-shell" in css
    assert "session-events" in css
    assert "session-event-card" in css
    assert "status-pill" in css
    assert "codex-prompt-dock" in css
    assert "command-palette" in css
    assert "command-palette-dialog" in css
    assert "command-palette-results" in css
    assert "command-palette-item" in css
    assert "command-palette-empty" in css
    assert "data-workbench-mode=\"chat\"" in css
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
