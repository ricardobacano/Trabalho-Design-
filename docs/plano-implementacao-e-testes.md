# Plano de implementação e testes

**Projeto:** Sistema de Gerenciamento de Chamados de Suporte Técnico
**Tema:** 16
**Status:** roteiro para executar o MVP
**Base:** `requisitos.md`, `prioridade-e-ciclo-de-vida.md`, `modelo-dominio.md` e `arquitetura.md`

## 1. Objetivo

Transformar os requisitos e diagramas em entregas pequenas que o grupo possa implementar, revisar e demonstrar. O plano prioriza um fluxo vertical completo: autenticar, abrir, encaminhar, atender e fechar um chamado.

## 2. Antes de começar a codificar

- [ ] Conferir se o Pull Request da documentação está completo e integrado em `develop`.
- [ ] Escolher e registrar linguagem, framework, banco e ferramenta de testes.
- [ ] Confirmar como os integrantes executarão o projeto no mesmo ambiente.
- [ ] Criar `src/` e a estrutura de testes adequada à stack.
- [ ] Definir dados de demonstração sem informações pessoais reais.

**Critério de saída:** todos conseguem clonar, executar e testar a aplicação localmente.

## 3. Marcos do MVP

### Marco 1 — Esqueleto executável

- Criar aplicação mínima que inicia localmente.
- Separar os módulos/camadas definidos em `arquitetura.md`.
- Configurar persistência escolhida e migração inicial, se aplicável.
- Documentar comandos de execução no README.

**Aceite:** qualquer integrante consegue iniciar a aplicação seguindo apenas o README.

### Marco 2 — Login, papéis e equipes

- Implementar login obrigatório para solicitante e equipe de suporte.
- Preparar contas de demonstração para os papéis solicitante, técnico e coordenador.
- Restringir cada usuário aos chamados e ações permitidos.
- Associar técnicos às equipes.

**Aceite:** solicitante não consulta chamados de outra conta; técnico acessa a fila da própria equipe; coordenador acessa triagem.

### Marco 3 — Abertura e encaminhamento

- Implementar abertura por solicitante autenticado.
- Implementar abertura por técnico em nome de um solicitante.
- Validar resumo, descrição, categoria, impacto e urgência.
- Obter equipe padrão pela categoria fixa.
- Encaminhar falta de categoria/equipe válida para triagem do coordenador.
- Calcular prioridade pela matriz.
- Criar prazos de SLA pelo calendário comercial.
- Registrar evento de criação e gerar notificação interna simulada.

**Aceite:** o chamado aparece na fila correta com prioridade, situação do SLA e histórico inicial.

### Marco 4 — Fila, assunção e interações

- Exibir chamados em fila para a equipe.
- Permitir que técnico autorizado assuma um chamado.
- Permitir comentários públicos e anotações internas.
- Aplicar permissões de visibilidade no servidor.
- Registrar assunção, comentários e mudanças no histórico.

**Aceite:** outro solicitante não vê comentários internos; o histórico identifica ator e horário de cada evento.

### Marco 5 — Atendimento, SLA e fechamento

- Implementar transições válidas de estado.
- Permitir espera por solicitante e por terceiro, com motivo.
- Pausar e retomar o relógio de resolução conforme a política.
- Exigir descrição de solução para resolver o chamado.
- Permitir ao solicitante fechar um chamado Resolvido.
- Permitir reabertura enquanto estiver Resolvido; não reabrir após Fechado no MVP.
- Exibir se os prazos de primeira resposta e resolução estão dentro ou fora do SLA.

**Aceite:** ações inválidas são recusadas, e cada mudança fica no histórico.

### Marco 6 — Revisão e demonstração

- Rodar todos os testes automatizados.
- Fazer revisão cruzada entre os três integrantes.
- Conferir README, documentos e diagramas.
- Preparar uma demonstração com abertura, triagem, atendimento, espera e resolução.
- Atualizar os diagramas se a implementação divergir das decisões.

## 4. Casos de teste prioritários

| ID | Cenário | Resultado esperado |
|---|---|---|
| T-01 | Acesso sem autenticação a uma função protegida | Acesso negado ou encaminhado ao login. |
| T-02 | Solicitante tenta consultar chamado de outra conta | Acesso negado. |
| T-03 | Técnico tenta assumir chamado de equipe à qual não pertence | Ação recusada, salvo reatribuição autorizada. |
| T-04 | Técnico abre chamado para outra pessoa | Solicitante e autor do registro ficam distintos. |
| T-05 | Categoria possui equipe padrão | Chamado entra na fila dessa equipe. |
| T-06 | Categoria/equipe não possui mapeamento válido | Chamado entra na fila de triagem do coordenador. |
| T-07 a T-15 | Cada uma das nove combinações da matriz de impacto e urgência | Prioridade corresponde à matriz aprovada. |
| T-16 | Usuário não autorizado tenta alterar prioridade manualmente | Alteração recusada. |
| T-17 | Coordenador altera prioridade sem justificativa | Alteração recusada. |
| T-18 | Interação interna é consultada por solicitante | Conteúdo interno não é retornado. |
| T-19 | Chamado é resolvido sem descrição da solução | Operação recusada. |
| T-20 | Chamado entra em Aguardando solicitante/terceiro | Relógio de resolução pausa. |
| T-21 | Atendimento é retomado | Relógio continua do tempo já consumido. |
| T-22 | SLA atravessa fim do expediente ou feriado configurado | Tempo fora do calendário não é contabilizado. |
| T-23 | Solicitante fecha chamado Resolvido | Estado passa para Fechado e evento é registrado. |
| T-24 | Tentativa de reabrir chamado Fechado | Operação recusada no MVP. |
| T-25 | Estado muda ou equipe/técnico é reatribuído | Evento de histórico guarda ator, instante e mudança. |
| T-26 | Notificação simulada falha ou não é exibida | Chamado e evento permanecem gravados. |

## 5. Níveis de teste

- **Unidade:** matriz de prioridade, transições de estado, cálculo do calendário comercial, permissões e validações.
- **Integração:** caso de uso com repositórios, persistência e registro de histórico.
- **Aceitação:** fluxo completo executado pela interface com os papéis de solicitante, técnico e coordenador.

A matriz de prioridade deve ter teste para cada combinação. Não basta testar somente um exemplo P1 e um exemplo P4.

## 6. Divisão sugerida entre três integrantes

| Integrante | Frente principal | Revisão cruzada |
|---|---|---|
| Pessoa 1 | Login, papéis, autorização e acesso às filas | Revisar testes de permissões da Pessoa 3 |
| Pessoa 2 | Regras de chamado, prioridade, SLA e transições | Revisar modelo de domínio e testes da Pessoa 1 |
| Pessoa 3 | Interface do fluxo, persistência, histórico e notificações simuladas | Revisar regras e cenários da Pessoa 2 |

A divisão depende da stack escolhida. As três pessoas devem compartilhar decisões de domínio e revisar pull requests; evitem deixar integração e testes com apenas um integrante.

## 7. Pull requests e commits

Criar branches curtas a partir de `develop`, por exemplo:

- `feature/login-e-papeis`
- `feature/abrir-chamado`
- `feature/triagem-e-assuncao`
- `feature/prioridade-sla`
- `feature/historico-interacoes`
- `test/ciclo-de-vida`

Exemplos de commits:

```text
feat(auth): adiciona login e controle por papel
feat(chamados): encaminha chamado pela categoria
feat(prioridade): calcula prioridade pela matriz
test(sla): cobre pausa durante espera por terceiro
docs(readme): documenta execução local
```

Cada Pull Request deve descrever o requisito atendido, resumir a mudança e informar os testes executados.

## 8. Decisão necessária para iniciar o Marco 1

A stack ainda não foi informada. Antes de criar a estrutura real do código, o grupo precisa registrar:

- linguagem e versão;
- framework de interface/backend;
- banco de dados;
- ferramenta de testes;
- forma de execução local.

Depois dessa escolha, atualizar `arquitetura.md` e registrar a decisão em um ADR, se ela afetar dependências ou implantação.
