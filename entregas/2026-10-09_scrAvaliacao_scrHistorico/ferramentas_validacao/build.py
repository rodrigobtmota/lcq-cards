"""Gera o .msapp consolidado e o pacote importável a partir dos arquivos de origem.

Uso: python3 -I build.py <scratchpad>
"""
import glob
import json
import os
import shutil
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pa_edit import Screen  # noqa: E402
import changes_avaliacao  # noqa: E402
import changes_historico  # noqa: E402

S = sys.argv[1]
SRC_MSAPP = os.path.join(S, 'orig.msapp')
SRC_ZIP = os.path.join(S, 'orig.zip')
WORK = os.path.join(S, 'work')
OUT = os.path.join(S, 'out')
MSAPP_NAME = 'SGC_LCQ_RJ_AVALIACAO_CONTEXTO_FINAL.msapp'
ZIP_NAME = 'SGC_LCQ_RJ_AVALIACAO_CONTEXTO_FINAL_IMPORTAVEL.zip'

shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(OUT, exist_ok=True)

# 1) descompactar preservando nomes originais das entradas (com '\')
with zipfile.ZipFile(SRC_MSAPP) as z:
    entries = [(i, z.read(i.filename)) for i in z.infolist()]
files = {}
for info, data in entries:
    p = os.path.join(WORK, *info.filename.split('\\'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'wb').write(data)
    files[info.filename] = p

# 2) alocador de IDs únicos no app inteiro
mx_uid, mx_poi = 0, 0
for f in glob.glob(os.path.join(WORK, 'Controls', '*.json')):
    d = json.load(open(f, encoding='utf-8'))

    def walk(c):
        global mx_uid, mx_poi
        mx_uid = max(mx_uid, int(c['ControlUniqueId']))
        mx_poi = max(mx_poi, c['PublishOrderIndex'])
        for ch in c.get('Children', []):
            walk(ch)
    walk(d['TopParent'])
state = {'uid': mx_uid, 'poi': mx_poi}


def alloc():
    state['uid'] += 1
    state['poi'] += 1
    return state['uid'], state['poi']


# 3) aplicar alterações
screens = []
for ctrl_file, yaml_file, mod in (('563.json', 'scrAvaliacao.pa.yaml', changes_avaliacao),
                                  ('678.json', 'scrHistoricoAvaliacoes.pa.yaml', changes_historico)):
    sc = Screen(os.path.join(WORK, 'Controls', ctrl_file), os.path.join(WORK, 'Src', yaml_file), alloc)
    mod.apply(sc)
    sc.save()
    screens.append(sc)

# 4) Properties.json: contagem de controles (informativa)
pp = os.path.join(WORK, 'Properties.json')
raw = open(pp, encoding='utf-8').read()
props = json.loads(raw)
for sc in screens:
    for _, tpl, _, _ in sc.created:
        props['ControlCount'][tpl] = props['ControlCount'].get(tpl, 0) + 1
open(pp, 'w', encoding='utf-8', newline='').write(json.dumps(props, ensure_ascii=False, indent=2).replace('\n', '\r\n'))

# 5) empacotar .msapp com a mesma ordem/nomes/compressão do original
out_msapp = os.path.join(OUT, MSAPP_NAME)
with zipfile.ZipFile(out_msapp, 'w') as zout:
    for info, _ in entries:
        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        zi.compress_type = info.compress_type
        zi.external_attr = info.external_attr
        zi.create_system = info.create_system
        zout.writestr(zi, open(files[info.filename], 'rb').read())

# 6) pacote importável: estrutura original, troca somente o document.msapp
out_zip = os.path.join(OUT, ZIP_NAME)
with zipfile.ZipFile(SRC_ZIP) as zin, zipfile.ZipFile(out_zip, 'w') as zout:
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename.endswith('-document.msapp'):
            data = open(out_msapp, 'rb').read()
        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        zi.compress_type = info.compress_type
        zi.external_attr = info.external_attr
        zi.create_system = info.create_system
        zout.writestr(zi, data)

# 7) registro de alterações para relatório
log = []
for sc in screens:
    for c, p, a, b in sc.changes:
        log.append({'tela': sc.name, 'controle': c, 'propriedade': p, 'antes': a, 'depois': b})
created = [{'tela': sc.name, 'controle': n, 'tipo': t, 'pai': p, 'modelo': m} for sc in screens for n, t, p, m in sc.created]
json.dump({'alteracoes': log, 'criados': created}, open(os.path.join(S, 'changes_log.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('alterações:', len(log), 'controles criados:', len(created))
print(out_msapp)
print(out_zip)
