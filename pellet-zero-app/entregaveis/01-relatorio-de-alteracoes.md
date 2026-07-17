# Entregável 2 — Relatório de Alterações

Auditoria e correção do aplicativo **Programa de Segurança, Organização Física e Pellet Zero — LCQ/RJ** (pacote exportado em 17/07/2026).

Todas as correções foram aplicadas diretamente no `.msapp` (Controls/*.json + Src/*.pa.yaml, mantidos consistentes) e nos `definition.json` dos fluxos. As fórmulas foram gravadas no formato invariante do arquivo-fonte; o Power Apps Studio as exibirá automaticamente no padrão brasileiro (`;` / `;;`).

## Correções aplicadas

| # | Tela / Recurso | Controle | Propriedade | Problema identificado | Correção aplicada | Impacto | Status |
|---|---|---|---|---|---|---|---|
| 1 | App | App | OnStart | Variáveis globais `varBusyIndicadores`, `varBusyPDF`, `varBusyAuditoria`, `varResultadoAuditoria` nunca inicializadas (estados indefinidos no primeiro uso e após reaberturas) | Inicialização explícita no OnStart | Elimina comportamento indefinido de botões que dependem dessas variáveis | Aplicado |
| 2 | scrIndicadoresPrograma | (tela) | OnVisible | Lógica de cálculo duplicada e **divergente** da do botão Buscar; indicador oficial 4.4 (Conformidade Sustentada) inexistente; sem métricas de prazo/criticidade das NCs | Script canônico único, com: reset completo, `IfError`, cálculo de NCs vencidas, NCs Críticas/Segurança, reincidência por sala+item e Conformidade Sustentada | Números idênticos independentemente do caminho de atualização; indicador 4.4 disponível | Aplicado |
| 3 | scrIndicadoresPrograma | btnAtualizarIndicadores | OnSelect | **Erro bloqueador**: sem `IfError` — qualquer falha (rede/SharePoint) deixava `varBusyIndicadores = true` para sempre, travando o botão e a tela; não repovoava `colSalas`; sem fallback "TODAS" quando dropdown vazio; sem fallback de datas; não recalculava `varNCsNaoEncerradasPeriodo`; faltava a checagem `!IsBlank('DataCriacao ')` no cálculo de DiasTratamento | Substituído pelo **mesmo script canônico** do OnVisible | Elimina travamento permanente e divergência de resultados entre entrada na tela e clique em Buscar | Aplicado |
| 4 | scrIndicadoresPrograma | lblSubtituloRelatorioFlex_1 | Text | A tela não indicava o período analisado | Passa a exibir período (dd/mm/aaaa a dd/mm/aaaa) e sala após a busca | Leitura executiva do recorte analisado | Aplicado |
| 5 | scrIndicadoresPrograma | lbl_meta (card NCs) | Text | Card de NCs mostrava apenas encerradas/pendentes, sem leitura de prazo e criticidade | Inclui contagem de NCs **vencidas** e **Críticas/Segurança** | Card útil para decisão (exigência 4.3/4.5) | Aplicado |
| 6 | scrIndicadoresPrograma | pieGraficoIndicadores | Height | Gráfico ocupava toda a área do card (400px), sem espaço para o indicador 4.4 | Height = 330 | Abre espaço para o card de Conformidade Sustentada | Aplicado |
| 7 | scrIndicadoresPrograma | lblTituloSustentada, lblValorSustentada | (novos controles) | Indicador oficial **4.4 Conformidade Sustentada** ausente | Card novo: % de salas avaliadas sem reincidência (mesma sala + mesmo item de checklist com 2+ NCs no período filtrado) | Atende ao indicador 4.4 sem usar quantidade bruta como critério | Aplicado |
| 8 | scrIndicadoresPrograma | btnLimparFiltrosInd | (novo controle) | Não havia botão para limpar filtros (exigência 4.5) | Botão "Limpar": Reset de sala e datas + orientação ao usuário | Usabilidade dos filtros | Aplicado |
| 9 | scrIndicadoresPrograma | ddSalaFiltroInd, dtIniFiltroInd, dtFimFiltroInd, btnAtualizarIndicadores, Icone_home_14 | AccessibleLabel | Ausente (apontado pelo App Checker) | Rótulos acessíveis em pt-BR | Acessibilidade | Aplicado |
| 10 | TelaNovaAuditoria | (tela) | OnVisible | Inexistente — campos e variáveis não eram limpos ao entrar; `varResultadoAuditoria` podia carregar valor de sessão anterior | OnVisible novo: zera busy, resultado e reseta todos os campos | Evita conclusão de auditoria com dados residuais | Aplicado |
| 11 | TelaNovaAuditoria | btn_Salvar | OnSelect | **Erro bloqueador**: sem proteção contra duplo clique; `Patch` sem `IfError` — em falha de gravação o app exibia "sucesso", limpava os campos e navegava, **perdendo o registro da auditoria**; Claims usava `varUserEmail` sem fallback | Guard `varBusyAuditoria` + `IfError` no Patch + sucesso/limpeza/navegação condicionados ao êxito + `Coalesce(varUserEmail; User().Email)` | Elimina falso sucesso, perda de registro e envio duplicado | Aplicado |
| 12 | TelaNovaAuditoria | btn_Salvar | DisplayMode | Sempre habilitado, mesmo sem auditoria selecionada ou durante gravação | Desabilita durante salvamento e sem auditoria aberta selecionada | Previne concorrência e cliques inválidos | Aplicado |
| 13 | TelaNovaAuditoria | btn_Salvar | Text | Estático | "SALVANDO..." durante o processamento | Retorno visual exigido | Aplicado |
| 14 | TelaNovaAuditoria | 10 controles interativos | AccessibleLabel | Ausentes | Rótulos acessíveis (resultado, toggles, textos, home, salvar, cancelar) | Acessibilidade | Aplicado |
| 15 | scrRelatorioFiltroFlex | (tela) | OnVisible | 3 `Refresh()` desnecessários a cada visita (o `ClearCollect` subsequente já consulta o servidor) — carregamento lento | Refresh removidos do OnVisible (mantidos no botão Buscar, acionados pelo usuário) | Desempenho de navegação | Aplicado |
| 16 | scrRelatorioFiltroFlex | btnBuscar / btnGerarPDF | X, Width, Height | **Sobreposição de controles**: btnGerarPDF (920–1080) sobreposto ao btnBuscar (1030–1272) — botão parcialmente inacessível | btnBuscar X=930 W=160; btnGerarPDF X=1100 H=48 | Ambos os botões clicáveis e visíveis | Aplicado |
| 17 | scrRelatorioFiltroFlex | lblSemDadosRel | (novo controle) | Sem estado "sem dados" — tela vazia sem explicação | Rótulo "Sem resultados para exibir…" visível quando a galeria está vazia e não há busca em andamento | Estados exigidos (item 6) | Aplicado |
| 18 | scrRelatorioFiltroFlex | btnLimparFiltrosRel | (novo controle) | Sem botão limpar filtros | Botão "✕": reseta filtros, limpa coleções e link de PDF; desabilitado durante busca/geração | Usabilidade | Aplicado |
| 19 | scrRelatorioFiltroFlex | ddSalaFiltroRel, dtIniFiltroRel, dtFimFiltroRel, btnBuscar, btnGerarPDF, Icone_home_13 | AccessibleLabel | Ausentes | Rótulos acessíveis | Acessibilidade | Aplicado |
| 20 | Fluxo RelatorioPDF_HistoricoInspecoes_JSON_V2 | Build_vFiltroChecklist e Build_vFiltroNC | inputs (expressão) | **Risco de dados incorretos no PDF**: o filtro OData só combinava sala+datas quando as DUAS datas estavam preenchidas; com sala + uma única data, as datas eram silenciosamente ignoradas e o PDF trazia período maior que o filtrado | Expressão reescrita compondo as três condições de forma independente (sala, data inicial, data final, em qualquer combinação); fallback `ID gt 0` mantido | PDF fiel aos filtros informados no app | Aplicado |
| 21 | Fluxo RelatorioConsolidado_App_ProgramaPZ | Build_vFiltroChecklist e Build_vFiltroNC | inputs (expressão) | Mesmo defeito do item 20 | Mesma correção | Consistência (fluxo mantido no pacote, ver Pendências) | Aplicado |

## Auditado e mantido sem alteração (funcionamento correto verificado)

| Tela | Avaliação |
|---|---|
| TelaInicio | Criação do checklist com `IfError`, guard `varBusy`, validação de rodízio único ativo, ciclo por regra quadrimestral em contingência, navegação por sala correta (todas as 14 salas mapeadas para telas existentes) |
| TelaOrganizacao, TelaPellet, TelaReservaTecnica, TelaOficinaAOL, TelaAlmoxarifado, TelaLavagem, TelaShelter, TelaDeposito | Padrão uniforme: guard de duplo envio, validação de obrigatórios, cálculo de StatusGeral/StatusNC, `IfError` no Patch, navegação condicional Pellet/Final |
| TelaNCOrganizacao e demais 8 telas de NC | Enriquecimento pela MatrizClassificacaoNC com validação da regra oficial (Baixa 15d, Média 10d, Alta 7d, Crítica/Segurança ação imediata), contingência "Média/10 dias" rastreável, **prevenção de duplicidade** por ChecklistID+ItemChecklistOrigem, coleta de erros por item, atualização do checklist principal |
| TelaNCUsuario | Encerramento com tratativa obrigatória, `ConclusaoComAtraso`, recálculo de status do checklist, tratamento de status inválidos |
| TelaFinal | Consolidação e estados de erro adequados |
| Fluxos (estrutura) | TRY/CATCH/FINALLY, resposta padronizada (status/mensagem/urlrelatorio), tratamento "sem_dados", limpeza do HTML temporário, escape de aspas no OData |

## Classificação dos apontamentos do App Checker (576 itens)

| Categoria | Qtde | Classificação | Tratamento |
|---|---|---|---|
| Erros de fórmula | 0 | — | Nenhum erro bloqueador de Power Fx existia ou foi introduzido |
| acc-TabIndexShouldBeDefined | 355 | Acessibilidade (não bloqueador) | Parcial: AccessibleLabel adicionado nas 3 telas prioritárias; TabIndex em massa deve ser ajustado no Studio (ver Pendências) |
| acc-AccessibleLabelNeeded | 170 | Acessibilidade | Parcial (21 controles críticos corrigidos) |
| app-UnusedVariables | 16 | Recomendação | Não removidas por segurança (algumas são reservas de contingência); documentadas no Inventário |
| app-ForAllWithMutation | 13 | Desempenho (recomendação) | Mantido: os `ForAll` com Collect/Patch são intencionais (deduplicação sequencial); reescrever traria risco funcional |
| app-SuggestRemoteExecutionHint | 7+2 | Delegação | Avaliado: filtros principais (Choice `=`, datas) são delegáveis; `StatusRodizio.Value <> "Cancelado"` e casos análogos atuam sobre listas pequenas (rodízio) — sem risco prático; documentado |
| app-CollectingReadOnlyTable | 4 | Desempenho | Mantido (coleções locais deliberadas) |
| app-UnusedMediaResources | 5 | Recomendação | Mantido (sem risco) |
| app-CrossScreenEventDependencies | 2 | Recomendação | Mantido: `ResetForm` cross-screen na TelaInicio é intencional e funcional |
