"""Converte a árvore avaliada pelo simulador em HTML posicionado (aproximação visual do Canvas)."""
import base64
import html
import os

ICONS = {'Home': '⌂', 'DocumentWithContent': '▤', 'Add': '+', 'Clock': '◷', 'Waffle': '▦', 'Trending': '↗', 'Settings': '⚙',
         'Reset': '↻', 'Search': '⌕', 'CalendarBlank': '▭', 'Information': 'ⓘ', 'ChevronLeft': '‹', 'ChevronRight': '›'}
FONT = "'Open Sans','Segoe UI',Arial,sans-serif"


def _asset(name, assets_dir, cache={}):
    if name.startswith('data:'):
        return name
    if not name.startswith('asset:'):
        return ''
    fn = name[6:]
    if fn not in cache:
        p = os.path.join(assets_dir, fn)
        cache[fn] = 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode() if os.path.exists(p) else ''
    return cache[fn]


def _num(n, k, d=0):
    v = n.get(k)
    return d if v is None else v


def _radius(n):
    return f"border-radius:{_num(n,'RadiusTopLeft')}px {_num(n,'RadiusTopRight')}px {_num(n,'RadiusBottomRight')}px {_num(n,'RadiusBottomLeft')}px;"


def _weight(n, default=600):
    fw = n.get('FontWeight') or ''
    return {'FontWeight.Bold': 700, 'FontWeight.Semibold': 600, 'FontWeight.Normal': 400, 'FontWeight.Lighter': 300}.get(fw, default)


def node_html(n, assets_dir):
    if not n.get('visible', True):
        return ''
    t = n['type']
    x, y, w, h = _num(n, 'X'), _num(n, 'Y'), _num(n, 'Width'), _num(n, 'Height')
    base = f"position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;"
    kids = sorted(n.get('children') or [], key=lambda c: _num(c, 'ZIndex'))
    inner = ''.join(node_html(c, assets_dir) for c in kids)
    disabled = (n.get('DisplayMode') == 'DisplayMode.Disabled')
    fill = (n.get('DisabledFill') if disabled and n.get('DisabledFill') else n.get('Fill')) or 'transparent'
    color = (n.get('DisabledColor') if disabled and n.get('DisabledColor') else n.get('Color')) or '#000'
    bcol = (n.get('DisabledBorderColor') if disabled and n.get('DisabledBorderColor') else n.get('BorderColor')) or 'transparent'
    bth = _num(n, 'BorderThickness')
    border = f"border:{bth}px solid {bcol};" if bth else ''
    title = f' title="{html.escape(n["Tooltip"])}"' if n.get('Tooltip') else ''
    data = f' data-name="{n["name"]}"'
    if t == 'screen':
        return f'<div{data} style="position:relative;width:{w}px;height:{h}px;overflow:hidden;background:{fill};font-family:{FONT};">{inner}</div>'
    if t == 'groupContainer':
        return f'<div{data} style="{base}background:{fill};{border}{_radius(n)}overflow:hidden;">{inner}</div>'
    if t == 'rectangle':
        return f'<div{data} style="{base}background:{fill};{border}"></div>'
    if t == 'htmlViewer':
        pad = f"padding:{_num(n,'PaddingTop')}px {_num(n,'PaddingRight')}px {_num(n,'PaddingBottom')}px {_num(n,'PaddingLeft')}px;"
        return (f'<div{data}{title} class="hv" style="{base}{pad}background:{fill};color:{color};font-size:{_num(n,"Size",13)}pt;'
                f'overflow:hidden;font-family:{FONT};">{n.get("HtmlText") or ""}</div>')
    if t == 'button':
        pad = f"padding:0 {_num(n,'PaddingRight')}px 0 {_num(n,'PaddingLeft')}px;"
        just = 'flex-start' if n.get('Align') == 'Align.Left' else 'center'
        und = 'text-decoration:underline;' if n.get('Underline') == 'true' else ''
        return (f'<div{data}{title} style="{base}{pad}background:{fill};color:{color};{border}{_radius(n)}display:flex;align-items:center;'
                f'justify-content:{just};text-align:center;font-size:{_num(n,"Size",13)}pt;font-weight:{_weight(n)};{und}line-height:1.15;overflow:hidden;">'
                f'{html.escape(n.get("Text") or "")}</div>')
    if t == 'text':
        txt = n.get('Text') or ''
        hint = not txt
        shown = html.escape(n.get('HintText') or '') if hint else html.escape(txt).replace('\n', '<br/>')
        return (f'<div{data} style="{base}background:{n.get("Fill") or "#fff"};{border}{_radius(n)}padding:{_num(n,"PaddingTop",5)}px {_num(n,"PaddingRight",5)}px 0 {_num(n,"PaddingLeft",5)}px;'
                f'color:{"#8a94a3" if hint else color};font-size:{_num(n,"Size",13)}pt;line-height:1.3;overflow:hidden;">{shown}</div>')
    if t == 'image':
        src = _asset(n.get('Image') or '', assets_dir)
        fit = {'ImagePosition.Stretch': 'fill', 'ImagePosition.Fill': 'cover', 'ImagePosition.Fit': 'contain'}.get(n.get('ImagePosition'), 'contain')
        return f'<img{data} src="{src}" style="{base}object-fit:{fit};"/>' if src else f'<div{data} style="{base}"></div>'
    if t == 'icon':
        g = ICONS.get((n.get('Icon') or '').split('.')[-1], '•')
        return (f'<div{data}{title} style="{base}color:{color};display:flex;align-items:center;justify-content:center;font-size:{max(10, h*0.8)}px;line-height:1;">{g}</div>')
    if t == 'gallery':
        tw, th = n.get('TemplateWidth') or w, n.get('TemplateHeight') or 40
        wc = int(_num(n, 'WrapCount', 1) or 1)
        items = ''
        for it in n.get('items') or []:
            i = it['index']
            ix, iy = (i % wc) * tw, (i // wc) * th
            if iy > h + th:
                break
            ch = ''.join(node_html(c, assets_dir) for c in sorted(it['children'], key=lambda c: _num(c, 'ZIndex')))
            items += f'<div style="position:absolute;left:{ix}px;top:{iy}px;width:{tw}px;height:{th}px;">{ch}</div>'
        total_h = ((n.get('count') or 0) + wc - 1) // wc * th
        sb = (f'<div style="position:absolute;right:1px;top:2px;width:5px;height:{max(20, h*h/total_h-4)}px;border-radius:3px;background:rgba(0,0,0,.25);"></div>'
              if total_h > h + 1 else '')
        return f'<div{data} style="{base}background:{fill};{border}overflow:hidden;">{items}{sb}</div>'
    return f'<div{data} style="{base}"></div>'


def page(tree, assets_dir, title=''):
    return ('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0}.hv b{font-weight:700}</style>'
            f'<title>{html.escape(title)}</title></head><body>' + node_html(tree, assets_dir) + '</body></html>')
