# Obsidian Shell Commands

Integração recomendada para a v1: usar o plugin `Shell Commands` do Obsidian.

## Comandos sugeridos

### 1. Chat sobre a nota atual

```bash
/home/nikolasa/Downloads/Jarvis/scripts/obsidian_chat.sh "{{file_path:absolute}}" "Leia esta nota e proponha melhorias objetivas."
```

### 2. Pesquisa com contexto local

```bash
/home/nikolasa/Downloads/Jarvis/scripts/obsidian_research.sh "{{file_path:absolute}}" "Pesquise usando a base local e complemente esta nota."
```

### 3. Resumo da nota

```bash
/home/nikolasa/Downloads/Jarvis/scripts/obsidian_summarize_note.sh "{{file_path:absolute}}"
```

### 4. Salvar nota na memória do workspace

```bash
/home/nikolasa/Downloads/Jarvis/scripts/obsidian_remember_note.sh "{{file_path:absolute}}"
```

### 5. Sincronizar nota para a knowledge base local

```bash
/home/nikolasa/Downloads/Jarvis/scripts/obsidian_sync_note.sh "{{file_path:absolute}}"
```

### 6. Sincronizar uma pasta inteira de notas

```bash
/home/nikolasa/Downloads/Jarvis/scripts/obsidian_sync_dir.sh "{{folder_path:absolute}}"
```

## Frontmatter suportado

Você pode adicionar frontmatter para melhorar o roteamento:

```yaml
---
workspace: faculdade
jarvis_mode: research
---
```

Campos:

- `workspace`: força o contexto de workspace
- `jarvis_mode`: `research`, `code`, `programming`, `study`

## Comportamento

- o Jarvis lê a nota inteira
- infere o workspace pelo frontmatter ou pelo caminho
- responde em Markdown
- anexa a resposta no fim da própria nota
- também pode salvar a nota na memória do workspace
- também pode sincronizar a nota para RAG local
