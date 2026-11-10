# Trade-offs da arquitetura

**Projeto:** Sistema de Gerenciamento de Chamados de Suporte Técnico
**Arquitetura em avaliação:** monólito modular organizado em camadas

## 1. Resumo da escolha

A proposta mantém o sistema em uma única aplicação implantável e separa o código em módulos de domínio e camadas. Os casos de uso dependem de contratos para persistência e notificações; as regras centrais ficam separadas de interface e infraestrutura.

## 2. Benefícios esperados

- **Menor esforço de operação:** um artefato principal para executar e demonstrar.
- **Fluxo fácil de acompanhar:** abrir, encaminhar, assumir e resolver chamado ocorre dentro de uma aplicação.
- **Consistência simplificada:** mudanças do chamado e do histórico podem participar da mesma transação de banco.
- **Testes acessíveis:** prioridade e ciclo de vida podem ser testados sem infraestrutura distribuída.
- **Liberdade de evolução:** interfaces para banco e notificações reduzem dependência de uma implementação específica.
- **Adequação ao grupo:** permite divisão em módulos sem exigir que integrantes integrem serviços independentes desde o início.

## 3. Custos e limitações

- **Disciplina de módulos:** sem regras de dependência, um monólito pode virar código muito acoplado.
- **Implantação conjunta:** qualquer alteração do sistema pode exigir publicar a aplicação completa.
- **Escala conjunta:** módulos não podem ser escalados de forma independente.
- **Limites ainda sujeitos a mudança:** se as fronteiras do domínio forem mal definidas, módulos podem precisar ser reorganizados.
- **Separação em camadas exige cuidado:** abstrações excessivas podem atrasar um MVP pequeno.

## 4. Alternativas consideradas

| Alternativa | Motivo para não ser a escolha inicial |
|---|---|
| **Monólito sem módulos/camadas explícitos** | Começa simples, mas pode concentrar regras na interface e dificultar revisão e testes. |
| **Microsserviços** | Exigem implantação, comunicação, observabilidade e tratamento de falhas distribuídas sem necessidade demonstrada no escopo atual. |
| **Microkernel** | O requisito não prevê extensões instaláveis por plugins; não há um núcleo de produto que precise carregar funcionalidades independentes. |

## 5. Quando reavaliar

Reavaliar a decisão caso surjam necessidades concretas de escalar módulos isoladamente, implantar equipes independentes, integrar sistemas externos com disponibilidade própria ou separar domínios com regras e ciclos de mudança distintos. A reavaliação deve vir acompanhada de evidências e de um novo ADR.
