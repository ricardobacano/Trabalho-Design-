# Alternativas e trade-offs

## 1. Eixos da decisão

As alternativas não pertencem todas ao mesmo eixo. Monólito e microsserviços tratam
principalmente de implantação e distribuição. Camadas, Arquitetura Hexagonal e
microkernel tratam da organização interna e das dependências. A solução combina uma
decisão de cada nível: **monólito modular** como topologia e **camadas** como
organização interna.

## 2. Topologia e implantação

| Critério | Monólito simples | Monólito modular em camadas | Microsserviços |
|---|---|---|---|
| Modificabilidade | Baixa se regras, SQL e HTTP forem misturados. | Mudanças ficam concentradas nos módulos e camadas. | Alta independência quando fronteiras estão maduras. |
| Consistência | Transações locais simples. | Transações locais simples e fronteiras explícitas. | Continua local dentro de um serviço; operações entre bancos de serviços exigem coordenação ou consistência eventual. |
| Testabilidade | Pode exigir interface e banco se regras não forem isoladas. | Regras podem ser testadas sem HTTP. | Exige testes de contrato e de comunicação. |
| Implantação | Um artefato simples. | Um artefato simples. | Várias implantações e configuração de rede. |
| Escalabilidade | Escala a aplicação inteira. | Escala a aplicação inteira. | Permite escala independente. |
| Complexidade inicial | Menor. | Moderada e compatível com o trabalho. | Alta e sem requisito que a justifique. |
| Custo operacional | Baixo. | Baixo. | Maior: rede, observabilidade e várias implantações. |

O ASR-01 exige que chamado e histórico permaneçam na mesma fronteira transacional,
mas não obriga que toda a aplicação seja monolítica. O monólito modular foi escolhido
porque, além de atender essa fronteira local, não existem requisitos de implantação
independente, escala separada, equipes autônomas ou isolamento por processo.

## 3. Organização interna

| Alternativa | Ganho | Custo ou inadequação ao cenário atual |
|---|---|---|
| Camadas no monólito modular | Separa HTTP, coordenação, domínio e persistência com poucos mecanismos adicionais. | As dependências não são invertidas em todas as fronteiras e existe acesso direto localizado da apresentação ao catálogo. |
| Arquitetura Hexagonal | Isola o núcleo por portas e facilita trocar entradas, persistência e integrações. | Exigiria portas para repositórios, adaptadores e mapeamentos sem haver múltiplas persistências ou apresentações no protótipo. |
| Microkernel | Permite ampliar um núcleo estável por plugins opcionais. | Não há descoberta, instalação ou ciclo de vida de plugins; os módulos atuais são partes fixas do fluxo. |

A interface **Notificador** não transforma a solução em Hexagonal: ela é uma
abstração pontual para uma variação externa concreta. Da mesma forma,
**MatrizPrioridade** não é um plugin de microkernel; é uma política coesa chamada
diretamente pelo domínio.

## 4. Decisão

O **monólito modular em camadas** foi escolhido porque mantém chamado e histórico na
mesma fronteira transacional do ASR-01 e fornece separação interna suficiente para a
notificação e a prioridade dos ASRs 02 e 03, sem introduzir rede, mensageria,
infraestrutura de plugins ou portas para variações que ainda não existem.

O monólito simples teria menos arquivos, mas aumentaria o risco de concentrar
validação, prioridade e SQL nas rotas. Microsserviços permitiriam implantação
independente, porém o protótipo possui uma equipe pequena, uma única implantação e
nenhum requisito de escala independente.

## 5. Custos aceitos

- os módulos são implantados e escalados juntos;
- o banco é compartilhado;
- as fronteiras dependem de disciplina de código;
- a separação em camadas cria mais elementos que um script Flask único;
- a interface de notificação adiciona uma abstração, justificada pelo enunciado e
  pela necessidade de substituição.

## 6. Quando reavaliar

A decisão deve ser revista se surgirem equipes autônomas, implantação independente,
escalas muito diferentes entre módulos ou integrações que não possam compartilhar a
disponibilidade do monólito. Arquitetura Hexagonal deve ser reconsiderada se surgirem
múltiplas apresentações ou persistências que precisem ser substituídas; microkernel,
se o produto passar a exigir plugins opcionais mantidos e carregados separadamente.
