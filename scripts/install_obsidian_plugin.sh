#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PLUGIN_SRC="$ROOT_DIR/apps/obsidian-plugin/jarvis-local"

if [ "$#" -lt 1 ]; then
  echo "Usage: scripts/install_obsidian_plugin.sh /path/to/obsidian/vault"
  exit 1
fi

VAULT_DIR=$1
PLUGIN_DEST="$VAULT_DIR/.obsidian/plugins/jarvis-local"
OBSIDIAN_DIR="$VAULT_DIR/.obsidian"
COMMUNITY_PLUGINS_FILE="$OBSIDIAN_DIR/community-plugins.json"

mkdir -p "$PLUGIN_DEST"
mkdir -p "$OBSIDIAN_DIR"
cp "$PLUGIN_SRC/manifest.json" "$PLUGIN_DEST/manifest.json"
cp "$PLUGIN_SRC/main.js" "$PLUGIN_DEST/main.js"
cp "$PLUGIN_SRC/styles.css" "$PLUGIN_DEST/styles.css"

if [ ! -f "$COMMUNITY_PLUGINS_FILE" ]; then
  printf '[]\n' > "$COMMUNITY_PLUGINS_FILE"
fi

python3 - <<'PY' "$COMMUNITY_PLUGINS_FILE"
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
if "jarvis-local" not in payload:
    payload.append("jarvis-local")
path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PY

echo "[jarvis] Obsidian plugin installed to:"
echo "  $PLUGIN_DEST"
echo
echo "[jarvis] Next steps:"
echo "1. Open Obsidian"
echo "2. Enable community plugins if needed"
echo "3. Confirm 'Jarvis Local' is enabled"
