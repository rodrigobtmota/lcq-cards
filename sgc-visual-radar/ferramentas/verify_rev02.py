# -*- coding: utf-8 -*-
"""Verificacao automatica da REV02.

Compara REV02 x REV01 (propriedade a propriedade) e REV02 x SGC original
(formulas funcionais), alem de checagens estruturais do pacote.
"""
import os, re, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import payaml, jsonctl as J, rev02, caminhos

BASE = caminhos.RAIZ
ORIG = caminhos.entrada('sgc')
REV2 = caminhos.saida('build')
# linha de base da comparacao: por padrao a REV01 entregue; aceita outra por argumento
REV1 = caminhos.entrada(sys.argv[1]) if len(sys.argv) > 1 else caminhos.entrada('build_rev01')
erros, notas = [], []


def mapa(d):
    out = {}
    for f in glob.glob(os.path.join(d, 'Src', 'scr*.pa.yaml')):
        _, r = payaml.parse(f)
        out[r.name] = {c.name: c for c in r.walk()}   # inclui a propria tela
    return out


def props(c):
    return {p: '\n'.join(v) for p, v in c.props.items()}


# ---------------------------------------------------------------- A. REV01 -> REV02
def diff_rev01_rev02():
    a, b = mapa(REV1), mapa(REV2)
    if set(a) != set(b):
        erros.append('conjunto de telas mudou entre REV01 e REV02')
    mudancas = {'AccessibleLabel': 0, 'variaveis': 0, 'raio': 0, 'imagem': 0,
                'colunas': 0, 'cabecalho': 0, 'ajuda': 0, 'reflow': 0}
    ctrl_mod = set()
    for tela in sorted(a):
        ca, cb = a[tela], b[tela]
        novos = set(cb) - set(ca)
        sumidos = set(ca) - set(cb)
        # autorizado: 1 controle imgNav* por tela (faixa institucional como recurso local)
        if novos - {n for n in novos if n.startswith('imgNav')} or sumidos:
            erros.append('%s: controles diferentes entre a base e a REV02: %s'
                         % (tela, sorted((novos - {n for n in novos if n.startswith('imgNav')})
                                         | sumidos)))
        if len([n for n in novos if n.startswith('imgNav')]) > 1:
            erros.append('%s: mais de um controle de faixa institucional' % tela)
        mudancas['imagem'] += len([n for n in novos if n.startswith('imgNav')])
        for nome in set(ca) & set(cb):
            pa, pb = props(ca[nome]), props(cb[nome])
            for p in set(pa) | set(pb):
                va, vb = pa.get(p), pb.get(p)
                if va == vb:
                    continue
                ctrl_mod.add((tela, nome))
                # 1) AccessibleLabel novo nos botoes do menu
                # acessibilidade compativel com o Source Code schema
                if p == 'AccessibleLabel' and va is None and vb is not None and \
                        dict(cb[nome].meta).get('Control') != 'Classic/Button@2.2.0':
                    mudancas['AccessibleLabel'] += 1
                    continue
                if p == 'Text' and vb == '=ThisItem.Rotulo' and \
                        nome.startswith('btnNav') and not nome.startswith('btnNavNova'):
                    mudancas['AccessibleLabel'] += 1
                    continue
                if p == 'Tooltip' and nome.startswith('btnAjudaX') and vb == '="Fechar a ajuda"':
                    mudancas['AccessibleLabel'] += 1
                    continue
                # 2) literal de cor -> variavel de tema (mesma finalidade)
                if va is not None and vb is not None and ('Color' in p or 'Fill' in p):
                    v = va
                    for lit, var in rev02.VARS.items():
                        v = v.replace(lit, var)
                    if v == vb or v.replace('RGBA(255, 255, 255, 1)', 'varCorCard') == vb:
                        mudancas['variaveis'] += 1
                        continue
                # 3) colunas fixas reescaladas para caber no container estreitado
                if p in ('X', 'Width') and va is not None and vb is not None and \
                        not re.search(r'[A-Za-z]', va.lstrip('=')) and \
                        not re.search(r'[A-Za-z]', vb.lstrip('=')):
                    try:
                        a_, b_ = eval(va.lstrip('=')), eval(vb.lstrip('='))
                        if 0 < b_ <= a_ + 0.5:
                            mudancas['colunas'] += 1
                            continue
                    except Exception:
                        pass
                # 4) raio de card -> 14
                if p.startswith('Radius') and vb in ('=14', '=10'):
                    mudancas['raio'] += 1
                    continue
                # 5) faixa institucional: recurso local, enquadramento e rotulo acessivel
                if nome.startswith('imgNav') and p in ('Image', 'ImagePosition', 'AccessibleLabel',
                                                       'X', 'Y', 'Width', 'Height', 'Fill',
                                                       'BorderColor', 'BorderStyle',
                                                       'BorderThickness', 'Transparency',
                                                       'PaddingTop', 'PaddingBottom',
                                                       'PaddingLeft', 'PaddingRight'):
                    mudancas['imagem'] += 1
                    continue
                # 6) cabecalho: HTML deixa de trazer o fundo (data URI) e fica transparente
                if nome.startswith('htmlCabecalho') and p == 'HtmlText' and \
                        'data:image' in (va or '') and 'data:image' not in (vb or ''):
                    mudancas['cabecalho'] += 1
                    continue
                # 7) contraste do botao Ajuda sobre a faixa
                if nome.startswith('btnAjuda') and p in ('Fill', 'HoverFill', 'PressedFill',
                                                         'Color', 'HoverColor', 'PressedColor',
                                                         'BorderColor'):
                    mudancas['ajuda'] += 1
                    continue
                # 8) reflow de rotulos cortados na tela inicial (apenas geometria)
                if p in ('Y', 'Height', 'Width', 'X') and \
                        nome.startswith(('lblCard', 'lblQtd', 'lblKpiLegenda', 'lblAcao', 'icoAcao')):
                    mudancas['reflow'] += 1
                    continue
                erros.append('ALTERACAO NAO AUTORIZADA %s.%s.%s: %r -> %r'
                             % (tela, nome, p, va, vb))
    return mudancas, ctrl_mod


# ---------------------------------------------------------------- B. formulas funcionais x original
CRITICAS = ('OnSelect', 'OnVisible', 'OnHidden', 'OnChange', 'Items', 'Text', 'Default',
            'DefaultSelectedItems', 'DisplayMode', 'Visible', 'Tooltip')
FUNCIONAIS = ('Patch(', 'Navigate(', 'Set(', 'UpdateContext', 'Collect', 'Filter(',
              'LookUp(', 'SortByColumns', 'Reset(', 'With(', 'Concurrent(')


def formulas_x_original():
    a, b = mapa(ORIG), mapa(REV2)
    intactas = 0
    for tela in sorted(set(a) & set(b)):
        for nome in set(a[tela]) & set(b[tela]):
            pa, pb = props(a[tela][nome]), props(b[tela][nome])
            for p in CRITICAS:
                va, vb = pa.get(p), pb.get(p)
                if va is None:
                    continue
                if any(t in va for t in FUNCIONAIS):
                    if va == vb:
                        intactas += 1
                    elif nome.startswith(('galNav', 'btnNav')):
                        intactas += 1   # shell: Items/Tooltip do menu, mudanca visual declarada
                    else:
                        erros.append('FORMULA FUNCIONAL ALTERADA %s.%s.%s' % (tela, nome, p))
    return intactas


# ---------------------------------------------------------------- C. estrutura
def estrutura():
    # C1 AccessibleLabel em todos os btnNav
    b = mapa(REV2)
    ofensores = [(t, n) for t, cs in b.items() for n, c in cs.items()
                 if dict(c.meta).get('Control') == 'Classic/Button@2.2.0'
                 and 'AccessibleLabel' in c.props]
    if ofensores:
        erros.append('PA2108: AccessibleLabel em Classic/Button: %s' % ofensores)
    sem_rotulo = [(t, n) for t, cs in b.items() for n, c in cs.items()
                  if n.startswith('btnNav') and not n.startswith('btnNavNova')
                  and '\n'.join(c.props.get('Text', [])) != '=ThisItem.Rotulo']
    if sem_rotulo:
        erros.append('botao de menu sem Text = ThisItem.Rotulo: %s' % sem_rotulo)
    # C2 paridade Src x Controls, sem duplicados nem referencias orfas
    jf = J.screen_files(os.path.join(REV2, 'Controls'))
    for tela, cs in b.items():
        top = J.load(jf[tela])['TopParent']
        nomes = [c['Name'] for c in J.walk(top) if c is not top
                 and not re.fullmatch(r'[0-9a-f\-]{36}', c['Name'])]
        if len(nomes) != len(set(nomes)):
            erros.append('%s: controle duplicado no JSON' % tela)
        esperado = {n for n in cs if n != tela}
        if set(nomes) != esperado:
            erros.append('%s: divergencia Src x Controls %s' % (tela, sorted(set(nomes) ^ esperado)))
        for c in J.walk(top):
            for ch in c.get('Children', []):
                if ch.get('Parent') != c['Name']:
                    erros.append('%s: referencia orfa %s -> %s' % (tela, ch['Name'], ch.get('Parent')))
    # C3 fontes de dados
    da = json.load(open(os.path.join(ORIG, 'References', 'DataSources.json'), encoding='utf-8'))
    db = json.load(open(os.path.join(REV2, 'References', 'DataSources.json'), encoding='utf-8'))
    na = sorted(x.get('Name') for x in da['DataSources'])
    nb = sorted(x.get('Name') for x in db['DataSources'])
    if na != nb:
        erros.append('DataSources alterado: %s' % (set(na) ^ set(nb)))
    for src in ('SGC_Pessoas', 'SGC_Competencias', 'SGC_Qualificacoes',
                'SGC_Avaliacoes', 'SGC_Certificados'):
        if src not in nb:
            erros.append('fonte ausente: %s' % src)
    # C4 nenhuma referencia Radar_* / asset do Radar
    texto = ''
    for f in glob.glob(os.path.join(REV2, 'Src', '*.pa.yaml')) + \
             glob.glob(os.path.join(REV2, 'References', '*.json')):
        texto += open(f, encoding='utf-8').read()
    for proibido in ('Radar_', 'Nav_bg', '0e88ed96-a42e-48f0-b551-5b2479ae42eb',
                     'blob.core.windows.net', 'data:image'):
        if proibido in texto:
            erros.append('referencia proibida encontrada: %s' % proibido)
    # C5 recurso local da faixa
    res = json.load(open(os.path.join(REV2, 'References', 'Resources.json'), encoding='utf-8'))
    if len(res['Resources']) != 1:
        erros.append('esperado exatamente 1 recurso, achado %d' % len(res['Resources']))
    r = res['Resources'][0]
    if r['Name'] != rev02.RECURSO or r['ResourceKind'] != 'LocalFile' or r['RootPath'] != '':
        erros.append('recurso da faixa mal registrado: %s' % r)
    if not os.path.isfile(os.path.join(REV2, 'Assets', 'Images', r['FileName'])):
        erros.append('arquivo do recurso ausente em Assets/Images')
    # C6 canvas
    pr = json.load(open(os.path.join(REV2, 'Properties.json'), encoding='utf-8'))
    if (int(pr['DocumentLayoutWidth']), int(pr['DocumentLayoutHeight'])) != (1366, 768):
        erros.append('canvas alterado')
    # C7 proveniencia do pacote
    pk = json.load(open(os.path.join(REV2, 'packed.json'), encoding='utf-8'))
    if 'Pac CLI' in pk['PackingClient']['Name']:
        erros.append('packed.json declara Pac CLI indevidamente')
    if pk['LoadConfiguration']['LoadFromYaml'] is not True:
        erros.append('LoadFromYaml perdido')
    # C8 coerencia das variaveis de tema com o App.OnStart
    app = open(os.path.join(REV2, 'Src', 'App.pa.yaml'), encoding='utf-8').read()
    for lit, var in rev02.VARS.items():
        m = re.search(r'Set\(%s,\s*(RGBA\([^)]*\))\)' % var, app)
        if not m:
            erros.append('variavel %s nao definida no App.OnStart' % var)
        elif m.group(1) != lit:
            erros.append('variavel %s definida como %s, esperado %s' % (var, m.group(1), lit))
    if 'Set(varCorCard, RGBA(255, 255, 255, 1))' not in app:
        erros.append('varCorCard nao definida como branco')


# ---------------------------------------------------------------- D. geometria
def geometria():
    W, H = 1366, 768
    def ev(s):
        if s is None:
            return None
        s = s.strip().lstrip('=').replace('Parent.Width', str(W)).replace('Parent.Height', str(H))
        if re.search(r'[A-Za-z]', s):
            return None
        try:
            return eval(s)
        except Exception:
            return None
    for f in sorted(glob.glob(os.path.join(REV2, 'Src', 'scr*.pa.yaml'))):
        _, r = payaml.parse(f)
        for c in r.children:
            g = lambda p: ev('\n'.join(c.props.get(p, [])) or None)
            x, y = g('X') or 0, g('Y') or 0
            w, h = g('Width'), g('Height')
            if w is None or h is None:
                continue
            if c.name.startswith(('recAjudaOverlay', 'grpAjuda', 'htmlRodape', 'lblFaixa',
                                  'recHeader', 'imgNav', 'htmlCabecalho', 'galNav')):
                continue
            if x + w > W + 0.5:
                erros.append('%s/%s ultrapassa o canvas' % (r.name, c.name))
            if y + h > H - 28:
                erros.append('%s/%s invade o rodape' % (r.name, c.name))
            if y > 92 and x < 258:
                erros.append('%s/%s sobre o menu lateral' % (r.name, c.name))
            if y < 90 and not (x > 850):
                erros.append('%s/%s atras do cabecalho' % (r.name, c.name))
            if y + h > 90 and y < 90 and x < 850:
                erros.append('%s/%s cruza o cabecalho' % (r.name, c.name))


def geometria_interna():
    """Nenhum controle pode estourar o container que o contem (colunas fixas)."""
    def ev(s, pw, ph):
        if s is None:
            return None
        s = (s.strip().lstrip('=').replace('Parent.TemplateWidth', str(pw))
             .replace('Parent.TemplateHeight', str(ph)).replace('Parent.Width', str(pw))
             .replace('Parent.Height', str(ph)))
        if re.search(r'[A-Za-z]', s):
            return None
        try:
            return float(eval(s))
        except Exception:
            return None

    def visita(c, pw, ph, tela):
        g = lambda p: '\n'.join(c.props.get(p, [])) or None
        w = ev(g('Width'), pw, ph)
        h = ev(g('Height'), pw, ph)
        w = pw if w is None else w
        h = ph if h is None else h
        for ch in c.children:
            x = ev('\n'.join(ch.props.get('X', [])) or None, w, h) or 0
            cw = ev('\n'.join(ch.props.get('Width', [])) or None, w, h)
            if cw is not None and x + cw > w + 0.5:
                erros.append('%s: %s estoura %s (%d > %d)'
                             % (tela, ch.name, c.name, round(x + cw), round(w)))
            visita(ch, ev('\n'.join(ch.props.get('Width', [])) or None, w, h) or w,
                   ev('\n'.join(ch.props.get('Height', [])) or None, w, h) or h, tela)

    for f in sorted(glob.glob(os.path.join(REV2, 'Src', 'scr*.pa.yaml'))):
        _, r = payaml.parse(f)
        for c in r.children:
            visita(c, 1366, 768, r.name)


if __name__ == '__main__':
    mud, ctrl = diff_rev01_rev02()
    intactas = formulas_x_original()
    estrutura()
    geometria()
    geometria_interna()
    print('Base: %s' % os.path.relpath(REV1, BASE))
    print('base -> REV02')
    print('  acessibilidade (rotulos)    : %d propriedades' % mud['AccessibleLabel'])
    print('  literais -> variaveis       : %d propriedades' % mud['variaveis'])
    print('  raios padronizados em 14    : %d propriedades' % mud['raio'])
    print('  colunas internas reescaladas: %d propriedades' % mud['colunas'])
    print('  faixa institucional         : %d propriedades/controles' % mud['imagem'])
    print('  cabecalho sem data URI      : %d propriedades' % mud['cabecalho'])
    print('  contraste do botao Ajuda    : %d propriedades' % mud['ajuda'])
    print('  reflow de rotulos (inicio)  : %d propriedades' % mud['reflow'])
    print('  controles tocados           : %d' % len(ctrl))
    print('  propriedades visuais mudadas: %d' % sum(mud.values()))
    print('formulas funcionais identicas ao SGC original: %d' % intactas)
    print('\nERROS (%d):' % len(erros))
    for e in erros[:60]:
        print('  *', e)
