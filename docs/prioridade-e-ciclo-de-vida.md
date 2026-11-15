# Prioridade, prazo e estados

## 1. Matriz de prioridade

| Impacto \ Urgência | Alta | Média | Baixa |
|---|---|---|---|
| Alto | P1 - Crítica | P2 - Alta | P3 - Média |
| Médio | P2 - Alta | P3 - Média | P4 - Baixa |
| Baixo | P3 - Média | P4 - Baixa | P4 - Baixa |

A matriz está implementada somente em **MatrizPrioridade**. Alterá-la exige
atualizar essa classe e os nove testes parametrizados.

## 2. Prazo inicial do protótipo

| Prioridade | Prazo inicial |
|---|---:|
| P1 - Crítica | 4 horas corridas |
| P2 - Alta | 8 horas corridas |
| P3 - Média | 48 horas corridas |
| P4 - Baixa | 120 horas corridas |

Esses valores são uma política didática do protótipo. Não são apresentados como
valores obrigatórios do ITIL. Calendário comercial, feriados e pausas não fazem
parte da fatia implementada.

## 3. Estados

| Estado | Significado |
|---|---|
| **EM_FILA** | Chamado encaminhado à equipe da categoria. |
| **EM_TRIAGEM** | Categoria válida sem equipe padrão; aguarda encaminhamento. |
| **EM_ATENDIMENTO** | Técnico assumiu o chamado. |
| **RESOLVIDO** | Solução foi registrada. |
| **FECHADO** | Atendimento foi encerrado. |

A fatia implementa a criação em **EM_FILA** ou **EM_TRIAGEM**. As transições
seguintes estão no modelo para orientar evolução, mas não fazem parte do protótipo.
