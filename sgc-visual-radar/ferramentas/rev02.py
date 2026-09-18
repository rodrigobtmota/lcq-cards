# -*- coding: utf-8 -*-
"""REV02 — endurecimento tecnico e acabamento visual.

Aplicado sobre o resultado da migracao (mesmo pipeline), em Src/*.pa.yaml e
Controls/*.json simultaneamente, via a camada de operacoes `ops.Screen`.
"""
import os, re, json, shutil, uuid
import design as D

# ---------------------------------------------------------------- 1. acessibilidade
BOTAO_CLASSICO = 'Classic/Button@2.2.0'


def accessible_menu(sc, btn):
    """Acessibilidade compativel com o Source Code schema.

    `AccessibleLabel` nao e propriedade valida de `Classic/Button@2.2.0`
    (erro PA2108 na importacao real). Nos botoes classicos a identificacao
    acessivel fica no proprio `Text` e no `Tooltip`; `AccessibleLabel` e usado
    apenas nos tipos que o aceitam (Image, Gallery).
    """
    # menu lateral: texto real (invisivel, pois a cor e transparente) + tooltip
    sc.set(btn, {'Text': 'ThisItem.Rotulo', 'Tooltip': 'ThisItem.Rotulo'})
    n = 1
    for cy in list(sc.y.walk()):
        if cy.name.startswith('btnAjudaX'):
            sc.set(cy.name, {'Tooltip': '"Fechar a ajuda"'})
            n += 1
    return n


def remover_accessiblelabel_classico(sc):
    """PA2108: remove AccessibleLabel de todo Classic/Button@2.2.0."""
    removidos = []
    for cy in list(sc.y.walk()):
        if dict(cy.meta).get('Control') == BOTAO_CLASSICO and 'AccessibleLabel' in cy.props:
            sc.set(cy.name, {'AccessibleLabel': None})
            removidos.append(cy.name)
    return removidos


# ---------------------------------------------------------------- 2. tokens -> variaveis
VARS = {
    'RGBA(14, 42, 74, 1)':    'varCorPrimaria',
    'RGBA(28, 85, 130, 1)':   'varCorSecundaria',
    'RGBA(245, 247, 250, 1)': 'varCorFundo',
    'RGBA(32, 42, 53, 1)':    'varCorTexto',
    'RGBA(101, 115, 132, 1)': 'varCorTextoSuave',
    'RGBA(216, 225, 234, 1)': 'varCorBorda',
    'RGBA(46, 125, 50, 1)':   'varCorVerde',
    'RGBA(202, 138, 4, 1)':   'varCorAmarelo',
    'RGBA(180, 83, 9, 1)':    'varCorLaranja',
    'RGBA(185, 28, 28, 1)':   'varCorVermelho',
}
BRANCO = 'RGBA(255, 255, 255, 1)'


def _e_propriedade_de_cor(p):
    return ('Color' in p or 'Fill' in p) and 'DropShadow' not in p


def _e_card(cy):
    """Container/retangulo que representa um card institucional do Radar."""
    tpl = dict(cy.meta).get('Control', '')
    if not (tpl.startswith('GroupContainer') or tpl.startswith('Rectangle')):
        return False
    fill = '\n'.join(cy.props.get('Fill', [])).lstrip('=')
    alt = '\n'.join(cy.props.get('Height', [])).lstrip('=')
    if fill not in (BRANCO, 'varCorCard'):
        # cards de acao com fundo institucional tambem seguem o raio de card
        if not (tpl.startswith('GroupContainer') and alt not in ('', '1') and
                fill in ('varCorSecundaria', 'varCorPrimaria', 'RGBA(28, 85, 130, 1)',
                         'RGBA(14, 42, 74, 1)')):
            return False
    esp = '\n'.join(cy.props.get('BorderThickness', ['0'])).lstrip('=')
    tem_raio = 'RadiusTopLeft' in cy.props
    return tem_raio and esp not in ('0', '')


def usar_variaveis(sc):
    """Troca literais por variaveis de tema apenas em propriedades de cor."""
    trocas = 0
    for cy in list(sc.y.walk()):
        if cy is sc.y:
            alvo = {p: '\n'.join(v) for p, v in cy.props.items() if _e_propriedade_de_cor(p)}
        else:
            alvo = {p: '\n'.join(v) for p, v in cy.props.items() if _e_propriedade_de_cor(p)}
        novos = {}
        card = cy is not sc.y and _e_card(cy)
        for p, val in alvo.items():
            v = val[1:] if val.startswith('=') else val
            orig = v
            for lit, var in VARS.items():
                if lit in v:
                    v = v.replace(lit, var)
            # branco -> varCorCard somente no Fill de um card institucional
            if card and p == 'Fill' and v == BRANCO:
                v = 'varCorCard'
            if v != orig:
                novos[p] = v
                trocas += len(re.findall(r'varCor', v)) - len(re.findall(r'varCor', orig))
        if novos:
            if cy is sc.y:
                sc.screen_set(novos)
            else:
                sc.set(cy.name, novos)
    return trocas


# ---------------------------------------------------------------- 3. raios
NAO_ARREDONDAR = ('bdg', 'recAcento', 'recProg', 'recDiv', 'recLinha', 'ico',
                  'recNav', 'recSep', 'recBarra')


def padronizar_raios(sc):
    """Cards institucionais em 14 px, botoes/campos secundarios em 10 px.
    Menu 13, modal 18, pills, barras e divisores intactos."""
    ajustes = []
    for cy in list(sc.y.walk()):
        if cy is sc.y or cy.name.startswith(NAO_ARREDONDAR) or cy.name.startswith('grpAjuda'):
            continue
        tpl = dict(cy.meta).get('Control', '')
        atual = '\n'.join(cy.props.get('RadiusTopLeft', [])).lstrip('=')
        if atual not in ('4', '8'):
            continue
        # botao transparente que cobre um card inteiro acompanha o raio do card
        cobre_card = (tpl.startswith('Classic/Button')
                      and '\n'.join(cy.props.get('Width', [])).lstrip('=') == 'Parent.Width'
                      and '\n'.join(cy.props.get('Height', [])).lstrip('=') == 'Parent.Height')
        if tpl.startswith('GroupContainer') or cobre_card:
            novo = '14'
        elif tpl.startswith(('Classic/Button', 'Classic/TextInput', 'Rectangle')):
            novo = '10'
        else:
            continue
        sc.set(cy.name, {'RadiusTopLeft': novo, 'RadiusTopRight': novo,
                         'RadiusBottomLeft': novo, 'RadiusBottomRight': novo})
        ajustes.append((cy.name, atual))
    for cy in list(sc.y.walk()):
        if cy is sc.y:
            continue
        n = cy.name
        if n.startswith(NAO_ARREDONDAR) or n.startswith('grpAjuda') or n.startswith('htmlMenu'):
            continue
        if not _e_card(cy):
            continue
        atual = '\n'.join(cy.props.get('RadiusTopLeft', [])).lstrip('=')
        if atual == '14':
            continue
        try:
            if int(float(atual)) < 6:      # cantos tecnicos (barras, divisores)
                continue
        except ValueError:
            continue
        sc.set(n, {'RadiusTopLeft': '14', 'RadiusTopRight': '14',
                   'RadiusBottomLeft': '14', 'RadiusBottomRight': '14'})
        ajustes.append((n, atual))
    return ajustes


# ---------------------------------------------------------------- 3b. colunas internas
CANVAS = (1366, 768)


def _ev(expr, pw, ph):
    if expr is None:
        return None
    s = expr.strip().lstrip('=')
    s = (s.replace('Parent.TemplateWidth', str(pw)).replace('Parent.TemplateHeight', str(ph))
          .replace('Parent.Width', str(pw)).replace('Parent.Height', str(ph)))
    if re.search(r'[A-Za-z]', s):
        return None
    try:
        return float(eval(s))
    except Exception:
        return None


def _prop(cy, p):
    v = '\n'.join(cy.props.get(p, []))
    return v or None


def corrigir_colunas(sc):
    """Reescala colunas fixas que estouram containers estreitados pelo menu lateral."""
    ajustes = []

    def visita(cy, pw, ph):
        w = _ev(_prop(cy, 'Width'), pw, ph)
        h = _ev(_prop(cy, 'Height'), pw, ph)
        w = pw if w is None else w
        h = ph if h is None else h
        fixos = []
        extensao = 0.0
        for ch in cy.children:
            bx, bw = _prop(ch, 'X'), _prop(ch, 'Width')
            # apenas colunas de posicao fixa; ancoradas a direita ou relativas ficam intactas
            if bw is None or re.search(r'[A-Za-z]', bw.lstrip('=')):
                continue
            if bx is not None and re.search(r'[A-Za-z]', bx.lstrip('=')):
                continue
            x = _ev(bx, w, h) or 0
            cw = _ev(bw, w, h)
            if cw is None:
                continue
            fixos.append((ch, x, cw))
            extensao = max(extensao, x + cw)
        if extensao > w + 0.5 and fixos:
            f = (w - 8) / extensao
            for ch, x, cw in fixos:
                novo = {}
                if x > 0:
                    novo['X'] = '%g' % round(x * f)
                novo['Width'] = '%g' % round(cw * f)
                sc.set(ch.name, novo)
                ajustes.append(ch.name)
        for ch in cy.children:
            cx = _ev(_prop(ch, 'Width'), w, h)
            visita(ch, cx if cx is not None else w, _ev(_prop(ch, 'Height'), w, h) or h)

    for c in sc.y.children:
        visita(c, CANVAS[0], CANVAS[1])
    return ajustes


# ---------------------------------------------------------------- 3c. rotulos cortados
def corrigir_textos_inicio(sc):
    """Reflow dos rotulos da tela inicial que nao cabiam na altura herdada.
    Apenas geometria: nenhum texto, formula ou altura de card foi alterada."""
    ajustes = []
    for cy in list(sc.y.walk()):
        n = cy.name
        novo = None
        if n.startswith('lblCard') and n.endswith('Titulo'):
            novo = {'Y': '14', 'Height': '36', 'Width': 'Parent.Width - 40'}
        elif n.startswith('lblQtd'):
            novo = {'Y': '52', 'Height': '46'}
        elif n.startswith('lblKpiLegenda'):
            novo = {'Y': 'Parent.Height - 36', 'Height': '32'}
        elif n.startswith('lblAcao') and n.endswith('Titulo'):
            novo = {'Y': '18', 'Height': '28'}
        elif n.startswith('lblAcao') and n.endswith('Texto'):
            novo = {'Y': '50', 'Height': '80', 'Width': 'Parent.Width - 40'}
        elif n.startswith('icoAcao'):
            novo = {'Y': 'Parent.Height - 32'}
        if novo:
            sc.set(n, novo)
            ajustes.append(n)
    return ajustes


# ---------------------------------------------------------------- 4. faixa institucional local
RECURSO = 'FaixaCabecalhoLCQ'
ARQUIVO_FONTE = 'faixa_cabecalho_lcq.png'


def registrar_faixa(out_dir, tools_dir):
    """Registra a faixa do cabecalho como recurso LOCAL do SGC (sem vinculo com o Radar)."""
    nome_arquivo = '%s.png' % uuid.uuid5(uuid.NAMESPACE_URL, 'sgc-lcq-rj/faixa-cabecalho')
    destino = os.path.join(out_dir, 'Assets', 'Images')
    os.makedirs(destino, exist_ok=True)
    shutil.copy(os.path.join(tools_dir, ARQUIVO_FONTE), os.path.join(destino, nome_arquivo))
    res_p = os.path.join(out_dir, 'References', 'Resources.json')
    res = json.load(open(res_p, encoding='utf-8'))
    res['Resources'] = [r for r in res['Resources'] if r.get('Name') not in (RECURSO, 'Nav')]
    res['Resources'].append({
        'Name': RECURSO, 'Schema': 'i', 'IsSampleData': False, 'IsWritable': False,
        'Type': 'ResourceInfo', 'FileName': nome_arquivo,
        'Path': 'Assets\\Images\\' + nome_arquivo, 'Content': 'Image',
        'ResourceKind': 'LocalFile', 'RootPath': ''})
    json.dump(res, open(res_p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    # remove qualquer imagem herdada do pacote do Radar
    for f in os.listdir(destino):
        if f != nome_arquivo:
            os.remove(os.path.join(destino, f))
    return nome_arquivo


# ---------------------------------------------------------------- 5. metadado de empacotamento
def packed_json(out_dir, versao):
    json.dump({"PackedStructureVersion": "0.1",
               "LastPackedDateTimeUtc": "2026-09-18 12:00:00Z",
               "PackingClient": {"Name": "Custom Canvas Package Builder (scripts do projeto SGC LCQ RJ)",
                                 "Version": versao},
               "LoadConfiguration": {"LoadFromYaml": True}},
              open(os.path.join(out_dir, 'packed.json'), 'w', encoding='utf-8'), indent=2)
