#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PID_FILE="$ROOT_DIR/logs/jarvis-core.pid"
HOST="${JARVIS_HOST:-127.0.0.1}"
PORT="${JARVIS_PORT:-8000}"
stopped=0

stop_pid() {
  pid="$1"
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid"
    echo "[jarvis] Stopped Jarvis core PID $pid"
    stopped=1
  fi
}

if [ -f "$PID_FILE" ]; then
  pid=$(cat "$PID_FILE" 2>/dev/null || true)
  stop_pid "$pid"
  if [ "$stopped" -eq 0 ]; then
    echo "[jarvis] PID file existed but process was not running."
  fi
else
  echo "[jarvis] No PID file found."
fi

rm -f "$PID_FILE"

port_pid=""
if command -v ss >/dev/null 2>&1; then
  port_pid=$(ss -ltnp "sport = :$PORT" 2>/dev/null | awk -F 'pid=' 'NR > 1 && NF > 1 {split($2, a, ","); print a[1]; exit}')
elif command -v lsof >/dev/null 2>&1; then
  port_pid=$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -n 1 || true)
fi

if [ -n "$port_pid" ]; then
  stop_pid "$port_pid"
fi

if [ "$stopped" -eq 0 ]; then
  echo "[jarvis] No running Jarvis core process found on ${HOST}:${PORT}."
fi
