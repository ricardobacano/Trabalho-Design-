# Requisitos

## 1. Contexto

O sistema organiza o atendimento técnico de TI por meio de chamados. Um chamado
pode ser registrado pelo próprio solicitante ou por um técnico em nome de outra
pessoa. Ao ser registrado, ele é encaminhado a uma equipe responsável; depois,
um técnico dessa equipe pode assumir o atendimento.

O sistema considera práticas de gestão de serviços inspiradas em ITIL, como
classificação, prioridade baseada em impacto e urgência, acompanhamento do estado
e registro do histórico. O GLPI é usado como referência de domínio, não como
modelo obrigatório da arquitetura.

## 2. Atores

- **Solicitante:** pessoa que precisa do suporte e acompanha o chamado.
- **Registrador:** pessoa que cria o chamado; pode ser o solicitante ou um técnico.
- **Técnico:** integrante de uma equipe que pode assumir e atender chamados.
- **Coordenador:** organiza a fila, define prioridades e encaminha chamados.
- **Serviço de notificação:** dependência externa que envia avisos sobre o chamado.

## 3. Requisitos funcionais

- **RF01:** O solicitante ou um técnico pode registrar um chamado.
- **RF02:** O sistema deve registrar quem abriu o chamado e quem é o solicitante.
- **RF03:** O chamado deve ser encaminhado a uma equipe responsável.
- **RF04:** Um técnico da equipe responsável pode assumir o chamado.
- **RF05:** O coordenador pode classificar o chamado e definir seu impacto e urgência.
- **RF06:** O sistema deve determinar a prioridade usando a matriz definida pelo grupo.
- **RF07:** O técnico pode atualizar o estado e registrar interações no chamado.
- **RF08:** O solicitante pode consultar o estado e o histórico de seus chamados.
- **RF09:** Técnicos e coordenadores podem consultar chamados por estado, prioridade
  ou equipe.

## 4. Restrições e escopo

- O sistema será um protótipo acadêmico, não uma implementação completa do GLPI.
- O protótipo deve persistir os dados dos chamados.
- A integração de notificação pode ser simulada, mas deve poder ser substituída.
- A fatia funcional inicial deve incluir abertura de chamado, consulta, persistência
  e pelo menos um fluxo alternativo.

## 5. Requisitos arquiteturalmente significativos (ASRs)

- **ASR01 — Rastreabilidade:** cada alteração de estado e cada mudança de equipe
  ou técnico responsável deve registrar autor, data e valores anterior e novo.
- **ASR02 — Alteração da priorização:** a matriz de prioridade deve poder ser
  ajustada sem reescrever o fluxo de abertura e atendimento do chamado.
- **ASR03 — Substituição da notificação:** deve ser possível trocar a implementação
  de notificação sem alterar as regras de atendimento.

## 6. Questões a confirmar

- Quais categorias de chamado o protótipo terá?
- A prioridade será calculada automaticamente ou poderá ser ajustada pelo
  coordenador?
- Quais estados serão implementados na fatia funcional?
