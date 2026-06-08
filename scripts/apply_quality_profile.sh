#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
ENV_FILE="$ROOT_DIR/.env"

ensure_key() {
  key="$1"
  value="$2"

  if [ -f "$ENV_FILE" ] && grep -q "^${key}=" "$ENV_FILE"; then
    tmp_file=$(mktemp)
    sed "s|^${key}=.*|${key}=${value}|" "$ENV_FILE" > "$tmp_file"
    mv "$tmp_file" "$ENV_FILE"
  else
    printf '%s=%s\n' "$key" "$value" >> "$ENV_FILE"
  fi
}

touch "$ENV_FILE"

ensure_key "JARVIS_HOST" "127.0.0.1"
ensure_key "JARVIS_PORT" "8000"
ensure_key "JARVIS_LOG_LEVEL" "info"
ensure_key "JARVIS_OLLAMA_BASE_URL" "http://127.0.0.1:11434"
ensure_key "JARVIS_QDRANT_URL" "http://127.0.0.1:6333"
ensure_key "JARVIS_QDRANT_COLLECTION" "jarvis-knowledge"
ensure_key "JARVIS_PLANNER_MODEL" "gemma4:e4b"
ensure_key "JARVIS_PLANNER_FALLBACK_MODEL" "gemma4:e2b"
ensure_key "JARVIS_CODER_MODEL" "qwen3:8b"
ensure_key "JARVIS_CODER_FALLBACK_MODEL" "qwen3:1.7b"
ensure_key "JARVIS_EMBEDDING_MODEL" "nomic-embed-text"
ensure_key "JARVIS_DEFAULT_RESPONSE_LANGUAGE" "auto"
ensure_key "JARVIS_MODEL_SELECTION_STRATEGY" "quality"
ensure_key "JARVIS_MEMORY_ARCHIVE_DAYS" "30"

echo "[jarvis] Quality profile applied to $ENV_FILE"
