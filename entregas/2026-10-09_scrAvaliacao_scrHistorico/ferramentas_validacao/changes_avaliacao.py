"""Alterações da tela scrAvaliacao — Contexto da avaliação + Base documental no topo."""
from fx import esc, s, box, div

LBL = 'font-size:8.5pt;line-height:1.2;color:#627083;font-weight:700;letter-spacing:.02em;text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'
VAL1 = 'font-size:11pt;line-height:1.25;color:#1D2A3A;font-weight:600;text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'
SUB = 'font-size:8.5pt;line-height:1.25;color:#6B7A8D;font-weight:400;text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'

# geometria da faixa de identificação (dentro de conIdAva)
CWI = '(Parent.Width - 190)'
COLS = {  # coluna: (fração X, fração largura)
    0: ('0', '0.24'),      # Pessoa
    1: ('0.24', '0.06'),   # Área
    2: ('0.30', '0.25'),   # Módulo
    3: ('0.55', '0.15'),   # Tipo
    4: ('0.70', '0.30'),   # Avaliador
}
Y_R, Y_V, Y_S = '34', '50', '70'
BAND = '98'  # início da faixa Base documental / Método dentro do card

# expressões reutilizadas
N_CRIT_NA = 'CountRows(Filter(colCritAva, PermiteNA)) > 0'
BW = 'Min(124, (Parent.TemplateWidth - 96) / 5)'
NB = f'If({N_CRIT_NA}, 3, 2)'


def btn_x(k):
    return f'Parent.TemplateWidth - 18 - ({NB} - {k}) * ({BW} + 8)'


EDITAVEL = '(locAv.Estado = "PREENCHIMENTO" && locAv.Avaliador = varUsuario.Codigo)'
RX = '260 + (Parent.Width - 284) * 0.66 + 16'
RW = '(Parent.Width - 284) * 0.34 - 16'

DOC_ROW_H = ('If(Max(colDocsAva, Len(Coalesce(Titulo, Codigo))) > (({W} - 36) / 2 - 36) / 6.2, 82, 66)')

PEND_HTML = (
    'With({_n: CountRows(colCritAva), '
    '_sem: CountRows(Filter(colCritAva, IsBlank(Resposta))), '
    '_na: CountRows(Filter(colCritAva, Resposta = "Não atendeu" && IsBlank(Trim(Coalesce(Comentario, ""))))), '
    '_naj: CountRows(Filter(colCritAva, Resposta = "N/A" && IsBlank(Trim(Coalesce(Comentario, ""))))), '
    '_soNA: CountRows(Filter(colCritAva, Resposta = "Atendeu")) = 0 && CountRows(Filter(colCritAva, Resposta = "Não atendeu")) = 0, '
    '_par: Len(Trim(txtParecerAva.Text)), '
    '_com: CountRows(Filter(colCritAva, !IsBlank(Resposta) && IsBlank(Trim(Coalesce(Comentario, "")))))}, '
    'With({_k: If(_n = 0, 0, _sem > 0, 1, _na > 0, 2, _naj > 0, 3, _soNA, 4, _par < 30, 5, _com > 0, 6, 7)}, '
    '"<div style=\'margin-top:3px;font-size:9pt;line-height:1.25;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:" & '
    'Switch(_k, 6, "#627083", 7, "#2E7D32", "#B54708") & ";\'>" & ' + esc(
        'Switch(_k, '
        '0, "Nenhum critério disponível para esta avaliação", '
        '1, If(_sem = 1, "Falta 1 critério para responder", "Faltam " & _sem & " critérios para responder"), '
        '2, If(_na = 1, "Há 1 critério Não atendeu aguardando comentário", "Há " & _na & " critérios Não atendeu aguardando comentário"), '
        '3, If(_naj = 1, "Há 1 critério N/A sem justificativa", "Há " & _naj & " critérios N/A sem justificativa"), '
        '4, "Não é possível concluir com todos os critérios como N/A", '
        '5, "Parecer técnico pendente · " & _par & " de 30 caracteres", '
        '6, If(_com = 1, "1 comentário pendente", _com & " comentários pendentes"), '
        '"Pronto para concluir")') + ' & "</div>"))'
)

SALVAR_OLD = 'Notify("Rascunho salvo com sucesso.", NotificationType.Success),'
SALVAR_NEW = ('With({_comentPend: CountRows(Filter(colCritAva, !IsBlank(Resposta) && IsBlank(Trim(Coalesce(Comentario, "")))))}, '
              'If(_comentPend = 0, Notify("Rascunho salvo com sucesso.", NotificationType.Success), '
              'Notify("Rascunho salvo. Aguardando comentário em " & _comentPend & If(_comentPend = 1, " critério.", " critérios."), NotificationType.Warning))),')


def apply(sc):
    # ---------------------------------------------------- card Contexto da avaliação
    sc.set('conIdAva', 'Height', BAND + ' + Max(conDocAva.Height, conMetAva.Height) + 10')
    sc.clone('lblIdR0Ava', 'lblCtxTitAva', 'conIdAva', {
        'HtmlText': box(div('font-size:12.5pt;line-height:1.2;color:#0E2A4A;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                            esc(s('Contexto da avaliação'))), 'display:flex;align-items:center;'),
        'Color': 'RGBA(14, 42, 74, 1)', 'Size': '12.5',
        'X': '18', 'Y': '8', 'Width': 'Parent.Width - 36', 'Height': '22',
    }, zindex=21)
    # divisor horizontal: retângulo novo baseado em recDocLinhaAva
    sc.clone('recDocLinhaAva', 'recCtxLinhaAva', 'conIdAva', {
        'X': '18', 'Y': '90', 'Width': 'Parent.Width - 36', 'Height': '1',
        'Fill': 'RGBA(230, 236, 243, 1)',
    }, zindex=22)

    for k, (fx, fw) in COLS.items():
        x = '18' if fx == '0' else f'18 + {CWI} * {fx}'
        w = f'{CWI} * {fw} - 16'
        for kind, y in (('R', Y_R), ('V', Y_V), ('S', Y_S)):
            sc.setmany(f'lblId{kind}{k}Ava', X=x, Width=w, Y=y)
    # rótulos das colunas: estilo único
    for k, txt in ((0, 'PESSOA'), (1, 'ÁREA'), (2, 'MÓDULO'), (3, 'TIPO'), (4, 'AVALIADOR')):
        sc.set(f'lblIdR{k}Ava', 'HtmlText', box(div(LBL, esc(s(txt))), 'display:flex;align-items:center;'))
    sc.set('lblIdR6Ava', 'HtmlText', box(div(LBL, esc(s('ESTADO'))), 'display:flex;align-items:center;'))
    sc.setmany('lblIdR6Ava', Y=Y_R, X='Parent.Width - 150', Width='132')
    sc.setmany('bdgIdEstAva', Y='52', X='Parent.Width - 150', Width='132',
               Tooltip='If(IsBlank(locAv.Tentativa), "", "Tentativa " & locAv.Tentativa)')

    one = 'font-size:10.5pt;line-height:1.25;color:#1D2A3A;font-weight:600;text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'
    two = 'font-size:10.5pt;line-height:1.25;color:#1D2A3A;font-weight:600;text-align:left;white-space:normal;overflow:hidden;max-height:2.5em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;'
    sc.set('lblIdV0Ava', 'HtmlText', box(div(one, esc('Coalesce(locAv.PessoaNomeSnap, LookUp(colPessoas, Codigo = locAv.Pessoa).Nome)')), 'display:flex;align-items:center;'))
    sc.set('lblIdV1Ava', 'HtmlText', box(div(one, esc('locAv.Area')), 'display:flex;align-items:center;'))
    sc.set('lblIdV3Ava', 'HtmlText', box(div(one, esc('Switch(locAv.Tipo, "QUALIFICACAO", "Qualificação", "REQUALIFICACAO", "Requalificação", "EXTRAORDINARIA", "Extraordinária", locAv.Tipo)')), 'display:flex;align-items:center;'))
    fits = 'Len(Coalesce(locAv.AvaliadorNome, "")) * 7.6 <= lblIdV4Ava.Width'
    sc.set('lblIdV4Ava', 'Height', 'If(' + fits.replace('lblIdV4Ava.Width', 'Self.Width') + ', 20, 36)')
    sc.set('lblIdV4Ava', 'HtmlText', box(div(two, esc('locAv.AvaliadorNome')), 'display:flex;align-items:flex-start;'))
    sc.set('lblIdS4Ava', 'Visible', fits)
    # Módulo: nome amigável em destaque, até 2 linhas; sem "Módulo 14.1"
    sc.set('lblIdV2Ava', 'Height', '36')
    sc.set('lblIdV2Ava', 'HtmlText', box(div(
        'font-size:10.5pt;line-height:1.25;color:#1D2A3A;font-weight:600;text-align:left;white-space:normal;overflow:hidden;max-height:2.5em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;',
        esc('If(" — " in Coalesce(locAv.ModuloNome, ""), First(Split(locAv.ModuloNome, " — ")).Value, Coalesce(locAv.ModuloNome, "—"))')),
        'display:flex;align-items:flex-start;'))
    sc.set('lblIdS2Ava', 'Visible', 'false')
    sc.set('lblIdS2Ava', 'Tooltip', '""')

    # Ciclo sai do resumo visual (dados internos preservados)
    for n in ('lblIdR5Ava', 'lblIdV5Ava', 'lblIdS5Ava'):
        sc.set(n, 'Visible', 'false')

    # ---------------------------------------------------- Base documental (topo)
    sc.setmany('conDocAva',
               X='conIdAva.X', Y='conIdAva.Y + ' + BAND, Width='conIdAva.Width * 0.66',
               Height='48 + If(CountRows(colDocsAva) = 0, 34, ' + DOC_ROW_H.format(W='Self.Width') +
                      ' * Min(RoundUp(CountRows(colDocsAva) / 2, 0), 2))',
               BorderThickness='0', Fill='RGBA(0, 0, 0, 0)')
    sc.setmany('lblDocTitAva', X='18', Y='0', Width='Parent.Width * 0.64 - 18', Height='40',
               HtmlText=box(div('font-size:12pt;line-height:1.25;color:#0E2A4A;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                esc(s('Base documental'))) + ' & ' +
                            div('margin-top:2px;font-size:9pt;line-height:1.25;color:#627083;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                esc(s('Documentos utilizados como referência para esta avaliação.'))),
                            'display:flex;flex-direction:column;justify-content:center;'))
    sc.setmany('lblDocAuxAva', X='Parent.Width * 0.64', Y='4', Width='Parent.Width * 0.36 - 20', Height='22',
               Visible='CountRows(colDocsAva) > 0',
               HtmlText=box(div('font-size:9pt;line-height:1.25;color:#1C5582;font-weight:600;text-align:right;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                esc('If(CountRows(colDocsAva) = 1, "1 documento aplicável", CountRows(colDocsAva) & " documentos aplicáveis")')),
                            'display:flex;align-items:center;justify-content:flex-end;'))
    # divisor vertical entre Base documental e Método
    sc.setmany('recDocLinhaAva', X='Parent.Width - 1', Y='4', Width='1', Height='Parent.Height - 8')
    sc.setmany('galDocAva', X='18', Y='44', Width='Parent.Width - 36', Height='Parent.Height - 46',
               WrapCount='2', TemplateSize=DOC_ROW_H.format(W='Parent.Width'))
    sc.setmany('htmlDocCardAva', X='0', Y='0', Width='Parent.TemplateWidth - 12', Height='Parent.TemplateHeight - 8',
               HtmlText='"<div style=\'box-sizing:border-box;width:100%;height:" & Text(Max(Self.Height - 2, 0), "0", "en-US") & "px;background:#F7F9FC;border:1px solid #E6ECF3;border-radius:8px;\'></div>"')
    sc.setmany('lblDocAva', X='12', Y='5', Width='Parent.TemplateWidth - 36', Height='Parent.TemplateHeight - 33',
               Tooltip='ThisItem.Codigo & If(IsBlank(ThisItem.Titulo), "", " — " & ThisItem.Titulo)',
               HtmlText=box(div('font-size:9pt;line-height:1.25;color:#0E2A4A;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                esc('Coalesce(ThisItem.Codigo, ThisItem.Titulo)')) +
                            ' & If(IsBlank(ThisItem.Titulo) || IsBlank(ThisItem.Codigo), "", ' +
                            div('font-size:10pt;line-height:1.25;color:#344054;font-weight:400;white-space:normal;overflow:hidden;max-height:2.5em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;',
                                esc('ThisItem.Titulo')) + ')'))
    sc.setmany('lblDocSubAva', X='12', Y='Parent.TemplateHeight - 28', Width='Parent.TemplateWidth - 36', Height='16',
               HtmlText=box(div('font-size:8.5pt;line-height:1.25;color:#6B7A8D;font-weight:400;text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                esc('With({_v: Trim(Coalesce(ThisItem.Versao, "")), _e: Trim(Coalesce(ThisItem.Expiracao, ""))}, '
                                    'With({_d: If(IsMatch(_e, "\\d{4}-\\d{2}-\\d{2}.*"), Mid(_e, 9, 2) & "/" & Mid(_e, 6, 2) & "/" & Left(_e, 4), _e)}, '
                                    'If(!IsBlank(_v) && !IsBlank(_e), "Versão " & _v & " · validade " & _d, !IsBlank(_v), "Versão " & _v, !IsBlank(_e), "Validade " & _d, "")))')),
                            'display:flex;align-items:center;'))
    sc.setmany('lblDocVazioAva', X='18', Y='46', Width='Parent.Width - 36',
               HtmlText=box(div('font-size:10pt;line-height:1.25;color:#627083;font-weight:400;text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                esc(s('Nenhum documento de referência disponível.'))), 'display:flex;align-items:center;'))

    # ---------------------------------------------------- Método de avaliação (topo)
    sc.setmany('conMetAva',
               X='conIdAva.X + conDocAva.Width', Y='conDocAva.Y', Width='conIdAva.Width - conDocAva.Width',
               Height='34 + 19 * Min(Max(RoundUp(Len(Coalesce(locAv.MetodoSnap, "—")) / Max(20, (Self.Width - 40) / 6.6), 0), 1), 6) + 8',
               BorderThickness='0', Fill='RGBA(0, 0, 0, 0)')
    sc.setmany('lblMetTitAva', X='20', Y='0', Width='Parent.Width - 40', Height='24')
    sc.setmany('lblMetAva', X='20', Y='28', Width='Parent.Width - 40', Height='Parent.Height - 30')

    # ---------------------------------------------------- banner somente leitura
    sc.set('lblBannerAva', 'Y', 'conIdAva.Y + conIdAva.Height + 12')

    # ---------------------------------------------------- corpo: critérios (esq.) + parecer (dir.)
    body_y = 'conIdAva.Y + conIdAva.Height + 16 + If(lblBannerAva.Visible, lblBannerAva.Height + 12, 0)'
    sc.setmany('conCritAva', Y=body_y, Height='Parent.Height - Self.Y - 20', Width='(Parent.Width - 284) * 0.66')
    sc.setmany('lblCritTitAva', Y='6', Height='56')
    sc.setmany('lblCritAuxAva', Y='6', Height='56')
    sc.set('recCritLinhaAva', 'Y', '66')
    sc.setmany('galCritAva', Y='67', Height='Parent.Height - 68',
               TemplateSize='188 + 19 * Min(Max(RoundUp(Max(colCritAva, Len(Descricao)) / Max(30, (Self.Width - 96) / 7.2), 0), 1), 20)')
    sc.set('htmlCardCritAva', 'HtmlText',
           '"<div style=\'box-sizing:border-box;width:100%;height:" & Text(Max(Self.Height - 2, 0), "0", "en-US") & "px;background:#FFFFFF;border-radius:10px;border:1px solid #E1E8F0;box-shadow:inset 3px 0 0 " & '
           'Switch(ThisItem.Resposta, "Atendeu", "#2E7D32", "Não atendeu", "#B91C1C", "N/A", "#98A2B3", "transparent") & ";\'></div>"')
    sc.setmany('lblCritIdAva', Y='14', Height='36', Width=f'Parent.TemplateWidth - 18 - {NB} * ({BW} + 8) - 70',
               HtmlText=box(div('font-size:11pt;line-height:1.25;color:#0E2A4A;font-weight:700;text-align:left;white-space:normal;overflow:hidden;max-height:2.5em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;',
                                esc('Switch(ThisItem.Dimensao, "preparacao_execucao", "Preparação e execução", "equipamentos_materiais_controles", "Equipamentos, materiais e controles", "pontos_criticos_validade_anomalias", "Pontos críticos, validade e anomalias", "resultado_interpretacao", "Resultado e interpretação", "registros_rastreabilidade", "Registros e rastreabilidade", "seguranca", "Segurança na execução", "preparacao", "Preparação", "execucao", "Execução", "pontos_criticos_anomalias", "Pontos críticos e anomalias", Substitute(ThisItem.Dimensao, "_", " "))')),
                            'display:flex;align-items:center;'))
    sc.set('htmlNumCritAva', 'Y', '18')
    sc.setmany('lblCritDescAva', Y='54', Height='Parent.TemplateHeight - 180')
    for k, n in enumerate(('btnAtAva', 'btnNaoAva', 'btnNaAva')):
        sc.setmany(n, X=btn_x(k), Y='16', Width=BW, Height='32')
    sc.set('lblComRotAva', 'Y', 'Parent.TemplateHeight - 120')
    sc.setmany('txtComAva', Y='Parent.TemplateHeight - 100', Height='38')
    sc.set('lblCritNAAva', 'Y', 'Parent.TemplateHeight - 60')
    sc.set('lblCritFonteAva', 'Y', 'Parent.TemplateHeight - 44')

    # coluna direita: Parecer é o único card permanente
    sc.setmany('conParAva', X=RX, Width=RW, Y='conCritAva.Y',
               Height='Parent.Height - 20 - If(conBarraAva.Visible, conBarraAva.Height + 12, 0) - Self.Y')
    sc.set('txtParecerAva', 'HintText', s('Registre aqui o parecer técnico sobre o resultado da avaliação.'))
    k = '((Parent.Height - 104) * 0.56)'
    sc.setmany('lblParTitAva', Y='4', Height='28')
    sc.set('lblParRotAva', 'Y', '32')
    sc.setmany('txtParecerAva', Y='50', Height=k)
    sc.set('lblParAjAva', 'Y', '52 + ' + k)
    sc.set('lblObsRotAva', 'Y', '72 + ' + k)
    sc.setmany('txtObsAva', Y='92 + ' + k, Height='Parent.Height - (92 + ' + k + ') - 12')

    # ---------------------------------------------------- barra inferior
    wide = 'Parent.Width >= 470'
    sc.setmany('conBarraAva', X=RX, Width=RW, Height='If(Self.Width >= 470, 106, 144)')
    old_res = sc.get('lblResumoAva', 'HtmlText')
    tail = ' & "</div>"'
    assert old_res.endswith(tail)
    # mantém o resumo atual (progresso + resultado) e acrescenta a linha de pendência
    sc.setmany('lblResumoAva', Y='8', Height='50',
               HtmlText=old_res.replace('height:100%;gap:12px;', 'height:30px;gap:12px;', 1)[:-len(tail)] + ' & ' + PEND_HTML + tail)
    sc.setmany('btnSalvarAva', X='16', Y='62', Width=f'If({wide}, (Parent.Width - 48) / 3, (Parent.Width - 40) / 2)')
    sc.setmany('btnCancAva', Y='62', X=f'If({wide}, 24 + (Parent.Width - 48) / 3, 24 + (Parent.Width - 40) / 2)',
               Width=f'If({wide}, (Parent.Width - 48) / 3, (Parent.Width - 40) / 2)')
    sc.setmany('btnConcluirAva', Y=f'If({wide}, 62, 100)', X=f'If({wide}, 32 + 2 * (Parent.Width - 48) / 3, 16)',
               Width=f'If({wide}, (Parent.Width - 48) / 3, Parent.Width - 32)')

    # ---------------------------------------------------- feedback do rascunho (autorizado — itens 38 a 43)
    old = sc.get('btnSalvarAva', 'OnSelect')
    assert old.count(SALVAR_OLD) == 1
    sc.set('btnSalvarAva', 'OnSelect', old.replace(SALVAR_OLD, SALVAR_NEW))
