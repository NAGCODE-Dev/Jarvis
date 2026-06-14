#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
eval "$($ROOT_DIR/scripts/_runtime_env.sh "$ROOT_DIR")"
SMOKE_DIR="$JARVIS_RUNTIME_HOME/continue-smoke"
SMOKE_FILE="$SMOKE_DIR/continue_smoke.py"

mkdir -p "$SMOKE_DIR"

cat > "$SMOKE_FILE" <<'EOF'
"""Continue smoke test file for Jarvis local integration."""


def bubble_sort(values):
    for i in range(len(values)):
        for j in range(len(values) - 1):
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
    return values


def render_workout(plan):
    return " -> ".join(plan)


if __name__ == "__main__":
    print(bubble_sort([5, 3, 4, 1, 2]))
    print(render_workout(["warmup", "strength", "metcon"]))
EOF

"$ROOT_DIR/scripts/continue_preflight.sh"

echo
echo "[jarvis] Continue smoke file prepared:"
echo "  $SMOKE_FILE"
echo
echo "[jarvis] Suggested tests inside VS Code / Continue"
echo "1. Open: $SMOKE_FILE"
echo "2. Chat with 'Jarvis Programador Quality':"
echo "   Explique este arquivo e proponha melhorias objetivas."
echo "3. Select bubble_sort and use Edit:"
echo "   Refatore para ficar mais legível e adicione type hints."
echo "4. Select render_workout and use Edit:"
echo "   Torne esta função mais robusta para listas vazias."
echo "5. Test autocomplete:"
echo "   Add a new function below named training_summary and stop after 'def training_summary(plan):'"
echo "6. Chat with 'Jarvis Geral Quality':"
echo "   Com base no workspace Jarvis, o que este projeto já suporta hoje?"
echo "7. Chat with 'Jarvis Pesquisador':"
echo "   Procure contexto documental local sobre Linux ou CrossFit se existir."
