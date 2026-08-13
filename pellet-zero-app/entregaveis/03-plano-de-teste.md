# Entregável 4 — Plano de Teste Integrado

Status possíveis: **Validado estaticamente** (comportamento verificado no código-fonte corrigido) | **A executar em homologação** (exige ambiente Braskem conectado às listas reais).

## Cenários funcionais

| # | Cenário | Resultado esperado | Status |
|---|---|---|---|
| 1 | Usuário abre o aplicativo | OnStart inicializa usuário, busy-flags e carrega `colMatrizClassificacaoNCAtiva`; aviso claro se a matriz falhar ou estiver vazia (modo contingência) | Validado estaticamente |
| 2 | Sistema identifica ciclo e responsável | TelaInicio busca rodízio ativo publicado da sala; sem rodízio → ciclo por regra quadrimestral (C1/C2/C3-AAAA) em modo contingência com aviso; mais de um rodízio ativo → bloqueio com orientação | Validado estaticamente |
| 3 | Usuário acessa a sala correta | Navegação por sala (14 salas → 8 telas de checklist; Shelter por prefixo) | Validado estaticamente |
| 4 | Checklist 100% conforme | Patch com StatusGeral="Conforme", StatusNC="Concluído" (exceto salas com etapa Pellet), navegação para TelaFinal/TelaPellet | Validado estaticamente |
| 5 | Checklist com item "Não Conforme" | `colNCtemporarias` criada com item/pilar; navegação para a tela de NC da sala | Validado estaticamente |
| 6 | NC criada corretamente | Classificação pela MatrizClassificacaoNC (Baixa 15d / Média 10d / Alta 7d / Crítica ação imediata); matriz inválida → contingência "Média/10 dias" rastreável (`StatusClassificacaoNC`) | Validado estaticamente |
| 7 | Responsável visualiza a NC | TelaNCUsuario lista NCs Aberta/Em Tratamento ordenadas por prazo, filtro por sala, estado vazio presente | Validado estaticamente |
| 8 | Tratativa registrada | Encerramento exige ação corretiva preenchida; grava responsável, data e `ConclusaoComAtraso` | Validado estaticamente |
| 9 | Evidência anexada | **Sem suporte no app hoje** — ver Pendência 3 e Entregável 6-B | A executar após decisão |
| 10 | NC encerrada | Status "Encerrada"; recálculo do StatusGeral/StatusNC do checklist pai; avisos sobre pendências remanescentes | Validado estaticamente |
| 11 | Indicador atualizado | Tela de Indicadores recalcula pelos registros oficiais; busca com IfError; busy nunca fica travado (**corrigido**) | Validado estaticamente + executar |
| 12 | Auditoria consulta o registro | Dropdown lista auditorias "Aberta"; dados exibidos (tipo, sala, ciclo, data programada, status) | Validado estaticamente |
| 13 | Auditoria gera nova NC quando necessário | **Não automatizado**: auditoria registra achados/encaminhamento; geração de NC de auditoria depende do bloco 6-A (OrigemNC="Auditoria" já é suportado pela coluna) | A executar após decisão |
| 14 | Relatório gerado | Busca client-side + fluxo PDF com busy, botão desabilitado durante geração (**duplo clique bloqueado**) | Validado estaticamente + executar |
| 15 | PDF com dados corretos | Filtros sala+data única agora aplicados corretamente no OData (**corrigido nos 2 fluxos**) | A executar em homologação |
| 16 | Usuário sem permissão tenta função restrita | **Sem base de perfis hoje** — ver Pendência 4 / Entregável 6-C | A executar após criação da lista de perfis |
| 17 | Usuário tenta enviar duas vezes | Guards `varBusy*` + DisplayMode desabilitado em: envio de checklist, envio de NCs, tratativa, auditoria (**novo**), busca e PDF | Validado estaticamente |
| 18 | Dois usuários atualizam a mesma ocorrência | Patch por ID + deduplicação de NC por ChecklistID+Item; último Patch vence nos campos de status (comportamento SharePoint padrão — documentado) | Validado estaticamente |
| 19 | Lista com mais de 2.000 registros | Filtros principais delegáveis; limites de fluxo `$top 5000` — ver Pendência 7 | A executar (volume real) |
| 20 | Consulta sem resultados | Indicadores: cards "Sem base/Sem inspeção"; Relatórios: `lblSemDadosRel` (**novo**); NC: `lblSemResultados` | Validado estaticamente |

## Testes de falha

| # | Falha simulada | Resultado esperado | Status |
|---|---|---|---|
| F1 | SharePoint indisponível | OnStart: aviso de contingência da matriz; Indicadores/Relatórios: mensagem de erro e busy liberado (**corrigido**); checklist: erro sem falso sucesso | Validado estaticamente |
| F2 | Fluxo Power Automate com erro | CATCH responde `status="erro"` + `errotecnico`; app exibe a mensagem e libera o botão | Validado estaticamente |
| F3 | Usuário sem conexão | IfError nos Patches críticos com notificação; sem navegação em falha (**auditoria corrigida**) | Validado estaticamente |
| F4 | Campo obrigatório vazio | Checklist: botão desabilitado + validação dupla; Auditoria: aviso e bloqueio; NC: descrição obrigatória por item | Validado estaticamente |
| F5 | Matriz de classificação vazia | NCs em contingência Média/10d com motivo registrado | Validado estaticamente |
| F6 | Ciclo inexistente | Bloqueio com orientação ("Não foi possível definir o ciclo atual") | Validado estaticamente |
| F7 | Rodízio não configurado | Modo contingência com responsável = usuário logado e aviso | Validado estaticamente |
| F8 | Relatório sem registros | Fluxo responde `status="sem_dados"`; app exibe a mensagem sem abrir link | Validado estaticamente |
| F9 | Anexo inválido | Não aplicável (sem anexos no app) — ver Pendência 3 | A executar após decisão |

## Roteiro mínimo de homologação (pós-importação)

1. Importar o pacote (`Atualizar` app e fluxos), revisar conexões (SharePoint, Office 365 Users, OneDrive for Business).
2. Executar cenários 11, 14 e 15 com filtros: sala+período completo, só sala, sala+apenas data inicial (validar que o PDF respeita a data), só período.
3. Executar cenário 17 clicando rapidamente 2× em cada botão de envio.
4. Concluir 1 auditoria de teste com falha simulada (desligar rede) e confirmar que **não** aparece mensagem de sucesso.
5. Conferir o indicador 4.4 com uma sala que tenha 2 NCs do mesmo item no período.
