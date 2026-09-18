# -*- coding: utf-8 -*-
"""Migracao do padrao visual do Radar de Liderancas para o SGC LCQ RJ."""
import os, re, sys, json, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import payaml, jsonctl as J, design as D
from ops import Screen

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'sgc')
OUT = os.path.join(BASE, 'build')

MENU_ITEMS = ('=Table({Chave: "Inicio", Rotulo: "Início", Sigla: "IN"}, '
              '{Chave: "Qualificacoes", Rotulo: "Qualificações", Sigla: "QL"}, '
              '{Chave: "Historico", Rotulo: "Histórico", Sigla: "HI"}, '
              '{Chave: "Modulos", Rotulo: "Módulos", Sigla: "MD"}, '
              '{Chave: "Cobertura", Rotulo: "Cobertura", Sigla: "CB"})')

# screen -> (sufixo, faixa, marca, divisor, galeria, btnNav, recAtivo, usuario, cta, ajuda,
#            titulo, sub, back, titulo_txt)
SCREENS = {
 'scrInicio': dict(suf='Ini', faixa='lblFaixaInicio', marca='lblMarcaIni', div='recDivisorHeaderIni',
                   gal='galNavIni', btn='btnNavIni', ativo='recNavAtivoIni', user='lblUsuarioInicio',
                   cta='btnNavNovaIni', ajuda='btnAjudaInicio', titulo='lblTituloInicio',
                   sub='lblSubtituloInicio', back=None),
 'scrQualificacoes': dict(suf='Qua', faixa='lblFaixaQualificacoes', marca='lblMarcaQua', div='recDivisorHeaderQua',
                   gal='galNavQua', btn='btnNavQua', ativo='recNavAtivoQua', user='lblUsuarioQua',
                   cta='btnNavNovaQua', ajuda='btnAjudaQualificacoes', titulo='lblTituloQualificacoes',
                   sub='lblSubQualificacoes', back='btnVoltarQualificacoes'),
 'scrDetalheQualificacao': dict(suf='Det', faixa='lblFaixaDetalhe', marca='lblMarcaDet', div='recDivisorHeaderDet',
                   gal='galNavDet', btn='btnNavDet', ativo='recNavAtivoDet', user='lblUsuarioDet',
                   cta='btnNavNovaDet', ajuda='btnAjudaDetalhe', titulo='lblTituloDetalhe',
                   sub='lblSubDetalhe', back='btnVoltarDetalhe'),
 'scrNovaAvaliacao': dict(suf='Nov', faixa='lblFaixaNovaAvaliacao', marca='lblMarcaNov', div='recDivisorHeaderNov',
                   gal='galNavNov', btn='btnNavNov', ativo='recNavAtivoNov', user='lblUsuarioNov',
                   cta=None, ajuda='btnAjudaNovaAvaliacao', titulo='lblTituloNovaAvaliacao',
                   sub='lblInstrucaoNovaAvaliacao', back='btnVoltarNovaAvaliacao'),
 'scrAvaliacao': dict(suf='Ava', faixa='recHeaderAva', marca='lblMarcaAva', div='recDivisorHeaderAva',
                   gal='galNavAva', btn='btnNavAva', ativo='recNavAtivoAva', user='lblUsuarioAva',
                   cta=None, ajuda='btnAjudaAvaliacao', titulo='lblAvaliacaoTitulo',
                   sub='lblAvaliacaoSub', back='btnAvaliacaoVoltar'),
 'scrHistoricoAvaliacoes': dict(suf='His', faixa='recHeaderHis', marca='lblMarcaHis', div='recDivisorHeaderHis',
                   gal='galNavHis', btn='btnNavHis', ativo='recNavAtivoHis', user='lblUsuarioHis',
                   cta='btnNavNovaHis', ajuda='btnAjudaHistorico', titulo='lblHistoricoTitulo',
                   sub='lblHistoricoSub', back='btnHistoricoInicio'),
 'scrModulos': dict(suf='Mod', faixa='recHeaderMod', marca='lblMarcaMod', div='recDivisorHeaderMod',
                   gal='galNavMod', btn='btnNavMod', ativo='recNavAtivoMod', user='lblUsuarioMod',
                   cta='btnNavNovaMod', ajuda='btnAjudaModulos', titulo='lblModulosTitulo',
                   sub='lblModulosSub', back='btnModulosInicio'),
 'scrCobertura': dict(suf='Cob', faixa='recHeaderCob', marca='lblMarcaCob', div='recDivisorHeaderCob',
                   gal='galNavCob', btn='btnNavCob', ativo='recNavAtivoCob', user='lblUsuarioCob',
                   cta='btnNavNovaCob', ajuda='btnAjudaCobertura', titulo='lblCoberturaTitulo',
                   sub='lblCoberturaRegra', back='btnCoberturaInicio'),
}

MENU_W = 260          # largura da faixa do menu lateral
HEADER_H = 90         # altura do cabecalho institucional (Radar)
FOOTER_H = 30         # rodape
DY = HEADER_H - 64    # 26 -> deslocamento vertical do conteudo
DBOT = DY + FOOTER_H  # 56 -> reducao de altura util


# ---------------------------------------------------------------- geometria
NUM = r'-?\d+(?:\.\d+)?'


def shift_x(s):
    """Desloca para a direita o conteudo que antes comecava na margem esquerda."""
    if s is None:
        return None
    s = s.strip()
    if re.fullmatch(NUM, s):
        return str(float(s) + MENU_W if '.' in s else int(s) + MENU_W)
    m = re.match(r'^(%s)\s*\+\s*(.*)$' % NUM, s)
    if m:
        return '%d + %s' % (int(m.group(1)) + MENU_W, sub_width(m.group(2)))
    if s.startswith('Parent.Width -'):
        return s                      # ancorado a direita: preserva
    if s.startswith('(Parent.Width -'):
        return '%d + %s' % (MENU_W, sub_width(s))
    return s


def sub_width(s):
    """Reduz larguras relativas a Parent.Width pela faixa do menu."""
    def rep(m):
        return 'Parent.Width - %d' % (int(m.group(1)) + MENU_W)
    return re.sub(r'Parent\.Width\s*-\s*(\d+)', rep, s)


def sub_height(s):
    def rep(m):
        return 'Parent.Height - %d' % (int(m.group(1)) + DBOT)
    return re.sub(r'Parent\.Height\s*-\s*(\d+)', rep, s)


def shift_y(s):
    if s is None:
        return None
    s = s.strip()
    if re.fullmatch(NUM, s):
        return str(int(s) + DY)
    m = re.match(r'^(%s)\s*\+\s*(.*)$' % NUM, s)
    if m:
        return '%d + %s' % (int(m.group(1)) + DY, sub_height(m.group(2)))
    if 'Parent.Height' in s:
        return sub_height(s)
    return s


def move_content(sc, name):
    """Aplica o deslocamento do shell (menu lateral + cabecalho + rodape)."""
    props = {}
    x = sc.get(name, 'X')
    y = sc.get(name, 'Y')
    w = sc.get(name, 'Width')
    h = sc.get(name, 'Height')
    largura_total = (w is not None and w.strip() == 'Parent.Width')
    if largura_total:
        props['X'] = str(MENU_W)
        props['Width'] = 'Parent.Width - %d' % MENU_W
        if y is not None and y.strip().startswith('Parent.Height -'):
            ny = re.sub(r'Parent\.Height\s*-\s*(\d+)',
                        lambda m: 'Parent.Height - %d' % (int(m.group(1)) + FOOTER_H + 4), y)
        else:
            ny = shift_y(y) if y is not None else str(DY)
        if ny != y:
            props['Y'] = ny
        if h is not None and sub_height(h) != h:
            props['Height'] = sub_height(h)
        sc.set(name, props)
        return
    nx = shift_x(x) if x is not None else str(MENU_W + 32)
    if nx != x:
        props['X'] = nx
    ny = shift_y(y) if y is not None else str(DY)
    if y is None:
        props['Y'] = ny
    elif ny != y:
        props['Y'] = ny
    if w is not None:
        nw = sub_width(w)
        if nw != w:
            props['Width'] = nw
    if h is not None:
        nh = sub_height(h)
        if nh != h:
            props['Height'] = nh
    if props:
        sc.set(name, props)


# ---------------------------------------------------------------- shell
def build_shell(sc, cfg, chave):
    suf = cfg['suf']
    # --- fundo da tela
    sc.screen_set({'Fill': D.FUNDO})

    # --- cabecalho institucional
    sc.set(cfg['faixa'], {'Height': str(HEADER_H), 'Fill': D.PRIM, 'Width': 'Parent.Width',
                          'X': '0', 'Y': '0'})
    sc.move_to_start(cfg['faixa'])
    sc.delete(cfg['marca'])
    sc.delete(cfg['div'])
    sc.add_html('htmlCabecalho' + suf,
                {'HtmlText': D.header_html('Sistema de Gest&#227;o de Compet&#234;ncias'),
                 'X': '0', 'Y': '0', 'Width': 'Parent.Width', 'Height': str(HEADER_H)},
                index=1)

    # --- identificacao do usuario
    sc.set(cfg['user'], {'Height': str(HEADER_H), 'Y': '0', 'Size': '12',
                         'Font': D.FONTE, 'Color': 'RGBA(255, 255, 255, 0.88)',
                         'Align': 'Align.Right', 'VerticalAlign': 'VerticalAlign.Middle',
                         'Width': '230', 'X': 'Parent.Width - 510'})

    # --- CTA e ajuda no cabecalho
    if cfg['cta']:
        sc.set(cfg['cta'], {'Y': '27', 'Height': '36', 'Width': '150',
                            'X': 'Parent.Width - 278',
                            'Fill': 'RGBA(255, 255, 255, 1)', 'Color': D.SEC,
                            'HoverFill': 'RGBA(234, 241, 248, 1)', 'HoverColor': D.PRIM,
                            'PressedFill': 'RGBA(214, 225, 236, 1)', 'PressedColor': D.PRIM,
                            'BorderColor': 'RGBA(255, 255, 255, 1)',
                            'HoverBorderColor': 'RGBA(255, 255, 255, 1)',
                            'PressedBorderColor': 'RGBA(255, 255, 255, 1)',
                            'BorderThickness': '1', 'Font': D.FONTE,
                            'FontWeight': 'FontWeight.Bold', 'Size': '12',
                            'RadiusTopLeft': '10', 'RadiusTopRight': '10',
                            'RadiusBottomLeft': '10', 'RadiusBottomRight': '10'})
    sc.set(cfg['ajuda'], {'Y': '27', 'Height': '36', 'Width': '92', 'X': 'Parent.Width - 116',
                          'Fill': 'RGBA(255, 255, 255, 0.12)', 'Color': 'RGBA(255, 255, 255, 1)',
                          'HoverFill': 'RGBA(255, 255, 255, 0.22)',
                          'PressedFill': 'RGBA(255, 255, 255, 0.28)',
                          'BorderColor': 'RGBA(255, 255, 255, 0.55)', 'BorderThickness': '1',
                          'Font': D.FONTE, 'FontWeight': 'FontWeight.Semibold', 'Size': '12',
                          'RadiusTopLeft': '10', 'RadiusTopRight': '10',
                          'RadiusBottomLeft': '10', 'RadiusBottomRight': '10'})

    # --- menu lateral (260 px), no padrao galMenuLateralNovo do Radar
    sc.set(cfg['gal'], {'X': '8', 'Y': str(HEADER_H + 8), 'Width': '252',
                        'Height': 'Parent.Height - %d' % (HEADER_H + 8 + FOOTER_H + 8),
                        'TemplateSize': '68', 'TemplatePadding': '3', 'WrapCount': '1',
                        'ShowScrollbar': 'false', 'Fill': 'RGBA(0, 0, 0, 0)',
                        'Items': MENU_ITEMS,
                        'AccessibleLabel': '"Menu principal do SGC LCQ RJ"'})
    sc.delete(cfg['ativo'])
    sc.add_html('htmlMenu' + suf,
                {'HtmlText': D.menu_item_html(chave),
                 'X': '3', 'Y': '3',
                 'Width': 'Parent.TemplateWidth - 6', 'Height': 'Parent.TemplateHeight - 6'},
                parent=cfg['gal'], index=0)
    sc.json_template_first(cfg['gal'])
    sc.set(cfg['btn'], {'X': '0', 'Y': '0', 'Width': 'Parent.TemplateWidth',
                        'Height': 'Parent.TemplateHeight', 'Text': '""',
                        'Fill': 'RGBA(0, 0, 0, 0)', 'Color': 'RGBA(0, 0, 0, 0)',
                        'HoverFill': 'RGBA(14, 42, 74, 0.06)', 'HoverColor': 'RGBA(0, 0, 0, 0)',
                        'PressedFill': 'RGBA(14, 42, 74, 0.10)', 'PressedColor': 'RGBA(0, 0, 0, 0)',
                        'BorderColor': 'RGBA(0, 0, 0, 0)', 'BorderThickness': '0',
                        'HoverBorderColor': 'RGBA(0, 0, 0, 0)',
                        'PressedBorderColor': 'RGBA(0, 0, 0, 0)',
                        'Font': D.FONTE, 'Size': '12',
                        'Tooltip': 'ThisItem.Rotulo',
                        'RadiusTopLeft': '13', 'RadiusTopRight': '13',
                        'RadiusBottomLeft': '13', 'RadiusBottomRight': '13'})
    sc.move_to_end(cfg['btn'])

    # --- rodape institucional
    sc.add_html('htmlRodape' + suf,
                {'HtmlText': D.RODAPE_HTML, 'X': '0', 'Y': 'Parent.Height - %d' % FOOTER_H,
                 'Width': 'Parent.Width', 'Height': str(FOOTER_H)})


def build_titulo(sc, cfg, titulo_txt):
    """Substitui titulo + subtitulo por um bloco executivo no padrao Radar."""
    suf = cfg['suf']
    sub_expr = sc.get(cfg['sub'], 'Text')
    sub_expr = sub_expr.lstrip('=').strip() if sub_expr else '""'
    x = MENU_W + 32 + (116 if cfg['back'] else 0)
    sc.delete(cfg['titulo'])
    sc.delete(cfg['sub'])
    sc.add_html('htmlTitulo' + suf,
                {'HtmlText': D.titulo_html(titulo_txt, sub_expr),
                 'X': str(x), 'Y': str(74 + DY),
                 'Width': 'Parent.Width - %d' % (x + 360), 'Height': '64'})


# ---------------------------------------------------------------- acabamento
RADIUS = {'4': '10', '8': '14'}


def restyle(sc, cfg):
    """Acabamento Radar: raios, bordas, sombras, acentos de card e tipografia."""
    for cy in sc.y.walk():
        if cy is sc.y:
            continue
        p = cy.props
        tpl = dict(cy.meta).get('Control', '')
        upd = {}
        r = p.get('RadiusTopLeft')
        if r and len(r) == 1 and r[0] in RADIUS:
            nr = RADIUS[r[0]]
            for k in ('RadiusTopLeft', 'RadiusTopRight', 'RadiusBottomLeft', 'RadiusBottomRight'):
                if k in p:
                    upd[k] = nr
        # cards brancos: borda discreta + sombra suave do Radar
        if tpl.startswith('GroupContainer') and p.get('Fill') == ['RGBA(255, 255, 255, 1)']:
            upd['BorderColor'] = D.BORDA
            upd['BorderThickness'] = '1'
            upd['DropShadow'] = 'DropShadow.Semilight'
        # barra vertical colorida dos cards de situacao: 4 -> 5 px (padrao Radar)
        if cy.name.lower().startswith('recacento') and p.get('Width') == ['4']:
            upd['Width'] = '5'
        if upd:
            sc.set(cy.name, upd)

    # modal de ajuda: overlay + card branco com raio 18 e sombra marcada
    suf = cfg['suf']
    for nm in sc.names():
        if nm.startswith('recAjudaOverlay'):
            sc.set(nm, {'Fill': 'RGBA(14, 42, 74, 0.34)'})
        if nm.startswith('grpAjuda'):
            sc.set(nm, {'Fill': 'RGBA(255, 255, 255, 1)', 'BorderColor': D.BORDA,
                        'BorderThickness': '1', 'DropShadow': 'DropShadow.Bold',
                        'RadiusTopLeft': '18', 'RadiusTopRight': '18',
                        'RadiusBottomLeft': '18', 'RadiusBottomRight': '18'})


def kpi_typography(sc):
    """Hierarquia tipografica dos KPIs no padrao do Cockpit/Capacidade do Radar."""
    for cy in sc.y.walk():
        n = cy.name
        if n.startswith('lblQtd') or n.startswith('lblKpiValor') or n.startswith('lblValorKpi'):
            sc.set(n, {'Size': '32', 'FontWeight': 'FontWeight.Bold', 'Font': D.FONTE})
        if n.startswith('lblCard') and n.endswith('Titulo'):
            sc.set(n, {'Size': '12', 'FontWeight': 'FontWeight.Bold',
                       'Color': 'RGBA(36, 59, 83, 1)', 'Font': D.FONTE})
        if n.startswith('lblQtd'):
            sc.set(n, {'Color': D.PRIM})
        if n.startswith('lblHdr'):
            sc.set(n, {'Size': '10', 'FontWeight': 'FontWeight.Bold',
                       'Color': 'RGBA(82, 101, 122, 1)', 'Font': D.FONTE})
        # titulos estaticos de secao: hierarquia do Radar
        txt = '\n'.join(cy.props.get('Text', []))
        estatico = txt.startswith('="') and '&' not in txt
        if estatico and n.endswith('Titulo') and not n.startswith(('lblCard', 'lblAjuda')):
            sc.set(n, {'Size': '14', 'FontWeight': 'FontWeight.Bold',
                       'Color': D.PRIM, 'Font': D.FONTE})
        if estatico and not n.endswith(('Sub', 'Texto', 'Info')) and \
                (n.startswith('lblAcessoRapido') or n.startswith('lblSecao')
                 or n.startswith('lblLegenda')):
            sc.set(n, {'Size': '14', 'FontWeight': 'FontWeight.Bold',
                       'Color': D.PRIM, 'Font': D.FONTE})
        if n.startswith('lblKpiLegenda'):
            sc.set(n, {'Size': '10', 'Color': D.TEXTO2, 'Font': D.FONTE})


def polish(sc):
    """Badges, campos e botoes com o acabamento do Radar (pill, raio, tipografia)."""
    for cy in list(sc.y.walk()):
        if cy is sc.y:
            continue
        n = cy.name
        tpl = dict(cy.meta).get('Control', '')
        upd = {}
        if n.startswith('bdg') and 'Button' in tpl:
            h = '\n'.join(cy.props.get('Height', ['26']))
            try:
                raio = str(min(int(h) // 2, 15))
            except ValueError:
                raio = '13'
            upd.update({'RadiusTopLeft': raio, 'RadiusTopRight': raio,
                        'RadiusBottomLeft': raio, 'RadiusBottomRight': raio,
                        'Size': '10', 'FontWeight': 'FontWeight.Bold', 'Font': D.FONTE,
                        'BorderThickness': '0'})
        if tpl.startswith('Classic/TextInput'):
            upd.update({'RadiusTopLeft': '10', 'RadiusTopRight': '10',
                        'RadiusBottomLeft': '10', 'RadiusBottomRight': '10',
                        'BorderColor': D.BORDA, 'Font': D.FONTE})
        if upd:
            sc.set(n, upd)


SHELL_PREFIX = ('recAjudaOverlay', 'grpAjuda')


# ajustes finos por tela (evita sobreposicao com rodape/barra de acoes)
OVERRIDES = {
    'scrNovaAvaliacao': {'grpFormNovaAvaliacao': {'Y': '138', 'Height': '600'}},
}


def migrate_screen(name, cfg):
    yml = os.path.join(OUT, 'Src', name + '.pa.yaml')
    jsn = SCREEN_JSON[name]
    sc = Screen(yml, jsn)
    # chave ativa do menu, lida do proprio app (preserva a navegacao existente)
    chave = sc.get(cfg['ativo'], 'Visible') or '=ThisItem.Chave = ""'
    m = re.search(r'"(.*)"', chave)
    chave = m.group(1) if m else ''
    titulo_txt = (sc.get(cfg['titulo'], 'Text') or '=""').strip().strip('=').strip('"')

    shell = {cfg['faixa'], cfg['user'], cfg['gal'], cfg['ajuda'], cfg['titulo'], cfg['sub'],
             cfg['marca'], cfg['div']}
    if cfg['cta']:
        shell.add(cfg['cta'])
    conteudo = [n for n in sc.names()
                if n not in shell and not n.startswith(SHELL_PREFIX)]

    build_shell(sc, cfg, chave)
    for n in conteudo:
        move_content(sc, n)
    build_titulo(sc, cfg, titulo_txt)
    restyle(sc, cfg)
    kpi_typography(sc)
    polish(sc)
    for nm, props in OVERRIDES.get(name, {}).items():
        sc.set(nm, props)
    sc.save()
    return chave, titulo_txt, conteudo


# ---------------------------------------------------------------- app / tema
TEMA = """

// ════════════════════════════════════════════════════════════════
// TEMA VISUAL — PADRÃO LCQ RJ (alinhado ao Radar de Lideranças)
// Apenas variáveis de apresentação. Nenhuma regra de negócio aqui.
// ════════════════════════════════════════════════════════════════
Set(varCorPrimaria, RGBA(14, 42, 74, 1));
Set(varCorSecundaria, RGBA(28, 85, 130, 1));
Set(varCorFundo, RGBA(245, 247, 250, 1));
Set(varCorCard, RGBA(255, 255, 255, 1));
Set(varCorTexto, RGBA(32, 42, 53, 1));
Set(varCorTextoSuave, RGBA(101, 115, 132, 1));
Set(varCorBorda, RGBA(216, 225, 234, 1));
Set(varCorVerde, RGBA(46, 125, 50, 1));
Set(varCorAmarelo, RGBA(202, 138, 4, 1));
Set(varCorLaranja, RGBA(180, 83, 9, 1));
Set(varCorVermelho, RGBA(185, 28, 28, 1))"""


def patch_app():
    # yaml
    p = os.path.join(OUT, 'Src', 'App.pa.yaml')
    txt = open(p, encoding='utf-8').read()
    bloco = '\n'.join('      ' + l if l.strip() else '' for l in TEMA.strip('\n').split('\n'))
    txt = txt.replace('\n    Theme: =PowerAppsTheme', ';\n' + bloco + '\n    Theme: =PowerAppsTheme')
    open(p, 'w', encoding='utf-8').write(txt)
    # json
    pj = SCREEN_JSON['App']
    doc = J.load(pj)
    app = doc['TopParent']
    cur = J.get_rule(app, 'OnStart')
    J.set_rule(app, 'OnStart', cur + ';\n' + TEMA.strip('\n'))
    J.save(doc, pj)


# ---------------------------------------------------------------- tokens globais
def apply_tokens():
    alvos = glob.glob(os.path.join(OUT, 'Src', '*.pa.yaml')) + \
            glob.glob(os.path.join(OUT, 'Controls', '*.json'))
    tot = 0
    for f in alvos:
        t = open(f, encoding='utf-8').read()
        o = t
        for k, v in D.CORES.items():
            t = t.replace(k, v)
        t = t.replace("Font.Lato", "Font.'Open Sans'") if f.endswith('.yaml') else \
            t.replace("Font.Lato", "Font.'Open Sans'")
        if t != o:
            tot += 1
            open(f, 'w', encoding='utf-8').write(t)
    return tot


def add_htmlviewer_template():
    p = os.path.join(OUT, 'References', 'Templates.json')
    d = json.load(open(p, encoding='utf-8'))
    nomes = {t['Name'] for t in d['UsedTemplates']}
    if 'htmlViewer' not in nomes:
        proto = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            'proto_template_htmlviewer.json'), encoding='utf-8'))
        d['UsedTemplates'].append(proto)
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        return True
    return False


def write_packed():
    p = os.path.join(OUT, 'packed.json')
    json.dump({"PackedStructureVersion": "0.1",
               "LastPackedDateTimeUtc": "2026-09-18 12:00:00Z",
               "PackingClient": {"Name": "Pac CLI", "Version": "2.12.2"},
               "LoadConfiguration": {"LoadFromYaml": True}},
              open(p, 'w', encoding='utf-8'), indent=2)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)
    global SCREEN_JSON
    SCREEN_JSON = J.screen_files(os.path.join(OUT, 'Controls'))
    for name, cfg in SCREENS.items():
        chave, titulo, conteudo = migrate_screen(name, cfg)
        print('%-24s menu=%-14s titulo=%-40s conteudo=%d' % (name, chave, titulo[:40], len(conteudo)))
    patch_app()
    print('tokens aplicados em', apply_tokens(), 'arquivos')
    print('template htmlViewer:', add_htmlviewer_template())
    write_packed()


if __name__ == '__main__':
    main()
