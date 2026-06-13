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
   grep -q 'id="ctx-active-file"' "$HTML_FILE" && \
   grep -q 'id="ctx-open-tabs"' "$HTML_FILE" && \
   grep -q 'id="ctx-terminal"' "$HTML_FILE" && \
   grep -q 'id="ctx-search"' "$HTML_FILE" && \
   grep -q 'id="composer-context-preview"' "$HTML_FILE" && \
   grep -q 'id="session-search"' "$HTML_FILE" && \
   grep -q 'id="export-chat"' "$HTML_FILE" && \
   grep -q 'id="workspace-files"' "$HTML_FILE" && \
   grep -q 'id="workspace-search"' "$HTML_FILE" && \
   grep -q 'id="run-workspace-search"' "$HTML_FILE" && \
   grep -q 'id="clear-workspace-search"' "$HTML_FILE" && \
   grep -q 'id="new-folder"' "$HTML_FILE" && \
   grep -q 'id="open-path"' "$HTML_FILE" && \
   grep -q 'id="editor-tabs"' "$HTML_FILE" && \
   grep -q 'id="editor-instruction"' "$HTML_FILE" && \
   grep -q 'id="editor-selection"' "$HTML_FILE" && \
   grep -q 'id="ask-jarvis-batch-edit"' "$HTML_FILE" && \
   grep -q 'id="apply-batch-proposal"' "$HTML_FILE" && \
   grep -q 'id="editor-batch-output"' "$HTML_FILE" && \
   grep -q 'id="editor-batch-proposals"' "$HTML_FILE" && \
   grep -q 'id="run-task-assist"' "$HTML_FILE" && \
   grep -q 'id="run-task-cycle"' "$HTML_FILE" && \
   grep -q 'id="run-suggested-command"' "$HTML_FILE" && \
   grep -q 'id="editor-task-output"' "$HTML_FILE" && \
   grep -q 'id="editor-diff"' "$HTML_FILE" && \
   grep -q 'id="editor-hunks"' "$HTML_FILE" && \
   grep -q 'id="ask-jarvis-edit"' "$HTML_FILE" && \
   grep -q 'id="apply-proposal"' "$HTML_FILE" && \
   grep -q 'id="rename-file"' "$HTML_FILE" && \
   grep -q 'id="delete-file"' "$HTML_FILE" && \
   grep -q 'id="terminal-sessions"' "$HTML_FILE" && \
   grep -q 'id="new-terminal"' "$HTML_FILE" && \
   grep -q 'id="close-terminal"' "$HTML_FILE" && \
   grep -q 'id="restart-terminal"' "$HTML_FILE" && \
   grep -q 'id="interrupt-terminal"' "$HTML_FILE"; then
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

WORKSPACE_SEARCH=$(curl -fsS "$BASE_URL/api/workspace/search?q=Jarvis&limit=5" \
  -H 'authorization: Bearer local')
if printf '%s' "$WORKSPACE_SEARCH" | grep -q '"results"'; then
  echo "[ok] workspace search endpoint responded"
else
  echo "[fail] workspace search endpoint did not respond as expected"
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

TERMINAL_SESSION_ID=$(curl -fsS -X POST "$BASE_URL/api/terminal/sessions" \
  -H 'content-type: application/json' \
  -H 'authorization: Bearer local' \
  -d '{"cwd":".","cols":80,"rows":24}' | \
  sed -n 's/.*"session_id": *"\([^"]*\)".*/\1/p' | head -n 1)

if [ -z "$TERMINAL_SESSION_ID" ]; then
  echo "[fail] could not create terminal session"
  exit 1
fi

TERMINAL_WRITE=$(curl -fsS -X POST "$BASE_URL/api/terminal/sessions/$TERMINAL_SESSION_ID/write" \
  -H 'content-type: application/json' \
  -H 'authorization: Bearer local' \
  -d '{"data":"printf pwa-terminal-ok\n","wait_ms":120}')
TERMINAL_READ=$(curl -fsS "$BASE_URL/api/terminal/sessions/$TERMINAL_SESSION_ID/read?wait_ms=200" \
  -H 'authorization: Bearer local')
curl -fsS -X DELETE "$BASE_URL/api/terminal/sessions/$TERMINAL_SESSION_ID" \
  -H 'authorization: Bearer local' >/dev/null

if printf '%s\n%s\n' "$TERMINAL_WRITE" "$TERMINAL_READ" | grep -q 'pwa-terminal-ok'; then
  echo "[ok] persistent terminal session executed a bash command"
else
  echo "[fail] terminal session did not return expected output"
  exit 1
fi

echo "[ok] PWA smoke passed"
