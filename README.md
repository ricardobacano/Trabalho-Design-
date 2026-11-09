# Sistema de Gerenciamento de Chamados de Suporte Técnico

Projeto final da disciplina **Design de Software — Tema 16**.

## Visão geral

O grupo está projetando um sistema de suporte técnico inspirado no fluxo de chamados do GLPI e em práticas de gestão de serviços associadas ao ITIL.

O sistema permitirá que solicitantes autenticados abram chamados ou que um técnico os registre em nome de alguém. O chamado é encaminhado para uma equipe; um técnico da equipe pode assumi-lo. Prioridade, SLA, interações e mudanças ficam registrados até o encerramento.

A arquitetura em avaliação é um **monólito modular organizado em camadas**. A linguagem, o framework e o banco de dados ainda serão escolhidos pelo grupo e alinhados com a professora.

## Escopo atual do MVP

- Login obrigatório para solicitantes e equipe de suporte.
- Abertura de chamado por solicitante ou por técnico em nome do solicitante.
- Encaminhamento por categoria para uma equipe padrão; casos sem correspondência vão para triagem do coordenador.
- Cálculo de prioridade com base em impacto e urgência.
- Fila da equipe e assunção por técnico.
- Comentários públicos e anotações internas.
- Histórico de alterações e acompanhamento do SLA.
- Notificações internas simuladas.
- Resolução e fechamento pelo solicitante; reabertura permitida somente enquanto o chamado estiver Resolvido.

O escopo e os tempos de SLA ainda devem ser validados com a professora.

## Documentação

| Documento | Conteúdo |
|---|---|
| [Requisitos](docs/requisitos.md) | Objetivo, escopo, atores, requisitos e regras de negócio. |
| [Prioridade e ciclo de vida](docs/prioridade-e-ciclo-de-vida.md) | Matriz de impacto × urgência, SLA, calendário e estados do chamado. |
| [Modelo de domínio](docs/modelo-dominio.md) | Conceitos, relações e responsabilidades do domínio. |
| [Arquitetura](docs/arquitetura.md) | Proposta de monólito modular em camadas e limites dos módulos. |
| [Trade-offs](docs/tradeoffs.md) | Benefícios, custos e alternativas consideradas. |
| [Plano de implementação e testes](docs/plano-implementacao-e-testes.md) | Marcos do MVP, critérios de aceite e casos de teste. |
| [ADR-001 — Arquitetura](docs/adr/ADR-001-arquitetura.md) | Registro da decisão arquitetural, ainda sujeito à revisão do grupo/professora. |

## Diagramas

- [Classes](docs/diagramas/classes.puml)
- [Sequência de abertura](docs/diagramas/sequencia.puml)
- [Comunicação da abertura](docs/diagramas/comunicacao.puml)
- [Componentes](docs/diagramas/componentes.puml)

## Estrutura prevista

```text
.
├── README.md
├── docs/
│   ├── requisitos.md
│   ├── prioridade-e-ciclo-de-vida.md
│   ├── modelo-dominio.md
│   ├── arquitetura.md
│   ├── tradeoffs.md
│   ├── plano-implementacao-e-testes.md
│   ├── adr/
│   │   └── ADR-001-arquitetura.md
│   └── diagramas/
│       ├── classes.puml
│       ├── sequencia.puml
│       ├── comunicacao.puml
│       └── componentes.puml
├── src/       # a definir após a escolha da stack
└── tests/     # a definir após a escolha da stack
```

Os ADRs sobre autenticação e persistência serão criados quando as decisões correspondentes forem confirmadas.

## Desenvolvimento

O grupo pretende integrar o trabalho por Pull Requests:

- `main`: versão estável para entrega.
- `develop`: integração do trabalho.
- `feature/*`, `docs/*` e `fix/*`: branches curtas para tarefas.

A stack e as instruções para executar a aplicação serão adicionadas ao README assim que forem definidas e o esqueleto do projeto estiver disponível.

