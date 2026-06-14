#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
eval "$($ROOT_DIR/scripts/_runtime_env.sh "$ROOT_DIR")"
VENV_PYTHON="$JARVIS_VENV_DIR/bin/python"
STATUS_URL="http://127.0.0.1:8000/api/status"
GLOBAL_CONTINUE_CONFIG="${HOME}/.continue/config.yaml"
RAG_SMOKE=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --rag-smoke)
      RAG_SMOKE=1
      ;;
    *)
      echo "[jarvis] Unknown option: $1"
      echo "Usage: scripts/verify_local.sh [--rag-smoke]"
      exit 1
      ;;
  esac
  shift
done

failures=0
ok() { echo "[ok] $1"; }
warn() { echo "[warn] $1"; }
fail() { echo "[fail] $1"; failures=$((failures + 1)); }

echo "[jarvis] Local verification"
echo

if [ -x "$VENV_PYTHON" ]; then
  ok "virtualenv found: $VENV_PYTHON"
else
  fail "virtualenv missing; run scripts/install_host.sh or scripts/jarvis.sh setup-local"
fi

if [ -f "$JARVIS_ENV_FILE" ]; then
  ok ".env found: $JARVIS_ENV_FILE"
else
  fail ".env missing; run scripts/apply_quality_profile.sh, scripts/install_host.sh or scripts/jarvis.sh setup-local"
fi

if [ -f "$GLOBAL_CONTINUE_CONFIG" ]; then
  ok "Continue config found: $GLOBAL_CONTINUE_CONFIG"
else
  warn "Continue config missing: $GLOBAL_CONTINUE_CONFIG"
fi

if command -v curl >/dev/null 2>&1; then
  if curl -fsS "$STATUS_URL" >/tmp/jarvis-verify-status.json 2>/dev/null; then
    ok "Jarvis core reachable at $STATUS_URL"
    cat /tmp/jarvis-verify-status.json
    rm -f /tmp/jarvis-verify-status.json
  else
    fail "Jarvis core not reachable; start with scripts/run_core.sh or scripts/boot_local.sh"
  fi
else
  fail "curl not found"
fi

if command -v ollama >/dev/null 2>&1; then
  ok "ollama command available"
  ollama list 2>/dev/null || warn "ollama list failed"
else
  warn "ollama command not found in PATH from this shell"
fi

if command -v docker >/dev/null 2>&1; then
  ok "docker command available"
else
  warn "docker command not found; degraded local mode is expected"
fi

if [ "$RAG_SMOKE" -eq 1 ]; then
  echo
  echo "[jarvis] Running RAG smoke"
  mkdir -p "$JARVIS_DATA_DIR/knowledge/linux"
  SAMPLE_DOC="$JARVIS_DATA_DIR/knowledge/linux/verify-local.md"
  cat > "$SAMPLE_DOC" <<'EOF'
# Verify Local

Jarvis local verification document for Linux knowledge search.
EOF
  if curl -fsS -X POST "http://127.0.0.1:8000/api/knowledge/index" -H 'content-type: application/json' -d '{"domains":["linux"],"force":true}' >/tmp/jarvis-rag-index.json 2>/tmp/jarvis-rag-index.err; then
    ok "knowledge indexing succeeded"
    cat /tmp/jarvis-rag-index.json
  else
    fail "knowledge indexing failed"
    cat /tmp/jarvis-rag-index.err
  fi
  if curl -fsS -X POST "http://127.0.0.1:8000/api/knowledge/search" -H 'content-type: application/json' -d '{"query":"Jarvis local Linux verification","domain":"linux","top_k":1}' >/tmp/jarvis-rag-search.json 2>/tmp/jarvis-rag-search.err; then
    ok "knowledge search succeeded"
    cat /tmp/jarvis-rag-search.json
  else
    fail "knowledge search failed"
    cat /tmp/jarvis-rag-search.err
  fi
  rm -f "$SAMPLE_DOC" /tmp/jarvis-rag-index.json /tmp/jarvis-rag-index.err /tmp/jarvis-rag-search.json /tmp/jarvis-rag-search.err
fi

echo
if [ "$failures" -gt 0 ]; then
  echo "[jarvis] Verification finished with $failures failure(s)"
  exit 1
fi

echo "[jarvis] Verification finished successfully"
