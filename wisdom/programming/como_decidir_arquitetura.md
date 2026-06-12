# Como Decidir Arquitetura

## Heurística

- Comece pelo fluxo principal do negócio.
- Modele as mudanças esperadas, não as imaginadas.
- Prefira modularidade antes de distribuição.
- Separe o que muda rápido do que deve ser estável.

## Regras de Decisão

- Se só uma equipe mexe no sistema, microserviço cedo demais provavelmente é custo.
- Se a dependência externa domina risco, isole o adaptador.
- Se não há observabilidade, a arquitetura ainda não está pronta para crescer.
