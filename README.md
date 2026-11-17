# Plataforma de Atendimento Técnico de TI

Trabalho final da disciplina **Design e Arquitetura de Software (2026-2)**, Tema 16.

O repositório contém a documentação arquitetural e um protótipo executável de uma
plataforma de chamados. A fatia vertical implementada permite que um solicitante de
demonstração abra um chamado, receba prioridade e prazo iniciais, seja encaminhado
para uma equipe ou para triagem e consulte seus próprios chamados.

## O que está implementado

- abertura de chamado com resumo, descrição, categoria, impacto e urgência;
- cálculo da prioridade pela matriz impacto x urgência;
- cálculo de prazo inicial em horas corridas;
- encaminhamento para a equipe da categoria;
- fluxo alternativo para categoria sem equipe: fila de triagem;
- persistência transacional do chamado e do evento inicial de histórico;
- consulta de lista e detalhe dos chamados do usuário de demonstração;
- confirmação por um **NotificadorFake** substituível;
- tolerância à falha da notificação após a persistência;
- testes automatizados da regra e da fatia vertical.

O protótipo não implementa login completo. O usuário de demonstração é carregado
automaticamente, conforme permitido pelo enunciado.

## Executar

Requisitos: Python 3.11 ou superior.

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
~~~

Acesse: <http://127.0.0.1:5000>

Na primeira execução, o SQLite é criado em **instance/chamados.db** e recebe
usuários, equipes e categorias de demonstração.

## Testar

~~~bash
source .venv/bin/activate
pytest
~~~

Os testes cobrem as nove combinações da matriz de prioridade, os quatro prazos,
abertura normal, triagem, validação, rollback transacional, histórico, isolamento
da consulta e falha do notificador.

## Arquitetura

A solução usa **cliente-servidor**, **monólito modular**, **organização em camadas**
e **MVC na apresentação**. Os módulos executam no mesmo processo e compartilham um
banco relacional, mas mantêm responsabilidades explícitas:

- **app/chamados**: domínio, aplicação, apresentação e persistência de chamados;
- **app/catalogo**: usuários, categorias e equipes;
- **app/notificacoes**: contrato e implementação simulada de confirmação.

Não existe uma camada arquitetural chamada “Portas”. A interface **Notificador**
existe porque a dependência externa deve ser substituível.

## Documentação

| Documento | Conteúdo |
|---|---|
| [Requisitos](docs/requisitos.md) | Contexto, atores, 8 RFs, restrições e 3 ASRs. |
| [Modelo de domínio](docs/modelo-dominio.md) | Responsabilidades, relações, GRASP, coesão, acoplamento e SOLID. |
| [Prioridade e prazo](docs/prioridade-e-ciclo-de-vida.md) | Matriz, prazo inicial e estados considerados. |
| [Arquitetura](docs/arquitetura.md) | Componentes, dependências, comunicação, persistência e implantação. |
| [Trade-offs](docs/tradeoffs.md) | Comparação com monólito simples e microsserviços. |
| [Evolução](docs/evolucao.md) | Banco, notificação, aplicativo móvel, aumento de carga e implantação independente. |
| [Plano e testes](docs/plano-implementacao-e-testes.md) | Escopo implementado e rastreabilidade dos testes. |
| [Roteiro de defesa](docs/roteiro-defesa.md) | Sequência de apresentação e respostas concretas a perguntas prováveis. |

### ADRs

- [ADR-001 - Monólito modular em camadas](docs/adr/ADR-001.md)
- [ADR-002 - Persistência relacional transacional](docs/adr/ADR-002.md)
- [ADR-003 - Notificação síncrona substituível](docs/adr/ADR-003.md)

### UML

| Diagrama | Fonte PlantUML | Imagem renderizada |
|---|---|---|
| Classes | [classes.puml](docs/diagramas/classes.puml) | [classes.png](docs/diagramas/classes.png) |
| Sequência | [sequencia.puml](docs/diagramas/sequencia.puml) | [sequencia.png](docs/diagramas/sequencia.png) |
| Comunicação | [comunicacao.puml](docs/diagramas/comunicacao.puml) | [comunicacao.png](docs/diagramas/comunicacao.png) |
| Componentes | [componentes.puml](docs/diagramas/componentes.puml) | [componentes.png](docs/diagramas/componentes.png) |

## Limites conscientes do protótipo

- somente o solicitante abre o próprio chamado;
- autenticação real, assunção por técnico, interações e mudanças posteriores de
  estado estão modeladas como evolução, não implementadas;
- o prazo inicial usa horas corridas; calendário comercial, pausas e feriados são
  evolução;
- a notificação é simulada e mantida em memória;
- SQLite é adequado à demonstração local, não à implantação institucional.
