# Modelo de domínio e responsabilidades

## 1. Conceitos principais

| Conceito | Responsabilidade |
|---|---|
| **Usuario** | Representar o solicitante identificado no contexto da demonstração. |
| **Categoria** | Classificar o chamado e informar a equipe padrão, quando configurada. |
| **Equipe** | Representar o grupo responsável pela fila de atendimento. |
| **Chamado** | Manter dados da solicitação e proteger as regras de sua criação. |
| **EventoHistorico** | Registrar um fato auditável ocorrido com o chamado. |
| **MatrizPrioridade** | Calcular a prioridade a partir de impacto e urgência. |
| **PoliticaPrazo** | Calcular o prazo inicial conforme a prioridade. |
| **AbrirChamadoService** | Coordenar o caso de uso sem executar regras internas das entidades. |
| **ConsultarChamadosService** | Coordenar lista e detalhe sempre limitados ao solicitante informado. |
| **UsuarioRepositorySQLAlchemy** | Recuperar os dados do solicitante usados pela aplicação e pela apresentação. |
| **ChamadoRepositorySQLAlchemy** | Persistir chamado e histórico na mesma transação e realizar consultas. |
| **Notificador** | Definir o contrato mínimo para confirmação da abertura. |
| **NotificadorFake** | Simular a dependência externa durante demonstração e testes. |

## 2. Relações

- Um usuário pode abrir vários chamados; cada chamado possui um solicitante.
- Uma categoria pode possuir zero ou uma equipe padrão.
- Cada chamado possui exatamente uma categoria.
- Um chamado pode possuir uma equipe; quando não possui, fica na triagem.
- Um chamado possui um ou mais eventos de histórico ao longo de sua vida.
- A matriz calcula uma prioridade para cada combinação válida de impacto e urgência.

## 3. Distribuição de responsabilidades

### Abertura

O **AbrirChamadoService** recebe o evento do sistema, consulta o solicitante e a
categoria pelos repositórios, pede que **Chamado** seja criado, solicita a
persistência e aciona o notificador. Ele não consulta campos internos do chamado
para decidir suas regras.

**Chamado.abrir** valida resumo e descrição, solicita o cálculo da prioridade e
define o estado inicial:

- **EM_FILA**, quando existe equipe;
- **EM_TRIAGEM**, quando a categoria não possui equipe.

O repositório grava o chamado e o evento inicial na mesma transação.

### Consulta

O **ConsultarChamadosService** recebe o identificador do solicitante e pede ao
repositório a lista ou o detalhe aplicando esse filtro. A apresentação recebe
somente o resultado permitido para aquele usuário.

## 4. GRASP

| Princípio | Aplicação |
|---|---|
| Controller | **AbrirChamadoService** coordena o caso de uso de abertura. |
| Information Expert | **Chamado** conhece os dados necessários para validar sua criação e definir seu estado inicial. |
| Creator | **Chamado.abrir** cria uma instância válida; **EventoHistorico.abertura** cria o evento correspondente. |
| High Cohesion | Prioridade, prazo, persistência e notificação possuem elementos separados. |
| Low Coupling | O caso de uso depende do contrato **Notificador**, não de e-mail ou WhatsApp. |
| Polymorphism | **NotificadorFake** pode ser substituído por outra implementação de **Notificador**. |
| Protected Variations | A interface **Notificador** protege o fluxo contra mudanças no mecanismo externo. |
| Pure Fabrication | O repositório concentra persistência sem atribuí-la à entidade de domínio. |

## 5. Coesão e acoplamento

- A matriz contém somente regras de prioridade.
- O chamado contém regras relacionadas à própria criação e estado.
- O serviço de aplicação apenas coordena colaboradores.
- A apresentação conhece formulários e HTTP, mas não contém a matriz.
- SQLAlchemy permanece nos elementos de persistência.
- A notificação conhece somente os dados mínimos da confirmação.

O principal acoplamento deliberado é o uso de SQLAlchemy nos repositórios concretos.
Esse custo foi aceito para um protótipo pequeno e está documentado na ADR-002.

## 6. SOLID pertinente

- **SRP:** abertura, prioridade, persistência e notificação têm razões diferentes
  para mudar.
- **OCP:** um novo notificador pode ser adicionado sem modificar o caso de uso.
- **LSP:** toda implementação de **Notificador** deve aceitar a mesma confirmação e
  não alterar o significado do contrato.
- **ISP:** **Notificador** possui apenas a operação utilizada pela abertura.
- **DIP:** o serviço recebe a abstração **Notificador**; a implementação fake é
  escolhida na criação da aplicação.

Não foram criadas interfaces para todos os repositórios. Essa abstração não era
necessária para cumprir a fatia e aumentaria o código sem uma variação concreta.
