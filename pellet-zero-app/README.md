# Programa de Segurança, Organização Física e Pellet Zero — LCQ/RJ
## Auditoria técnica e correção do aplicativo (17/07/2026)

## Entregável 1 — Aplicativo corrigido

- **`pacote-corrigido/PelletZero_LCQRJ_pacote_corrigido.zip`** — pacote importável completo (app + 2 fluxos), reconstruído a partir do pacote original com todas as correções aplicadas.
- `pacote-corrigido/PelletZero_LCQRJ_document_corrigido.msapp` — somente o app, para abertura direta no Studio se preferir.
- `fontes-app/` — código-fonte corrigido (Src/*.pa.yaml e definition.json dos fluxos) para conferência e versionamento.

**Como importar:** Power Apps → Apps → Importar pacote de tela → selecionar o zip → em "Configuração de Importação" escolher **Atualizar** para o app e para os dois fluxos → revisar as conexões (SharePoint, Usuários do Office 365, OneDrive for Business) → Importar. Nada foi alterado em listas, colunas ou conexões — apenas fórmulas, dois reposicionamentos de botão, cinco controles novos e as expressões de filtro dos fluxos.

## Demais entregáveis

| Arquivo | Conteúdo |
|---|---|
| `entregaveis/01-relatorio-de-alteracoes.md` | Entregável 2 — tabela completa tela/controle/propriedade/problema/correção/impacto/status + classificação dos 576 apontamentos do App Checker |
| `entregaveis/02-pendencias-externas.md` | Entregável 3 — 10 pendências que dependem de decisão/estrutura externa |
| `entregaveis/03-plano-de-teste.md` | Entregável 4 — 20 cenários funcionais + 9 testes de falha, com resultado esperado e status |
| `entregaveis/04-inventario-final.md` | Entregável 5 — telas, listas, fluxos, conexões, coleções, variáveis, perfis e regras |
| `entregaveis/05-codigo-corrigido-ptbr.md` | Entregável 6 — código pt-BR completo, pronto para colar, dos pontos não aplicáveis diretamente ao .msapp (nova auditoria, evidência, perfis) |

## Resumo executivo das correções

Defeitos reais corrigidos dentro do pacote:

1. **Indicadores** — botão Buscar sem tratamento de erro podia **travar a tela permanentemente**; lógica duplicada e divergente do OnVisible produzia números diferentes conforme o caminho; indicador oficial **4.4 (Conformidade Sustentada)** não existia; sem botão limpar filtros, sem indicação do período, card de NCs sem leitura de prazo/criticidade. Tudo corrigido/complementado.
2. **Auditoria** — gravação **sem IfError** exibia sucesso, limpava os campos e navegava mesmo quando o SharePoint falhava (perda silenciosa do registro); sem bloqueio de duplo clique; campos não eram limpos ao entrar na tela. Corrigido.
3. **Relatórios** — botões **Buscar e Gerar PDF sobrepostos** (região 1030–1080 inacessível); 3 Refresh desnecessários no carregamento; sem estado "sem dados"; sem limpar filtros. Corrigido.
4. **Fluxos (ambos)** — filtro OData **ignorava as datas** quando apenas uma data era informada junto com a sala: o PDF podia sair com período maior que o filtrado. Expressão reescrita.
5. **App.OnStart** — 4 variáveis globais de estado nunca inicializadas. Corrigido.
6. Acessibilidade: AccessibleLabel adicionado a 21 controles interativos das 3 telas prioritárias.

O restante do aplicativo (início, 8 checklists, 9 telas de NC, tratativa e finalização) foi auditado integralmente e **mantido** — o padrão existente (guards de duplo envio, IfError, matriz de classificação com contingência rastreável, deduplicação de NC, atualização do checklist pai) está correto e preserva as regras institucionais do programa.

## Situação frente ao critério de conclusão

| Critério | Situação |
|---|---|
| Tela de Indicadores funcional e metodologicamente coerente | ✅ Corrigida; 4 indicadores oficiais presentes (4.2 com metas fixas atuais — refinamento por sala depende de decisão, ver Pendência 2) |
| Tela de Auditoria completa | ✅ Conclusão de auditorias corrigida e protegida; **criação de nova auditoria** depende de confirmação dos valores de Choice — código pronto no Entregável 6-A |
| Tela de Relatórios funcional | ✅ |
| Fluxos validados | ✅ Estrutura validada e filtros corrigidos; execução real exige ambiente (roteiro no plano de teste) |
| Sem erros bloqueadores de Power Fx | ✅ (0 no App Checker; nenhum introduzido — JSON e YAML validados) |
| Sem botões principais sem funcionamento | ✅ |
| Registros gravados corretamente / filtros confiáveis | ✅ no código; homologação com dados reais pendente |
| Delegação grave corrigida ou documentada | ✅ documentada (Relatório de Alterações + Pendência 7) |
| Acessos restritos protegidos | ⚠️ Depende da lista de perfis e permissões SharePoint (Pendência 4 / Entregável 6-C) — não existe base atual no app |
| Testes integrados | ⚠️ Validação estática completa; execução em homologação pendente (roteiro entregue) |
| Limitações documentadas | ✅ (10 pendências explícitas) |

O aplicativo **não** é declarado "finalizado" no sentido pleno do item 12: os itens marcados ⚠️ dependem de ambiente corporativo e decisões metodológicas que estão fora do pacote — todos documentados com a menor alteração necessária proposta.
