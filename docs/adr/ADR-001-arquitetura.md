# ADR-001 — Arquitetura da aplicação

- **Status:** Proposto para revisão do grupo
- **Data:** 2026-11-09
- **Decisores:** integrantes do grupo
- **Relacionados:** `docs/arquitetura.md`, `docs/tradeoffs.md`

## Contexto

O sistema precisa apoiar abertura e atendimento de chamados, prioridade, SLA, equipe, comentários e histórico. O grupo está construindo um MVP acadêmico e ainda está refinando as fronteiras dos módulos. O fluxo principal usa dados relacionados que precisam permanecer consistentes.

## Decisão proposta

Adotar um **monólito modular organizado em camadas**, com uma única aplicação implantável e módulos internos para identidade e acesso, atendimento, catálogo/equipes, prioridade/SLA e notificações.

Os casos de uso dependem de interfaces para persistência e notificações. Regras de domínio, como matriz de prioridade e transições de estado, não dependem do framework web nem do banco escolhido.

## Alternativas consideradas

### Monólito sem separação explícita

Seria simples no começo, mas aumenta o risco de misturar interface, casos de uso, regras e persistência. Isso dificulta testes e mudanças posteriores.

### Microsserviços

Separariam módulos em aplicações independentes, mas acrescentariam chamadas de rede, implantação múltipla, monitoramento e tratamento de falhas distribuídas. Não há requisito atual que justifique esse custo.

### Microkernel

É útil quando o produto oferece funcionalidades extensíveis por plugins. O escopo atual não prevê plugins nem extensões instaláveis.

## Consequências

### Positivas

- Uma aplicação e uma implantação para o MVP.
- Chamado, histórico e SLA podem ser coordenados com transações locais.
- Regras centrais ficam testáveis isoladamente.
- Interfaces deixam possíveis trocas futuras de banco e mecanismo de notificação.

### Negativas

- A equipe precisa manter limites de módulo e evitar dependências cruzadas sem controle.
- Todos os módulos são publicados juntos.
- Módulos não podem escalar independentemente.
- A divisão lógica não garante separação física: a estrutura do código precisa preservar as fronteiras.

## Evidências para reavaliar

Reabrir este ADR se os requisitos passarem a exigir implantação independente, escala específica por módulo, equipes autônomas ou isolamento operacional que a aplicação única não consiga atender.
