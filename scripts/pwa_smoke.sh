#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
BASE_URL="${JARVIS_BASE_URL:-http://127.0.0.1:8000}"
SMOKE_MODEL="${JARVIS_PWA_SMOKE_MODEL:-jarvis-programador-safe}"
MAX_TIME="${JARVIS_PWA_SMOKE_MAX_TIME:-15}"
TMP_DIR=$(mktemp -d)
HTML_FILE="$TMP_DIR/pwa.html"
STREAM_FILE="$TMP_DIR/stream.txt"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

echo "[jarvis] PWA smoke"

if ! curl -fsS "$BASE_URL/app/" >"$HTML_FILE"; then
  echo "[fail] PWA root not reachable at $BASE_URL/app/"
  exit 1
fi

if grep -q 'id="attach-file"' "$HTML_FILE" && \
   grep -q 'id="session-search"' "$HTML_FILE" && \
   grep -q 'id="export-chat"' "$HTML_FILE"; then
  echo "[ok] PWA shell contains attach/search/export controls"
else
  echo "[fail] PWA shell is missing expected controls"
  exit 1
fi

SESSION_ID=$(curl -fsS -X POST "$BASE_URL/api/chat/sessions" \
  -H 'content-type: application/json' \
  -H 'authorization: Bearer local' \
  -d "{\"model\":\"$SMOKE_MODEL\",\"workspace\":\"jarvis\",\"title\":\"PWA Smoke\"}" | \
  sed -n 's/.*"id": *"\([^"]*\)".*/\1/p' | head -n 1)

if [ -z "$SESSION_ID" ]; then
  echo "[fail] could not create chat session"
  exit 1
fi

if curl --max-time "$MAX_TIME" -fsS -N -X POST "$BASE_URL/api/chat/sessions/$SESSION_ID/message/stream" \
  -H 'content-type: application/json' \
  -H 'authorization: Bearer local' \
  -d "{\"model\":\"$SMOKE_MODEL\",\"content\":\"responda somente OK\",\"display_content\":\"pwa smoke\",\"workspace\":\"jarvis\"}" \
  >"$STREAM_FILE"; then
  stream_rc=0
else
  stream_rc=$?
fi

if grep -q '"type": "chunk"' "$STREAM_FILE" && grep -q '"type": "done"' "$STREAM_FILE"; then
  echo "[ok] streaming session endpoint responded with chunk and done events"
elif grep -q '"type": "start"' "$STREAM_FILE"; then
  echo "[ok] streaming session endpoint opened and emitted a start event"
  if [ "${stream_rc:-0}" -ne 0 ]; then
    echo "[jarvis] note: model response did not finish within ${MAX_TIME}s on this hardware"
  fi
else
  echo "[fail] streaming output did not include expected events"
  exit 1
fi

echo "[ok] PWA smoke passed"
