# Continue Smoke Tests

## Preconditions

1. Run `scripts/run_core.sh`
2. Run `scripts/continue_smoke.sh`
3. Open the generated file `.continue-smoke/continue_smoke.py` in VS Code
4. Reload the VS Code window

## Model Selection

Use these Continue models:

- `Jarvis Programador Quality`
- `Jarvis Geral Quality`
- `Jarvis Pesquisador`

## Chat Test

With `Jarvis Programador Quality`:

```text
Explique este arquivo e proponha melhorias objetivas.
```

Expected:

- explain `bubble_sort`
- identify readability improvements
- preserve code-oriented tone

## Edit / Apply Test

Select `bubble_sort` and ask:

```text
Refatore para ficar mais legível e adicione type hints.
```

Expected:

- cleaner loop structure
- type annotations
- no unrelated changes

Select `render_workout` and ask:

```text
Torne esta função mais robusta para listas vazias.
```

Expected:

- safe handling for empty list
- small, localized edit

## Autocomplete Test

At the end of the file, type:

```python
def training_summary(plan):
```

Expected:

- inline suggestion appears
- suggestion is short and code-focused

## General Jarvis Test

Switch to `Jarvis Geral Quality` and ask:

```text
Com base no workspace Jarvis, o que este projeto já suporta hoje?
```

Expected:

- summary of local assistant capabilities
- mention memory/context/RAG/router when relevant

## Research Test

Switch to `Jarvis Pesquisador` and ask:

```text
Procure contexto documental local sobre Linux ou CrossFit se existir.
```

Expected:

- use local indexed knowledge when available
- mention source paths when retrieval occurs
