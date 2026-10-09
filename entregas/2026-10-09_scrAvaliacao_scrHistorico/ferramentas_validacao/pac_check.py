"""Validação independente com o Power Platform CLI (pac canvas unpack/pack).
Uso: python3 -I pac_check.py <scratchpad>
"""
import filecmp
import json
import os
import shutil
import subprocess
import sys

S = sys.argv[1]
P = os.path.join(S, 'tools', 'pac')
PAC = os.path.join(P, 'pkg', 'tools', 'pac')
NEW = os.path.join(S, 'out', 'SGC_LCQ_RJ_AVALIACAO_CONTEXTO_FINAL.msapp')
res = []


def run(*a):
    r = subprocess.run([PAC, 'canvas', *a], capture_output=True, text=True, cwd=P)
    return r.returncode, (r.stdout + r.stderr)


def diff_tree(a, b):
    out = []
    cmp = filecmp.dircmp(a, b)

    def walk(c, rel=''):
        out.extend(os.path.join(rel, x) for x in c.diff_files + c.left_only + c.right_only)
        for k, sub in c.subdirs.items():
            walk(sub, os.path.join(rel, k))
    walk(cmp)
    return sorted(out)


ver = subprocess.run([PAC, 'help'], capture_output=True, text=True).stdout.split('\n')[1].strip()
for f in ('repacked.msapp',):
    if os.path.exists(os.path.join(P, f)):
        os.remove(os.path.join(P, f))
for d in ('un_orig', 'un_new', 'un_re'):
    shutil.rmtree(os.path.join(P, d), ignore_errors=True)
rc1, o1 = run('unpack', '--msapp', os.path.join(S, 'orig.msapp'), '--sources', 'un_orig')
rc2, o2 = run('unpack', '--msapp', NEW, '--sources', 'un_new')
res.append({'etapa': f'pac canvas unpack do .msapp entregue ({ver})', 'ok': rc2 == 0 and 'error' not in o2.lower(),
            'detalhe': 'sem erros nem avisos de checksum' if rc2 == 0 else o2[-300:]})
rc3, o3 = run('pack', '--sources', 'un_new', '--msapp', 'repacked.msapp')
res.append({'etapa': 'pac canvas pack das fontes desempacotadas', 'ok': rc3 == 0, 'detalhe': 'repacked.msapp gerado' if rc3 == 0 else o3[-300:]})
rc4, o4 = run('unpack', '--msapp', 'repacked.msapp', '--sources', 'un_re')
d_rt = diff_tree(os.path.join(P, 'un_new'), os.path.join(P, 'un_re'))
res.append({'etapa': 'Roundtrip pac (unpack → pack → unpack): fontes idênticas', 'ok': rc4 == 0 and not d_rt,
            'detalhe': 'nenhuma diferença' if not d_rt else ', '.join(d_rt)})
d_on = diff_tree(os.path.join(P, 'un_orig'), os.path.join(P, 'un_new'))
esperado = {'Entropy/Entropy.json', 'Entropy/checksum.json', 'Other/Src/scrAvaliacao.pa.yaml', 'Other/Src/scrHistoricoAvaliacoes.pa.yaml',
            'Src/EditorState/scrAvaliacao.editorstate.json', 'Src/EditorState/scrHistoricoAvaliacoes.editorstate.json',
            'Src/scrAvaliacao.fx.yaml', 'Src/scrHistoricoAvaliacoes.fx.yaml'}
res.append({'etapa': 'Original × novo (fontes pac): diferenças só nas 2 telas e nos metadados de controle',
            'ok': set(d_on) <= esperado, 'detalhe': ', '.join(d_on)})
json.dump(res, open(os.path.join(S, 'pac_check.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in res:
    print(('OK   ' if r['ok'] else 'FALHA') + ' | ' + r['etapa'] + ' | ' + r['detalhe'][:200])
