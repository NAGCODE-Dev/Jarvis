#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
LOG_DIR="$ROOT_DIR/logs"
PID_FILE="$LOG_DIR/jarvis-core.pid"
LOG_FILE="$LOG_DIR/jarvis-core.log"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
HOST="${JARVIS_HOST:-127.0.0.1}"
PORT="${JARVIS_PORT:-8000}"
SEED_DEMO=1
RUN_BENCHMARK=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --no-seed)
      SEED_DEMO=0
      ;;
    --benchmark)
      RUN_BENCHMARK=1
      ;;
    *)
      echo "[jarvis] Unknown option: $1"
      echo "Usage: scripts/boot_local.sh [--no-seed] [--benchmark]"
      exit 1
      ;;
  esac
  shift
done

mkdir -p "$LOG_DIR"

if [ ! -x "$VENV_PYTHON" ]; then
  echo "[jarvis] Virtual environment not found. Run scripts/install_host.sh first."
  exit 1
fi

echo "[jarvis] Applying quality profile"
"$ROOT_DIR/scripts/apply_quality_profile.sh"

echo "[jarvis] Starting infra when available"
if ! "$ROOT_DIR/scripts/start_infra.sh"; then
  echo "[jarvis] Infra startup skipped; continuing with degraded local mode"
fi

if [ "$SEED_DEMO" -eq 1 ]; then
  echo "[jarvis] Seeding demo memory"
  "$ROOT_DIR/scripts/seed_demo.sh"
fi

if [ -f "$PID_FILE" ]; then
  old_pid=$(cat "$PID_FILE" 2>/dev/null || true)
  if [ -n "${old_pid}" ] && kill -0 "$old_pid" 2>/dev/null; then
    echo "[jarvis] Jarvis core already running with PID $old_pid"
  else
    rm -f "$PID_FILE"
  fi
fi

if [ ! -f "$PID_FILE" ]; then
  echo "[jarvis] Starting Jarvis core on ${HOST}:${PORT}"
  nohup "$ROOT_DIR/scripts/run_core.sh" >"$LOG_FILE" 2>&1 &
  new_pid=$!
  echo "$new_pid" > "$PID_FILE"
fi

echo "[jarvis] Waiting for core health"
attempt=0
until curl -fsS "http://${HOST}:${PORT}/health" >/dev/null 2>&1; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 30 ]; then
    echo "[jarvis] Core did not become healthy in time. Check $LOG_FILE"
    exit 1
  fi
  sleep 1
done

echo "[jarvis] Core is healthy"
"$ROOT_DIR/scripts/status.sh" || true

if [ "$RUN_BENCHMARK" -eq 1 ]; then
  echo "[jarvis] Running benchmark"
  "$ROOT_DIR/scripts/benchmark_models.sh" || true
fi

echo "[jarvis] Preparing Continue smoke"
"$ROOT_DIR/scripts/continue_smoke.sh"

echo
echo "[jarvis] Boot complete"
echo "Core URL: http://${HOST}:${PORT}"
echo "Log file: $LOG_FILE"
echo "PID file: $PID_FILE"
echo
echo "Next steps:"
echo "1. Open VS Code: code \"$ROOT_DIR\""
echo "2. Use Continue with Jarvis Programador Quality"
echo "3. Follow CONTINUE_TESTS.md"
