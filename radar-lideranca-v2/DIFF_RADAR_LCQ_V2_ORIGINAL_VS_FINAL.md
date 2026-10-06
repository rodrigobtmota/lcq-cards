# Diff técnico — Radar de Lideranças LCQ V2 (original × final)

Comparação semântica: fórmulas normalizadas (espaços e comentários ignorados) e diff por tokens. Base: `pac canvas unpack` do original × 2º unpack do `.msapp` final.

## Arquivos do pacote

```
packed.json: {'LoadFromYaml': True}
Header: 1.349
Telas (ordem): ['TelaCockpit', 'TelaDemandas', 'TelaCapacidade', 'TelaEquipamentos', 'TelaRadarSemanal', 'TelaAuditoria', 'TelaDecisoesEncaminhamentos', 'TelaAdministracao']
Arquivos de tela: 8
DataSources: ['ClickabuttoninPowerAppstosendanemail', 'ComboBoxSample', 'CustomGallerySample', 'DropDownSample', 'Radar_Bloqueios', 'Radar_Config', 'Radar_Decisoes', 'Radar_Demandas', 'Radar_Encaminhamentos', 'Radar_EquipamentosOperacionais', 'Radar_GestaoAuditoria_LCQ', 'Radar_Integrantes', 'Radar_RegistrosRotina', 'Radar_SnapshotsKPI']
DataSources com definição alterada: []
LocalConnectionReferences idênticas: True
Arquivos adicionados: ['Src/TelaDecisoesEncaminhamentos.pa.yaml', 'packed.json']
Arquivos removidos: []
Arquivos modificados: ['References/DataSources.json', 'Src/App.pa.yaml', 'Src/TelaAdministracao.pa.yaml', 'Src/TelaAuditoria.pa.yaml', 'Src/TelaCapacidade.pa.yaml', 'Src/TelaCockpit.pa.yaml', 'Src/TelaDemandas.pa.yaml', 'Src/TelaEquipamentos.pa.yaml', 'Src/TelaRadarSemanal.pa.yaml', 'Src/_EditorState.pa.yaml']
Assets/Resources preservados byte a byte: True 27
Controles em telas (final): 552
```

Arquivos modificados: apenas os esperados. `References/DataSources.json` teve só a remoção de `RadioSample`; as demais definições estão idênticas. Assets, temas, recursos, `Properties.json`, `Header.json` e `Controls/*.json` não mudaram (com `LoadFromYaml: true`, `Controls/*.json` é regenerado pelo Studio a partir do YAML).

## Resumo por tela

| Tela | Controles adicionados | Propriedades alteradas/novas/removidas |
|---|---|---|
| App | 0 | 1 |
| TelaAdministracao | 0 | 12 |
| TelaAuditoria | 0 | 11 |
| TelaCapacidade | 0 | 6 |
| TelaCockpit | 1 | 6 |
| TelaDecisoesEncaminhamentos | 95 | 3 |
| TelaDemandas | 0 | 30 |
| TelaEquipamentos | 42 | 27 |
| TelaRadarSemanal | 1 | 35 |

Controle removido: `TelaRadarSemanal.btnAbaMelhoriaRotina`, renomeado para `btnEnviarPautaRotina`. A lógica é idêntica; só foram adicionadas a trava anti-duplo-clique (`OnSelect`) e o `DisplayMode`.

## Detalhe (diff por tokens; HTML truncado em 400 caracteres por trecho)

```
## Controles adicionados
+ ('TelaCockpit', 'htmlGestaoExcecoes') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'Header_PT_Decisoes') CanvasComponent
+ ('TelaDecisoesEncaminhamentos', 'btnAbaDecisoes') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnAbaEncaminhamentos') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnAbrirDecisao') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnAbrirEncaminhamento') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnAtualizarDecisoes') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnAtualizarEncaminhamentos') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnConcluirEncaminhamento') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnFecharAjudaDecisoes') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnFecharPainelDecisao') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnFecharPainelEncaminhamento') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnFecharRodapeDecisao') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnFecharRodapeEncaminhamento') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnFundoAjudaDecisoes') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnFundoPainelDecisao') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnFundoPainelEncaminhamento') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnMenuDecisoes') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnNovaDecisao') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnNovoEncaminhamento') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnSalvarDecisao') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'btnSalvarEncaminhamento') Classic/Button@2.2.0
+ ('TelaDecisoesEncaminhamentos', 'cntAbasDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntAjudaDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntAreaListaDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntAreaListaEncaminhamentos') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntCabecalhoAjudaDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntConteudoDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntCorpoAjudaDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntCorpoDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntEspacoFiltrosDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntEspacoFiltrosEncaminhamentos') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntFiltrosDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntFiltrosEncaminhamentos') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntMenuDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntPainelDecisao') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntPainelEncaminhamento') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'cntPrincipalDecisoes') GroupContainer@1.5.0
+ ('TelaDecisoesEncaminhamentos', 'ddResponsavelDecisao') Classic/DropDown@2.3.1
+ ('TelaDecisoesEncaminhamentos', 'ddResponsavelEncaminhamento') Classic/DropDown@2.3.1
+ ('TelaDecisoesEncaminhamentos', 'ddSituacaoDecisoes') Classic/DropDown@2.3.1
+ ('TelaDecisoesEncaminhamentos', 'ddSituacaoEncaminhamentos') Classic/DropDown@2.3.1
+ ('TelaDecisoesEncaminhamentos', 'ddStatusDecisao') Classic/DropDown@2.3.1
+ ('TelaDecisoesEncaminhamentos', 'ddStatusEncaminhamento') Classic/DropDown@2.3.1
+ ('TelaDecisoesEncaminhamentos', 'ddTipoDecisao') Classic/DropDown@2.3.1
+ ('TelaDecisoesEncaminhamentos', 'ddTipoFiltroDecisoes') Classic/DropDown@2.3.1
+ ('TelaDecisoesEncaminhamentos', 'dpPrazoDecisao') Classic/DatePicker@2.6.0
+ ('TelaDecisoesEncaminhamentos', 'dpPrazoEncaminhamento') Classic/DatePicker@2.6.0
+ ('TelaDecisoesEncaminhamentos', 'galDecisoes') Gallery@2.15.0
+ ('TelaDecisoesEncaminhamentos', 'galEncaminhamentos') Gallery@2.15.0
+ ('TelaDecisoesEncaminhamentos', 'galMenuDecisoes') Gallery@2.15.0
+ ('TelaDecisoesEncaminhamentos', 'htmlAjudaDecisoes') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlCabecalhoDecisoes') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlCabecalhoEncaminhamentos') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlCreditosDecisoes') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlEstadoDecisoes') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlEstadoEncaminhamentos') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlHeaderPainelDecisao') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlHeaderPainelEncaminhamento') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlKpisDecisoes') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlLinhaDecisao') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlLinhaEncaminhamento') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlMenuDecisoes') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlNotaDecisao') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlNotaEncaminhamento') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlTituloAjudaDecisoes') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlTituloCabecalhoDecisoes') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlTituloDecisoesEnc') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlVazioDecisoes') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'htmlVazioEncaminhamentos') HtmlViewer@2.1.0
+ ('TelaDecisoesEncaminhamentos', 'icoAjudaDecisoes') Image@2.2.3
+ ('TelaDecisoesEncaminhamentos', 'lblDescricaoDecisao') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblObservacaoEncaminhamento') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblOrigemDecisao') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblOrigemEncaminhamento') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblPrazoDecisao') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblPrazoEncaminhamento') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblResponsavelDecisao') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblResponsavelEncaminhamento') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblResultadoDecisao') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblSemanaDecisao') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblStatusDecisao') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblStatusEncaminhamento') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblTipoDecisao') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblTituloDecisao') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'lblTituloEncaminhamento') Label@2.5.1
+ ('TelaDecisoesEncaminhamentos', 'txtBuscaDecisoes') Classic/TextInput@2.3.2
+ ('TelaDecisoesEncaminhamentos', 'txtBuscaEncaminhamentos') Classic/TextInput@2.3.2
+ ('TelaDecisoesEncaminhamentos', 'txtDescricaoDecisao') Classic/TextInput@2.3.2
+ ('TelaDecisoesEncaminhamentos', 'txtObservacaoEncaminhamento') Classic/TextInput@2.3.2
+ ('TelaDecisoesEncaminhamentos', 'txtOrigemDecisao') Classic/TextInput@2.3.2
+ ('TelaDecisoesEncaminhamentos', 'txtOrigemEncaminhamento') Classic/TextInput@2.3.2
+ ('TelaDecisoesEncaminhamentos', 'txtResultadoDecisao') Classic/TextInput@2.3.2
+ ('TelaDecisoesEncaminhamentos', 'txtSemanaDecisao') Classic/TextInput@2.3.2
+ ('TelaDecisoesEncaminhamentos', 'txtTituloDecisao') Classic/TextInput@2.3.2
+ ('TelaDecisoesEncaminhamentos', 'txtTituloEncaminhamento') Classic/TextInput@2.3.2
+ ('TelaEquipamentos', 'btnAbaBloqueiosOc') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'btnAbaEquipamentosOc') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'btnAbrirBloqueio') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'btnAtualizarBloqueios') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'btnCancelarStatusBloqueio') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'btnConcluirBloqueio') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'btnFecharPainelBloqueio') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'btnFecharRodapeBloqueio') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'btnFundoPainelBloqueio') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'btnNovoBloqueio') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'btnSalvarBloqueio') Classic/Button@2.2.0
+ ('TelaEquipamentos', 'cntAbasOcorrencias') GroupContainer@1.5.0
+ ('TelaEquipamentos', 'cntAreaListaBloqueios') GroupContainer@1.5.0
+ ('TelaEquipamentos', 'cntEspacoFiltrosBloqueios') GroupContainer@1.5.0
+ ('TelaEquipamentos', 'cntFiltrosBloqueios') GroupContainer@1.5.0
+ ('TelaEquipamentos', 'cntPainelBloqueio') GroupContainer@1.5.0
+ ('TelaEquipamentos', 'ddImpactoBloqueio') Classic/DropDown@2.3.1
+ ('TelaEquipamentos', 'ddResponsavelBloqueio') Classic/DropDown@2.3.1
+ ('TelaEquipamentos', 'ddSituacaoBloqueios') Classic/DropDown@2.3.1
+ ('TelaEquipamentos', 'ddStatusBloqueio') Classic/DropDown@2.3.1
+ ('TelaEquipamentos', 'dpAberturaBloqueio') Classic/DatePicker@2.6.0
+ ('TelaEquipamentos', 'dpResolucaoBloqueio') Classic/DatePicker@2.6.0
+ ('TelaEquipamentos', 'galBloqueios') Gallery@2.15.0
+ ('TelaEquipamentos', 'htmlCabecalhoBloqueios') HtmlViewer@2.1.0
+ ('TelaEquipamentos', 'htmlEstadoBloqueios') HtmlViewer@2.1.0
+ ('TelaEquipamentos', 'htmlHeaderPainelBloqueio') HtmlViewer@2.1.0
+ ('TelaEquipamentos', 'htmlKpisBloqueios') HtmlViewer@2.1.0
+ ('TelaEquipamentos', 'htmlLinhaBloqueio') HtmlViewer@2.1.0
+ ('TelaEquipamentos', 'htmlNotaBloqueio') HtmlViewer@2.1.0
+ ('TelaEquipamentos', 'htmlVazioBloqueios') HtmlViewer@2.1.0
+ ('TelaEquipamentos', 'lblAberturaBloqueio') Label@2.5.1
+ ('TelaEquipamentos', 'lblDemandaBloqueio') Label@2.5.1
+ ('TelaEquipamentos', 'lblImpactoBloqueio') Label@2.5.1
+ ('TelaEquipamentos', 'lblMotivoBloqueio') Label@2.5.1
+ ('TelaEquipamentos', 'lblResolucaoBloqueio') Label@2.5.1
+ ('TelaEquipamentos', 'lblResponsavelBloqueio') Label@2.5.1
+ ('TelaEquipamentos', 'lblStatusBloqueio') Label@2.5.1
+ ('TelaEquipamentos', 'lblTituloBloqueio') Label@2.5.1
+ ('TelaEquipamentos', 'txtBuscaBloqueios') Classic/TextInput@2.3.2
+ ('TelaEquipamentos', 'txtDemandaBloqueio') Classic/TextInput@2.3.2
+ ('TelaEquipamentos', 'txtMotivoBloqueio') Classic/TextInput@2.3.2
+ ('TelaEquipamentos', 'txtTituloBloqueio') Classic/TextInput@2.3.2
+ ('TelaRadarSemanal', 'btnEnviarPautaRotina') Classic/Button@2.2.0
## Controles removidos
- ('TelaRadarSemanal', 'btnAbaMelhoriaRotina') Classic/Button@2.2.0
## Controles com tipo/pai alterado
## Propriedades alteradas
* ALTERADA App.App.OnStart
    insert: -[]  +[varSomaPesosConfig , Round ( varPesoEsforco + varPesoImpacto + varPesoUrgencia + varPesoRisco , 4 ) ) ; Set ( varPesosConfigValidos , Abs ( varSomaPesosConfig - 1 ) < = 0 . 0001 ) ; If ( ! varPesosConfigValidos , Set ( varPesoEsforco , 0 . 40 ) ; Set ( varPesoImpacto , 0 . 30 ) ; Set ( varPesoUrgencia , 0 . 20 ) ; Set ( varPesoRisco , 0 . 10 ) ) ; Set (]
    delete: -[varUsuarioAtual , Lower ( Trim ( User ( ) . Email ) ) ) ; Set (]  +[]
    insert: -[]  +[) ; If ( ! varUsuarioCadastrado , Notify ( "Seu usuário não está cadastrado como integrante ativo do Radar. O acesso fica restrito à consulta do Cockpit e do Guia. Procure a liderança para solicitar o cadastro." , NotificationType . Warning ) ) ; If ( ! varPesosConfigValidos & & varEhLideranca , Notify ( "A soma dos pesos do IPD em Radar_Config é " & Text ( varSomaPesosConfig , "[$-en-US]0.00" ) &]
    replace: -[true]  +[varUsuarioCadastrado]
    replace: -["Equipamentos Críticos"]  +["Ocorrências Operacionais"]
    replace: -["EQ"]  +["OC"]
    replace: -[true]  +[varUsuarioCadastrado]
    replace: -[true]  +[varUsuarioCadastrado]
    insert: -[]  +["Decisoes" , Titulo : "Decisões e Encaminhamentos" , Sigla : "DE" , Ordem : 7 , Visivel : varUsuarioCadastrado } , { Chave :]
    replace: -[7]  +[8]
    replace: -[8]  +[9]
    delete: -[colMelhoriasSemana , { IDLocal : GUID ( ) , Ordem : 0 , Texto : "" , Obrigatorio : false , Salvo : false } ) ; Clear ( colMelhoriasSemana ) ; ClearCollect (]  +[]
* ALTERADA TelaAdministracao.TelaAdministracao.OnVisible
    delete: -[If ( varEhAdmin ,]  +[]
    delete: -[, "Parametros" )]  +[]
* ALTERADA TelaAdministracao.btnMenuAdministracao.OnSelect
    insert: -[]  +["Decisoes" , Navigate ( TelaDecisoesEncaminhamentos , ScreenTransition . Fade ) ,]
* ALTERADA TelaAdministracao.btnSalvarIntegranteAdmin.OnSelect
    insert: -[]  +[, NotificationType . Warning ) , ! IsMatch ( Trim ( txtEmailIntegranteAdmin . Text ) , Match . Email ) , Notify ( "Informe um e-mail válido." , NotificationType . Warning ) , varFaixaIntegranteNumerica < = 0 , Notify ( "A faixa sustentável deve ser maior que zero." , NotificationType . Warning ) , ! varEhAdmin & & ( ddPerfilIntegranteAdmin . Selected . Value = "Administrador" | | ( varModoIntegran]
    replace: -[Select]  +[Set]
    replace: -[btnAtualizarAdministracao]  +[varFalhaRecargaIntegranteAdmin , IfError ( Refresh ( Radar_Integrantes ) ; ClearCollect ( colIntegrantesAdmin , SortByColumns ( Radar_Integrantes , "Title" , SortOrder . Ascending ) ) ; ClearCollect ( colIntegrantes , Filter ( Radar_Integrantes , Ativo = true )]
    replace: -[varFalhaRecargaIntegranteAdmin]  +[varDataUltimaAtualizacao]
    replace: -[! IsBlank]  +[Now]
    replace: -[varErroAdministracao]  +[) ) ; false , true]
* ALTERADA TelaAdministracao.btnSalvarParametroAdmin.OnSelect
    insert: -[]  +[, NotificationType . Warning ) , varModoParametroAdmin = "Novo" & & ! varEhAdmin , Notify ( "Somente o Administrador pode criar novos parâmetros." , NotificationType . Warning ) , ! varEhAdmin & & ! ( Trim ( txtChaveParametroAdmin . Text ) in [ "PesoEsforco" , "PesoImpacto" , "PesoUrgencia" , "PesoRisco" , "FaixaSustentavelPadrao" , "DiasAtraso" , "IPDLimiteBaixa" , "IPDLimiteModerada" , "IPDLimit]
    replace: -[Select]  +[IfError]
    replace: -[btnRecarregarParametrosAdmin]  +[Refresh ( Radar_Config ) ; ClearCollect ( colConfigAdmin , SortByColumns ( Radar_Config , "Title" , SortOrder . Ascending ) ) ; ClearCollect ( colConfig , ForAll ( Radar_Config As cfg , { Chave : cfg . Título , ValorTexto : cfg . Valor , ValorNumerico : IfError ( Value ( cfg . Valor , "en-US" ) , Blank ( ) ) , Descricao : cfg . Descricao } ) ) ; Set ( varPesoEsforco , Coalesce ( LookUp ( colConfig]
    insert: -[]  +[If ( varFalhaRecargaParametroAdmin , Notify ( "Parâmetro salvo, mas os parâmetros não puderam ser recarregados agora. Use Recarregar parâmetros." , NotificationType . Warning ) , ! varPesosConfigValidos , Notify ( "Parâmetro salvo. A soma atual dos pesos é " & Text ( varSomaPesosConfig , "[$-en-US]0.00" ) & " (esperado 1.00): até a correção, o IPD usa os pesos oficiais 0.40 / 0.30 / 0.20 / 0.10." ]
    insert: -[]  +[)]
* ALTERADA TelaAdministracao.htmlAjudaAdministracao.HtmlText
    replace: -[" </div> </div> <div style='margin-top:20px;color:#102A4C;font-size:18px;font-weight:800;'> 1. Integrantes </div> <div style='margin-top:9px;color:#41576E;line-height:23px;'> • Cadastre o nome, o e-mail corporativo e o perfil.<br> • Os perfis oficiais são Integrante, Lideranca e Administrador.<br> • Defina a faixa sustentável de carga de cada pessoa.<br> • Desative integrantes que saírem do escopo]  +[" </div> </div> <div style='margin-top:20px;color:#102A4C;font-size:18px;font-weight:800;'> 1. Integrantes </div> <div style='margin-top:9px;color:#41576E;line-height:23px;'> • Cadastre o nome, o e-mail corporativo e o perfil.<br> • Os perfis oficiais são Integrante, Lideranca e Administrador.<br> • Defina a faixa sustentável de carga de cada pessoa.<br> • Desative integrantes que saírem do escopo]
* ALTERADA TelaAdministracao.htmlMenuAdministracao.HtmlText
    replace: -["Equipamentos<br>Críticos"]  +["Ocorrências<br>Operacionais"]
    insert: -[]  +[, "Decisoes" , "Decisões e<br>Encaminhamentos"]
* NOVA TelaAdministracao.lblChaveParametroAdmin.TabIndex
* NOVA TelaAdministracao.lblDescricaoParametroAdmin.TabIndex
* NOVA TelaAdministracao.lblEmailIntegranteAdmin.TabIndex
* NOVA TelaAdministracao.lblNomeIntegranteAdmin.TabIndex
* NOVA TelaAdministracao.lblPerfilFaixaIntegranteAdmin.TabIndex
* NOVA TelaAdministracao.lblValorParametroAdmin.TabIndex
* ALTERADA TelaAuditoria.btnMenuAuditoria.OnSelect
    insert: -[]  +["Decisoes" , Navigate ( TelaDecisoesEncaminhamentos , ScreenTransition . Fade ) ,]
* ALTERADA TelaAuditoria.btnNovoRegistroAuditoria.Visible
    replace: -[false]  +[varEhLideranca | | varEhAdmin]
* ALTERADA TelaAuditoria.btnSalvarAuditoria.OnSelect
    insert: -[]  +[If ( vStatusRegistro = "Cancelado" , Blank ( ) ,]
    insert: -[]  +[( Filter]
    insert: -[]  +[) , StatusRegistro . Value < > "Cancelado" )]
* ALTERADA TelaAuditoria.galMatrizAuditoria.Items
    insert: -[]  +[Trim (]
    insert: -[]  +[)]
* ALTERADA TelaAuditoria.htmlMenuAuditoria.HtmlText
    replace: -["Equipamentos<br>Críticos"]  +["Ocorrências<br>Operacionais"]
    insert: -[]  +[, "Decisoes" , "Decisões e<br>Encaminhamentos"]
* NOVA TelaAuditoria.lblAcaoAuditoria.TabIndex
* NOVA TelaAuditoria.lblClassificacaoAuditoria.TabIndex
* NOVA TelaAuditoria.lblDescricaoAuditoria.TabIndex
* NOVA TelaAuditoria.lblResponsavelPrazoAuditoria.TabIndex
* NOVA TelaAuditoria.lblStatusLinkAuditoria.TabIndex
* NOVA TelaAuditoria.lblTituloMesAuditoria.TabIndex
* ALTERADA TelaCapacidade.TelaCapacidade.OnVisible
    replace: -[CapacidadeMaxima]  +[FaixaSustentavel]
* ALTERADA TelaCapacidade.btnMenuCapacidade.OnSelect
    insert: -[]  +["Decisoes" , Navigate ( TelaDecisoesEncaminhamentos , ScreenTransition . Fade ) ,]
* ALTERADA TelaCapacidade.htmlKpisCapacidade.HtmlText
    replace: -[CapacidadeMaxima]  +[FaixaSustentavel]
* ALTERADA TelaCapacidade.htmlLinhaCapacidade.HtmlText
    replace: -[CapacidadeMaxima]  +[FaixaSustentavel]
* ALTERADA TelaCapacidade.htmlMenuCapacidade.HtmlText
    replace: -["Equipamentos<br>Críticos"]  +["Ocorrências<br>Operacionais"]
    insert: -[]  +[, "Decisoes" , "Decisões e<br>Encaminhamentos"]
* ALTERADA TelaCapacidade.htmlResumoPessoaCapacidade.HtmlText
    replace: -[CapacidadeMaxima]  +[FaixaSustentavel]
* ALTERADA TelaCockpit.HtmlMenuCockPit.HtmlText
    replace: -["Equipamentos<br>Críticos"]  +["Ocorrências<br>Operacionais"]
    insert: -[]  +[, "Decisoes" , "Decisões e<br>Encaminhamentos"]
* ALTERADA TelaCockpit.TelaCockpit.OnVisible
    insert: -[]  +[} ) ; UpdateIf ( colMenu , Chave = "Demandas" | | Chave = "Equipamentos" | | Chave = "Rotina" | | Chave = "Decisoes" , { Visivel : varUsuarioCadastrado]
    insert: -[]  +[varFalhaGestaoCockpit , false ) ; IfError ( Concurrent ( Refresh ( Radar_Bloqueios ) , Refresh ( Radar_Encaminhamentos ) , If ( varEhLideranca | | varEhAdmin , Refresh ( Radar_GestaoAuditoria_LCQ ) ) ) ; ClearCollect ( colBloqueiosAtivosCockpit , AddColumns ( Filter ( Filter ( Radar_Bloqueios , Criado > = DateAdd ( Today ( ) , - 730 , TimeUnit . Days ) ) , ! ( Coalesce ( Status . Value , "" ) in []
* ALTERADA TelaCockpit.btnMenuItem.OnSelect
    insert: -[]  +["Decisoes" , Navigate ( TelaDecisoesEncaminhamentos , ScreenTransition . Fade ) ,]
* NOVA TelaCockpit.cntConteudoNovo.LayoutOverflowY
* ALTERADA TelaCockpit.htmlAjudaCockpit.HtmlText
    replace: -["<div style='padding:10px 12px;border:1px solid #DCE5EE;border-radius:9px'><b>Cockpit Executivo</b><br>Mostra as principais exceções e o que precisa da atenção da liderança.</div>"]  +["<div style='padding:10px 12px;border:1px solid #DCE5EE;border-radius:9px'><b>Cockpit Executivo</b><br>Mostra as principais exceções ao vivo: demandas atrasadas, capacidade, equipamentos, bloqueios ativos, encaminhamentos atrasados e auditorias em risco.</div>"]
    replace: -["<div style='padding:10px 12px;border:1px solid #DCE5EE;border-radius:9px'><b>Equipamentos Críticos</b><br>Acompanha ocorrências até o retorno do equipamento ao status Operacional.</div>"]  +["<div style='padding:10px 12px;border:1px solid #DCE5EE;border-radius:9px'><b>Ocorrências Operacionais</b><br>Aba Equipamentos: ocorrências até o retorno ao status Operacional. Aba Bloqueios: impedimentos que travam a rotina, com responsável e motivo de resolução.</div>"]
    insert: -[]  +[& "<div style='padding:10px 12px;border:1px solid #DCE5EE;border-radius:9px'><b>Decisões e Encaminhamentos</b><br>Memória da gestão (decisões, alinhamentos e pendências de definição) e ações executáveis com responsável, prazo e status.</div>"]
    replace: -["<div style='margin-top:12px'><b>Exemplo de uma demanda</b><br>Esforço 4, Impacto 5, Urgência 3 e Risco 2:<br><span style='font-weight:800'>4 × 40% + 5 × 30% + 3 × 20% + 2 × 10% = 3,90 pontos de carga.</span></div>"]  +["<div style='margin-top:12px'><b>Exemplo de uma demanda</b><br>Esforço 4, Impacto 3, Urgência 3 e Risco 2 (escala oficial de 1 a 4):<br><span style='font-weight:800'>4 × 40% + 3 × 30% + 3 × 20% + 2 × 10% = 3,30 pontos de carga.</span></div>"]
* ALTERADA TelaCockpit.htmlGuiaConteudoCockpit.HtmlText
    replace: -["<div style='padding:16px;border:1px solid #CFE0EF;border-radius:12px;background:#F4F8FC;font-family:Segoe UI,Arial,sans-serif;color:#334155;font-size:14px;line-height:21px'><div style='font-size:19px;font-weight:800;color:#0E2A4A'>Telas do Radar</div><div style='margin-top:8px'><b>Cockpit Executivo:</b> exceções e prioridades.<br><b>Demandas:</b> atividades que consomem capacidade e IPD.<br><b>Ca]  +["<div style='padding:16px;border:1px solid #CFE0EF;border-radius:12px;background:#F4F8FC;font-family:Segoe UI,Arial,sans-serif;color:#334155;font-size:14px;line-height:21px'><div style='font-size:19px;font-weight:800;color:#0E2A4A'>Telas do Radar</div><div style='margin-top:8px'><b>Cockpit Executivo:</b> exceções e prioridades, calculadas ao vivo.<br><b>Demandas:</b> atividades que consomem capaci]
    replace: -["<div style='padding:16px;border:1px solid #CFE0EF;border-radius:12px;background:#F4F8FC;font-family:Segoe UI,Arial,sans-serif;color:#334155;font-size:14px;line-height:21px'><div style='font-size:19px;font-weight:800;color:#0E2A4A'>Meu perfil</div><div style='margin-top:8px'><b>Integrante:</b> registra e atualiza fatos da rotina.<br><b>Liderança:</b> acompanha capacidade, prioriza, seleciona pauta]  +["<div style='padding:16px;border:1px solid #CFE0EF;border-radius:12px;background:#F4F8FC;font-family:Segoe UI,Arial,sans-serif;color:#334155;font-size:14px;line-height:21px'><div style='font-size:19px;font-weight:800;color:#0E2A4A'>Meu perfil</div><div style='margin-top:8px'><b>Integrante:</b> registra e atualiza fatos da rotina (demandas, ocorrências, bloqueios e registro semanal) e atualiza os e]
    replace: -["<div style='padding:16px;border:1px solid #CFE0EF;border-radius:12px;background:#F4F8FC;font-family:Segoe UI,Arial,sans-serif;color:#334155;font-size:14px;line-height:21px'><div style='font-size:19px;font-weight:800;color:#0E2A4A'>Regras de uso</div><div style='margin-top:8px'>Registre somente fatos que melhorem uma decisão de gestão. Não use Demandas como lista de pequenas tarefas pessoais. Em E]  +["<div style='padding:16px;border:1px solid #CFE0EF;border-radius:12px;background:#F4F8FC;font-family:Segoe UI,Arial,sans-serif;color:#334155;font-size:14px;line-height:21px'><div style='font-size:19px;font-weight:800;color:#0E2A4A'>Regras de uso</div><div style='margin-top:8px'>Registre somente fatos que melhorem uma decisão de gestão. Não use Demandas como lista de pequenas tarefas pessoais. Em E]
* NOVA TelaDecisoesEncaminhamentos.TelaDecisoesEncaminhamentos.Fill
* NOVA TelaDecisoesEncaminhamentos.TelaDecisoesEncaminhamentos.LoadingSpinnerColor
* NOVA TelaDecisoesEncaminhamentos.TelaDecisoesEncaminhamentos.OnVisible
* NOVA TelaDemandas.DataCardKey1.TabIndex
* NOVA TelaDemandas.DataCardKey12.TabIndex
* NOVA TelaDemandas.DataCardKey2.TabIndex
* NOVA TelaDemandas.DataCardKey3.TabIndex
* NOVA TelaDemandas.DataCardKey5.TabIndex
* NOVA TelaDemandas.DataCardKeyCriticidade.TabIndex
* NOVA TelaDemandas.ErrorMessage1.TabIndex
* NOVA TelaDemandas.ErrorMessage12.TabIndex
* NOVA TelaDemandas.ErrorMessage2.TabIndex
* NOVA TelaDemandas.ErrorMessage3.TabIndex
* NOVA TelaDemandas.ErrorMessage5.TabIndex
* NOVA TelaDemandas.ErrorMessageCriticidade.TabIndex
* NOVA TelaDemandas.StarVisible1.TabIndex
* NOVA TelaDemandas.StarVisible12.TabIndex
* NOVA TelaDemandas.StarVisible2.TabIndex
* NOVA TelaDemandas.StarVisible3.TabIndex
* NOVA TelaDemandas.StarVisible5.TabIndex
* NOVA TelaDemandas.StarVisibleCriticidade.TabIndex
* ALTERADA TelaDemandas.btnMenuItemDemandas.OnSelect
    insert: -[]  +["Decisoes" , Navigate ( TelaDecisoesEncaminhamentos , ScreenTransition . Fade ) ,]
* NOVA TelaDemandas.btnNovaDemanda.DisplayMode
* ALTERADA TelaDemandas.btnNovaDemanda.OnSelect
    insert: -[]  +[If ( ! varUsuarioCadastrado , Notify ( "Somente integrantes cadastrados podem registrar demandas." , NotificationType . Warning ) ,]
    insert: -[]  +[)]
* ALTERADA TelaDemandas.btnSalvarDemanda.OnSelect
    insert: -[]  +[= / / = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =]
    insert: -[]  +[! ( ( varModoDemanda = "Nova" & & varUsuarioCadastrado ) | | ( varModoDemanda = "Editar" & & varPodeEditarDemanda ) ) , Notify ( "Você não possui permissão para salvar esta demanda." , NotificationType . Error ) , ! frmDemanda . Valid , Notify ( "Revise os campos obrigatórios da demanda." , NotificationType . Warning ) ,]
    insert: -[]  +[varErroSalvarIPD , false ) ; Set (]
    replace: -[SubmitForm]  +[Set ( varDataHoje , Today ( ) ) ; With ( { vImpacto : Switch ( drpConsequencia . Selected . Value , "Não afeta a rotina no curto prazo" , 1 , "Gera retrabalho ou dificuldade operacional" , 2 , "Afeta entrega, resultado ou rotina do laboratório" , 3 , "Risco de parada, auditoria, segurança ou não conformidade" , 4 , Blank ( ) ) , vEsforco : Switch ( drpDedicacao . Selected . Value , "Resolvo em pou]
    insert: -[]  +[; Set ( varDemandaSelecionada , Blank (]
    insert: -[]  +[) ; Set ( varDataLimiteAnterior , Blank ( ) ) ; UpdateContext ( { varMostrarPainelDemanda : false , varModoDemanda : "" , varPodeEditarDemanda : false } ) ; Set ( varCarregandoDemandas , false ) ; Notify ( If ( varFalhaRecargaDemandas , "A demanda foi salva, mas a lista não pôde ser atualizada agora. Reabra a tela para ver os dados mais recentes." , If ( varDemandaSalva . Status . Value = "Conclui]
* REMOVIDA TelaDemandas.frmDemanda.OnFailure
* REMOVIDA TelaDemandas.frmDemanda.OnSuccess
* ALTERADA TelaDemandas.htmlItemMenuDemandas.HtmlText
    replace: -["Equipamentos<br>Críticos"]  +["Ocorrências<br>Operacionais"]
    insert: -[]  +[, "Decisoes" , "Decisões e<br>Encaminhamentos"]
* NOVA TelaDemandas.lblPainelDemandaTitulo.TabIndex
* NOVA TelaDemandas.lblPergunta1.TabIndex
* NOVA TelaDemandas.lblPergunta2.TabIndex
* NOVA TelaDemandas.lblPergunta3.TabIndex
* NOVA TelaDemandas.lblPerguntaRisco.TabIndex
* ALTERADA TelaEquipamentos.TelaEquipamentos.OnVisible
    insert: -[]  +[; Set ( varAbaOcorrencias , Coalesce ( varAbaOcorrenciasInicial , "Equipamentos" ) ) ; Set ( varAbaOcorrenciasInicial , Blank ( ) ) ; Set ( varMostrarPainelBloqueio , false ) ; Set ( varBloqueioSelecionado , Blank ( ) ) ; Set ( varModoBloqueio , "" ) ; Set ( varPodeEditarBloqueio , false ) ; Set ( varSalvandoBloqueio , false ) ; Set ( varFalhaSalvarBloqueio , false ) ; Set ( varErroSalvarBloqueio ]
* ALTERADA TelaEquipamentos.btnMenuEquipamentos.OnSelect
    insert: -[]  +["Decisoes" , Navigate ( TelaDecisoesEncaminhamentos , ScreenTransition . Fade ) ,]
* NOVA TelaEquipamentos.cntAreaListaEquipamentos.Visible
* NOVA TelaEquipamentos.cntFiltrosEquipamentos.Visible
* ALTERADA TelaEquipamentos.htmlAjudaEquipamentos.HtmlText
    replace: -["<div style='width:100%;box-sizing:border-box;padding:2px 4px 18px 2px;font-family:Segoe UI,Arial,sans-serif;color:#334155;font-size:14px;line-height:21px'> <div style='padding:14px 15px;border:1px solid #CFE0EF;border-radius:12px;background:#F4F8FC'><div style='font-size:17px;font-weight:800;color:#0E2A4A'>Objetivo da tela</div><div style='margin-top:5px'>Registrar e acompanhar somente ocorrência]  +["<div style='width:100%;box-sizing:border-box;padding:2px 4px 18px 2px;font-family:Segoe UI,Arial,sans-serif;color:#334155;font-size:14px;line-height:21px'> <div style='padding:14px 15px;border:1px solid #CFE0EF;border-radius:12px;background:#F4F8FC'><div style='font-size:17px;font-weight:800;color:#0E2A4A'>Objetivo da tela</div><div style='margin-top:5px'>Registrar e acompanhar somente ocorrência]
* ALTERADA TelaEquipamentos.htmlCabecalhoEquipamentos.Visible
    insert: -[]  +[varAbaOcorrencias < > "Bloqueios" & & (]
    insert: -[]  +[)]
* ALTERADA TelaEquipamentos.htmlEstadoEquipamentos.Visible
    insert: -[]  +[varAbaOcorrencias < > "Bloqueios" & & (]
    insert: -[]  +[)]
* ALTERADA TelaEquipamentos.htmlKpisEquipamentos.Visible
    insert: -[]  +[varAbaOcorrencias < > "Bloqueios" & & (]
    insert: -[]  +[)]
* ALTERADA TelaEquipamentos.htmlMenuEquipamentos.HtmlText
    replace: -["Equipamentos<br>Críticos"]  +["Ocorrências<br>Operacionais"]
    insert: -[]  +[, "Decisoes" , "Decisões e<br>Encaminhamentos"]
* ALTERADA TelaEquipamentos.htmlTituloAjudaEquipamentos.HtmlText
    replace: -["<div style=' width:100%; height:100%; box-sizing:border-box; display:flex; flex-direction:column; justify-content:center; overflow:hidden; font-family:Segoe UI,Arial,sans-serif; '> <div style=' color:#0E2A4A; font-size:20px; font-weight:800; line-height:28px; letter-spacing:-0.3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; '> Como utilizar a tela de Equipamentos Críticos </div>]  +["<div style=' width:100%; height:100%; box-sizing:border-box; display:flex; flex-direction:column; justify-content:center; overflow:hidden; font-family:Segoe UI,Arial,sans-serif; '> <div style=' color:#0E2A4A; font-size:20px; font-weight:800; line-height:28px; letter-spacing:-0.3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; '> Como utilizar a tela de Ocorrências Operacionais </d]
* ALTERADA TelaEquipamentos.htmlTituloEquipamentos.HtmlText
    replace: -["<div style='width:100%;height:100%;box-sizing:border-box;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;color:#0E2A4A'><div style='font-size:30px;line-height:36px;font-weight:800'>Equipamentos Críticos</div><div style='font-size:16px;line-height:22px;color:#657384'>Ocorrências que impactam a rotina, previsões de retorno e tratativas em andamento.</div></div>"]  +["<div style='width:100%;height:100%;box-sizing:border-box;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;color:#0E2A4A'><div style='font-size:30px;line-height:36px;font-weight:800'>Ocorrências Operacionais</div><div style='font-size:16px;line-height:22px;color:#657384'>Equipamentos com ocorrência e bloqueios que impedem a rotina, com responsáveis, previsões e tratativas.</div></div>"]
* ALTERADA TelaEquipamentos.icoAjudaEquipamentos.AccessibleLabel
    replace: -["Entenda como utilizar a tela Equipamentos Críticos"]  +["Entenda como utilizar a tela Ocorrências Operacionais"]
* ALTERADA TelaEquipamentos.icoAjudaEquipamentos.Tooltip
    replace: -["Como utilizar a tela de Equipamentos Críticos"]  +["Como utilizar a tela de Ocorrências Operacionais"]
* NOVA TelaEquipamentos.lblAreaEquipamento.TabIndex
* NOVA TelaEquipamentos.lblAtivoEquipamento.TabIndex
* NOVA TelaEquipamentos.lblCriticidadeEquipamento.TabIndex
* NOVA TelaEquipamentos.lblDataEncerramentoEquipamento.TabIndex
* NOVA TelaEquipamentos.lblDescricaoEquipamento.TabIndex
* NOVA TelaEquipamentos.lblImpactoEquipamento.TabIndex
* NOVA TelaEquipamentos.lblInicioOcorrenciaEquipamento.TabIndex
* NOVA TelaEquipamentos.lblNomeEquipamento.TabIndex
* NOVA TelaEquipamentos.lblOcorrenciaEquipamento.TabIndex
* NOVA TelaEquipamentos.lblPrevisaoRetornoEquipamento.TabIndex
* NOVA TelaEquipamentos.lblResponsavelEquipamento.TabIndex
* NOVA TelaEquipamentos.lblStatusEquipamento.TabIndex
* NOVA TelaEquipamentos.lblTipoOcorrenciaEquipamento.TabIndex
* NOVA TelaEquipamentos.lblTratativaEquipamento.TabIndex
* ALTERADA TelaRadarSemanal.TelaRadarSemanal.OnVisible
    insert: -[]  +[, false ) ; Set ( varEnviandoPautaRotina]
* REMOVIDA TelaRadarSemanal.btnAbaMelhoriaRotina.BorderColor
* REMOVIDA TelaRadarSemanal.btnAbaMelhoriaRotina.Color
* REMOVIDA TelaRadarSemanal.btnAbaMelhoriaRotina.Fill
* REMOVIDA TelaRadarSemanal.btnAbaMelhoriaRotina.Height
* REMOVIDA TelaRadarSemanal.btnAbaMelhoriaRotina.OnSelect
* REMOVIDA TelaRadarSemanal.btnAbaMelhoriaRotina.Text
* REMOVIDA TelaRadarSemanal.btnAbaMelhoriaRotina.Visible
* REMOVIDA TelaRadarSemanal.btnAbaMelhoriaRotina.Width
* ALTERADA TelaRadarSemanal.btnAdicionarHighlight.DisplayMode
    delete: -[) , "MelhoriaIdentificada" , CountRows ( colMelhoriasSemana]  +[]
* ALTERADA TelaRadarSemanal.btnAdicionarHighlight.OnSelect
    delete: -["MelhoriaIdentificada" , If ( CountRows ( colMelhoriasSemana ) < 6 , Collect ( colMelhoriasSemana , { IDLocal : GUID ( ) , Ordem : CountRows ( colMelhoriasSemana ) + 1 , Texto : "" , Obrigatorio : false , Salvo : false } ) ) ,]  +[]
* ALTERADA TelaRadarSemanal.btnAdicionarHighlight.Text
    delete: -[) , "MelhoriaIdentificada" , CountRows ( colMelhoriasSemana]  +[]
    delete: -["MelhoriaIdentificada" , "melhoria" ,]  +[]
* ALTERADA TelaRadarSemanal.btnCancelarRegistroSemanal.OnSelect
    delete: -[colMelhoriasSemana ) ; Clear (]  +[]
* ALTERADA TelaRadarSemanal.btnEnviarRotina.DisplayMode
    delete: -[colMelhoriasSemana , ! IsBlank ( Trim ( Texto ) ) & & ! Salvo ) + CountIf (]  +[]
* ALTERADA TelaRadarSemanal.btnEnviarRotina.OnSelect
    insert: -[]  +[, NotificationType . Warning ) , With ( { vEmailAutor : Lower ( User ( ) . Email ) } , CountIf ( colRegistrosRotinaBase , Upper ( Trim ( Coalesce ( SemanaReferencia , "" ) ) ) = vSemana & & Lower ( Coalesce ( CriadoPor , "" ) ) = vEmailAutor & & TipoRegistro . Value = "Highlight" ) + CountIf ( colHighlightsSemana , ! IsBlank ( Trim ( Texto ) ) & & ! Salvo ) > 6 | | CountIf ( colRegistrosRotinaBase]
    delete: -[colMelhoriasSemana , false & & ! IsBlank ( Trim ( Texto ) ) & & ! Salvo ) As item , Collect ( colResultadoEnvioRotina , { Categoria : "MelhoriaIdentificada" , IDLocal : item . IDLocal , Sucesso : IfError ( ! IsBlank ( Patch ( Radar_RegistrosRotina , Defaults ( Radar_RegistrosRotina ) , { Título : Left ( Trim ( item . Texto ) , 120 ) , Descricao : Trim ( item . Texto ) , TipoRegistro : { Value : "M]  +[]
    delete: -[, IDLocal = resultado . IDLocal ) , { Salvo : true } ) ) ; ForAll ( Filter ( colResultadoEnvioRotina , Categoria = "MelhoriaIdentificada" & & Sucesso = true ) As resultado , Patch ( colMelhoriasSemana , LookUp ( colMelhoriasSemana]  +[]
    delete: -[colMelhoriasSemana , ! IsBlank ( Trim ( Texto ) ) & & ! Salvo ) + CountIf (]  +[]
    delete: -[colMelhoriasSemana ) ; Clear (]  +[]
* ALTERADA TelaRadarSemanal.btnEnviarRotina.Text
    delete: -[colMelhoriasSemana , Salvo ) + CountIf (]  +[]
* ALTERADA TelaRadarSemanal.btnFecharPainelRotina.OnSelect
    delete: -[colMelhoriasSemana ) ; Clear (]  +[]
* ALTERADA TelaRadarSemanal.btnMenuRotina.OnSelect
    insert: -[]  +["Decisoes" , Navigate ( TelaDecisoesEncaminhamentos , ScreenTransition . Fade ) ,]
* NOVA TelaRadarSemanal.btnNovoRegistroRotina.DisplayMode
* ALTERADA TelaRadarSemanal.btnNovoRegistroRotina.OnSelect
    insert: -[]  +[If ( ! varUsuarioCadastrado , Notify ( "Somente integrantes cadastrados podem registrar a rotina semanal." , NotificationType . Warning ) ,]
    delete: -[ClearCollect ( colMelhoriasSemana , { IDLocal : GUID ( ) , Ordem : 1 , Texto : "" , Obrigatorio : false , Salvo : false } ) ;]  +[]
    insert: -[]  +[)]
* ALTERADA TelaRadarSemanal.galHighlightsSemana.AccessibleLabel
    delete: -["MelhoriaIdentificada" , "Lista de melhorias identificadas" ,]  +[]
* ALTERADA TelaRadarSemanal.galHighlightsSemana.Items
    delete: -["MelhoriaIdentificada" , SortByColumns ( colMelhoriasSemana , "Ordem" , SortOrder . Ascending ) ,]  +[]
* NOVA TelaRadarSemanal.galHighlightsSemana.TabIndex
* ALTERADA TelaRadarSemanal.htmlCabecalhoHighlights.HtmlText
    delete: -[, "MelhoriaIdentificada" , "Melhorias identificadas"]  +[]
    delete: -["MelhoriaIdentificada" , "Registre oportunidades de melhoria percebidas durante a rotina." ,]  +[]
    delete: -[, "MelhoriaIdentificada" , "#1C5582"]  +[]
    delete: -["MelhoriaIdentificada" , CountIf ( colMelhoriasSemana , ! IsBlank ( Trim ( Texto ) ) ) ,]  +[]
    replace: -[varCategoriaCadastroRotina < > "MelhoriaIdentificada"]  +[true]
* ALTERADA TelaRadarSemanal.htmlKpisRotina.HtmlText
    delete: -[vM : CountRows ( Filter ( colRegistrosRotinaTela , Upper ( Trim ( Coalesce ( SemanaReferencia , "" ) ) ) = vSemana & & TipoRegistro . Value = "MelhoriaIdentificada" ) ) ,]  +[]
* ALTERADA TelaRadarSemanal.htmlMenuRotina.HtmlText
    replace: -["Equipamentos<br>Críticos"]  +["Ocorrências<br>Operacionais"]
    insert: -[]  +[, "Decisoes" , "Decisões e<br>Encaminhamentos"]
* NOVA TelaRadarSemanal.lblAutorCuradoriaRotina.TabIndex
* NOVA TelaRadarSemanal.lblDataCuradoriaRotina.TabIndex
* ALTERADA TelaRadarSemanal.lblNumeroHighlight.Color
    delete: -["MelhoriaIdentificada" , RGBA ( 28 , 85 , 130 , 1 ) ,]  +[]
* NOVA TelaRadarSemanal.lblNumeroHighlight.TabIndex
* NOVA TelaRadarSemanal.lblTextoCuradoriaRotina.TabIndex
* NOVA TelaRadarSemanal.lblTipoCuradoriaRotina.TabIndex
* NOVA TelaRadarSemanal.togCuradoriaRotina.AccessibleLabel
* ALTERADA TelaRadarSemanal.txtItemHighlight.AccessibleLabel
    delete: -[, "MelhoriaIdentificada" , "Melhoria identificada "]  +[]
* ALTERADA TelaRadarSemanal.txtItemHighlight.OnChange
    delete: -["MelhoriaIdentificada" , Patch ( colMelhoriasSemana , LookUp ( colMelhoriasSemana , IDLocal = ThisItem . IDLocal ) , { Texto : Trim ( Self . Text ) } ) ,]  +[]

```