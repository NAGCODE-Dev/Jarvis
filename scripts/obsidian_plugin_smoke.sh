#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TMP_DIR=$(mktemp -d)
VAULT_DIR="$TMP_DIR/vault"

mkdir -p "$VAULT_DIR"
"$ROOT_DIR/scripts/install_obsidian_plugin.sh" "$VAULT_DIR" >/dev/null

PLUGIN_DIR="$VAULT_DIR/.obsidian/plugins/jarvis-local"
COMMUNITY_PLUGINS_FILE="$VAULT_DIR/.obsidian/community-plugins.json"

for path in \
  "$PLUGIN_DIR/manifest.json" \
  "$PLUGIN_DIR/main.js" \
  "$PLUGIN_DIR/styles.css"
do
  if [ ! -f "$path" ]; then
    echo "[jarvis] missing plugin file: $path"
    rm -rf "$TMP_DIR"
    exit 1
  fi
done

if ! grep -q 'jarvis-local' "$COMMUNITY_PLUGINS_FILE"; then
  echo "[jarvis] plugin was not enabled in $COMMUNITY_PLUGINS_FILE"
  rm -rf "$TMP_DIR"
  exit 1
fi

echo "[jarvis] Obsidian plugin smoke passed"
echo "[jarvis] temp vault: $VAULT_DIR"

rm -rf "$TMP_DIR"
