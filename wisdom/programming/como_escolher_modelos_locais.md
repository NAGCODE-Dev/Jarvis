# Como Escolher Modelos Locais

## Heurística

- Escolha pelo tempo de ciclo completo, não pelo benchmark isolado.
- Um modelo menor com retrieval bom costuma bater um modelo maior mal configurado no hardware doméstico.
- Mantenha o modelo de código separado do modelo geral se o hardware permitir.

## Regras de Decisão

- Se o hardware é CPU-only com 16 GB RAM, priorize estabilidade, contexto curto e corpus forte.
- Se duas respostas quentes ficam mais lentas que a primeira, investigue modelos residentes e paralelismo antes de trocar de LLM.
