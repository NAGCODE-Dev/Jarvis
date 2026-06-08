const modelSelect = document.querySelector("#model");
const workspaceInput = document.querySelector("#workspace");
const messagesEl = document.querySelector("#messages");
const sessionsEl = document.querySelector("#sessions");
const form = document.querySelector("#chat-form");
const promptEl = document.querySelector("#prompt");
const statusEl = document.querySelector("#status");
const clearButton = document.querySelector("#clear-chat");
const newChatButton = document.querySelector("#new-chat");
const deleteButton = document.querySelector("#delete-chat");
const installButton = document.querySelector("#install-app");
const sessionTitleEl = document.querySelector("#session-title");
const template = document.querySelector("#message-template");

let installPrompt = null;
let currentSessionId = null;
let messages = [];
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

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const prompt = promptEl.value.trim();
  if (!prompt || !currentSessionId) return;

  setPending(true);
  try {
    const response = await api(`/api/chat/sessions/${currentSessionId}/message`, {
      method: "POST",
      body: JSON.stringify({
        model: modelSelect.value,
        content: prompt,
        workspace: workspaceInput.value.trim() || null,
      }),
    });
    promptEl.value = "";
    messages = response.session.messages || [];
    renderMessages();
    await loadSessions();
  } catch (error) {
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
  const sessions = payload.sessions || [];
  renderSessions(sessions);
  const preferredId = currentSessionId || localStorage.getItem(STORAGE_KEY);
  if (preferredId && sessions.some((session) => session.id === preferredId)) {
    await selectSession(preferredId);
    return;
  }
  if (!currentSessionId && sessions.length) {
    await selectSession(sessions[0].id);
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
  if (!sessions.length) {
    sessionsEl.textContent = "Nenhuma conversa ainda.";
    return;
  }
  for (const session of sessions) {
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

function appendMessageElement(role, content) {
  const node = template.content.firstElementChild.cloneNode(true);
  node.classList.add(role === "user" ? "user" : "assistant");
  node.querySelector(".message-role").textContent = role === "user" ? "Você" : "Jarvis";
  node.querySelector(".message-body").textContent = content;
  messagesEl.appendChild(node);
  messagesEl.scrollTop = messagesEl.scrollHeight;
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
