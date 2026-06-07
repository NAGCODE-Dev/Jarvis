#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  docker compose -f "$ROOT_DIR/infra/docker-compose.yml" up -d
  exit 0
fi

if command -v docker-compose >/dev/null 2>&1; then
  docker-compose -f "$ROOT_DIR/infra/docker-compose.yml" up -d
  exit 0
fi

echo "[jarvis] Docker Compose not found. Install Docker or run scripts/install_host.sh first."
exit 1

