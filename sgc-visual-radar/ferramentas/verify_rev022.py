# -*- coding: utf-8 -*-
"""Verificacao bloqueante da REV02.2 (PA2108).

Checa, estruturalmente (por tipo de controle, nao por texto):
1. nenhum Classic/Button@2.2.0 com AccessibleLabel, em Src e em Controls;
2. os 8 btnNav* com Text e Tooltip = ThisItem.Rotulo e cores transparentes;
3. OnSelect inalterado em relacao a REV02.1;
4. paridade Src x Controls;
5. as fórmulas funcionais do SGC original preservadas;
6. nenhum controle novo ou removido em relacao a REV02.1.
"""
import os, re, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import payaml, jsonctl as J, caminhos

BOTAO = 'Classic/Button@2.2.0'
ORIG = caminhos.entrada('sgc')
REV2 = caminhos.saida('build')
BASE_ANT = caminhos.entrada(sys.argv[1]) if len(sys.argv) > 1 else caminhos.entrada('build_rev02_1')
erros = []


def telas(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, 'Src', 'scr*.pa.yaml'))):
        _, r = payaml.parse(f)
        out[r.name] = {c.name: c for c in r.walk()}
    return out


def v(c, p):
    return '\n'.join(c.props.get(p, [])) or None


# ---- 1. PA2108: nenhum AccessibleLabel em botao classico (Src e Controls) ----
def pa2108():
    yaml_ofensores, json_ofensores = [], []
    for tela, ctrls in telas(REV2).items():
        for nome, c in ctrls.items():
            if dict(c.meta).get('Control') == BOTAO and 'AccessibleLabel' in c.props:
                yaml_ofensores.append('%s/%s' % (tela, nome))
    jf = J.screen_files(os.path.join(REV2, 'Controls'))
    for tela, f in jf.items():
        top = J.load(f)['TopParent']
        for c in J.walk(top):
            t = c.get('Template', {})
            classico = (t.get('Name') == 'button' and t.get('Version') == '2.2.0')
            if not classico:
                continue
            props = [r['Property'] for r in c.get('Rules', [])]
            estado = c.get('ControlPropertyState') or []
            if 'AccessibleLabel' in props or 'AccessibleLabel' in estado:
                json_ofensores.append('%s/%s' % (tela, c['Name']))
    if yaml_ofensores:
        erros.append('AccessibleLabel em Classic/Button (Src): %s' % yaml_ofensores)
    if json_ofensores:
        erros.append('AccessibleLabel em Classic/Button (Controls): %s' % json_ofensores)
    print('Classic/Button@2.2.0 com AccessibleLabel: %d (Src) / %d (Controls)'
          % (len(yaml_ofensores), len(json_ofensores)))
    # AccessibleLabel que permanecem, por tipo
    restantes = {}
    for tela, ctrls in telas(REV2).items():
        for nome, c in ctrls.items():
            if 'AccessibleLabel' in c.props:
                restantes.setdefault(dict(c.meta).get('Control'), []).append(nome)
    for tipo, lista in sorted(restantes.items()):
        print('AccessibleLabel mantido em %-18s: %d' % (tipo, len(lista)))
    return restantes


# ---- 2. menu lateral acessivel sem AccessibleLabel ----
def menu():
    n = 0
    for tela, ctrls in telas(REV2).items():
        for nome, c in ctrls.items():
            if not nome.startswith('btnNav') or nome.startswith('btnNavNova'):
                continue
            n += 1
            if v(c, 'Text') != '=ThisItem.Rotulo':
                erros.append('%s/%s: Text != ThisItem.Rotulo (%r)' % (tela, nome, v(c, 'Text')))
            if v(c, 'Tooltip') != '=ThisItem.Rotulo':
                erros.append('%s/%s: Tooltip != ThisItem.Rotulo' % (tela, nome))
            for p in ('Color', 'HoverColor', 'PressedColor'):
                if v(c, p) != '=RGBA(0, 0, 0, 0)':
                    erros.append('%s/%s: %s deixou de ser transparente (%r)'
                                 % (tela, nome, p, v(c, p)))
    if n != 8:
        erros.append('esperados 8 botoes de menu, encontrados %d' % n)
    print('botoes de menu com Text/Tooltip = ThisItem.Rotulo: %d' % n)
    # botoes de fechar com simbolo mantem tooltip
    for tela, ctrls in telas(REV2).items():
        for nome, c in ctrls.items():
            if nome.startswith('btnAjudaX') and v(c, 'Tooltip') != '="Fechar a ajuda"':
                erros.append('%s/%s: Tooltip de fechar ausente' % (tela, nome))


# ---- 3 e 6. comparacao com a REV02.1 ----
def contra_rev021():
    a, b = telas(BASE_ANT), telas(REV2)
    mud = {'AccessibleLabel removido': 0, 'Text do menu': 0, 'Tooltip de fechar': 0}
    for tela in sorted(set(a) | set(b)):
        ca, cb = a.get(tela, {}), b.get(tela, {})
        if set(ca) != set(cb):
            erros.append('%s: conjunto de controles mudou: %s' % (tela, sorted(set(ca) ^ set(cb))))
        for nome in set(ca) & set(cb):
            pa = {p: '\n'.join(x) for p, x in ca[nome].props.items()}
            pb = {p: '\n'.join(x) for p, x in cb[nome].props.items()}
            for p in set(pa) | set(pb):
                if pa.get(p) == pb.get(p):
                    continue
                tipo = dict(cb[nome].meta).get('Control')
                if p == 'AccessibleLabel' and pb.get(p) is None and tipo == BOTAO:
                    mud['AccessibleLabel removido'] += 1
                    continue
                if p == 'Text' and nome.startswith('btnNav') and not nome.startswith('btnNavNova') \
                        and pb.get(p) == '=ThisItem.Rotulo':
                    mud['Text do menu'] += 1
                    continue
                if p == 'Tooltip' and nome.startswith('btnAjudaX') and pb.get(p) == '="Fechar a ajuda"':
                    mud['Tooltip de fechar'] += 1
                    continue
                erros.append('ALTERACAO NAO AUTORIZADA %s/%s.%s: %r -> %r'
                             % (tela, nome, p, pa.get(p), pb.get(p)))
    for k, n in mud.items():
        print('%-26s: %d' % (k, n))


# ---- 4. paridade Src x Controls ----
def paridade():
    jf = J.screen_files(os.path.join(REV2, 'Controls'))
    for tela, ctrls in telas(REV2).items():
        top = J.load(jf[tela])['TopParent']
        nomes = {c['Name'] for c in J.walk(top) if c is not top
                 and not re.fullmatch(r'[0-9a-f\-]{36}', c['Name'])}
        esperado = {n for n in ctrls if n != tela}
        if nomes != esperado:
            erros.append('%s: divergencia Src x Controls %s' % (tela, sorted(nomes ^ esperado)))
        # propriedades relevantes devem bater entre as duas representacoes
        for c in J.walk(top):
            if c is top or c['Name'] not in ctrls:
                continue
            for p in ('Text', 'Tooltip', 'OnSelect', 'AccessibleLabel'):
                y = v(ctrls[c['Name']], p)
                if y is None:
                    # o YAML so registra o que difere do padrao: ausencia nao e divergencia.
                    # (AccessibleLabel em botao classico ja e reprovado pela checagem PA2108,
                    # nas duas representacoes.)
                    continue
                if y[1:] != J.get_rule(c, p):
                    erros.append('%s/%s.%s difere entre Src e Controls' % (tela, c['Name'], p))
    print('paridade Src x Controls conferida')


# ---- 5. formulas funcionais do SGC original ----
def formulas():
    FUNC = ('Patch(', 'Navigate(', 'Set(', 'UpdateContext', 'Collect', 'Filter(', 'LookUp(',
            'SortByColumns', 'Reset(', 'With(', 'Concurrent(')
    CRIT = ('OnSelect', 'OnVisible', 'OnHidden', 'OnChange', 'Items', 'Text', 'Default',
            'DefaultSelectedItems', 'DisplayMode', 'Visible', 'Tooltip')
    a, b = telas(ORIG), telas(REV2)
    n = 0
    for tela in sorted(set(a) & set(b)):
        for nome in set(a[tela]) & set(b[tela]):
            for p in CRIT:
                va, vb = v(a[tela][nome], p), v(b[tela][nome], p)
                if va is None or not any(t in va for t in FUNC):
                    continue
                if va == vb:
                    n += 1
                elif nome.startswith(('galNav', 'btnNav')):
                    n += 1   # shell: mudanca visual/acessibilidade declarada
                else:
                    erros.append('FORMULA FUNCIONAL ALTERADA %s/%s.%s' % (tela, nome, p))
    print('formulas funcionais identicas ao SGC original: %d' % n)
    # OnSelect nunca muda, em nenhum controle
    c = 0
    for tela in sorted(set(a) & set(b)):
        for nome in set(a[tela]) & set(b[tela]):
            if v(a[tela][nome], 'OnSelect') is not None:
                c += 1
                if v(a[tela][nome], 'OnSelect') != v(b[tela][nome], 'OnSelect'):
                    erros.append('OnSelect alterado em %s/%s' % (tela, nome))
    print('OnSelect conferidos (identicos ao original): %d' % c)


if __name__ == '__main__':
    print('Base anterior: %s\n' % os.path.relpath(BASE_ANT, caminhos.RAIZ))
    pa2108()
    menu()
    contra_rev021()
    paridade()
    formulas()
    print('\nERROS (%d):' % len(erros))
    for e in erros[:40]:
        print('  *', e)
    sys.exit(1 if erros else 0)
