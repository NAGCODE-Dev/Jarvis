const modelSelect = document.querySelector("#model");
const workspaceInput = document.querySelector("#workspace");
const messagesEl = document.querySelector("#messages");
const sessionsEl = document.querySelector("#sessions");
const form = document.querySelector("#chat-form");
const promptEl = document.querySelector("#prompt");
const statusEl = document.querySelector("#status");
const replaySessionButton = document.querySelector("#replay-session");
const replayToggleButton = document.querySelector("#replay-toggle");
const replayNextButton = document.querySelector("#replay-next");
const replayStopButton = document.querySelector("#replay-stop");
const replayStatusEl = document.querySelector("#replay-status");
const missionStatusEl = document.querySelector("#mission-status");
const missionNextActionsEl = document.querySelector("#mission-next-actions");
const refreshMissionControlButton = document.querySelector("#refresh-mission-control");
const missionBriefingButton = document.querySelector("#mission-briefing");
const missionObjectiveInputEl = document.querySelector("#mission-objective");
const missionStatusInputEl = document.querySelector("#mission-status-input");
const missionNextStepsInputEl = document.querySelector("#mission-next-steps-input");
const saveMissionButton = document.querySelector("#save-mission");
const taskTitleEl = document.querySelector("#task-title");
const taskPhaseEl = document.querySelector("#task-phase");
const createTaskButton = document.querySelector("#create-task");
const taskBoardEl = document.querySelector("#task-board");
const workbenchStatusEl = document.querySelector("#workbench-status");
const workbenchModeButtons = Array.from(document.querySelectorAll(".workbench-mode"));
const attachmentsEl = document.querySelector("#attachments");
const clearButton = document.querySelector("#clear-chat");
const newChatButton = document.querySelector("#new-chat");
const deleteButton = document.querySelector("#delete-chat");
const installButton = document.querySelector("#install-app");
const contextActiveFileCheckbox = document.querySelector("#ctx-active-file");
const contextOpenTabsCheckbox = document.querySelector("#ctx-open-tabs");
const contextTerminalCheckbox = document.querySelector("#ctx-terminal");
const contextSearchCheckbox = document.querySelector("#ctx-search");
const composerContextPreviewEl = document.querySelector("#composer-context-preview");
const attachFileButton = document.querySelector("#attach-file");
const fileInput = document.querySelector("#file-input");
const sessionTitleEl = document.querySelector("#session-title");
const sessionSearchEl = document.querySelector("#session-search");
const sessionFiltersEl = document.querySelector("#session-filters");
const sessionFilterButtons = Array.from(document.querySelectorAll(".session-filter"));
const pinSessionButton = document.querySelector("#pin-session");
const archiveSessionButton = document.querySelector("#archive-session");
const exportChatButton = document.querySelector("#export-chat");
const promptActiveFileButton = document.querySelector("#prompt-active-file");
const promptTerminalDebugButton = document.querySelector("#prompt-terminal-debug");
const promptCreateFileButton = document.querySelector("#prompt-create-file");
const promptNextStepButton = document.querySelector("#prompt-next-step");
const quickTargetPathEl = document.querySelector("#quick-target-path");
const quickGoalEl = document.querySelector("#quick-goal");
const quickOpenTargetButton = document.querySelector("#quick-open-target");
const quickBuildPromptButton = document.querySelector("#quick-build-prompt");
const quickStageTaskButton = document.querySelector("#quick-stage-task");
const quickFlowButtons = Array.from(document.querySelectorAll(".quick-flow-button"));
const openCommandPaletteButton = document.querySelector("#open-command-palette");
const commandPaletteEl = document.querySelector("#command-palette");
const commandPaletteBackdropEl = document.querySelector("#command-palette-backdrop");
const commandPaletteInputEl = document.querySelector("#command-palette-input");
const commandPaletteResultsEl = document.querySelector("#command-palette-results");
const closeCommandPaletteButton = document.querySelector("#close-command-palette");
const quickActionButtons = Array.from(document.querySelectorAll(".quick-action"));
const refreshFilesButton = document.querySelector("#refresh-files");
const newFileButton = document.querySelector("#new-file");
const newFolderButton = document.querySelector("#new-folder");
const openPathButton = document.querySelector("#open-path");
const attachOpenFileButton = document.querySelector("#attach-open-file");
const workspaceSearchInput = document.querySelector("#workspace-search");
const runWorkspaceSearchButton = document.querySelector("#run-workspace-search");
const clearWorkspaceSearchButton = document.querySelector("#clear-workspace-search");
const workspaceSearchResultsEl = document.querySelector("#workspace-search-results");
const workspaceFilesEl = document.querySelector("#workspace-files");
const refreshOperationsButton = document.querySelector("#refresh-operations");
const createCheckpointButton = document.querySelector("#create-checkpoint");
const sessionOperationsEl = document.querySelector("#session-operations");
const sessionCheckpointsEl = document.querySelector("#session-checkpoints");
const sessionTimelineFiltersEl = document.querySelector("#timeline-filters");
const sessionTimelineFilterButtons = Array.from(document.querySelectorAll(".timeline-filter"));
const sessionTimelineEl = document.querySelector("#session-timeline");
const sessionEventsEl = document.querySelector("#session-events");
const editorPathEl = document.querySelector("#editor-path");
const editorTabsEl = document.querySelector("#editor-tabs");
const editorInstructionEl = document.querySelector("#editor-instruction");
const editorSelectionEl = document.querySelector("#editor-selection");
const runTaskAssistButton = document.querySelector("#run-task-assist");
const runTaskCycleButton = document.querySelector("#run-task-cycle");
const runSuggestedCommandButton = document.querySelector("#run-suggested-command");
const editorTaskOutputEl = document.querySelector("#editor-task-output");
const editorBatchOutputEl = document.querySelector("#editor-batch-output");
const editorBatchProposalsEl = document.querySelector("#editor-batch-proposals");
const editorDiffEl = document.querySelector("#editor-diff");
const editorHunksEl = document.querySelector("#editor-hunks");
const fileEditorEl = document.querySelector("#file-editor");
const saveFileButton = document.querySelector("#save-file");
const askJarvisEditButton = document.querySelector("#ask-jarvis-edit");
const askJarvisBatchEditButton = document.querySelector("#ask-jarvis-batch-edit");
const applyProposalButton = document.querySelector("#apply-proposal");
const applyBatchProposalButton = document.querySelector("#apply-batch-proposal");
const saveAllFilesButton = document.querySelector("#save-all-files");
const attachOpenTabsButton = document.querySelector("#attach-open-tabs");
const runSelectionButton = document.querySelector("#run-selection");
const renameFileButton = document.querySelector("#rename-file");
const deleteFileButton = document.querySelector("#delete-file");
const terminalCwdEl = document.querySelector("#terminal-cwd");
const terminalSessionsEl = document.querySelector("#terminal-sessions");
const terminalCommandEl = document.querySelector("#terminal-command");
const runTerminalCommandButton = document.querySelector("#run-terminal-command");
const sendTerminalCommandButton = document.querySelector("#send-terminal-command");
const cdFileDirButton = document.querySelector("#cd-file-dir");
const attachTerminalContextButton = document.querySelector("#attach-terminal-context");
const askTerminalContextButton = document.querySelector("#ask-terminal-context");
const planTerminalContextButton = document.querySelector("#plan-terminal-context");
const newTerminalButton = document.querySelector("#new-terminal");
const nativeTerminalButton = document.querySelector("#native-terminal");
const nativeTerminalFileButton = document.querySelector("#native-terminal-file");
const closeTerminalButton = document.querySelector("#close-terminal");
const restartTerminalButton = document.querySelector("#restart-terminal");
const interruptTerminalButton = document.querySelector("#interrupt-terminal");
const clearTerminalViewButton = document.querySelector("#clear-terminal-view");
const terminalOutputEl = document.querySelector("#terminal-output");
const rememberNoteButton = document.querySelector("#remember-note");
const indexNoteButton = document.querySelector("#index-note");
const chatAboutNoteButton = document.querySelector("#chat-about-note");
const obsidianStatusEl = document.querySelector("#obsidian-status");
const obsidianAutoRememberCheckbox = document.querySelector("#obsidian-auto-remember");
const obsidianAutoIndexCheckbox = document.querySelector("#obsidian-auto-index");
const recentFilesEl = document.querySelector("#recent-files");
const clearRecentFilesButton = document.querySelector("#clear-recent-files");
const slashCommandsEl = document.querySelector("#slash-commands");
const commandHistoryEl = document.querySelector("#command-history");
const clearCommandHistoryButton = document.querySelector("#clear-command-history");
const gitStatusButton = document.querySelector("#git-status");
const gitDiffButton = document.querySelector("#git-diff");
const gitLogButton = document.querySelector("#git-log");
const gitGithubButton = document.querySelector("#git-github");
const gitPrsButton = document.querySelector("#git-prs");
const gitIssuesButton = document.querySelector("#git-issues");
const gitPrViewButton = document.querySelector("#git-pr-view");
const gitPrCheckoutButton = document.querySelector("#git-pr-checkout");
const gitPrDiffButton = document.querySelector("#git-pr-diff");
const gitPrCreateButton = document.querySelector("#git-pr-create");
const gitIssueViewButton = document.querySelector("#git-issue-view");
const gitIssueCreateButton = document.querySelector("#git-issue-create");
const gitAttachButton = document.querySelector("#git-attach");
const gitOutputEl = document.querySelector("#git-output");
const githubTargetInput = document.querySelector("#github-target");
const githubTitleInput = document.querySelector("#github-title");
const refreshApprovalsButton = document.querySelector("#refresh-approvals");
const selfImproveActiveButton = document.querySelector("#self-improve-active");
const queueSuggestedCommandButton = document.querySelector("#queue-suggested-command");
const queueEditProposalButton = document.querySelector("#queue-edit-proposal");
const approvalsEl = document.querySelector("#approvals");
const template = document.querySelector("#message-template");

let installPrompt = null;
let currentSessionId = null;
let messages = [];
let pendingAttachments = [];
let allSessions = [];
let currentSessionOperations = [];
let currentSessionCheckpoints = [];
let currentSessionMeta = { pinned: false, archived: false };
let currentSessionFilter = "active";
let dragDepth = 0;
let workspaceTree = null;
let workspaceSearchResults = [];
let currentOpenFilePath = null;
let openEditors = [];
let pendingEditProposal = null;
let pendingBatchProposal = null;
let pendingTaskAssist = null;
let terminalSessions = [];
let terminalSessionId = null;
let terminalPollTimer = null;
let terminalBuffer = "";
let terminalBuffers = {};
let editorSelection = null;
let recentFiles = [];
let commandHistory = [];
let latestGitContext = "";
let currentApprovals = [];
let currentMission = null;
let currentTasks = [];
let currentEvents = [];
let currentSessionUiState = null;
let sessionUiStateSaveTimer = null;
let restoringSessionUiState = false;
let replayMode = false;
let replayPlaying = false;
let replayIndex = 0;
let replayTimer = null;
let replaySourceMessages = [];
let replayStartOffset = 0;
let replayOriginLabel = "sessão inteira";
let currentTimelineFilter = "all";
let workbenchMode = "chat";
let quickFlowMode = "create";
let commandPaletteOpen = false;
let commandPaletteIndex = 0;
let commandPaletteItems = [];
const STORAGE_KEY = "jarvis-pwa-current-session-id";
const QUICK_FLOW_MODE_KEY = "jarvis-pwa-quick-flow-mode";
const CONTEXT_PREFS_KEY = "jarvis-pwa-context-prefs";
const RECENT_FILES_KEY = "jarvis-pwa-recent-files";
const COMMAND_HISTORY_KEY = "jarvis-pwa-command-history";
const OBSIDIAN_PREFS_KEY = "jarvis-pwa-obsidian-prefs";
const WORKBENCH_MODE_KEY = "jarvis-pwa-workbench-mode";
const SLASH_COMMANDS = [
  { label: "/help", mode: "run", value: "/help" },
  { label: "/open", mode: "fill", value: "/open apps/web/app.js" },
  { label: "/search", mode: "fill", value: "/search terminal" },
  { label: "/run", mode: "fill", value: "/run pytest -q" },
  { label: "/new", mode: "fill", value: "/new notes/tarefa.md" },
  { label: "/save-all", mode: "run", value: "/save-all" },
  { label: "/attach-tabs", mode: "run", value: "/attach-tabs" },
  { label: "/run-selection", mode: "run", value: "/run-selection" },
  { label: "/remember-note", mode: "run", value: "/remember-note" },
  { label: "/index-note", mode: "run", value: "/index-note" },
  { label: "/chat-note", mode: "run", value: "/chat-note" },
  { label: "/attach active", mode: "run", value: "/attach active" },
  { label: "/git-status", mode: "run", value: "/git-status" },
  { label: "/git-diff", mode: "run", value: "/git-diff" },
  { label: "/git-log", mode: "run", value: "/git-log" },
  { label: "/git-prs", mode: "run", value: "/git-prs" },
  { label: "/git-issues", mode: "run", value: "/git-issues" },
  { label: "/gh-pr-view", mode: "fill", value: "/gh-pr-view 123" },
  { label: "/gh-pr-checkout", mode: "fill", value: "/gh-pr-checkout 123" },
  { label: "/gh-pr-diff", mode: "fill", value: "/gh-pr-diff 123" },
  { label: "/gh-pr-create", mode: "fill", value: "/gh-pr-create melhorar-fluxo-do-jarvis" },
  { label: "/gh-issue-view", mode: "fill", value: "/gh-issue-view 123" },
  { label: "/gh-issue-create", mode: "fill", value: "/gh-issue-create corrigir-lentidao-no-chat" },
  { label: "/linux-terminal", mode: "run", value: "/linux-terminal" },
  { label: "/linux-terminal-file", mode: "run", value: "/linux-terminal-file" },
  { label: "/attach-terminal", mode: "run", value: "/attach-terminal" },
  { label: "/fix-terminal", mode: "run", value: "/fix-terminal" },
  { label: "/build-file", mode: "fill", value: "/build-file apps/web/new_panel.js :: criar um painel novo e funcional" },
  { label: "/git-attach", mode: "run", value: "/git-attach" },
  { label: "/mode build", mode: "run", value: "/mode build" },
  { label: "/explain-file", mode: "run", value: "/explain-file" },
  { label: "/debug-terminal", mode: "run", value: "/debug-terminal" },
  { label: "/queue-command", mode: "run", value: "/queue-command" },
  { label: "/queue-edit", mode: "run", value: "/queue-edit" },
  { label: "/self-review", mode: "run", value: "/self-review" },
  { label: "/focus terminal", mode: "run", value: "/focus terminal" },
];

bootstrap().catch((error) => {
  statusEl.textContent = `Erro ao inicializar: ${error.message}`;
});

window.addEventListener("keydown", async (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    if (commandPaletteOpen) {
      closeCommandPalette();
    } else {
      openCommandPalette();
    }
    return;
  }
  if (event.key === "Escape" && commandPaletteOpen) {
    event.preventDefault();
    closeCommandPalette();
  }
});

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  installPrompt = event;
  installButton.classList.remove("hidden");
});

installButton.addEventListener("click", async () => {
  if (!installPrompt) return;
  installPrompt.prompt();
  await installPrompt.userChoice;
  installPrompt = null;
  installButton.classList.add("hidden");
});

clearButton.addEventListener("click", async () => {
  if (!currentSessionId) return;
  await api(`/api/chat/sessions/${currentSessionId}`, {
    method: "PUT",
    body: JSON.stringify({
      messages: [],
      model: modelSelect.value,
      workspace: workspaceInput.value.trim() || null,
    }),
  });
  stopSessionReplay({ render: false });
  stopSessionReplay({ render: false });
  messages = [];
  renderMessages();
  await loadSessions();
});

async function loadCurrentSessionOperations() {
  if (!currentSessionId) return;
  const payload = await api(`/api/chat/sessions/${currentSessionId}`);
  currentSessionOperations = payload.session.operations || [];
  currentSessionCheckpoints = payload.session.checkpoints || [];
  currentApprovals = payload.session.approvals || [];
  currentMission = payload.session.mission || null;
  currentTasks = payload.session.tasks || [];
  currentEvents = payload.session.events || [];
  currentSessionUiState = payload.session.ui_state || null;
  currentSessionMeta = normalizeSessionMeta(payload.session.meta);
  syncSessionMetaControls();
  renderSessionOperations();
  renderSessionCheckpoints();
  renderSessionTimeline();
  renderApprovals();
  renderEventStream();
  renderMissionControl();
}

async function loadCurrentSessionApprovals() {
  if (!currentSessionId) return;
  const payload = await api(`/api/chat/sessions/${currentSessionId}`);
  currentApprovals = payload.session.approvals || [];
  currentSessionMeta = normalizeSessionMeta(payload.session.meta);
  syncSessionMetaControls();
  renderApprovals();
  renderEventStream();
  renderMissionControl();
}

function renderEventStream() {
  if (!sessionEventsEl) return;
  sessionEventsEl.innerHTML = "";
  if (!currentEvents.length) {
    sessionEventsEl.textContent = "Nenhum evento emitido ainda.";
    return;
  }
  for (const item of [...currentEvents].reverse().slice(0, 24)) {
    const card = document.createElement("div");
    card.className = "session-event-card";
    const payloadText = Object.entries(item.payload || {})
      .filter(([key]) => key !== "source")
      .map(([key, value]) => `${key}: ${value}`)
      .join(" | ");
    card.textContent = [item.type || "event", payloadText, item.created_at].filter(Boolean).join("\n");
    sessionEventsEl.appendChild(card);
  }
}

function setTimelineFilter(filter) {
  const normalized = ["all", "checkpoint", "operation", "event", "file", "terminal", "approval", "task"].includes(filter) ? filter : "all";
  currentTimelineFilter = normalized;
  sessionTimelineFilterButtons.forEach((button) => {
    button.classList.toggle("active", (button.dataset.timelineFilter || "all") === normalized);
  });
  renderSessionTimeline();
}

function classifyTimelineItem(item) {
  if (item.kind === "checkpoint") return "checkpoint";
  if (item.kind === "event") {
    const type = String(item.event_type || item.title || "").toLowerCase();
    if (type.includes("task")) return "task";
    if (type.includes("approval")) return "approval";
    if (type.includes("command")) return "terminal";
    if (type.includes("workspace")) return "file";
    return "event";
  }
  const title = [item.title, item.detail].filter(Boolean).join(" ").toLowerCase();
  if (title.includes("approval")) return "approval";
  if (title.includes("terminal") || title.includes("comando") || title.includes("bash") || title.includes("exit_code")) return "terminal";
  if (title.includes("tarefa") || title.includes("task")) return "task";
  if (title.includes("arquivo") || title.includes("diff") || title.includes("workspace") || title.includes("pasta") || title.includes("path")) return "file";
  return item.kind;
}

function renderSessionCheckpoints() {

  if (!sessionCheckpointsEl) return;
  sessionCheckpointsEl.innerHTML = "";
  if (!currentSessionCheckpoints.length) {
    sessionCheckpointsEl.textContent = "Nenhum checkpoint ainda.";
    return;
  }
  for (const checkpoint of [...currentSessionCheckpoints].reverse().slice(0, 12)) {
    const card = document.createElement("div");
    card.className = "session-checkpoint-card";
    const meta = [checkpoint.active_file, checkpoint.created_at].filter(Boolean).join("\n");
    card.innerHTML = `<strong>${escapeHtml(checkpoint.title || "Checkpoint")}</strong><span>${escapeHtml(checkpoint.summary || meta || "checkpoint operacional")}</span>`;

    const actions = document.createElement("div");
    actions.className = "session-checkpoint-actions";

    const restoreButton = document.createElement("button");
    restoreButton.type = "button";
    restoreButton.className = "secondary";
    restoreButton.textContent = "Restaurar";
    restoreButton.addEventListener("click", async () => {
      await restoreSessionCheckpoint(checkpoint.id);
    });

    const replayButton = document.createElement("button");
    replayButton.type = "button";
    replayButton.className = "secondary";
    replayButton.textContent = "Replay daqui";
    replayButton.addEventListener("click", () => {
      startSessionReplay({ fromIndex: checkpoint.message_count || 0, label: checkpoint.title || "checkpoint" });
    });

    actions.append(restoreButton, replayButton);
    card.appendChild(actions);
    sessionCheckpointsEl.appendChild(card);
  }
}

function buildSessionTimelineItems() {
  const operationItems = currentSessionOperations.map((item) => ({
    kind: "operation",
    created_at: item.created_at,
    title: item.title || item.kind || "Operação",
    detail: [item.path, item.command ? `$ ${item.command}` : null, item.detail].filter(Boolean).join("\n"),
  }));
  const eventItems = currentEvents.map((item) => ({
    kind: "event",
    created_at: item.created_at,
    title: item.type || "event",
    event_type: item.type || "event",
    detail: Object.entries(item.payload || {}).filter(([key]) => key !== "source").map(([key, value]) => `${key}: ${value}`).join(" | "),
  }));
  const checkpointItems = currentSessionCheckpoints.map((item) => ({
    kind: "checkpoint",
    created_at: item.created_at,
    title: item.title || "Checkpoint",
    detail: [item.active_file, item.summary, item.source === "auto" ? `origem: ${item.trigger_event || "auto"}` : null].filter(Boolean).join("\n"),
    checkpoint_id: item.id,
    message_count: item.message_count || 0,
  }));
  return [...operationItems, ...eventItems, ...checkpointItems]
    .filter((item) => item.created_at)
    .sort((left, right) => String(right.created_at).localeCompare(String(left.created_at)));
}

function renderSessionTimeline() {
  if (!sessionTimelineEl) return;
  sessionTimelineEl.innerHTML = "";
  const items = buildSessionTimelineItems()
    .filter((item) => currentTimelineFilter === "all" || classifyTimelineItem(item) === currentTimelineFilter || item.kind === currentTimelineFilter)
    .slice(0, 40);
  if (!items.length) {
    sessionTimelineEl.textContent = "Nenhuma atividade ainda para este filtro.";
    return;
  }
  for (const item of items) {
    const category = classifyTimelineItem(item);
    const card = document.createElement("div");
    card.className = `session-timeline-card ${item.kind} ${category}`;
    const title = document.createElement("div");
    title.className = "session-timeline-title";
    title.textContent = `${category} · ${item.title}`;
    const meta = document.createElement("div");
    meta.className = "session-timeline-meta";
    meta.textContent = [item.detail, item.created_at].filter(Boolean).join("\n");
    card.append(title, meta);
    if (item.kind === "checkpoint" && item.checkpoint_id) {
      const actions = document.createElement("div");
      actions.className = "session-timeline-actions";
      const restoreButton = document.createElement("button");
      restoreButton.type = "button";
      restoreButton.className = "secondary";
      restoreButton.textContent = "Restaurar";
      restoreButton.addEventListener("click", async () => {
        await restoreSessionCheckpoint(item.checkpoint_id);
      });
      const replayButton = document.createElement("button");
      replayButton.type = "button";
      replayButton.className = "secondary";
      replayButton.textContent = "Replay daqui";
      replayButton.addEventListener("click", () => {
        startSessionReplay({ fromIndex: item.message_count || 0, label: item.title || "checkpoint" });
      });
      actions.append(restoreButton, replayButton);
      card.appendChild(actions);
    }
    sessionTimelineEl.appendChild(card);
  }
}

function renderSessionOperations() {
  sessionOperationsEl.innerHTML = "";
  if (!currentSessionOperations.length) {
    sessionOperationsEl.textContent = "Nenhum evento operacional ainda.";
    return;
  }
  for (const item of [...currentSessionOperations].reverse().slice(0, 20)) {
    const card = document.createElement("div");
    card.className = "session-operation-card";
    const parts = [item.title || item.kind || "evento"];
    if (item.path) parts.push(item.path);
    if (item.command) parts.push(`$ ${item.command}`);
    if (item.detail) parts.push(item.detail);
    if (item.created_at) parts.push(item.created_at);
    card.textContent = parts.join("\n");
    sessionOperationsEl.appendChild(card);
  }
}

async function appendSessionOperation(operation) {
  if (!currentSessionId) return;
  const payload = await api(`/api/chat/sessions/${currentSessionId}/operations`, {
    method: "POST",
    body: JSON.stringify(operation),
  });
  currentSessionOperations = payload.session.operations || [];
  currentSessionCheckpoints = payload.session.checkpoints || currentSessionCheckpoints;
  renderSessionOperations();
  renderSessionCheckpoints();
  renderSessionTimeline();
  renderEventStream();
  renderMissionControl();
}


newChatButton.addEventListener("click", async () => {
  await createSession();
});

deleteButton.addEventListener("click", async () => {
  if (!currentSessionId) return;
  await api(`/api/chat/sessions/${currentSessionId}`, { method: "DELETE" });
  currentSessionId = null;
  currentSessionMeta = { pinned: false, archived: false };
  sessionTitleEl.value = "";
  persistCurrentSessionId();
  messages = [];
  renderMessages();
  syncSessionMetaControls();
  await loadSessions();
  if (!currentSessionId) {
    await createSession();
  }
});

attachFileButton.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener("change", async () => {
  const files = Array.from(fileInput.files || []);
  if (!files.length) return;
  await queueAttachments(files);
  fileInput.value = "";
  renderAttachments();
});

form.addEventListener("dragenter", (event) => {
  event.preventDefault();
  dragDepth += 1;
  setDropzoneState(true);
});

form.addEventListener("dragover", (event) => {
  event.preventDefault();
  event.dataTransfer.dropEffect = "copy";
});

form.addEventListener("dragleave", (event) => {
  event.preventDefault();
  dragDepth = Math.max(0, dragDepth - 1);
  if (dragDepth === 0) {
    setDropzoneState(false);
  }
});

form.addEventListener("drop", async (event) => {
  event.preventDefault();
  dragDepth = 0;
  setDropzoneState(false);
  const files = Array.from(event.dataTransfer?.files || []);
  if (!files.length) return;
  await queueAttachments(files);
  renderAttachments();
});

sessionSearchEl.addEventListener("input", () => {
  renderSessions(allSessions);
});

for (const button of sessionFilterButtons) {
  button.addEventListener("click", () => {
    setSessionFilter(button.dataset.sessionFilter || "active");
  });
}

pinSessionButton?.addEventListener("click", async () => {
  await toggleCurrentSessionMeta("pinned");
});

archiveSessionButton?.addEventListener("click", async () => {
  await toggleCurrentSessionMeta("archived");
});

exportChatButton.addEventListener("click", () => {
  exportCurrentSessionMarkdown();
});

refreshOperationsButton.addEventListener("click", async () => {
  await loadCurrentSessionOperations();
});

createCheckpointButton.addEventListener("click", async () => {
  await createSessionCheckpoint();
});

for (const button of sessionTimelineFilterButtons) {
  button.addEventListener("click", () => {
    setTimelineFilter(button.dataset.timelineFilter || "all");
  });
}

replaySessionButton.addEventListener("click", () => {
  startSessionReplay();
});

replayToggleButton.addEventListener("click", () => {
  toggleReplayPlayback();
});

replayNextButton.addEventListener("click", () => {
  replayNextMessage();
});

replayStopButton.addEventListener("click", () => {
  stopSessionReplay();
});

for (const button of workbenchModeButtons) {
  button.addEventListener("click", () => {
    setWorkbenchMode(button.dataset.mode || "chat");
  });
}

promptActiveFileButton.addEventListener("click", () => {
  preparePromptForActiveFile();
});

promptTerminalDebugButton.addEventListener("click", () => {
  preparePromptForTerminalDebug();
});

promptCreateFileButton.addEventListener("click", async () => {
  await preparePromptForCreateFile();
});

promptNextStepButton.addEventListener("click", () => {
  preparePromptForNextStep();
});

quickOpenTargetButton.addEventListener("click", async () => {
  await openQuickFlowTarget();
});

quickBuildPromptButton.addEventListener("click", async () => {
  await runQuickFlowPrompt();
});

quickStageTaskButton.addEventListener("click", async () => {
  await stageQuickFlowInEditor();
});

for (const button of quickFlowButtons) {
  button.addEventListener("click", async () => {
    await setQuickFlowMode(button.dataset.quickFlow || "create");
  });
}

refreshMissionControlButton.addEventListener("click", () => {
  renderMissionControl();
  announceAssistantMessage(buildMissionBriefingText());
});

missionBriefingButton.addEventListener("click", () => {
  primePrompt(buildMissionPrompt(), { mode: "chat", activeFile: Boolean(getCurrentEditor()), terminal: true, search: true });
});

saveMissionButton.addEventListener("click", async () => {
  await persistMissionFromInputs();
});

createTaskButton.addEventListener("click", async () => {
  await createSessionTaskFromInputs();
});

openCommandPaletteButton.addEventListener("click", () => {
  openCommandPalette();
});

closeCommandPaletteButton.addEventListener("click", () => {
  closeCommandPalette();
});

commandPaletteBackdropEl.addEventListener("click", () => {
  closeCommandPalette();
});

commandPaletteInputEl.addEventListener("input", () => {
  commandPaletteIndex = 0;
  renderCommandPaletteResults();
});

commandPaletteInputEl.addEventListener("keydown", async (event) => {
  if (event.key === "ArrowDown") {
    event.preventDefault();
    moveCommandPaletteSelection(1);
    return;
  }
  if (event.key === "ArrowUp") {
    event.preventDefault();
    moveCommandPaletteSelection(-1);
    return;
  }
  if (event.key === "Enter") {
    event.preventDefault();
    await executeSelectedCommandPaletteItem();
    return;
  }
  if (event.key === "Escape") {
    event.preventDefault();
    closeCommandPalette();
  }
});

refreshFilesButton.addEventListener("click", () => {
  loadWorkspaceTree().catch((error) => {
    workspaceFilesEl.textContent = `Erro ao carregar workspace: ${error.message}`;
  });
});

clearRecentFilesButton.addEventListener("click", () => {
  recentFiles = [];
  persistRecentFiles();
  renderRecentFiles();
});

clearCommandHistoryButton.addEventListener("click", () => {
  commandHistory = [];
  persistCommandHistory();
  renderCommandHistory();
});

gitStatusButton.addEventListener("click", async () => {
  await loadGitContext("status");
});

gitDiffButton.addEventListener("click", async () => {
  await loadGitContext("diff");
});

gitLogButton.addEventListener("click", async () => {
  await loadGitContext("log");
});

gitGithubButton.addEventListener("click", async () => {
  await loadGitContext("github");
});

gitPrsButton.addEventListener("click", async () => {
  await loadGitContext("prs");
});

gitIssuesButton.addEventListener("click", async () => {
  await loadGitContext("issues");
});

gitPrViewButton.addEventListener("click", async () => {
  await promptGitHubAction("pr-view");
});

gitPrCheckoutButton.addEventListener("click", async () => {
  await promptGitHubAction("pr-checkout");
});

gitPrDiffButton.addEventListener("click", async () => {
  await promptGitHubAction("pr-diff");
});

gitPrCreateButton.addEventListener("click", async () => {
  await promptGitHubAction("pr-create");
});

gitIssueViewButton.addEventListener("click", async () => {
  await promptGitHubAction("issue-view");
});

gitIssueCreateButton.addEventListener("click", async () => {
  await promptGitHubAction("issue-create");
});

gitAttachButton.addEventListener("click", async () => {
  await attachGitContextToChat();
});

refreshApprovalsButton.addEventListener("click", async () => {
  await loadCurrentSessionApprovals();
});

selfImproveActiveButton.addEventListener("click", async () => {
  await runSelfImproveActive();
});

queueSuggestedCommandButton.addEventListener("click", async () => {
  await queueSuggestedCommandApproval();
});

queueEditProposalButton.addEventListener("click", async () => {
  await queueEditProposalApproval();
});

obsidianAutoRememberCheckbox.addEventListener("change", () => {
  persistObsidianPrefs();
  renderObsidianStatus();
});

obsidianAutoIndexCheckbox.addEventListener("change", () => {
  persistObsidianPrefs();
  renderObsidianStatus();
});

newFileButton.addEventListener("click", async () => {
  const path = window.prompt("Novo arquivo relativo ao workspace:", "notes/todo.md");
  if (!path) return;
  await api(`/api/workspace/file?session_id=${encodeURIComponent(currentSessionId || "")}`, {
    method: "POST",
    body: JSON.stringify({ path: path.trim(), content: "" }),
  });
  await loadWorkspaceTree();
  await openWorkspaceFile(path.trim());
  await appendSessionOperation({ kind: "file_create", title: `Criou ${path.trim()}`, path: path.trim(), detail: "arquivo criado no workspace" });
});

newFolderButton.addEventListener("click", async () => {
  const path = window.prompt("Nova pasta relativa ao workspace:", "notes");
  if (!path) return;
  await api(`/api/workspace/directory?session_id=${encodeURIComponent(currentSessionId || "")}`, {
    method: "POST",
    body: JSON.stringify({ path: path.trim() }),
  });
  await loadWorkspaceTree();
  await appendSessionOperation({ kind: "directory_create", title: `Criou pasta ${path.trim()}`, path: path.trim(), detail: "diretório criado no workspace" });
});

openPathButton.addEventListener("click", async () => {
  const path = window.prompt("Abrir arquivo relativo ao workspace:", currentOpenFilePath || "apps/web/app.js");
  if (!path) return;
  await openWorkspaceFile(path.trim());
  await appendSessionOperation({ kind: "file_open", title: `Abriu ${path.trim()}`, path: path.trim(), detail: "arquivo aberto manualmente" });
});

attachOpenFileButton.addEventListener("click", async () => {
  if (!currentOpenFilePath) return;
  pendingAttachments.push({
    id: `workspace-${currentOpenFilePath}-${Date.now()}`,
    name: currentOpenFilePath,
    content: fileEditorEl.value,
    size: new Blob([fileEditorEl.value]).size,
  });
  renderAttachments();
});

runWorkspaceSearchButton.addEventListener("click", async () => {
  await searchWorkspace();
});

clearWorkspaceSearchButton.addEventListener("click", () => {
  workspaceSearchInput.value = "";
  workspaceSearchResults = [];
  renderWorkspaceSearchResults();
});

workspaceSearchInput.addEventListener("keydown", async (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    await searchWorkspace();
  }
});

for (const checkbox of [
  contextActiveFileCheckbox,
  contextOpenTabsCheckbox,
  contextTerminalCheckbox,
  contextSearchCheckbox,
]) {
  checkbox.addEventListener("change", () => {
    persistContextPrefs();
    renderComposerContextPreview();
  });
}

saveFileButton.addEventListener("click", async () => {
  await saveCurrentEditor();
});

saveAllFilesButton.addEventListener("click", async () => {
  await saveAllEditors();
});

attachOpenTabsButton.addEventListener("click", async () => {
  await attachOpenTabsToChat();
});

runSelectionButton.addEventListener("click", async () => {
  await runEditorSelectionInTerminal();
});

askJarvisEditButton.addEventListener("click", async () => {
  const active = getCurrentEditor();
  const instruction = (editorInstructionEl.value || "").trim();
  if (!active || !instruction) return;
  editorDiffEl.textContent = "Gerando proposta de edição...";
  try {
    const payload = await api("/api/workspace/edit-proposal", {
      method: "POST",
      body: JSON.stringify({
        path: active.path,
        instruction: mergeInstructionWithSelection(instruction),
        model: modelSelect.value,
        content: active.content,
        workspace: workspaceInput.value.trim() || null,
      }),
    });
    pendingEditProposal = payload;
    pendingEditProposal.hunks = (pendingEditProposal.hunks || []).map((hunk) => ({ ...hunk, applied: false }));
    renderEditProposal();
    await appendSessionOperation({ kind: "edit_proposal", title: `Gerou proposta para ${active.path}`, path: active.path, detail: instruction.slice(0, 160) });
  } catch (error) {
    editorDiffEl.textContent = `Erro ao gerar proposta: ${error.message}`;
  }
});

askJarvisBatchEditButton.addEventListener("click", async () => {
  const instruction = (editorInstructionEl.value || "").trim();
  if (!openEditors.length || !instruction) return;
  editorBatchOutputEl.textContent = "Gerando proposta em lote...";
  try {
    const payload = await api("/api/workspace/batch-edit-proposal", {
      method: "POST",
      body: JSON.stringify({
        instruction: mergeInstructionWithSelection(instruction),
        model: modelSelect.value,
        workspace: workspaceInput.value.trim() || null,
        files: openEditors.map((editor) => ({ path: editor.path, content: editor.content })),
      }),
    });
    pendingBatchProposal = {
      ...payload,
      proposals: (payload.proposals || []).map((proposal) => ({
        ...proposal,
        hunks: (proposal.hunks || []).map((hunk) => ({ ...hunk, applied: false })),
      })),
    };
    renderBatchProposal();
    await appendSessionOperation({ kind: "batch_edit_proposal", title: "Gerou proposta em lote", detail: `${openEditors.length} arquivo(s)` });
  } catch (error) {
    editorBatchOutputEl.textContent = `Erro ao gerar lote: ${error.message}`;
  }
});

runTaskAssistButton.addEventListener("click", async () => {
  const active = getCurrentEditor();
  const instruction = (editorInstructionEl.value || "").trim();
  if (!active || !instruction) return;
  editorTaskOutputEl.textContent = "Gerando tarefa operacional...";
  try {
    const payload = await api("/api/workspace/task-assist", {
      method: "POST",
      body: JSON.stringify({
        instruction: mergeInstructionWithSelection(instruction),
        model: modelSelect.value,
        path: active.path,
        content: active.content,
        workspace: workspaceInput.value.trim() || null,
        terminal_output: terminalBuffer.slice(-6000),
      }),
    });
    pendingTaskAssist = payload;
    if (payload.edit_proposal) {
      pendingEditProposal = {
        ...payload.edit_proposal,
        hunks: (payload.edit_proposal.hunks || []).map((hunk) => ({ ...hunk, applied: false })),
      };
    } else {
      pendingEditProposal = null;
    }
    renderTaskAssist();
    renderEditProposal();
    await appendSessionOperation({ kind: "task_assist", title: `Gerou tarefa em ${active.path}`, path: active.path, command: payload.command_result?.command || null, detail: instruction.slice(0, 160) });
  } catch (error) {
    editorTaskOutputEl.textContent = `Erro ao gerar tarefa: ${error.message}`;
  }
});

runTaskCycleButton.addEventListener("click", async () => {
  const active = getCurrentEditor();
  const instruction = (editorInstructionEl.value || "").trim();
  if (!active || !instruction) return;
  editorTaskOutputEl.textContent = "Executando ciclo operacional do Jarvis...";
  try {
    const payload = await api("/api/workspace/task-cycle", {
      method: "POST",
      body: JSON.stringify({
        instruction: mergeInstructionWithSelection(instruction),
        model: modelSelect.value,
        path: active.path,
        content: active.content,
        workspace: workspaceInput.value.trim() || null,
        terminal_output: terminalBuffer.slice(-6000),
        execute_command: true,
      }),
    });
    const finalTask = payload.final || {};
    pendingTaskAssist = {
      ...finalTask,
      initial: payload.initial || null,
      command_result: payload.command_result || null,
      mode: "cycle",
    };
    if (finalTask.edit_proposal) {
      pendingEditProposal = {
        ...finalTask.edit_proposal,
        hunks: (finalTask.edit_proposal.hunks || []).map((hunk) => ({ ...hunk, applied: false })),
      };
    } else {
      pendingEditProposal = null;
    }
    if (payload.command_result?.command || payload.command_result?.output) {
      const commandBlock = [
        "",
        "[jarvis task cycle]",
        payload.command_result?.command ? `$ ${payload.command_result.command}` : "",
        payload.command_result?.output || "",
      ]
        .filter(Boolean)
        .join("\n");
      terminalBuffer += `${commandBlock}\n`;
      if (terminalSessionId) {
        terminalBuffers[terminalSessionId] = terminalBuffer;
      }
      renderTerminal();
    }
    renderTaskAssist();
    renderEditProposal();
    await appendSessionOperation({
      kind: "task_cycle",
      title: `Executou ciclo em ${active.path}`,
      path: active.path,
      command: payload.command_result?.command || null,
      detail: instruction.slice(0, 160),
    });
  } catch (error) {
    editorTaskOutputEl.textContent = `Erro ao executar ciclo: ${error.message}`;
  }
});

runSuggestedCommandButton.addEventListener("click", async () => {
  const command = pendingTaskAssist?.suggested_command?.trim();
  if (!command) return;
  await sendTerminalData(`${command}\n`);
  await appendSessionOperation({
    kind: "suggested_command",
    title: "Executou comando sugerido",
    command,
    path: getCurrentEditor()?.path || null,
    detail: "comando enviado ao terminal pelo painel operacional",
  });
});

applyProposalButton.addEventListener("click", async () => {
  const active = getCurrentEditor();
  if (!active || !pendingEditProposal || pendingEditProposal.path !== active.path) return;
  active.content = pendingEditProposal.proposed_content;
  active.dirty = true;
  if (Array.isArray(pendingEditProposal.hunks)) {
    pendingEditProposal.hunks = pendingEditProposal.hunks.map((hunk) => ({ ...hunk, applied: true }));
  }
  fileEditorEl.value = active.content;
  renderEditorTabs();
  syncEditorHeader();
  renderEditProposal();
  await appendSessionOperation({ kind: "apply_edit", title: `Aplicou proposta em ${active.path}`, path: active.path, detail: "arquivo atualizado com a proposta" });
});

applyBatchProposalButton.addEventListener("click", async () => {
  if (!pendingBatchProposal?.proposals?.length) return;
  const totalFiles = pendingBatchProposal.proposals.length;
  for (const proposal of pendingBatchProposal.proposals) {
    const editor = openEditors.find((item) => item.path === proposal.path);
    if (!editor) continue;
    editor.content = proposal.proposed_content;
    editor.dirty = true;
    if (Array.isArray(proposal.hunks)) {
      proposal.hunks = proposal.hunks.map((hunk) => ({ ...hunk, applied: true }));
    }
    proposal.applied = true;
  }
  const active = getCurrentEditor();
  if (active) {
    fileEditorEl.value = active.content;
  }
  pendingBatchProposal = {
    ...pendingBatchProposal,
    applied: true,
  };
  renderEditorTabs();
  syncEditorHeader();
  renderBatchProposal();
  await appendSessionOperation({ kind: "apply_batch", title: "Aplicou lote completo", detail: `${totalFiles} arquivo(s)` });
});

renameFileButton.addEventListener("click", async () => {
  if (!currentOpenFilePath) return;
  const targetPath = window.prompt("Novo caminho relativo para o arquivo atual:", currentOpenFilePath);
  if (!targetPath || targetPath.trim() === currentOpenFilePath) return;
  await api(`/api/workspace/rename?session_id=${encodeURIComponent(currentSessionId || "")}`, {
    method: "POST",
    body: JSON.stringify({ source_path: currentOpenFilePath, target_path: targetPath.trim() }),
  });
  const previousPath = currentOpenFilePath;
  const active = getCurrentEditor();
  if (active) {
    active.path = targetPath.trim();
  }
  if (pendingEditProposal && pendingEditProposal.path === previousPath) {
    pendingEditProposal.path = targetPath.trim();
  }
  if (pendingBatchProposal?.proposals?.length) {
    pendingBatchProposal.proposals = pendingBatchProposal.proposals.map((proposal) =>
      proposal.path === previousPath
        ? { ...proposal, path: targetPath.trim() }
        : proposal,
    );
  }
  currentOpenFilePath = targetPath.trim();
  renderEditorTabs();
  syncEditorFromState();
  await loadWorkspaceTree();
  await appendSessionOperation({ kind: "file_rename", title: `Renomeou ${previousPath} para ${targetPath.trim()}`, path: targetPath.trim(), detail: "arquivo renomeado" });
});

deleteFileButton.addEventListener("click", async () => {
  if (!currentOpenFilePath) return;
  if (!window.confirm(`Excluir ${currentOpenFilePath}?`)) return;
  await api(`/api/workspace/path?path=${encodeURIComponent(currentOpenFilePath)}&session_id=${encodeURIComponent(currentSessionId || "")}`, {
    method: "DELETE",
  });
  const deletedPath = currentOpenFilePath;
  closeEditor(currentOpenFilePath);
  await loadWorkspaceTree();
  await appendSessionOperation({ kind: "file_delete", title: `Excluiu ${deletedPath}`, path: deletedPath, detail: "arquivo removido do workspace" });
});

restartTerminalButton.addEventListener("click", async () => {
  await restartTerminal();
});

newTerminalButton.addEventListener("click", async () => {
  await createTerminalSession();
});

nativeTerminalButton.addEventListener("click", async () => {
  await openNativeLinuxTerminal();
});

nativeTerminalFileButton.addEventListener("click", async () => {
  await openNativeLinuxTerminalForActiveFile();
});

closeTerminalButton.addEventListener("click", async () => {
  await closeActiveTerminalSession();
});

interruptTerminalButton.addEventListener("click", async () => {
  if (!terminalSessionId) return;
  await api(`/api/terminal/sessions/${terminalSessionId}/signal`, {
    method: "POST",
    body: JSON.stringify({ signal: "int" }),
  });
  await pollTerminalOutputOnce(80);
});

clearTerminalViewButton.addEventListener("click", () => {
  terminalBuffer = "";
  terminalOutputEl.textContent = "";
});

runTerminalCommandButton.addEventListener("click", async () => {
  await runTerminalCommandFromInput();
});

sendTerminalCommandButton.addEventListener("click", async () => {
  await sendTerminalCommandFromInput();
});

cdFileDirButton.addEventListener("click", async () => {
  await jumpTerminalToActiveFileDir();
});

attachTerminalContextButton.addEventListener("click", async () => {
  await attachTerminalSnapshot();
});

askTerminalContextButton.addEventListener("click", async () => {
  await preparePromptForTerminalFix();
});

planTerminalContextButton.addEventListener("click", async () => {
  await createTerminalFollowupTask();
});

rememberNoteButton.addEventListener("click", async () => {
  await rememberCurrentNote();
});

indexNoteButton.addEventListener("click", async () => {
  await indexCurrentNote();
});

chatAboutNoteButton.addEventListener("click", () => {
  prepareChatFromCurrentNote();
});

terminalOutputEl.addEventListener("click", () => {
  terminalOutputEl.focus();
});

terminalCommandEl.addEventListener("keydown", async (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    await runTerminalCommandFromInput();
  }
});

terminalOutputEl.addEventListener("paste", async (event) => {
  if (!terminalSessionId) return;
  event.preventDefault();
  const text = event.clipboardData?.getData("text/plain") || "";
  if (!text) return;
  await sendTerminalData(text);
});

terminalOutputEl.addEventListener("keydown", async (event) => {
  if (!terminalSessionId) return;

  if (event.ctrlKey && event.key.toLowerCase() === "c") {
    event.preventDefault();
    await api(`/api/terminal/sessions/${terminalSessionId}/signal`, {
      method: "POST",
      body: JSON.stringify({ signal: "int" }),
    });
    await pollTerminalOutputOnce(80);
    return;
  }

  const special = mapTerminalKey(event);
  if (special !== null) {
    event.preventDefault();
    await sendTerminalData(special);
    return;
  }

  if (!event.ctrlKey && !event.metaKey && !event.altKey && event.key.length === 1) {
    event.preventDefault();
    await sendTerminalData(event.key);
  }
});

fileEditorEl.addEventListener("keydown", async (event) => {
  if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key.toLowerCase() === "s") {
    event.preventDefault();
    await saveAllEditors();
    return;
  }
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {
    event.preventDefault();
    await saveCurrentEditor();
  }
});

fileEditorEl.addEventListener("select", () => {
  syncEditorSelection();
});

fileEditorEl.addEventListener("click", () => {
  syncEditorSelection();
});

fileEditorEl.addEventListener("keyup", () => {
  syncEditorSelection();
});

editorInstructionEl.addEventListener("keydown", async (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    event.preventDefault();
    if (event.shiftKey) {
      runTaskAssistButton.click();
      return;
    }
    runTaskCycleButton.click();
  }
});

fileEditorEl.addEventListener("input", () => {
  const active = getCurrentEditor();
  if (!active) return;
  active.content = fileEditorEl.value;
  active.dirty = true;
  if (pendingEditProposal && pendingEditProposal.path === active.path) {
    pendingEditProposal = null;
    renderEditProposal();
  }
  if (pendingTaskAssist?.edit_proposal?.path === active.path) {
    pendingTaskAssist = null;
    renderTaskAssist();
  }
  renderEditorTabs();
  syncEditorHeader();
  syncEditorSelection();
});

for (const button of quickActionButtons) {
  button.addEventListener("click", async () => {
    const model = button.dataset.model;
    const prompt = button.dataset.prompt || "";
    if (model) {
      modelSelect.value = model;
      if (currentSessionId) {
        await api(`/api/chat/sessions/${currentSessionId}`, {
          method: "PUT",
          body: JSON.stringify({ model }),
        });
        await loadSessions();
      }
    }
    promptEl.value = prompt;
    promptEl.focus();
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const prompt = promptEl.value.trim();
  if (!prompt || !currentSessionId) return;

  if (prompt.startsWith("/")) {
    const handled = await handleSlashCommand(prompt);
    if (handled) {
      promptEl.value = "";
      return;
    }
  }

  setPending(true);
  try {
    const attachmentPrompt = buildAttachmentPrompt(prompt);
    const response = await streamSessionMessage({
      sessionId: currentSessionId,
      model: modelSelect.value,
      content: attachmentPrompt,
      displayContent: prompt,
      workspace: workspaceInput.value.trim() || null,
      attachments: pendingAttachments.map((attachment) => ({
        id: attachment.id,
        name: attachment.name,
        content: attachment.content,
        size: attachment.size,
      })),
    });
    promptEl.value = "";
    pendingAttachments = [];
    renderAttachments();
    stopSessionReplay({ render: false });
    messages = response.session.messages || [];
    renderMessages();
    await loadSessions();
  } catch (error) {
    stopSessionReplay({ render: false });
    messages = messages.slice(0, Math.max(0, messages.length - 2));
    renderMessages();
    appendMessageElement("assistant", `Erro ao falar com o Jarvis: ${error.message}`);
  } finally {
    setPending(false);
    loadStatus();
  }
});

promptEl.addEventListener("input", () => {
  scheduleSessionUiStateSave();
});

quickTargetPathEl.addEventListener("input", () => {
  scheduleSessionUiStateSave();
});

quickGoalEl.addEventListener("input", () => {
  scheduleSessionUiStateSave();
});

editorInstructionEl.addEventListener("input", () => {
  scheduleSessionUiStateSave();
});

terminalCommandEl.addEventListener("input", () => {
  scheduleSessionUiStateSave();
});

promptEl.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

modelSelect.addEventListener("change", async () => {
  if (!currentSessionId) return;
  await api(`/api/chat/sessions/${currentSessionId}`, {
    method: "PUT",
    body: JSON.stringify({ model: modelSelect.value }),
  });
  await loadSessions();
});

workspaceInput.addEventListener("change", async () => {
  if (!currentSessionId) return;
  await api(`/api/chat/sessions/${currentSessionId}`, {
    method: "PUT",
    body: JSON.stringify({ workspace: workspaceInput.value.trim() || null }),
  });
  await loadSessions();
});
sessionTitleEl.addEventListener("change", async () => {
  if (!currentSessionId) return;
  await api(`/api/chat/sessions/${currentSessionId}`, {
    method: "PUT",
    body: JSON.stringify({ title: sessionTitleEl.value.trim() || "Nova conversa" }),
  });
  await loadSessions();
});

async function bootstrap() {
  loadContextPrefs();
  loadObsidianPrefs();
  loadRecentFiles();
  loadCommandHistory();
  loadWorkbenchMode();
  loadQuickFlowMode();
  renderMessages();
  renderRecentFiles();
  renderMissionControl();
  renderCommandHistory();
  renderGitOutput();
  renderApprovals();
  renderSlashCommands();
  renderObsidianStatus();
  syncQuickFlowUi();
  renderComposerContextPreview();
  renderWorkbenchStatus();
  await loadStatus();
  registerServiceWorker();
  await loadWorkspaceTree();
  await startTerminalSession();
  await loadSessions();
  if (!currentSessionId) {
    await createSession();
  }
  setWorkbenchMode(workbenchMode, { persist: false });
}

async function loadSessions() {
  const payload = await api("/api/chat/sessions");
  allSessions = payload.sessions || [];
  renderSessions(allSessions);
  const preferredId = currentSessionId || localStorage.getItem(STORAGE_KEY);
  if (preferredId && allSessions.some((session) => session.id === preferredId)) {
    await selectSession(preferredId);
    return;
  }
  if (!currentSessionId && allSessions.length) {
    await selectSession(allSessions[0].id);
  }
}

async function createSession() {
  const payload = await api("/api/chat/sessions", {
    method: "POST",
    body: JSON.stringify({
      model: modelSelect.value,
      workspace: workspaceInput.value.trim() || null,
    }),
  });
  currentSessionId = payload.session.id;
  currentMission = payload.session.mission || null;
  currentTasks = payload.session.tasks || [];
  currentEvents = payload.session.events || [];
  currentSessionUiState = payload.session.ui_state || null;
  currentSessionMeta = normalizeSessionMeta(payload.session.meta);
  persistCurrentSessionId();
  messages = [];
  clearSessionWorkspaceState();
  renderMessages();
  await loadSessions();
  await selectSession(currentSessionId);
  currentSessionOperations = [];
  currentSessionCheckpoints = payload.session.checkpoints || [];
  currentApprovals = [];
  currentMission = payload.session.mission || null;
  currentTasks = payload.session.tasks || [];
  currentEvents = payload.session.events || [];
  syncSessionMetaControls();
  renderSessionOperations();
  renderSessionCheckpoints();
  renderSessionTimeline();
  renderApprovals();
  renderEventStream();
}

async function selectSession(sessionId) {
  let payload;
  try {
    payload = await api(`/api/chat/sessions/${sessionId}`);
  } catch {
    currentSessionId = null;
    persistCurrentSessionId();
    await loadSessions();
    if (!currentSessionId) {
      await createSession();
    }
    return;
  }
  const session = payload.session;
  currentSessionId = session.id;
  persistCurrentSessionId();
  stopSessionReplay({ render: false });
  clearSessionWorkspaceState();
  messages = session.messages || [];
  modelSelect.value = session.model || "jarvis-safe";
  workspaceInput.value = session.workspace || "";
  sessionTitleEl.value = session.title || "Nova conversa";
  renderMessages();
  currentSessionOperations = session.operations || [];
  currentSessionCheckpoints = session.checkpoints || [];
  currentApprovals = session.approvals || [];
  currentMission = session.mission || null;
  currentTasks = session.tasks || [];
  currentEvents = session.events || [];
  currentSessionUiState = session.ui_state || null;
  currentSessionMeta = normalizeSessionMeta(session.meta);
  syncSessionMetaControls();
  renderSessionOperations();
  renderSessionCheckpoints();
  renderSessionTimeline();
  renderApprovals();
  highlightSelectedSession();
  await restoreSessionUiState(session);
  renderWorkbenchStatus();
  renderMissionControl();
}

function normalizeSessionMeta(meta = null) {
  return {
    pinned: Boolean(meta?.pinned),
    archived: Boolean(meta?.archived),
  };
}

function normalizeSessionFilter(filter) {
  return ["active", "pinned", "archived", "all"].includes(filter) ? filter : "active";
}

function setSessionFilter(filter) {
  currentSessionFilter = normalizeSessionFilter(filter);
  sessionFilterButtons.forEach((button) => {
    button.classList.toggle("active", (button.dataset.sessionFilter || "active") === currentSessionFilter);
  });
  renderSessions(allSessions);
}

function matchSessionFilter(session) {
  const meta = normalizeSessionMeta(session.meta || session);
  if (currentSessionFilter === "pinned") return meta.pinned && !meta.archived;
  if (currentSessionFilter === "archived") return meta.archived;
  if (currentSessionFilter === "all") return true;
  return !meta.archived;
}

function compareSessionsForSidebar(left, right) {
  const leftMeta = normalizeSessionMeta(left.meta || left);
  const rightMeta = normalizeSessionMeta(right.meta || right);
  if (leftMeta.pinned !== rightMeta.pinned) return leftMeta.pinned ? -1 : 1;
  return String(right.updated_at || "").localeCompare(String(left.updated_at || ""));
}

function syncSessionMetaControls() {
  if (pinSessionButton) {
    pinSessionButton.textContent = currentSessionMeta.pinned ? "Desfixar" : "Fixar";
  }
  if (archiveSessionButton) {
    archiveSessionButton.textContent = currentSessionMeta.archived ? "Restaurar" : "Arquivar";
  }
}

async function toggleCurrentSessionMeta(field) {
  if (!currentSessionId) return;
  const nextMeta = {
    ...normalizeSessionMeta(currentSessionMeta),
    [field]: !currentSessionMeta[field],
  };
  const payload = await api(`/api/chat/sessions/${currentSessionId}`, {
    method: "PUT",
    body: JSON.stringify({ meta: nextMeta }),
  });
  currentSessionMeta = normalizeSessionMeta(payload.session.meta);
  if (field === "archived") {
    if (currentSessionMeta.archived && currentSessionFilter === "active") {
      setSessionFilter("archived");
    } else if (!currentSessionMeta.archived && currentSessionFilter === "archived") {
      setSessionFilter("active");
    }
  }
  syncSessionMetaControls();
  await loadSessions();
}

function renderSessions(sessions) {
  sessionsEl.innerHTML = "";
  const term = (sessionSearchEl.value || "").trim().toLowerCase();
  const filtered = sessions
    .filter((session) => matchSessionFilter(session))
    .filter((session) => {
      if (!term) return true;
      return [session.title || "", session.model || "", session.workspace || "", session.mission_objective || "", session.preview || ""]
        .join(" ")
        .toLowerCase()
        .includes(term);
    })
    .sort(compareSessionsForSidebar);
  if (!filtered.length) {
    sessionsEl.textContent = "Nenhuma conversa ainda.";
    return;
  }
  for (const session of filtered) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "session-item";
    button.dataset.sessionId = session.id;
    const tags = [
      session.pinned ? "fixada" : null,
      session.archived ? "arquivada" : null,
      session.workspace ? `ws:${session.workspace}` : null,
      session.active_tasks ? `${session.active_tasks} tarefa(s)` : null,
      session.checkpoint_count ? `${session.checkpoint_count} ckpt` : null,
    ].filter(Boolean).join(" · ");
    const sessionMeta = [session.model || "jarvis-safe", session.active_file ? `arquivo ${session.active_file}` : null, session.mission_status || null, session.updated_at || null]
      .filter(Boolean)
      .join(" · ");
    button.innerHTML = `
      <strong>${escapeHtml(session.title || "Nova conversa")}</strong>
      <span>${escapeHtml(sessionMeta)}</span>
      ${tags ? `<small>${escapeHtml(tags)}</small>` : ""}
      ${session.preview ? `<small>${escapeHtml(session.preview)}</small>` : ""}
    `;
    button.addEventListener("click", () => selectSession(session.id));
    sessionsEl.appendChild(button);
  }
  highlightSelectedSession();
}

function highlightSelectedSession() {
  for (const node of sessionsEl.querySelectorAll(".session-item")) {
    node.classList.toggle("active", node.dataset.sessionId === currentSessionId);
  }
}

function buildSessionUiStateSnapshot() {
  return {
    active_file: currentOpenFilePath || null,
    open_files: openEditors.map((editor) => editor.path),
    quick_flow_mode: quickFlowMode || null,
    quick_target_path: (quickTargetPathEl?.value || "").trim() || null,
    quick_goal: (quickGoalEl?.value || "").trim() || null,
    draft_prompt: (promptEl?.value || "").trim() || null,
    editor_instruction: (editorInstructionEl?.value || "").trim() || null,
    terminal_command: (terminalCommandEl?.value || "").trim() || null,
    workbench_mode: workbenchMode || null,
  };
}

function clearSessionWorkspaceState() {
  openEditors = [];
  currentOpenFilePath = null;
  pendingEditProposal = null;
  pendingBatchProposal = null;
  pendingTaskAssist = null;
  editorSelection = null;
  fileEditorEl.value = "";
  editorInstructionEl.value = "";
  renderEditorTabs();
  syncEditorFromState();
  renderWorkspaceTree();
}

async function persistSessionUiState() {
  if (!currentSessionId || restoringSessionUiState) return;
  const snapshot = buildSessionUiStateSnapshot();
  currentSessionUiState = snapshot;
  const payload = await api(`/api/chat/sessions/${currentSessionId}`, {
    method: "PUT",
    body: JSON.stringify({ ui_state: snapshot }),
  });
  currentSessionUiState = payload.session.ui_state || snapshot;
}

function scheduleSessionUiStateSave() {
  if (!currentSessionId || restoringSessionUiState) return;
  if (sessionUiStateSaveTimer) {
    window.clearTimeout(sessionUiStateSaveTimer);
  }
  sessionUiStateSaveTimer = window.setTimeout(() => {
    sessionUiStateSaveTimer = null;
    persistSessionUiState().catch((error) => {
      console.warn("jarvis ui_state persist failed", error);
    });
  }, 250);
}

async function restoreSessionUiState(session) {
  restoringSessionUiState = true;
  try {
    const uiState = session?.ui_state || {};
    currentSessionUiState = uiState;
    quickFlowMode = normalizeQuickFlowMode(uiState.quick_flow_mode || quickFlowMode);
    if (quickTargetPathEl) quickTargetPathEl.value = uiState.quick_target_path || "";
    if (quickGoalEl) quickGoalEl.value = uiState.quick_goal || "";
    promptEl.value = uiState.draft_prompt || "";
    editorInstructionEl.value = uiState.editor_instruction || "";
    terminalCommandEl.value = uiState.terminal_command || "";
    setWorkbenchMode(uiState.workbench_mode || workbenchMode, { persist: false });
    syncQuickFlowUi();

    const paths = Array.isArray(uiState.open_files) ? uiState.open_files.slice(0, 8) : [];
    for (const path of paths) {
      try {
        await openWorkspaceFile(path, { persist: false });
      } catch {
        // ignore missing files during restore
      }
    }
    if (uiState.active_file) {
      const existing = openEditors.find((editor) => editor.path === uiState.active_file);
      if (existing) {
        currentOpenFilePath = existing.path;
        syncEditorFromState();
        renderEditorTabs();
      }
    }
    renderComposerContextPreview();
    renderWorkbenchStatus();
  } finally {
    restoringSessionUiState = false;
  }
}

function phaseLabel(phase) {
  return ["planner", "executor", "verifier", "memory"].includes(phase) ? phase : "planner";
}

function nextTaskPhase(phase) {
  const phases = ["planner", "executor", "verifier", "memory"];
  const index = phases.indexOf(phaseLabel(phase));
  return phases[Math.min(index + 1, phases.length - 1)];
}

async function createSessionTaskFromInputs() {
  if (!currentSessionId) return;
  const title = (taskTitleEl.value || "").trim();
  if (!title) return;
  const payload = await api(`/api/chat/sessions/${currentSessionId}/tasks`, {
    method: "POST",
    body: JSON.stringify({
      title,
      objective: missionObjectiveInputEl.value.trim() || null,
      phase: taskPhaseEl.value || "planner",
      status: "todo",
      workspace: workspaceInput.value.trim() || null,
    }),
  });
  currentTasks = payload.session.tasks || [];
  currentEvents = payload.session.events || [];
  taskTitleEl.value = "";
  renderMissionControl();
  await loadSessions();
  announceAssistantMessage(`Tarefa criada: ${title}`);
}

async function updateSessionTask(taskId, patch) {
  if (!currentSessionId) return;
  const payload = await api(`/api/chat/sessions/${currentSessionId}/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(patch),
  });
  currentTasks = payload.session.tasks || [];
  currentEvents = payload.session.events || [];
  renderMissionControl();
  await loadSessions();
}

function renderTaskBoard() {
  if (!taskBoardEl) return;
  taskBoardEl.innerHTML = "";
  if (!currentTasks.length) {
    taskBoardEl.innerHTML = '<div class="task-board-empty">Nenhuma tarefa ativa nesta sessão.</div>';
    return;
  }
  [...currentTasks].slice().reverse().forEach((task) => {
    const card = document.createElement("div");
    card.className = `task-card ${task.status || "todo"}`;
    card.innerHTML = `<strong>${escapeHtml(task.title || "Nova tarefa")}</strong><span>${escapeHtml(`${phaseLabel(task.phase)} · ${task.status || "todo"}`)}</span>${task.objective ? `<small>${escapeHtml(task.objective)}</small>` : ""}`;

    const actions = document.createElement("div");
    actions.className = "task-card-actions";

    const start = document.createElement("button");
    start.type = "button";
    start.className = "secondary";
    start.textContent = "Iniciar";
    start.disabled = task.status === "in_progress";
    start.addEventListener("click", async () => {
      await updateSessionTask(task.id, { status: "in_progress" });
    });

    const next = document.createElement("button");
    next.type = "button";
    next.className = "secondary";
    next.textContent = "Próxima fase";
    next.disabled = phaseLabel(task.phase) === "memory";
    next.addEventListener("click", async () => {
      await updateSessionTask(task.id, { phase: nextTaskPhase(task.phase), status: task.status === "todo" ? "in_progress" : task.status });
    });

    const done = document.createElement("button");
    done.type = "button";
    done.className = "secondary";
    done.textContent = "Concluir";
    done.disabled = task.status === "done";
    done.addEventListener("click", async () => {
      await updateSessionTask(task.id, { status: "done", phase: phaseLabel(task.phase) === "memory" ? "memory" : "verifier" });
    });

    actions.append(start, next, done);
    card.appendChild(actions);
    taskBoardEl.appendChild(card);
  });
}

function normalizeMissionPayload(mission = null) {
  const payload = mission || {};
  return {
    objective: payload.objective || "",
    status: payload.status || "idle",
    next_steps: Array.isArray(payload.next_steps) ? payload.next_steps.filter((item) => String(item || "").trim()) : [],
    updated_at: payload.updated_at || null,
  };
}

function syncMissionInputs() {
  const mission = normalizeMissionPayload(currentMission);
  missionObjectiveInputEl.value = mission.objective || "";
  missionStatusInputEl.value = mission.status || "idle";
  missionNextStepsInputEl.value = mission.next_steps.join("\n");
}

async function persistMissionFromInputs() {
  if (!currentSessionId) return;
  const mission = normalizeMissionPayload({
    objective: missionObjectiveInputEl.value.trim() || null,
    status: missionStatusInputEl.value.trim() || "idle",
    next_steps: missionNextStepsInputEl.value.split(/\n+/).map((item) => item.trim()).filter(Boolean),
  });
  const payload = await api(`/api/chat/sessions/${currentSessionId}`, {
    method: "PUT",
    body: JSON.stringify({ mission }),
  });
  currentMission = payload.session.mission || mission;
  currentTasks = payload.session.tasks || currentTasks;
  currentEvents = payload.session.events || currentEvents;
  renderMissionControl();
  await loadSessions();
  await appendSessionOperation({
    kind: "mission_update",
    title: "Atualizou missão ativa",
    detail: mission.objective || mission.status || "missão sem objetivo definido",
  });
  announceAssistantMessage("Missão persistida nesta sessão do Jarvis.");
}

function buildMissionModel() {
  const active = getCurrentEditor();
  const dirtyEditors = openEditors.filter((editor) => editor.dirty);
  const hasTerminalOutput = Boolean(terminalBuffer.trim());
  const hasGitContext = Boolean(latestGitContext.trim());
  const pendingApprovals = currentApprovals.filter((item) => item.status === "pending");
  const latestOperation = currentSessionOperations.length ? currentSessionOperations[currentSessionOperations.length - 1] : null;
  const risks = [];
  if (dirtyEditors.length) risks.push(`${dirtyEditors.length} arquivo(s) com alterações não salvas`);
  if (pendingApprovals.length) risks.push(`${pendingApprovals.length} ação(ões) aguardando decisão`);
  if (active && !hasTerminalOutput) risks.push("sem saída recente de terminal para validar a alteração atual");
  if (!active) risks.push("nenhum arquivo ativo no editor");
  const focus = active
    ? `Trabalhando em ${active.path}`
    : `Sem arquivo aberto no workspace ${workspaceInput.value.trim() || "jarvis"}`;
  const mission = normalizeMissionPayload(currentMission);
  const activeTasks = currentTasks.filter((task) => task.status !== "done");
  return {
    active,
    dirtyEditors,
    hasTerminalOutput,
    hasGitContext,
    pendingApprovals,
    latestOperation,
    focus,
    risks,
    mission,
    activeTasks,
  };
}

function buildMissionActions(model) {
  const actions = [];
  if (!model.active) {
    actions.push({
      label: "Abrir arquivo do workspace",
      detail: "Escolha um arquivo para o Jarvis acompanhar",
      run: async () => {
        openPathButton.click();
        setWorkbenchMode("build");
      },
    });
  }
  if (model.active && model.dirtyEditors.length) {
    actions.push({
      label: "Salvar abas pendentes",
      detail: "Persistir mudanças antes de validar",
      run: async () => {
        await saveAllEditors();
      },
    });
  }
  if (model.active && !model.hasTerminalOutput) {
    actions.push({
      label: "Pedir plano de validação",
      detail: "Jarvis sugere como testar a mudança atual",
      run: async () => {
        primePrompt(`Sou seu parceiro técnico. Para o arquivo ${model.active.path}, proponha o melhor plano curto de validação e o primeiro comando a executar.`, { mode: "build", activeFile: true, terminal: true });
      },
    });
  }
  if (model.pendingApprovals.length) {
    actions.push({
      label: "Entrar em modo review",
      detail: "Revisar fila de ações pendentes do Jarvis",
      run: async () => {
        setWorkbenchMode("review");
      },
    });
  }
  if (model.active && model.hasTerminalOutput) {
    actions.push({
      label: "Diagnosticar saída atual",
      detail: "Usar terminal e arquivo ativo para próxima decisão",
      run: async () => {
        preparePromptForTerminalDebug();
      },
    });
  }
  if (model.active && !model.hasGitContext) {
    actions.push({
      label: "Coletar contexto Git",
      detail: "Carregar status/diff para revisão e PR",
      run: async () => {
        await loadGitContext("status");
        setWorkbenchMode("review");
      },
    });
  }
  actions.push({
    label: "Briefing completo",
    detail: "Pedir ao Jarvis um resumo operacional e próxima ação",
    run: async () => {
      primePrompt(buildMissionPrompt(), { mode: "chat", activeFile: Boolean(model.active), terminal: true, search: true });
    },
  });
  return actions.slice(0, 4);
}

function buildMissionBriefingText() {
  const model = buildMissionModel();
  const lines = [
    `Missão: ${model.mission.objective || "não definida"}`,
    `Status: ${model.mission.status || "idle"}`,
    model.mission.next_steps.length ? `Próximos passos: ${model.mission.next_steps.join("; ")}` : "Próximos passos: nenhum registrado",
    `Foco: ${model.focus}`,
    model.latestOperation ? `Última operação: ${model.latestOperation.title || model.latestOperation.kind}` : "Última operação: nenhuma ainda",
    model.risks.length ? `Alertas: ${model.risks.join("; ")}` : "Alertas: nenhum crítico no momento",
  ];
  return lines.join("\n");
}

function buildMissionPrompt() {
  const model = buildMissionModel();
  const lines = [
    "Atue como meu parceiro virtual local no estilo Jarvis.",
    "Faça um briefing curto, diga o estado atual, o maior risco e a próxima melhor ação.",
    `Missão persistida: ${model.mission.objective || "não definida"}`,
    `Status da missão: ${model.mission.status || "idle"}`,
    model.mission.next_steps.length ? `Próximos passos registrados: ${model.mission.next_steps.join("; ")}` : "Próximos passos registrados: nenhum.",
    `Foco atual: ${model.focus}`,
    model.latestOperation ? `Última operação: ${model.latestOperation.title || model.latestOperation.kind}` : "Última operação: nenhuma",
    model.risks.length ? `Alertas: ${model.risks.join('; ')}` : "Alertas: nenhum crítico.",
  ];
  return lines.join(" ");
}

function renderMissionControl() {
  if (!missionStatusEl || !missionNextActionsEl) return;
  const model = buildMissionModel();
  syncMissionInputs();
  const latestOperation = model.latestOperation?.title || model.latestOperation?.kind || "nenhuma";
  const statusCards = [
    { label: "Missão", value: model.mission.objective || "Nenhum objetivo persistido nesta sessão" },
    { label: "Status", value: model.mission.status || "idle" },
    { label: "Foco", value: model.focus },
    { label: "Última ação", value: latestOperation },
    { label: "Aprovações", value: model.pendingApprovals.length ? `${model.pendingApprovals.length} pendente(s)` : "fila limpa" },
    { label: "Tarefas", value: model.activeTasks.length ? `${model.activeTasks.length} ativa(s)` : "sem tarefas ativas" },
    { label: "Risco", value: model.risks[0] || "baixo no momento" },
  ];
  missionStatusEl.innerHTML = statusCards
    .map((item) => `<div class="mission-card"><strong>${escapeHtml(item.label)}</strong><span>${escapeHtml(item.value)}</span></div>`)
    .join("");

  const actions = buildMissionActions(model);
  missionNextActionsEl.innerHTML = "";
  actions.forEach((action) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "secondary mission-action";
    button.innerHTML = `<strong>${escapeHtml(action.label)}</strong><span>${escapeHtml(action.detail)}</span>`;
    button.addEventListener("click", async () => {
      await action.run();
      renderMissionControl();
    });
    missionNextActionsEl.appendChild(button);
  });
  renderTaskBoard();
}

function buildCommandPaletteItems() {
  const active = getCurrentEditor();
  const workspace = workspaceInput.value.trim() || "jarvis";
  const items = [
    { label: "Abrir arquivo", description: "Solicita um caminho e abre no editor", keywords: ["open", "arquivo", "editor"], action: async () => { openPathButton.click(); setWorkbenchMode("build"); } },
    { label: "Criar arquivo", description: "Cria um arquivo e prepara o Jarvis para implementar", keywords: ["new", "criar", "file", "jarvis"], action: async () => { await preparePromptForCreateFile(); } },
    { label: "Fluxo rápido: abrir/criar alvo", description: resolveQuickTargetPath() || "Usa o alvo do cockpit rápido", keywords: ["quick", "target", "codex", "arquivo"], action: async () => { await openQuickFlowTarget(); } },
    { label: "Fluxo rápido: pedir ao Jarvis", description: "Gera prompt com intenção, alvo e objetivo atuais", keywords: ["quick", "prompt", "codex", "jarvis"], action: async () => { await runQuickFlowPrompt(); } },
    { label: "Anexar terminal ao chat", description: "Leva a saída recente do bash para o próximo prompt", keywords: ["terminal", "attach", "bash", "chat"], action: async () => { await attachTerminalSnapshot(); } },
    { label: "Explicar arquivo atual", description: active ? active.path : "Requer um arquivo aberto", keywords: ["explain", "arquivo", "analise"], action: async () => { preparePromptForActiveFile(); } },
    { label: "Diagnosticar terminal", description: "Usa a saída recente do terminal como contexto", keywords: ["debug", "terminal", "bash"], action: async () => { await preparePromptForTerminalFix(); } },
    { label: "Próximo passo sugerido", description: `Planejar próxima ação no workspace ${workspace}`, keywords: ["next", "step", "planner", "workspace"], action: async () => { preparePromptForNextStep(); } },
    { label: "Modo Chat", description: "Foco em conversa com Jarvis", keywords: ["mode", "chat"], action: async () => { setWorkbenchMode("chat"); } },
    { label: "Modo Build", description: "Foco em arquivos, edição e implementação", keywords: ["mode", "build", "editor"], action: async () => { setWorkbenchMode("build"); } },
    { label: "Modo Review", description: "Foco em diffs, fila e revisão", keywords: ["mode", "review", "diff", "approval"], action: async () => { setWorkbenchMode("review"); } },
    { label: "Modo Focus", description: "Esconde painéis para conversa concentrada", keywords: ["mode", "focus", "minimal"], action: async () => { setWorkbenchMode("focus"); } },
    { label: "Novo terminal", description: "Abre uma nova sessão bash persistente", keywords: ["terminal", "bash", "new"], action: async () => { await createTerminalSession(); setWorkbenchMode("build"); } },
    { label: "Terminal no diretório do arquivo", description: active ? active.path : "Requer um arquivo aberto", keywords: ["terminal", "file", "cwd"], action: async () => { await jumpTerminalToActiveFileDir(); setWorkbenchMode("build"); } },
    { label: "Abrir terminal Linux nativo", description: "Lança um terminal externo do sistema", keywords: ["linux", "native", "terminal"], action: async () => { await openNativeLinuxTerminal(); } },
    { label: "Anexar contexto Git", description: "Prepara status/diff/log para o próximo prompt", keywords: ["git", "attach", "context"], action: async () => { await attachGitContextToChat(); setWorkbenchMode("review"); } },
    { label: "Salvar todas as abas", description: "Persiste todos os arquivos pendentes", keywords: ["save", "tabs", "files"], action: async () => { await saveAllEditors(); } },
    { label: "Criar tarefa planner", description: "Abre uma nova tarefa no ciclo planner → executor → verifier → memory", keywords: ["task", "planner", "cycle"], action: async () => { taskPhaseEl.value = "planner"; taskTitleEl.focus(); setWorkbenchMode("chat"); } },
    { label: "Anexar abas abertas", description: "Coloca as abas abertas no próximo prompt", keywords: ["attach", "tabs", "prompt"], action: async () => { await attachOpenTabsToChat(); } },
  ];
  if (active) {
    items.unshift({ label: `Perguntar sobre ${active.path}`, description: "Prepara um prompt direto sobre o arquivo ativo", keywords: ["ask", active.path, "active"], action: async () => { primePrompt(`Analise ${active.path} como meu parceiro técnico. Explique o que está acontecendo e proponha a melhor próxima ação.`, { mode: "build", activeFile: true, terminal: true }); } });
  }
  return items;
}

function getFilteredCommandPaletteItems() {
  const term = (commandPaletteInputEl.value || "").trim().toLowerCase();
  const items = buildCommandPaletteItems();
  if (!term) return items;
  return items.filter((item) => [item.label, item.description || "", ...(item.keywords || [])].join(" ").toLowerCase().includes(term));
}

function openCommandPalette() {
  commandPaletteOpen = true;
  commandPaletteIndex = 0;
  commandPaletteInputEl.value = "";
  commandPaletteEl.classList.remove("hidden");
  commandPaletteEl.setAttribute("aria-hidden", "false");
  renderCommandPaletteResults();
  window.setTimeout(() => {
    commandPaletteInputEl.focus();
    commandPaletteInputEl.select();
  }, 0);
}

function closeCommandPalette() {
  commandPaletteOpen = false;
  commandPaletteEl.classList.add("hidden");
  commandPaletteEl.setAttribute("aria-hidden", "true");
  commandPaletteItems = [];
  focusComposer();
}

function moveCommandPaletteSelection(delta) {
  if (!commandPaletteItems.length) return;
  commandPaletteIndex = (commandPaletteIndex + delta + commandPaletteItems.length) % commandPaletteItems.length;
  renderCommandPaletteResults();
}

async function executeSelectedCommandPaletteItem() {
  const item = commandPaletteItems[commandPaletteIndex];
  if (!item) return;
  closeCommandPalette();
  await item.action();
}

function renderCommandPaletteResults() {
  commandPaletteItems = getFilteredCommandPaletteItems();
  if (!commandPaletteItems.length) {
    commandPaletteResultsEl.innerHTML = '<div class="command-palette-empty">Nenhum comando encontrado.</div>';
    return;
  }
  commandPaletteIndex = Math.min(commandPaletteIndex, commandPaletteItems.length - 1);
  commandPaletteResultsEl.innerHTML = "";
  commandPaletteItems.forEach((item, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "command-palette-item secondary";
    if (index === commandPaletteIndex) button.classList.add("active");
    button.innerHTML = `<strong>${escapeHtml(item.label)}</strong><span>${escapeHtml(item.description || "")}</span>`;
    button.addEventListener("mousemove", () => {
      if (commandPaletteIndex !== index) {
        commandPaletteIndex = index;
        renderCommandPaletteResults();
      }
    });
    button.addEventListener("click", async () => {
      commandPaletteIndex = index;
      await executeSelectedCommandPaletteItem();
    });
    commandPaletteResultsEl.appendChild(button);
  });
}

function loadWorkbenchMode() {
  try {
    const raw = localStorage.getItem(WORKBENCH_MODE_KEY);
    if (raw) workbenchMode = raw;
  } catch {
    workbenchMode = "chat";
  }
}

function setWorkbenchMode(mode, options = {}) {
  const normalized = ["chat", "build", "review", "focus"].includes(mode) ? mode : "chat";
  workbenchMode = normalized;
  document.body.dataset.workbenchMode = normalized;
  for (const button of workbenchModeButtons) {
    button.classList.toggle("active", button.dataset.mode === normalized);
  }
  if (options.persist !== false) {
    localStorage.setItem(WORKBENCH_MODE_KEY, normalized);
  }
  if (options.syncSession !== false) {
    scheduleSessionUiStateSave();
  }
  renderWorkbenchStatus();
}

function focusComposer() {
  promptEl.focus();
  const end = promptEl.value.length;
  promptEl.setSelectionRange(end, end);
}

function primePrompt(prompt, { mode = null, activeFile = false, terminal = false, search = false } = {}) {
  if (activeFile) contextActiveFileCheckbox.checked = true;
  if (terminal) contextTerminalCheckbox.checked = true;
  if (search) contextSearchCheckbox.checked = true;
  persistContextPrefs();
  renderComposerContextPreview();
  promptEl.value = prompt;
  if (mode) setWorkbenchMode(mode);
  focusComposer();
}

function preparePromptForActiveFile() {
  const active = getCurrentEditor();
  if (!active) {
    announceAssistantMessage("Abra um arquivo antes de pedir análise do arquivo atual.");
    return;
  }
  primePrompt(`Explique o arquivo ${active.path}, aponte riscos, gargalos e melhorias concretas.`, { mode: "build", activeFile: true });
}

function preparePromptForTerminalDebug() {
  if (!terminalBuffer.trim()) {
    announceAssistantMessage("Ainda não há saída recente no terminal para diagnosticar.");
    return;
  }
  primePrompt("Analise a saída recente do terminal, identifique a causa raiz do problema e proponha a próxima ação objetiva.", { mode: "review", activeFile: Boolean(getCurrentEditor()), terminal: true });
}

async function preparePromptForCreateFile() {
  const path = (window.prompt("Caminho do novo arquivo relativo ao workspace:", quickTargetPathEl?.value || currentOpenFilePath || "notes/tarefa.md") || "").trim();
  if (!path) return;
  const goal = (window.prompt("O que o Jarvis deve criar nesse arquivo?", quickGoalEl?.value || "Implemente a primeira versão com estrutura clara e comentários mínimos.") || "").trim();
  if (quickTargetPathEl) quickTargetPathEl.value = path;
  if (quickGoalEl && goal) quickGoalEl.value = goal;
  await setQuickFlowMode("create");
  await ensureWorkspaceFile(path);
  await runQuickFlowPrompt();
}

function preparePromptForNextStep() {
  const workspace = workspaceInput.value.trim() || "jarvis";
  const active = getCurrentEditor();
  const suffix = active ? ` Considere especialmente o arquivo ${active.path}.` : "";
  primePrompt(`Com base no estado atual do workspace ${workspace}, proponha o próximo passo de maior impacto e menor risco.${suffix}`, { mode: "chat", activeFile: Boolean(active), terminal: true, search: true });
}

const QUICK_FLOW_CONFIG = {
  create: {
    label: "criar",
    model: "jarvis-programador",
    targetRequired: true,
    defaultGoal: "criar uma primeira versão funcional com estrutura clara e manutenção simples",
    placeholder: "Objetivo, ex: criar um chat lateral com streaming",
    taskInstruction: (path, goal) => `Implemente o arquivo ${path}. Objetivo: ${goal}. Mantenha a solução simples e funcional.`,
    prompt: (path, goal) => `Crie ou continue o arquivo ${path}. Objetivo: ${goal}. Entregue uma primeira versão funcional e explique o próximo passo.`,
    context: { mode: "build", activeFile: true, terminal: true },
  },
  implement: {
    label: "implementar",
    model: "jarvis-programador",
    targetRequired: true,
    defaultGoal: "implementar a funcionalidade solicitada com validação objetiva",
    placeholder: "Objetivo, ex: implementar o fluxo de aprovações no editor",
    taskInstruction: (path, goal) => `No arquivo ${path}, implemente: ${goal}. Priorize clareza, baixo risco e código diretamente utilizável.`,
    prompt: (path, goal) => `Implemente no arquivo ${path}: ${goal}. Proponha a melhor abordagem e a primeira alteração concreta.`,
    context: { mode: "build", activeFile: true, terminal: true },
  },
  "fix-terminal": {
    label: "corrigir erro",
    model: "jarvis-programador",
    targetRequired: false,
    requiresTerminal: true,
    defaultGoal: "diagnosticar a falha atual, explicar a causa raiz e sugerir a menor correção segura",
    placeholder: "Objetivo, ex: entender por que o backend não sobe no VS Code",
    taskInstruction: (path, goal) => `Use o terminal recente${path ? ` e o arquivo ${path}` : ""} para ${goal}. Se houver edição, proponha a menor correção segura.`,
    prompt: (path, goal) => `Analise o terminal recente${path ? ` e o arquivo ${path}` : ""}. Objetivo: ${goal}. Diga a causa raiz e a próxima ação objetiva.`,
    context: { mode: "review", activeFile: true, terminal: true },
  },
  review: {
    label: "revisar",
    model: "jarvis-programador",
    targetRequired: false,
    defaultGoal: "revisar o arquivo ativo, apontar riscos e sugerir melhorias concretas",
    placeholder: "Objetivo, ex: revisar este arquivo como código de produção",
    taskInstruction: (path, goal) => `Revise ${path || "o arquivo ativo"}. Objetivo: ${goal}. Priorize bugs, regressões e clareza.`,
    prompt: (path, goal) => `Revise ${path || "o arquivo ativo"} com foco em bugs, riscos, gargalos e melhorias objetivas. Objetivo adicional: ${goal}.`,
    context: { mode: "review", activeFile: true, terminal: true },
  },
  research: {
    label: "pesquisar",
    model: "jarvis-pesquisador",
    targetRequired: false,
    defaultGoal: "buscar contexto documental local e resumir o que é mais útil agora",
    placeholder: "Objetivo, ex: procurar notas e documentos locais sobre Linux ou CrossFit",
    taskInstruction: (path, goal) => `Pesquise o contexto local${path ? ` relacionado a ${path}` : ""}. Objetivo: ${goal}.`,
    prompt: (path, goal) => `Pesquise a base local${path ? ` relacionada a ${path}` : ""}. Objetivo: ${goal}. Cite caminhos e próximos passos úteis.`,
    context: { mode: "chat", activeFile: Boolean(getCurrentEditor()), terminal: false, search: true },
  },
};

function loadQuickFlowMode() {
  try {
    const raw = localStorage.getItem(QUICK_FLOW_MODE_KEY);
    if (raw && QUICK_FLOW_CONFIG[raw]) quickFlowMode = raw;
  } catch {
    quickFlowMode = "create";
  }
}

async function setPreferredModel(model) {
  if (!model || modelSelect.value === model) return;
  modelSelect.value = model;
  if (currentSessionId) {
    await api(`/api/chat/sessions/${currentSessionId}`, {
      method: "PUT",
      body: JSON.stringify({ model }),
    });
    await loadSessions();
  }
}

function normalizeQuickFlowMode(mode) {
  return QUICK_FLOW_CONFIG[mode] ? mode : "create";
}

function resolveQuickFlowConfig(mode = quickFlowMode) {
  return QUICK_FLOW_CONFIG[normalizeQuickFlowMode(mode)];
}

function resolveQuickTargetPath() {
  return (quickTargetPathEl?.value || currentOpenFilePath || "").trim();
}

function resolveQuickGoal(mode = quickFlowMode) {
  const config = resolveQuickFlowConfig(mode);
  const goal = (quickGoalEl?.value || "").trim();
  return goal || config.defaultGoal;
}

function syncQuickFlowUi() {
  const config = resolveQuickFlowConfig();
  if (quickGoalEl) quickGoalEl.placeholder = config.placeholder;
  quickFlowButtons.forEach((button) => {
    button.classList.toggle("active", (button.dataset.quickFlow || "") === quickFlowMode);
  });
  renderComposerContextPreview();
  scheduleSessionUiStateSave();
}

async function setQuickFlowMode(mode, options = {}) {
  quickFlowMode = normalizeQuickFlowMode(mode);
  if (options.persist !== false) {
    localStorage.setItem(QUICK_FLOW_MODE_KEY, quickFlowMode);
  }
  const config = resolveQuickFlowConfig();
  if (quickGoalEl && !quickGoalEl.value.trim()) {
    quickGoalEl.value = config.defaultGoal;
  }
  await setPreferredModel(config.model);
  syncQuickFlowUi();
}

async function ensureWorkspaceFile(path) {
  const normalizedPath = String(path || "").trim();
  if (!normalizedPath) return null;
  try {
    await api(`/api/workspace/file?session_id=${encodeURIComponent(currentSessionId || "")}`, {
      method: "POST",
      body: JSON.stringify({ path: normalizedPath, content: "" }),
    });
    await appendSessionOperation({ kind: "quick_file_create", title: `Fluxo rápido criou ${normalizedPath}`, path: normalizedPath, detail: "arquivo preparado para o Jarvis" });
  } catch {
    // file may already exist
  }
  await loadWorkspaceTree();
  await openWorkspaceFile(normalizedPath);
  return normalizedPath;
}

function getRecentTerminalExcerpt(limit = 6000) {
  const text = String(terminalBuffer || "").trim();
  if (!text) return "";
  return text.length > limit ? text.slice(-limit) : text;
}

async function attachTerminalSnapshot(options = {}) {
  const excerpt = getRecentTerminalExcerpt(options.limit || 6000);
  if (!excerpt) {
    if (options.announce !== false) announceAssistantMessage("Ainda não há saída recente no terminal para anexar.");
    return false;
  }
  pendingAttachments.push({
    id: `terminal-context-${Date.now()}`,
    name: options.name || "terminal-context.txt",
    content: excerpt,
    size: new Blob([excerpt]).size,
  });
  renderAttachments();
  await appendSessionOperation({
    kind: "terminal_attach",
    title: "Anexou saída recente do terminal",
    command: commandHistory[0] || null,
    path: getCurrentEditor()?.path || null,
    detail: `${excerpt.length} chars prontos para o próximo prompt`,
  });
  if (options.announce !== false) announceAssistantMessage("Saída recente do terminal anexada ao próximo prompt.");
  return true;
}

async function openQuickFlowTarget() {
  const config = resolveQuickFlowConfig();
  const path = resolveQuickTargetPath();
  if (config.targetRequired && !path) {
    announceAssistantMessage("Defina um caminho no fluxo rápido antes de abrir ou criar o alvo.");
    return;
  }
  if (!path) {
    const active = getCurrentEditor();
    if (active) {
      setWorkbenchMode("build");
      announceAssistantMessage(`Usando o arquivo ativo ${active.path} como alvo do fluxo rápido.`);
      return;
    }
    announceAssistantMessage("Abra um arquivo ou informe um alvo no fluxo rápido.");
    return;
  }
  await ensureWorkspaceFile(path);
  setWorkbenchMode("build");
  announceAssistantMessage(`Alvo pronto no editor: ${path}`);
}

function buildQuickFlowPrompt(mode = quickFlowMode) {
  const config = resolveQuickFlowConfig(mode);
  const target = resolveQuickTargetPath() || getCurrentEditor()?.path || "o contexto atual";
  const goal = resolveQuickGoal(mode);
  return config.prompt(target, goal);
}

async function runQuickFlowPrompt() {
  const config = resolveQuickFlowConfig();
  const target = resolveQuickTargetPath();
  if (config.requiresTerminal && !getRecentTerminalExcerpt()) {
    announceAssistantMessage("Execute algo no terminal antes de usar o fluxo de correção por terminal.");
    return;
  }
  if (config.targetRequired && target) {
    await ensureWorkspaceFile(target);
  }
  if (config.targetRequired && !target && !getCurrentEditor()) {
    announceAssistantMessage("Defina um alvo no workspace ou abra um arquivo antes de pedir implementação.");
    return;
  }
  await setPreferredModel(config.model);
  if (config.requiresTerminal) {
    await attachTerminalSnapshot({ announce: false });
  }
  primePrompt(buildQuickFlowPrompt(), config.context);
}

async function stageQuickFlowInEditor() {
  const config = resolveQuickFlowConfig();
  const target = resolveQuickTargetPath();
  if (config.targetRequired && target) {
    await ensureWorkspaceFile(target);
  }
  const active = getCurrentEditor();
  if (!active) {
    announceAssistantMessage("Abra ou crie um arquivo antes de levar o fluxo rápido para o editor.");
    return;
  }
  if (config.requiresTerminal && !getRecentTerminalExcerpt()) {
    announceAssistantMessage("Ainda não há saída recente no terminal para transformar em tarefa do editor.");
    return;
  }
  editorInstructionEl.value = config.taskInstruction(active.path, resolveQuickGoal());
  if (config.requiresTerminal) {
    await attachTerminalSnapshot({ announce: false });
  }
  setWorkbenchMode("build");
  editorInstructionEl.focus();
  announceAssistantMessage(`Fluxo ${config.label} preparado no editor para ${active.path}. Use 'Jarvis executar' quando quiser.`);
}

async function preparePromptForTerminalFix() {
  const excerpt = getRecentTerminalExcerpt();
  if (!excerpt) {
    announceAssistantMessage("Ainda não há saída recente no terminal para diagnosticar.");
    return;
  }
  await setQuickFlowMode("fix-terminal");
  await attachTerminalSnapshot({ announce: false });
  primePrompt(buildQuickFlowPrompt("fix-terminal"), { mode: "review", activeFile: Boolean(getCurrentEditor()), terminal: true });
}

async function createTerminalFollowupTask() {
  if (!currentSessionId) return;
  const excerpt = getRecentTerminalExcerpt(400);
  if (!excerpt) {
    announceAssistantMessage("Ainda não há saída recente no terminal para virar tarefa.");
    return;
  }
  const firstLine = excerpt.split("\n").map((line) => line.trim()).find(Boolean) || "diagnosticar terminal local";
  const title = `Diagnosticar terminal: ${firstLine.slice(0, 72)}`;
  const payload = await api(`/api/chat/sessions/${currentSessionId}/tasks`, {
    method: "POST",
    body: JSON.stringify({
      title,
      objective: resolveQuickGoal("fix-terminal"),
      phase: "planner",
      status: "todo",
      workspace: workspaceInput.value.trim() || null,
    }),
  });
  currentTasks = payload.session.tasks || [];
  currentEvents = payload.session.events || [];
  renderMissionControl();
  await loadSessions();
  announceAssistantMessage("Saída recente do terminal convertida em tarefa do ciclo planner → executor → verifier → memory.");
}

function renderWorkbenchStatus() {
  if (!workbenchStatusEl) return;
  const active = getCurrentEditor();
  const dirtyCount = openEditors.filter((editor) => editor.dirty).length;
  const partnerHint = active ? `Jarvis acompanhando ${active.path}` : "Jarvis em escuta";
  const parts = [
    partnerHint,
    `modo ${workbenchMode}`,
    `perfil ${modelSelect.value || "jarvis-safe"}`,
    `sessão ${currentSessionId ? currentSessionId.slice(0, 6) : "nova"}`,
    `workspace ${workspaceInput.value.trim() || "none"}`,
    active ? `arquivo ${active.path}` : "sem arquivo",
    dirtyCount ? `${dirtyCount} aba(s) pendente(s)` : "abas salvas",
    terminalSessionId ? `terminal ${terminalSessionId.slice(0, 6)}` : "sem terminal",
  ];
  workbenchStatusEl.innerHTML = parts
    .filter(Boolean)
    .map((part) => `<span class="status-pill">${escapeHtml(part)}</span>`)
    .join("");
}

function persistCurrentSessionId() {
  if (currentSessionId) {
    localStorage.setItem(STORAGE_KEY, currentSessionId);
  } else {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function loadContextPrefs() {
  try {
    const raw = localStorage.getItem(CONTEXT_PREFS_KEY);
    if (!raw) return;
    const prefs = JSON.parse(raw);
    contextActiveFileCheckbox.checked = Boolean(prefs.activeFile);
    contextOpenTabsCheckbox.checked = Boolean(prefs.openTabs);
    contextTerminalCheckbox.checked = Boolean(prefs.terminal);
    contextSearchCheckbox.checked = Boolean(prefs.search);
  } catch {
    // ignore
  }
}

function persistContextPrefs() {
  const prefs = {
    activeFile: contextActiveFileCheckbox.checked,
    openTabs: contextOpenTabsCheckbox.checked,
    terminal: contextTerminalCheckbox.checked,
    search: contextSearchCheckbox.checked,
  };
  localStorage.setItem(CONTEXT_PREFS_KEY, JSON.stringify(prefs));
}

function loadObsidianPrefs() {
  try {
    const raw = localStorage.getItem(OBSIDIAN_PREFS_KEY);
    if (!raw) return;
    const prefs = JSON.parse(raw);
    obsidianAutoRememberCheckbox.checked = prefs.autoRemember !== false;
    obsidianAutoIndexCheckbox.checked = Boolean(prefs.autoIndex);
  } catch {
    obsidianAutoRememberCheckbox.checked = true;
    obsidianAutoIndexCheckbox.checked = false;
  }
}

function persistObsidianPrefs() {
  const prefs = {
    autoRemember: obsidianAutoRememberCheckbox.checked,
    autoIndex: obsidianAutoIndexCheckbox.checked,
  };
  localStorage.setItem(OBSIDIAN_PREFS_KEY, JSON.stringify(prefs));
}

function clearReplayTimer() {
  if (replayTimer) {
    window.clearInterval(replayTimer);
    replayTimer = null;
  }
}

function renderReplayStatus() {
  if (!replayMode) {
    replayStatusEl.textContent = "Replay inativo.";
    replayToggleButton.textContent = "Pausar";
    return;
  }
  replayStatusEl.textContent = `Replay ${Math.min(replayIndex, replaySourceMessages.length)}/${replaySourceMessages.length} · ${replayPlaying ? "rodando" : "pausado"} · origem: ${replayOriginLabel}`;
  replayToggleButton.textContent = replayPlaying ? "Pausar" : "Continuar";
}

function stopSessionReplay(options = {}) {
  clearReplayTimer();
  replayMode = false;
  replayPlaying = false;
  replayIndex = 0;
  replayStartOffset = 0;
  replayOriginLabel = "sessão inteira";
  replaySourceMessages = [];
  renderReplayStatus();
  if (options.render !== false) {
    renderMessages();
  }
}

function replayNextMessage() {
  if (!replayMode) return;
  if (replayIndex >= replaySourceMessages.length) {
    replayPlaying = false;
    clearReplayTimer();
    renderReplayStatus();
    return;
  }
  replayIndex += 1;
  renderReplayStatus();
  renderMessages();
  if (replayIndex >= replaySourceMessages.length) {
    replayPlaying = false;
    clearReplayTimer();
    renderReplayStatus();
  }
}

function startReplayTimer() {
  clearReplayTimer();
  replayPlaying = true;
  renderReplayStatus();
  replayTimer = window.setInterval(() => {
    replayNextMessage();
  }, 700);
}

function toggleReplayPlayback() {
  if (!replayMode) return;
  if (replayPlaying) {
    replayPlaying = false;
    clearReplayTimer();
    renderReplayStatus();
    return;
  }
  startReplayTimer();
}

function startSessionReplay(options = {}) {
  if (!messages.length) {
    announceAssistantMessage("Nenhuma mensagem salva para reproduzir nesta sessão.");
    return;
  }
  const fromIndex = Math.max(0, Number(options.fromIndex || 0));
  const sourceMessages = messages.slice(fromIndex);
  if (!sourceMessages.length) {
    announceAssistantMessage("Não há mensagens suficientes a partir desse checkpoint para reproduzir.");
    return;
  }
  clearReplayTimer();
  replayMode = true;
  replayPlaying = false;
  replayIndex = 0;
  replayStartOffset = fromIndex;
  replayOriginLabel = options.label || (fromIndex > 0 ? `mensagem ${fromIndex}` : "sessão inteira");
  replaySourceMessages = sourceMessages.map((message) => ({ ...message }));
  renderReplayStatus();
  renderMessages();
  startReplayTimer();
}

function renderMessages() {
  messagesEl.innerHTML = "";
  const sourceMessages = replayMode ? replaySourceMessages.slice(0, replayIndex) : messages;
  if (!sourceMessages.length) {
    appendMessageElement("assistant", replayMode ? "Replay iniciado. Aguardando primeira mensagem..." : "Jarvis pronto. Escolha um perfil e envie sua mensagem.");
    renderWorkbenchStatus();
    return;
  }
  for (const message of sourceMessages) {
    appendMessageElement(message.role, message.display_content || message.content, message.metadata || null, message.attachments || []);
  }
  renderWorkbenchStatus();
}

function formatMessageMetadata(metadata) {
  if (!metadata || typeof metadata !== "object") return "";
  const parts = [];
  if (metadata.effective_agent) parts.push(`agente: ${metadata.effective_agent}`);
  if (metadata.route_kind) parts.push(`rota: ${metadata.route_kind}`);
  if (metadata.primary_model) parts.push(`modelo: ${metadata.primary_model}`);
  if (metadata.workspace) parts.push(`workspace: ${metadata.workspace}`);
  return parts.join(" | ");
}

function renderAttachments() {
  attachmentsEl.innerHTML = "";
  if (!pendingAttachments.length) {
    renderComposerContextPreview();
    return;
  }
  for (const attachment of pendingAttachments) {
    const chip = document.createElement("div");
    chip.className = "attachment-chip";
    const label = document.createElement("span");
    label.textContent = `${attachment.name} (${formatSize(attachment.size)})`;
    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.textContent = "x";
    removeButton.addEventListener("click", () => {
      pendingAttachments = pendingAttachments.filter((item) => item.id !== attachment.id);
      renderAttachments();
    });
    chip.append(label, removeButton);
    attachmentsEl.appendChild(chip);
  }
  renderComposerContextPreview();
  renderWorkbenchStatus();
}

async function loadWorkspaceTree() {
  const payload = await api("/api/workspace/tree");
  workspaceTree = payload.tree;
  renderWorkspaceTree();
}

async function searchWorkspace() {
  const query = (workspaceSearchInput.value || "").trim();
  if (!query) {
    workspaceSearchResults = [];
    renderWorkspaceSearchResults();
    return;
  }
  const payload = await api(`/api/workspace/search?q=${encodeURIComponent(query)}&limit=40`);
  workspaceSearchResults = payload.results || [];
  renderWorkspaceSearchResults();
}

async function loadTerminalSessions() {
  const payload = await api("/api/terminal/sessions");
  terminalSessions = payload.sessions || [];
  if (terminalSessionId && !terminalSessions.some((session) => session.session_id === terminalSessionId)) {
    terminalSessionId = null;
    terminalBuffer = "";
  }
  renderTerminalSessions();
  renderWorkbenchStatus();
}

async function createTerminalSession() {
  const payload = await api(`/api/terminal/sessions?session_id=${encodeURIComponent(currentSessionId || "")}`, {
    method: "POST",
    body: JSON.stringify({
      cwd: terminalCwdEl.value.trim() || null,
      cols: 120,
      rows: 28,
    }),
  });
  terminalSessionId = payload.session.session_id;
  terminalBuffer = payload.session.output || "";
  terminalBuffers[terminalSessionId] = terminalBuffer;
  await loadTerminalSessions();
  renderTerminal();
  startTerminalPolling();
}

async function startTerminalSession() {
  await loadTerminalSessions();
  if (terminalSessionId) {
    terminalBuffer = terminalBuffers[terminalSessionId] || terminalBuffer;
    renderTerminal();
    startTerminalPolling();
    return;
  }
  if (terminalSessions.length) {
    terminalSessionId = terminalSessions[0].session_id;
    terminalBuffer = terminalBuffers[terminalSessionId] || "";
    renderTerminal();
    startTerminalPolling();
    return;
  }
  await createTerminalSession();
}

async function restartTerminal() {
  stopTerminalPolling();
  if (terminalSessionId) {
    try {
      await api(`/api/terminal/sessions/${terminalSessionId}`, { method: "DELETE" });
    } catch {
      // ignore
    }
  }
  delete terminalBuffers[terminalSessionId];
  terminalSessionId = null;
  terminalBuffer = "Reiniciando terminal...\n";
  renderTerminal();
  await createTerminalSession();
}

async function closeActiveTerminalSession() {
  if (!terminalSessionId) return;
  const closingId = terminalSessionId;
  stopTerminalPolling();
  await api(`/api/terminal/sessions/${closingId}`, { method: "DELETE" });
  delete terminalBuffers[closingId];
  terminalSessions = terminalSessions.filter((session) => session.session_id !== closingId);
  terminalSessionId = terminalSessions[0]?.session_id || null;
  terminalBuffer = terminalSessionId ? (terminalBuffers[terminalSessionId] || "") : "";
  renderTerminalSessions();
  renderTerminal();
  if (terminalSessionId) {
    startTerminalPolling();
  } else {
    await createTerminalSession();
  }
}

function renderTerminalSessions() {
  terminalSessionsEl.innerHTML = "";
  if (!terminalSessions.length) {
    const empty = document.createElement("div");
    empty.className = "terminal-session-empty";
    empty.textContent = "Sem terminais ativos.";
    terminalSessionsEl.appendChild(empty);
    return;
  }
  for (const session of terminalSessions) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "terminal-session-chip secondary";
    if (session.session_id === terminalSessionId) {
      button.classList.add("active");
    }
    const shortId = session.session_id.slice(0, 6);
    button.textContent = `${session.cwd || "."} · ${shortId}`;
    button.addEventListener("click", async () => {
      await switchTerminalSession(session.session_id);
    });
    terminalSessionsEl.appendChild(button);
  }
}

async function switchTerminalSession(sessionId) {
  if (!sessionId || sessionId === terminalSessionId) return;
  stopTerminalPolling();
  terminalSessionId = sessionId;
  terminalBuffer = terminalBuffers[sessionId] || "";
  renderTerminalSessions();
  renderTerminal();
  await pollTerminalOutputOnce(40);
  startTerminalPolling();
}

function startTerminalPolling() {
  stopTerminalPolling();
  terminalPollTimer = window.setInterval(() => {
    pollTerminalOutputOnce().catch((error) => {
      terminalBuffer += `\n[terminal error] ${error.message}\n`;
      renderTerminal();
    });
  }, 500);
}

function stopTerminalPolling() {
  if (terminalPollTimer) {
    window.clearInterval(terminalPollTimer);
    terminalPollTimer = null;
  }
}

async function pollTerminalOutputOnce(waitMs = 0) {
  if (!terminalSessionId) return;
  const payload = await api(`/api/terminal/sessions/${terminalSessionId}/read?wait_ms=${waitMs}`);
  const result = payload.result;
  if (result.output) {
    terminalBuffer += result.output;
    terminalBuffers[terminalSessionId] = terminalBuffer;
    renderTerminal();
  }
  if (result.alive === false) {
    stopTerminalPolling();
    await loadTerminalSessions();
  }
}

async function sendTerminalData(data) {
  if (!terminalSessionId) return;
  const payload = await api(`/api/terminal/sessions/${terminalSessionId}/write?chat_session_id=${encodeURIComponent(currentSessionId || "")}`, {
    method: "POST",
    body: JSON.stringify({ data, wait_ms: 60 }),
  });
  const result = payload.result;
  if (result.output) {
    terminalBuffer += result.output;
    terminalBuffers[terminalSessionId] = terminalBuffer;
    renderTerminal();
  }
}

function renderTerminal() {
  terminalOutputEl.textContent = terminalBuffer || "Terminal pronto.";
  terminalOutputEl.scrollTop = terminalOutputEl.scrollHeight;
  renderComposerContextPreview();
}

function mapTerminalKey(event) {
  switch (event.key) {
    case "Enter":
      return "\r";
    case "Backspace":
      return "\x7f";
    case "Tab":
      return "\t";
    case "ArrowUp":
      return "\x1b[A";
    case "ArrowDown":
      return "\x1b[B";
    case "ArrowRight":
      return "\x1b[C";
    case "ArrowLeft":
      return "\x1b[D";
    case "Escape":
      return "\x1b";
    default:
      return null;
  }
}

function renderWorkspaceTree() {
  workspaceFilesEl.innerHTML = "";
  if (!workspaceTree) {
    workspaceFilesEl.textContent = "Nenhum arquivo carregado.";
    return;
  }
  const rootList = document.createElement("div");
  rootList.className = "workspace-tree-root";
  renderWorkspaceNode(workspaceTree, rootList, 0);
  workspaceFilesEl.appendChild(rootList);
}

function renderWorkspaceSearchResults() {
  workspaceSearchResultsEl.innerHTML = "";
  if (!workspaceSearchResults.length) {
    renderComposerContextPreview();
    return;
  }
  for (const result of workspaceSearchResults) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "workspace-search-card secondary";
    const snippet = result.snippet ? `\n${result.snippet}` : "";
    card.textContent = `${result.path}${snippet}`;
    card.addEventListener("click", () => openWorkspaceFile(result.path));
    workspaceSearchResultsEl.appendChild(card);
  }
  renderComposerContextPreview();
}

function renderEditorTabs() {
  editorTabsEl.innerHTML = "";
  if (!openEditors.length) return;
  for (const editor of openEditors) {
    const tab = document.createElement("button");
    tab.type = "button";
    tab.className = "editor-tab";
    if (editor.path === currentOpenFilePath) {
      tab.classList.add("active");
    }
    const label = editor.dirty ? `${editor.path} *` : editor.path;
    tab.textContent = label;
    tab.addEventListener("click", () => {
      currentOpenFilePath = editor.path;
      syncEditorFromState();
      renderEditorTabs();
      renderWorkspaceTree();
    });
    const closeButton = document.createElement("span");
    closeButton.className = "editor-tab-close";
    closeButton.textContent = "×";
    closeButton.addEventListener("click", (event) => {
      event.stopPropagation();
      closeEditor(editor.path);
    });
    tab.appendChild(closeButton);
    editorTabsEl.appendChild(tab);
  }
  renderWorkbenchStatus();
}

function getCurrentEditor() {
  return openEditors.find((editor) => editor.path === currentOpenFilePath) || null;
}

function announceAssistantMessage(content) {
  messages.push({ role: "assistant", content, transient: true });
  renderMessages();
  scheduleSessionUiStateSave();
}

function loadRecentFiles() {
  try {
    const raw = localStorage.getItem(RECENT_FILES_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      recentFiles = parsed.filter((item) => typeof item === "string");
    }
  } catch {
    recentFiles = [];
  }
}

function persistRecentFiles() {
  localStorage.setItem(RECENT_FILES_KEY, JSON.stringify(recentFiles));
}

function loadCommandHistory() {
  try {
    const raw = localStorage.getItem(COMMAND_HISTORY_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      commandHistory = parsed.filter((item) => typeof item === "string");
    }
  } catch {
    commandHistory = [];
  }
}

function persistCommandHistory() {
  localStorage.setItem(COMMAND_HISTORY_KEY, JSON.stringify(commandHistory));
}

function trackCommandHistory(command) {
  const normalized = String(command || "").trim();
  if (!normalized) return;
  commandHistory = [normalized, ...commandHistory.filter((item) => item !== normalized)].slice(0, 12);
  persistCommandHistory();
  renderCommandHistory();
}

async function saveAllEditors() {
  const dirtyEditors = openEditors.filter((editor) => editor.dirty);
  if (!dirtyEditors.length) {
    announceAssistantMessage("Nenhuma aba pendente para salvar.");
    return;
  }
  for (const editor of dirtyEditors) {
    await api(`/api/workspace/file?session_id=${encodeURIComponent(currentSessionId || "")}`, {
      method: "PUT",
      body: JSON.stringify({ path: editor.path, content: editor.content }),
    });
    editor.dirty = false;
  }
  renderEditorTabs();
  syncEditorHeader();
  await loadWorkspaceTree();
  await appendSessionOperation({
    kind: "save_all_files",
    title: "Salvou abas pendentes",
    detail: `${dirtyEditors.length} arquivo(s) salvo(s)`,
  });
  announceAssistantMessage(`${dirtyEditors.length} aba(s) salva(s).`);
}

async function attachOpenTabsToChat() {
  if (!openEditors.length) {
    announceAssistantMessage("Nenhuma aba aberta para anexar.");
    return;
  }
  const created = [];
  for (const editor of openEditors) {
    const id = `workspace-tab-${editor.path}-${Date.now()}-${created.length}`;
    pendingAttachments.push({
      id,
      name: editor.path,
      content: editor.content,
      size: new Blob([editor.content]).size,
    });
    created.push(editor.path);
  }
  renderAttachments();
  await appendSessionOperation({
    kind: "attach_open_tabs",
    title: "Anexou abas abertas ao chat",
    detail: `${created.length} arquivo(s) anexado(s)`,
  });
  announceAssistantMessage(`${created.length} aba(s) anexada(s) ao próximo prompt.`);
  scheduleSessionUiStateSave();
}

async function runEditorSelectionInTerminal() {
  const active = getCurrentEditor();
  if (!active || !editorSelection || editorSelection.path !== active.path) {
    announceAssistantMessage("Selecione um trecho do arquivo ativo para executar no terminal.");
    return;
  }
  const command = editorSelection.text.trim();
  if (!command) {
    announceAssistantMessage("A seleção está vazia para execução no terminal.");
    return;
  }
  terminalCommandEl.value = command;
  await sendTerminalData(`${command}
`);
  trackCommandHistory(command);
  await appendSessionOperation({
    kind: "run_selection",
    title: `Executou seleção em ${active.path}`,
    path: active.path,
    command,
    detail: `range ${editorSelection.start}-${editorSelection.end}`,
  });
  announceAssistantMessage("Seleção enviada ao terminal.");
  scheduleSessionUiStateSave();
}

function trackRecentFile(path) {
  if (!path) return;
  recentFiles = [path, ...recentFiles.filter((item) => item !== path)].slice(0, 10);
  persistRecentFiles();
  renderRecentFiles();
}

function renderRecentFiles() {
  recentFilesEl.innerHTML = "";
  if (!recentFiles.length) {
    recentFilesEl.textContent = "Nenhum arquivo recente ainda.";
    return;
  }
  for (const item of recentFiles) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "secondary recent-file-chip";
    button.textContent = item;
    button.addEventListener("click", async () => {
      await openWorkspaceFile(item);
    });
    recentFilesEl.appendChild(button);
  }
}

function slugifyLabel(value) {
  return String(value || "note")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "") || "note";
}

function isMarkdownNote(path) {
  return /\.(md|markdown)$/i.test(path || "");
}

function resolveWorkspaceHint(path) {
  const explicit = (workspaceInput.value || "").trim();
  if (explicit) return explicit;
  const match = String(path || "").match(/data\/knowledge\/([^/]+)\/obsidian\//i);
  if (match) return match[1];
  return "jarvis";
}

function extractMarkdownTitle(content, fallback) {
  const match = String(content || "").match(/^#\s+(.+)$/m);
  return (match?.[1] || fallback || "Jarvis Note").trim();
}

function renderGitOutput() {
  gitOutputEl.textContent = latestGitContext || "Nenhum contexto Git carregado ainda.";
  renderComposerContextPreview();
}

function buildGitCommand(mode) {
  switch (mode) {
    case "status":
      return "git status --short --branch";
    case "diff":
      return "git diff --stat && printf '\n---\n' && git diff --";
    case "log":
      return "git log --oneline -5";
    case "github":
      return "command -v gh >/dev/null 2>&1 && (gh repo view --json nameWithOwner,url,defaultBranchRef 2>/dev/null || gh auth status 2>/dev/null) || echo 'GitHub CLI nao disponivel no sistema.'";
    case "prs":
      return "command -v gh >/dev/null 2>&1 && gh pr list --limit 5 || echo 'GitHub CLI nao disponivel no sistema.'";
    case "issues":
      return "command -v gh >/dev/null 2>&1 && gh issue list --limit 5 || echo 'GitHub CLI nao disponivel no sistema.'";
    default:
      return "";
  }
}

function buildGitLabel(mode) {
  switch (mode) {
    case "status":
      return "status";
    case "diff":
      return "diff";
    case "log":
      return "log";
    case "github":
      return "github";
    case "prs":
      return "prs";
    case "issues":
      return "issues";
    default:
      return "git";
  }
}

async function runGitCommand(mode) {
  const command = buildGitCommand(mode);
  if (!command) return "";
  const payload = await api(`/api/terminal/run?session_id=${encodeURIComponent(currentSessionId || "")}`, {
    method: "POST",
    body: JSON.stringify({
      command,
      cwd: ".",
    }),
  });
  const result = payload.result || {};
  const output = String(result.output || "").trim();
  const exitCode = result.exit_code;
  const label = buildGitLabel(mode);
  latestGitContext = [
    `[GIT_${label.toUpperCase()}]`,
    `$ ${command}`,
    exitCode !== undefined ? `exit_code: ${exitCode}` : null,
    output || "[sem saida]",
  ]
    .filter(Boolean)
    .join("\n");
  renderGitOutput();
  await appendSessionOperation({
    kind: `git_${label}`,
    title: `Consultou Git ${label}`,
    command,
    detail: exitCode !== undefined ? `exit ${exitCode}` : "painel Git",
    path: getCurrentEditor()?.path || null,
  });
  return latestGitContext;
}

async function loadGitContext(mode) {
  gitOutputEl.textContent = "Carregando contexto Git...";
  try {
    const output = await runGitCommand(mode);
    if (!output.trim()) {
      gitOutputEl.textContent = "Comando Git executado sem saida visivel.";
    }
  } catch (error) {
    latestGitContext = `[GIT_ERROR] ${error.message}`;
    renderGitOutput();
  }
}

function readGitHubTarget(promptLabel, fallback = "") {
  const inline = (githubTargetInput?.value || "").trim();
  if (inline) return inline;
  return (window.prompt(promptLabel, fallback) || "").trim();
}

function readGitHubTitle(promptLabel, fallback = "") {
  const inline = (githubTitleInput?.value || "").trim();
  if (inline) return inline;
  return (window.prompt(promptLabel, fallback) || "").trim();
}

function buildGitHubBody(title) {
  const active = getCurrentEditor();
  const parts = [
    `Contexto gerado pelo Jarvis: ${title}`,
  ];
  if (active) {
    parts.push(`Arquivo ativo: ${active.path}`);
    parts.push("");
    parts.push("Trecho do arquivo ativo:");
    parts.push(truncateContext(active.content, 1500));
  }
  if (terminalBuffer.trim()) {
    parts.push("");
    parts.push("Terminal recente:");
    parts.push(truncateContext(terminalBuffer, 1500));
  }
  if (latestGitContext.trim()) {
    parts.push("");
    parts.push("Contexto Git:");
    parts.push(truncateContext(latestGitContext, 1500));
  }
  return parts.join("\n");
}

async function queueGitHubApproval(command, title, detail) {
  await queueApproval({
    kind: "terminal_command",
    title,
    command,
    detail,
    path: getCurrentEditor()?.path || null,
    payload: { command, cwd: "." },
  });
  await appendSessionOperation({
    kind: "github_queue_command",
    title,
    command,
    detail,
    path: getCurrentEditor()?.path || null,
  });
}

async function promptGitHubAction(mode) {
  let value = "";
  if (mode === "pr-view") {
    value = readGitHubTarget("Número da PR para visualizar:", "1");
    if (!value.trim()) return;
    await queueGitHubApproval(`gh pr view ${value.trim()} --comments`, `Visualizar PR #${value.trim()}`, "ação GitHub via gh enfileirada");
    announceAssistantMessage(`PR #${value.trim()} enviada para a fila do Jarvis.`);
    return;
  }
  if (mode === "pr-checkout") {
    value = readGitHubTarget("Número da PR para checkout:", "1");
    if (!value.trim()) return;
    await queueGitHubApproval(`gh pr checkout ${value.trim()}`, `Checkout da PR #${value.trim()}`, "ação GitHub via gh enfileirada");
    announceAssistantMessage(`Checkout da PR #${value.trim()} enviado para a fila do Jarvis.`);
    return;
  }
  if (mode === "issue-view") {
    value = readGitHubTarget("Número da issue para visualizar:", "1");
    if (!value.trim()) return;
    await queueGitHubApproval(`gh issue view ${value.trim()} --comments`, `Visualizar issue #${value.trim()}`, "ação GitHub via gh enfileirada");
    announceAssistantMessage(`Issue #${value.trim()} enviada para a fila do Jarvis.`);
    return;
  }
  if (mode === "pr-diff") {
    value = readGitHubTarget("Número da PR para diff:", "1");
    if (!value.trim()) return;
    await queueGitHubApproval(`gh pr diff ${value.trim()}`, `Diff da PR #${value.trim()}`, "ação GitHub via gh enfileirada");
    announceAssistantMessage(`Diff da PR #${value.trim()} enviado para a fila do Jarvis.`);
    return;
  }
  if (mode === "pr-create") {
    value = readGitHubTitle("Título da PR para criar:", "melhorar fluxo do jarvis");
    if (!value.trim()) return;
    const body = buildGitHubBody(value.trim());
    await queueGitHubApproval(`gh pr create --title ${JSON.stringify(value.trim())} --body ${JSON.stringify(body)}`, `Criar PR: ${value.trim()}`, "ação GitHub via gh enfileirada");
    announceAssistantMessage("Criação da PR enviada para a fila do Jarvis.");
    return;
  }
  if (mode === "issue-create") {
    value = readGitHubTitle("Título da issue para criar:", "corrigir lentidao do chat");
    if (!value.trim()) return;
    const body = buildGitHubBody(value.trim());
    await queueGitHubApproval(`gh issue create --title ${JSON.stringify(value.trim())} --body ${JSON.stringify(body)}`, `Criar issue: ${value.trim()}`, "ação GitHub via gh enfileirada");
    announceAssistantMessage(`Criação da issue enviada para a fila do Jarvis.`);
  }
}

async function attachGitContextToChat() {
  if (!latestGitContext.trim()) {
    await loadGitContext("status");
  }
  if (!latestGitContext.trim()) {
    announceAssistantMessage("Nao foi possivel carregar contexto Git para anexar.");
    return;
  }
  pendingAttachments.push({
    id: `git-context-${Date.now()}`,
    name: "git-context.txt",
    content: latestGitContext,
    size: new Blob([latestGitContext]).size,
  });
  renderAttachments();
  await appendSessionOperation({
    kind: "git_attach",
    title: "Anexou contexto Git ao chat",
    detail: "status/diff/log pronto para o proximo prompt",
    path: getCurrentEditor()?.path || null,
  });
  announceAssistantMessage("Contexto Git anexado ao proximo prompt.");
  scheduleSessionUiStateSave();
}

function renderApprovals() {
  approvalsEl.innerHTML = "";
  if (!currentApprovals.length) {
    approvalsEl.textContent = "Nenhuma ação pendente.";
    return;
  }
  for (const approval of [...currentApprovals].reverse()) {
    const card = document.createElement("div");
    card.className = `approval-card ${approval.status || "pending"}`;

    const title = document.createElement("div");
    title.className = "approval-card-title";
    title.textContent = `${approval.title || approval.kind || "ação"} · ${approval.status || "pending"}`;

    const meta = document.createElement("div");
    meta.className = "approval-card-meta";
    meta.textContent = [approval.path, approval.command, approval.created_at].filter(Boolean).join("\n");

    const preview = document.createElement("pre");
    preview.className = "approval-card-preview";
    preview.textContent = buildApprovalPreview(approval);

    const actions = document.createElement("div");
    actions.className = "approval-card-actions";

    const applyButton = document.createElement("button");
    applyButton.type = "button";
    applyButton.className = "secondary";
    applyButton.textContent = approval.status === "pending" ? "Aplicar" : "Aplicado";
    applyButton.disabled = approval.status !== "pending";
    applyButton.addEventListener("click", async () => {
      await actOnApproval(approval.id, "apply");
    });

    const rejectButton = document.createElement("button");
    rejectButton.type = "button";
    rejectButton.className = "secondary danger";
    rejectButton.textContent = approval.status === "pending" ? "Rejeitar" : "Fechado";
    rejectButton.disabled = approval.status !== "pending";
    rejectButton.addEventListener("click", async () => {
      await actOnApproval(approval.id, "reject");
    });

    actions.append(applyButton, rejectButton);
    card.append(title, meta, actions, preview);
    approvalsEl.appendChild(card);
  }
}

function buildApprovalPreview(approval) {
  const payload = approval.payload || {};
  if (approval.kind === "terminal_command") {
    return [`$ ${approval.command || payload.command || ""}`, approval.detail || ""].filter(Boolean).join("\n");
  }
  if (approval.kind === "file_edit") {
    return payload.diff || payload.proposed_content || approval.detail || "[sem diff]";
  }
  if (approval.kind === "batch_edit") {
    const files = Array.isArray(payload.files) ? payload.files : [];
    return [approval.detail || "Lote de arquivos", ...files.map((item) => item.path || "[arquivo]")].join("\n");
  }
  return approval.detail || JSON.stringify(payload, null, 2);
}

async function queueApproval(request) {
  if (!currentSessionId) return null;
  const payload = await api(`/api/chat/sessions/${currentSessionId}/approvals`, {
    method: "POST",
    body: JSON.stringify(request),
  });
  currentApprovals = payload.session.approvals || [];
  renderApprovals();
  return payload.approval;
}

async function actOnApproval(approvalId, action) {
  if (!currentSessionId) return;
  const payload = await api(`/api/chat/sessions/${currentSessionId}/approvals/${approvalId}`, {
    method: "POST",
    body: JSON.stringify({ action }),
  });
  currentApprovals = payload.session.approvals || [];
  currentSessionOperations = payload.session.operations || currentSessionOperations;
  renderApprovals();
  renderSessionOperations();
  if (action === "apply") {
    if (payload.result?.output) {
      terminalBuffer += `
[jarvis approval]
${payload.result.output}
`;
      if (terminalSessionId) terminalBuffers[terminalSessionId] = terminalBuffer;
      renderTerminal();
    }
    if (payload.approval?.kind === "file_edit") {
      const updatedPath = payload.approval.path || payload.approval.payload?.path;
      if (updatedPath) {
        const openEditor = openEditors.find((item) => item.path === updatedPath);
        const proposed = payload.approval.payload?.proposed_content;
        if (openEditor && typeof proposed === "string") {
          openEditor.content = proposed;
          openEditor.dirty = false;
          if (currentOpenFilePath === updatedPath) fileEditorEl.value = proposed;
          renderEditorTabs();
          syncEditorHeader();
        }
      }
    }
  }
  announceAssistantMessage(action === "apply" ? "Ação aplicada na fila do Jarvis." : "Ação rejeitada na fila do Jarvis.");
}

async function queueSuggestedCommandApproval() {
  const command = pendingTaskAssist?.suggested_command?.trim();
  if (!command) {
    announceAssistantMessage("Nenhum comando sugerido disponível para enviar à fila.");
    return;
  }
  await queueApproval({
    kind: "terminal_command",
    title: "Comando sugerido pelo Jarvis",
    path: getCurrentEditor()?.path || null,
    command,
    detail: pendingTaskAssist?.summary || "Comando gerado pelo assistente operacional",
    payload: { command, cwd: getCurrentEditor()?.path?.includes("/") ? getCurrentEditor().path.slice(0, getCurrentEditor().path.lastIndexOf("/")) : "." },
  });
  await appendSessionOperation({ kind: "approval_queue_command", title: "Enfileirou comando sugerido", command, path: getCurrentEditor()?.path || null, detail: "fila operacional do Jarvis" });
  announceAssistantMessage("Comando sugerido enviado para a fila de ações.");
}

async function queueEditProposalApproval() {
  const active = getCurrentEditor();
  if (!active || !pendingEditProposal || pendingEditProposal.path !== active.path) {
    announceAssistantMessage("Nenhuma proposta de edição ativa para enviar à fila.");
    return;
  }
  await queueApproval({
    kind: "file_edit",
    title: `Diff proposto para ${active.path}`,
    path: active.path,
    detail: pendingEditProposal.instruction || editorInstructionEl.value || "Aplicar diff atual",
    payload: {
      path: active.path,
      proposed_content: pendingEditProposal.proposed_content,
      diff: pendingEditProposal.diff,
      instruction: pendingEditProposal.instruction || null,
    },
  });
  await appendSessionOperation({ kind: "approval_queue_edit", title: `Enfileirou diff ${active.path}`, path: active.path, detail: "diff pronto para aplicar" });
  announceAssistantMessage("Diff atual enviado para a fila de ações.");
}

async function runSelfImproveActive() {
  const active = getCurrentEditor();
  if (!active) {
    announceAssistantMessage("Abra um arquivo no editor antes de pedir autoaprimoramento.");
    return;
  }
  editorTaskOutputEl.textContent = "Jarvis está revisando o arquivo ativo para autoaprimoramento...";
  const instruction = [
    "Revise este arquivo do workspace como um agente de autoaprimoramento local.",
    "Priorize correções objetivas, clareza, manutenção e consistência com o projeto.",
    "Se fizer sentido, sugira um comando bash de validação e uma edição concreta no arquivo.",
  ].join(" ");
  try {
    const payload = await api("/api/workspace/task-assist", {
      method: "POST",
      body: JSON.stringify({
        instruction,
        model: modelSelect.value,
        path: active.path,
        content: active.content,
        workspace: workspaceInput.value.trim() || null,
        terminal_output: terminalBuffer.slice(-6000),
      }),
    });
    pendingTaskAssist = payload;
    pendingEditProposal = payload.edit_proposal
      ? { ...payload.edit_proposal, hunks: (payload.edit_proposal.hunks || []).map((hunk) => ({ ...hunk, applied: false })) }
      : null;
    renderTaskAssist();
    renderEditProposal();
    let queued = 0;
    if (payload.suggested_command) {
      await queueSuggestedCommandApproval();
      queued += 1;
    }
    if (payload.edit_proposal) {
      await queueEditProposalApproval();
      queued += 1;
    }
    await appendSessionOperation({ kind: "self_improve", title: `Autoaprimorou análise de ${active.path}`, path: active.path, detail: `${queued} ação(ões) enviada(s) para a fila` });
    announceAssistantMessage(`Autoaprimoramento concluído para ${active.path}. ${queued} ação(ões) foram enviadas para a fila.`);
  } catch (error) {
    editorTaskOutputEl.textContent = `Erro no autoaprimoramento: ${error.message}`;
  }
}

function renderCommandHistory() {
  commandHistoryEl.innerHTML = "";
  if (!commandHistory.length) {
    commandHistoryEl.textContent = "Nenhum comando recente ainda.";
    return;
  }
  for (const command of commandHistory) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "secondary command-history-chip";
    button.textContent = command;
    button.addEventListener("click", () => {
      terminalCommandEl.value = command;
      terminalCommandEl.focus();
    });
    commandHistoryEl.appendChild(button);
  }
}

function renderSlashCommands() {
  slashCommandsEl.innerHTML = "";
  for (const command of SLASH_COMMANDS) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "secondary slash-command-chip";
    button.textContent = command.label;
    button.addEventListener("click", async () => {
      if (command.mode === "fill") {
        promptEl.value = command.value;
        promptEl.focus();
        return;
      }
      const handled = await handleSlashCommand(command.value);
      if (handled) {
        promptEl.value = "";
      }
    });
    slashCommandsEl.appendChild(button);
  }
}

function renderObsidianStatus() {
  const active = getCurrentEditor();
  if (!active) {
    obsidianStatusEl.textContent = "Abra uma nota Markdown para usar memória e conhecimento do Obsidian no Jarvis.";
    return;
  }
  if (!isMarkdownNote(active.path)) {
    obsidianStatusEl.textContent = [
      `Arquivo ativo: ${active.path}`,
      "Este arquivo não é uma nota Markdown.",
      "Abra uma nota .md para lembrar ou indexar contexto do Obsidian.",
].join("\n");
    return;
  }
  const workspace = resolveWorkspaceHint(active.path);
  const title = extractMarkdownTitle(active.content, active.path.split("/").pop()?.replace(/\.md$/i, ""));
  obsidianStatusEl.textContent = [
    `Nota ativa: ${active.path}`,
    `Título: ${title}`,
    `Workspace alvo: ${workspace}`,
    `Tamanho: ${active.content.length} chars`,
    "Ações: lembrar na memória, indexar para RAG, usar como base do chat.",
  ].join("\n");
}

function syncEditorHeader() {
  const active = getCurrentEditor();
  editorPathEl.textContent = active ? (active.dirty ? `${active.path} *` : active.path) : "Nenhum arquivo aberto";
}

function syncEditorFromState() {
  const active = getCurrentEditor();
  fileEditorEl.value = active?.content || "";
  syncEditorHeader();
  syncEditorSelection();
  renderTaskAssist();
  renderBatchProposal();
  renderEditProposal();
  renderObsidianStatus();
  renderComposerContextPreview();
}

function closeEditor(path, options = {}) {
  const target = openEditors.find((editor) => editor.path === path);
  if (target?.dirty && !window.confirm(`Fechar ${path} sem salvar?`)) {
    return;
  }
  openEditors = openEditors.filter((editor) => editor.path !== path);
  if (currentOpenFilePath === path) {
    currentOpenFilePath = openEditors[openEditors.length - 1]?.path || null;
  }
  if (pendingEditProposal?.path === path) {
    pendingEditProposal = null;
  }
  if (pendingBatchProposal?.proposals?.some((proposal) => proposal.path === path)) {
    pendingBatchProposal = null;
  }
  if (pendingTaskAssist?.edit_proposal?.path === path) {
    pendingTaskAssist = null;
  }
  renderEditorTabs();
  syncEditorFromState();
  renderWorkspaceTree();
  if (options.persist !== false) {
    scheduleSessionUiStateSave();
  }
}

async function saveCurrentEditor() {
  const active = getCurrentEditor();
  if (!active) return;
  await api(`/api/workspace/file?session_id=${encodeURIComponent(currentSessionId || "")}`, {
    method: "PUT",
    body: JSON.stringify({ path: active.path, content: active.content }),
  });
  active.dirty = false;
  if (pendingEditProposal?.path === active.path) {
    pendingEditProposal = null;
  }
  if (pendingBatchProposal?.proposals?.some((proposal) => proposal.path === active.path)) {
    pendingBatchProposal = null;
  }
  if (pendingTaskAssist?.edit_proposal?.path === active.path) {
    pendingTaskAssist = null;
  }
  renderEditorTabs();
  syncEditorHeader();
  renderBatchProposal();
  renderTaskAssist();
  renderEditProposal();
  await loadWorkspaceTree();
  await appendSessionOperation({ kind: "file_save", title: `Salvou ${active.path}`, path: active.path, detail: "arquivo salvo no editor" });
  await runObsidianAssistOnSave(active);
}

function syncEditorSelection() {
  const active = getCurrentEditor();
  if (!active) {
    editorSelection = null;
    renderEditorSelection();
    return;
  }
  const start = fileEditorEl.selectionStart ?? 0;
  const end = fileEditorEl.selectionEnd ?? 0;
  if (end <= start) {
    editorSelection = null;
    renderEditorSelection();
    return;
  }
  editorSelection = {
    path: active.path,
    start,
    end,
    text: fileEditorEl.value.slice(start, end),
  };
  renderEditorSelection();
}

function renderEditorSelection() {
  if (!editorSelection) {
    editorSelectionEl.textContent = "Nenhuma seleção ativa.";
    return;
  }
  editorSelectionEl.textContent = [
    `Seleção: ${editorSelection.path}`,
    `Range: ${editorSelection.start}-${editorSelection.end}`,
    "",
    truncateContext(editorSelection.text, 700),
  ].join("\n");
}

function renderTaskAssist() {
  const active = getCurrentEditor();
  if (
    !active ||
    !pendingTaskAssist ||
    (pendingTaskAssist.edit_proposal && pendingTaskAssist.edit_proposal.path !== active.path)
  ) {
    editorTaskOutputEl.textContent = "Nenhuma tarefa operacional ainda.";
    return;
  }
  const lines = [];
  if (pendingTaskAssist.mode === "cycle") {
    lines.push("Modo: ciclo operacional");
    lines.push("");
  }
  if (pendingTaskAssist.initial) {
    lines.push(`Resumo inicial: ${pendingTaskAssist.initial.summary || "[sem resumo]"}`);
    lines.push(`Comando inicial: ${pendingTaskAssist.initial.suggested_command || "[nenhum]"}`);
    lines.push("");
  }
  lines.push(`Resumo atual: ${pendingTaskAssist.summary || "[sem resumo]"}`);
  lines.push("");
  lines.push(`Comando sugerido: ${pendingTaskAssist.suggested_command || "[nenhum]"}`);
  lines.push("");
  lines.push(`Instrução de edição: ${pendingTaskAssist.edit_instruction || "[nenhuma]"}`);
  if (pendingTaskAssist.command_result) {
    lines.push("");
    lines.push(`Saída do comando: ${pendingTaskAssist.command_result.exit_code ?? "[rodando]"}`);
    lines.push(trimTaskOutput(pendingTaskAssist.command_result.output || "[sem saída]"));
  }
  editorTaskOutputEl.textContent = lines.join("\n");
}

function renderBatchProposal() {
  editorBatchProposalsEl.innerHTML = "";
  if (!pendingBatchProposal?.proposals?.length) {
    editorBatchOutputEl.textContent = "Nenhuma proposta em lote ainda.";
    return;
  }
  const appliedFiles = pendingBatchProposal.proposals.filter((proposal) => proposal.applied).length;
  const lines = [
    `Resumo do lote: ${pendingBatchProposal.summary || "[sem resumo]"}`,
    `Arquivos propostos: ${pendingBatchProposal.proposals.length}`,
    `Arquivos aplicados: ${appliedFiles}`,
  ];
  if (pendingBatchProposal.applied) {
    lines.push("Status: lote aplicado parcialmente ou por completo.");
  }
  editorBatchOutputEl.textContent = lines.join("\n");

  for (const proposal of pendingBatchProposal.proposals) {
    const card = document.createElement("div");
    card.className = "editor-batch-card";
    if (proposal.applied) {
      card.classList.add("applied");
    }

    const title = document.createElement("div");
    title.className = "editor-batch-card-title";
    title.textContent = proposal.path;

    const actions = document.createElement("div");
    actions.className = "editor-batch-card-actions";

    const applyButton = document.createElement("button");
    applyButton.type = "button";
    applyButton.className = "secondary";
    applyButton.textContent = proposal.applied ? "Aplicado" : "Aplicar arquivo";
    applyButton.disabled = Boolean(proposal.applied);
    applyButton.addEventListener("click", async () => {
      await applyBatchProposalFile(proposal.path);
    });
    actions.appendChild(applyButton);

    for (const hunk of proposal.hunks || []) {
      const hunkButton = document.createElement("button");
      hunkButton.type = "button";
      hunkButton.className = "secondary editor-batch-hunk-button";
      hunkButton.textContent = hunk.applied ? `Hunk ${hunk.index} aplicado` : `Aplicar hunk ${hunk.index}`;
      hunkButton.disabled = Boolean(hunk.applied);
      hunkButton.addEventListener("click", async () => {
        await applyBatchProposalHunk(proposal.path, hunk.index);
      });
      actions.appendChild(hunkButton);
    }

    const preview = document.createElement("pre");
    preview.className = "editor-batch-card-preview";
    preview.textContent = proposal.diff || "[sem diff]";

    card.append(title, actions, preview);
    editorBatchProposalsEl.appendChild(card);
  }
}

async function applyBatchProposalFile(path) {
  if (!pendingBatchProposal?.proposals?.length) return;
  const proposal = pendingBatchProposal.proposals.find((item) => item.path === path);
  if (!proposal || proposal.applied) return;
  const editor = openEditors.find((item) => item.path === proposal.path);
  if (!editor) return;
  editor.content = proposal.proposed_content;
  editor.dirty = true;
  proposal.applied = true;
  if (Array.isArray(proposal.hunks)) {
    proposal.hunks = proposal.hunks.map((hunk) => ({ ...hunk, applied: true }));
  }
  pendingBatchProposal = {
    ...pendingBatchProposal,
    applied: true,
  };
  const active = getCurrentEditor();
  if (active?.path === proposal.path) {
    fileEditorEl.value = active.content;
  }
  renderEditorTabs();
  syncEditorHeader();
  renderBatchProposal();
  await appendSessionOperation({ kind: "apply_batch_file", title: `Aplicou arquivo ${proposal.path}`, path: proposal.path, detail: "arquivo aplicado individualmente" });
}

async function applyBatchProposalHunk(path, hunkIndex) {
  if (!pendingBatchProposal?.proposals?.length) return;
  const proposal = pendingBatchProposal.proposals.find((item) => item.path === path);
  if (!proposal) return;
  const editor = openEditors.find((item) => item.path === proposal.path);
  if (!editor) return;
  const target = (proposal.hunks || []).find((hunk) => hunk.index === hunkIndex);
  if (!target || target.applied) return;

  const lines = splitEditorLines(editor.content);
  const offset = (proposal.hunks || [])
    .filter((hunk) => hunk.applied && hunk.original_start < target.original_start)
    .reduce(
      (sum, hunk) => sum + ((hunk.proposed_end - hunk.proposed_start) - (hunk.original_end - hunk.original_start)),
      0,
    );
  const start = target.original_start + offset;
  const deleteCount = target.original_end - target.original_start;
  lines.splice(start, deleteCount, ...target.proposed_lines);

  editor.content = joinEditorLines(lines);
  editor.dirty = true;
  target.applied = true;
  proposal.applied = Boolean((proposal.hunks || []).every((hunk) => hunk.applied));
  pendingBatchProposal = {
    ...pendingBatchProposal,
    applied: true,
  };
  const active = getCurrentEditor();
  if (active?.path === proposal.path) {
    fileEditorEl.value = active.content;
  }
  renderEditorTabs();
  syncEditorHeader();
  renderBatchProposal();
  await appendSessionOperation({
    kind: "apply_batch_hunk",
    title: `Aplicou hunk ${hunkIndex} em ${proposal.path}`,
    path: proposal.path,
    detail: "hunk aplicado individualmente",
  });
}

function renderEditProposal() {
  const active = getCurrentEditor();
  if (!active || !pendingEditProposal || pendingEditProposal.path !== active.path) {
    editorDiffEl.textContent = "Nenhuma proposta de edição ainda.";
    editorHunksEl.innerHTML = "";
    return;
  }
  editorDiffEl.textContent = pendingEditProposal.diff || "[sem diferenças detectadas]";
  renderProposalHunks();
}

function renderProposalHunks() {
  editorHunksEl.innerHTML = "";
  const active = getCurrentEditor();
  if (!active || !pendingEditProposal || pendingEditProposal.path !== active.path) {
    return;
  }
  const hunks = pendingEditProposal.hunks || [];
  if (!hunks.length) {
    const empty = document.createElement("div");
    empty.className = "editor-hunk-empty";
    empty.textContent = "Sem hunks para aplicar separadamente.";
    editorHunksEl.appendChild(empty);
    return;
  }

  for (const hunk of hunks) {
    const card = document.createElement("div");
    card.className = "editor-hunk-card";
    if (hunk.applied) {
      card.classList.add("applied");
    }

    const header = document.createElement("div");
    header.className = "editor-hunk-header";
    header.textContent = `${hunk.tag} linhas ${hunk.original_start + 1}-${hunk.original_end}`;

    const applyButton = document.createElement("button");
    applyButton.type = "button";
    applyButton.className = "secondary";
    applyButton.textContent = hunk.applied ? "Aplicado" : "Aplicar hunk";
    applyButton.disabled = Boolean(hunk.applied);
    applyButton.addEventListener("click", async () => {
      await applyProposalHunk(hunk.index);
    });

    const preview = document.createElement("pre");
    preview.className = "editor-hunk-preview";
    preview.textContent = hunk.preview || "[sem preview]";

    card.append(header, applyButton, preview);
    editorHunksEl.appendChild(card);
  }
}

async function applyProposalHunk(hunkIndex) {
  const active = getCurrentEditor();
  if (!active || !pendingEditProposal || pendingEditProposal.path !== active.path) return;
  const hunks = pendingEditProposal.hunks || [];
  const target = hunks.find((hunk) => hunk.index === hunkIndex);
  if (!target || target.applied) return;

  const lines = splitEditorLines(active.content);
  const offset = hunks
    .filter((hunk) => hunk.applied && hunk.original_start < target.original_start)
    .reduce(
      (sum, hunk) => sum + ((hunk.proposed_end - hunk.proposed_start) - (hunk.original_end - hunk.original_start)),
      0,
    );
  const start = target.original_start + offset;
  const deleteCount = target.original_end - target.original_start;
  lines.splice(start, deleteCount, ...target.proposed_lines);

  active.content = joinEditorLines(lines);
  active.dirty = true;
  target.applied = true;
  fileEditorEl.value = active.content;
  renderEditorTabs();
  syncEditorHeader();
  renderEditProposal();
  await appendSessionOperation({
    kind: "apply_edit_hunk",
    title: `Aplicou hunk ${hunkIndex} em ${active.path}`,
    path: active.path,
    detail: "hunk aplicado individualmente",
  });
}

function splitEditorLines(content) {
  if (!content) return [];
  return content.split("\n");
}

function joinEditorLines(lines) {
  return lines.join("\n");
}

function trimTaskOutput(output) {
  const text = String(output || "");
  if (text.length <= 1200) return text;
  return `${text.slice(-1200)}`;
}

function renderWorkspaceNode(node, container, depth) {
  if (node.type === "file") {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "workspace-file-item";
    button.dataset.path = node.path;
    button.style.paddingLeft = `${12 + depth * 14}px`;
    button.textContent = node.path;
    if (node.path === currentOpenFilePath) {
      button.classList.add("active");
    }
    button.addEventListener("click", () => openWorkspaceFile(node.path));
    container.appendChild(button);
    return;
  }

  const group = document.createElement("div");
  group.className = "workspace-dir-group";
  const title = document.createElement("div");
  title.className = "workspace-dir-title";
  title.style.paddingLeft = `${8 + depth * 14}px`;
  title.textContent = node.path === "." ? "workspace" : node.path;
  group.appendChild(title);
  for (const child of node.children || []) {
    renderWorkspaceNode(child, group, depth + 1);
  }
  container.appendChild(group);
}

async function openWorkspaceFile(path, options = {}) {
  const payload = await api(`/api/workspace/file?path=${encodeURIComponent(path)}`);
  const existing = openEditors.find((editor) => editor.path === payload.path);
  if (existing) {
    currentOpenFilePath = existing.path;
  } else {
    openEditors.push({
      path: payload.path,
      content: payload.content,
      dirty: false,
    });
    currentOpenFilePath = payload.path;
  }
  trackRecentFile(payload.path);
  pendingEditProposal = pendingEditProposal?.path === payload.path ? pendingEditProposal : null;
  pendingTaskAssist = pendingTaskAssist?.edit_proposal?.path === payload.path ? pendingTaskAssist : null;
  syncEditorFromState();
  renderEditorTabs();
  renderWorkspaceTree();
  renderComposerContextPreview();
  if (options.persist !== false) {
    scheduleSessionUiStateSave();
  }
}

async function queueAttachments(files) {
  for (const file of files) {
    const content = await safeReadFile(file);
    pendingAttachments.push({
      id: `${file.name}-${file.lastModified}-${pendingAttachments.length}`,
      name: file.name,
      content,
      size: file.size,
    });
  }
  renderComposerContextPreview();
}

function appendMessageElement(role, content, metadata = null, attachments = []) {
  const node = template.content.firstElementChild.cloneNode(true);
  node.classList.add(role === "user" ? "user" : "assistant");
  node.querySelector(".message-role").textContent = role === "user" ? "Você" : "Jarvis";
  const metaEl = node.querySelector(".message-meta");
  const metaLine = formatMessageMetadata(metadata);
  if (metaLine) {
    metaEl.textContent = metaLine;
  } else {
    metaEl.remove();
  }
  node.querySelector(".message-body").textContent = content;
  const renderedAttachments = Array.isArray(attachments) ? attachments.filter((attachment) => attachment && attachment.name) : [];
  if (renderedAttachments.length) {
    const attachmentsEl = document.createElement("div");
    attachmentsEl.className = "message-attachments";
    for (const attachment of renderedAttachments) {
      const details = document.createElement("details");
      details.className = "message-attachment";
      const summary = document.createElement("summary");
      summary.textContent = `${attachment.name} (${formatSize(Number(attachment.size) || String(attachment.content || "").length)})`;
      const preview = document.createElement("pre");
      preview.className = "message-attachment-preview";
      preview.textContent = truncateContext(String(attachment.content || ""), 2000);
      details.append(summary, preview);
      attachmentsEl.appendChild(details);
    }
    node.appendChild(attachmentsEl);
  }
  messagesEl.appendChild(node);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return node;
}

async function loadStatus() {
  try {
    const status = await api("/api/status", { auth: false });
    const ollama = status.ollama?.status ?? "unknown";
    const qdrant = status.qdrant?.status ?? "unknown";
    const strategy = status.core?.model_selection_strategy ?? "unknown";
    statusEl.textContent = `core: ok\nstrategy: ${strategy}\nollama: ${ollama}\nqdrant: ${qdrant}`;
  } catch (error) {
    statusEl.textContent = `Erro: ${error.message}`;
  }
}

function setPending(pending) {
  form.querySelector("#send").disabled = pending;
  promptEl.disabled = pending;
  attachFileButton.disabled = pending;
}

async function api(path, options = {}) {
  const auth = options.auth ?? true;
  const response = await fetch(path, {
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...(auth ? { Authorization: "Bearer local" } : {}),
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

async function streamSessionMessage({ sessionId, model, content, displayContent, workspace, attachments = [] }) {
  const userMessage = {
    role: "user",
    content,
    display_content: displayContent,
    attachments,
  };
  messages.push(userMessage);
  const assistantMessage = {
    role: "assistant",
    content: "",
  };
  messages.push(assistantMessage);
  renderMessages();

  const assistantNode = messagesEl.lastElementChild;
  const assistantBody = assistantNode?.querySelector(".message-body");
  const assistantMeta = assistantNode?.querySelector(".message-meta");

  const response = await fetch(`/api/chat/sessions/${sessionId}/message/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer local",
    },
    body: JSON.stringify({
      model,
      content,
      display_content: displayContent,
      workspace,
      attachments,
    }),
  });
  if (!response.ok || !response.body) {
    throw new Error(`HTTP ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let finalPayload = null;

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop() || "";
    for (const event of events) {
      const trimmed = event.trim();
      if (!trimmed.startsWith("data:")) continue;
      const payloadText = trimmed.slice(5).trim();
      if (payloadText === "[DONE]") continue;
      const payload = JSON.parse(payloadText);
      if (payload.type === "start") {
        assistantMessage.metadata = payload.assistant_metadata || null;
        if (assistantMeta) {
          const metaLine = formatMessageMetadata(assistantMessage.metadata);
          if (metaLine) assistantMeta.textContent = metaLine;
        }
        continue;
      } else if (payload.type === "chunk") {
        assistantMessage.content += payload.delta || "";
        if (assistantBody) {
          assistantBody.textContent = assistantMessage.content;
          messagesEl.scrollTop = messagesEl.scrollHeight;
        }
      } else if (payload.type === "done") {
        finalPayload = payload;
      } else if (payload.type === "error") {
        throw new Error(payload.detail || "Erro desconhecido no stream.");
      }
    }
  }

  if (!finalPayload) {
    throw new Error("Stream finalizado sem payload final.");
  }
  return finalPayload;
}

async function registerServiceWorker() {
  if (!("serviceWorker" in navigator)) return;
  try {
    await navigator.serviceWorker.register("/app/sw.js", { scope: "/app/" });
  } catch {
    // ignore
  }
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function buildAttachmentPrompt(prompt) {
  const operationalContext = buildOperationalContextBlock();
  if (!pendingAttachments.length && !operationalContext) return prompt;
  const parts = [
    ...(operationalContext ? [operationalContext, ""] : []),
    ...(pendingAttachments.length
      ? [
          "[ATTACHMENTS]",
          ...pendingAttachments.map((attachment) => `FILE: ${attachment.name}\n${attachment.content}`),
          "",
        ]
      : []),
    prompt,
  ];
  return parts.join("\n\n");
}

function buildOperationalContextBlock() {
  const sections = [];
  const activeEditor = getCurrentEditor();

  if (contextActiveFileCheckbox.checked && activeEditor) {
    sections.push([
      "[ACTIVE_FILE]",
      `PATH: ${activeEditor.path}`,
      `DIRTY: ${activeEditor.dirty ? "yes" : "no"}`,
      truncateContext(activeEditor.content, 12000),
    ].join("\n"));
    if (editorSelection?.path === activeEditor.path) {
      sections.push([
        "[ACTIVE_SELECTION]",
        `PATH: ${editorSelection.path}`,
        `RANGE: ${editorSelection.start}-${editorSelection.end}`,
        truncateContext(editorSelection.text, 4000),
      ].join("\n"));
    }
  }

  if (contextOpenTabsCheckbox.checked && openEditors.length) {
    sections.push([
      "[OPEN_TABS]",
      ...openEditors.map((editor) => `${editor.path}${editor.dirty ? " *" : ""}`),
    ].join("\n"));
  }

  if (contextTerminalCheckbox.checked && terminalBuffer.trim()) {
    sections.push([
      "[TERMINAL_TAIL]",
      `SESSION: ${terminalSessionId || "none"}`,
      truncateContext(terminalBuffer, 5000),
    ].join("\n"));
  }

  if (contextSearchCheckbox.checked && workspaceSearchResults.length) {
    sections.push([
      "[WORKSPACE_SEARCH]",
      ...workspaceSearchResults.slice(0, 8).map((result) =>
        `${result.path}${result.snippet ? ` :: ${result.snippet}` : ""}`,
      ),
    ].join("\n"));
  }

  if (latestGitContext.trim()) {
    sections.push(latestGitContext);
  }

  if (!sections.length) {
    return "";
  }

  return ["[WORKSPACE_CONTEXT]", `WORKSPACE: ${workspaceInput.value.trim() || "none"}`, "", ...sections].join("\n");
}

function renderComposerContextPreview() {
  const activeParts = [];
  if (contextActiveFileCheckbox.checked && getCurrentEditor()) {
    activeParts.push(`arquivo: ${getCurrentEditor().path}`);
  }
  if (contextOpenTabsCheckbox.checked && openEditors.length) {
    activeParts.push(`abas: ${openEditors.length}`);
  }
  if (contextTerminalCheckbox.checked && terminalBuffer.trim()) {
    activeParts.push(`terminal: ${Math.min(terminalBuffer.length, 5000)} chars`);
  }
  if (contextSearchCheckbox.checked && workspaceSearchResults.length) {
    activeParts.push(`busca: ${workspaceSearchResults.length} hits`);
  }
  if (pendingAttachments.length) {
    activeParts.push(`anexos: ${pendingAttachments.length}`);
  }
  if (latestGitContext.trim()) {
    activeParts.push("git: pronto");
  }
  if (quickFlowMode) {
    activeParts.push(`fluxo: ${quickFlowMode}`);
  }
  if (resolveQuickTargetPath()) {
    activeParts.push(`alvo: ${resolveQuickTargetPath()}`);
  }

  const block = buildOperationalContextBlock();
  if (!activeParts.length) {
    composerContextPreviewEl.textContent = "Contexto automático desativado.";
    renderWorkbenchStatus();
    return;
  }

  const preview = [activeParts.join(" | ")];
  if (block) {
    preview.push("", truncateContext(block, 900));
  }
  composerContextPreviewEl.textContent = preview.join("\n");
  renderWorkbenchStatus();
}

async function openNativeLinuxTerminal(cwd = null) {
  const payload = await api("/api/terminal/native", {
    method: "POST",
    body: JSON.stringify({ cwd }),
  });
  const result = payload.result || {};
  await appendSessionOperation({
    kind: "native_terminal_open",
    title: "Abriu terminal Linux nativo",
    detail: `${result.launcher || "launcher"} em ${result.cwd || cwd || "."}`,
    path: getCurrentEditor()?.path || null,
  });
  announceAssistantMessage(`Terminal Linux nativo aberto com ${result.launcher || "launcher"} em ${result.cwd || cwd || "."}.`);
}

async function openNativeLinuxTerminalForActiveFile() {
  const active = getCurrentEditor();
  if (!active) {
    announceAssistantMessage("Abra um arquivo antes de pedir o terminal Linux no diretório ativo.");
    return;
  }
  const cwd = active.path.includes("/") ? active.path.slice(0, active.path.lastIndexOf("/")) : ".";
  await openNativeLinuxTerminal(cwd);
}

async function runTerminalCommandFromInput() {
  const command = (terminalCommandEl.value || "").trim();
  if (!command) return;
  await sendTerminalData(`${command}
`);
  trackCommandHistory(command);
  await appendSessionOperation({
    kind: "terminal_run",
    title: "Executou comando bash",
    command,
    path: getCurrentEditor()?.path || null,
    detail: "comando executado pelo launcher do terminal",
  });
  terminalCommandEl.select();
  scheduleSessionUiStateSave();
}

async function sendTerminalCommandFromInput() {
  const command = terminalCommandEl.value || "";
  if (!command) return;
  await sendTerminalData(command);
  trackCommandHistory(command);
  await appendSessionOperation({
    kind: "terminal_send",
    title: "Enviou texto ao terminal",
    command,
    path: getCurrentEditor()?.path || null,
    detail: "texto enviado ao shell sem Enter automático",
  });
  terminalCommandEl.focus();
  scheduleSessionUiStateSave();
}

async function jumpTerminalToActiveFileDir() {
  const active = getCurrentEditor();
  if (!active) return;
  const directory = active.path.includes("/") ? active.path.slice(0, active.path.lastIndexOf("/")) : ".";
  const command = `cd ${JSON.stringify(directory)}`;
  terminalCommandEl.value = command;
  await sendTerminalData(`${command}
`);
  trackCommandHistory(command);
  await appendSessionOperation({
    kind: "terminal_cd",
    title: `Terminal em ${directory}`,
    command,
    path: active.path,
    detail: "terminal sincronizado com o diretório do arquivo ativo",
  });
}

async function rememberCurrentNote(options = {}) {
  const active = options.activeEditor || getCurrentEditor();
  if (!active || !isMarkdownNote(active.path)) {
    renderObsidianStatus();
    return false;
  }
  const workspace = resolveWorkspaceHint(active.path);
  const title = extractMarkdownTitle(active.content, active.path.split("/").pop()?.replace(/\.md$/i, ""));
  const field = `obsidian.${slugifyLabel(title)}`;
  const excerpt = truncateContext(active.content, 1800);
  await api("/api/memory/workspace", {
    method: "POST",
    body: JSON.stringify({
      workspace,
      field,
      value: `Nota: ${title}
Path: ${active.path}

${excerpt}`,
      source: "pwa-obsidian",
    }),
  });
  await appendSessionOperation({
    kind: options.auto ? "obsidian_remember_auto" : "obsidian_remember",
    title: `${options.auto ? "Auto-" : ""}lembrou nota ${title}`,
    path: active.path,
    detail: `workspace ${workspace}`,
  });
  obsidianStatusEl.textContent = [
    `${options.auto ? "Nota sincronizada automaticamente na memória." : "Nota lembrada com sucesso."}`,
    `Workspace: ${workspace}`,
    `Campo: ${field}`,
    `Path: ${active.path}`,
].join("\n");
  if (options.announce !== false) {
    announceAssistantMessage(`Nota ${title} registrada na memória do workspace ${workspace}.`);
  }
  return true;
}

async function indexCurrentNote(options = {}) {
  const active = options.activeEditor || getCurrentEditor();
  if (!active || !isMarkdownNote(active.path)) {
    renderObsidianStatus();
    return false;
  }
  const workspace = resolveWorkspaceHint(active.path);
  const title = extractMarkdownTitle(active.content, active.path.split("/").pop()?.replace(/\.md$/i, ""));
  const payload = await api("/api/knowledge/ingest-note", {
    method: "POST",
    body: JSON.stringify({
      domain: workspace,
      title,
      content: active.content,
      source_path: active.path,
      force: true,
    }),
  });
  await appendSessionOperation({
    kind: options.auto ? "obsidian_index_auto" : "obsidian_index",
    title: `${options.auto ? "Auto-" : ""}indexou nota ${title}`,
    path: active.path,
    detail: payload.stored_path || `workspace ${workspace}`,
  });
  obsidianStatusEl.textContent = [
    `${options.auto ? "Nota indexada automaticamente para RAG." : "Nota indexada para RAG."}`,
    `Workspace: ${workspace}`,
    `Chunks: ${payload.indexed_chunks ?? "?"}`,
    `Destino: ${payload.stored_path || "knowledge/obsidian"}`,
].join("\n");
  if (options.announce !== false) {
    announceAssistantMessage(`Nota ${title} indexada para conhecimento local em ${workspace}.`);
  }
  return true;
}

function prepareChatFromCurrentNote() {
  const active = getCurrentEditor();
  if (!active || !isMarkdownNote(active.path)) {
    renderObsidianStatus();
    return;
  }
  contextActiveFileCheckbox.checked = true;
  persistContextPrefs();
  promptEl.value = "Use esta nota como contexto principal. Extraia os pontos centrais, relacione com o workspace atual e proponha próximos passos objetivos.";
  renderComposerContextPreview();
  promptEl.focus();
  announceAssistantMessage(`Nota ${active.path} preparada como contexto principal do próximo prompt.`);
}

async function runObsidianAssistOnSave(active) {
  if (!active || !isMarkdownNote(active.path)) return;
  if (obsidianAutoRememberCheckbox.checked) {
    await rememberCurrentNote({ activeEditor: active, auto: true, announce: false });
  }
  if (obsidianAutoIndexCheckbox.checked) {
    await indexCurrentNote({ activeEditor: active, auto: true, announce: false });
  }
}

function buildHelpGuide() {
  return [
    "Jarvis /help",
    "",
    "Comandos do terminal bash:",
    "/run <comando> -> executa e envia Enter no terminal",
    "/send <texto> -> envia texto bruto ao terminal sem Enter automático",
    "/focus terminal -> leva o foco para o terminal",
    "/focus editor -> leva o foco para o editor",
    "/focus chat -> volta para o composer",
    "",
    "Comandos de workspace:",
    "/open <caminho> -> abre um arquivo do workspace",
    "/new <caminho> -> cria um arquivo vazio",
    "/save-all -> salva todas as abas com alterações",
    "/attach-tabs -> anexa todas as abas abertas ao próximo prompt",
    "/run-selection -> executa a seleção atual do editor no terminal",
    "/search <termo> -> busca arquivo e conteúdo no workspace",
    "/attach active -> anexa o arquivo ativo ao chat",
    "",
    "Comandos de Git:",
    "/git-status -> coleta status resumido do repositório",
    "/git-diff -> coleta diff atual para revisar mudanças",
    "/git-log -> coleta histórico recente do repositório",
    "/git-prs -> lista pull requests locais via gh",
    "/git-issues -> lista issues locais via gh",
    "/gh-pr-view <n> -> enfileira visualização detalhada da PR no Jarvis",
    "/gh-pr-checkout <n> -> enfileira checkout da PR no Jarvis",
    "/gh-pr-diff <n> -> enfileira diff da PR no Jarvis",
    "/gh-pr-create <titulo> -> enfileira criação de PR via gh",
    "/gh-issue-view <n> -> enfileira visualização detalhada da issue no Jarvis",
    "/gh-issue-create <titulo> -> enfileira criação de issue via gh",
    "/linux-terminal -> abre um terminal Linux nativo no workspace",
    "/mode <chat|build|review|focus> -> alterna o modo principal da interface",
    "/explain-file -> prepara o prompt para analisar o arquivo ativo",
    "/debug-terminal -> prepara o prompt para diagnosticar a saída recente do terminal",
    "/linux-terminal-file -> abre um terminal Linux no diretório do arquivo ativo",
    "/git-attach -> anexa o último contexto Git ao próximo prompt",
    "/attach-terminal -> anexa a saída recente do terminal ao próximo prompt",
    "/fix-terminal -> prepara o Jarvis para diagnosticar o erro atual do terminal",
    "/build-file <caminho> :: <objetivo> -> cria/abre um arquivo e prepara um prompt de implementação",
    "",
    "Comandos de automação:",
    "/queue-command -> envia o comando sugerido para a fila do Jarvis",
    "/queue-edit -> envia o diff atual para a fila do Jarvis",
    "/self-review -> Jarvis revisa o arquivo ativo e enfileira melhorias",
    "",
    "Comandos de Obsidian:",
    "/remember-note -> grava a nota Markdown ativa na memória do workspace",
    "/index-note -> indexa a nota ativa no RAG local",
    "/chat-note -> prepara a nota ativa como contexto principal do próximo prompt",
    "",
    "Fluxo recomendado:",
    "1. /open ou abra um arquivo pela árvore",
    "2. /run para testar ou navegar no bash",
    "3. peça edição ao Jarvis ou use Jarvis executar",
    "4. em notas Markdown, use /remember-note e /index-note",
].join("\n");
}

async function handleSlashCommand(prompt) {
  const [command, ...rest] = prompt.slice(1).split(" ");
  const args = rest.join(" ").trim();
  if (!command) return false;

  switch (command.toLowerCase()) {
    case "help":
      announceAssistantMessage(buildHelpGuide());
      return true;
    case "mode":
      if (!args) {
        announceAssistantMessage("Uso: /mode chat|build|review|focus");
        return true;
      }
      setWorkbenchMode(args.toLowerCase());
      announceAssistantMessage(`Modo alterado para ${args.toLowerCase()}.`);
      return true;
    case "explain-file":
      preparePromptForActiveFile();
      return true;
    case "debug-terminal":
      preparePromptForTerminalDebug();
      return true;
    case "open":
      if (!args) {
        announceAssistantMessage("Uso: /open caminho/do/arquivo");
        return true;
      }
      await openWorkspaceFile(args);
      await appendSessionOperation({ kind: "slash_open", title: `Slash abriu ${args}`, path: args, detail: "arquivo aberto pelo composer" });
      announceAssistantMessage(`Arquivo aberto: ${args}`);
      setWorkbenchMode("build");
      return true;
    case "search":
      if (!args) {
        announceAssistantMessage("Uso: /search termo");
        return true;
      }
      workspaceSearchInput.value = args;
      await searchWorkspace();
      await appendSessionOperation({ kind: "slash_search", title: `Slash buscou ${args}`, detail: "busca executada no workspace" });
      announceAssistantMessage(`Busca executada no workspace por: ${args}`);
      return true;
    case "run":
      if (!args) {
        announceAssistantMessage("Uso: /run comando bash");
        return true;
      }
      terminalCommandEl.value = args;
      await runTerminalCommandFromInput();
      announceAssistantMessage(`Comando executado no terminal: ${args}`);
      return true;
    case "send":
      if (!args) {
        announceAssistantMessage("Uso: /send texto para o terminal");
        return true;
      }
      terminalCommandEl.value = args;
      await sendTerminalCommandFromInput();
      announceAssistantMessage(`Texto enviado ao terminal: ${args}`);
      return true;
    case "new":
      if (!args) {
        announceAssistantMessage("Uso: /new caminho/do/arquivo");
        return true;
      }
      await api(`/api/workspace/file?session_id=${encodeURIComponent(currentSessionId || "")}`, {
        method: "POST",
        body: JSON.stringify({ path: args, content: "" }),
      });
      await loadWorkspaceTree();
      await openWorkspaceFile(args);
      await appendSessionOperation({ kind: "slash_new", title: `Slash criou ${args}`, path: args, detail: "arquivo criado pelo composer" });
      announceAssistantMessage(`Arquivo criado: ${args}`);
      setWorkbenchMode("build");
      return true;
    case "save-all":
      await saveAllEditors();
      return true;
    case "attach-tabs":
      await attachOpenTabsToChat();
      return true;
    case "run-selection":
      await runEditorSelectionInTerminal();
      return true;
    case "remember-note":
      await rememberCurrentNote();
      return true;
    case "index-note":
      await indexCurrentNote();
      return true;
    case "chat-note":
      prepareChatFromCurrentNote();
      return true;
    case "attach":
      if (args === "active" && currentOpenFilePath) {
        attachOpenFileButton.click();
        announceAssistantMessage(`Arquivo ativo anexado ao chat: ${currentOpenFilePath}`);
        return true;
      }
      announceAssistantMessage("Uso: /attach active");
      return true;
    case "attach-terminal":
      await attachTerminalSnapshot();
      return true;
    case "fix-terminal":
      await preparePromptForTerminalFix();
      return true;
    case "build-file": {
      if (!args) {
        announceAssistantMessage("Uso: /build-file caminho/do/arquivo :: objetivo");
        return true;
      }
      const [rawPath, rawGoal] = args.split("::");
      const path = (rawPath || "").trim();
      const goal = (rawGoal || "").trim();
      if (!path) {
        announceAssistantMessage("Uso: /build-file caminho/do/arquivo :: objetivo");
        return true;
      }
      quickTargetPathEl.value = path;
      if (goal) quickGoalEl.value = goal;
      await setQuickFlowMode("create");
      await ensureWorkspaceFile(path);
      await runQuickFlowPrompt();
      announceAssistantMessage(`Fluxo de implementação preparado para ${path}.`);
      return true;
    }
    case "git-status":
      await loadGitContext("status");
      announceAssistantMessage("Status Git carregado no painel lateral.");
      return true;
    case "git-diff":
      await loadGitContext("diff");
      announceAssistantMessage("Diff Git carregado no painel lateral.");
      return true;
    case "git-log":
      await loadGitContext("log");
      announceAssistantMessage("Log Git carregado no painel lateral.");
      return true;
    case "git-prs":
      await loadGitContext("prs");
      announceAssistantMessage("Pull requests carregados no painel lateral.");
      return true;
    case "git-issues":
      await loadGitContext("issues");
      announceAssistantMessage("Issues carregadas no painel lateral.");
      return true;
    case "git-github":
      await loadGitContext("github");
      announceAssistantMessage("Contexto GitHub carregado no painel lateral.");
      return true;
    case "git-attach":
      await attachGitContextToChat();
      setWorkbenchMode("review");
      return true;
    case "gh-pr-view":
      if (!args) {
        announceAssistantMessage("Uso: /gh-pr-view numero-da-pr");
        return true;
      }
      await queueGitHubApproval(`gh pr view ${args} --comments`, `Visualizar PR #${args}`, "ação GitHub via gh enfileirada");
      announceAssistantMessage(`PR #${args} enviada para a fila do Jarvis.`);
      return true;
    case "gh-pr-checkout":
      if (!args) {
        announceAssistantMessage("Uso: /gh-pr-checkout numero-da-pr");
        return true;
      }
      await queueGitHubApproval(`gh pr checkout ${args}`, `Checkout da PR #${args}`, "ação GitHub via gh enfileirada");
      announceAssistantMessage(`Checkout da PR #${args} enviado para a fila do Jarvis.`);
      return true;
    case "gh-pr-diff":
      if (!args) {
        announceAssistantMessage("Uso: /gh-pr-diff numero-da-pr");
        return true;
      }
      await queueGitHubApproval(`gh pr diff ${args}`, `Diff da PR #${args}`, "ação GitHub via gh enfileirada");
      announceAssistantMessage(`Diff da PR #${args} enviado para a fila do Jarvis.`);
      return true;
    case "gh-pr-create":
      if (!args) {
        announceAssistantMessage("Uso: /gh-pr-create titulo-da-pr");
        return true;
      }
      await queueGitHubApproval(`gh pr create --title ${JSON.stringify(args)} --body ${JSON.stringify(buildGitHubBody(args))}`, `Criar PR: ${args}`, "ação GitHub via gh enfileirada");
      announceAssistantMessage("Criação da PR enviada para a fila do Jarvis.");
      return true;
    case "gh-issue-view":
      if (!args) {
        announceAssistantMessage("Uso: /gh-issue-view numero-da-issue");
        return true;
      }
      await queueGitHubApproval(`gh issue view ${args} --comments`, `Visualizar issue #${args}`, "ação GitHub via gh enfileirada");
      announceAssistantMessage(`Issue #${args} enviada para a fila do Jarvis.`);
      return true;
    case "gh-issue-create":
      if (!args) {
        announceAssistantMessage("Uso: /gh-issue-create titulo-da-issue");
        return true;
      }
      await queueGitHubApproval(`gh issue create --title ${JSON.stringify(args)} --body ${JSON.stringify(buildGitHubBody(args))}`, `Criar issue: ${args}`, "ação GitHub via gh enfileirada");
      announceAssistantMessage("Criação da issue enviada para a fila do Jarvis.");
      return true;
    case "linux-terminal":
      await openNativeLinuxTerminal();
      return true;
    case "linux-terminal-file":
      await openNativeLinuxTerminalForActiveFile();
      return true;
    case "queue-command":
      await queueSuggestedCommandApproval();
      return true;
    case "queue-edit":
      await queueEditProposalApproval();
      return true;
    case "self-review":
      await runSelfImproveActive();
      return true;
    case "focus":
      if (args === "editor") fileEditorEl.focus();
      else if (args === "terminal") terminalOutputEl.focus();
      else promptEl.focus();
      announceAssistantMessage(`Foco movido para: ${args || "chat"}`);
      return true;
    default:
      announceAssistantMessage(`Comando não reconhecido: /${command}. Use /help para ver o guia em português.`);
      return true;
  }
}

function truncateContext(content, limit) {
  const text = String(content || "").trim();
  if (text.length <= limit) return text;
  return `${text.slice(0, limit)}\n[truncated]`;
}

function mergeInstructionWithSelection(instruction) {
  if (!editorSelection) return instruction;
  return [
    instruction,
    "",
    "[SELECTED_RANGE]",
    `PATH: ${editorSelection.path}`,
    `RANGE: ${editorSelection.start}-${editorSelection.end}`,
    editorSelection.text,
  ].join("\n");
}

async function safeReadFile(file) {
  const content = await file.text();
  if (content.length > 20000) {
    return `${content.slice(0, 20000)}\n\n[truncated]`;
  }
  return content;
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function setDropzoneState(active) {
  form.dataset.dropzone = active ? "active" : "idle";
}

function exportCurrentSessionMarkdown() {
  if (!messages.length) return;
  const title = (sessionTitleEl.value || "jarvis-chat").trim();
  const safeTitle = title.toLowerCase().replace(/[^a-z0-9-_]+/gi, "-");
  const markdown = [
    `# ${title}`,
    "",
    `- model: ${modelSelect.value}`,
    `- workspace: ${workspaceInput.value.trim() || "none"}`,
    "",
    ...messages.flatMap((message) => [
      `## ${message.role === "user" ? "Você" : "Jarvis"}`,
      "",
      `${message.display_content || message.content}`,
      ...(Array.isArray(message.attachments) && message.attachments.length
        ? [
            "",
            "### Anexos",
            ...message.attachments.flatMap((attachment) => [
              `- ${attachment.name} (${formatSize(Number(attachment.size) || String(attachment.content || "").length)})`,
              "",
              '```text',
              `${truncateContext(String(attachment.content || ""), 4000)}`,
              '```',
              "",
            ]),
          ]
        : [""]),
    ]),
  ].join("\n");
  const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `${safeTitle || "jarvis-chat"}.md`;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}
