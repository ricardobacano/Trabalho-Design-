# Arquitetura proposta

**Projeto:** Sistema de Gerenciamento de Chamados de Suporte Técnico
**Tema:** 16
**Status:** proposta para revisão do grupo
**Decisão relacionada:** [ADR-001 — Arquitetura da aplicação](adr/ADR-001-arquitetura.md)

## 1. Objetivo

Definir uma estrutura que permita implementar e testar o fluxo de chamados com responsabilidades separadas. A proposta usa um **monólito modular organizado em camadas**: uma aplicação implantável, dividida em módulos de domínio e com dependências controladas.

O GLPI é referência de domínio e processo. Esta proposta descreve a arquitetura do projeto acadêmico e não presume como o GLPI é implementado internamente.

## 2. Contexto e premissas

- O grupo desenvolverá uma única aplicação para o MVP.
- O fluxo principal envolve solicitantes autenticados, técnicos, equipes, categorias, chamados, SLA e histórico.
- O volume e a necessidade de implantação são compatíveis com uma aplicação única.
- Os limites entre módulos ainda podem mudar conforme o domínio for detalhado.
- Notificações externas reais estão fora do MVP; notificações internas serão simuladas.
- Banco de dados, linguagem e framework ainda serão escolhidos pelo grupo.

## 3. Visão em camadas

1. **Apresentação:** interface web, controladores e validação de entrada. Converte requisições em comandos de aplicação e apresenta resultados.
2. **Aplicação:** casos de uso, autorização e coordenação das operações. Exemplos: abrir chamado, assumir chamado, comentar, resolver, fechar e reabrir.
3. **Domínio:** entidades e regras que não dependem de interface nem de tecnologia. Inclui transições de estado, prioridade, visibilidade de interação e cálculo de SLA.
4. **Infraestrutura:** implementações concretas de persistência, autenticação, calendário e notificações internas.

### Regra de dependência

A apresentação chama casos de uso. Casos de uso dependem de contratos definidos para persistência e notificações. O domínio não depende de banco, framework web ou provedor de e-mail. A infraestrutura implementa os contratos usados pela aplicação.

## 4. Módulos de domínio sugeridos

| Módulo | Responsabilidade | Principais conceitos |
|---|---|---|
| **Identidade e acesso** | Login, papéis, associação entre técnico e equipe e autorização. | Usuário, Papel, MembroEquipe |
| **Atendimento** | Abrir, encaminhar, assumir, comentar, resolver, fechar e cancelar chamados. | Chamado, Interação, EventoHistorico |
| **Catálogo e equipes** | Categorias e mapeamento fixo categoria → equipe no MVP; fila de triagem. | Categoria, Equipe |
| **Prioridade e SLA** | Calcular prioridade e prazos com calendário comercial, incluindo pausas. | MatrizPrioridade, PoliticaSLA, AcompanhamentoSLA |
| **Notificações** | Gerar notificações internas simuladas a partir de eventos de atendimento. | Notificacao |

Esses módulos podem ser pacotes da mesma aplicação; não são serviços separados nem exigem implantação independente.

## 5. Fluxo arquitetural: abertura de chamado

1. Um solicitante autenticado envia resumo, descrição, categoria, impacto e urgência.
2. A camada de apresentação encaminha a solicitação ao caso de uso de abertura.
3. O caso de uso verifica a permissão e valida os dados.
4. O módulo de catálogo obtém a equipe padrão da categoria. Sem correspondência, o chamado vai à fila de triagem do coordenador.
5. A política de prioridade calcula a prioridade.
6. A política de SLA cria os prazos conforme prioridade e calendário comercial.
7. O caso de uso persiste chamado e evento de histórico pelas interfaces de repositório.
8. Uma notificação interna simulada é gerada para a equipe/coordenador e o solicitante recebe a confirmação na aplicação.

O diagrama está em [`diagramas/sequencia.puml`](diagramas/sequencia.puml).

## 6. Contratos e infraestrutura

A camada de aplicação deve consumir abstrações como:

- repositório de chamados;
- repositório de categorias/equipes;
- repositório de interações e eventos, caso não façam parte do agregado de Chamado;
- serviço de autenticação/autorização;
- política de prioridade e política de SLA;
- serviço de notificações internas;
- relógio/calendário comercial, para tornar testes de prazo determinísticos.

A escolha de banco deve ser feita depois de confirmar a linguagem e o ambiente de execução. O diagrama de componentes em [`diagramas/componentes.puml`](diagramas/componentes.puml) mostra as dependências lógicas sem impor tecnologia.

## 7. Segurança e autorização

- Todas as ações protegidas exigem usuário autenticado.
- O solicitante consulta apenas chamados associados à sua conta.
- Técnicos consultam a fila das equipes às quais pertencem.
- Coordenadores podem tratar a fila de triagem e reatribuir chamados.
- Anotações internas não são retornadas ao solicitante.
- Senhas, se armazenadas localmente, devem ser persistidas com hash seguro; nunca em texto puro.
- A autorização deve ocorrer na aplicação/servidor, não apenas ocultando opções na interface.

## 8. Qualidades arquiteturais priorizadas

| Qualidade | Escolha que ajuda |
|---|---|
| **Manutenibilidade** | Casos de uso, regras de domínio e infraestrutura separados. |
| **Testabilidade** | Regras de prioridade e transição testadas sem interface ou banco real. |
| **Segurança** | Permissões verificadas nos casos de uso e visibilidade aplicada no servidor. |
| **Consistência** | Chamado, histórico e prazos gravados na mesma operação lógica quando possível. |
| **Simplicidade de implantação** | Um artefato da aplicação e uma base de dados para o MVP. |

## 9. Implantação do MVP

A implantação lógica contém uma aplicação e um banco de dados. Não são necessários microserviços, broker de mensagens ou integração de e-mail para demonstrar os requisitos atuais. A infraestrutura concreta depende da stack que o grupo escolher.

## 10. Diagramas relacionados

- [Modelo de classes](diagramas/classes.puml)
- [Sequência de abertura](diagramas/sequencia.puml)
- [Comunicação da abertura](diagramas/comunicacao.puml)
- [Componentes](diagramas/componentes.puml)

## 11. Decisões pendentes

- [ ] Escolher linguagem e framework.
- [ ] Escolher banco de dados e estratégia de migração.
- [ ] Definir se a autenticação local será feita pela própria aplicação ou por biblioteca/serviço externo.
- [ ] Confirmar limites dos módulos após revisar os diagramas.
- [ ] Definir como feriados serão cadastrados no calendário comercial do MVP.

Não escolher tecnologia antes de verificar os requisitos do curso, o conhecimento disponível no grupo e o tempo de entrega.
