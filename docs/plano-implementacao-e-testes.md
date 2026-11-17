# Implementação e testes

## 1. Fatia vertical

A implementação selecionada representa o fluxo central do Tema 16:

~~~text
abrir chamado
  -> validar
  -> buscar categoria
  -> calcular prioridade e prazo
  -> encaminhar à equipe ou triagem
  -> persistir chamado e histórico
  -> confirmar por notificador simulado
~~~

A consulta obrigatória lista e detalha somente os chamados do solicitante de
demonstração.
Categoria, impacto e urgência são informados no formulário; a prioridade é
calculada automaticamente. O encaminhamento atribui equipe e estado, sem tela
de atendimento por técnico. O usuário é fixo na configuração, sem login real.

## 2. Rastreabilidade

| Requisito/ASR | Código principal | Teste |
|---|---|---|
| RF-01 | Chamado.abrir e rota novo | test_resumo_obrigatorio_rejeita_abertura |
| RF-02 / ASR-03 | MatrizPrioridade | test_matriz_de_prioridade, 9 casos |
| RF-03 | CategoriaRepository e Chamado.abrir | test_categoria_sem_equipe_encaminha_para_triagem |
| RF-04 / ASR-01 | ChamadoRepositorySQLAlchemy.salvar_novo | test_abertura_persiste_chamado_historico_e_notifica; test_falha_ao_gravar_historico_desfaz_todo_o_commit |
| RF-05 | listar_por_solicitante | test_consulta_exibe_apenas_chamados_do_usuario_demo |
| RF-06 | PoliticaPrazo | test_politica_de_prazo, 4 casos |
| ASR-02 | Notificador e NotificadorFake | testes de abertura e de falha da notificação |

## 3. Níveis de teste

- **Unidade:** matriz de prioridade e criação do domínio.
- **Integração:** serviço, repositórios e SQLite em memória.
- **Aceitação HTTP:** envio do formulário, redirecionamento e consulta das páginas.

## 4. Casos cobertos

1. nove combinações de impacto e urgência;
2. quatro prazos conforme a prioridade;
3. abertura com categoria mapeada;
4. abertura com categoria sem equipe;
5. rejeição de resumo vazio;
6. gravação conjunta de chamado e histórico;
7. rollback completo quando a gravação do histórico falha;
8. chamada ao notificador;
9. preservação do chamado quando a notificação falha;
10. lista filtrada, sem incluir chamados de outro identificador de solicitante.

O detalhe também aplica o filtro por solicitante no código, mas ainda não há um
teste automatizado específico para o acesso direto ao detalhe de outro usuário.

## 5. Limites

Login real, assunção por técnico, comentários, resolução e calendário comercial não
foram implementados. Eles permanecem como evolução do sistema completo e não são
necessários para comprovar a fatia vertical exigida.
