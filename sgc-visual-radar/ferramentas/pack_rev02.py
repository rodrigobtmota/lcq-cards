# -*- coding: utf-8 -*-
"""Empacotamento da REV02: msapp, pacote de importacao e fontes auditaveis."""
import os, sys, zipfile, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import caminhos

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD, TOOLS, EVID = (os.path.join(BASE, d) for d in ('build', 'tools', 'evidencias'))
DIST = os.path.join(BASE, 'dist_rev02')
MSAPP = os.path.join(DIST, 'SGC_LCQ_RJ_VISUAL_RADAR_REV02.msapp')
PKG = os.path.join(DIST, 'SGC_LCQ_RJ_VISUAL_RADAR_REV02_IMPORT.zip')
FONTES = os.path.join(DIST, 'SGC_LCQ_RJ_VISUAL_RADAR_REV02_FONTES.zip')
ORIG_PKG = caminhos.entrada('pkg')
DOC = 'Microsoft.PowerApps/apps/11773394310992049878/Nd3ebf7dc-113a-45b6-9474-76e0c65b7319-document.msapp'

SCRIPTS = ['payaml.py', 'jsonctl.py', 'ops.py', 'design.py', 'migrate.py', 'rev02.py',
           'verify.py', 'verify_rev02.py', 'render_evidencias.py', 'pack.py', 'pack_rev02.py',
           'proto_htmlviewer.json', 'proto_template_htmlviewer.json',
           'proto_image.json', 'proto_template_image.json', 'faixa_cabecalho_lcq.png']


def add_dir(z, src, prefix):
    for root, _, files in os.walk(src):
        for f in sorted(files):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, src).replace(os.sep, '/')
            z.write(p, prefix + rel)


def main():
    os.makedirs(DIST, exist_ok=True)
    with zipfile.ZipFile(MSAPP, 'w', zipfile.ZIP_DEFLATED) as z:
        add_dir(z, BUILD, '')
    with zipfile.ZipFile(PKG, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(ORIG_PKG):
            for f in sorted(files):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, ORIG_PKG).replace(os.sep, '/')
                z.write(MSAPP if rel == DOC else p, rel)
    with zipfile.ZipFile(FONTES, 'w', zipfile.ZIP_DEFLATED) as z:
        add_dir(z, BUILD, '')
        for s in SCRIPTS:
            caminho = os.path.join(TOOLS, s)
            if os.path.isfile(caminho):
                z.write(caminho, 'ferramentas/' + s)
        add_dir(z, EVID, 'evidencias/')
    for f in (MSAPP, PKG, FONTES):
        print('%-52s %8.1f KB' % (os.path.basename(f), os.path.getsize(f) / 1024))


if __name__ == '__main__':
    main()
