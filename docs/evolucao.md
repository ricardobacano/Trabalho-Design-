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
