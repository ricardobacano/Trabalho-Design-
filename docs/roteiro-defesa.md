# Roteiro objetivo para a defesa

## 1. Problema e recorte

A plataforma organiza chamados de suporte que hoje poderiam ficar sem prioridade,
destino ou histórico. O sistema completo prevê solicitantes, técnicos e
coordenadores. O protótipo comprova a fatia de **abrir e consultar chamados do
usuário de demonstração**; assunção por técnico e interações são evoluções
documentadas. Não há login: todos os visitantes da instância atuam como o mesmo
usuário demo, e o filtro da consulta não equivale a autorização entre pessoas.

## 2. Três ASRs

1. **Consistência:** chamado e evento inicial são confirmados juntos ou sofrem
   rollback juntos.
2. **Notificação substituível:** o fake pode ser trocado por outra implementação do
   mesmo contrato sem alterar prioridade, prazo ou persistência. Um canal que exija
   novos dados de contato também exige evolução do catálogo e da montagem da
   confirmação no serviço.
3. **Modificabilidade da prioridade:** a matriz muda em um único componente do
   domínio e em seus testes quando são alteradas combinações entre os níveis já
   existentes. Um novo nível de prioridade afetaria também prazo e demais usos do
   enum.

## 3. Arquitetura escolhida

Foi escolhido **cliente-servidor + monólito modular + camadas + MVC na
apresentação**. O ASR-01 mantém chamado e histórico na mesma fronteira
transacional; os ASRs 02 e 03 justificam separar integração e políticas internas.
O monólito foi escolhido também porque não existem requisitos de implantação ou
escala independentes, equipes autônomas ou isolamento por processo.

Não foi adotada Arquitetura Hexagonal nem uma camada genérica de portas. A
interface **Notificador** existe porque o enunciado exige uma dependência externa
substituível e há uma variação concreta nesse ponto.

Também não foi adotado microkernel: chamados, catálogo e notificações são partes
fixas do fluxo, e não plugins opcionais com instalação e ciclo de vida próprios.

## 4. Duas decisões para justificar

### Monólito modular em vez de microsserviços

- **Problema:** entregar uma fatia coerente com transação entre chamado e histórico.
- **Decisão:** módulos no mesmo processo e banco.
- **Ganho:** transação, teste, execução e implantação simples.
- **Custo:** os módulos escalam e são implantados juntos.
- **Por que não microsserviços:** não existe requisito de escala independente,
  equipes autônomas ou implantação separada que pague rede, falhas parciais,
  observabilidade e múltiplas implantações. Microsserviços ainda poderiam manter
  chamado e histórico no mesmo serviço; o ASR-01 não os proíbe por si só.

### Camadas em vez de Hexagonal ou microkernel

- **Por que não Hexagonal:** há uma apresentação e uma persistência concreta. Portas
  para todos os repositórios e adaptadores adicionais não atenderiam uma variação
  atual. A aplicação inclusive depende de repositórios SQLAlchemy concretos.
- **Por que existe uma interface:** `Notificador` protege somente o ponto em que há
  substituição externa prevista; uma interface isolada não torna a arquitetura
  hexagonal.
- **Por que não microkernel:** não existem plugins opcionais, descoberta dinâmica ou
  versionamento de extensões. A matriz é uma política de domínio, não um plugin.
- **Trade-off das camadas:** menos abstrações e montagem mais simples; em troca, a
  troca da persistência exigiria alterar os repositórios concretos.

### Notificação síncrona e substituível

- **Problema:** demonstrar integração sem depender de credenciais ou provedor real.
- **Decisão:** `Notificador` com `NotificadorFake`, chamado depois do commit.
- **Ganho:** troca de tecnologia e testes simples; falha não apaga o chamado.
- **Custo:** com um provedor real, a chamada pode aumentar a latência e não há
  repetição automática.
- **Quando mudar:** se entrega confiável se tornar ASR, avaliar fila e processamento
  assíncrono.

## 5. Demonstração sugerida

1. Abrir um chamado de **Software**, impacto alto e urgência média.
2. Mostrar prioridade **P2_ALTA**, prazo de 8 horas e destino **Service Desk**.
3. Abrir outro chamado em **Outros - requer triagem**.
4. Mostrar estado **EM_TRIAGEM** e o evento inicial no histórico.
5. Abrir a lista do usuário de demonstração. Explicar que o filtro por
   solicitante é verificado no teste automatizado da lista, sem alegar
   autenticação ou isolamento de visitantes reais.
6. Executar `pytest` e destacar os 21 testes, especialmente matriz, rollback,
   isolamento da consulta e falha de notificação.

## 6. Perguntas prováveis

**O técnico pode abrir chamado em nome do usuário?**
Não no protótipo. Essa inclusão exigiria definir autorização, identificação do
solicitante representado e auditoria de quem realizou a ação. Ela foi mantida como
evolução para não criar um segundo fluxo na fatia escolhida.

**O suporte classifica o chamado? O que significa encaminhar à equipe?**
O solicitante informa categoria, impacto e urgência. A prioridade é calculada pela
matriz; a equipe da categoria é associada ao chamado em **EM_FILA**. O suporte ainda
não possui tela para revisar a classificação, receber ou assumir a solicitação.

**Pessoas diferentes conseguem ver apenas seus próprios chamados?**
Ainda não. Qualquer navegador acessa o usuário fixo de demonstração. As consultas
filtram por esse identificador e não retornam registros de outros IDs, mas não há
login nem autorização individual. Isso exigiria autenticação em uma evolução.

**Por que SQLite?**
Porque a entrega é local, em processo único, e precisa demonstrar persistência e
transação com baixo custo. Para uso institucional, a evolução proposta é
PostgreSQL, migração de esquema, backup e testes de integração.

**A matriz de prioridade foi copiada do ITIL?**
Não. A matriz e os prazos são políticas didáticas declaradas do protótipo. Elas
estão isoladas justamente para poderem ser substituídas pela política real da
instituição.

**A matriz é versionada? Uma mudança altera chamados antigos?**
O chamado guarda prioridade e prazo calculados na abertura, portanto uma mudança
na matriz afeta novas aberturas e não recalcula os registros existentes. O banco
não guarda uma versão formal da matriz aplicada a cada chamado.

**O que acontece se o notificador falhar?**
O chamado e o histórico já foram confirmados. A falha gera um aviso e não executa
rollback. O custo é não haver repetição automática nesta versão.

Na demonstração, o **NotificadorFake** apenas registra a confirmação em memória. Uma
implementação de produção poderia enviar e-mail ou outra mensagem preservando o
contrato, mas exigiria credenciais, configuração e testes de integração.

**O que muda se houver aplicativo móvel?**
A camada de apresentação ganha uma API HTTP e o aplicativo passa a consumi-la. O
domínio, a matriz, o prazo e a persistência podem permanecer; autenticação e formato
das respostas precisam ser projetados.

## 7. Mudanças de cenário do enunciado

### Substituição do serviço de e-mail

Criar outra implementação de **Notificador** e alterar sua composição. Se o canal
usar o e-mail existente, abertura, prioridade e banco de chamados permanecem. Se
exigir telefone ou preferência de canal, catálogo e montagem da confirmação também
mudam.

### Aumento significativo de carga

Medir primeiro os gargalos. Os candidatos iniciais são servidor de desenvolvimento,
SQLite e notificação síncrona. A evolução provável inclui servidor WSGI, PostgreSQL,
índices, testes de carga e observabilidade. O monólito pode ter várias instâncias,
mas seus módulos continuam escalando juntos.

### Troca do mecanismo de persistência

SQLAlchemy e a concentração das consultas nos repositórios reduzem os pontos de
alteração. Ainda seria necessário trocar driver e configuração, criar migrações e
reexecutar testes de integração. Não é apenas mudar a URL de conexão.

### Implantação independente de uma funcionalidade

Notificações é a candidata mais simples porque não precisa retirar chamado e
histórico da mesma transação. Seriam necessários contrato de rede, autenticação,
tratamento de indisponibilidade e observabilidade. Entrega garantida exigiria
persistir a intenção e processá-la posteriormente, por exemplo com outbox e fila.

## 8. Cadeias para ensaiar na defesa

Para cada ASR, seguir a mesma ordem: requisito, decisão registrada, ponto do código,
teste e custo aceito. Abrir esses arquivos durante o estudo ajuda a relacionar a
explicação à implementação real.

| Cadeia | Explicação concreta | Evidência e consequência |
|---|---|---|
| RF-04 → ASR-01 → ADR-002 | A abertura cria um chamado e um evento inicial inseparáveis. | `ChamadoRepositorySQLAlchemy.salvar_novo` faz `flush`, inclui o evento e confirma um único `commit`; `test_falha_ao_gravar_historico_desfaz_todo_o_commit` mostra o rollback. A transação é simples porque ambos permanecem no mesmo banco. |
| RF-01 → ASR-02 → ADR-003 | Após gravar o chamado, o serviço pede confirmação pela interface `Notificador`. | `AbrirChamadoService.executar` recebe a implementação na inicialização e trata sua falha; `test_falha_de_notificacao_nao_desfaz_chamado` comprova a permanência do chamado. O custo é a chamada síncrona sem repetição automática. |
| RF-02 → ASR-03 → ADR-001 | `Chamado.abrir` usa `MatrizPrioridade` para as combinações existentes de impacto e urgência. | `test_matriz_de_prioridade` cobre nove casos. A política fica isolada, mas não há versionamento formal; novos níveis exigiriam alterar enum e `PoliticaPrazo`. |

No ensaio, abrir um chamado e mostrar no detalhe prioridade, prazo, equipe e evento.
Em seguida, apontar o método de persistência e executar os testes. Não descrever
uma simulação de erro como recurso visível na interface: o rollback e a falha da
notificação são demonstrados pelos testes automatizados.
