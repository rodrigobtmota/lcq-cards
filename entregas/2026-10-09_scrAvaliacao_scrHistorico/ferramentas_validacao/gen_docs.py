"""Gera TXT de fórmulas (pt-BR), CSV de alterações, relatório e manifesto SHA-256.
Uso: python3 -I gen_docs.py <scratchpad>
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
from collections import OrderedDict, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ptbr import to_ptbr  # noqa: E402

S = sys.argv[1]
OUT = os.path.join(S, 'out')
log = json.load(open(os.path.join(S, 'changes_log.json'), encoding='utf-8'))
val = json.load(open(os.path.join(S, 'validation.json'), encoding='utf-8'))
tcs = json.load(open(os.path.join(S, 'tc_results.json'), encoding='utf-8'))['resultados']
pac = json.load(open(os.path.join(S, 'pac_check.json'), encoding='utf-8'))

GEO = {'X', 'Y', 'Width', 'Height', 'TemplateSize', 'WrapCount'}
FUN = {'OnSelect', 'OnChange', 'OnVisible', 'Items', 'DisplayMode', 'Default'}
TXT = {'HtmlText', 'Text', 'HintText', 'Tooltip'}
AUTORIZADAS = {
    ('scrAvaliacao', 'btnSalvarAva', 'OnSelect'): 'Itens 38–43: aviso de comentários pendentes após o rascunho salvo. Patch preservado; só a notificação de sucesso foi trocada.',
    ('scrHistoricoAvaliacoes', 'btnEvTecHis', 'OnSelect'): 'Item 24 (Histórico): botão novo que só alterna a variável de tela locEvTec (mostrar/ocultar Informações técnicas). Não grava dados.',
    ('scrHistoricoAvaliacoes', 'galEvCritHis', 'Items'): 'Item 25 (Histórico): leitura do mesmo CriteriosJson preservado, acrescentando os campos dimensao e fontes para exibir título e referência técnica. Somente leitura.',
}


def cat(c):
    if (c['tela'], c['controle'], c['propriedade']) in AUTORIZADAS:
        return 'FUNCIONAL (autorizada)'
    p = c['propriedade']
    if p in FUN:
        return 'FUNCIONAL'
    if p in GEO:
        return 'GEOMETRIA'
    if p in TXT:
        return 'TEXTO/CONTEÚDO'
    return 'VISUAL'


created = {(x['tela'], x['controle']) for x in log['criados']}
for c in log['alteracoes']:
    c['categoria'] = cat(c)
nao_aut = [c for c in log['alteracoes'] if c['categoria'] == 'FUNCIONAL']

# ------------------------------------------------------------------ validação pt-BR das fórmulas do TXT
items = [{'id': f"{c['tela']}/{c['controle']}.{c['propriedade']}", 'formula': to_ptbr(c['depois'])} for c in log['alteracoes']]
json.dump(items, open(os.path.join(S, 'rules_ptbr.json'), 'w'), ensure_ascii=False)
r = subprocess.run(['dotnet', os.path.join(S, 'tools/pfxcheck/out/pfxcheck.dll'), os.path.join(S, 'rules_ptbr.json'), 'pt-BR'],
                   capture_output=True, text=True)
ptbr_line = r.stdout.strip().splitlines()[-1].replace('\t', ' ')
ptbr_ok = 'FALHA 0' in ptbr_line

# ------------------------------------------------------------------ TXT pt-BR
por = OrderedDict()
for c in log['alteracoes']:
    por.setdefault(c['tela'], OrderedDict()).setdefault(c['controle'], []).append(c)
L = []
L.append('SGC LCQ RJ — FÓRMULAS ALTERADAS (notação pt-BR do Power Apps Studio)')
L.append('Telas: scrAvaliacao (Contexto da avaliação + Base documental no topo) e scrHistoricoAvaliacoes')
L.append('Status: CANDIDATO VISUAL E FUNCIONAL À HOMOLOGAÇÃO NO TENANT')
L.append('')
L.append('Como usar: o .msapp entregue já contém todas as fórmulas abaixo. Este arquivo serve para conferência')
L.append('e para reaplicação manual, se necessário. Separadores pt-BR: ";" entre argumentos, ";;" entre ações')
L.append('e "," como separador decimal. Textos entre aspas não foram alterados.')
L.append(f'Validação: {ptbr_line} (parser oficial Microsoft.PowerFx, cultura pt-BR).')
L.append('')
L.append('Legenda: [NOVO] controle criado nesta versão · [FUNCIONAL AUTORIZADA] alteração de comportamento autorizada.')
for tela, ctrls in por.items():
    L.append('')
    L.append('=' * 100)
    L.append(f'TELA: {tela}')
    L.append('=' * 100)
    for ctrl, chs in ctrls.items():
        L.append('')
        tag = ' [NOVO]' if (tela, ctrl) in created else ''
        L.append(f'--- {ctrl}{tag} ' + '-' * max(3, 80 - len(ctrl) - len(tag)))
        for c in chs:
            aut = ' [FUNCIONAL AUTORIZADA]' if c['categoria'].startswith('FUNCIONAL') else ''
            L.append(f'{c["propriedade"]}{aut}:')
            L.append('=' + to_ptbr(c['depois']))
            L.append('')
open(os.path.join(OUT, 'CODIGOS_AVALIACAO_CONTEXTO_FINAL_ptBR.txt'), 'w', encoding='utf-8').write('\n'.join(L))

# ------------------------------------------------------------------ CSV
with open(os.path.join(OUT, 'CONTROLES_PROPRIEDADES_ALTERADAS.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['Tela', 'Controle', 'Situação do controle', 'Propriedade', 'Categoria', 'Fórmula anterior (invariante)', 'Fórmula nova (invariante)'])
    for c in log['alteracoes']:
        w.writerow([c['tela'], c['controle'], 'criado' if (c['tela'], c['controle']) in created else 'existente',
                    c['propriedade'], c['categoria'], c['antes'] if c['antes'] is not None else '(não definida)', c['depois']])

# ------------------------------------------------------------------ relatório
cnt = defaultdict(lambda: defaultdict(int))
ctrl_by_cat = defaultdict(lambda: defaultdict(set))
for c in log['alteracoes']:
    cnt[c['tela']][c['categoria']] += 1
    ctrl_by_cat[c['tela']][c['categoria']].add(c['controle'])
ocultos = sorted({(c['tela'], c['controle']) for c in log['alteracoes'] if c['propriedade'] == 'Visible' and c['depois'] == 'false'})
condicionais = sorted({(c['tela'], c['controle'], c['depois']) for c in log['alteracoes'] if c['propriedade'] == 'Visible' and c['depois'] not in ('false', 'true') and (c['tela'], c['controle']) not in created})
ctrl_alt = sorted({(c['tela'], c['controle']) for c in log['alteracoes'] if (c['tela'], c['controle']) not in created})
val_ok = sum(1 for v in val if v['ok'])
tc_ok = sum(1 for t in tcs if t['ok'])


def tabela_props(tela):
    linhas = ['| Controle | Propriedades alteradas |', '|---|---|']
    props = OrderedDict()
    for c in log['alteracoes']:
        if c['tela'] == tela:
            props.setdefault(c['controle'], []).append(c['propriedade'])
    for k, v in props.items():
        linhas.append(f"| `{k}`{' **(novo)**' if (tela, k) in created else ''} | {', '.join(dict.fromkeys(v))} |")
    return '\n'.join(linhas)


def resumo_cat(tela):
    out = []
    for k in ('VISUAL', 'TEXTO/CONTEÚDO', 'GEOMETRIA', 'FUNCIONAL (autorizada)', 'FUNCIONAL'):
        if cnt[tela][k]:
            out.append(f'| {k} | {cnt[tela][k]} | {len(ctrl_by_cat[tela][k])} |')
    return '| Categoria | Propriedades | Controles |\n|---|---|---|\n' + '\n'.join(out)


val_tab = '| Verificação | Resultado | Detalhe |\n|---|---|---|\n' + '\n'.join(
    f"| {v['verificacao']} | {'OK' if v['ok'] else 'FALHA'} | {(v['detalhe'] or '')[:140].replace('|', '/')} |" for v in val)
tc_tab = '| Grupo | Verificação | Resultado |\n|---|---|---|\n' + '\n'.join(
    f"| {t['tc']} | {t['descricao'].replace('|', '/')} | {'OK' if t['ok'] else 'FALHA'} |" for t in tcs)
pac_tab = '\n'.join(f"- {p['etapa']}: **{'OK' if p['ok'] else 'FALHA'}** — {p['detalhe']}" for p in pac)

rel = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'relatorio_modelo.md'), encoding='utf-8').read()
rel = rel.format(
    n_alt=len(log['alteracoes']), n_criados=len(log['criados']), n_ctrl_alt=len(ctrl_alt),
    resumo_ava=resumo_cat('scrAvaliacao'), resumo_his=resumo_cat('scrHistoricoAvaliacoes'),
    nao_aut=len(nao_aut),
    criados='\n'.join(f"| `{x['controle']}` | {x['tela']} | {x['tipo']} | `{x['pai']}` | `{x['modelo']}` |" for x in log['criados']),
    ocultos='\n'.join(f'- `{c}` ({t})' for t, c in ocultos),
    condicionais='\n'.join(f'- `{c}` ({t}): `{v}`' for t, c, v in condicionais) or '- nenhum',
    tab_ava=tabela_props('scrAvaliacao'), tab_his=tabela_props('scrHistoricoAvaliacoes'),
    val_ok=val_ok, val_n=len(val), val_tab=val_tab, tc_ok=tc_ok, tc_n=len(tcs), tc_tab=tc_tab,
    ptbr=ptbr_line, pac_tab=pac_tab,
)
open(os.path.join(OUT, 'RELATORIO_AVALIACAO_CONTEXTO_FINAL.md'), 'w', encoding='utf-8').write(rel)

# ------------------------------------------------------------------ evidências (JSON resumido)
ev = os.path.join(OUT, 'evidencias')
os.makedirs(ev, exist_ok=True)
json.dump(val, open(os.path.join(ev, 'validacao_pacote.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(tcs, open(os.path.join(ev, 'testes_cenarios.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(pac, open(os.path.join(ev, 'pac_cli_pack_unpack.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ manifesto SHA-256
lin = ['SGC LCQ RJ — MANIFESTO SHA-256 DOS ARTEFATOS', 'Gerado em 2026-10-09 (UTC). Algoritmo: SHA-256.', '',
       'ENTRADAS (recebidas):']
for nome, p in (('SGC LCQ RJ (3).msapp', os.path.join(S, 'orig.msapp')), ('SGCLCQRJ_20261009060323.zip', os.path.join(S, 'orig.zip'))):
    lin.append(f'{hashlib.sha256(open(p, "rb").read()).hexdigest()}  {nome}')
lin += ['', 'ENTREGAS:']
for root, _, files in sorted(os.walk(OUT)):
    for fn in sorted(files):
        if fn == 'MANIFESTO_SHA256.txt':
            continue
        p = os.path.join(root, fn)
        lin.append(f'{hashlib.sha256(open(p, "rb").read()).hexdigest()}  {os.path.relpath(p, OUT)}')
lin += ['', 'Conferência: o arquivo *-document.msapp dentro do ZIP importável tem o mesmo SHA-256 do .msapp entregue.']
open(os.path.join(OUT, 'MANIFESTO_SHA256.txt'), 'w', encoding='utf-8').write('\n'.join(lin) + '\n')
print('pt-BR:', ptbr_line, '| não autorizadas:', len(nao_aut), '| validação', val_ok, '/', len(val), '| TCs', tc_ok, '/', len(tcs))
