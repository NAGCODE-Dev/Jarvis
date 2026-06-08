const { Plugin, PluginSettingTab, Setting, ItemView, Notice, MarkdownView, requestUrl } = require("obsidian");

const VIEW_TYPE_JARVIS_CHAT = "jarvis-chat-view";

const DEFAULT_SETTINGS = {
  apiBase: "http://127.0.0.1:8000",
  generalModel: "jarvis-safe",
  codeModel: "jarvis-programador-safe",
  researchModel: "jarvis-pesquisador-safe",
  chatModel: "jarvis-safe",
  appendResponsesToNote: true,
  responseHeadingPrefix: "Jarvis",
  defaultWorkspace: "",
  createNewNotesInFolder: "Jarvis",
  chatUseCurrentNoteContext: true,
  persistChatHistory: true,
  currentChatSessionId: "",
};

class JarvisChatView extends ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.messages = [];
  }

  getViewType() {
    return VIEW_TYPE_JARVIS_CHAT;
  }

  getDisplayText() {
    return "Jarvis Chat";
  }

  async onOpen() {
    await this.plugin.ensureChatSession({
      model: this.plugin.settings.chatModel || this.plugin.settings.generalModel,
      workspace: this.plugin.settings.defaultWorkspace || null,
    });
    this.messages = await this.plugin.getCurrentSessionMessages();
    this.render();
  }

  async sendExternalMessage(content, displayContent = "Contexto externo enviado ao Jarvis.") {
    const model = this.plugin.settings.chatModel || this.plugin.settings.generalModel;
    try {
      await this.plugin.ensureChatSession({
        model,
        workspace: this.plugin.settings.defaultWorkspace || null,
      });
      const payload = await this.plugin.sendSessionMessage({
        model,
        content,
        displayContent,
        workspace: this.plugin.settings.defaultWorkspace || null,
      });
      this.messages = payload.session.messages || [];
      this.render();
    } catch (error) {
      new Notice(`Jarvis error: ${error.message}`);
    }
  }

  render() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass("jarvis-chat-view");

    const toolbar = contentEl.createDiv({ cls: "jarvis-chat-toolbar" });
    const modelSelect = toolbar.createEl("select");
    [
      ["Geral Safe", this.plugin.settings.generalModel],
      ["Programador Safe", this.plugin.settings.codeModel],
      ["Pesquisador Safe", this.plugin.settings.researchModel],
      ["Geral Quality", "jarvis"],
      ["Programador Quality", "jarvis-programador"],
      ["Pesquisador Quality", "jarvis-pesquisador"],
    ].forEach(([label, value]) => {
      const option = modelSelect.createEl("option", { text: label, value });
      option.value = value;
    });

    modelSelect.value = this.plugin.settings.chatModel || this.plugin.settings.generalModel;

    const workspaceInput = toolbar.createEl("input", {
      attr: { placeholder: "workspace" },
    });
    workspaceInput.value = this.plugin.settings.defaultWorkspace || "";

    const noteToggleLabel = toolbar.createEl("label");
    const noteToggle = noteToggleLabel.createEl("input", { attr: { type: "checkbox" } });
    noteToggle.checked = this.plugin.settings.chatUseCurrentNoteContext;
    noteToggleLabel.appendText(" nota atual");

    const newButton = toolbar.createEl("button", { text: "Nova" });
    const clearButton = toolbar.createEl("button", { text: "Limpar" });
    const messagesEl = contentEl.createDiv({ cls: "jarvis-chat-messages" });
    const composer = contentEl.createDiv({ cls: "jarvis-chat-composer" });
    const textarea = composer.createEl("textarea", { attr: { placeholder: "Pergunte algo ao Jarvis..." } });
    const sendButton = composer.createEl("button", { text: "Enviar" });

    const renderMessages = () => {
      messagesEl.empty();
      const source = this.messages.length ? this.messages : [{ role: "assistant", content: "Jarvis pronto." }];
      for (const message of source) {
        const node = messagesEl.createDiv({
          cls: `jarvis-chat-message ${message.role === "user" ? "is-user" : "is-assistant"}`,
        });
        node.setText(message.display_content || message.content);
      }
    };

    const send = async () => {
      const prompt = textarea.value.trim();
      if (!prompt) return;
      const model = modelSelect.value;
      const userPrompt = await this.plugin.buildChatPrompt({
        prompt,
        workspace: workspaceInput.value.trim(),
        useCurrentNoteContext: noteToggle.checked,
      });
      textarea.value = "";
      sendButton.disabled = true;
      try {
        await this.plugin.ensureChatSession({
          model,
          workspace: workspaceInput.value.trim() || null,
        });
        const payload = await this.plugin.sendSessionMessage({
          model,
          content: userPrompt,
          displayContent: prompt,
          workspace: workspaceInput.value.trim() || null,
        });
        this.messages = payload.session.messages || [];
        renderMessages();
      } catch (error) {
        new Notice(`Jarvis error: ${error.message}`);
      } finally {
        sendButton.disabled = false;
      }
    };

    newButton.addEventListener("click", async () => {
      try {
        await this.plugin.createFreshChatSession({
          model: modelSelect.value,
          workspace: workspaceInput.value.trim() || null,
        });
        this.messages = [];
        renderMessages();
      } catch (error) {
        new Notice(`Jarvis error: ${error.message}`);
      }
    });
    clearButton.addEventListener("click", () => {
      this.plugin.clearCurrentSession(modelSelect.value, workspaceInput.value.trim() || null)
        .then((session) => {
          this.messages = session.messages || [];
          renderMessages();
        })
        .catch((error) => new Notice(`Jarvis error: ${error.message}`));
    });
    modelSelect.addEventListener("change", async () => {
      this.plugin.settings.chatModel = modelSelect.value;
      await this.plugin.saveSettings();
    });
    workspaceInput.addEventListener("change", async () => {
      this.plugin.settings.defaultWorkspace = workspaceInput.value.trim();
      await this.plugin.saveSettings();
    });
    noteToggle.addEventListener("change", async () => {
      this.plugin.settings.chatUseCurrentNoteContext = noteToggle.checked;
      await this.plugin.saveSettings();
    });
    sendButton.addEventListener("click", send);
    textarea.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        send();
      }
    });

    renderMessages();
  }
}

class JarvisSettingTab extends PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();

    new Setting(containerEl)
      .setName("API base")
      .setDesc("Jarvis Core local URL")
      .addText((text) =>
        text.setValue(this.plugin.settings.apiBase).onChange(async (value) => {
          this.plugin.settings.apiBase = value.trim();
          await this.plugin.saveSettings();
        }),
      );

    new Setting(containerEl)
      .setName("General model")
      .addText((text) =>
        text.setValue(this.plugin.settings.generalModel).onChange(async (value) => {
          this.plugin.settings.generalModel = value.trim();
          await this.plugin.saveSettings();
        }),
      );

    new Setting(containerEl)
      .setName("Code model")
      .addText((text) =>
        text.setValue(this.plugin.settings.codeModel).onChange(async (value) => {
          this.plugin.settings.codeModel = value.trim();
          await this.plugin.saveSettings();
        }),
      );

    new Setting(containerEl)
      .setName("Research model")
      .addText((text) =>
        text.setValue(this.plugin.settings.researchModel).onChange(async (value) => {
          this.plugin.settings.researchModel = value.trim();
          await this.plugin.saveSettings();
        }),
      );

    new Setting(containerEl)
      .setName("Chat model")
      .addText((text) =>
        text.setValue(this.plugin.settings.chatModel).onChange(async (value) => {
          this.plugin.settings.chatModel = value.trim() || this.plugin.settings.generalModel;
          await this.plugin.saveSettings();
        }),
      );

    new Setting(containerEl)
      .setName("Append responses to note")
      .addToggle((toggle) =>
        toggle.setValue(this.plugin.settings.appendResponsesToNote).onChange(async (value) => {
          this.plugin.settings.appendResponsesToNote = value;
          await this.plugin.saveSettings();
        }),
      );

    new Setting(containerEl)
      .setName("Response heading prefix")
      .addText((text) =>
        text.setValue(this.plugin.settings.responseHeadingPrefix).onChange(async (value) => {
          this.plugin.settings.responseHeadingPrefix = value.trim() || "Jarvis";
          await this.plugin.saveSettings();
        }),
      );

    new Setting(containerEl)
      .setName("Default workspace")
      .addText((text) =>
        text.setValue(this.plugin.settings.defaultWorkspace).onChange(async (value) => {
          this.plugin.settings.defaultWorkspace = value.trim();
          await this.plugin.saveSettings();
        }),
      );

    new Setting(containerEl)
      .setName("Derived notes folder")
      .setDesc("Pasta padrão para notas criadas pelo Jarvis.")
      .addText((text) =>
        text.setPlaceholder("Jarvis")
          .setValue(this.plugin.settings.createNewNotesInFolder)
          .onChange(async (value) => {
            this.plugin.settings.createNewNotesInFolder = value.trim() || "Jarvis";
            await this.plugin.saveSettings();
          }),
      );

    new Setting(containerEl)
      .setName("Use current note in chat")
      .addToggle((toggle) =>
        toggle.setValue(this.plugin.settings.chatUseCurrentNoteContext).onChange(async (value) => {
          this.plugin.settings.chatUseCurrentNoteContext = value;
          await this.plugin.saveSettings();
        }),
      );

    new Setting(containerEl)
      .setName("Persist chat history")
      .addToggle((toggle) =>
        toggle.setValue(this.plugin.settings.persistChatHistory).onChange(async (value) => {
          this.plugin.settings.persistChatHistory = value;
          if (!value) {
            this.plugin.settings.currentChatSessionId = "";
          }
          await this.plugin.saveSettings();
        }),
      );
  }
}

module.exports = class JarvisLocalPlugin extends Plugin {
  async onload() {
    await this.loadSettings();

    this.registerView(VIEW_TYPE_JARVIS_CHAT, (leaf) => new JarvisChatView(leaf, this));
    this.addRibbonIcon("bot", "Jarvis Chat", () => this.activateView());
    this.addSettingTab(new JarvisSettingTab(this.app, this));

    this.addCommand({
      id: "open-chat-view",
      name: "Open Jarvis Chat",
      callback: () => this.activateView(),
    });

    this.addCommand({
      id: "check-connection",
      name: "Jarvis: Check Connection",
      callback: async () => {
        try {
          const status = await this.getStatus();
          new Notice(`Jarvis ok. Ollama: ${status.ollama?.status || "unknown"}`);
        } catch (error) {
          new Notice(`Jarvis connection error: ${error.message}`);
        }
      },
    });

    this.addCommand({
      id: "chat-current-note",
      name: "Jarvis: Chat About Current Note",
      callback: async () => {
        await this.runOnActiveNote({
          model: this.settings.generalModel,
          instruction: "Leia esta nota e proponha melhorias objetivas em Markdown.",
          heading: `${this.settings.responseHeadingPrefix} Chat`,
        });
      },
    });

    this.addCommand({
      id: "send-current-note-to-chat",
      name: "Jarvis: Send Current Note To Chat View",
      callback: async () => {
        const context = await this.getCurrentNoteContext();
        if (!context) {
          new Notice("Nenhuma nota Markdown ativa.");
          return;
        }
        await this.activateView();
        const leaves = this.app.workspace.getLeavesOfType(VIEW_TYPE_JARVIS_CHAT);
        const view = leaves[0]?.view;
        if (view && typeof view.sendExternalMessage === "function") {
          await view.sendExternalMessage(context, "Contexto da nota atual enviado ao Jarvis.");
        }
      },
    });

    this.addCommand({
      id: "send-selection-to-chat",
      name: "Jarvis: Send Selection To Chat View",
      editorCallback: async (editor) => {
        const selected = editor.getSelection().trim();
        if (!selected) {
          new Notice("Selecione algum texto primeiro.");
          return;
        }
        await this.activateView();
        const leaves = this.app.workspace.getLeavesOfType(VIEW_TYPE_JARVIS_CHAT);
        const view = leaves[0]?.view;
        if (view && typeof view.sendExternalMessage === "function") {
          await view.sendExternalMessage(`Selecao atual da nota:\n\n${selected}`, "Selecao atual enviada ao Jarvis.");
          new Notice("Selecao enviada para o chat do Jarvis.");
        }
      },
    });

    this.addCommand({
      id: "remember-current-note",
      name: "Jarvis: Remember Current Note In Workspace Memory",
      callback: async () => {
        await this.rememberCurrentNote();
      },
    });

    this.addCommand({
      id: "sync-current-note-to-knowledge",
      name: "Jarvis: Sync Current Note To Knowledge Base",
      callback: async () => {
        await this.syncCurrentNoteToKnowledgeBase();
      },
    });

    this.addCommand({
      id: "sync-current-folder-to-knowledge",
      name: "Jarvis: Sync Current Folder To Knowledge Base",
      callback: async () => {
        await this.syncCurrentFolderToKnowledgeBase();
      },
    });

    this.addCommand({
      id: "research-current-note",
      name: "Jarvis: Research Current Note",
      callback: async () => {
        await this.runOnActiveNote({
          model: this.settings.researchModel,
          instruction: "Pesquise usando o contexto local do Jarvis e complemente esta nota em Markdown.",
          heading: `${this.settings.responseHeadingPrefix} Research`,
        });
      },
    });

    this.addCommand({
      id: "summarize-current-note",
      name: "Jarvis: Summarize Current Note",
      callback: async () => {
        await this.runOnActiveNote({
          model: this.settings.generalModel,
          instruction: "Resuma esta nota em Markdown, destacando pontos-chave, lacunas e próximos passos.",
          heading: `${this.settings.responseHeadingPrefix} Summary`,
        });
      },
    });

    this.addCommand({
      id: "create-note-from-current-note",
      name: "Jarvis: Create New Note From Current Note",
      callback: async () => {
        await this.runOnActiveNote({
          model: this.settings.generalModel,
          instruction: "Crie uma nova nota derivada desta nota em Markdown, com titulo, resumo, topicos principais e proximos passos.",
          heading: `${this.settings.responseHeadingPrefix} Derived`,
          createNewNote: true,
        });
      },
    });

    this.addCommand({
      id: "ask-about-selection",
      name: "Jarvis: Ask About Selection",
      editorCallback: async (editor, view) => {
        const selected = editor.getSelection().trim();
        if (!selected) {
          new Notice("Selecione algum texto primeiro.");
          return;
        }
        try {
          const answer = await this.chat(this.settings.codeModel, [
            { role: "user", content: `Explique ou melhore esta seleção do Obsidian:\n\n${selected}` },
          ]);
          if (this.settings.appendResponsesToNote) {
            editor.replaceSelection(`${selected}\n\n> Jarvis\n>\n> ${answer.replace(/\n/g, "\n> ")}\n`);
            new Notice("Resposta do Jarvis inserida na nota.");
          } else {
            await navigator.clipboard.writeText(answer);
            new Notice("Resposta do Jarvis copiada para a área de transferência.");
          }
        } catch (error) {
          new Notice(`Jarvis error: ${error.message}`);
        }
      },
    });
  }

  async onunload() {
    if (!this.settings.persistChatHistory) {
      this.settings.currentChatSessionId = "";
      await this.saveSettings();
    }
    this.app.workspace.detachLeavesOfType(VIEW_TYPE_JARVIS_CHAT);
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    if (!this.settings.persistChatHistory) {
      this.settings.currentChatSessionId = "";
    }
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }

  async activateView() {
    let leaf = this.app.workspace.getLeavesOfType(VIEW_TYPE_JARVIS_CHAT)[0];
    if (!leaf) {
      leaf = this.app.workspace.getRightLeaf(false);
      await leaf.setViewState({ type: VIEW_TYPE_JARVIS_CHAT, active: true });
    }
    this.app.workspace.revealLeaf(leaf);
  }

  async ensureChatSession({ model, workspace }) {
    if (this.settings.currentChatSessionId) {
      try {
        return await this.requestJson(`/api/chat/sessions/${this.settings.currentChatSessionId}`);
      } catch {
        this.settings.currentChatSessionId = "";
        await this.saveSettings();
      }
    }
    return this.createFreshChatSession({ model, workspace });
  }

  async createFreshChatSession({ model, workspace }) {
    const payload = await this.requestJson("/api/chat/sessions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer local",
      },
      body: JSON.stringify({
        model,
        workspace,
      }),
    });
    this.settings.currentChatSessionId = payload.session.id;
    if (this.settings.persistChatHistory) {
      await this.saveSettings();
    }
    return payload;
  }

  async getCurrentSessionMessages() {
    if (!this.settings.currentChatSessionId) return [];
    const payload = await this.requestJson(`/api/chat/sessions/${this.settings.currentChatSessionId}`);
    return payload.session.messages || [];
  }

  async sendSessionMessage({ model, content, displayContent, workspace }) {
    await this.ensureChatSession({ model, workspace });
    return this.requestJson(`/api/chat/sessions/${this.settings.currentChatSessionId}/message`, {
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
  }

  async clearCurrentSession(model, workspace) {
    await this.ensureChatSession({ model, workspace });
    const payload = await this.requestJson(`/api/chat/sessions/${this.settings.currentChatSessionId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer local",
      },
      body: JSON.stringify({
        model,
        workspace,
        messages: [],
      }),
    });
    return payload.session;
  }

  async chat(model, messages) {
    const payload = await this.requestJson("/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer local",
      },
      body: JSON.stringify({ model, messages }),
    });
    return payload.choices?.[0]?.message?.content || "Sem resposta.";
  }

  async getStatus() {
    return this.requestJson("/api/status");
  }

  async requestJson(path, options = {}) {
    const response = await requestUrl({
      url: `${this.settings.apiBase}${path}`,
      method: options.method || "GET",
      headers: options.headers,
      body: options.body,
    });
    return JSON.parse(response.text);
  }

  async postJson(path, payload) {
    return this.requestJson(path, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer local",
      },
      body: JSON.stringify(payload),
    });
  }

  async buildChatPrompt({ prompt, workspace, useCurrentNoteContext }) {
    const pieces = [];
    const effectiveWorkspace = workspace || this.settings.defaultWorkspace || "";
    if (effectiveWorkspace) {
      pieces.push(`[WORKSPACE: ${effectiveWorkspace}]`);
    }
    if (useCurrentNoteContext) {
      const context = await this.getCurrentNoteContext();
      if (context) {
        pieces.push(context);
      }
    }
    pieces.push(prompt);
    return pieces.join("\n\n");
  }

  async getCurrentNoteContext() {
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view) return "";
    const file = view.file;
    const content = await this.readMarkdownViewContent(view);
    const workspace = this.inferWorkspace(file.path, content);
    return (
      `[OBSIDIAN_NOTE]\n` +
      `path: ${file.path}\n` +
      `workspace: ${workspace || "none"}\n\n` +
      `${content}`
    );
  }

  sanitizeFileName(value) {
    return value
      .replace(/[\\/:*?"<>|#^[\]]+/g, "-")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 80) || "jarvis-note";
  }

  async createDerivedNote(sourceFile, heading, content) {
    const folder = (this.settings.createNewNotesInFolder || "Jarvis").replace(/^\/+|\/+$/g, "");
    if (folder && !this.app.vault.getAbstractFileByPath(folder)) {
      await this.app.vault.createFolder(folder);
    }
    const baseName = sourceFile?.basename || "nota";
    const safeBaseName = this.sanitizeFileName(baseName);
    const suffix = heading.toLowerCase().replace(/\s+/g, "-");
    const fileName = `${safeBaseName}-${suffix}.md`;
    const fullPath = folder ? `${folder}/${fileName}` : fileName;
    const body = `# ${heading}\n\nFonte: [[${baseName}]]\n\n${content.trim()}\n`;
    const existing = this.app.vault.getAbstractFileByPath(fullPath);
    if (existing) {
      await this.app.vault.modify(existing, body);
      return existing;
    }
    return this.app.vault.create(fullPath, body);
  }

  async rememberCurrentNote() {
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view || !view.file) {
      new Notice("Nenhuma nota Markdown ativa.");
      return;
    }
    const content = await this.readMarkdownViewContent(view);
    const workspace = this.inferWorkspace(view.file.path, content) || this.settings.defaultWorkspace || "jarvis";
    const field = `obsidian.${this.sanitizeFileName(view.file.basename).replace(/\s+/g, "-").toLowerCase()}`;
    const excerpt = content.trim().slice(0, 1600);
    await this.postJson("/api/memory/workspace", {
      workspace,
      field,
      value: `Nota: ${view.file.basename}\nPath: ${view.file.path}\n\n${excerpt}`,
      source: "obsidian-plugin",
    });
    new Notice(`Nota salva na memória do workspace '${workspace}'.`);
  }

  async syncCurrentNoteToKnowledgeBase() {
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view || !view.file) {
      new Notice("Nenhuma nota Markdown ativa.");
      return;
    }
    const content = await this.readMarkdownViewContent(view);
    const domain = this.inferWorkspace(view.file.path, content) || this.settings.defaultWorkspace || "pessoal";
    const payload = await this.postJson("/api/knowledge/ingest-note", {
      domain,
      title: view.file.basename,
      content,
      source_path: view.file.path,
    });
    new Notice(`Nota sincronizada para a base '${payload.domain}'.`);
  }

  async syncCurrentFolderToKnowledgeBase() {
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view || !view.file || !view.file.parent) {
      new Notice("Nenhuma nota Markdown ativa.");
      return;
    }
    const folderPath = view.file.parent.path;
    const markdownFiles = this.app.vault.getMarkdownFiles().filter((file) => file.path.startsWith(`${folderPath}/`) || file.path === view.file.path);
    if (!markdownFiles.length) {
      new Notice("Nenhuma nota Markdown encontrada na pasta atual.");
      return;
    }

    let synced = 0;
    for (const file of markdownFiles) {
      const content = await this.app.vault.cachedRead(file);
      const domain = this.inferWorkspace(file.path, content) || this.settings.defaultWorkspace || "pessoal";
      await this.postJson("/api/knowledge/ingest-note", {
        domain,
        title: file.basename,
        content,
        source_path: file.path,
      });
      synced += 1;
    }
    new Notice(`Jarvis sincronizou ${synced} nota(s) da pasta atual.`);
  }

  async runOnActiveNote({ model, instruction, heading, createNewNote = false }) {
    const view = this.app.workspace.getActiveViewOfType(MarkdownView);
    if (!view) {
      new Notice("Nenhuma nota Markdown ativa.");
      return;
    }
    const file = view.file;
    const content = await this.readMarkdownViewContent(view);
    const workspace = this.inferWorkspace(file.path, content);
    const prompt =
      `Você está ajudando com uma nota do Obsidian.\n` +
      `Path da nota: ${file.path}\n` +
      `Workspace inferido: ${workspace || "none"}\n` +
      `Tarefa: ${instruction}\n\n` +
      `Conteúdo da nota:\n${content}`;

    try {
      const answer = await this.chat(model, [{ role: "user", content: prompt }]);
      if (createNewNote) {
        const derived = await this.createDerivedNote(file, heading, answer);
        await this.app.workspace.getLeaf(true).openFile(derived);
      } else if (this.settings.appendResponsesToNote) {
        const stamp = new Date().toISOString().slice(0, 16).replace("T", " ");
        const block = `\n\n## ${heading} (${stamp})\n\n${answer}\n`;
        const latest = await this.app.vault.cachedRead(file);
        await this.app.vault.modify(file, `${latest}${block}`);
      } else {
        await navigator.clipboard.writeText(answer);
      }
      new Notice("Resposta do Jarvis pronta.");
    } catch (error) {
      new Notice(`Jarvis error: ${error.message}`);
    }
  }

  inferWorkspace(notePath, content) {
    const fm = parseFrontmatter(content);
    if (fm.workspace) return fm.workspace;
    const parts = notePath.toLowerCase().split("/");
    for (const candidate of ["jarvis", "faculdade", "crossfit", "programacao", "minecraft", "linux", "musculacao", "pessoal"]) {
      if (parts.includes(candidate)) return candidate;
    }
    return "";
  }

  async readMarkdownViewContent(view) {
    if (view.editor && typeof view.editor.getValue === "function") {
      return view.editor.getValue();
    }
    if (view.file) {
      return this.app.vault.cachedRead(view.file);
    }
    return "";
  }
};

function parseFrontmatter(content) {
  if (!content.startsWith("---\n")) return {};
  const end = content.indexOf("\n---\n", 4);
  if (end === -1) return {};
  const block = content.slice(4, end);
  const result = {};
  for (const line of block.split("\n")) {
    if (!line.includes(":")) continue;
    const [key, ...rest] = line.split(":");
    result[key.trim()] = rest.join(":").trim().replace(/^['"]|['"]$/g, "");
  }
  return result;
}
