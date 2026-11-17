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
   domínio e em seus testes.

## 3. Arquitetura escolhida

Foi escolhido **cliente-servidor + monólito modular + camadas + MVC na
apresentação**. Essa combinação mantém a transação local do ASR-01 e separa regras,
HTTP, persistência e integração sem o custo operacional de microsserviços.

Não foi adotada Arquitetura Hexagonal nem uma camada genérica de portas. A
interface **Notificador** existe porque o enunciado exige uma dependência externa
substituível e há uma variação concreta nesse ponto.

## 4. Duas decisões para justificar

### Monólito modular em vez de microsserviços

- **Problema:** entregar uma fatia coerente com transação entre chamado e histórico.
- **Decisão:** módulos no mesmo processo e banco.
- **Ganho:** transação, teste, execução e implantação simples.
- **Custo:** os módulos escalam e são implantados juntos.
- **Por que não microsserviços:** não existe requisito de escala independente,
  equipes autônomas ou implantação separada que pague a complexidade distribuída.

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
6. Executar `pytest` e destacar os 19 testes, especialmente matriz, rollback e
   falha de notificação.

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

**O que muda se houver aplicativo móvel?**
A camada de apresentação ganha uma API HTTP e o aplicativo passa a consumi-la. O
domínio, a matriz, o prazo e a persistência podem permanecer; autenticação e formato
das respostas precisam ser projetados.
