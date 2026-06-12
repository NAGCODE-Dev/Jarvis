# Jarvis Local Obsidian Plugin

Plugin local do Obsidian para falar direto com a API do Jarvis.

O chat lateral prefere streaming quando o runtime do Obsidian suporta `fetch` com stream. Se não suportar, ele faz fallback automático para resposta tradicional.

## Recursos

- chat lateral dentro do Obsidian
- chat com contexto opcional da nota atual
- chat lateral usando sessões persistidas do Jarvis
- lista de sessões no próprio chat lateral
- busca local de sessões no próprio chat lateral
- renomeação rápida da sessão ativa
- ações rápidas no painel para nota atual, seleção, resumo, pesquisa e exportação
- ação por mensagem para salvar uma resposta específica do Jarvis como nota derivada
- ação por mensagem para inserir uma resposta específica diretamente na nota ativa
- anexos no composer do chat para nota atual e seleção atual antes do envio
- comando para verificar conexão com o Jarvis
- comando para conversar sobre a nota atual
- comando para pesquisar com base local do Jarvis
- comando para resumir a nota atual
- comando para mandar a nota atual para o chat lateral
- comando para mandar a seleção atual para o chat lateral
- comando para perguntar sobre a seleção atual
- comando para criar uma nota derivada a partir da nota atual
- comando para salvar a nota atual na memória do workspace
- comando para sincronizar a nota atual com a base de conhecimento do Jarvis
- comando para sincronizar em lote a pasta atual do Obsidian com a base de conhecimento
- comando para exportar a sessão atual do chat para uma nota Markdown

## Instalação

Copie esta pasta para:

```text
<vault>/.obsidian/plugins/jarvis-local/
```

Ou use:

```bash
/home/nikolasa/Downloads/Jarvis/scripts/install_obsidian_plugin.sh /caminho/do/vault
```

Depois, no Obsidian:

1. ative `Community Plugins`
2. ative `Jarvis Local`

## Configuração

Configuração padrão:

- API base: `http://127.0.0.1:8000`
- general model: `jarvis-safe`
- code model: `jarvis-programador-safe`
- research model: `jarvis-pesquisador-safe`
- chat model: `jarvis-safe`
- derived notes folder: `Jarvis`
- use current note in chat: `true`
- persist chat history: controla se a sessão lateral continua entre reinicializações
- current chat session id: persistido nas settings do plugin

## Requisito

O Jarvis Core precisa estar rodando localmente:

```bash
cd /home/nikolasa/Downloads/Jarvis
scripts/boot_local.sh --no-seed
```
