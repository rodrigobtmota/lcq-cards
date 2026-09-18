# -*- coding: utf-8 -*-
"""Empacota o msapp e o pacote de importacao do Power Apps."""
import os, zipfile, shutil, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(BASE, 'build')
DIST = os.path.join(BASE, 'dist')
MSAPP = os.path.join(DIST, 'SGC_LCQ_RJ_VISUAL_RADAR.msapp')
PKG = os.path.join(DIST, 'SGC_LCQ_RJ_VISUAL_RADAR_IMPORT.zip')
FONTES = os.path.join(DIST, 'SGC_LCQ_RJ_VISUAL_RADAR_FONTES.zip')
ORIG_PKG = os.path.join(BASE, 'pkg')
DOCNAME = 'Microsoft.PowerApps/apps/11773394310992049878/Nd3ebf7dc-113a-45b6-9474-76e0c65b7319-document.msapp'


def zipdir(src, dest, arc_prefix=''):
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(src):
            for f in sorted(files):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, src).replace(os.sep, '/')
                z.write(p, arc_prefix + rel)


def main():
    os.makedirs(DIST, exist_ok=True)
    zipdir(BUILD, MSAPP)
    # pacote de importacao: mantem manifest, identity e logo originais
    with zipfile.ZipFile(PKG, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(ORIG_PKG):
            for f in sorted(files):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, ORIG_PKG).replace(os.sep, '/')
                if rel == DOCNAME:
                    z.write(MSAPP, rel)
                else:
                    z.write(p, rel)
    zipdir(BUILD, FONTES, 'SGC_LCQ_RJ_VISUAL_RADAR_FONTES/')
    for f in (MSAPP, PKG, FONTES):
        print('%-70s %8.1f KB' % (os.path.basename(f), os.path.getsize(f) / 1024))


if __name__ == '__main__':
    main()
