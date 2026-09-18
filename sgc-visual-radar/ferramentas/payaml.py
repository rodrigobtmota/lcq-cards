"""Parser/serializador minimalista para arquivos *.pa.yaml de Canvas Apps."""
import re

HEADER = """# ************************************************************************************************
# Warning: YAML source code for Canvas Apps should only be used to review changes made within Power Apps Studio and for minor edits (Preview).
# Use the maker portal to create and edit your Power Apps.
# 
# The schema file for Canvas Apps is available at https://go.microsoft.com/fwlink/?linkid=2304907
# 
# For more information, visit https://go.microsoft.com/fwlink/?linkid=2292623
# ************************************************************************************************
"""


class Ctrl:
    def __init__(self, name):
        self.name = name
        self.meta = []            # [(key, value)] ex.: Control, Variant, ComponentName
        self.props = {}           # nome -> lista de linhas (sem o '=' inicial? não: com)
        self.children = []

    def get(self, p):
        return self.props.get(p)

    def set(self, p, value):
        """value: string (pode conter \n)."""
        self.props[p] = value.split('\n')

    def setall(self, d):
        for k, v in d.items():
            if v is None:
                self.props.pop(k, None)
            else:
                self.set(k, v)

    def drop(self, *props):
        for p in props:
            self.props.pop(p, None)

    def find(self, name):
        if self.name == name:
            return self
        for c in self.children:
            r = c.find(name)
            if r:
                return r
        return None

    def parent_of(self, name):
        for c in self.children:
            if c.name == name:
                return self
            r = c.parent_of(name)
            if r:
                return r
        return None

    def remove(self, name):
        p = self.parent_of(name)
        if p:
            p.children = [c for c in p.children if c.name != name]
            return True
        return False

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()


def _indent_of(line):
    return len(line) - len(line.lstrip(' '))


def parse(path):
    """Devolve (screen_name, root_props(dict), children[list of Ctrl], kind)."""
    raw = open(path, encoding='utf-8').read()
    lines = raw.split('\n')
    # localizar 'Screens:' ou 'App:'
    i = 0
    while i < len(lines) and not re.match(r'^(Screens|App|EditorState|ComponentDefinitions):\s*$', lines[i]):
        i += 1
    kind = lines[i].rstrip(':').strip() if i < len(lines) else None
    if kind == 'Screens':
        i += 1
        screen = lines[i].strip().rstrip(':')
        i += 1
        base = 4
    else:
        screen = None
        i += 1
        base = 2
    root = Ctrl(screen or kind)
    _parse_body(lines, i, base, root)
    return kind, root


def _parse_body(lines, i, base, ctrl):
    """Lê 'Properties:' e 'Children:' de um controle cujos campos estão em indent=base."""
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        ind = _indent_of(line)
        if ind < base:
            return i
        key = line.strip()
        if key == 'Properties:':
            i = _parse_props(lines, i + 1, base + 2, ctrl)
        elif key == 'Children:':
            i = _parse_children(lines, i + 1, base + 2, ctrl)
        else:
            m = re.match(r'^([A-Za-z]+):\s*(.*)$', key)
            if m:
                ctrl.meta.append((m.group(1), m.group(2)))
            i += 1
    return i


def _parse_props(lines, i, base, ctrl):
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        ind = _indent_of(line)
        if ind < base:
            return i
        m = re.match(r'^\s*([A-Za-z0-9_\.\' ]+):\s?(.*)$', line)
        name = m.group(1)
        val = m.group(2)
        if val.strip() in ('|-', '|', '|+', '>-'):
            chomp = val.strip()
            block = []
            i += 1
            bind = None
            while i < n:
                l2 = lines[i]
                if l2.strip() == '':
                    block.append('')
                    i += 1
                    continue
                if bind is None:
                    bind = _indent_of(l2)
                if _indent_of(l2) < bind:
                    break
                block.append(l2[bind:])
                i += 1
            while block and block[-1] == '':
                block.pop()
            ctrl.props[name] = block
        else:
            ctrl.props[name] = [val]
            i += 1
    return i


def _parse_children(lines, i, base, parent):
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        ind = _indent_of(line)
        if ind < base:
            return i
        m = re.match(r'^\s*- ([^:]+):\s*$', line)
        if not m:
            return i
        c = Ctrl(m.group(1))
        parent.children.append(c)
        i = _parse_body(lines, i + 1, base + 4, c)
    return i


def _emit_value(name, lines_, indent):
    pad = ' ' * indent
    if len(lines_) == 1 and '\n' not in lines_[0]:
        v = lines_[0]
        simple = (': ' not in v) and not v.startswith('|') and ' #' not in v and not v.endswith(':')
        if simple:
            return ["%s%s: %s" % (pad, name, v)]
    out = ["%s%s: |-" % (pad, name)]
    for l in lines_:
        out.append((pad + '  ' + l).rstrip() if l else '')
    return out


def emit_ctrl(c, indent):
    pad = ' ' * indent
    out = ["%s- %s:" % (pad, c.name)]
    ip = indent + 4
    for k, v in c.meta:
        out.append("%s%s: %s" % (' ' * ip, k, v))
    if c.props:
        out.append("%sProperties:" % (' ' * ip))
        for k in sorted(c.props, key=lambda s: s.lower()):
            out += _emit_value(k, c.props[k], ip + 2)
    if c.children:
        out.append("%sChildren:" % (' ' * ip))
        for ch in c.children:
            out += emit_ctrl(ch, ip + 2)
    return out


def dump_screen(root, path):
    out = [HEADER.rstrip('\n'), "Screens:", "  %s:" % root.name]
    if root.props:
        out.append("    Properties:")
        for k in sorted(root.props, key=lambda s: s.lower()):
            out += _emit_value(k, root.props[k], 6)
    if root.children:
        out.append("    Children:")
        for ch in root.children:
            out += emit_ctrl(ch, 6)
    open(path, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
