"""Pequenos construtores de fórmulas Power Fx (sintaxe invariante, separador ',')."""


def esc(expr):
    """Escapa texto dinâmico para uso em HtmlText (mesmo padrão do app)."""
    return ('Substitute(Substitute(Substitute(Coalesce(Text(' + expr +
            '), ""), "&", "&amp;"), "<", "&lt;"), ">", "&gt;")')


def s(text):
    """Literal de texto Power Fx."""
    return '"' + text.replace('"', '""') + '"'


def box(inner, extra_style=''):
    """Contêiner HTML com a altura do próprio controle (padrão do app)."""
    return ('"<div style=\'box-sizing:border-box;width:100%;height:" & Text(Max(Self.Height - 2, 0), "0", "en-US") & '
            '"px;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;' + extra_style + '\'>" & ' + inner + ' & "</div>"')


def div(style, content_expr):
    return '"<div style=\'' + style + '\'>" & ' + content_expr + ' & "</div>"'
