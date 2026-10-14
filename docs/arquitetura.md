# Arquitetura

## 1. Modelo de domínio e responsabilidades

O sistema organiza chamados de suporte técnico. Um chamado pode ser aberto pelo
próprio solicitante ou por um técnico em nome de outra pessoa. Cada chamado é
encaminhado a uma equipe; um técnico dessa equipe pode assumir o atendimento.

### 1.1 Conceitos e responsabilidades

- **Chamado:** mantém título, descrição, categoria, impacto, urgência, prioridade,
  estado, solicitante, registrador, equipe responsável, técnico responsável e datas.
  Também valida mudanças permitidas de estado.
- **Usuário:** representa uma pessoa que participa do atendimento. Conforme sua
  atuação, pode ser solicitante, registrador, técnico ou coordenador. O registrador
  e o solicitante podem ser pessoas diferentes.
- **Equipe:** reúne técnicos e recebe chamados para atendimento.
- **Interação:** registra comentário ou atualização feita durante o atendimento,
  com autor e data.
- **Registro de histórico:** registra mudanças relevantes do chamado, como estado,
  equipe ou técnico responsável, incluindo autor e data.
- **Regra de prioridade:** determina a prioridade a partir do impacto e da urgência,
  de acordo com a matriz definida pelo grupo.

### 1.2 Regras iniciais do domínio

1. Um chamado deve ter um solicitante e um registrador.
2. Um chamado encaminhado deve ter uma equipe responsável.
3. O técnico responsável pode permanecer vazio até alguém da equipe assumir o chamado.
4. A prioridade é determinada pela combinação de impacto e urgência.
5. Mudanças de estado, equipe e técnico responsável devem ser registradas no histórico.
6. Uma interação deve estar associada a um chamado e a um autor.

### 1.3 Responsabilidades e princípios de design

- **GRASP — Information Expert:** o chamado valida as próprias mudanças de estado,
  pois conhece seu estado atual e seu histórico.
- **Alta coesão:** prioridade, histórico e interações têm responsabilidades distintas,
  em vez de concentrar todas as regras em uma única classe.
- **Baixo acoplamento:** o chamado não envia notificações diretamente nem conhece
  detalhes do banco de dados.
- **SOLID — SRP:** a regra de prioridade e o envio de notificações ficam separados
  das responsabilidades centrais do chamado.
- **SOLID — DIP:** a aplicação depende de interfaces para persistência e notificação;
  as implementações concretas ficam na infraestrutura.
