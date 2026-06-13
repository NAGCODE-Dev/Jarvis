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
8. Abrir um arquivo no painel `Workspace`, editar e salvar.
9. Criar um novo arquivo pelo botão `Novo arquivo`.
10. Abrir mais de um arquivo e trocar entre abas no editor.
11. Renomear e excluir um arquivo pelo editor integrado.
12. Pedir ao Jarvis uma edição no arquivo ativo e revisar o diff antes de aplicar.
13. Aplicar apenas um hunk específico da proposta e verificar o efeito no buffer.
14. Rodar `Jarvis tarefa` com o arquivo ativo e confirmar resumo, comando sugerido e proposta de edição.
15. Executar o comando sugerido no terminal pelo botão dedicado.
16. Usar `Anexar no chat` para mandar o conteúdo do arquivo aberto como contexto.
17. Clicar no terminal, digitar comandos reais em bash, usar `Enter`, `Tab`, setas e `Ctrl+C`.
18. Confirmar que `cd` persiste entre comandos no mesmo terminal.
19. Recarregar a página e confirmar que a conversa anterior foi restaurada.
20. Excluir a conversa atual.

Smoke rápido:

```bash
scripts/pwa_smoke.sh
```

## Aplicação Linux

Para validar o Jarvis como aplicação Linux local:

1. Rode `scripts/install_linux_app.sh`
2. Confirme que o launcher `jarvis-local` foi criado em `~/.local/bin`
3. Confirme que a entrada `.desktop` foi criada em `~/.local/share/applications/jarvis-local.desktop`
4. Abra pelo menu do sistema procurando `Jarvis Local` ou rode `jarvis-local`
5. Confirme que a interface abre em modo app apontando para `http://127.0.0.1:8000/app/`

Smoke rápido:

```bash
JARVIS_HOST=127.0.0.1 JARVIS_PORT=8000 scripts/linux_app_smoke.sh
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
- PWA permitir abrir/salvar arquivos do workspace e usar um terminal bash persistente dentro do app
- plugin do Obsidian funcionar com chat, memória, sync e export
- RAG responder com documento indexado local
- Continue conseguir conversar com o router local
