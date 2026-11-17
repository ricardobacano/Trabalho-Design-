# Requisitos e ASRs

## 1. Contexto

A plataforma organiza solicitações de suporte técnico de TI. O problema central é
evitar chamados dispersos e sem prioridade, destino ou histórico. O sistema deve
registrar a solicitação, calcular sua prioridade, encaminhá-la e permitir o
acompanhamento do atendimento.

O protótipo implementa uma pequena fatia vertical: abertura e consulta de chamados
pelo solicitante. A solução completa poderá incluir assunção por técnico,
interações e demais transições de estado.

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

## 3. Requisitos funcionais

| ID | Requisito | Protótipo |
|---|---|---|
| RF-01 | O solicitante deve abrir um chamado informando resumo, descrição, categoria, impacto e urgência. | Implementado |
| RF-02 | O sistema deve calcular a prioridade inicial pela combinação de impacto e urgência. | Implementado |
| RF-03 | O sistema deve encaminhar o chamado à equipe da categoria; sem equipe configurada, deve encaminhá-lo à triagem. | Implementado |
| RF-04 | O sistema deve registrar a criação do chamado em seu histórico. | Implementado |
| RF-05 | O solicitante deve consultar a lista e os detalhes dos próprios chamados. | Implementado |
| RF-06 | O sistema deve calcular e exibir um prazo inicial de atendimento conforme a prioridade. | Implementado |
| RF-07 | Um técnico deve poder assumir chamados da equipe e alterar o estado para Em atendimento. | Evolução |
| RF-08 | Técnicos e solicitantes devem registrar interações visíveis conforme o seu papel. | Evolução |

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
  consulta usada no protótipo.

## 5. Requisitos arquiteturalmente significativos

### ASR-01 - Consistência e rastreabilidade da abertura

Ao abrir um chamado, o chamado e o evento inicial de histórico devem ser gravados
na mesma transação. Se qualquer uma dessas gravações falhar, nenhuma deve ser
confirmada.

**Influência arquitetural:** exige persistência transacional compartilhada entre
chamado e histórico. Favorece banco relacional e monólito com transação local.

### ASR-02 - Substituição da notificação

Deve ser possível substituir o **NotificadorFake** por outra implementação que
preserve o contrato **ConfirmacaoAbertura**, sem modificar as regras de prioridade,
prazo ou persistência do chamado. Se o novo canal exigir dados de contato que não
existem no protótipo, como telefone ou preferência de canal, catálogo e composição
também precisarão evoluir.

**Influência arquitetural:** exige uma interface estável de notificação e composição
da implementação no início da aplicação. A falha da notificação não pode desfazer
um chamado já persistido.

### ASR-03 - Modificação da política de prioridade

Se a combinação entre impacto, urgência e prioridade mudar, a alteração deve ficar
restrita à **MatrizPrioridade** e aos seus testes. Rotas, templates e persistência
não devem conter cópias da matriz.

**Influência arquitetural:** exige isolar a política em um elemento coeso do
domínio, evitando condicionais duplicadas em outras camadas.

## 6. Critérios de aceite da fatia vertical

1. Uma abertura válida cria chamado e evento de histórico.
2. As nove combinações da matriz retornam a prioridade documentada.
3. Categoria com equipe gera estado **EM_FILA** e registra o destino.
4. Categoria sem equipe gera estado **EM_TRIAGEM**.
5. Campo obrigatório ausente impede a gravação.
6. A consulta de um solicitante não retorna chamados de outro.
7. A confirmação é enviada ao **NotificadorFake**.
8. Falha da notificação não remove o chamado já persistido.
