# Requisitos, escopo e regras de negócio

**Projeto:** Sistema de Gerenciamento de Chamados de Suporte Técnico
**Tema:** 16
**Status:** versão revisada com as decisões já informadas pelo grupo

## 1. Objetivo

Construir um sistema acadêmico de suporte técnico que permita registrar solicitações, encaminhá-las a uma equipe, acompanhar o atendimento e manter o histórico das ações. O fluxo toma o GLPI como referência de domínio e aplica práticas de gestão de serviços inspiradas em ITIL, sem pretender reproduzir integralmente esses produtos ou processos.

## 2. Problema que o sistema resolve

Solicitações de suporte podem chegar por diferentes meios e ficar sem responsável, prioridade ou histórico claro. O sistema deve reunir os chamados em uma fila de equipe, indicar sua prioridade com critérios consistentes e permitir que um técnico assuma e conduza cada atendimento até a resolução.

## 3. Escopo do MVP

### 3.1 Incluído

- Abertura de chamado por solicitante autenticado.
- Registro de chamado por técnico autenticado em nome de um solicitante.
- Identificação do solicitante por conta do sistema, com nome e e-mail associados.
- Registro de resumo, descrição e categoria do problema.
- Seleção de impacto e urgência e cálculo automático da prioridade.
- Encaminhamento do chamado para uma equipe responsável.
- Exibição do chamado na fila da equipe até que um técnico o assuma.
- Atribuição do atendimento a um técnico da equipe.
- Atualização de status e registro de comentários/interações.
- Histórico de alterações importantes, incluindo responsável, equipe, prioridade e status.
- Resolução, fechamento e cancelamento de chamados conforme as regras deste documento.
- Acompanhamento de prazo de primeira resposta e de resolução por prioridade, conforme a proposta de SLA do documento de prioridade.
- Notificações internas simuladas para eventos relevantes, exibidas dentro da aplicação.

### 3.2 Fora do escopo do MVP

- Inventário e descoberta automática de equipamentos.
- Gestão de mudanças, problemas e configurações (CMDB).
- Chat em tempo real ou telefonia.
- Envio real de e-mail, SMS, WhatsApp ou integração com sistemas externos.
- Base de conhecimento completa e sugestão automática de soluções.
- Regras de automação configuráveis pelo administrador.
- Gestão de múltiplas organizações ou contratos.
- Relatórios gerenciais avançados e análises preditivas.
- Autenticação federada ou integração com diretório institucional.
- Aplicativo móvel nativo.

Esses itens podem aparecer como evolução futura, mas não devem ser necessários para demonstrar o fluxo central.

## 4. Atores e permissões

| Ator | Responsabilidades e permissões no MVP |
|---|---|
| Solicitante | Entrar com sua conta, abrir chamado, consultar os próprios chamados, acrescentar informações quando solicitado, acompanhar atualizações, fechar um chamado resolvido ou pedir reabertura antes do fechamento. |
| Técnico | Entrar com sua conta, registrar chamado em nome de alguém, consultar a fila da equipe, assumir chamados, publicar comentário visível ou anotação interna, alterar estados permitidos e registrar a resolução. |
| Coordenador de suporte | Administrar equipes e categorias, corrigir encaminhamento, reatribuir chamados e ajustar prioridade com justificativa. Pode ser representado por um perfil técnico com permissão ampliada no protótipo. |

### 4.1 Autenticação e autorização

Todo solicitante e técnico deve entrar no sistema com uma conta. O MVP pode usar contas previamente cadastradas e autenticação local simples; cadastro público, recuperação de senha e login federado ficam fora do escopo inicial. O sistema deve autorizar as ações pelo papel do usuário e impedir que um solicitante consulte chamados de outras contas. Um técnico pode registrar chamado em nome de um solicitante existente.

## 5. Requisitos funcionais

| ID | Requisito |
|---|---|
| RF-01 | O sistema deve permitir que um solicitante autenticado registre um chamado com resumo, descrição e categoria, associando-o à sua conta. |
| RF-02 | O sistema deve permitir que um técnico registre um chamado em nome de um solicitante, identificando quem realizou o registro e quem precisa do suporte. |
| RF-03 | O sistema deve validar os campos obrigatórios e rejeitar chamados sem informações mínimas para triagem. |
| RF-04 | O sistema deve solicitar impacto e urgência e calcular a prioridade conforme a matriz aprovada pelo grupo. |
| RF-05 | O sistema deve encaminhar o chamado para a equipe associada à categoria. Quando não houver associação válida, o chamado deve ficar disponível para triagem do coordenador. |
| RF-06 | O sistema deve manter o chamado na fila da equipe até que um técnico o assuma. |
| RF-07 | O sistema deve permitir que um técnico da equipe assuma um chamado ainda sem técnico responsável. |
| RF-08 | O sistema deve permitir comentários visíveis ao solicitante e anotações internas da equipe, identificando claramente a visibilidade de cada interação. |
| RF-09 | O sistema deve permitir mudanças de estado somente quando forem válidas para o estado atual e para o papel do ator. |
| RF-10 | O sistema deve registrar no histórico a criação do chamado e as mudanças de estado, equipe, técnico responsável, prioridade e resolução. |
| RF-11 | O sistema deve restringir a consulta: solicitantes autenticados veem seus próprios chamados; técnicos veem chamados das equipes às quais pertencem; coordenadores podem consultar a fila de triagem e administrar encaminhamentos. |
| RF-12 | O sistema deve permitir resolver um chamado com descrição da solução e registrar o responsável e o horário da resolução. |
| RF-13 | O sistema deve permitir ao solicitante fechar diretamente um chamado resolvido ou solicitar sua reabertura enquanto ainda estiver Resolvido. Chamados Fechados não são reabertos no MVP. |
| RF-14 | O sistema deve exibir o prazo ou a situação do SLA de primeira resposta e de resolução. |
| RF-15 | O sistema deve exibir notificações internas simuladas sobre criação, atribuição, solicitação de informação, resolução e reabertura. Envio real por e-mail fica fora do MVP. |

## 6. Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF-01 | O sistema deve separar apresentação, casos de uso, regras de domínio e infraestrutura, conforme a arquitetura escolhida pelo grupo. |
| RNF-02 | As regras de prioridade e de transição de estado devem ser verificáveis sem depender de interação visual com a interface. |
| RNF-03 | Ações que alteram o chamado devem deixar registro de auditoria com ator, data/hora, tipo de alteração e valores relevantes. |
| RNF-04 | O sistema deve autenticar usuários e impedir acesso a chamados e ações fora do escopo de permissão do ator. |
| RNF-05 | Mensagens de validação devem indicar ao usuário o que precisa ser corrigido sem expor detalhes técnicos internos. |
| RNF-06 | O projeto deve incluir instruções reproduzíveis de instalação e execução no README. |
| RNF-07 | O MVP deve ter testes automatizados para cálculo de prioridade, transições de estado e regras centrais de abertura e atribuição. |

## 7. Regras de negócio

- **RN-01 — Identificação do solicitante:** todo chamado deve estar associado a uma pessoa que necessita do suporte, mesmo quando um técnico registra o chamado.
- **RN-02 — Registro do autor:** o sistema deve diferenciar o solicitante do usuário que efetivamente cadastrou o chamado.
- **RN-03 — Equipe antes do técnico:** um chamado pode ser encaminhado para uma equipe sem possuir técnico individual responsável.
- **RN-04 — Compatibilidade da assunção:** apenas um técnico pertencente à equipe responsável pode assumir o chamado, salvo reatribuição explícita por coordenador.
- **RN-05 — Categoria e equipe:** no MVP, cada categoria possui um mapeamento fixo para uma equipe padrão. Se a categoria estiver ausente ou sem equipe configurada, o chamado vai para a fila de triagem do coordenador.
- **RN-06 — Prioridade calculada:** a prioridade inicial deve ser calculada a partir de impacto e urgência pela matriz aprovada.
- **RN-07 — Alteração manual de prioridade:** somente coordenador ou perfil autorizado pode substituir a prioridade calculada; deve informar justificativa, e o sistema deve registrar valor anterior, novo valor, autor e data/hora.
- **RN-08 — Histórico preservado:** comentários e eventos de auditoria não devem ser apagados como se nunca tivessem ocorrido. Correções devem gerar novo registro.
- **RN-09 — Resolução documentada:** um chamado só pode ser marcado como resolvido se houver uma descrição da solução ou do resultado do atendimento.
- **RN-10 — Cancelamento justificado:** cancelamento deve indicar motivo, como duplicidade, solicitação retirada ou registro inválido.
- **RN-11 — Relógios de SLA:** os relógios e suas pausas devem seguir a política documentada no arquivo de prioridade e ciclo de vida.
- **RN-12 — Notificações não substituem histórico:** a notificação interna simulada não substitui o evento registrado no chamado.
- **RN-13 — Autenticação:** solicitantes e técnicos devem estar autenticados para acessar as funções correspondentes ao seu papel.
- **RN-14 — Visibilidade das interações:** comentários públicos ficam visíveis ao solicitante e à equipe; anotações internas ficam visíveis somente a técnicos e coordenadores.
- **RN-15 — Triagem:** chamados sem categoria válida ou sem equipe mapeada são encaminhados à fila do coordenador de suporte.

## 8. Dados mínimos do chamado

| Campo | Obrigatório? | Observação |
|---|---:|---|
| Identificador | Sim | Gerado pelo sistema. |
| Solicitante | Sim | Conta autenticada com nome e e-mail cadastrados. |
| Autor do registro | Sim | Solicitante ou técnico que abriu em nome dele. |
| Resumo | Sim | Frase curta que identifica o problema. |
| Descrição | Sim | Contexto suficiente para iniciar a triagem. |
| Categoria | Sim | Determina a equipe padrão, se houver mapeamento. |
| Impacto | Sim | Entrada da matriz de prioridade. |
| Urgência | Sim | Entrada da matriz de prioridade. |
| Prioridade | Sim | Calculada pela matriz; ajuste manual requer justificativa. |
| Equipe responsável | Sim, após triagem | Pode iniciar como “triagem” quando não houver correspondência. |
| Técnico responsável | Não | Preenchido quando um técnico assume o atendimento. |
| Estado | Sim | Controlado pelo ciclo de vida. |
| Histórico | Sim | Eventos e interações relevantes. |
| Datas | Sim | Criação, primeira resposta, atualização, resolução e fechamento, conforme ocorram. |

## 9. Critérios de aceite do fluxo principal

O fluxo principal estará demonstrável quando:

1. Um solicitante ou técnico conseguir registrar um chamado válido.
2. O sistema identificar solicitante e autor do registro separadamente.
3. O sistema calcular prioridade com base em impacto e urgência.
4. O chamado aparecer na fila da equipe correta ou na fila de triagem.
5. Um técnico autorizado conseguir assumir o chamado.
6. O técnico conseguir registrar interação e avançar o estado de forma válida.
7. O sistema exigir uma solução antes de marcar o chamado como resolvido.
8. O histórico mostrar quem fez cada mudança e quando.
9. O solicitante conseguir acompanhar o resultado e confirmar ou pedir reabertura conforme as regras.
10. Os prazos de SLA exibidos corresponderem à política configurada.

## 10. Decisões adotadas pelo grupo

As escolhas recebidas do grupo foram incorporadas como regras do MVP:

- **Login:** obrigatório para solicitantes e técnicos; contas podem ser previamente cadastradas.
- **Categoria → equipe:** mapeamento fixo no MVP.
- **Triagem:** chamados sem categoria/equipe válida ficam na fila do coordenador.
- **Comentários:** haverá interações públicas para o solicitante e anotações internas para a equipe.
- **SLA:** usa calendário comercial definido no documento complementar; espera por terceiro pausa o relógio de resolução.
- **Fechamento:** o solicitante pode fechar diretamente um chamado resolvido.
- **Reabertura:** permitida enquanto o chamado estiver Resolvido; chamados Fechados não serão reabertos no MVP.
- **Notificações:** serão simuladas dentro da aplicação no MVP; envio real por e-mail fica como evolução futura.

## 11. Limites e evolução

## 11. Limites e evolução

A prioridade do grupo é demonstrar o ciclo completo do chamado com regras consistentes. Funcionalidades fora do MVP podem ser citadas em evolução futura, mas não devem atrasar a entrega dos requisitos centrais. Toda mudança de escopo deve ser refletida nos requisitos, nos diagramas, nos testes e no README.
