# -*- coding: utf-8 -*-
import sys, os, re, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import payaml, jsonctl as J

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def tree(root):
    out = {}
    def w(c, path):
        out[c.name] = path
        for x in c.children:
            w(x, path + '/' + c.name)
    for c in root.children:
        w(c, root.name)
    return out


def jtree(top):
    out = {}
    for c in J.walk(top):
        if c is not top:
            out[c['Name']] = 1
    return out


def check(orig_dir, new_dir):
    erros, avisos = [], []
    so = {os.path.basename(f): f for f in glob.glob(os.path.join(orig_dir, 'Src', '*.pa.yaml'))}
    sn = {os.path.basename(f): f for f in glob.glob(os.path.join(new_dir, 'Src', '*.pa.yaml'))}
    if set(so) != set(sn):
        erros.append('conjunto de arquivos Src difere: %s' % (set(so) ^ set(sn)))
    jo = J.screen_files(os.path.join(orig_dir, 'Controls'))
    jn = J.screen_files(os.path.join(new_dir, 'Controls'))
    if set(jo) != set(jn):
        erros.append('conjunto de telas difere')
    telas = [k for k in jn if k.startswith('scr')]
    print('telas:', len(telas), sorted(telas))

    # 1. paridade yaml x json
    for f in sorted(sn):
        if not f.startswith('scr'):
            continue
        k, r = payaml.parse(sn[f])
        y = set(tree(r))
        j = set(jtree(J.load(jn[r.name])['TopParent']))
        # galleryTemplate existe so no json
        j = {n for n in j if not re.fullmatch(r'[0-9a-f\-]{36}', n)}
        if y != j:
            erros.append('%s: divergencia yaml/json %s' % (r.name, sorted(y ^ j)))

    # 2. formulas funcionais preservadas
    criticos = ('OnSelect', 'OnVisible', 'OnHidden', 'Items', 'Text', 'Default',
                'DefaultSelectedItems', 'DisplayMode', 'Visible', 'OnChange', 'Tooltip')
    novos = set()
    for f in sorted(so):
        if not f.startswith('scr'):
            continue
        _, ro = payaml.parse(so[f])
        _, rn = payaml.parse(sn[f])
        mo = {c.name: c for c in ro.walk()}
        mn = {c.name: c for c in rn.walk()}
        novos |= set(mn) - set(mo)
        for name, co in mo.items():
            cn = mn.get(name)
            if cn is None:
                continue
            for p in criticos:
                a = '\n'.join(co.props.get(p, []))
                b = '\n'.join(cn.props.get(p, []))
                if a == b:
                    continue
                if not a:
                    continue
                # mudancas visuais deliberadas
                if p in ('Items', 'Text', 'Tooltip', 'Visible', 'DisplayMode') and \
                   name.startswith(('galNav', 'btnNav', 'recNavAtivo', 'lblMarca', 'lblFaixa')):
                    continue
                if ('Patch(' in a or 'Navigate(' in a or 'Set(' in a or 'Collect' in a
                        or 'UpdateContext' in a or 'Filter(' in a or 'LookUp(' in a
                        or 'SortByColumns' in a or 'Reset(' in a):
                    erros.append('FORMULA ALTERADA %s.%s' % (name, p))
                else:
                    avisos.append('texto/estilo alterado %s.%s' % (name, p))
    print('controles novos:', sorted(novos))

    # 3. fontes de dados
    ds = json.load(open(os.path.join(new_dir, 'References', 'DataSources.json'), encoding='utf-8'))
    nomes = sorted({d.get('Name') for d in ds['DataSources']})
    print('datasources:', nomes)
    if any(n and n.startswith('Radar') for n in nomes):
        erros.append('fonte Radar_* presente')
    todo = '\n'.join(open(f, encoding='utf-8').read() for f in sn.values())
    if 'Radar_' in todo:
        erros.append('referencia Radar_ no codigo')
    for src in ('SGC_Pessoas', 'SGC_Competencias', 'SGC_Qualificacoes', 'SGC_Avaliacoes'):
        if src not in todo and src not in json.dumps(nomes):
            erros.append('fonte %s ausente' % src)

    # 4. App.OnStart
    app = open(os.path.join(new_dir, 'Src', 'App.pa.yaml'), encoding='utf-8').read()
    for t in ('Refresh(SGC_Pessoas)', 'ClearCollect(colAreas', 'colStatusQualificacao',
              'varModoSomenteLeitura', 'varCorPrimaria', 'varCorVermelho'):
        if t not in app:
            erros.append('App.OnStart sem %s' % t)

    # 4b. sanidade sintatica das formulas (strings/parenteses/HTML fora de literal)
    def fora_de_string(s):
        out = []; dentro = False; i = 0
        while i < len(s):
            c = s[i]
            if c == '"':
                if dentro and i + 1 < len(s) and s[i + 1] == '"':
                    i += 2; continue
                dentro = not dentro
            elif not dentro:
                out.append(c)
            i += 1
        return ''.join(out), dentro
    for f in sorted(sn):
        _, r = payaml.parse(sn[f])
        for c in r.walk():
            for p, v in c.props.items():
                s = '\n'.join(v)
                s = s[1:] if s.startswith('=') else s
                fora, aberta = fora_de_string(s)
                if aberta:
                    erros.append('%s.%s: string nao fechada' % (c.name, p))
                if fora.count('(') != fora.count(')'):
                    erros.append('%s.%s: parenteses desbalanceados' % (c.name, p))
                if '<div' in fora or 'style=' in fora or 'px;' in fora or 'data:' in fora:
                    erros.append('%s.%s: HTML fora de literal' % (c.name, p))

    # 5. contagem de controles
    for f in sorted(so):
        if not f.startswith('scr'):
            continue
        _, ro = payaml.parse(so[f]); _, rn = payaml.parse(sn[f])
        a = len(list(ro.walk())); b = len(list(rn.walk()))
        print('  %-26s controles %d -> %d' % (f, a, b))
    return erros, avisos


if __name__ == '__main__':
    e, a = check(os.path.join(BASE, 'sgc'), os.path.join(BASE, 'build'))
    print('\nAVISOS (%d):' % len(a))
    for x in sorted(set(a))[:40]:
        print('  -', x)
    print('\nERROS (%d):' % len(e))
    for x in e:
        print('  *', x)
