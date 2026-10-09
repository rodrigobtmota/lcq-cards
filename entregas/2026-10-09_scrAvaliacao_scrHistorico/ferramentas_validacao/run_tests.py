"""Executa os cenários de teste nas fórmulas reais (simulador Power Fx) e gera as imagens.
Uso: python3 -I run_tests.py <scratchpad>
"""
import copy
import html as H
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures as F  # noqa: E402
import render as R  # noqa: E402

S = sys.argv[1]
SIM = os.path.join(S, 'sim')
IMG = os.path.join(S, 'out', 'imagens')
os.makedirs(SIM, exist_ok=True)
os.makedirs(IMG, exist_ok=True)
ASSETS = os.path.join(S, 'src_msapp', 'Assets', 'Images')
CTRL = {('new', 'ava'): f'{S}/work/Controls/563.json', ('old', 'ava'): f'{S}/src_msapp/Controls/563.json',
        ('new', 'his'): f'{S}/work/Controls/678.json', ('old', 'his'): f'{S}/src_msapp/Controls/678.json'}
jobs, results, runs = [], [], {}


def sim(tag, ver, tela, scen, png=None):
    p = f'{SIM}/{tag}.json'
    json.dump(scen, open(p, 'w'), ensure_ascii=False)
    r = subprocess.run(['dotnet', f'{S}/tools/screensim/out/screensim.dll', CTRL[(ver, tela)], p, f'{SIM}/{tag}.out.json'],
                       capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stdout + r.stderr)
    out = json.load(open(f'{SIM}/{tag}.out.json'))
    out['warnings'] = [w for w in out['warnings'] if not w.startswith(('scrAvaliacao.Size', 'scrHistoricoAvaliacoes.Size'))]
    hp = f'{SIM}/{tag}.html'
    open(hp, 'w').write(R.page(out['tree'], ASSETS, tag))
    jobs.append({'id': tag, 'html': hp, 'png': png, 'w': scen['screenW'], 'h': scen['screenH']})
    runs[tag] = out
    return out


def nodes(tree, name, acc=None):
    acc = [] if acc is None else acc
    if tree.get('name') == name:
        acc.append(tree)
    for c in tree.get('children') or []:
        nodes(c, name, acc)
    for it in tree.get('items') or []:
        for c in it['children']:
            nodes(c, name, acc)
    return acc


def one(tree, name):
    n = nodes(tree, name)
    return n[0] if n else {}


def txt(h):
    h = re.sub(r'<br\s*/?>', ' ', h or '')
    return H.unescape(re.sub(r'<[^>]+>', '', h)).strip()


def expect(tc, desc, ok, detail=''):
    results.append({'tc': tc, 'descricao': desc, 'ok': bool(ok), 'detalhe': detail})


def paren_arg(src, start_token):
    i = src.index(start_token) + len(start_token)
    depth, k, st = 1, i, False
    while k < len(src):
        ch = src[k]
        if ch == '"':
            st = not st
        elif not st and ch == '(':
            depth += 1
        elif not st and ch == ')':
            depth -= 1
            if depth == 0:
                return src[i:k]
        k += 1
    raise ValueError(start_token)


def rule(ctrl_file, name, prop):
    d = json.load(open(ctrl_file, encoding='utf-8'))

    def f(c):
        if c['Name'] == name:
            return next(r['InvariantScript'] for r in c['Rules'] if r['Property'] == prop)
        for ch in c.get('Children', []):
            v = f(ch)
            if v:
                return v
    return f(d['TopParent'])


# ============================================================== scrAvaliacao
salvar = rule(CTRL[('new', 'ava')], 'btnSalvarAva', 'OnSelect')
k = salvar.index('With({_comentPend')
NOTIFY = 'With(' + paren_arg(salvar[k:], 'With(') + ')'
PROBES = [{'name': 'concluir', 'control': 'btnConcluirAva', 'prop': 'DisplayMode'},
          {'name': 'salvar_dm', 'control': 'btnSalvarAva', 'prop': 'DisplayMode'},
          {'name': 'resumo', 'control': 'lblResumoAva', 'prop': 'HtmlText'},
          {'name': 'notify', 'expr': NOTIFY}]
AT = {c[0]: 'Atendeu' for c in F.CRITERIOS}
COM = {c[0]: 'Evidência conferida no registro do lote.' for c in F.CRITERIOS}
P30 = 'Domínio técnico adequado na classificação e liberação.'


def ava(tag, av, parecer, w=1366, h=768, png=None, ver='new'):
    return sim(tag, ver, 'ava', F.scen_avaliacao(av, w, h, parecer_txt=parecer, probes=PROBES), png)


def pend(out):
    return txt(out['probes']['resumo']).split('Atendeu')[-1].strip() if 'Atendeu' in txt(out['probes']['resumo']) else txt(out['probes']['resumo'])


def geom_checks(tc, out, W, Hh):
    t = out['tree']
    ci, cc, cp, cb = one(t, 'conIdAva'), one(t, 'conCritAva'), one(t, 'conParAva'), one(t, 'conBarraAva')
    vis = [n for n in (t.get('children') or []) if n.get('visible')]
    expect(tc, f'{W}×{Hh}: nenhum controle visível ultrapassa a largura da tela',
           all(n.get('X', 0) + n.get('Width', 0) <= W + 0.5 for n in vis))
    expect(tc, f'{W}×{Hh}: card Contexto termina antes dos Critérios', ci['Y'] + ci['Height'] < cc['Y'],
           f"Contexto {ci['Y']:.0f}–{ci['Y'] + ci['Height']:.0f}, Critérios Y={cc['Y']:.0f}")
    expect(tc, f'{W}×{Hh}: Critérios e Parecer lado a lado sem sobreposição', cc['X'] + cc['Width'] <= cp['X'],
           f"Critérios {cc['Width'] / (cc['Width'] + cp['Width'] + 16):.0%} da largura útil")
    if cb.get('visible'):
        expect(tc, f'{W}×{Hh}: barra inferior dentro da tela e abaixo do Parecer',
               cb['Y'] + cb['Height'] <= Hh and cp['Y'] + cp['Height'] <= cb['Y'])
    expect(tc, f'{W}×{Hh}: Parecer com altura útil ≥ 170 px', cp['Height'] >= 170, f"{cp['Height']:.0f} px")
    g = one(t, 'galCritAva')
    vis_c = g['Height'] / g['TemplateHeight']
    expect(tc, f'{W}×{Hh}: ao menos 1 critério inteiro visível na lista', vis_c >= 1.0, f'{vis_c:.2f} critérios visíveis')


# base (TC-A08 = estado da imagem de referência: 6 de 6 Atendeu, parecer com 2 caracteres)
base = F.avaliacao(respostas=AT, parecer='ok')
o = ava('A08_1366', base, 'ok', png=f'{IMG}/scrAvaliacao_depois_1366x768.png')
ava('A08_1920', base, 'ok', 1920, 1080, png=f'{IMG}/scrAvaliacao_depois_1920x1080.png')
ava('A08_old_1366', base, 'ok', png=f'{IMG}/scrAvaliacao_antes_1366x768.png', ver='old')
ava('A08_old_1920', base, 'ok', 1920, 1080, png=f'{IMG}/scrAvaliacao_antes_1920x1080.png', ver='old')
expect('TC-A08', 'Concluir desabilitado', o['probes']['concluir'] == 'DisplayMode.Disabled', o['probes']['concluir'])
expect('TC-A08', 'Mensagem "Parecer técnico pendente · 2 de 30 caracteres"', 'Parecer técnico pendente · 2 de 30 caracteres' in txt(o['probes']['resumo']), txt(o['probes']['resumo']))
geom_checks('TC-A08', o, 1366, 768)
geom_checks('TC-A08', runs['A08_1920'], 1920, 1080)
t = o['tree']
ctx_txt = ' '.join(txt(n.get('HtmlText')) for n in nodes(t, 'conIdAva')[0]['children'] if n.get('visible'))
expect('Layout', 'Contexto não exibe CICLO / Tentativa / GUID / Módulo 14.1',
       not any(k in ctx_txt for k in ('CICLO', 'Tentativa', 'CIC-', 'Módulo 14.1')), ctx_txt[:160])
expect('Layout', 'Contexto mostra Pessoa, Área, Módulo, Tipo, Avaliador e Estado',
       all(k in ctx_txt for k in ('Kathleen Caroline', 'PE9', 'Classificação e liberação de lotes', 'Qualificação', 'Rodrigo Barbosa Tavares da Mota', 'Em preenchimento')))
expect('Layout', 'Tentativa disponível só como tooltip do selo de estado', one(t, 'bdgIdEstAva').get('Tooltip') == 'Tentativa 1')
doc_txt = txt(one(t, 'lblDocTitAva').get('HtmlText')) + ' | ' + txt(one(t, 'lblDocAuxAva').get('HtmlText'))
expect('Layout', 'Base documental no topo com subtítulo e contagem', 'Base documental' in doc_txt and '2 documentos aplicáveis' in doc_txt, doc_txt)
expect('Layout', 'Método no topo sem versão interna do catálogo',
       'R4-' not in ' '.join(txt(n.get('HtmlText')) for n in nodes(t, 'conMetAva')[0]['children'] if n.get('visible')))
d1 = [txt(n.get('HtmlText')) for n in nodes(t, 'lblDocSubAva')]
expect('TC-A03', '2 documentos: versão e validade convertidas sem fuso (texto)', d1 == ['Versão 21.0 · validade 10/04/2031', 'Versão 4.5 · validade 28/11/2030'], str(d1))
gd = one(t, 'galDocAva')
expect('TC-A03', '2 documentos cabem sem rolagem', gd['TemplateHeight'] <= gd['Height'], f"linha {gd['TemplateHeight']} / área {gd['Height']}")
card = nodes(t, 'htmlCardCritAva')[0].get('HtmlText', '')
expect('Layout', 'Card de critério com borda neutra #E1E8F0 (só barra lateral semântica)', 'border:1px solid #E1E8F0' in card)
expect('Layout', 'lblCritEvAva continua invisível', all(not n.get('visible') for n in nodes(t, 'lblCritEvAva')))

# TC-A01 pessoa com nome longo
av = F.avaliacao(pessoa=F.PESSOAS[2], respostas=AT)
o = ava('A01', av, 'ok', png=f'{SIM}/A01.png')
v0 = one(o['tree'], 'lblIdV0Ava')
expect('TC-A01', 'Nome longo: 1 linha com reticências + tooltip com nome completo', v0.get('Tooltip') == F.PESSOAS[2]['Nome'], v0.get('Tooltip'))
# TC-A02 módulo longo
av = F.avaliacao(modulo_nome='Classificação, codificação, liberação e reclassificação de lotes de produto final em tancagem e expedição', respostas=AT)
o = ava('A02', av, 'ok', png=f'{SIM}/A02.png')
v2 = one(o['tree'], 'lblIdV2Ava')
expect('TC-A02', 'Módulo longo: até 2 linhas + tooltip completo; sem "Módulo 14.1"', v2['Height'] == 36 and 'tancagem' in (v2.get('Tooltip') or '') and not one(o['tree'], 'lblIdS2Ava').get('visible'))
# TC-A04 4 e 5 documentos
d4 = F.DOCS + [dict(F.DOCS[0], codigo='BRK-INS-01-012001-PT', titulo='Amostragem de produto acabado'), dict(F.DOCS[1], codigo='BRK-INS-01-012002-PT', titulo='Registro de liberação')]
o = ava('A04', F.avaliacao(docs=d4, respostas=AT), 'ok', png=f'{SIM}/A04.png')
gd = one(o['tree'], 'galDocAva')
expect('TC-A04', '4 documentos: 2 colunas × 2 linhas, sem rolagem', gd['count'] == 4 and 2 * gd['TemplateHeight'] <= gd['Height'], f"{gd['count']} docs; área {gd['Height']}")
d5 = d4 + [dict(F.DOCS[0], codigo='BRK-INS-01-012003-PT', titulo='Rastreabilidade de lotes')]
o = ava('A04b', F.avaliacao(docs=d5, respostas=AT), 'ok', png=f'{SIM}/A04b.png')
gd, ci = one(o['tree'], 'galDocAva'), one(o['tree'], 'conIdAva')
expect('TC-A04', '5+ documentos: altura limitada a 2 linhas e rolagem vertical discreta na galeria', 2 * gd['TemplateHeight'] <= gd['Height'] < 3 * gd['TemplateHeight'],
       f"card Contexto {ci['Height']:.0f} px")
# TC-A05 título longo
dl = [dict(F.DOCS[0], titulo='Especificação, classificação e critérios de aceitação de produto final para polietileno de alta densidade grau injeção'), F.DOCS[1]]
o = ava('A05', F.avaliacao(docs=dl, respostas=AT), 'ok', png=f'{SIM}/A05.png')
gd = one(o['tree'], 'galDocAva')
expect('TC-A05', 'Título longo: linha do documento cresce para 2 linhas de título', gd['TemplateHeight'] == 82, f"TemplateHeight {gd['TemplateHeight']}")
# TC-A06 sem Expiracao / sem versão / sem título
ds = [dict(F.DOCS[0], expiracao=''), dict(F.DOCS[1], versao='', titulo='')]
o = ava('A06', F.avaliacao(docs=ds, respostas=AT), 'ok', png=f'{SIM}/A06.png')
subs = [txt(n.get('HtmlText')) for n in nodes(o['tree'], 'lblDocSubAva')]
heads = [txt(n.get('HtmlText')) for n in nodes(o['tree'], 'lblDocAva')]
expect('TC-A06', 'Sem Expiracao → só "Versão 21.0"; sem versão → só "Validade …"; sem título → só código',
       subs == ['Versão 21.0', 'Validade 28/11/2030'] and heads[1] == 'BRK-INS-01-011947-PT', f'{subs} {heads}')
# TC-A07 método longo
ml = F.METODO + ' ' + ('Inclui verificação cruzada entre os registros do sistema de gestão laboratorial, os certificados emitidos e a rastreabilidade dos lotes expedidos no período, com discussão dos desvios recentes. ' * 3)
o = ava('A07', F.avaliacao(metodo=ml, respostas=AT), 'ok', png=f'{SIM}/A07.png')
cm = one(o['tree'], 'conMetAva')
expect('TC-A07', 'Método longo: altura limitada a 6 linhas (texto rola dentro do bloco)', cm['Height'] <= 34 + 19 * 6 + 8, f"{cm['Height']:.0f} px")
# TC-A09 parecer ≥ 30 e critérios válidos
o = ava('A09', F.avaliacao(respostas=AT), P30)
expect('TC-A09', 'Concluir habilitado', o['probes']['concluir'] == 'DisplayMode.Edit', o['probes']['concluir'])
expect('TC-A09', 'Mensagem apenas informativa (comentários de Atendeu são opcionais)', '6 comentários pendentes' in txt(o['probes']['resumo']), txt(o['probes']['resumo']))
o = ava('A09b', F.avaliacao(respostas=AT, comentarios=COM), P30)
expect('TC-A09', 'Tudo preenchido → "Pronto para concluir"', 'Pronto para concluir' in txt(o['probes']['resumo']) and o['probes']['concluir'] == 'DisplayMode.Edit')
# TC-A10 Não atendeu sem comentário
o = ava('A10', F.avaliacao(respostas={**AT, 'C04': 'Não atendeu'}), P30)
expect('TC-A10', 'Concluir bloqueado + "Há 1 critério Não atendeu aguardando comentário"',
       o['probes']['concluir'] == 'DisplayMode.Disabled' and 'Há 1 critério Não atendeu aguardando comentário' in txt(o['probes']['resumo']), txt(o['probes']['resumo']))
# TC-A11 N/A sem justificativa
o = ava('A11', F.avaliacao(respostas={**AT, 'C03': 'N/A'}), P30)
expect('TC-A11', 'Concluir bloqueado + "Há 1 critério N/A sem justificativa"',
       o['probes']['concluir'] == 'DisplayMode.Disabled' and 'Há 1 critério N/A sem justificativa' in txt(o['probes']['resumo']), txt(o['probes']['resumo']))
o = ava('A11b', F.avaliacao(respostas={c[0]: ('N/A' if c[3] else '') for c in F.CRITERIOS}), P30)
expect('Prioridade', 'Critério sem resposta tem prioridade: "Faltam 4 critérios para responder"', 'Faltam 4 critérios para responder' in txt(o['probes']['resumo']), txt(o['probes']['resumo']))
# TC-A12/13 concluída e cancelada
for tc, est, res, extra in (('TC-A12', 'CONCLUIDA', 'ATENDEU', {}), ('TC-A13', 'CANCELADA', '', {'obs': 'Aberta por engano.'})):
    av = F.avaliacao(estado=est, resultado=res, respostas=AT, comentarios=COM, parecer=P30, conclusao='2026-10-08T10:00:00', **extra)
    o = ava(tc, av, None, png=f'{IMG}/scrAvaliacao_{"concluida" if est == "CONCLUIDA" else "cancelada"}_1366x768.png')
    b = txt(one(o['tree'], 'lblBannerAva').get('HtmlText'))
    btns = [n.get('DisplayMode') for n in nodes(o['tree'], 'btnAtAva')]
    expect(tc, 'Somente leitura: banner visível, barra de ações oculta, respostas desabilitadas',
           one(o['tree'], 'lblBannerAva').get('visible') and not one(o['tree'], 'conBarraAva').get('visible') and set(btns) == {'DisplayMode.Disabled'}, b)
    expect(tc, 'Banner sem a palavra "snapshot" e com texto amigável', 'snapshot' not in b.lower() and 'preservados conforme estavam no início da avaliação' in b)
    geom_checks(tc, o, 1366, 768)
# TC-A14..A19 notificação do rascunho (trecho real inserido no btnSalvarAva.OnSelect)
casos = [
    ('TC-A14', {'C01': 'Atendeu'}, {}, 'Rascunho salvo. Aguardando comentário em 1 critério. [NotificationType.Warning]', None),
    ('TC-A15', {'C01': 'Atendeu', 'C02': 'Atendeu', 'C03': 'Atendeu'}, {}, 'Rascunho salvo. Aguardando comentário em 3 critérios. [NotificationType.Warning]', None),
    ('TC-A16', AT, COM, 'Rascunho salvo com sucesso. [NotificationType.Success]', 'DisplayMode.Edit'),
    ('TC-A17', AT, {k: v for k, v in COM.items() if k != 'C01'}, 'Rascunho salvo. Aguardando comentário em 1 critério. [NotificationType.Warning]', 'DisplayMode.Edit'),
    ('TC-A18', {**AT, 'C04': 'Não atendeu'}, {k: v for k, v in COM.items() if k != 'C04'}, 'Rascunho salvo. Aguardando comentário em 1 critério. [NotificationType.Warning]', 'DisplayMode.Disabled'),
    ('TC-A19', {**AT, 'C03': 'N/A'}, {k: v for k, v in COM.items() if k != 'C03'}, 'Rascunho salvo. Aguardando comentário em 1 critério. [NotificationType.Warning]', 'DisplayMode.Disabled'),
]
for tc, resp, com, msg, concl in casos:
    o = ava(tc, F.avaliacao(respostas=resp, comentarios=com), P30)
    expect(tc, f'Salvar habilitado e notificação: {msg.split(" [")[0]}', o['probes']['salvar_dm'] == 'DisplayMode.Edit' and o['probes']['notify'] == msg, o['probes']['notify'])
    if concl:
        expect(tc, f'Concluir: {"habilitado" if concl.endswith("Edit") else "bloqueado pela regra existente"}', o['probes']['concluir'] == concl, txt(o['probes']['resumo']))

# ============================================================== scrHistoricoAvaliacoes
ds = F.historico_dataset()
HP = [{'name': 'cont', 'control': 'htmlExibindoHis', 'prop': 'HtmlText'},
      {'name': 'copia', 'expr': paren_arg(rule(CTRL[('new', 'his')], 'btnCopiarHis', 'OnSelect'), 'Copy(')}]


def his(tag, ver='new', w=1366, h=768, png=None, **kw):
    return sim(tag, ver, 'his', F.scen_historico(ds, w, h, probes=HP, **kw), png)


o = his('H_lista_1366', png=f'{IMG}/scrHistorico_depois_1366x768.png')
his('H_lista_old_1366', 'old', png=f'{IMG}/scrHistorico_antes_1366x768.png')
his('H_lista_1920', w=1920, h=1080, png=f'{IMG}/scrHistorico_depois_1920x1080.png')
his('H_lista_old_1920', 'old', w=1920, h=1080, png=f'{IMG}/scrHistorico_antes_1920x1080.png')
t = o['tree']
expect('Lista', 'Histórico aparece sem filtro (16 registros, 7 na página 1)', '16 registros encontrados' in txt(o['probes']['cont']) and len(one(t, 'galHis')['items']) == 7, txt(o['probes']['cont']))
expect('Lista', 'Subtítulo novo, sem "snapshot"', txt(one(t, 'lblSubtituloHis').get('HtmlText')) == 'Consulte e acompanhe as avaliações técnicas do laboratório.')
expect('Lista', 'Título da tabela "Registros de avaliação"', txt(one(t, 'htmlTabelaTituloHis').get('HtmlText')) == 'Registros de avaliação')
uids = [txt(n.get('HtmlText')) for n in nodes(t, 'lblUidHis')]
expect('Lista', 'UID removido da lista; 2ª linha = cargo · grupo', not any('AV-' in u for u in uids) and uids[0] == 'Analista Júnior · Grupo D', str(uids[:3]))
expect('Lista', 'Código do módulo (M14.1) fora da lista', all(not n.get('visible') for n in nodes(t, 'lblModCodHis')))
expect('Lista', 'Ação "Ver detalhes"', {n.get('Text') for n in nodes(t, 'R3btnAbrirEventoHis')} == {'Ver detalhes'})
rows = one(t, 'galHis')['items']
cell = lambda i, n: txt(next(c for c in rows[i]['children'] if c['name'] == n).get('HtmlText'))
tip = lambda i, n: next(c for c in rows[i]['children'] if c['name'] == n).get('Tooltip')
expect('TC-H01', 'Nome longo: tooltip com nome completo', tip(1, 'lblNomeHis') == F.PESSOAS[2]['Nome'])
expect('TC-H02', 'Módulo longo em caixa alta normalizado com segurança', cell(1, 'lblModHis') == 'Cromatografia Gasosa para Determinação de Voláteis Residuais em Polietileno', cell(1, 'lblModHis'))
expect('TC-H03', 'Avaliador longo em até 2 linhas + tooltip', tip(0, 'lblAvHis') == 'Rodrigo Barbosa Tavares da Mota')
expect('TC-H04', 'Em preenchimento: selo azul + data "Desde 07/10/2026" + tooltip de início',
       cell(0, 'bdgEstHis') == 'Em preenchimento' and cell(0, 'lblDataHis') == 'Desde 07/10/2026' and tip(0, 'lblDataHis') == 'Início da avaliação: 07/10/2026')
expect('TC-H05', 'Concluída / Atendeu + tooltip "Concluída em 06/10/2026"', cell(1, 'bdgEstHis') == 'Concluída' and cell(1, 'bdgResHis') == 'Atendeu' and tip(1, 'lblDataHis') == 'Concluída em 06/10/2026')
expect('TC-H06', 'Concluída / Não atendeu', cell(2, 'bdgResHis') == 'Não atendeu')
expect('TC-H07', 'Cancelada: selo + data de cancelamento', cell(3, 'bdgEstHis') == 'Cancelada' and cell(3, 'lblDataHis') == '22/09/2026' and tip(3, 'lblDataHis') == 'Cancelada em 22/09/2026')
expect('TC-H08', 'Sem resultado exibido como "—" (cinza, não erro)', cell(0, 'bdgResHis') == '—')
o = his('H09', filtros={'locPaginaHis': 3})
expect('TC-H09', 'Página 3 de 16 registros mostra 2 linhas', len(one(o['tree'], 'galHis')['items']) == 2)
o = his('H10', filtros={'locFArea': 'Q4', 'locFEst': 'PREENCHIMENTO'}, png=f'{SIM}/H10.png')
expect('TC-H10', 'Nenhum registro: estado vazio visível e contador "0 registros encontrados"',
       one(o['tree'], 'lblVazioHis').get('visible') and '0 registros encontrados' in txt(o['probes']['cont']), txt(o['probes']['cont']))
for tc, w, h in (('TC-H11', 1366, 768), ('TC-H12', 1920, 1080)):
    o = his(tc, w=w, h=h, evento='AV-0016', png=f'{IMG}/scrHistorico_detalhe_{w}x{h}.png')
    t = o['tree']
    head = ' '.join(txt(one(t, n).get('HtmlText')) for n in ('lblEvTitHis', 'lblEvSubHis', 'lblEvR0His', 'lblEvV0His', 'lblEvBanHis'))
    expect(tc, 'Painel: cabeçalho sem UID/ciclo e com pessoa, módulo·área, chips e "Avaliação em andamento"',
           'AV-' not in head and 'CIC-' not in head and all(k in head for k in ('Detalhes da avaliação', 'Kathleen Caroline', 'Analista Júnior · Grupo D', 'Classificação e liberação de lotes · PE9', 'Qualificação', 'Em preenchimento', 'Avaliação em andamento')), head[:200])
    resumo = ' '.join(txt(one(t, f'lblEvV{i}His').get('HtmlText')) for i in range(1, 6))
    expect(tc, 'Resumo: avaliador, início, conclusão, resultado, tentativa', resumo == 'Rodrigo Barbosa Tavares da Mota 07/10/2026 Em aberto Em andamento 1', resumo)
    dtx = txt(one(t, 'lblEvDocHis').get('HtmlText'))
    expect(tc, 'Documentos preservados na avaliação com versão e validade', 'BRK-INS-01-011939-PT' in dtx and 'Versão 21.0 · validade 10/04/2031' in dtx)
    expect(tc, 'Informações técnicas recolhidas por padrão', not one(t, 'lblEvTecHis').get('visible') and not one(t, 'lblEvV7His').get('visible'))
    pnl = one(t, 'conEvHis')
    expect(tc, 'Painel lateral dentro da tela', pnl['X'] >= 0 and pnl['X'] + pnl['Width'] <= w)
o = his('H_tec', evento='AV-0016', tec=True, png=f'{IMG}/scrHistorico_detalhe_info_tecnica_1366x768.png')
tt = txt(one(o['tree'], 'lblEvTecHis').get('HtmlText'))
expect('Painel', 'Informações técnicas (expandido): UID, ciclo, tentativa, versão', all(k in tt for k in ('AV-0016', 'CIC-', 'Tentativa: 1', 'R4-LIBERADO')), tt)
o = his('H_canc', evento='AV-0013', png=f'{SIM}/H_canc.png')
t = o['tree']
expect('Painel', 'Cancelada: "Avaliação cancelada" + "Justificativa do cancelamento" com o texto registrado',
       'Avaliação cancelada' in txt(one(t, 'lblEvBanHis').get('HtmlText')) and 'Justificativa do cancelamento' in txt(one(t, 'lblEvObsRotHis').get('HtmlText'))
       and 'módulo incorreto' in txt(one(t, 'lblEvObsHis').get('HtmlText')))
expect('Painel', 'Parecer vazio → "Não informado."', txt(one(t, 'lblEvParHis').get('HtmlText')) == 'Não informado.')
o = his('H_fallback', evento='AV-0012', png=f'{SIM}/H_fallback.png')
expect('Painel', 'Sem dados preservados da pessoa → aviso discreto de histórico incompleto',
       'não estavam disponíveis no histórico original' in txt(one(o['tree'], 'lblEvBanHis').get('HtmlText')))
o = his('H_concl', evento='AV-0014', png=f'{SIM}/H_concl.png')
ct = [txt(n.get('HtmlText')) for n in nodes(o['tree'], 'lblEvCIdHis')]
expect('Painel', 'Critérios com título amigável (sem código em destaque) e referência técnica',
       ct[0] == 'Preparação e execução' and 'Referência técnica' in txt(nodes(o['tree'], 'lblEvCComHis')[0].get('HtmlText')), str(ct[:2]))
expect('Painel', 'Concluída: "Avaliação concluída" e resultado "Não atendeu"',
       'Avaliação concluída' in txt(one(o['tree'], 'lblEvBanHis').get('HtmlText')) and txt(one(o['tree'], 'lblEvV4His').get('HtmlText')) == 'Não atendeu')

# filtros (fórmula galHis.Items inalterada) — esperado calculado de forma independente


def esperado(f=lambda a: True, gestao=True):
    vis = [a for a in ds if gestao or a['Pessoa'] == 'P002' or a['Avaliador'] == 'P002']
    return sum(1 for a in vis if f(a))


nome = {p['Codigo']: p['Nome'] for p in F.PESSOAS}
filtros = [
    ('Pessoa ("kathleen")', {}, {'txtBuscaHis': 'kathleen'}, lambda a: 'kathleen' in nome[a['Pessoa']].lower()),
    ('Módulo ("m14")', {}, {'txtModHis': 'm14'}, lambda a: 'm14' in a['Modulo'].lower()),
    ('Área PP5', {'locFArea': 'PP5'}, {}, lambda a: a['Area'] == 'PP5'),
    ('Tipo Requalificação', {'locFTipo': 'REQUALIFICACAO'}, {}, lambda a: a['Tipo'] == 'REQUALIFICACAO'),
    ('Estado Cancelada', {'locFEst': 'CANCELADA'}, {}, lambda a: a['Estado'] == 'CANCELADA'),
    ('Resultado Não atendeu', {'locFRes': 'NAO_ATENDEU'}, {}, lambda a: a['Resultado'] == 'NAO_ATENDEU'),
    ('Sem resultado', {'locFRes': 'SEM'}, {}, lambda a: not a['Resultado']),
    ('Período a partir de 01/10/2026', {}, {'txtDeHis': '01/10/2026'}, lambda a: (a['Conclusao'] or a['Inicio']) >= '2026-10-01'),
]
for i, (nm, fl, inp, fn) in enumerate(filtros):
    o = his(f'F{i}', filtros=fl, inputs=inp)
    exp = esperado(fn)
    expect('Funcional', f'Filtro {nm}: {exp} registros', f'{exp} registro' in txt(o['probes']['cont']), txt(o['probes']['cont']))
o = his('F_perm', gestao=False)
exp = esperado(gestao=False)
expect('Funcional', f'Permissão sem gestão: só avaliado/avaliador ({exp})', f'{exp} registros' in txt(o['probes']['cont']), txt(o['probes']['cont']))
o = his('F_copia', filtros={'locFArea': 'PE9'})
lin = o['probes']['copia'].split('\n')
expect('Funcional', 'Copiar para Excel: todos os filtrados (inclusive outras páginas) + UID mantido', len(lin) - 1 == esperado(lambda a: a['Area'] == 'PE9') and lin[1].startswith('AV-'), f'{len(lin) - 1} linhas')

# ============================================================== imagens + medições de corte
json.dump(jobs, open(f'{SIM}/jobs_all.json', 'w'))
subprocess.run(['node', f'{S}/tools/render/shot.js', f'{SIM}/jobs_all.json'], cwd=f'{S}/tools/render', check=True)
meas = json.load(open(f'{SIM}/jobs_all.json.out.json'))
for tag in ('A08_1366', 'A08_1920', 'H_lista_1366', 'H_lista_1920', 'TC-H11', 'TC-H12'):
    expect('Responsivo', f'{tag}: sem rolagem horizontal', not meas[tag]['hscroll'])
crit = {'A08_1366': ['lblCritDescAva', 'lblIdV0Ava', 'lblIdV1Ava', 'lblIdV2Ava', 'lblIdV3Ava', 'lblIdV4Ava', 'lblDocAva', 'lblDocSubAva', 'lblCritIdAva', 'btnConcluirAva', 'lblResumoAva'],
        'A08_1920': ['lblCritDescAva', 'lblIdV0Ava', 'lblIdV2Ava', 'lblIdV4Ava', 'lblDocAva', 'lblCritIdAva'],
        'A07': ['lblCritDescAva'],
        'TC-H11': ['lblEvR3His', 'lblEvV1His', 'lblEvDocHis', 'lblEvBanHis']}
for tag, names in crit.items():
    cut = sorted({x['name'] for x in meas[tag]['truncated'] if x['name'] in names})
    expect('Responsivo', f'{tag}: textos principais sem corte ({", ".join(names[:4])}…)', not cut, ', '.join(cut))
warn = {k: v['warnings'] for k, v in runs.items() if v['warnings']}
expect('Simulador', 'Nenhum erro de avaliação Power Fx nas telas (todas as fórmulas executadas)', not warn, json.dumps(warn, ensure_ascii=False)[:600])
json.dump({'resultados': results, 'medicoes': meas}, open(f'{S}/tc_results.json', 'w'), ensure_ascii=False, indent=1)
ok = sum(r['ok'] for r in results)
for r in results:
    print(('OK   ' if r['ok'] else 'FALHA') + f" | {r['tc']} | {r['descricao']}" + ('' if r['ok'] else f" | {r['detalhe']}"))
print(f'\n{ok}/{len(results)} verificações OK')
