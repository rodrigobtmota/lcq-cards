"""Motor de edição de telas Power Apps (.msapp descompactado).

Mantém Controls/<n>.json (fonte que o Studio carrega) e Src/<tela>.pa.yaml
(espelho para revisão) sincronizados, registrando cada propriedade alterada.
"""
import copy
import json
import re

CATEGORY_HINT = {
    'OnSelect': 'Behavior', 'OnChange': 'Behavior', 'OnVisible': 'Behavior',
    'Items': 'Data', 'Default': 'Data', 'HtmlText': 'Data', 'Text': 'Data',
    'Tooltip': 'Data', 'HintText': 'Data', 'AccessibleLabel': 'Data',
}


def _yaml_needs_block(s):
    return ('\n' in s or ': ' in s or ' #' in s or s.endswith(':')
            or s != s.strip() or s.startswith(('|', '>')))


class Screen:
    def __init__(self, json_path, yaml_path, uid_alloc):
        self.json_path = json_path
        self.yaml_path = yaml_path
        self.doc = json.load(open(json_path, encoding='utf-8'))
        self.yaml_lines = open(yaml_path, encoding='utf-8').read().split('\n')
        self.uid_alloc = uid_alloc
        self.changes = []      # (controle, propriedade, antes, depois)
        self.created = []      # (controle, template, pai, origem)
        self.name = self.doc['TopParent']['Name']

    # ------------------------------------------------------------ JSON
    def find(self, name, node=None):
        node = node or self.doc['TopParent']
        if node['Name'] == name:
            return node
        for ch in node.get('Children', []):
            r = self.find(name, ch)
            if r:
                return r
        return None

    def ctrl(self, name):
        c = self.find(name)
        if c is None:
            raise KeyError(f'{self.name}: controle inexistente {name}')
        return c

    def get(self, name, prop):
        for r in self.ctrl(name)['Rules']:
            if r['Property'] == prop:
                return r['InvariantScript']
        return None

    def set(self, name, prop, script, expect_old=None):
        c = self.ctrl(name)
        old = None
        for r in c['Rules']:
            if r['Property'] == prop:
                old = r['InvariantScript']
                if expect_old is not None and old != expect_old:
                    raise ValueError(f'{name}.{prop}: valor anterior inesperado')
                r['InvariantScript'] = script
                break
        else:
            c['Rules'].append({'Property': prop,
                               'Category': CATEGORY_HINT.get(prop, 'Design'),
                               'InvariantScript': script,
                               'RuleProviderType': 'Unknown'})
            if prop not in c.get('ControlPropertyState', []):
                c.setdefault('ControlPropertyState', []).append(prop)
        if old != script:
            self.changes.append((name, prop, old, script))
            self._yaml_set(name, prop, script)

    def replace(self, name, prop, a, b):
        """Troca exatamente uma ocorrência de `a` por `b` na fórmula."""
        old = self.get(name, prop)
        if old is None or old.count(a) != 1:
            raise ValueError(f'{name}.{prop}: trecho esperado não encontrado exatamente 1 vez')
        self.set(name, prop, old.replace(a, b))

    def setmany(self, name, **props):
        for k, v in props.items():
            self.set(name, k, v)

    def clone(self, src, new, parent, props, zindex):
        """Cria controle visual novo copiando o modelo de `src`."""
        if self.find(new):
            raise ValueError(f'{new} já existe')
        s = self.ctrl(src)
        p = self.ctrl(parent)
        c = copy.deepcopy(s)
        c['Name'] = new
        c['Parent'] = parent
        c['Children'] = []
        uid, poi = self.uid_alloc()
        c['ControlUniqueId'] = str(uid)
        c['PublishOrderIndex'] = poi
        for r in c['Rules']:
            if r['Property'] == 'ZIndex':
                r['InvariantScript'] = str(zindex)
        p['Children'].append(c)
        self.created.append((new, c['Template']['Name'], parent, src))
        self._yaml_clone(src, new, parent)
        for k, v in props.items():
            self.set(new, k, v)
        return c

    # ------------------------------------------------------------ YAML
    def _yaml_find_ctrl(self, name):
        pat = re.compile(r'^(\s*)- ' + re.escape(name) + r':\s*$')
        for i, ln in enumerate(self.yaml_lines):
            m = pat.match(ln)
            if m:
                return i, len(m.group(1))
        raise KeyError(f'YAML: {name} não encontrado')

    def _yaml_block_end(self, start, indent):
        """Índice da primeira linha após o bloco do item de lista em `start`."""
        i = start + 1
        while i < len(self.yaml_lines):
            ln = self.yaml_lines[i]
            if ln.strip() and (len(ln) - len(ln.lstrip())) <= indent:
                break
            i += 1
        return i

    def _fmt_prop(self, prop, script, ind):
        val = '=' + script
        pad = ' ' * ind
        if _yaml_needs_block(val):
            out = [f'{pad}{prop}: |-']
            out += [(' ' * (ind + 2) + l) if l else '' for l in val.split('\n')]
            return out
        return [f'{pad}{prop}: {val}']

    def _yaml_set(self, name, prop, script):
        i, ind = self._yaml_find_ctrl(name)
        end = self._yaml_block_end(i, ind)
        # localizar "Properties:"
        pi = None
        for k in range(i + 1, end):
            if self.yaml_lines[k].strip() == 'Properties:' and \
                    len(self.yaml_lines[k]) - len(self.yaml_lines[k].lstrip()) == ind + 4:
                pi = k
                break
        if pi is None:
            # inserir após "Control:"/"Variant:"
            k = i + 1
            while k < end and self.yaml_lines[k].strip().split(':')[0] in ('Control', 'Variant'):
                k += 1
            self.yaml_lines[k:k] = [' ' * (ind + 4) + 'Properties:']
            pi = k
            end += 1
        pind = ind + 6
        # varrer propriedades
        k = pi + 1
        insert_at = None
        while k < end:
            ln = self.yaml_lines[k]
            cur = len(ln) - len(ln.lstrip()) if ln.strip() else None
            if cur is not None and cur < pind:
                break
            if cur == pind:
                key = ln.strip().split(':', 1)[0]
                pend = k + 1
                while pend < end:
                    l2 = self.yaml_lines[pend]
                    if l2.strip() and len(l2) - len(l2.lstrip()) <= pind:
                        break
                    pend += 1
                if key == prop:
                    self.yaml_lines[k:pend] = self._fmt_prop(prop, script, pind)
                    return
                if insert_at is None and key.lower() > prop.lower():
                    insert_at = k
                k = pend
                continue
            k += 1
        if insert_at is None:
            insert_at = k
        self.yaml_lines[insert_at:insert_at] = self._fmt_prop(prop, script, pind)

    def _yaml_clone(self, src, new, parent):
        i, ind = self._yaml_find_ctrl(src)
        end = self._yaml_block_end(i, ind)
        block = self.yaml_lines[i:end]
        # remover Children de origem (não se aplica a rótulos)
        pi, pind = self._yaml_find_ctrl(parent)
        pend = self._yaml_block_end(pi, pind)
        child_ind = pind + 6
        delta = child_ind - ind
        newblock = []
        for ln in block:
            if not ln.strip():
                newblock.append(ln)
            elif delta >= 0:
                newblock.append(' ' * delta + ln)
            else:
                newblock.append(ln[-delta:])
        newblock[0] = ' ' * child_ind + f'- {new}:'
        # garantir que o pai tem "Children:"
        has_children = any(self.yaml_lines[k].strip() == 'Children:' and
                           len(self.yaml_lines[k]) - len(self.yaml_lines[k].lstrip()) == pind + 4
                           for k in range(pi, pend))
        if not has_children:
            self.yaml_lines[pend:pend] = [' ' * (pind + 4) + 'Children:']
            pend += 1
        self.yaml_lines[pend:pend] = newblock

    # ------------------------------------------------------------ saída
    def save(self):
        # mesmo formato gravado pelo Studio: indentação 2, CRLF, UTF-8 sem BOM
        txt = json.dumps(self.doc, ensure_ascii=False, indent=2).replace('\n', '\r\n')
        with open(self.json_path, 'w', encoding='utf-8', newline='') as f:
            f.write(txt)
        with open(self.yaml_path, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(self.yaml_lines))
