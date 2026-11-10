# Prioridade, SLA e ciclo de vida do chamado


**Observação:** a matriz e os tempos abaixo são uma política inicial do projeto, inspirada em práticas de gestão de serviços. Não são apresentados como valores obrigatórios do ITIL.

## 1. Objetivo

Este documento define uma regra reproduzível para calcular prioridade, acompanhar os prazos de SLA do MVP e controlar as transições de estado dos chamados.

A prioridade representa a ordem de atendimento resultante do impacto e da urgência. SLA e estado são conceitos relacionados, mas diferentes: o estado descreve em que etapa está o atendimento; o SLA descreve se os prazos acordados estão sendo cumpridos.

## 2. Escalas de impacto e urgência

### 2.1 Impacto

| Nível | Nome | Critério para triagem |
|---:|---|---|
| 3 | Alto | Serviço essencial indisponível ou vários usuários/uma área inteira afetados, sem alternativa adequada. |
| 2 | Médio | Um grupo pequeno ou uma função importante afetada; existe alternativa parcial ou o impacto é limitado. |
| 1 | Baixo | Um usuário ou função não essencial afetada; há alternativa aceitável e o trabalho pode continuar. |

### 2.2 Urgência

| Nível | Nome | Critério para triagem |
|---:|---|---|
| 3 | Alta | A ação precisa começar imediatamente para evitar paralisação ou agravamento relevante. |
| 2 | Média | O atendimento deve começar em breve; existe alguma alternativa temporária. |
| 1 | Baixa | O atendimento pode ser programado sem impacto relevante no curto prazo. |

O solicitante pode fornecer informações que ajudem a classificar impacto e urgência. O técnico pode corrigir a classificação durante a triagem, registrando o motivo quando a alteração mudar a prioridade.

## 3. Matriz de prioridade proposta

| Impacto \ Urgência | 3 — Alta | 2 — Média | 1 — Baixa |
|---|---|---|---|
| **3 — Alto** | **P1 — Crítica** | **P2 — Alta** | **P3 — Média** |
| **2 — Médio** | **P2 — Alta** | **P3 — Média** | **P4 — Baixa** |
| **1 — Baixo** | **P3 — Média** | **P4 — Baixa** | **P4 — Baixa** |

### 3.1 Interpretação

- **P1 — Crítica:** impacto alto e urgência alta. A equipe deve iniciar a resposta antes dos demais níveis.
- **P2 — Alta:** impacto ou urgência elevados, mas sem a combinação máxima.
- **P3 — Média:** impacto/urgência moderados ou isolados.
- **P4 — Baixa:** impacto e urgência baixos ou com alternativa aceitável.

O sistema deve calcular a prioridade inicial automaticamente. O cálculo deve ficar numa regra de domínio isolada, para que a matriz possa ser alterada sem reescrever telas ou persistência.

### 3.2 Exemplo de aplicação

- Um serviço usado por toda a equipe está indisponível e não há alternativa: impacto 3, urgência 3 → P1.
- Um usuário não consegue usar uma função importante, mas consegue concluir a atividade por outro caminho: impacto 1 ou 2 e urgência 2 → P3 ou P4, conforme o impacto confirmado.
- Uma solicitação de melhoria sem bloqueio operacional: impacto 1, urgência 1 → P4.

Os exemplos devem ser adaptados às categorias e ao cenário apresentados pelo grupo.

## 4. Alteração manual da prioridade

A prioridade manual deve ser excepcional e auditável:

1. O sistema calcula a prioridade com a matriz.
2. Um técnico pode corrigir impacto ou urgência durante a triagem, e o sistema recalcula.
3. Um coordenador ou perfil autorizado pode substituir diretamente a prioridade quando houver justificativa operacional.
4. A alteração deve guardar prioridade anterior, prioridade nova, responsável, data/hora e justificativa.
5. O histórico deve deixar claro se a prioridade veio do cálculo ou de ajuste autorizado.

## 5. SLA do MVP

### 5.1 Relógios acompanhados

- **Prazo de primeira resposta:** tempo até a primeira interação de atendimento registrada por um técnico.
- **Prazo de resolução:** tempo até o chamado alcançar o estado Resolvido.

Uma mensagem automática de recebimento confirma a abertura, mas não conta como primeira resposta de um técnico.

### 5.2 Metas iniciais propostas

Os tempos abaixo são valores didáticos para o protótipo. O grupo deve validá-los com o enunciado e pode alterá-los antes de implementar.

| Prioridade | Primeira resposta | Resolução |
|---|---:|---:|
| P1 — Crítica | 15 minutos úteis | 4 horas úteis |
| P2 — Alta | 1 hora útil | 8 horas úteis |
| P3 — Média | 4 horas úteis | 2 dias úteis |
| P4 — Baixa | 1 dia útil | 5 dias úteis |

### 5.3 Calendário comercial e pausas

O MVP adotará um calendário comercial explícito:

- **Dias de atendimento:** segunda a sexta-feira.
- **Horário:** das 08:00 às 18:00.
- **Fuso horário:** `America/Sao_Paulo`.
- **Feriados:** o calendário deve permitir cadastrar feriados sem expediente. Para a demonstração, usar uma lista de feriados configurada no sistema; feriados locais e institucionais aplicáveis devem ser acrescentados pelo grupo.
- **Contagem:** todos os prazos de SLA contam somente dentro do horário comercial, inclusive P1 e P2. Tempo fora do expediente não consome o prazo.
- **Aguardando solicitante:** pausa o relógio de resolução até a resposta ou retomada registrada.
- **Aguardando terceiro:** também pausa o relógio de resolução até a dependência ser atendida ou o atendimento ser retomado.
- **Primeira resposta:** é registrada uma única vez quando um técnico faz a primeira interação de atendimento; uma mensagem automática não conta.

O sistema deve manter a duração já consumida antes de uma pausa e continuar a contagem quando o chamado voltar ao atendimento. Se a implementação de feriados for simplificada, o comportamento simplificado deve ser identificado no protótipo e coberto por testes.

### 5.4 Estados de SLA

O sistema deve apresentar para cada prazo um destes resultados:

- **Dentro do prazo:** ainda não atingiu o limite.
- **Em risco:** atingiu o limite de alerta configurado, se esse alerta for implementado.
- **Estourado:** ultrapassou o prazo.
- **Pausado:** relógio suspenso por uma espera definida na política.
- **Concluído:** evento correspondente ocorreu dentro ou fora do prazo; registrar o resultado final.

O aviso de risco pode ser simplificado ou omitido no MVP. A medição e a indicação de prazo devem permanecer coerentes.

## 6. Estados do chamado

| Estado | Significado |
|---|---|
| **Em fila** | Chamado registrado e encaminhado para uma equipe ou fila de triagem; ainda sem técnico responsável. |
| **Em atendimento** | Um técnico assumiu o chamado e está trabalhando nele. |
| **Aguardando solicitante** | A equipe precisa de informação ou ação do solicitante para continuar. |
| **Aguardando terceiro** | A equipe depende de fornecedor ou área externa para prosseguir. |
| **Resolvido** | A equipe registrou uma solução e aguarda confirmação ou encerramento. |
| **Fechado** | Atendimento encerrado; estado final normal. |
| **Cancelado** | Chamado encerrado sem solução, por duplicidade, retirada ou invalidação justificada. |

## 7. Transições permitidas

| Estado atual | Próximo estado permitido | Quem pode executar | Condições |
|---|---|---|---|
| Em fila | Em atendimento | Técnico da equipe | O técnico assume o chamado; fica registrado como responsável. |
| Em fila | Cancelado | Coordenador ou perfil autorizado | Motivo obrigatório. |
| Em atendimento | Aguardando solicitante | Técnico responsável | Deve informar o que precisa do solicitante. |
| Em atendimento | Aguardando terceiro | Técnico responsável | Deve registrar a dependência externa. |
| Em atendimento | Resolvido | Técnico responsável | Descrição da solução obrigatória. |
| Aguardando solicitante | Em atendimento | Técnico responsável ou técnico da equipe | O solicitante respondeu ou a equipe retomou o trabalho; registrar a retomada. |
| Aguardando terceiro | Em atendimento | Técnico responsável ou técnico da equipe | A dependência foi atendida ou a equipe retomou o trabalho; registrar a retomada e reativar o relógio de resolução. |
| Resolvido | Fechado | Solicitante | O solicitante pode fechar diretamente após avaliar a solução. |
| Resolvido | Em atendimento | Solicitante solicita reabertura ou técnico autorizado reabre | Motivo obrigatório; retoma o atendimento e registra o evento. |
| Qualquer estado não final | Cancelado | Coordenador ou perfil autorizado | Motivo obrigatório. |

Estados finais: **Fechado** e **Cancelado**. Para reduzir o escopo do MVP, a reabertura de um chamado Fechado fica fora da primeira versão; se for necessária, deve ser uma decisão explícita e uma transição adicional documentada.

## 8. Regras de transição

- **RC-01:** todo chamado começa em Em fila depois de passar pela validação e pelo encaminhamento inicial.
- **RC-02:** um chamado Em fila pertence a uma equipe ou à fila de triagem.
- **RC-03:** somente um técnico autorizado pode assumir um chamado e iniciar Em atendimento.
- **RC-04:** um técnico não pode colocar um chamado em Resolvido sem registrar a solução.
- **RC-05:** ao entrar em Aguardando solicitante ou Aguardando terceiro, a causa da espera deve ser registrada.
- **RC-06:** ao voltar de uma espera para Em atendimento, a retomada deve ser registrada no histórico.
- **RC-07:** cancelamento exige justificativa e não equivale a resolução.
- **RC-08:** cada transição registra estado anterior, estado novo, ator e instante.
- **RC-09:** notificações internas simuladas podem ser exibidas após transições relevantes, mas o histórico é a fonte de auditoria.
- **RC-10:** transição não listada na tabela deve ser recusada pelo sistema.

## 9. Notificações relacionadas ao ciclo

No MVP, usar notificação interna ou simulada para:

- confirmação de abertura ao solicitante;
- aviso de novo chamado à equipe;
- aviso ao solicitante quando a equipe pedir informação;
- aviso ao solicitante quando o chamado for resolvido;
- confirmação de fechamento ou reabertura;
- alerta de SLA próximo do vencimento, se esse recurso estiver implementado.

A notificação deve ser produzida a partir de um evento registrado. Falha no envio não deve impedir a gravação da mudança de estado.

## 10. Casos de teste derivados

- [ ] Todas as nove combinações de impacto e urgência retornam a prioridade indicada na matriz.
- [ ] Um chamado sem impacto ou urgência não pode ser enviado para a fila.
- [ ] Um técnico fora da equipe não consegue assumir o chamado sem reatribuição autorizada.
- [ ] Não é possível resolver chamado sem descrição da solução.
- [ ] Entrar em Aguardando solicitante exige uma pergunta ou ação esperada.
- [ ] Entrar em Aguardando terceiro exige a identificação da dependência.
- [ ] Uma transição não listada é recusada e não altera o histórico.
- [ ] A alteração manual de prioridade exige permissão e justificativa.
- [ ] A mudança de status é registrada com ator, data/hora, estado anterior e novo.
- [ ] Pausa e retomada do SLA seguem o calendário comercial e a política para espera pelo solicitante e por terceiro.
- [ ] Fechamento e cancelamento são distinguidos no estado e no histórico.

## 11. Decisões registradas

As escolhas do grupo foram incorporadas. Os valores de prazo aceitos são:

- [x] Matriz de impacto × urgência aceita.
- [x] Tempos iniciais de resposta e resolução aceitos.
- [x] Usar a matriz e os tempos de SLA apresentados neste documento.
- [x] Usar calendário comercial de segunda a sexta, das 08:00 às 18:00, no fuso `America/Sao_Paulo`; feriados sem expediente serão configurados.
- [x] Pausar o relógio de resolução em Aguardando solicitante e Aguardando terceiro.
- [x] Permitir que o solicitante feche diretamente um chamado Resolvido.
- [x] Não permitir reabertura após Fechado no MVP; a solicitação de reabertura ocorre enquanto o chamado está Resolvido.
- [x] Exibir situação e prazos do SLA. Alertas automáticos de vencimento são opcionais e podem ser omitidos se aumentarem demais a complexidade.

## 12. Referência de uso

A matriz e o processo descritos aqui são decisões de projeto do grupo, inspiradas em práticas de gestão de serviços. O documento deve ser alinhado com o enunciado da disciplina e atualizado junto com requisitos, arquitetura, diagramas e testes sempre que uma regra mudar.
