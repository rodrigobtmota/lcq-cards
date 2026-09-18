# -*- coding: utf-8 -*-
"""Empacotamento da REV02.2: msapp, pacote de importacao e fontes auditaveis."""
import os, sys, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import caminhos

BASE = caminhos.RAIZ
BUILD, TOOLS, EVID = caminhos.saida('build'), caminhos.FERRAMENTAS, caminhos.saida('evidencias')
DIST = caminhos.saida('dist_rev02_2')
MSAPP = os.path.join(DIST, 'SGC_LCQ_RJ_VISUAL_RADAR_REV02_2.msapp')
PKG = os.path.join(DIST, 'SGC_LCQ_RJ_VISUAL_RADAR_REV02_2_IMPORT.zip')
FONTES = os.path.join(DIST, 'SGC_LCQ_RJ_VISUAL_RADAR_REV02_2_FONTES.zip')
DOC = 'Microsoft.PowerApps/apps/11773394310992049878/Nd3ebf7dc-113a-45b6-9474-76e0c65b7319-document.msapp'

SCRIPTS = ['caminhos.py', 'payaml.py', 'jsonctl.py', 'ops.py', 'design.py', 'migrate.py',
           'rev02.py', 'verify.py', 'verify_rev02.py', 'render_evidencias.py',
           'pack.py', 'pack_rev02.py', 'pack_rev021.py', 'pack_rev022.py', 'verify_rev022.py',
           'proto_htmlviewer.json', 'proto_template_htmlviewer.json',
           'proto_image.json', 'proto_template_image.json', 'faixa_cabecalho_lcq.png']
ENTRADAS = ['sgc', 'pkg', 'build_rev01', 'build_rev01_prefaixa', 'build_rev02_1']


def add_dir(z, src, prefixo):
    for raiz, _, arquivos in os.walk(src):
        for f in sorted(arquivos):
            p = os.path.join(raiz, f)
            rel = os.path.relpath(p, src).replace(os.sep, '/')
            z.write(p, prefixo + rel)


def main():
    os.makedirs(DIST, exist_ok=True)
    with zipfile.ZipFile(MSAPP, 'w', zipfile.ZIP_DEFLATED) as z:
        add_dir(z, BUILD, '')
    orig_pkg = caminhos.entrada('pkg')
    with zipfile.ZipFile(PKG, 'w', zipfile.ZIP_DEFLATED) as z:
        for raiz, _, arquivos in os.walk(orig_pkg):
            for f in sorted(arquivos):
                p = os.path.join(raiz, f)
                rel = os.path.relpath(p, orig_pkg).replace(os.sep, '/')
                z.write(MSAPP if rel == DOC else p, rel)
    with zipfile.ZipFile(FONTES, 'w', zipfile.ZIP_DEFLATED) as z:
        add_dir(z, BUILD, '')
        for s in SCRIPTS:
            caminho = os.path.join(TOOLS, s)
            if os.path.isfile(caminho):
                z.write(caminho, 'ferramentas/' + s)
        for origem in (os.path.join(TOOLS, 'REPRODUZIR.md'), os.path.join(BASE, 'REPRODUZIR.md')):
            if os.path.isfile(origem):
                z.write(origem, 'REPRODUZIR.md')
                break
        if os.path.isdir(EVID):
            add_dir(z, EVID, 'evidencias/')
        for e in ENTRADAS:
            add_dir(z, caminhos.entrada(e), 'entrada/%s/' % e)
    for f in (MSAPP, PKG, FONTES):
        print('%-52s %8.1f KB' % (os.path.basename(f), os.path.getsize(f) / 1024))


if __name__ == '__main__':
    main()
