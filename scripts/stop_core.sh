#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PID_FILE="$ROOT_DIR/logs/jarvis-core.pid"

if [ ! -f "$PID_FILE" ]; then
  echo "[jarvis] No PID file found."
  exit 0
fi

pid=$(cat "$PID_FILE" 2>/dev/null || true)
if [ -n "${pid}" ] && kill -0 "$pid" 2>/dev/null; then
  kill "$pid"
  echo "[jarvis] Stopped Jarvis core PID $pid"
else
  echo "[jarvis] PID file existed but process was not running."
fi

rm -f "$PID_FILE"
