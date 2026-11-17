# Requisitos e ASRs

## 1. Contexto

A plataforma organiza solicitações de suporte técnico de TI. O problema central é
evitar chamados dispersos e sem prioridade, destino ou histórico. O sistema deve
registrar a solicitação, calcular sua prioridade, encaminhá-la e permitir o
acompanhamento do atendimento.

O protótipo implementa uma pequena fatia vertical: abertura e consulta de chamados
pelo solicitante. A solução completa poderá incluir assunção por técnico,
interações e demais transições de estado.

Na abertura demonstrada, o solicitante informa categoria, impacto e urgência; a
aplicação calcula a prioridade e associa a equipe padrão da categoria, se houver.
O suporte não revisa nem reclassifica o chamado nessa fatia.

## 2. Atores

| Ator | Responsabilidade |
|---|---|
| Solicitante | Abre o próprio chamado e consulta seus chamados. |
| Técnico | Futuramente consulta a fila da equipe, assume e atualiza chamados. |
| Coordenador | Futuramente trata a triagem e corrige encaminhamentos. |
| Serviço de notificação | Recebe a confirmação da abertura; no protótipo é simulado. |

No protótipo, o técnico **não abre chamado em nome do solicitante**. Essa
possibilidade foi excluída para manter a fatia pequena e evitar um segundo fluxo de
autorização e auditoria.

Não existe login no protótipo: qualquer visitante da instância atua como o mesmo
solicitante de demonstração configurado. O filtro por identificador na consulta
não representa autorização entre pessoas reais.

## 3. Requisitos funcionais

| ID | Requisito | Protótipo |
|---|---|---|
| RF-01 | O solicitante deve abrir um chamado informando resumo, descrição, categoria, impacto e urgência. | Implementado |
| RF-02 | O sistema deve calcular a prioridade inicial pela combinação de impacto e urgência. | Implementado |
| RF-03 | O sistema deve associar a equipe padrão da categoria e iniciar o chamado em **EM_FILA**; sem equipe, deve iniciá-lo em **EM_TRIAGEM**. | Implementado |
| RF-04 | O sistema deve registrar a criação do chamado em seu histórico. | Implementado |
| RF-05 | O solicitante deve consultar a lista e os detalhes dos próprios chamados. | Implementado |
| RF-06 | O sistema deve calcular e exibir um prazo inicial de atendimento conforme a prioridade. | Implementado |
| RF-07 | Um técnico deve poder assumir chamados da equipe e alterar o estado para Em atendimento. | Evolução |
| RF-08 | Técnicos e solicitantes devem registrar interações visíveis conforme o seu papel. | Evolução |

Em RF-03, associar uma equipe não implica que um técnico tenha recebido ou assumido
o chamado. Em RF-05, “próprios chamados” são os do usuário fixo de demonstração;
não há identificação individual de cada visitante.

## 4. Restrições

- **R-01:** o trabalho é um protótipo acadêmico e não uma reprodução integral do GLPI.
- **R-02:** a aplicação deve ser executável localmente em um único processo.
- **R-03:** o protótipo usa Python, Flask, SQLAlchemy, SQLite e páginas HTML
  renderizadas no servidor.
- **R-04:** login completo, cadastro público, recuperação de senha, interface
  sofisticada e implantação em nuvem estão fora do escopo.
- **R-05:** a categoria é obrigatória. A triagem ocorre quando a categoria existe,
  mas não possui equipe padrão configurada.
- **R-06:** o prazo do protótipo é calculado em horas corridas. Calendário comercial,
  feriados e pausas são evolução.
- **R-07:** somente chamados do usuário de demonstração podem ser retornados pela
  consulta usada no protótipo; visitantes distintos compartilham esse usuário.

## 5. Requisitos arquiteturalmente significativos

### ASR-01 - Consistência e rastreabilidade da abertura

Ao abrir um chamado, o chamado e o evento inicial de histórico devem ser gravados
na mesma transação. Se qualquer uma dessas gravações falhar, nenhuma deve ser
confirmada.

**Influência arquitetural:** exige que chamado e histórico permaneçam na mesma
fronteira transacional. No protótipo, isso é realizado em um banco relacional
compartilhado e uma transação local. Esse requisito, isoladamente, não obriga que
todo o sistema seja um monólito.

### ASR-02 - Substituição da notificação

Deve ser possível substituir o **NotificadorFake** por outra implementação que
preserve o contrato **ConfirmacaoAbertura**, sem modificar as regras de prioridade,
prazo ou persistência do chamado. Se o novo canal exigir dados de contato que não
existem no protótipo, como telefone ou preferência de canal, o catálogo e a montagem
da confirmação no serviço também precisarão evoluir.

**Influência arquitetural:** exige uma interface estável de notificação e composição
da implementação no início da aplicação. A falha da notificação não pode desfazer
um chamado já persistido.

### ASR-03 - Modificação da política de prioridade

Se a combinação entre impacto, urgência e prioridade mudar, a alteração deve ficar
restrita à **MatrizPrioridade** e aos seus testes. Rotas, templates e persistência
não devem conter cópias da matriz.

Esse escopo considera mudanças nas combinações entre os níveis já existentes.
Criar um novo nível de prioridade também afetaria **Prioridade**,
**PoliticaPrazo**, seus testes e possivelmente a apresentação.

**Influência arquitetural:** exige isolar a política em um elemento coeso do
domínio, evitando condicionais duplicadas em outras camadas.

A prioridade e o prazo calculados ficam gravados em cada chamado. Alterar a matriz
afeta novas aberturas, não recalcula os registros antigos. O protótipo não grava
uma versão formal da matriz utilizada em cada chamado.

## 6. Critérios de aceite da fatia vertical

1. Uma abertura válida cria chamado e evento de histórico.
2. As nove combinações da matriz retornam a prioridade documentada.
3. Categoria com equipe gera estado **EM_FILA** e registra o destino.
4. Categoria sem equipe gera estado **EM_TRIAGEM**.
5. Campo obrigatório ausente impede a gravação.
6. A consulta de um solicitante não retorna chamados de outro.
7. A confirmação é registrada pelo **NotificadorFake**.
8. Falha da notificação não remove o chamado já persistido.
