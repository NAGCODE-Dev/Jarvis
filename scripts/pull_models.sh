#!/usr/bin/env sh
set -eu

MODELS="
gemma4:e4b
gemma4:e2b
qwen3:8b
qwen3:4b
qwen3:1.7b
nomic-embed-text
"

for model in $MODELS; do
  echo "[jarvis] Pulling $model"
  ollama pull "$model"
done
