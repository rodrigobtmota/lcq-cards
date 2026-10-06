# Matriz de testes — Radar de Lideranças LCQ V2

Legenda: **PASS_OFFLINE** = executado offline com evidência · **ESTÁTICO** = verificado por validador/script sobre o YAML final · **PENDENTE_VALIDACAO_TENANT** = depende de SharePoint, Pessoa, permissão ou Power Automate reais.

## A. Validações estruturais (sobre o 2º unpack do `.msapp` final)

| Teste | Resultado | Evidência |
|---|---|---|
| Schema oficial pa.yaml v3.0 | PASS_OFFLINE — 0 erros | `evidencias/roundtrip_check.txt` |
| Sintaxe Power Fx (6.391 fórmulas) | PASS_OFFLINE — 0 erros | idem |
| Referências entre telas, Navigate, variáveis, coleções, Data Sources, chaves de Patch | PASS_OFFLINE — 0 problemas | idem |
| Round-trip PAC (pack → unpack) | PASS_OFFLINE — `Src` idêntico | idem |
| Conexões e Data Sources preservados | PASS_OFFLINE — conexões idênticas; só `RadioSample` removida | idem |
| Cobertura de campos do Patch × schema | PASS_OFFLINE — Demandas 16/16; módulos novos 100% | `evidencias/patch_coverage.txt` |
| Ausência de `MelhoriaIdentificada`, `colMelhoriasSemana`, `Select(btn…)`, `AllItems`, `DataHoraNormalizacao`, `PercentualProgresso`, `Aprendizado` | PASS_OFFLINE — 0 ocorrências | varredura final |
| Importação e abertura no Studio, App Checker | PENDENTE_VALIDACAO_TENANT | — |

## B. Lógica crítica executada no interpretador Power Fx (expressões extraídas do YAML final)

| # | Cenário | Resultado |
|---|---|---|
| 1 | Menu visível perfil SemAcesso | PASS |
| 2 | Menu visível perfil Integrante | PASS |
| 3 | Menu visível perfil Lideranca | PASS |
| 4 | Menu visível perfil Administrador | PASS |
| 5 | Soma pesos 0.4+0.3+0.2+0.1 válida | PASS |
| 6 | Soma pesos 0.4+0.3+0.2+0.05 válida | PASS |
| 7 | Soma pesos 0.25+0.25+0.25+0.25 válida | PASS |
| 8 | IPD E1 I1 U1 R1 | PASS |
| 9 | IPD E4 I4 U4 R4 | PASS |
| 10 | IPD E4 I3 U3 R2 | PASS |
| 11 | IPD E2 I4 U1 R3 | PASS |
| 12 | IPD E3 I2 U4 R1 | PASS |
| 13 | IPD: resposta Impacto nível 4 | PASS |
| 14 | IPD: pergunta sem resposta -> Blank (bloqueia gravação) | PASS |
| 15 | IPD: resposta fora da escala -> Blank | PASS |
| 16 | Demanda: bloqueio de permissão modo=Nova cadastrado=true podeEditar=false | PASS |
| 17 | Demanda: bloqueio de permissão modo=Nova cadastrado=false podeEditar=false | PASS |
| 18 | Demanda: bloqueio de permissão modo=Editar cadastrado=true podeEditar=true | PASS |
| 19 | Demanda: bloqueio de permissão modo=Editar cadastrado=true podeEditar=false | PASS |
| 20 | Demanda: bloqueio de permissão modo=Visualizar cadastrado=true podeEditar=true | PASS |
| 21 | Admin: Liderança tenta se autoelevar | PASS |
| 22 | Admin: Liderança promove terceiro a Administrador | PASS |
| 23 | Admin: Liderança cria integrante Administrador | PASS |
| 24 | Admin: Liderança rebaixa/edita Administrador | PASS |
| 25 | Admin: Liderança promove Integrante a Liderança (permitido) | PASS |
| 26 | Admin: Liderança cadastra Integrante (permitido) | PASS |
| 27 | Admin: Administrador promove a Administrador (permitido) | PASS |
| 28 | Integrante: e-mail duplicado (maiúsculas diferentes) | PASS |
| 29 | Integrante: edição do próprio registro não acusa duplicidade | PASS |
| 30 | Auditoria duplicidade: Novo com dimensão já avaliada no mês | PASS |
| 31 | Auditoria duplicidade: Novo quando o único existente está Cancelado | PASS |
| 32 | Auditoria duplicidade: Editar o próprio registro | PASS |
| 33 | Auditoria duplicidade: Editar outro registro para dimensão ocupada | PASS |
| 34 | Auditoria duplicidade: Cancelar registro não sofre bloqueio | PASS |
| 35 | Auditoria duplicidade: Novo em dimensão livre | PASS |
| 36 | Auditoria: botão Novo visível lid=false adm=false | PASS |
| 37 | Auditoria: botão Novo visível lid=true adm=false | PASS |
| 38 | Auditoria: botão Novo visível lid=true adm=true | PASS |
| 39 | Rotina limite 6: 3 novos de cada, nada gravado | PASS |
| 40 | Rotina limite 6: 6 novos de cada, nada gravado | PASS |
| 41 | Rotina limite 6: 4 Highlights gravados + 3 novos = 7 | PASS |
| 42 | Rotina limite 6: 3 gravados + 3 novos = 6 (limite exato) | PASS |
| 43 | Rotina limite 6: 6 de outro autor não contam (sem máximo global) | PASS |
| 44 | Rotina limite 6: 6 do mesmo autor em outra semana não contam | PASS |
| 45 | Rotina limite 6: 5 Concentrações gravadas + 3 novas = 8 | PASS |
| 46 | Rotina mínimo 3: H3 L3 C3 bloqueado | PASS |
| 47 | Rotina mínimo 3: H2 L3 C3 bloqueado | PASS |
| 48 | Rotina mínimo 3: H3 L3 C2 bloqueado | PASS |
| 49 | Rotina mínimo 3: H6 L3 C3 bloqueado | PASS |
| 50 | Bloqueio Concluir: opção Resolvido existe | PASS |
| 51 | Bloqueio Concluir: só "Concluído" existe | PASS |
| 52 | Bloqueio Concluir: sem opção exata (apenas "Em resolução") -> Blank, Patch não executa | PASS |
| 53 | Bloqueio Cancelar: opção Cancelado | PASS |
| 54 | Bloqueio Cancelar: ausente -> Blank | PASS |
| 55 | Bloqueio encerrado? status=Aberto | PASS |
| 56 | Bloqueio encerrado? status=Resolvido | PASS |
| 57 | Bloqueio encerrado? status=Cancelado | PASS |
| 58 | Bloqueio encerrado? status=Em resolução | PASS |
| 59 | Bloqueio encerrado? status=Concluído | PASS |
| 60 | Bloqueio edição: Integrante responsável | PASS |
| 61 | Bloqueio edição: Integrante criador | PASS |
| 62 | Bloqueio edição: Integrante sem vínculo | PASS |
| 63 | Bloqueio edição: Liderança sem vínculo | PASS |
| 64 | Encaminhamento atualização: Integrante responsável | PASS |
| 65 | Encaminhamento atualização: Integrante não responsável | PASS |
| 66 | Encaminhamento atualização: Liderança | PASS |
| 67 | Encaminhamento atrasado: aberto vencido | PASS |
| 68 | Encaminhamento atrasado: aberto no prazo | PASS |
| 69 | Encaminhamento atrasado: concluído vencido | PASS |
| 70 | Encaminhamento atrasado: sem prazo | PASS |
| 71 | Semana ISO Date(2026,10,6) | PASS |
| 72 | Semana ISO Date(2021,1,1) | PASS |
| 73 | Semana ISO Date(2024,12,30) | PASS |
| 74 | Semana ISO Date(2026,1,1) | PASS |

**Total: 74/74 PASS** (`evidencias/tests_result.txt`, especificação em `evidencias/tests_spec.json`).

## C. Matriz por perfil — roteiro para o tenant

Executar com um usuário real de cada perfil. A coluna "Offline" indica o que já está coberto por B ou pela verificação estática.

### Integrante

| Caso | Esperado | Offline | Tenant |
|---|---|---|---|
| Acesso / menu | Cockpit, Demandas, Ocorrências, Radar Semanal, Decisões e Guia; sem Capacidade, Auditoria e Administração | PASS_OFFLINE (B2) | PENDENTE_VALIDACAO_TENANT |
| Criar demanda | Grava em 1 Patch com Responsável (Pessoa), Status Aberta, 4 fatores e CargaReal | ESTÁTICO + B (IPD, permissão) | PENDENTE_VALIDACAO_TENANT |
| Editar demanda própria / de outro | Própria: edita. De outro: só visualiza | PASS_OFFLINE (B permissão) | PENDENTE_VALIDACAO_TENANT |
| Criticidade | Não editável | ESTÁTICO | PENDENTE_VALIDACAO_TENANT |
| Rotina semanal | Mínimo 3 / máximo 6 por categoria na semana | PASS_OFFLINE (B rotina) | PENDENTE_VALIDACAO_TENANT |
| Curadoria / envio da pauta | Toggle desabilitado; botão de envio oculto e com guarda | ESTÁTICO | PENDENTE_VALIDACAO_TENANT |
| Equipamentos | Cria; edita o que criou ou do qual é responsável | ESTÁTICO (sem alteração) | PENDENTE_VALIDACAO_TENANT |
| Bloqueios | Cria; edita, conclui e cancela o que criou ou do qual é responsável | PASS_OFFLINE (B bloqueio) | PENDENTE_VALIDACAO_TENANT |
| Decisões | Somente leitura | ESTÁTICO | PENDENTE_VALIDACAO_TENANT |
| Encaminhamentos | Atualiza status e acompanhamento dos seus; não cria | PASS_OFFLINE (B encaminhamento) | PENDENTE_VALIDACAO_TENANT |
| Auditoria / Administração | Sem acesso (menu e guardas) | PASS_OFFLINE (B2) | PENDENTE_VALIDACAO_TENANT |

### Liderança

| Caso | Esperado | Offline | Tenant |
|---|---|---|---|
| Priorização (Criticidade) | Editável | ESTÁTICO | PENDENTE_VALIDACAO_TENANT |
| Capacidade | Vê todos os integrantes ativos; semáforo por FaixaSustentavel | ESTÁTICO | PENDENTE_VALIDACAO_TENANT |
| Curadoria | Marca/desmarca `SelecionadoParaReuniao` | ESTÁTICO (sem alteração) | PENDENTE_VALIDACAO_TENANT |
| Envio da pauta | Só selecionados da semana; destinatários = integrantes ativos; sem envio duplo | ESTÁTICO | PENDENTE_VALIDACAO_TENANT (fluxo real) |
| Auditoria | Novo, Editar, Encerrar, Cancelar; bloqueio de duplicidade mês+dimensão, ignorando Cancelado | PASS_OFFLINE (B auditoria) | PENDENTE_VALIDACAO_TENANT |
| Integrantes | Cria e edita Integrante/Liderança; e-mail duplicado bloqueado | PASS_OFFLINE (B admin) | PENDENTE_VALIDACAO_TENANT |
| Elevação a Administrador (própria ou de terceiros) | Bloqueada | PASS_OFFLINE (B admin) | PENDENTE_VALIDACAO_TENANT |
| Parâmetros | Edita apenas os permitidos; não cria; soma dos pesos ≠ 1,00 gera aviso e usa pesos oficiais | PASS_OFFLINE (B pesos) + ESTÁTICO | PENDENTE_VALIDACAO_TENANT |
| Bloqueios | Edita todos | PASS_OFFLINE | PENDENTE_VALIDACAO_TENANT |
| Decisões / Encaminhamentos | Cria e edita; conclui encaminhamento | ESTÁTICO + B | PENDENTE_VALIDACAO_TENANT |
| Cockpit | 3 indicadores de exceção + auditoria do mês | ESTÁTICO | PENDENTE_VALIDACAO_TENANT |

### Administrador

| Caso | Esperado | Offline | Tenant |
|---|---|---|---|
| Acesso total | Todas as 9 entradas do menu | PASS_OFFLINE (B2) | PENDENTE_VALIDACAO_TENANT |
| Perfis | Concede e altera Administrador | PASS_OFFLINE (B admin) | PENDENTE_VALIDACAO_TENANT |
| Parâmetros | Cria e edita qualquer chave; duplicidade de chave bloqueada | ESTÁTICO | PENDENTE_VALIDACAO_TENANT |
| Manutenção | Diagnóstico e recarga | ESTÁTICO (sem alteração) | PENDENTE_VALIDACAO_TENANT |

### Usuário não cadastrado (SemAcesso)

| Caso | Esperado | Offline | Tenant |
|---|---|---|---|
| Menu | Só Cockpit e Guia, mais aviso no início | PASS_OFFLINE (B1) | PENDENTE_VALIDACAO_TENANT |
| Criar demanda, rotina ou bloqueio | Bloqueado | ESTÁTICO | PENDENTE_VALIDACAO_TENANT |

## D. CRUD por lista — casos-limite (tenant)

| Lista | Create | Read | Update | Concluir/Cancelar | Blank/obrigatório | Inválido/inexistente | Duplicidade | Erro de gravação |
|---|---|---|---|---|---|---|---|---|
| Radar_Demandas | Patch único | Coleção ativa | Patch por ID | Status via Choices; DataConclusao automática | Form.Valid + 4 perguntas | ID não localizado → aviso | — | Nada gravado + Notify |
| Radar_Bloqueios | ✔ | ✔ | ✔ | LookUp exato; sem opção → não grava | Título, responsável, abertura; motivo para encerrar | ID de demanda inexistente → aviso | — | Nada gravado + Notify |
| Radar_Decisoes | ✔ | ✔ | ✔ | DataFechamento automática | Título, tipo, semana AAAA-Sxx | IDPontoOrigem inexistente → aviso | — | idem |
| Radar_Encaminhamentos | ✔ | ✔ | ✔ (responsável: status e obs) | LookUp exato | Ação, responsável, prazo | idem | — | idem |
| Radar_GestaoAuditoria_LCQ | ✔ (restaurado) | ✔ | ✔ | Encerrado/Cancelado | Campos obrigatórios, e-mail, link | Registro não localizado | Mês+dimensão (exceto Cancelado) | idem |
| Radar_Integrantes | ✔ | ✔ | ✔ | Ativo=false | Nome, e-mail válido, faixa > 0 | — | E-mail (Lower, exclui o próprio ID) | idem |
| Radar_Config | ✔ (Admin) | ✔ | ✔ | — | Chave e valor numérico | — | Chave (Lower, exclui o próprio ID) | idem |
| Radar_RegistrosRotina | ✔ (lote) | ✔ | Curadoria | — | 3 mínimos | Semana inválida | Máximo de 6 por autor+semana | Retentativa parcial preservada |
| Radar_EquipamentosOperacionais | ✔ | ✔ | ✔ | Operacional → DataHoraEncerramento | Validações existentes | — | — | idem |

Todas as colunas desta seção: **PENDENTE_VALIDACAO_TENANT** para execução real; a lógica foi verificada offline conforme A e B.

## E. Regressão das telas

| Tela | Alteração | Validação offline |
|---|---|---|
| TelaCockpit | Exceções de gestão, menu, Guia | Schema, sintaxe, referências OK |
| TelaDemandas | Salvamento atômico, guarda de cadastro | + cobertura 16/16 + testes B |
| TelaCapacidade | Schema da coleção unificado | OK |
| TelaEquipamentos | Abas + Bloqueios; lógica de equipamentos intacta (apenas Visible por aba) | OK + testes B |
| TelaRadarSemanal | Melhoria removida, limite por semana, anti-duplo-clique | OK + testes B + diff por tokens |
| TelaAuditoria | Criação restaurada, duplicidade | OK + testes B |
| TelaDecisoesEncaminhamentos | Nova | OK + testes B |
| TelaAdministracao | Proteção de perfil, recarga síncrona, parâmetros | OK + testes B |
| Guia / Header / Menu | Menu atualizado nas 8 telas; Header (componente) inalterado | OK |
