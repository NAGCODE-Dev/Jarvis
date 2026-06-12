# Manual Validation

Use este checklist para validar o Jarvis v1 no navegador e no Obsidian real.

## Preparação

1. Rode `scripts/boot_local.sh --no-seed`
2. Confirme `scripts/verify_local.sh --rag-smoke`
3. Se for validar Obsidian, reinstale o plugin:
   `scripts/install_obsidian_plugin.sh /caminho/do/vault`

## PWA

Abra:

```text
http://127.0.0.1:8000/app/
```

Verificações:

1. Criar uma nova conversa.
2. Renomear a conversa.
3. Filtrar a conversa pelo campo de busca.
4. Usar um atalho rápido de agente.
5. Anexar um arquivo `.md` ou `.txt`.
6. Enviar uma pergunta e confirmar streaming visual da resposta.
7. Exportar a conversa atual para Markdown.
8. Recarregar a página e confirmar que a conversa anterior foi restaurada.
9. Excluir a conversa atual.

Smoke rápido:

```bash
scripts/pwa_smoke.sh
```

## Obsidian Plugin

No Obsidian, recarregue os plugins e valide:

1. `Jarvis: Check Connection`
2. No painel `Jarvis Chat`, testar os botões `Nota atual`, `Seleção`, `Resumo`, `Pesquisa` e `Exportar`
3. No painel `Jarvis Chat`, enviar uma mensagem e usar `Salvar resposta` em uma resposta específica
4. No painel `Jarvis Chat`, enviar uma mensagem e usar `Inserir na nota` em uma resposta específica
5. No painel `Jarvis Chat`, testar `Anexar nota` e `Anexar seleção` antes de enviar uma pergunta
6. `Jarvis: Send Current Note To Chat View`
7. `Jarvis: Send Selection To Chat View`
8. `Jarvis: Remember Current Note In Workspace Memory`
9. `Jarvis: Sync Current Note To Knowledge Base`
10. `Jarvis: Sync Current Folder To Knowledge Base`
11. `Jarvis: Create New Note From Current Note`
12. `Jarvis: Export Current Chat Session To Note`

Resultados esperados:

- a nota atual deve aparecer no chat lateral como contexto limpo
- a memória do workspace deve ser atualizada em `data/memory/workspaces/<workspace>/`
- a sync para knowledge base deve criar arquivos em `data/knowledge/<workspace>/obsidian/`
- a exportação de sessão deve gerar uma nota Markdown no vault

## Shell Commands do Obsidian

Se você usar `Shell Commands`, valide:

```bash
scripts/obsidian_chat.sh /path/to/note.md
scripts/obsidian_research.sh /path/to/note.md
scripts/obsidian_summarize_note.sh /path/to/note.md
scripts/obsidian_remember_note.sh /path/to/note.md
scripts/obsidian_sync_note.sh /path/to/note.md
scripts/obsidian_sync_dir.sh /path/to/folder
```

## Continue / VS Code

1. Abra o workspace no VS Code.
2. Confirme que Continue vê o endpoint local do Jarvis.
3. Teste chat, edit/apply e autocomplete com os perfis configurados.

## Aceite final

Considere o Jarvis v1 validado quando:

- PWA funcionar com sessões, anexos, streaming e exportação
- plugin do Obsidian funcionar com chat, memória, sync e export
- RAG responder com documento indexado local
- Continue conseguir conversar com o router local
