#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
GLOBAL_CONTINUE_CONFIG="${HOME}/.continue/config.yaml"
PROJECT_CONTINUE_CONFIG="$ROOT_DIR/config/continue/config.yaml"
STATUS_URL="http://127.0.0.1:8000/api/status"

echo "[jarvis] Continue preflight"
echo

if [ -f "$GLOBAL_CONTINUE_CONFIG" ]; then
  echo "[ok] Continue global config found: $GLOBAL_CONTINUE_CONFIG"
else
  echo "[warn] Continue global config missing: $GLOBAL_CONTINUE_CONFIG"
fi

if [ -f "$PROJECT_CONTINUE_CONFIG" ]; then
  echo "[ok] Project Continue config found: $PROJECT_CONTINUE_CONFIG"
else
  echo "[warn] Project Continue config missing: $PROJECT_CONTINUE_CONFIG"
fi

if command -v curl >/dev/null 2>&1; then
  if curl -fsS "$STATUS_URL" >/tmp/jarvis-continue-status.json 2>/dev/null; then
    echo "[ok] Jarvis core reachable at $STATUS_URL"
    cat /tmp/jarvis-continue-status.json
    rm -f /tmp/jarvis-continue-status.json
  else
    echo "[warn] Jarvis core not reachable at $STATUS_URL"
    echo "       Start it with: scripts/run_core.sh"
  fi
else
  echo "[warn] curl not found; skipping API status check"
fi

if command -v code >/dev/null 2>&1; then
  echo "[ok] VS Code command available: $(command -v code)"
else
  echo "[warn] VS Code command not found in PATH"
fi

echo
echo "[jarvis] Recommended VS Code test flow"
echo "1. Run: scripts/run_core.sh"
echo "2. In another terminal run: scripts/continue_preflight.sh"
echo "3. Open this folder in VS Code: code \"$ROOT_DIR\""
echo "4. Reload window in VS Code: Ctrl+Shift+P -> Developer: Reload Window"
echo "5. Open Continue and select:"
echo "   - Jarvis Programador Quality"
echo "   - Jarvis Geral Quality"
echo "   - Jarvis Pesquisador"
echo "6. Test chat: 'Explique este arquivo e sugira melhorias'"
echo "7. Test edit/apply on a selected block"
echo "8. Test autocomplete in a code file"
