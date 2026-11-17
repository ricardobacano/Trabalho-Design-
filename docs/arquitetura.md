# Arquitetura da solução

## 1. Visão geral

A solução combina:

- **cliente-servidor**: navegador acessa a aplicação Flask por HTTP;
- **monólito modular**: catálogo, chamados e notificações são módulos do mesmo
  processo e da mesma implantação;
- **organização em camadas**: apresentação, aplicação, domínio e infraestrutura;
- **MVC na apresentação**: rotas controlam requisições, modelos fornecem dados e
  templates Jinja renderizam as páginas.

Não há uma camada denominada “Portas”. A interface **Notificador** é um contrato
específico exigido pela variação da integração externa, e não uma adoção de
Arquitetura Hexagonal.

## 2. Módulos

| Módulo | Responsabilidade | Código |
|---|---|---|
| Chamados | Abertura, prioridade, prazo, histórico, consulta e regras do chamado. | **app/chamados** |
| Catálogo | Usuários de demonstração, categorias e equipes. | **app/catalogo** |
| Notificações | Contrato de confirmação e implementação simulada. | **app/notificacoes** |
| Infraestrutura comum | Inicialização e sessão do banco SQLite. | **app/banco.py** |

Os módulos executam no mesmo processo. Chamados e catálogo usam o banco SQLite
compartilhado; chamado e evento inicial de histórico são gravados na mesma
transação. A notificação ocorre depois do commit. Os módulos não são
microsserviços e não possuem implantação ou bancos independentes.

## 3. Camadas e dependências

### Apresentação

**app/chamados/apresentacao.py** recebe HTTP, converte campos do formulário em um
comando e apresenta resultados. Não contém matriz de prioridade nem SQL.

### Aplicação

**AbrirChamadoService** coordena a abertura. Ele consulta o solicitante e a
categoria, pede a criação do chamado, solicita persistência e aciona a notificação.
**ConsultarChamadosService** coordena lista e detalhe e sempre informa o
solicitante ao repositório.

### Domínio

**Chamado**, **MatrizPrioridade**, **PoliticaPrazo** e **EventoHistorico** mantêm as
regras que não dependem de HTTP ou templates.

### Infraestrutura

Os repositórios SQLAlchemy convertem e persistem os objetos no SQLite.
**NotificadorFake** simula a dependência de confirmação.

Fluxo de chamadas e dependências no protótipo:

- O navegador acessa a apresentação por HTTP.
- A apresentação chama os serviços de aplicação para abrir e consultar chamados.
  Para montar as páginas, ela também consulta diretamente os repositórios do
  catálogo para obter o usuário de demonstração e as categorias.
- Os serviços de aplicação usam as regras do domínio e os repositórios SQLAlchemy.
- Os repositórios SQLAlchemy acessam o SQLite.
- **AbrirChamadoService** depende da interface **Notificador**, implementada por
  **NotificadorFake** nesta demonstração e escolhida na criação da aplicação.

A consulta direta do catálogo pela apresentação é uma simplificação localizada
do protótipo. Em uma evolução com autenticação real, ela pode ser coordenada por
um caso de uso da aplicação.

O identificador do solicitante é fixado na configuração da demonstração. O
repositório filtra as consultas por esse identificador, mas a aplicação não
autentica cada visitante: navegadores diferentes atuam como o mesmo usuário demo.

## 4. Fluxo implementado de abertura

1. O solicitante de demonstração informa categoria, impacto e urgência, além dos
   dados descritivos, no formulário.
2. A apresentação valida a forma dos dados e cria **AbrirChamadoComando**.
3. **AbrirChamadoService** busca o solicitante e a categoria pelos repositórios do
   catálogo.
4. **Chamado.abrir** valida os dados, calcula prioridade e prazo e define o estado.
5. **EventoHistorico.abertura** descreve o evento inicial.
6. O repositório grava chamado e histórico em uma única transação.
7. O serviço solicita confirmação ao **Notificador**.
8. A aplicação retorna o protocolo e exibe o detalhe persistido.

Se a categoria não tiver equipe, o chamado é criado em **EM_TRIAGEM**. Se a
notificação falhar, o chamado permanece gravado e a interface apresenta um aviso.
A equipe associada a um chamado em **EM_FILA** é apenas seu destino inicial; não
existe tela para recebimento ou assunção por técnico. Também não ocorre
classificação manual posterior pelo suporte nesta fatia.

## 5. Comunicação

- Navegador e aplicação comunicam-se de forma síncrona por HTTP.
- Chamadas entre módulos são chamadas locais no mesmo processo.
- SQLAlchemy comunica-se com SQLite de forma síncrona.
- A notificação do protótipo também é síncrona, mas ocorre depois da transação.
- Não existem broker, fila, RPC ou chamadas de rede internas.

## 6. Persistência

O protótipo utiliza um banco SQLite compartilhado. As tabelas principais são:

- **usuarios**;
- **equipes**;
- **categorias**;
- **chamados**;
- **eventos_historico**.

Chamado e evento de abertura são confirmados pelo mesmo commit. Uma exceção durante
a gravação provoca rollback dos dois registros.

## 7. Integração externa

**Notificador** possui somente a operação **confirmar_abertura**.
**NotificadorFake** registra confirmações em memória. Uma implementação futura que
preserve o contrato pode enviar e-mail ou outra mensagem sem alterar prioridade,
prazo ou persistência. Canais que exijam novos dados de contato também afetam o
catálogo e a montagem da confirmação no serviço.

## 8. Implantação

A implantação do protótipo contém:

~~~text
[Navegador] -> [Processo Flask] -> [Arquivo SQLite]
~~~

Essa forma é suficiente para demonstração local. Uma implantação institucional
deveria usar servidor WSGI, banco gerenciado, configuração externa e autenticação.

## 9. Relação com os ASRs

| ASR | Resposta arquitetural |
|---|---|
| ASR-01 - consistência | Mesma fronteira transacional para chamado e histórico, realizada no banco compartilhado. |
| ASR-02 - notificação substituível | Interface Notificador e implementação composta na inicialização. |
| ASR-03 - prioridade modificável | Matriz isolada no domínio e coberta por nove testes; prioridade e prazo calculados são persistidos, mas a versão da matriz não é. |

O ASR-01 restringe a fronteira de chamado e histórico, mas não determina sozinho a
topologia de toda a aplicação. Os ASRs 02 e 03 justificam fronteiras internas e a
organização em camadas. A escolha do monólito modular também considera a ausência
de requisitos de implantação independente, escala por módulo ou equipes autônomas.
