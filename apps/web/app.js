const modelSelect = document.querySelector("#model");
const workspaceInput = document.querySelector("#workspace");
const messagesEl = document.querySelector("#messages");
const sessionsEl = document.querySelector("#sessions");
const form = document.querySelector("#chat-form");
const promptEl = document.querySelector("#prompt");
const statusEl = document.querySelector("#status");
const attachmentsEl = document.querySelector("#attachments");
const clearButton = document.querySelector("#clear-chat");
const newChatButton = document.querySelector("#new-chat");
const deleteButton = document.querySelector("#delete-chat");
const installButton = document.querySelector("#install-app");
const attachFileButton = document.querySelector("#attach-file");
const fileInput = document.querySelector("#file-input");
const sessionTitleEl = document.querySelector("#session-title");
const sessionSearchEl = document.querySelector("#session-search");
const exportChatButton = document.querySelector("#export-chat");
const quickActionButtons = Array.from(document.querySelectorAll(".quick-action"));
const template = document.querySelector("#message-template");

let installPrompt = null;
let currentSessionId = null;
let messages = [];
let pendingAttachments = [];
let allSessions = [];
let dragDepth = 0;
const STORAGE_KEY = "jarvis-pwa-current-session-id";

bootstrap().catch((error) => {
  statusEl.textContent = `Erro ao inicializar: ${error.message}`;
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
  messages = [];
  renderMessages();
  await loadSessions();
});

newChatButton.addEventListener("click", async () => {
  await createSession();
});

deleteButton.addEventListener("click", async () => {
  if (!currentSessionId) return;
  await api(`/api/chat/sessions/${currentSessionId}`, { method: "DELETE" });
  currentSessionId = null;
  sessionTitleEl.value = "";
  persistCurrentSessionId();
  messages = [];
  renderMessages();
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

exportChatButton.addEventListener("click", () => {
  exportCurrentSessionMarkdown();
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

  setPending(true);
  try {
    const attachmentPrompt = buildAttachmentPrompt(prompt);
    const response = await streamSessionMessage({
      sessionId: currentSessionId,
      model: modelSelect.value,
      content: attachmentPrompt,
      displayContent: prompt,
      workspace: workspaceInput.value.trim() || null,
    });
    promptEl.value = "";
    pendingAttachments = [];
    renderAttachments();
    messages = response.session.messages || [];
    renderMessages();
    await loadSessions();
  } catch (error) {
    messages = messages.slice(0, Math.max(0, messages.length - 2));
    renderMessages();
    appendMessageElement("assistant", `Erro ao falar com o Jarvis: ${error.message}`);
  } finally {
    setPending(false);
    loadStatus();
  }
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
  renderMessages();
  await loadStatus();
  registerServiceWorker();
  await loadSessions();
  if (!currentSessionId) {
    await createSession();
  }
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
  persistCurrentSessionId();
  messages = [];
  renderMessages();
  await loadSessions();
  await selectSession(currentSessionId);
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
  messages = session.messages || [];
  modelSelect.value = session.model || "jarvis-safe";
  workspaceInput.value = session.workspace || "";
  sessionTitleEl.value = session.title || "Nova conversa";
  renderMessages();
  highlightSelectedSession();
}

function renderSessions(sessions) {
  sessionsEl.innerHTML = "";
  const term = (sessionSearchEl.value || "").trim().toLowerCase();
  const filtered = sessions.filter((session) => {
    if (!term) return true;
    return [session.title || "", session.model || "", session.workspace || ""]
      .join(" ")
      .toLowerCase()
      .includes(term);
  });
  if (!filtered.length) {
    sessionsEl.textContent = "Nenhuma conversa ainda.";
    return;
  }
  for (const session of filtered) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "session-item";
    button.dataset.sessionId = session.id;
    button.innerHTML = `
      <strong>${escapeHtml(session.title || "Nova conversa")}</strong>
      <span>${escapeHtml(session.model || "jarvis-safe")}</span>
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

function persistCurrentSessionId() {
  if (currentSessionId) {
    localStorage.setItem(STORAGE_KEY, currentSessionId);
  } else {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function renderMessages() {
  messagesEl.innerHTML = "";
  if (!messages.length) {
    appendMessageElement("assistant", "Jarvis pronto. Escolha um perfil e envie sua mensagem.");
    return;
  }
  for (const message of messages) {
    appendMessageElement(message.role, message.display_content || message.content);
  }
}

function renderAttachments() {
  attachmentsEl.innerHTML = "";
  if (!pendingAttachments.length) {
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
}

function appendMessageElement(role, content) {
  const node = template.content.firstElementChild.cloneNode(true);
  node.classList.add(role === "user" ? "user" : "assistant");
  node.querySelector(".message-role").textContent = role === "user" ? "Você" : "Jarvis";
  node.querySelector(".message-body").textContent = content;
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

async function streamSessionMessage({ sessionId, model, content, displayContent, workspace }) {
  const userMessage = {
    role: "user",
    content,
    display_content: displayContent,
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
  if (!pendingAttachments.length) return prompt;
  const parts = [
    "[ATTACHMENTS]",
    ...pendingAttachments.map((attachment) => `FILE: ${attachment.name}\n${attachment.content}`),
    "",
    prompt,
  ];
  return parts.join("\n\n");
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
      "",
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
