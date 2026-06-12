# Como Projetar um RAG Local

## Heurística

- Curadoria de corpus vence prompt longo.
- Estrutura vence volume bruto.
- Metadados vencem scraping desorganizado.
- Knowledge e wisdom devem ficar separados.

## Regras de Decisão

- Se o modelo é pequeno, reduza ambiguidade da base antes de trocar de modelo.
- Se a resposta alucina, verifique recuperação e chunking antes de culpar o LLM.
- Se o contexto estoura, compacte histórico e aumente precisão do retrieval.
