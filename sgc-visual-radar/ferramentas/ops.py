# -*- coding: utf-8 -*-
"""Aplica a mesma lista de operacoes nas duas representacoes do msapp
(Src/*.pa.yaml e Controls/*.json), mantendo-as equivalentes."""
import json, copy, os
import payaml, jsonctl as J

PROTO_HTML = json.load(open(os.path.join(os.path.dirname(__file__), 'proto_htmlviewer.json'), encoding='utf-8'))

HTML_DEFAULTS = {
    'AutoHeight': 'false', 'BorderStyle': 'BorderStyle.None', 'BorderThickness': '0',
    'DisplayMode': 'DisplayMode.View', 'Fill': 'RGBA(0, 0, 0, 0)',
    'BorderColor': 'RGBA(0, 0, 0, 0)', 'Font': "Font.'Open Sans'", 'Size': '13',
    'PaddingTop': '0', 'PaddingBottom': '0', 'PaddingLeft': '0', 'PaddingRight': '0',
}


class Screen:
    def __init__(self, yaml_path, json_path):
        self.yaml_path = yaml_path
        self.json_path = json_path
        _, self.y = payaml.parse(yaml_path)
        self.jdoc = J.load(json_path)
        self.j = self.jdoc['TopParent']
        assert self.y.name == self.j['Name'], (self.y.name, self.j['Name'])

    # ---------- operacoes ----------
    def delete(self, name):
        ok1 = self.y.remove(name)
        ok2 = J.remove(self.j, name)
        assert ok1 and ok2, ('delete', name, ok1, ok2)

    @staticmethod
    def _s(v):
        return v[1:] if v.startswith('=') else v

    @classmethod
    def _y(cls, v):
        return '=' + cls._s(v)

    def set(self, name, props):
        cy = self.y.find(name)
        cj = J.find(self.j, name)
        assert cy is not None and cj is not None, ('set', name)
        for p, v in props.items():
            if v is None:
                cy.props.pop(p, None)
                cj['Rules'] = [r for r in cj['Rules'] if r['Property'] != p]
            else:
                cy.set(p, self._y(v))
                J.set_rule(cj, p, self._s(v))

    def screen_set(self, props):
        for p, v in props.items():
            self.y.set(p, self._y(v))
            J.set_rule(self.j, p, self._s(v))

    def add_html(self, name, props, parent=None, index=None):
        full = dict(HTML_DEFAULTS)
        full.update(props)
        # yaml
        cy = payaml.Ctrl(name)
        cy.meta.append(('Control', 'HtmlViewer@2.1.0'))
        for p, v in full.items():
            cy.set(p, self._y(v))
        py = self.y if parent is None else self.y.find(parent)
        assert py is not None, ('add_html parent', parent)
        if index is None:
            py.children.append(cy)
        else:
            py.children.insert(index, cy)
        # json
        pj = self.j if parent is None else J.find(self.j, parent)
        cj = J.clone(PROTO_HTML, name, pj['Name'])
        cj['Rules'] = [r for r in cj['Rules'] if r['Property'] not in full]
        for p, v in full.items():
            J.set_rule(cj, p, self._s(v))
        st = [r['Property'] for r in cj['Rules']]
        cj['ControlPropertyState'] = st
        if index is None:
            pj.setdefault('Children', []).append(cj)
        else:
            pj.setdefault('Children', []).insert(index, cj)
        return cy

    def clone_ctrl(self, src_name, new_name, props, parent=None, index=None):
        """Duplica um controle existente (mesmo screen) com novas propriedades."""
        sy = self.y.find(src_name)
        sj = J.find(self.j, src_name)
        assert sy and sj
        cy = payaml.Ctrl(new_name)
        cy.meta = list(sy.meta)
        cy.props = copy.deepcopy(sy.props)
        for p, v in props.items():
            if v is None:
                cy.props.pop(p, None)
            else:
                cy.set(p, self._y(v))
        py = self.y if parent is None else self.y.find(parent)
        (py.children.append(cy) if index is None else py.children.insert(index, cy))
        pj = self.j if parent is None else J.find(self.j, parent)
        cj = J.clone(sj, new_name, pj['Name'])
        for p, v in props.items():
            if v is None:
                cj['Rules'] = [r for r in cj['Rules'] if r['Property'] != p]
            else:
                J.set_rule(cj, p, self._s(v))
        (pj.setdefault('Children', []).append(cj) if index is None
         else pj.setdefault('Children', []).insert(index, cj))
        return cy

    def json_template_first(self, gal_name):
        """Mantem o galleryTemplate como primeiro filho na representacao JSON."""
        g = J.find(self.j, gal_name)
        tpl = [c for c in g['Children'] if c['Template']['Name'] == 'galleryTemplate']
        g['Children'] = tpl + [c for c in g['Children'] if c not in tpl]

    def move_to_end(self, name):
        py = self.y.parent_of(name)
        c = [x for x in py.children if x.name == name][0]
        py.children = [x for x in py.children if x.name != name] + [c]
        pj = J.parent_of(self.j, name)
        cj = [x for x in pj['Children'] if x['Name'] == name][0]
        pj['Children'] = [x for x in pj['Children'] if x['Name'] != name] + [cj]

    def move_to_start(self, name):
        py = self.y.parent_of(name)
        c = [x for x in py.children if x.name == name][0]
        py.children = [c] + [x for x in py.children if x.name != name]
        pj = J.parent_of(self.j, name)
        cj = [x for x in pj['Children'] if x['Name'] == name][0]
        pj['Children'] = [cj] + [x for x in pj['Children'] if x['Name'] != name]

    def get(self, name, prop):
        cy = self.y.find(name)
        if cy is None or prop not in cy.props:
            return None
        v = '\n'.join(cy.props[prop])
        return v[1:] if v.startswith('=') else v

    def names(self):
        return [c.name for c in self.y.children]

    def save(self):
        J.reindex(self.j)
        payaml.dump_screen(self.y, self.yaml_path)
        J.save(self.jdoc, self.json_path)
