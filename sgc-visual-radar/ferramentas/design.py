# -*- coding: utf-8 -*-
"""Design system extraido do Radar de Liderancas LCQ V2."""

# ---- tokens (valores lidos diretamente do Radar) ----
PRIM      = 'RGBA(14, 42, 74, 1)'        # #0E2A4A
SEC       = 'RGBA(28, 85, 130, 1)'       # #1C5582
FUNDO     = 'RGBA(245, 247, 250, 1)'     # #F5F7FA
CARD      = 'RGBA(255, 255, 255, 1)'
TEXTO     = 'RGBA(32, 42, 53, 1)'        # #202A35
TEXTO2    = 'RGBA(101, 115, 132, 1)'     # #657384
BORDA     = 'RGBA(216, 225, 234, 1)'     # #D8E1EA
VERDE     = 'RGBA(46, 125, 50, 1)'       # #2E7D32
AMARELO   = 'RGBA(202, 138, 4, 1)'       # #CA8A04
LARANJA   = 'RGBA(180, 83, 9, 1)'        # #B45309
VERMELHO  = 'RGBA(185, 28, 28, 1)'       # #B91C1C
FONTE     = "Font.'Open Sans'"

NAVBG = open(__file__.replace('design.py', 'navbg_datauri.txt'), encoding='utf-8').read()

# ---- mapa de cores do SGC antigo -> paleta Radar ----
CORES = {
    'RGBA(0, 18, 107, 1)':    PRIM,
    'RGBA(0, 18, 107, 0.35)': 'RGBA(14, 42, 74, 0.35)',
    'RGBA(0, 87, 184, 1)':    SEC,
    'RGBA(0, 87, 184, 0.06)': 'RGBA(28, 85, 130, 0.06)',
    'RGBA(0, 87, 184, 0.05)': 'RGBA(28, 85, 130, 0.05)',
    'RGBA(0, 87, 184, 0.04)': 'RGBA(28, 85, 130, 0.04)',
    'RGBA(0, 72, 153, 1)':    PRIM,
    'RGBA(15, 108, 189, 1)':  PRIM,
    'RGBA(15, 43, 91, 1)':    PRIM,
    'RGBA(71, 158, 245, 1)':  SEC,
    'RGBA(246, 247, 249, 1)': FUNDO,
    'RGBA(244, 246, 249, 1)': 'RGBA(241, 245, 249, 1)',
    'RGBA(244, 248, 253, 1)': 'RGBA(234, 241, 248, 1)',   # #EAF1F8
    'RGBA(250, 250, 250, 1)': FUNDO,
    'RGBA(226, 229, 234, 1)': BORDA,
    'RGBA(229, 232, 236, 1)': BORDA,
    'RGBA(222, 226, 232, 1)': BORDA,
    'RGBA(236, 238, 242, 1)': 'RGBA(233, 238, 244, 1)',   # #E9EEF4
    'RGBA(241, 243, 246, 1)': 'RGBA(238, 242, 246, 1)',   # #EEF2F6
    'RGBA(199, 208, 222, 1)': 'RGBA(215, 227, 241, 1)',   # #D7E3F1
    'RGBA(200, 205, 212, 1)': BORDA,
    'RGBA(191, 196, 204, 1)': 'RGBA(148, 163, 184, 1)',   # #94A3B8
    'RGBA(51, 51, 51, 1)':    TEXTO,
    'RGBA(32, 33, 36, 1)':    TEXTO,
    'RGBA(76, 76, 76, 1)':    'RGBA(36, 59, 83, 1)',      # #243B53 (titulo de card)
    'RGBA(77, 86, 99, 1)':    'RGBA(52, 71, 92, 1)',      # #34475C
    'RGBA(128, 128, 128, 1)': TEXTO2,
    'RGBA(140, 140, 140, 1)': TEXTO2,
    'RGBA(90, 98, 110, 1)':   'RGBA(82, 101, 122, 1)',    # #52657A
    'RGBA(150, 158, 170, 1)': 'RGBA(82, 101, 122, 1)',
    'RGBA(106, 168, 40, 1)':  VERDE,
    'RGBA(57, 94, 13, 1)':    'RGBA(37, 107, 53, 1)',     # #256B35
    'RGBA(211, 244, 162, 1)': 'RGBA(198, 228, 204, 1)',
    'RGBA(245, 253, 232, 1)': 'RGBA(231, 243, 233, 1)',   # #E7F3E9
    'RGBA(230, 160, 20, 1)':  AMARELO,
    'RGBA(112, 76, 6, 1)':    'RGBA(128, 96, 0, 1)',      # #806000
    'RGBA(166, 95, 0, 1)':    'RGBA(161, 78, 8, 1)',      # #A14E08
    'RGBA(255, 248, 234, 1)': 'RGBA(255, 247, 216, 1)',   # #FFF7D8
    'RGBA(255, 244, 204, 1)': 'RGBA(255, 244, 220, 1)',   # #FFF4DC
    'RGBA(255, 238, 204, 1)': 'RGBA(255, 240, 223, 1)',   # #FFF0DF
    'RGBA(155, 54, 54, 1)':   'RGBA(169, 21, 21, 1)',     # #A91515
    'RGBA(196, 80, 80, 1)':   VERMELHO,
    'RGBA(200, 170, 170, 1)': 'RGBA(232, 190, 190, 1)',
    'RGBA(255, 240, 240, 1)': 'RGBA(251, 231, 231, 1)',   # #FBE7E7
    'RGBA(255, 194, 194, 1)': 'RGBA(240, 190, 190, 1)',
    'RGBA(229, 242, 255, 1)': 'RGBA(234, 241, 248, 1)',   # #EAF1F8
    'RGBA(229, 242, 255, 0.6)': 'RGBA(234, 241, 248, 0.6)',
    'RGBA(195, 230, 255, 1)': 'RGBA(214, 225, 236, 1)',   # #D6E1EC
}


def header_html(titulo):
    """Cabecalho institucional 90px, mesmo tratamento grafico do Nav_bg do Radar."""
    return ('"<div style=\'width:100%;height:100%;box-sizing:border-box;display:flex;'
            "align-items:center;padding:0 28px;background:#0E2A4A url(" + NAVBG + ") "
            "no-repeat center/cover;font-family:Segoe UI,Arial,sans-serif;color:#FFFFFF;'>"
            "<div style='display:flex;flex-direction:column;justify-content:center;min-width:0;'>"
            "<div style='font-size:31px;line-height:34px;font-weight:800;letter-spacing:-0.4px;"
            "color:#FFFFFF;white-space:nowrap;text-shadow:0 2px 5px rgba(0,0,0,0.20);'>"
            + titulo +
            "</div><div style='margin-top:4px;font-size:16px;line-height:20px;font-weight:700;"
            "letter-spacing:1.2px;color:rgba(255,255,255,0.92);text-transform:uppercase;'>"
            "LCQ-RJ</div></div></div>\"")


RODAPE_HTML = (
    '"<div style=\'width:100%;height:100%;box-sizing:border-box;display:flex;align-items:center;'
    "justify-content:center;overflow:hidden;padding:0 20px;background:transparent;"
    "font-family:Segoe UI,Arial,sans-serif;font-size:14px;color:#64748B;text-align:center;"
    "line-height:18px;white-space:nowrap;'><span>Idealizado e implementado por "
    "<strong style='color:#334155;'>Rodrigo Barbosa Tavares da Mota</strong>"
    "<span style='margin:0 7px;color:#94A3B8;'>|</span>LCQ RJ &#8212; Braskem</span></div>\"")


def menu_item_html(chave_ativa):
    """Item do menu lateral, identico ao galMenuLateralNovo do Radar."""
    return ('With(\n'
            '    {\n'
            '        vSelecionado: ThisItem.Chave = "%s"\n' % chave_ativa +
            '    },\n'
            '    With(\n'
            '        {\n'
            '            vFundo: If(vSelecionado, "#E5EEF9", "transparent"),\n'
            '            vCorTexto: If(vSelecionado, "#102A4C", "#344054"),\n'
            '            vCorSigla: If(vSelecionado, "#102A4C", "#526174"),\n'
            '            vFundoSigla: If(vSelecionado, "#FFFFFF", "#E9EEF4"),\n'
            '            vCorBarra: If(vSelecionado, "#143A66", "transparent"),\n'
            '            vCorBorda: If(vSelecionado, "#D7E3F1", "transparent"),\n'
            '            vCorBordaSigla: If(vSelecionado, "#D6E1EC", "transparent"),\n'
            '            vPesoTexto: If(vSelecionado, "700", "600")\n'
            '        },\n'
            '        "<div style=\'position:relative;width:100%;height:100%;box-sizing:border-box;'
            'display:flex;align-items:center;overflow:hidden;padding:8px 13px 8px 17px;'
            'border:1px solid " & vCorBorda & ";border-radius:13px;background:" & vFundo &\n'
            '        ";box-shadow:none;font-family:Segoe UI,Arial,sans-serif;\'>'
            '<div style=\'position:absolute;left:0;top:12px;bottom:12px;width:4px;'
            'border-radius:0 4px 4px 0;background:" & vCorBarra & ";\'></div>'
            '<div style=\'flex:none;width:39px;height:39px;min-width:39px;box-sizing:border-box;'
            'display:flex;align-items:center;justify-content:center;border:1px solid " & vCorBordaSigla &\n'
            '        ";border-radius:10px;background:" & vFundoSigla & ";color:" & vCorSigla &\n'
            '        ";font-size:11px;font-weight:800;line-height:1;letter-spacing:0.6px;\'>" &\n'
            '        Coalesce(ThisItem.Sigla, "") &\n'
            '        "</div><div style=\'flex:1;min-width:0;margin-left:13px;padding-right:2px;color:" & vCorTexto &\n'
            '        ";font-size:15px;font-weight:" & vPesoTexto & ";line-height:19px;letter-spacing:-0.1px;'
            'white-space:normal;word-break:normal;overflow:hidden;\'>" &\n'
            '        Coalesce(ThisItem.Rotulo, "") &\n'
            '        "</div></div>"\n'
            '    )\n'
            ')')


def titulo_html(titulo, sub_expr):
    """Titulo executivo de secao (26px/800) + subtitulo, padrao Radar."""
    return ('"<div style=\'width:100%;height:100%;box-sizing:border-box;display:flex;'
            "align-items:center;font-family:Segoe UI,Arial,sans-serif;'>"
            "<div style='width:5px;height:46px;border-radius:5px;background:#1C5582;flex:none;'></div>"
            "<div style='margin-left:14px;min-width:0;'>"
            "<div style='color:#0E2A4A;font-size:26px;font-weight:800;line-height:30px;"
            "letter-spacing:-0.4px;white-space:nowrap;'>" + titulo + "</div>"
            "<div style='margin-top:3px;color:#657384;font-size:16px;font-weight:500;"
            "line-height:20px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;'>\" & "
            + sub_expr + " & \"</div></div></div>\"")
