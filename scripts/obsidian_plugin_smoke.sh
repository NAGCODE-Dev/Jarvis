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

if ! grep -q 'text: "Pesquisa"' "$PLUGIN_DIR/main.js"; then
  echo "[jarvis] plugin quick actions were not installed"
  rm -rf "$TMP_DIR"
  exit 1
fi

if ! grep -q 'text: "Salvar resposta"' "$PLUGIN_DIR/main.js"; then
  echo "[jarvis] plugin per-message export action is missing"
  rm -rf "$TMP_DIR"
  exit 1
fi

if ! grep -q 'text: "Inserir na nota"' "$PLUGIN_DIR/main.js"; then
  echo "[jarvis] plugin per-message insert action is missing"
  rm -rf "$TMP_DIR"
  exit 1
fi

if ! grep -q 'text: "Anexar nota"' "$PLUGIN_DIR/main.js"; then
  echo "[jarvis] plugin attachment action for current note is missing"
  rm -rf "$TMP_DIR"
  exit 1
fi

if ! grep -q 'text: "Anexar seleção"' "$PLUGIN_DIR/main.js"; then
  echo "[jarvis] plugin attachment action for selection is missing"
  rm -rf "$TMP_DIR"
  exit 1
fi

if ! grep -q 'jarvis-chat-quick-actions' "$PLUGIN_DIR/styles.css"; then
  echo "[jarvis] plugin quick action styles are missing"
  rm -rf "$TMP_DIR"
  exit 1
fi

if ! grep -q 'jarvis-chat-message-actions' "$PLUGIN_DIR/styles.css"; then
  echo "[jarvis] plugin message action styles are missing"
  rm -rf "$TMP_DIR"
  exit 1
fi

if ! grep -q 'jarvis-chat-attachment-chip' "$PLUGIN_DIR/styles.css"; then
  echo "[jarvis] plugin attachment styles are missing"
  rm -rf "$TMP_DIR"
  exit 1
fi

if ! grep -q 'jarvis-local' "$COMMUNITY_PLUGINS_FILE"; then
  echo "[jarvis] plugin was not enabled in $COMMUNITY_PLUGINS_FILE"
  rm -rf "$TMP_DIR"
  exit 1
fi

echo "[jarvis] Obsidian plugin smoke passed"
echo "[jarvis] temp vault: $VAULT_DIR"

rm -rf "$TMP_DIR"
