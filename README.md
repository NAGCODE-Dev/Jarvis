# Jarvis v1

Jarvis is a local-first personal assistant for Ubuntu Linux. This repository contains:

- `Jarvis Core`: a FastAPI backend that exposes an OpenAI-compatible router and internal memory/RAG APIs
- `Open WebUI` and `Qdrant` infrastructure via Docker Compose
- persistent Markdown-based memory
- local knowledge ingestion for RAG
- VS Code Continue configuration for local coding workflows

Default model profile in this repo prioritizes quality over speed:

- planning/general: `gemma4:e4b`
- coding: `qwen3:8b`
- fallbacks: `gemma4:e2b`, `qwen3:4b`, `qwen3:1.7b`

## Quick start

1. Run `scripts/install_host.sh`
2. Run `scripts/pull_models.sh`
3. Start infra with `scripts/start_infra.sh`
4. Start the backend with `scripts/run_core.sh`
5. Open `http://localhost:3000` for Open WebUI
6. Run `scripts/benchmark_models.sh` to generate local model rankings
7. Run `scripts/seed_demo.sh` if you want a first pre-populated context

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
scripts/start_infra.sh
scripts/stop_infra.sh
scripts/status.sh
scripts/seed_demo.sh
scripts/show_context.sh --workspace jarvis
scripts/memory_action.sh update_state weight.current_kg 72
```

## Structure

- `apps/core/`: Python backend
- `config/`: prompts, routing rules, Continue config, env template
- `data/`: persistent memory and knowledge folders
- `infra/`: Docker Compose services
- `scripts/`: installation, indexing, benchmarks and smoke tests

## Current v1 capabilities

- OpenAI-compatible router for `Open WebUI` and `Continue`
- structured memory writes via `MemoryAction`
- identity/state/workspace memory separation
- Qdrant-backed local RAG
- benchmarked model rankings persisted in `data/benchmark/model_rankings.json`
- CLI helpers for indexing, benchmark and memory/context inspection
