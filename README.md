# Jarvis v1

Jarvis is a local-first personal assistant for Ubuntu Linux. This repository contains:

- `Jarvis Core`: a FastAPI backend that exposes an OpenAI-compatible router and internal memory/RAG APIs
- `Open WebUI` and `Qdrant` infrastructure via Docker Compose
- persistent Markdown-based memory
- local knowledge ingestion for RAG
- VS Code Continue configuration for local coding workflows

Default model profile in this repo prioritizes local stability on 16 GB RAM / CPU-only machines:

- planning/general: `qwen2.5:3b`
- coding/codex: `qwen2.5-coder:1.5b`
- coding fallback: `qwen2.5:3b`
- general fallback: `qwen3:1.7b`

Runtime model selection is controlled by `JARVIS_MODEL_SELECTION_STRATEGY`:

- `quality`: prefer stronger models unless benchmark/RAM say otherwise
- `balanced`: trade off capability and latency
- `speed`: prefer faster models when benchmark shows a large latency gap

## Quick start

1. Run `scripts/first_run.sh`
2. Open `http://localhost:3000` for Open WebUI when Docker/WebUI are available
3. Open the project in VS Code and test Continue

Local PWA chat:

1. Start Jarvis Core
2. Open `http://127.0.0.1:8000/app/`
3. Install it as an app from the browser if desired

If Docker/Qdrant are unavailable, Jarvis still works in degraded local mode:

- chat continues through Ollama
- memory continues through local Markdown + JSON indexes
- RAG falls back to local Qdrant storage under `data/qdrant-local/`
- embeddings fall back to deterministic local embeddings when `nomic-embed-text` is missing

## First usable flow

Seed memory without editing Markdown manually:

```bash
python3 -m jarvis.cli memory-action set_identity_fact profile.name "Nikolas"
python3 -m jarvis.cli memory-action update_preference preferences.editor "VS Code"
python3 -m jarvis.cli memory-action update_state weight.current_kg 72
python3 -m jarvis.cli memory-action append_workspace_note current_focus "router + memory service" --workspace jarvis
python3 -m jarvis.cli show-context --workspace jarvis
python3 -m jarvis.cli status
```

Useful API calls:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/api/memory/action \
  -H 'content-type: application/json' \
  -d '{"action":"update_state","field":"weight.current_kg","value":72,"source":"manual"}'
curl 'http://127.0.0.1:8000/api/memory/context?workspace=jarvis'
curl -X POST http://127.0.0.1:8000/api/benchmark/run \
  -H 'content-type: application/json' \
  -d '{}'
```

Continue configuration is in `config/continue/config.yaml`.

Useful helper scripts:

```bash
scripts/first_run.sh
scripts/boot_local.sh
scripts/verify_local.sh
scripts/apply_quality_profile.sh
scripts/continue_preflight.sh
scripts/continue_smoke.sh
scripts/start_infra.sh
scripts/stop_core.sh
scripts/stop_infra.sh
scripts/status.sh
scripts/seed_demo.sh
scripts/show_context.sh --workspace jarvis
scripts/memory_action.sh update_state weight.current_kg 72
scripts/chat.sh "resuma o estado atual do projeto"
scripts/code_chat.sh "explique este arquivo" --file apps/core/jarvis/router.py
scripts/research_chat.sh "o que existe sobre linux localmente?"
scripts/chat_repl.sh
scripts/code_chat_repl.sh
scripts/research_chat_repl.sh
scripts/obsidian_chat.sh /path/to/note.md
scripts/obsidian_research.sh /path/to/note.md
scripts/obsidian_summarize_note.sh /path/to/note.md
scripts/obsidian_remember_note.sh /path/to/note.md
scripts/obsidian_sync_note.sh /path/to/note.md
scripts/obsidian_sync_dir.sh /path/to/folder
scripts/install_obsidian_plugin.sh /path/to/vault
scripts/obsidian_plugin_smoke.sh
scripts/pwa_smoke.sh
```

To force the local environment to use the strongest default profile again:

```bash
scripts/apply_quality_profile.sh
```

For the fastest local coding profile on this hardware:

```bash
scripts/apply_speed_profile.sh
scripts/boot_local.sh --speed --no-seed
```

## Structure

- `apps/core/`: Python backend
- `config/`: prompts, routing rules, Continue config, env template
- `data/`: persistent memory and knowledge folders
- `infra/`: Docker Compose services
- `scripts/`: installation, indexing, benchmarks and smoke tests

## Current v1 capabilities

- OpenAI-compatible router for `Open WebUI` and `Continue`
- local PWA chat interface at `/app/`
- structured memory writes via `MemoryAction`
- identity/state/workspace memory separation
- Qdrant-backed local RAG
- benchmarked model rankings persisted in `data/benchmark/model_rankings.json`
- CLI helpers for indexing, benchmark and memory/context inspection

## VS Code / Continue

Preflight:

```bash
scripts/boot_local.sh
scripts/continue_preflight.sh
scripts/continue_smoke.sh
```

Recommended manual validation:

1. Run `scripts/first_run.sh`
2. Open the workspace with `code /home/nikolasa/Downloads/Jarvis`
3. Reload the VS Code window
4. In Continue, use `Jarvis Programador Quality` for code tasks
5. Prefer `Jarvis Codex Local` for iterative code edits on CPU-only hardware
6. Try chat, edit/apply and autocomplete in a real project file

Detailed checklist:

- [CONTINUE_TESTS.md](/home/nikolasa/Downloads/Jarvis/CONTINUE_TESTS.md:1)

Operational verification:

```bash
scripts/verify_local.sh
scripts/verify_local.sh --rag-smoke
scripts/pwa_smoke.sh
```

Manual runtime checklist:

- [MANUAL_VALIDATION.md](/home/nikolasa/Downloads/Jarvis/MANUAL_VALIDATION.md:1)

## Local PWA Chat

Jarvis now exposes a lightweight local PWA chat UI:

```bash
scripts/boot_local.sh --no-seed
```

Open:

```text
http://127.0.0.1:8000/app/
```

Recommended usage:

1. Start with `Jarvis Codex Local` or `Jarvis Programador Safe`.
2. Use the quality profiles only for slower but stronger responses.
3. Long conversations are compacted automatically before hitting Ollama, so the app stays usable even when the visible chat grows.
4. Install the PWA from the browser if you want Jarvis as a standalone local app.

The PWA supports:

- persistent chat sessions in the backend under `data/sessions/`
- quick model/profile switching
- workspace hint field
- rename and delete of saved conversations
- restore of the last selected conversation in the browser
- quick actions for `geral`, `programador`, `pesquisador`, `professor` and `coach`
- attachment of local files/notes directly into the prompt
- streamed responses in the chat UI
- filtering of saved conversations
- Markdown export of the current conversation
- installable app shell via manifest + service worker

## VS Code / Terminal Workflow

If Continue is too slow on CPU-only hardware, use the VS Code terminal and talk to Jarvis directly:

```bash
scripts/chat.sh "qual meu peso atual?"
scripts/code_chat.sh "analise este arquivo e proponha melhorias" --file apps/core/jarvis/router.py
scripts/research_chat.sh "procure contexto local sobre linux"
```

For a more chat-like experience in the terminal:

```bash
scripts/chat_repl.sh
scripts/code_chat_repl.sh
scripts/research_chat_repl.sh
```

Inside the REPL:

```text
/exit
/clear
/model jarvis-codex
/file apps/core/jarvis/router.py
```

You can also pipe content from shell commands:

```bash
sed -n '1,220p' apps/core/jarvis/router.py | scripts/code_chat.sh "explique este código" --stdin
git diff | scripts/code_chat.sh "revise este diff e aponte riscos" --stdin
```

Recommended usage in VS Code:

1. Open the integrated terminal.
2. Keep `scripts/boot_local.sh --no-seed` running in one terminal only when needed.
3. Use `scripts/code_chat.sh` for code questions and file reviews.
4. Use `rg`, `sed`, `git diff` and pipe the output into Jarvis instead of relying on the Continue panel.

## Obsidian Integration

Jarvis now supports a Markdown-first Obsidian workflow without a custom plugin.

Scripts:

```bash
scripts/obsidian_chat.sh /absolute/path/to/note.md
scripts/obsidian_research.sh /absolute/path/to/note.md
scripts/obsidian_summarize_note.sh /absolute/path/to/note.md
scripts/obsidian_remember_note.sh /absolute/path/to/note.md
scripts/obsidian_sync_note.sh /absolute/path/to/note.md
scripts/obsidian_sync_dir.sh /absolute/path/to/folder
```

What they do:

- read the note
- infer `workspace` from frontmatter or path
- route to the appropriate Jarvis profile
- return Markdown
- append the response at the end of the note

Supported frontmatter:

```yaml
---
workspace: faculdade
jarvis_mode: research
---
```

Recommended Obsidian setup:

1. Install the `Shell Commands` plugin.
2. Add commands from [config/obsidian/SHELL_COMMANDS.md](/home/nikolasa/Downloads/Jarvis/config/obsidian/SHELL_COMMANDS.md:1).
3. Run the command on the current note.

## Obsidian Plugin

Jarvis now also includes a real local Obsidian plugin:

- plugin path:
  [apps/obsidian-plugin/jarvis-local](/home/nikolasa/Downloads/Jarvis/apps/obsidian-plugin/jarvis-local/manifest.json)

Install:

```bash
scripts/install_obsidian_plugin.sh /path/to/your/obsidian/vault
```

Then in Obsidian:

1. enable Community Plugins
2. enable `Jarvis Local`

What the plugin supports:

- side chat view inside Obsidian
- side chat with optional current-note context
- side chat backed by Jarvis backend chat sessions
- `Jarvis: Check Connection`
- `Jarvis: Chat About Current Note`
- `Jarvis: Research Current Note`
- `Jarvis: Summarize Current Note`
- `Jarvis: Send Current Note To Chat View`
- `Jarvis: Send Selection To Chat View`
- `Jarvis: Ask About Selection`
- `Jarvis: Create New Note From Current Note`
- `Jarvis: Remember Current Note In Workspace Memory`
- `Jarvis: Sync Current Note To Knowledge Base`
- `Jarvis: Sync Current Folder To Knowledge Base`
- `Jarvis: Export Current Chat Session To Note`

These two commands make the Obsidian integration materially more useful:

- workspace memory command:
  stores the current note as scoped memory under `data/memory/workspaces/<workspace>/`
- knowledge sync command:
  copies the current note into `data/knowledge/<workspace>/obsidian/` and indexes it for local RAG

Operational requirement:

```bash
scripts/boot_local.sh --no-seed
```

Detailed plugin notes:

- [apps/obsidian-plugin/jarvis-local/README.md](/home/nikolasa/Downloads/Jarvis/apps/obsidian-plugin/jarvis-local/README.md:1)

Operational smoke:

```bash
scripts/obsidian_plugin_smoke.sh
```
