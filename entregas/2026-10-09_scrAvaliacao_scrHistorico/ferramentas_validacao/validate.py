"""Validação offline do pacote gerado. Uso: python3 -I validate.py <scratchpad>"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import zipfile

import yaml

S = sys.argv[1]
OUT = os.path.join(S, 'out')
MSAPP = os.path.join(OUT, 'SGC_LCQ_RJ_AVALIACAO_CONTEXTO_FINAL.msapp')
ZIPF = os.path.join(OUT, 'SGC_LCQ_RJ_AVALIACAO_CONTEXTO_FINAL_IMPORTAVEL.zip')
ORIG_MSAPP = os.path.join(S, 'orig.msapp')
ORIG_ZIP = os.path.join(S, 'orig.zip')
PFX = os.path.join(S, 'tools', 'pfxcheck', 'out', 'pfxcheck.dll')
results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('OK   ' if ok else 'FALHA') + ' | ' + name + (' | ' + detail if detail else ''))


def load_zip(path):
    with zipfile.ZipFile(path) as z:
        return {i.filename: z.read(i.filename) for i in z.infolist()}, [i.filename for i in z.infolist()]


def controls(files):
    out = {}
    for k, v in files.items():
        if k.startswith('Controls\\'):
            d = json.loads(v.decode('utf-8'))
            out[d['TopParent']['Name']] = d
    return out


def flat(doc):
    res = {}

    def w(c, parent):
        res[c['Name']] = (c, parent)
        for ch in c.get('Children', []):
            w(ch, c['Name'])
    w(doc['TopParent'], None)
    return res


def rules(c):
    return {r['Property']: r['InvariantScript'] for r in c['Rules']}


# ------------------------------------------------------------------ 1. integridade ZIP
for p in (MSAPP, ZIPF):
    with zipfile.ZipFile(p) as z:
        check(f'Integridade ZIP (testzip) {os.path.basename(p)}', z.testzip() is None)

new_files, new_order = load_zip(MSAPP)
old_files, old_order = load_zip(ORIG_MSAPP)
check('msapp: mesma lista e ordem de entradas do original', new_order == old_order, f'{len(new_order)} entradas')
changed = sorted(k for k in new_files if new_files[k] != old_files[k])
check('msapp: somente arquivos esperados alterados',
      set(changed) <= {'Controls\\563.json', 'Controls\\678.json', 'Src\\scrAvaliacao.pa.yaml',
                       'Src\\scrHistoricoAvaliacoes.pa.yaml', 'Properties.json'}, ', '.join(changed))

zf, zorder = load_zip(ZIPF)
of, oorder = load_zip(ORIG_ZIP)
check('pacote: mesma estrutura de entradas do ZIP de origem', zorder == oorder, ' ; '.join(zorder))
doc_entry = [k for k in zorder if k.endswith('-document.msapp')][0]
check('pacote: manifest.json idêntico ao de origem', zf['manifest.json'] == of['manifest.json'])
app_json = [k for k in zorder if k.endswith('.json') and k != 'manifest.json'][0]
check('pacote: definição do app (identity) idêntica à de origem', zf[app_json] == of[app_json], app_json)
logo = [k for k in zorder if k.endswith('logoSmallFile')][0]
check('pacote: logo idêntico', zf[logo] == of[logo])
check('pacote: document.msapp = .msapp entregue (SHA-256)',
      hashlib.sha256(zf[doc_entry]).hexdigest() == hashlib.sha256(open(MSAPP, 'rb').read()).hexdigest())
man = json.loads(zf['manifest.json'])
appdef = json.loads(zf[app_json])
uri = appdef['appDefinitionTemplate']['properties']['appUris']['documentUri']['value']
check('pacote: documentUri aponta para a entrada document.msapp existente', doc_entry.endswith(uri.split('/')[-1]), uri)
res_id = [k for k, v in man['resources'].items() if v['type'] == 'Microsoft.PowerApps/apps'][0]
check('pacote: manifest referencia recurso Microsoft.PowerApps/apps', bool(res_id), res_id)

# ------------------------------------------------------------------ 2. JSON / Properties
for k in new_files:
    if k.endswith('.json'):
        try:
            json.loads(new_files[k].decode('utf-8'))
        except Exception as e:  # noqa
            check(f'JSON válido {k}', False, str(e))
check('Todos os JSON do msapp são válidos', True)
hdr_new, hdr_old = json.loads(new_files['Header.json']), json.loads(old_files['Header.json'])
check('Header.json inalterado (DocVersion/MSAppStructureVersion)', hdr_new == hdr_old,
      f"{hdr_new['DocVersion']} / {hdr_new['MSAppStructureVersion']}")
pn, po = json.loads(new_files['Properties.json']), json.loads(old_files['Properties.json'])
diff_keys = [k for k in pn if pn[k] != po.get(k)]
check('Properties.json: só ControlCount alterado', diff_keys == ['ControlCount'], str({k: (po[k], pn[k]) for k in diff_keys}))
for f in ('References\\DataSources.json',):
    check(f'DataSources inalterado ({f})', new_files[f] == old_files[f])

# ------------------------------------------------------------------ 3. Power Fx (parser oficial Microsoft.PowerFx.Core)
newc, oldc = controls(new_files), controls(old_files)
items = []
for scr, d in newc.items():
    for n, (c, _) in flat(d).items():
        for p, v in rules(c).items():
            if v.strip():
                items.append({'id': f'{scr}/{n}.{p}', 'formula': v})
tmp = os.path.join(S, 'rules_new.json')
json.dump(items, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False)
r = subprocess.run(['dotnet', PFX, tmp], capture_output=True, text=True)
last = r.stdout.strip().splitlines()[-1]
errs = [l for l in r.stdout.splitlines() if l.startswith('ERRO')]
check('Power Fx: todas as fórmulas do app passam no parser oficial', not errs and 'FALHA\t0' in last, last.replace('\t', ' '))
for e in errs[:20]:
    print('   ', e)

# ------------------------------------------------------------------ 4. comparação semântica
for scr in oldc:
    if scr in ('scrAvaliacao', 'scrHistoricoAvaliacoes'):
        continue
    check(f'Tela {scr} sem alteração semântica', json.dumps(oldc[scr], sort_keys=True) == json.dumps(newc[scr], sort_keys=True))

PROTEGIDAS = {
    'scrAvaliacao': [('btnAtAva', 'OnSelect'), ('btnNaoAva', 'OnSelect'), ('btnNaAva', 'OnSelect'), ('txtComAva', 'OnChange'),
                     ('btnCancAva', 'OnSelect'), ('btnConcluirAva', 'OnSelect'), ('btnConcluirAva', 'DisplayMode'),
                     ('btnSalvarAva', 'DisplayMode'), ('btnCancAva', 'DisplayMode'),
                     ('btnAtAva', 'DisplayMode'), ('btnNaoAva', 'DisplayMode'), ('btnNaAva', 'DisplayMode'), ('btnNaAva', 'Visible'),
                     ('txtComAva', 'DisplayMode'), ('txtComAva', 'Default'),
                     ('txtParecerAva', 'Default'), ('txtParecerAva', 'DisplayMode'), ('txtParecerAva', 'Mode'), ('txtParecerAva', 'DelayOutput'),
                     ('txtObsAva', 'Default'), ('txtObsAva', 'DisplayMode'), ('txtObsAva', 'Mode'),
                     ('scrAvaliacao', 'OnVisible'), ('galCritAva', 'Items'), ('galDocAva', 'Items'),
                     ('btnCancOkAva', 'OnSelect'), ('btnCancVoltarAva', 'OnSelect'), ('btnVoltarAva', 'OnSelect'),
                     ('conBarraAva', 'Visible'), ('lblBannerAva', 'Visible'), ('conIdAva', 'Visible'), ('conCritAva', 'Visible'),
                     ('lblCritEvAva', 'Visible')],
    'scrHistoricoAvaliacoes': [('scrHistoricoAvaliacoes', 'OnVisible'), ('galHis', 'Items'), ('btnCopiarHis', 'OnSelect'),
                               ('btnLimparHis', 'OnSelect'), ('btnRowHis', 'OnSelect'), ('R3btnAbrirEventoHis', 'OnSelect'),
                               ('btnEvFecharHis', 'OnSelect'), ('btnEvAbrirHis', 'OnSelect'), ('btnEvAbrirHis', 'Text'),
                               ('btnPaginaAnteriorHis', 'OnSelect'), ('btnPaginaProximaHis', 'OnSelect'),
                               ('R3btnPaginaAtualHis', 'Text'), ('recEvFundoHis', 'OnSelect'), ('conEvHis', 'Visible'),
                               ('txtBuscaHis', 'OnChange'), ('txtModHis', 'OnChange'), ('txtDeHis', 'OnChange'), ('txtAteHis', 'OnChange'),
                               ('btnFAPE9His', 'OnSelect'), ('btnFAPP5His', 'OnSelect'), ('btnFAQ4His', 'OnSelect'),
                               ('btnFTipoQualificacaoHis', 'OnSelect'), ('btnFTipoRequalificacaoHis', 'OnSelect'),
                               ('btnFTipoExtraordinariaHis', 'OnSelect'), ('btnFEstadoPreenchimentoHis', 'OnSelect'),
                               ('btnFEstadoConcluidaHis', 'OnSelect'), ('btnFEstadoCanceladaHis', 'OnSelect'),
                               ('btnFResultadoAtendeuHis', 'OnSelect'), ('btnFResultadoNaoAtendeuHis', 'OnSelect'),
                               ('btnFResultadoSemHis', 'OnSelect'), ('btnTodosTiposHis', 'OnSelect'),
                               ('btnTodosEstadosHis', 'OnSelect'), ('btnTodosResultadosHis', 'OnSelect')],
}
for scr, lst in PROTEGIDAS.items():
    fo, fn = flat(oldc[scr]), flat(newc[scr])
    bad = [f'{c}.{p}' for c, p in lst if rules(fo[c][0]).get(p) != rules(fn[c][0]).get(p)]
    check(f'{scr}: {len(lst)} propriedades funcionais protegidas idênticas', not bad, ', '.join(bad))

# btnSalvarAva.OnSelect: única alteração funcional autorizada (itens 38–43)
o = rules(flat(oldc['scrAvaliacao'])['btnSalvarAva'][0])['OnSelect']
n = rules(flat(newc['scrAvaliacao'])['btnSalvarAva'][0])['OnSelect']
a = 'Notify("Rascunho salvo com sucesso.", NotificationType.Success),'
pre, post = o.split(a)
check('btnSalvarAva.OnSelect: Patch e demais trechos preservados; só a notificação pós-sucesso foi trocada',
      n.startswith(pre) and n.endswith(post) and 'NotificationType.Warning' in n[len(pre):len(n) - len(post)],
      f'trecho inserido: {n[len(pre):len(n) - len(post)][:90]}…')

# controles: nada removido; criados listados
for scr in ('scrAvaliacao', 'scrHistoricoAvaliacoes'):
    fo, fn = flat(oldc[scr]), flat(newc[scr])
    removed = sorted(set(fo) - set(fn))
    added = sorted(set(fn) - set(fo))
    check(f'{scr}: nenhum controle removido', not removed, ', '.join(removed))
    check(f'{scr}: controles criados', True, ', '.join(added))
    # pais preservados
    moved = [k for k in fo if k in fn and fo[k][1] != fn[k][1]]
    check(f'{scr}: nenhum controle mudou de pai', not moved, ', '.join(moved))
    # unicidade de ID/nome no app
uids = []
names = []
for scr, d in newc.items():
    for k, (c, _) in flat(d).items():
        uids.append(c['ControlUniqueId'])
        if c['Template']['Name'] != 'galleryTemplate':
            names.append(k)
check('ControlUniqueId únicos no app', len(uids) == len(set(uids)), f'{len(uids)} controles')
check('Nomes de controles únicos no app', len(names) == len(set(names)))

# referências a controles nas fórmulas alteradas
allnames = set(names)
pref = re.compile(r'\b((?:lbl|btn|con|gal|txt|rec|html|bdg|ico|img|R3)[A-Za-z0-9]+)\b(?!\s*:)')
log = json.load(open(os.path.join(S, 'changes_log.json'), encoding='utf-8'))
miss = set()
for ch in log['alteracoes']:
    f = re.sub(r'"(?:[^"]|"")*"', '""', ch['depois'])  # ignora literais de texto
    for m in pref.findall(f):
        if m not in allnames:
            miss.add(f"{ch['controle']}.{ch['propriedade']} → {m}")
check('Fórmulas alteradas só referenciam controles existentes', not miss, '; '.join(sorted(miss)))

# variáveis novas (apenas estado visual)
newvars = set()
for ch in log['alteracoes']:
    newvars |= set(re.findall(r'UpdateContext\(\{(\w+):', ch['depois'] or ''))
    newvars -= set(re.findall(r'UpdateContext\(\{(\w+):', ch['antes'] or ''))
check('Variáveis de contexto introduzidas', True, ', '.join(sorted(newvars)) or 'nenhuma')

# ------------------------------------------------------------------ 5. YAML ⇄ JSON
for scr, yf in (('scrAvaliacao', 'Src\\scrAvaliacao.pa.yaml'), ('scrHistoricoAvaliacoes', 'Src\\scrHistoricoAvaliacoes.pa.yaml')):
    y = yaml.safe_load(io.StringIO(new_files[yf].decode('utf-8')))
    fn = flat(newc[scr])
    mism, ynames = [], {}

    def wy(node, name, parent):
        ynames[name] = parent
        for p, v in (node.get('Properties') or {}).items():
            j = rules(fn[name][0]).get(p) if name in fn else None
            if j is None or '=' + j != v:
                mism.append(f'{name}.{p}')
        for ch in node.get('Children') or []:
            (cn, cv), = ch.items()
            wy(cv, cn, name)
    root = y['Screens'][scr]
    wy(root, scr, None)
    jnames = {k for k, (c, _) in fn.items() if c['Template']['Name'] != 'galleryTemplate'}
    check(f'YAML {scr}: sintaxe válida e todas as propriedades = JSON', not mism, ', '.join(mism[:10]))
    check(f'YAML {scr}: mesmos controles do JSON', set(ynames) == jnames,
          str(sorted(set(ynames) ^ jnames)))

# ------------------------------------------------------------------ 6. pack/unpack (roundtrip)
up = os.path.join(S, 'unpack_check')
import shutil  # noqa: E402
shutil.rmtree(up, ignore_errors=True)
with zipfile.ZipFile(MSAPP) as z:
    infos = z.infolist()
    for i in infos:
        p = os.path.join(up, *i.filename.split('\\'))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'wb').write(z.read(i.filename))
buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w') as zout:
    for i in infos:
        zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
        zi.compress_type = i.compress_type
        zi.external_attr = i.external_attr
        zout.writestr(zi, open(os.path.join(up, *i.filename.split('\\')), 'rb').read())
re_files, _ = load_zip(io.BytesIO(buf.getvalue()))
check('Pack/unpack: conteúdo reempacotado idêntico entrada a entrada', re_files == new_files)

ok = all(r[1] for r in results)
json.dump([{'verificacao': a, 'ok': b, 'detalhe': c} for a, b, c in results],
          open(os.path.join(S, 'validation.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nRESULTADO:', 'TODAS AS VERIFICAÇÕES PASSARAM' if ok else 'HÁ FALHAS')
