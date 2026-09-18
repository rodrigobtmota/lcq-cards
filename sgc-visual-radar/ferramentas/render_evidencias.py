# -*- coding: utf-8 -*-
"""Gera evidencias visuais a partir dos FONTES da REV02.

Cada retangulo, cor, raio, tamanho de fonte e texto vem das propriedades reais
de Src/*.pa.yaml. HtmlViewer usa o HTML real; Image usa o arquivo real do
recurso. NAO e um screenshot do Power Apps: valores dinamicos (ThisItem, dados
do SharePoint) nao podem ser resolvidos fora do Studio e aparecem como amostra.
"""
import os, re, sys, json, base64, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import payaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(BASE, 'build')
W, H = 1366, 768

TEMA = {
    'varCorPrimaria': 'RGBA(14, 42, 74, 1)', 'varCorSecundaria': 'RGBA(28, 85, 130, 1)',
    'varCorFundo': 'RGBA(245, 247, 250, 1)', 'varCorCard': 'RGBA(255, 255, 255, 1)',
    'varCorTexto': 'RGBA(32, 42, 53, 1)', 'varCorTextoSuave': 'RGBA(101, 115, 132, 1)',
    'varCorBorda': 'RGBA(216, 225, 234, 1)', 'varCorVerde': 'RGBA(46, 125, 50, 1)',
    'varCorAmarelo': 'RGBA(202, 138, 4, 1)', 'varCorLaranja': 'RGBA(180, 83, 9, 1)',
    'varCorVermelho': 'RGBA(185, 28, 28, 1)',
}
AMOSTRAS = {  # valores de exemplo para colunas dinamicas das galerias
    'Rotulo': ['Início', 'Qualificações', 'Histórico', 'Módulos', 'Cobertura'],
    'Sigla': ['IN', 'QL', 'HI', 'MD', 'CB'],
    'Chave': ['Inicio', 'Qualificacoes', 'Historico', 'Modulos', 'Cobertura'],
}


MENU_CTX = [False]   # True enquanto renderiza a galeria do menu lateral


def val(c, p):
    v = '\n'.join(c.props.get(p, []))
    return v[1:].strip() if v.startswith('=') else (v.strip() or None)


def num(expr, pw, ph):
    if expr is None:
        return None
    e = expr.replace('Parent.Width', str(pw)).replace('Parent.Height', str(ph))
    e = e.replace('Parent.TemplateWidth', str(pw)).replace('Parent.TemplateHeight', str(ph))
    e = re.sub(r'Self\.\w+', '0', e)
    if re.search(r'[A-Za-z]', e):
        return None
    try:
        return float(eval(e))
    except Exception:
        return None


def cor(expr, padrao=None):
    if expr is None:
        return padrao
    for var, lit in TEMA.items():
        expr = expr.replace(var, lit)
    m = re.search(r'RGBA\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)', expr)
    if m:
        r, g, b, a = m.groups()
        return 'rgba(%s,%s,%s,%s)' % (r, g, b, a)
    m = re.search(r'#[0-9A-Fa-f]{6}', expr)
    return m.group(0) if m else padrao


def texto(expr, idx=0):
    if expr is None:
        return ''
    e = expr.strip()
    if e.startswith('"') and e.endswith('"') and e.count('"') == 2:
        return html.escape(e[1:-1])
    if MENU_CTX[0]:
        for col, vals in AMOSTRAS.items():
            if 'ThisItem.' + col in e:
                return html.escape(vals[idx % len(vals)])
    if re.fullmatch(r'"[^"]*"', e):
        return html.escape(e[1:-1])
    return '<span style="opacity:.40">&#8212;</span>'


def _split_topo(s, sep):
    """Divide respeitando parenteses, chaves e strings."""
    partes, nivel, ins, atual = [], 0, False, ''
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == '"':
            ins = not ins
        if not ins:
            if ch in '({[':
                nivel += 1
            elif ch in ')}]':
                nivel -= 1
            elif ch == sep and nivel == 0:
                partes.append(atual); atual = ''; i += 1; continue
        atual += ch
        i += 1
    partes.append(atual)
    return partes


def _eval(expr, env, idx):
    """Avaliador minimo de expressao de texto Power Fx (With/If/&/Coalesce/literal)."""
    e = expr.strip()
    if e.startswith('With(') and e.endswith(')'):
        interno = e[5:-1]
        reg, corpo = _split_topo(interno, ',')[0], ','.join(_split_topo(interno, ',')[1:])
        # o primeiro argumento e um registro {a: x, b: y}
        campos = _split_topo(reg.strip()[1:-1], ',')
        novo = dict(env)
        for campo in campos:
            if ':' not in campo:
                continue
            k, v = campo.split(':', 1)
            novo[k.strip()] = _eval(v, novo, idx)
        return _eval(corpo, novo, idx)
    partes = _split_topo(e, '&')
    if len(partes) > 1:
        return ''.join(_eval(p, env, idx) for p in partes)
    if e.startswith('If(') and e.endswith(')'):
        args = [a.strip() for a in _split_topo(e[3:-1], ',')]
        cond = args[0]
        m = re.search(r'ThisItem\.Chave\s*=\s*"(\w*)"', cond)
        if m:
            ok = AMOSTRAS['Chave'][idx % 5] == m.group(1)
        else:
            ok = env.get(cond.strip()) in (True, 'true')
        return _eval(args[1] if ok else (args[2] if len(args) > 2 else '""'), env, idx)
    if e.startswith('Coalesce(') and e.endswith(')'):
        for a in _split_topo(e[9:-1], ','):
            v = _eval(a, env, idx)
            if v:
                return v
        return ''
    if e.startswith('"') and e.endswith('"'):
        return e[1:-1].replace('""', '"')
    for col, vals in AMOSTRAS.items():
        if e == 'ThisItem.' + col:
            return vals[idx % len(vals)]
    if e in env:
        v = env[e]
        return v if isinstance(v, str) else str(v)
    if re.fullmatch(r'ThisItem\.\w+\s*=\s*"\w*"', e):
        m = re.search(r'"(\w*)"', e)
        return AMOSTRAS['Chave'][idx % 5] == m.group(1)
    return ''


def html_literal(expr, idx=0):
    """Resolve a expressao do HtmlViewer (With/If/concatenacao) para o HTML final."""
    try:
        s = _eval(expr, {}, idx)
        if isinstance(s, str) and '<' in s:
            return s
    except Exception:
        pass
    out, ins = '', False
    for ch in expr:
        if ch == '"':
            ins = not ins
        elif ins:
            out += ch
    for col, vals in AMOSTRAS.items():
        out = out.replace('ThisItem.' + col, vals[idx % len(vals)])
    return out


def selecao_menu(expr, idx):
    m = re.search(r'ThisItem\.Chave = "(\w*)"', expr or '')
    if not m:
        return None
    return AMOSTRAS['Chave'][idx % 5] == m.group(1)


def render(c, pw, ph, idx=0, prof=0):
    tpl = dict(c.meta).get('Control', '')
    x = num(val(c, 'X'), pw, ph) or 0
    y = num(val(c, 'Y'), pw, ph) or 0
    w = num(val(c, 'Width'), pw, ph)
    h = num(val(c, 'Height'), pw, ph)
    if w is None:
        w = 100
    if h is None:
        h = 40
    if c.name.endswith('Resultados'):      # painel flutuante dependente de digitacao
        return ''
    vis = val(c, 'Visible')
    if vis in ('false', 'locAjuda', 'varMostrarAjuda'):
        return ''
    if vis and ('locAjuda' in vis or 'varMostrar' in vis):
        return ''
    fill = cor(val(c, 'Fill'), 'transparent')
    borda = cor(val(c, 'BorderColor'))
    esp = num(val(c, 'BorderThickness'), pw, ph) or 0
    raio = num(val(c, 'RadiusTopLeft'), pw, ph) or 0
    estilo = ("position:absolute;left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;"
              "box-sizing:border-box;overflow:hidden;background:%s;border-radius:%.0fpx;"
              % (x, y, w, h, fill, raio))
    if esp and borda:
        estilo += 'border:%.0fpx solid %s;' % (esp, borda)
    if val(c, 'DropShadow') and 'None' not in val(c, 'DropShadow'):
        estilo += 'box-shadow:0 2px 7px rgba(15,23,42,.08);'
    dentro = ''
    if tpl.startswith('HtmlViewer'):
        dentro = html_literal(val(c, 'HtmlText'), idx)
    elif tpl.startswith('Image'):
        res = json.load(open(os.path.join(BUILD, 'References', 'Resources.json'),
                             encoding='utf-8'))['Resources'][0]
        p = os.path.join(BUILD, 'Assets', 'Images', res['FileName'])
        b64 = base64.b64encode(open(p, 'rb').read()).decode()
        dentro = ("<img src='data:image/png;base64,%s' style='width:100%%;height:100%%;"
                  "object-fit:fill'>" % b64)
    elif tpl.startswith(('Label', 'Classic/Button', 'Classic/TextInput', 'ComboBox')):
        t = texto(val(c, 'Text') or val(c, 'HintText'), idx)
        tam = (num(val(c, 'Size'), pw, ph) or 11) * 4 / 3.0
        cr = cor(val(c, 'Color'), '#202A35')
        peso = '700' if 'Bold' in (val(c, 'FontWeight') or '') else \
               ('600' if 'Semibold' in (val(c, 'FontWeight') or '') else '400')
        al = val(c, 'Align') or ''
        just = 'flex-end' if 'Right' in al else ('center' if 'Center' in al else 'flex-start')
        pad = 8 if tpl.startswith('Classic/Button') else 0
        dentro = ("<div style='width:100%%;height:100%%;display:flex;align-items:center;"
                  "justify-content:%s;padding:0 %dpx;box-sizing:border-box;color:%s;"
                  "font:%s %.1fpx Segoe UI,Arial;line-height:1.25'>%s</div>"
                  % (just, pad, cr, peso, tam, t))
    elif tpl.startswith('Classic/Icon'):
        dentro = ("<div style='width:100%%;height:100%%;border:2px solid %s;border-radius:4px;"
                  "box-sizing:border-box;opacity:.65'></div>" % cor(val(c, 'Color'), '#657384'))
    filhos = ''
    if tpl.startswith('Gallery'):
        ts = num(val(c, 'TemplateSize'), pw, ph) or 64
        tp = num(val(c, 'TemplatePadding'), pw, ph) or 0
        wrap = num(val(c, 'WrapCount'), pw, ph) or 1
        horizontal = wrap > 1
        itens = val(c, 'Items') or ''
        fixos = len(re.findall(r'\{\s*\w+\s*:', itens)) if itens.strip().startswith('Table(') else 0
        n = int(wrap) if horizontal else max(1, min(6, int(h // (ts + tp))))
        if fixos:
            n = min(n, len(re.findall(r'\}\s*,|\}\s*\)', itens)))
        MENU_CTX[0] = 'Sigla' in (itens or '')
        for i in range(n):
            tw = (w / wrap) if horizontal else w
            th = ts
            ox = i * tw if horizontal else 0
            oy = 0 if horizontal else i * (ts + tp)
            inner = ''.join(render(ch, tw, th, i, prof + 1) for ch in c.children)
            filhos += ("<div style='position:absolute;left:%.1fpx;top:%.1fpx;width:%.1fpx;"
                       "height:%.1fpx'>%s</div>" % (ox, oy, tw, th, inner))
        MENU_CTX[0] = False
    else:
        filhos = ''.join(render(ch, w, h, idx, prof + 1) for ch in c.children)
    return "<div style='%s'>%s%s</div>" % (estilo, dentro, filhos)


def render_screen(nome):
    _, r = payaml.parse(os.path.join(BUILD, 'Src', nome + '.pa.yaml'))
    fundo = cor(val(r, 'Fill'), '#F5F7FA')
    corpo = ''.join(render(c, W, H) for c in r.children)
    return ("<html><body style='margin:0'><div style='position:relative;width:%dpx;height:%dpx;"
            "background:%s;font-family:Segoe UI,Arial;overflow:hidden'>%s</div></body></html>"
            % (W, H, fundo, corpo))


if __name__ == '__main__':
    saida = os.path.join(BASE, 'evidencias')
    os.makedirs(saida, exist_ok=True)
    for nome in ('scrInicio', 'scrQualificacoes', 'scrAvaliacao', 'scrCobertura'):
        open(os.path.join(saida, nome + '.html'), 'w', encoding='utf-8').write(render_screen(nome))
        print('html gerado:', nome)
