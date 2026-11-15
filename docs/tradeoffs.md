# Alternativas e trade-offs

## 1. Alternativas

Foram comparadas três formas de organizar a solução:

1. monólito simples sem módulos explícitos;
2. monólito modular em camadas, escolhido;
3. microsserviços.

## 2. Comparação

| Critério | Monólito simples | Monólito modular em camadas | Microsserviços |
|---|---|---|---|
| Modificabilidade | Baixa se regras, SQL e HTTP forem misturados. | Mudanças ficam concentradas nos módulos e camadas. | Alta independência quando fronteiras estão maduras. |
| Consistência | Transações locais simples. | Transações locais simples e fronteiras explícitas. | Exige consistência distribuída entre serviços. |
| Testabilidade | Pode exigir interface e banco se regras não forem isoladas. | Regras podem ser testadas sem HTTP. | Exige testes de contrato e de comunicação. |
| Implantação | Um artefato simples. | Um artefato simples. | Várias implantações e configuração de rede. |
| Escalabilidade | Escala a aplicação inteira. | Escala a aplicação inteira. | Permite escala independente. |
| Complexidade inicial | Menor. | Moderada e compatível com o trabalho. | Alta e sem requisito que a justifique. |
| Custo operacional | Baixo. | Baixo. | Alto. |

## 3. Decisão

O **monólito modular em camadas** foi escolhido porque preserva a transação local do
ASR-01 e permite isolar a prioridade e a notificação dos ASRs 02 e 03 sem introduzir
rede, mensageria ou múltiplos bancos.

O monólito simples teria menos arquivos, mas aumentaria o risco de concentrar
validação, prioridade e SQL nas rotas. Microsserviços permitiriam implantação
independente, porém o protótipo possui uma equipe pequena, uma única implantação e
nenhum requisito de escala independente.

## 4. Custos aceitos

- os módulos são implantados e escalados juntos;
- o banco é compartilhado;
- as fronteiras dependem de disciplina de código;
- a separação em camadas cria mais elementos que um script Flask único;
- a interface de notificação adiciona uma abstração, justificada pelo enunciado e
  pela necessidade de substituição.

## 5. Quando reavaliar

A decisão deve ser revista se surgirem equipes autônomas, implantação independente,
escalas muito diferentes entre módulos ou integrações que não possam compartilhar a
disponibilidade do monólito.
