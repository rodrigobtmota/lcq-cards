"""Edição do formato Controls/*.json (representação binária do msapp)."""
import json, copy, glob, os

CATEGORY = {
    'OnSelect': 'Behavior', 'OnVisible': 'Behavior', 'OnHidden': 'Behavior',
    'OnChange': 'Behavior', 'OnStart': 'Behavior', 'OnCheck': 'Behavior',
    'OnUncheck': 'Behavior', 'OnSelectDate': 'Behavior', 'OnReset': 'Behavior',
}
DATA_PROPS = {'Text', 'Items', 'Default', 'DefaultSelectedItems', 'Tooltip', 'HtmlText',
              'Image', 'Live', 'Role', 'ContentLanguage', 'AccessibleLabel', 'Value',
              'SearchPlaceholder', 'HintText', 'Icon', 'DisplayMode'}


def load(path):
    return json.load(open(path, encoding='utf-8'))


def save(doc, path):
    json.dump(doc, open(path, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))


def walk(ctrl):
    yield ctrl
    for c in ctrl.get('Children', []):
        yield from walk(c)


def find(root, name):
    for c in walk(root):
        if c.get('Name') == name:
            return c
    return None


def parent_of(root, name):
    for c in walk(root):
        for ch in c.get('Children', []):
            if ch.get('Name') == name:
                return c
    return None


def remove(root, name):
    p = parent_of(root, name)
    if not p:
        return False
    p['Children'] = [c for c in p['Children'] if c.get('Name') != name]
    return True


def category(prop):
    if prop in CATEGORY:
        return 'Behavior'
    if prop in DATA_PROPS:
        return 'Data'
    return 'Design'


def set_rule(ctrl, prop, script):
    for r in ctrl.get('Rules', []):
        if r['Property'] == prop:
            r['InvariantScript'] = script
            return
    ctrl.setdefault('Rules', []).append({
        'Property': prop, 'Category': category(prop),
        'InvariantScript': script, 'RuleProviderType': 'Unknown'})
    st = ctrl.get('ControlPropertyState')
    if isinstance(st, list) and prop not in st:
        st.append(prop)


def get_rule(ctrl, prop):
    for r in ctrl.get('Rules', []):
        if r['Property'] == prop:
            return r['InvariantScript']
    return None


def rename(ctrl, new_name):
    old = ctrl['Name']
    ctrl['Name'] = new_name
    for c in walk(ctrl):
        if c is not ctrl and c.get('Parent') == old:
            c['Parent'] = new_name
    return ctrl


def clone(src, new_name, parent_name, index=0):
    c = copy.deepcopy(src)
    c['Children'] = []
    c['Name'] = new_name
    c['Parent'] = parent_name
    c['Index'] = index
    c['PublishOrderIndex'] = index
    c['MetaDataIDKey'] = ''
    c['PersistMetaDataIDKey'] = False
    return c


def add_child(parent, ctrl):
    parent.setdefault('Children', []).append(ctrl)
    ctrl['Parent'] = parent['Name']
    return ctrl


def reindex(root):
    for c in walk(root):
        for i, ch in enumerate(c.get('Children', [])):
            ch['Index'] = i
            ch['PublishOrderIndex'] = i


def screen_files(ctrl_dir):
    out = {}
    for f in glob.glob(os.path.join(ctrl_dir, '*.json')):
        d = json.load(open(f, encoding='utf-8'))
        out[d['TopParent']['Name']] = f
    return out
