# Modelo de domínio — Sistema de Chamados

**Tema:** 16
**Status:** primeira versão para revisão do grupo
**Referências:** `requisitos.md` e `prioridade-e-ciclo-de-vida.md`

## 1. Objetivo do modelo

Este modelo descreve os principais conceitos do sistema e as relações entre eles. Ele deve orientar os diagramas UML e a implementação, sem decidir detalhes de framework, banco de dados ou interface.

O cenário central é: uma pessoa autenticada abre um chamado ou um técnico o registra em nome dela; o chamado é encaminhado a uma equipe; um técnico da equipe assume o atendimento; interações, mudanças e prazos ficam registrados até o fechamento.

## 2. Conceitos do domínio

| Conceito | Responsabilidade | Dados principais |
|---|---|---|
| **Usuário** | Representa uma pessoa autenticada que pode ser solicitante, técnico ou coordenador conforme seus papéis. | identificador, nome, e-mail, situação, papéis |
| **Equipe** | Agrupa técnicos e recebe chamados para atendimento. | identificador, nome, situação |
| **Membro de equipe** | Registra a participação de um usuário técnico em uma equipe. | equipe, usuário, situação |
| **Categoria** | Classifica a solicitação e define a equipe padrão no MVP. | identificador, nome, descrição, equipe padrão opcional |
| **Chamado** | Mantém solicitação, prioridade, estado, solicitante, autor do registro e responsáveis. | identificador, resumo, descrição, categoria, impacto, urgência, prioridade, estado, datas |
| **Interação** | Registra comentário público ou anotação interna. | conteúdo, visibilidade, autor, data/hora |
| **Evento de histórico** | Registra uma mudança relevante de forma auditável. | tipo, ator, data/hora, valores anteriores e novos |
| **Política de SLA** | Define metas de primeira resposta e resolução por prioridade, conforme o calendário comercial. | prioridade, metas, calendário |
| **Acompanhamento de SLA** | Controla prazos, pausas e resultado dos relógios de um chamado. | prazo inicial, prazo de resolução, tempo consumido, situação |
| **Matriz de prioridade** | Calcula a prioridade a partir de impacto e urgência. | regra de combinação |

## 3. Relações e cardinalidades

- Um usuário pode solicitar vários chamados; cada chamado possui um solicitante.
- Um usuário pode registrar vários chamados; cada chamado possui um autor do registro. O autor pode ser o próprio solicitante ou um técnico.
- Um chamado pode estar encaminhado para uma equipe; antes da triagem, essa equipe pode estar indefinida e o chamado fica na fila do coordenador.
- Uma categoria tem, no MVP, zero ou uma equipe padrão. Uma equipe pode atender várias categorias.
- Uma equipe possui vários membros; um técnico pode participar de mais de uma equipe.
- Um chamado pode ter zero ou um técnico responsável individual. O técnico deve pertencer à equipe responsável, exceto quando o coordenador fizer uma reatribuição.
- Um chamado contém zero ou mais interações e eventos de histórico.
- Cada interação e cada evento de histórico têm um autor/ator.
- Cada chamado possui um acompanhamento de SLA e uma prioridade resultante da matriz.

## 4. Regras que o modelo precisa preservar

1. Solicitante, autor do registro e técnico responsável são papéis diferentes no chamado, mesmo quando duas dessas funções pertencem à mesma pessoa.
2. A categoria direciona o chamado à equipe padrão. Sem categoria ou equipe configurada, o chamado fica na fila de triagem do coordenador.
3. O chamado pode estar atribuído a uma equipe antes de ser assumido por um técnico.
4. Comentários públicos são visíveis ao solicitante e à equipe; anotações internas são visíveis apenas à equipe e aos coordenadores.
5. Interações e eventos de histórico são registros distintos: comentário descreve comunicação; evento registra mudança de estado, prioridade, equipe ou responsável.
6. A prioridade inicial é calculada por impacto e urgência; ajustes autorizados exigem justificativa e histórico.
7. O relógio de resolução do SLA pausa em Aguardando solicitante e Aguardando terceiro, seguindo o calendário comercial acordado.
8. O chamado Resolvido pode ser fechado pelo solicitante; chamados Fechados não são reabertos no MVP.

## 5. Estados representados

O atributo `estado` do chamado usa os valores definidos em `prioridade-e-ciclo-de-vida.md`:

- Em fila
- Em atendimento
- Aguardando solicitante
- Aguardando terceiro
- Resolvido
- Fechado
- Cancelado

As transições permitidas ficam no diagrama de estados do chamado, que será produzido na próxima etapa. O diagrama de classes não substitui essa especificação.

## 6. Responsabilidades e limites

### Chamado

Mantém os dados e o estado atual da solicitação. Deve proteger invariantes, como exigir descrição da solução para resolver e impedir transições inválidas. Não deve enviar e-mail nem conhecer detalhes do banco.

### Matriz de prioridade

Recebe impacto e urgência e retorna a prioridade. A regra deve ser isolada para ser testada sem interface ou banco.

### Acompanhamento de SLA

Controla primeira resposta, prazo de resolução e pausas. O cálculo considera o calendário comercial: segunda a sexta, 08:00–18:00, fuso `America/Sao_Paulo`, com feriados configurados.

### Equipe e categoria

A categoria aponta para uma equipe padrão no MVP. Coordenador trata casos sem encaminhamento válido.

### Interação e evento de histórico

A interação registra conteúdo e visibilidade. Evento de histórico registra alteração do sistema e não deve ser apagado para ocultar uma ação anterior.

## 7. Conceitos deliberadamente fora do modelo inicial

Para manter o MVP controlado, este modelo não inclui ativos de TI, contratos, base de conhecimento, catálogo de serviços, fornecedores integrados, automação de regras ou múltiplas organizações. Se algum deles virar requisito, deve ser incluído por uma mudança explícita no escopo.

## 8. Arquivo UML associado

O diagrama inicial está em [`classes.puml`](diagramas/classes.puml). Ele mostra entidades, enumerações, dependências e cardinalidades principais.

Antes de implementar, o grupo deve revisar se as relações refletem os requisitos e se a professora espera outro nível de detalhe no diagrama.
