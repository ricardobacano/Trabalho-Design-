# Análise de evolução

## 1. SQLite para PostgreSQL

### Elementos afetados

- configuração da conexão;
- dependência do driver;
- criação e migração do esquema;
- ajustes SQL específicos, caso sejam introduzidos;
- testes de integração do repositório;
- estratégia de implantação e backup.

### Elementos que permanecem

- rotas e templates;
- **AbrirChamadoService**;
- **Chamado**, **MatrizPrioridade** e **PoliticaPrazo**;
- contrato **Notificador**;
- fluxo de abertura e critérios de prioridade.

### Decisões que ajudam ou dificultam

O uso do SQLAlchemy e a concentração das consultas nos repositórios reduzem os
pontos de alteração. O uso direto de modelos SQLAlchemy ainda mantém acoplamento ao
ORM, mas evita que SQL apareça na aplicação e na apresentação. O banco compartilhado
facilita a transação, mas exige migração coordenada de todo o monólito.

## 2. NotificadorFake para e-mail ou WhatsApp

### Elementos afetados

- nova classe que implemente **Notificador**;
- configuração de credenciais e endpoint;
- dados de contato e preferência de canal, caso a nova integração não utilize o
  e-mail já disponível;
- composição da implementação na inicialização;
- testes de integração e tratamento de indisponibilidade.

### Elementos que permanecem

- formulário e consulta;
- regra de prioridade e prazo;
- **Chamado** e **EventoHistorico**;
- repositório e esquema do banco;
- regras internas de **Chamado**, prioridade, prazo e persistência.

### Decisões que ajudam ou dificultam

A interface pequena aplica Protected Variations, DIP e ISP. Uma implementação que
aceite o mesmo contrato pode ser trocada na composição. Se o canal exigir telefone
ou preferência de contato, o catálogo e a montagem da confirmação também mudam;
a interface não cria dados ausentes. A comunicação síncrona é simples, mas um
provedor lento aumenta o tempo de resposta. Como o chamado é confirmado antes da
notificação, a indisponibilidade externa não desfaz o registro. Se a confiabilidade
da entrega se tornar um ASR, será necessário avaliar fila e processamento
assíncrono, aceitando consistência eventual e maior operação.

## 3. Inclusão de aplicativo móvel

### Elementos afetados

- nova apresentação móvel e uma API HTTP para receber e devolver dados;
- identificação e autorização do solicitante, hoje fixado na configuração da
  demonstração;
- validação e respostas HTTP em formato adequado ao novo cliente;
- testes das rotas da API e do isolamento entre solicitantes.

### Elementos que permanecem

- **Chamado**, **MatrizPrioridade**, **PoliticaPrazo** e regras de abertura;
- serviços de aplicação e repositórios, desde que recebam o solicitante
  identificado pela nova apresentação;
- transação local entre chamado e histórico.

### Decisões que ajudam ou dificultam

A separação entre apresentação e aplicação permite reutilizar o caso de uso.
Entretanto, as rotas atuais foram feitas para formulários e templates Jinja, e o
usuário de demonstração é fixo. A API exigiria autenticação e autorização reais;
não basta expor as rotas atuais ao aplicativo. Duas apresentações também aumentam
o trabalho de versionar contratos e testar os fluxos nos dois clientes.

## 4. Aumento significativo de carga

### Elementos afetados

- servidor de execução e configuração de implantação; o servidor de
  desenvolvimento Flask não atende a uma implantação institucional;
- SQLite, conexões, índices e consultas, após medir o padrão real de leitura e
  escrita; PostgreSQL é uma alternativa para maior concorrência;
- testes de carga e observabilidade para localizar gargalos;
- latência do provedor de notificação, caso uma integração real substitua o fake.

### Elementos que permanecem

- a matriz de prioridade e as regras de criação do chamado;
- as fronteiras entre módulos e a transação local entre chamado e histórico,
  enquanto ambos permanecerem no mesmo banco.

### Decisões que ajudam ou dificultam

O monólito modular pode ter mais instâncias atendendo requisições com um banco
compartilhado, mas módulos continuam escalando juntos. A migração de SQLite e o
ajuste das consultas devem ser guiados por medidas, não apenas pelo aumento
hipotético de usuários. O **NotificadorFake** guarda confirmações em memória de
cada processo e não serviria como registro compartilhado entre instâncias. Uma
integração síncrona lenta pode elevar o tempo de resposta, motivando rever a
ADR-003 se baixa latência ou entrega confiável se tornarem ASRs.

## 5. Implantação independente de uma funcionalidade

### Exemplo: extrair notificações

- A aplicação manteria o contrato **Notificador**, com uma implementação que
  chamasse o serviço de notificações por HTTP ou publicasse uma mensagem.
- Seriam necessários contrato de rede, configuração, autenticação entre serviços,
  tratamento de indisponibilidade e observabilidade.
- Com uma chamada síncrona após o commit, uma falha ainda deixa o chamado gravado,
  mas não há repetição automática. Se a entrega garantida for exigida, uma
  intenção de notificar gravada na transação e processada depois (outbox) poderia
  evitar a perda entre o commit e o envio; mensagens repetidas exigiriam
  processamento idempotente.

### Limite da separação

A extração de notificações não precisa separar chamado e histórico, então o
ASR-01 pode continuar com uma transação local no módulo de chamados. Separar
chamado e histórico em bancos distintos, por outro lado, perderia essa
atomicidade e exigiria rever o ASR-01 e a ADR-002. Implantação independente só
se justifica diante de uma necessidade concreta que compense contratos,
monitoramento, falhas parciais e operação adicionais.
