#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
eval "$($ROOT_DIR/scripts/_runtime_env.sh "$ROOT_DIR")"
ENV_FILE="$JARVIS_ENV_FILE"
mkdir -p "$(dirname "$ENV_FILE")"

ensure_key() {
  key="$1"
  value="$2"

  if [ -f "$ENV_FILE" ] && grep -q "^${key}=" "$ENV_FILE"; then
    tmp_file=$(mktemp)
    sed "s|^${key}=.*|${key}=${value}|" "$ENV_FILE" > "$tmp_file"
    mv "$tmp_file" "$ENV_FILE"
  else
    printf '%s=%s
' "$key" "$value" >> "$ENV_FILE"
  fi
}

touch "$ENV_FILE"
ensure_key "JARVIS_HOST" "127.0.0.1"
ensure_key "JARVIS_PORT" "8000"
ensure_key "JARVIS_LOG_LEVEL" "info"
ensure_key "JARVIS_OLLAMA_BASE_URL" "http://127.0.0.1:11434"
ensure_key "JARVIS_QDRANT_URL" "http://127.0.0.1:6333"
ensure_key "JARVIS_QDRANT_COLLECTION" "jarvis-knowledge"
ensure_key "JARVIS_PLANNER_MODEL" "qwen2.5:3b"
ensure_key "JARVIS_PLANNER_FALLBACK_MODEL" "qwen3:1.7b"
ensure_key "JARVIS_CODER_MODEL" "qwen2.5-coder:1.5b"
ensure_key "JARVIS_CODER_FALLBACK_MODEL" "qwen2.5:3b"
ensure_key "JARVIS_SAFE_MODEL" "qwen2.5:3b"
ensure_key "JARVIS_SAFE_FALLBACK_MODEL" "qwen3:1.7b"
ensure_key "JARVIS_SAFE_CODER_MODEL" "qwen2.5-coder:1.5b"
ensure_key "JARVIS_SAFE_CODER_FALLBACK_MODEL" "qwen2.5:3b"
ensure_key "JARVIS_OLLAMA_NUM_CTX" "1024"
ensure_key "JARVIS_OLLAMA_KEEP_ALIVE" "10m"
ensure_key "JARVIS_EMBEDDING_MODEL" "nomic-embed-text"
ensure_key "JARVIS_DEFAULT_RESPONSE_LANGUAGE" "auto"
ensure_key "JARVIS_MODEL_SELECTION_STRATEGY" "balanced"
ensure_key "JARVIS_MEMORY_ARCHIVE_DAYS" "30"
ensure_key "JARVIS_HISTORY_COMPACTION_ENABLED" "true"
ensure_key "JARVIS_HISTORY_CHAR_BUDGET" "9000"
ensure_key "JARVIS_HISTORY_PRESERVE_MESSAGES" "6"

echo "[jarvis] Quality profile applied to $ENV_FILE"
