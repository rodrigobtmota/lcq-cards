"""Alterações da tela scrHistoricoAvaliacoes — lista limpa + painel de detalhe."""
from fx import esc, s, box, div

V = 'LookUp(colAvaliacoes, Uid = locEvento)'

# nome do módulo: normaliza caixa alta só quando for seguro (sem dígitos nem siglas curtas)
CONECTORES = '["e", "de", "da", "do", "das", "dos", "em", "a", "o", "com", "por", "na", "no", "para"]'


def norm_mod(x):
    return (f'With({{_m: Trim(Coalesce({x}, ""))}}, If(!IsBlank(_m) && _m = Upper(_m) && _m <> Lower(_m) && !IsMatch(_m, ".*\\d.*") && '
            f'CountRows(Filter(Split(_m, " "), Len(Value) > 0 && Len(Value) <= 3 && !(Lower(Value) in {CONECTORES}))) = 0, '
            f'With({{_r: Concat(Split(Lower(_m), " ") As _w, If(_w.Value in {CONECTORES}, _w.Value, Proper(_w.Value)), " ")}}, Upper(Left(_r, 1)) & Mid(_r, 2)), _m))')


DIM = ('Switch({d}, "preparacao_execucao", "Preparação e execução", "equipamentos_materiais_controles", "Equipamentos, materiais e controles", '
       '"pontos_criticos_validade_anomalias", "Pontos críticos, validade e anomalias", "resultado_interpretacao", "Resultado e interpretação", '
       '"registros_rastreabilidade", "Registros e rastreabilidade", "seguranca", "Segurança na execução", "preparacao", "Preparação", '
       '"execucao", "Execução", "pontos_criticos_anomalias", "Pontos críticos e anomalias", "", "Critério", Substitute({d}, "_", " "))')

COLS = [  # (X, Largura) em fração da largura da tabela
    ('0.015', '0.16'),   # Pessoa
    ('0.18', '0.17'),    # Módulo
    ('0.355', '0.04'),   # Área
    ('0.40', '0.095'),   # Tipo
    ('0.50', '0.10'),    # Estado
    ('0.605', '0.075'),  # Resultado
    ('0.685', '0.12'),   # Avaliador
    ('0.81', '0.08'),    # Data
]

ROTULO_FILTRO = ('htmlPessoaRotHis', 'htmlModuloRotHis', 'htmlPeriodoRotHis', 'htmlAreaRotHis',
                 'lblFTipoHis', 'lblFEstadoHis', 'lblFResultadoHis')
BOTOES_L2 = ('btnTodosTiposHis', 'btnFTipoQualificacaoHis', 'btnFTipoRequalificacaoHis', 'btnFTipoExtraordinariaHis',
             'btnTodosEstadosHis', 'btnFEstadoPreenchimentoHis', 'btnFEstadoConcluidaHis', 'btnFEstadoCanceladaHis',
             'btnTodosResultadosHis', 'btnFResultadoAtendeuHis', 'btnFResultadoNaoAtendeuHis', 'btnFResultadoSemHis')

KEY = 'font-size:8.5pt;line-height:1.2;color:#627083;font-weight:700;letter-spacing:.02em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'
VAL = 'font-size:10.5pt;line-height:1.25;color:#1D2A3A;font-weight:600;white-space:normal;overflow:hidden;max-height:2.5em;'


def flex(extra=''):
    return 'display:flex;align-items:center;' + extra


def apply(sc):
    # ---------------------------------------------------- cabeçalho
    sc.replace('lblSubtituloHis', 'HtmlText',
               'Text("Trilha auditável. Eventos exibem o snapshot gravado, não dados atuais.")',
               'Text("Consulte e acompanhe as avaliações técnicas do laboratório.")')

    # ---------------------------------------------------- filtros mais compactos
    sc.setmany('htmlFiltrosHis', Y='152', Height='136')
    for n in ROTULO_FILTRO:
        old = sc.get(n, 'HtmlText')
        assert 'font-size:11pt' in old, n
        sc.set(n, 'HtmlText', old.replace('font-size:11pt', 'font-size:9pt'))
        sc.set(n, 'Height', '18')
    for n in ('htmlPessoaRotHis', 'htmlModuloRotHis', 'htmlPeriodoRotHis', 'htmlAreaRotHis'):
        sc.set(n, 'Y', '164')
    for n in ('lblFTipoHis', 'lblFEstadoHis', 'lblFResultadoHis'):
        sc.set(n, 'Y', '226')
    for n in ('txtBuscaHis', 'txtModHis', 'txtDeHis', 'txtAteHis', 'htmlAteRotHis', 'btnFAPE9His', 'btnFAPP5His', 'btnFAQ4His'):
        sc.setmany(n, Y='184', Height='34')
    for n in ('R3icoFiltrotxtBuscaHis', 'R3icoFiltrotxtModHis', 'R3icoFiltrotxtDeHis', 'R3icoFiltrotxtAteHis'):
        sc.set(n, 'Y', '192')
    for n in BOTOES_L2:
        sc.setmany(n, Y='246', Height='30')

    # ---------------------------------------------------- tabela
    sc.setmany('conTabHis', Y='300', Height='Parent.Height - 318')
    sc.replace('htmlTabelaTituloHis', 'HtmlText', 'Text("Avaliações realizadas")', 'Text("Registros de avaliação")')
    for i, (x, w) in enumerate(COLS, start=1):
        sc.setmany(f'lblH{i}His', X=f'Parent.Width * {x}', Width=f'Parent.Width * {w}')
    sc.setmany('R3htmlColAcaoHis', X='Parent.Width - 102', Width='92')
    sc.replace('R3htmlColAcaoHis', 'HtmlText', 'Text("AÇÕES")', 'Text("AÇÃO")')
    sc.set('galHis', 'TemplateSize', '44')

    def col(n, i, **extra):
        x, w = COLS[i]
        sc.setmany(n, X=f'Parent.TemplateWidth * {x}', Width=f'Parent.TemplateWidth * {w}', **extra)

    # Pessoa: nome + cargo · grupo (dados registrados na avaliação; cadastro atual só como fallback)
    col('lblNomeHis', 0, Y='5', Height='18', Tooltip='ThisItem.Nome')
    col('lblUidHis', 0, Y='23', Height='16', Tooltip='""',
        HtmlText=box(div('font-size:8.5pt;line-height:1.2;color:#6B7A8D;font-weight:400;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                         esc('With({_v: LookUp(colAvaliacoes, Uid = ThisItem.Uid), _p: LookUp(colPessoas, Codigo = ThisItem.Pessoa)}, '
                             'With({_c: Trim(Coalesce(_v.CargoSnap, _p.Cargo)), _g: Trim(Coalesce(_v.GrupoSnap, _p.Grupo))}, '
                             '_c & If(IsBlank(_g), "", If(IsBlank(_c), "", " · ") & "Grupo " & _g)))')), flex()))
    # Módulo: nome amigável (até 2 linhas); código só no tooltip
    col('lblModHis', 1, Y='0', Height='Parent.TemplateHeight',
        Tooltip='ThisItem.ModuloNome & If(IsBlank(ThisItem.Modulo), "", " · " & If(StartsWith(Upper(ThisItem.Modulo), "M"), "Módulo " & Mid(ThisItem.Modulo, 2), ThisItem.Modulo))',
        HtmlText=box(div('font-size:10pt;line-height:1.25;color:#0a1f49;font-weight:600;white-space:normal;overflow:hidden;max-height:2.5em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;',
                         esc(norm_mod('ThisItem.ModuloNome'))), flex()))
    sc.set('lblModCodHis', 'Visible', 'false')
    col('lblAreaHis', 2, Height='Parent.TemplateHeight')
    sc.replace('lblAreaHis', 'HtmlText', 'font-weight:700', 'font-weight:600')
    col('lblTipoHis', 3, Height='Parent.TemplateHeight')
    col('bdgEstHis', 4, Y='(Parent.TemplateHeight - 22) / 2')
    col('bdgResHis', 5, Y='(Parent.TemplateHeight - 22) / 2')
    col('lblAvHis', 6, Height='Parent.TemplateHeight', Tooltip='ThisItem.AvaliadorNome')
    col('lblDataHis', 7, Height='Parent.TemplateHeight',
        Tooltip='Switch(ThisItem.Estado, "PREENCHIMENTO", "Início da avaliação: " & Text(ThisItem.Inicio, "dd/mm/yyyy"), '
                '"CONCLUIDA", If(IsBlank(ThisItem.Conclusao), "Início da avaliação: " & Text(ThisItem.Inicio, "dd/mm/yyyy"), "Concluída em " & Text(ThisItem.Conclusao, "dd/mm/yyyy")), '
                '"CANCELADA", If(IsBlank(ThisItem.Conclusao), "Início da avaliação: " & Text(ThisItem.Inicio, "dd/mm/yyyy"), "Cancelada em " & Text(ThisItem.Conclusao, "dd/mm/yyyy")), '
                'If(IsBlank(ThisItem.Conclusao), "Início da avaliação: " & Text(ThisItem.Inicio, "dd/mm/yyyy"), "Concluída em " & Text(ThisItem.Conclusao, "dd/mm/yyyy")))')
    sc.replace('lblDataHis', 'HtmlText',
               'Text(If(IsBlank(ThisItem.Conclusao), "Início " & Text(ThisItem.Inicio, "dd/mm/yyyy"), Text(ThisItem.Conclusao, "dd/mm/yyyy")))',
               'Text(If(ThisItem.Estado = "PREENCHIMENTO" || IsBlank(ThisItem.Conclusao), "Desde " & Text(ThisItem.Inicio, "dd/mm/yyyy"), Text(ThisItem.Conclusao, "dd/mm/yyyy")))')
    sc.set('btnRowHis', 'Tooltip', '"Ver detalhes da avaliação de " & ThisItem.Nome')
    sc.setmany('R3btnAbrirEventoHis', Text=s('Ver detalhes'), Width='92', X='Parent.TemplateWidth - 102',
               Y='(Parent.TemplateHeight - 28) / 2', Tooltip=s('Ver detalhes da avaliação'))

    # contador com plural correto
    old = sc.get('htmlExibindoHis', 'HtmlText')
    a, b = 'Coalesce(Text(CountRows(', ' & " registro(s) encontrado(s)")'
    assert old.count(a) == 1 and old.count(b) == 1
    sc.set('htmlExibindoHis', 'HtmlText', old.replace(a, 'Coalesce(Text(With({_q: CountRows(').replace(
        b, '}, If(_q = 1, "1 registro encontrado", _q & " registros encontrados")))'))
    sc.set('lblRodTabHis', 'HtmlText', box(div('font-size:10pt;line-height:1.25;color:#627083;font-weight:400;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                               esc('If(varPodeGestao, "Exibindo todas as avaliações do laboratório", "Exibindo as avaliações em que você é avaliado ou avaliador")')), flex()))

    # ---------------------------------------------------- painel de detalhe
    sc.set('lblEvTitHis', 'Y', '14')
    sc.replace('lblEvTitHis', 'HtmlText',
               'Text((LookUp(colAvaliacoes, Uid = locEvento)).ModuloNome & " · " & (LookUp(colAvaliacoes, Uid = locEvento)).Area)',
               'Text("Detalhes da avaliação")')
    sc.setmany('lblEvSubHis', Y='46', Height='54', Width='Parent.Width - 40',
               HtmlText=box(div(KEY, esc(s('PESSOA'))) + ' & ' +
                            div('margin-top:2px;font-size:13pt;line-height:1.25;color:#0E2A4A;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                esc(f'With({{_v: {V}}}, Coalesce(_v.PessoaNomeSnap, LookUp(colPessoas, Codigo = _v.Pessoa).Nome))')) + ' & ' +
                            div('font-size:9.5pt;line-height:1.25;color:#627083;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                esc(f'With({{_v: {V}, _p: LookUp(colPessoas, Codigo = {V}.Pessoa)}}, '
                                    'With({_c: Trim(Coalesce(_v.CargoSnap, _p.Cargo)), _g: Trim(Coalesce(_v.GrupoSnap, _p.Grupo))}, '
                                    '_c & If(IsBlank(_g), "", If(IsBlank(_c), "", " · ") & "Grupo " & _g)))')),
                            'display:flex;flex-direction:column;justify-content:center;'))
    # módulo · área
    sc.setmany('lblEvR0His', X='20', Y='104', Width='Parent.Width - 40', Height='24',
               HtmlText=box(div('font-size:12pt;line-height:1.25;color:#0E2A4A;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                esc(f'With({{_v: {V}}}, ' + norm_mod('_v.ModuloNome') + ' & If(IsBlank(_v.Area), "", " · " & _v.Area))')), flex()))
    # chips: tipo + estado
    chip = "display:inline-block;margin-right:6px;padding:3px 10px;border-radius:5px;font-size:9pt;font-weight:600;"
    sc.setmany('lblEvV0His', X='20', Y='130', Width='Parent.Width - 40', Height='26',
               HtmlText=f'With({{_v: {V}}}, ' + box(
                   f'"<span style=\'{chip}background:#EEF2F6;color:#344054;\'>" & ' +
                   esc('Switch(_v.Tipo, "QUALIFICACAO", "Qualificação", "REQUALIFICACAO", "Requalificação", "EXTRAORDINARIA", "Extraordinária", _v.Tipo)') +
                   f' & "</span><span style=\'{chip}background:" & Switch(_v.Estado, "CONCLUIDA", "#E8F3EA;color:#2E7D32", "PREENCHIMENTO", "#E8F0F8;color:#1C5582", "#EEF2F6;color:#627083") & ";\'>" & ' +
                   esc('Switch(_v.Estado, "PREENCHIMENTO", "Em preenchimento", "CONCLUIDA", "Concluída", "CANCELADA", "Cancelada", _v.Estado)') +
                   ' & "</span>"', flex()) + ')')
    # faixa de situação
    sc.setmany('lblEvBanHis', Y='162', Height='40',
               Fill=f'Switch({V}.Estado, "PREENCHIMENTO", RGBA(232, 240, 248, 1), "CONCLUIDA", RGBA(232, 243, 234, 1), RGBA(238, 242, 246, 1))',
               Color=f'Switch({V}.Estado, "PREENCHIMENTO", RGBA(28, 85, 130, 1), "CONCLUIDA", RGBA(46, 125, 50, 1), RGBA(52, 64, 84, 1))',
               HtmlText=f'With({{_v: {V}}}, ' + box(div('font-size:9.5pt;line-height:1.3;color:inherit;white-space:normal;overflow:hidden;',
                   '"<b>" & Switch(_v.Estado, "PREENCHIMENTO", "Avaliação em andamento", "CONCLUIDA", "Avaliação concluída", "CANCELADA", "Avaliação cancelada", "Avaliação") & "</b> · " & '
                   'Switch(_v.Estado, "PREENCHIMENTO", "As respostas exibidas são as salvas no rascunho.", "Somente leitura. Informações registradas no momento da avaliação.") & '
                   'If(IsBlank(_v.PessoaNomeSnap) || IsBlank(_v.CargoSnap) || IsBlank(_v.GrupoSnap), "<br/>Algumas informações deste registro não estavam disponíveis no histórico original.", "")'),
                   flex()) + ')')
    # resumo: Avaliador | Início | Conclusão | Resultado | Tentativa
    grid = [('0', '0.30'), ('0.30', '0.15'), ('0.45', '0.19'), ('0.64', '0.21'), ('0.85', '0.15')]
    keys = [s('AVALIADOR'), s('INÍCIO'), f'If({V}.Estado = "CANCELADA", "CANCELAMENTO", "CONCLUSÃO")', s('RESULTADO'), s('TENTATIVA')]
    vals = [
        f'Coalesce({V}.AvaliadorNome, "—")',
        f'If(IsBlank({V}.Inicio), "—", Text({V}.Inicio, "dd/mm/yyyy"))',
        f'If(IsBlank({V}.Conclusao), If({V}.Estado = "PREENCHIMENTO", "Em aberto", "—"), Text({V}.Conclusao, "dd/mm/yyyy"))',
        f'With({{_v: {V}}}, If(_v.Estado = "CANCELADA", "Cancelada", _v.Resultado = "ATENDEU", "Atendeu", _v.Resultado = "NAO_ATENDEU", "Não atendeu", _v.Estado = "PREENCHIMENTO", "Em andamento", "—"))',
        f'If(IsBlank({V}.Tentativa), "—", Text({V}.Tentativa))',
    ]
    for i, ((x, w), k, v) in enumerate(zip(grid, keys, vals), start=1):
        X = f'20 + (Parent.Width - 40) * {x}'
        W = f'(Parent.Width - 40) * {w} - 10'
        sc.setmany(f'lblEvR{i}His', X=X, Width=W, Y='212', Height='16', HtmlText=box(div(KEY, esc(k)), flex()))
        style = VAL
        if i == 4:
            style = VAL.replace('color:#1D2A3A;', '') + 'color:" & With({_v: ' + V + '}, If(_v.Estado = "CANCELADA", "#627083", _v.Resultado = "ATENDEU", "#2E7D32", _v.Resultado = "NAO_ATENDEU", "#B91C1C", "#1C5582")) & ";'
        sc.setmany(f'lblEvV{i}His', X=X, Width=W, Y='228', Height='34',
                   HtmlText=box(div(style, esc(v)), 'display:flex;align-items:flex-start;'))
    sc.set('lblEvV1His', 'Tooltip', f'{V}.AvaliadorNome')
    for n in ('lblEvR6His', 'lblEvV6His', 'lblEvR7His'):
        sc.set(n, 'Visible', 'false')

    # documentos de referência — sempre os documentos preservados na própria avaliação
    docs = f'IfError(Table(ParseJSON({V}.DocumentosJson).documentos), Table(ParseJSON("[]")))'
    f = lambda k: f'Coalesce(IfError(Text(d.Value.{k}), ""), IfError(Text(d.Value.{k[0].upper() + k[1:]}), ""))'
    doc_item = (
        f'With({{_c: {f("codigo")}, _t: {f("titulo")}, _ver: Trim({f("versao")}), _e: Trim({f("expiracao")})}}, '
        'With({_d: If(IsMatch(_e, "\\d{4}-\\d{2}-\\d{2}.*"), Mid(_e, 9, 2) & "/" & Mid(_e, 6, 2) & "/" & Left(_e, 4), _e)}, '
        '"<div style=\'margin-top:6px;padding:4px 10px;background:#F7F9FC;border:1px solid #E6ECF3;border-radius:6px;\'>" & '
        '"<div style=\'font-size:9.5pt;line-height:1.3;color:#1D2A3A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;\'><b>" & ' + esc('Coalesce(_c, _t)') +
        ' & "</b>" & If(IsBlank(_t) || IsBlank(_c), "", " — " & ' + esc('_t') + ') & "</div>" & '
        '"<div style=\'font-size:8.5pt;line-height:1.3;color:#6B7A8D;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;\'>" & ' +
        esc('If(!IsBlank(_ver) && !IsBlank(_e), "Versão " & _ver & " · validade " & _d, !IsBlank(_ver), "Versão " & _ver, !IsBlank(_e), "Validade " & _d, "Versão não informada")') +
        ' & "</div></div>"))')
    sc.setmany('lblEvDocHis', Y='276', Height=f'28 + 48 * Min(Max(CountRows({docs}), 1), 3)',
               HtmlText=box(div('font-size:11pt;line-height:1.25;color:#0E2A4A;font-weight:700;', esc(s('Documentos de referência'))) + ' & ' +
                            f'If(CountRows({docs}) = 0, ' +
                            div('margin-top:6px;font-size:9.5pt;color:#627083;', esc(s('Nenhum documento de referência registrado nesta avaliação.'))) +
                            f', Concat({docs} As d, {doc_item}, ""))', 'overflow-y:auto;'))
    # critérios e respostas
    sc.setmany('lblEvCritTitHis', Y='lblEvDocHis.Y + lblEvDocHis.Height + 10')
    sc.setmany('galEvCritHis', Y='lblEvCritTitHis.Y + 26', Height=f'Max(Parent.Height - 214 - Self.Y, 60)',
               TemplateSize='96',
               Items=f'ForAll(IfError(Table(ParseJSON(({V}).CriteriosJson).criterios), Table(ParseJSON("[]"))) As c, '
                     '{Id: IfError(Text(c.Value.criterioId), ""), Dimensao: IfError(Text(c.Value.dimensao), ""), Descricao: IfError(Text(c.Value.descricao), ""), '
                     'Resposta: Coalesce(IfError(Text(c.Value.resposta), ""), IfError(Text(c.Value.resultado), "")), Comentario: IfError(Text(c.Value.comentario), ""), '
                     'Fontes: Coalesce(IfError(Text(c.Value.fontes), ""), "")})')
    sc.setmany('lblEvCIdHis', X='0', Y='6', Width='Parent.TemplateWidth - 116', Height='20', Tooltip='"Critério " & ThisItem.Id',
               HtmlText=box(div('font-size:10pt;line-height:1.25;color:#0E2A4A;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                esc(DIM.format(d='ThisItem.Dimensao'))), flex()))
    sc.setmany('bdgEvCRespHis', Y='6', X='Parent.TemplateWidth - 104', Width='104')
    sc.replace('bdgEvCRespHis', 'HtmlText', 'Text(Coalesce(ThisItem.Resposta, "—"))', 'Text(Coalesce(ThisItem.Resposta, "Sem resposta"))')
    sc.setmany('lblEvCDescHis', X='0', Y='28', Width='Parent.TemplateWidth - 4', Height='32',
               HtmlText=box(div('font-size:9.5pt;line-height:1.3;color:#344054;white-space:normal;overflow:hidden;max-height:2.6em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;',
                                esc('ThisItem.Descricao')), 'display:flex;align-items:flex-start;'),
               Tooltip='ThisItem.Descricao')
    sc.setmany('lblEvCComHis', X='0', Y='60', Width='Parent.TemplateWidth - 4', Height='32', Visible='true',
               Tooltip='ThisItem.Comentario',
               HtmlText=box(div('font-size:9pt;line-height:1.3;color:#344054;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                'If(IsBlank(Trim(ThisItem.Comentario)), "<span style=\'color:#98A2B3;\'>Sem comentário registrado.</span>", "<b>Comentário:</b> " & ' + esc('ThisItem.Comentario') + ')') +
                            ' & If(IsBlank(ThisItem.Fontes), "", ' +
                            div('font-size:8.5pt;line-height:1.3;color:#6B7A8D;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;',
                                '"Referência técnica: " & ' + esc('ThisItem.Fontes')) + ')',
                            'display:flex;flex-direction:column;justify-content:flex-start;'))
    # parecer e observações
    narr = lambda expr: box(div('font-size:10pt;line-height:1.35;color:#1D2A3A;white-space:normal;',
                                f'If(IsBlank(Trim({expr})), "<span style=\'color:#98A2B3;\'>Não informado.</span>", Substitute(' + esc(expr) + ', Char(10), "<br/>"))'),
                            'overflow-y:auto;')
    sc.set('lblEvParRotHis', 'Y', f'Parent.Height - 206')
    sc.setmany('lblEvParHis', Y=f'Parent.Height - 188', Height='50', HtmlText=narr(f'{V}.Parecer'))
    sc.set('lblEvObsRotHis', 'Y', f'Parent.Height - 132')
    sc.replace('lblEvObsRotHis', 'HtmlText', 'Text("Observações")',
               f'Text(If({V}.Estado = "CANCELADA", "Justificativa do cancelamento", "Observações complementares"))')
    sc.setmany('lblEvObsHis', Y=f'Parent.Height - 114', Height='52', HtmlText=narr(f'{V}.Observacoes'))
    # informações técnicas (recolhidas por padrão)
    for n in ('lblEvV7His',):
        sc.set(n, 'Visible', 'false')  # conteúdo técnico passa para lblEvTecHis (sobreposto)
    sc.clone('btnEvFecharHis', 'btnEvTecHis', 'conEvHis', {
        'Text': 'If(locEvTec, "Ocultar informações técnicas", "Informações técnicas")',
        'OnSelect': 'UpdateContext({locEvTec: !locEvTec})',
        'Tooltip': s('Identificadores internos para auditoria'),
        'X': '20', 'Y': 'Parent.Height - 50', 'Width': '210', 'Height': '34', 'Size': '10',
        'Color': 'RGBA(98, 112, 131, 1)', 'BorderColor': 'RGBA(216, 225, 234, 1)',
    }, zindex=max(int(sc.get(c['Name'], 'ZIndex') or 0) for c in sc.ctrl('conEvHis')['Children']
                  if c['Template']['Name'] != 'galleryTemplate') + 1)
    # painel técnico sobreposto (aberto sob demanda), sem deslocar o conteúdo operacional
    zmax = max(int(sc.get(c['Name'], 'ZIndex') or 0) for c in sc.ctrl('conEvHis')['Children']
               if c['Template']['Name'] != 'galleryTemplate')
    sc.clone('lblEvV7His', 'lblEvTecHis', 'conEvHis', {
        'X': '20', 'Y': 'Parent.Height - 146', 'Width': 'Parent.Width - 40', 'Height': '88',
        'Visible': 'locEvTec', 'Tooltip': '""',
        'HtmlText': f'With({{_v: {V}}}, ' + box(
                   '"<div style=\'box-sizing:border-box;height:100%;padding:8px 12px;background:#FFFFFF;border:1px solid #D8E1EA;border-radius:8px;box-shadow:0 4px 14px rgba(14,42,74,.16);font-size:8.5pt;line-height:1.45;color:#627083;word-break:break-all;\'>" & '
                   '"<b>Avaliação:</b> " & ' + esc('_v.Uid') + ' & "<br/><b>Ciclo:</b> " & ' + esc('_v.Ciclo') +
                   ' & "<br/><b>Tentativa:</b> " & ' + esc('_v.Tentativa') + ' & "<br/><b>Versão do catálogo:</b> " & ' + esc('Coalesce(_v.VersaoSnap, "não registrada")') +
                   ' & "</div>"') + ')',
    }, zindex=zmax + 1)

