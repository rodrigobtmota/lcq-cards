"""Dados FICTÍCIOS de teste (modelados na imagem enviada). Não são gravados no app."""
import copy
import json

PESSOAS = [
    {'ID': 1, 'Codigo': 'P001', 'Nome': 'Kathleen Caroline', 'Cargo': 'Analista Júnior', 'Grupo': 'D', 'Perfil': 'JUNIOR', 'Ativa': True, 'Email': 'p001@exemplo.local', 'Claims': '', 'PodeGestao': False, 'PodePessoas': False, 'PodeCatalogo': False, 'PodeExtra': False},
    {'ID': 2, 'Codigo': 'P002', 'Nome': 'Rodrigo Barbosa Tavares da Mota', 'Cargo': 'Analista Pleno', 'Grupo': 'A', 'Perfil': 'PLENO', 'Ativa': True, 'Email': 'p002@exemplo.local', 'Claims': '', 'PodeGestao': True, 'PodePessoas': True, 'PodeCatalogo': False, 'PodeExtra': True},
    {'ID': 3, 'Codigo': 'P003', 'Nome': 'Maria Aparecida dos Santos Albuquerque Figueiredo', 'Cargo': 'Técnica de Laboratório Sênior', 'Grupo': 'B', 'Perfil': 'SENIOR', 'Ativa': True, 'Email': 'p003@exemplo.local', 'Claims': '', 'PodeGestao': False, 'PodePessoas': False, 'PodeCatalogo': False, 'PodeExtra': False},
    {'ID': 4, 'Codigo': 'P004', 'Nome': 'João Pedro Lima', 'Cargo': 'Técnico de Laboratório', 'Grupo': 'C', 'Perfil': 'PLENO', 'Ativa': True, 'Email': 'p004@exemplo.local', 'Claims': '', 'PodeGestao': False, 'PodePessoas': False, 'PodeCatalogo': False, 'PodeExtra': False},
    {'ID': 5, 'Codigo': 'P005', 'Nome': 'Ana Beatriz Moreira', 'Cargo': 'Analista Sênior', 'Grupo': 'E', 'Perfil': 'SENIOR', 'Ativa': True, 'Email': 'p005@exemplo.local', 'Claims': '', 'PodeGestao': False, 'PodePessoas': False, 'PodeCatalogo': False, 'PodeExtra': False},
]
USUARIO = PESSOAS[1]

DOCS = [
    {'codigo': 'BRK-INS-01-011939-PT', 'versao': '21.0', 'titulo': 'Especificação e classificação de produto final', 'areas': 'PE9', 'publicacao': '2025-04-10', 'expiracao': '2031-04-10', 'status': 'Vigente'},
    {'codigo': 'BRK-INS-01-011947-PT', 'versao': '4.5', 'titulo': 'Classificação, codificação e liberação de lotes', 'areas': 'PE9', 'publicacao': '2024-11-28', 'expiracao': '2030-11-28', 'status': 'Vigente'},
]
METODO = 'Discussão técnica estruturada e revisão de registros/resultados de suporte para classificação, codificação e liberação de lotes.'
FONTES = 'BRK-INS-01-011939-PT 4/5.1/5.4 · BRK-INS-01-011947-PT 4/5.2/5.5'
CRITERIOS = [
    ('C01', 'preparacao_execucao', 'Identifica corretamente produto, lote, área e conjunto de requisitos/especificações aplicáveis antes da classificação.', False),
    ('C02', 'equipamentos_materiais_controles', 'Confere a disponibilidade e integridade dos resultados, registros e informações necessárias à decisão de classificação/liberação.', False),
    ('C03', 'pontos_criticos_validade_anomalias', 'Reconhece resultados fora de especificação, pendências analíticas e condições que impedem a liberação, tratando-as conforme o procedimento.', True),
    ('C04', 'resultado_interpretacao', 'Interpreta os resultados frente à especificação e atribui a classificação correta ao lote.', False),
    ('C05', 'registros_rastreabilidade', 'Registra a decisão de classificação, codificação e liberação com rastreabilidade completa no sistema.', False),
    ('C06', 'seguranca', 'Segue as orientações de segurança aplicáveis durante a consulta e o manuseio de registros e amostras.', True),
]


def crit_json(respostas=None, comentarios=None, n=6):
    respostas = respostas or {}
    comentarios = comentarios or {}
    out = []
    for cid, dim, desc, na in CRITERIOS[:n]:
        out.append({'criterioId': cid, 'dimensao': dim, 'descricao': desc, 'evidenciaEsperada': 'Registro conferido.',
                    'permiteNA': na, 'condicaoNA': 'quando não houver amostra física no turno' if na else '',
                    'areas': 'PE9,PP5,Q4', 'fontes': FONTES, 'modo': 'discussao',
                    'resposta': respostas.get(cid, ''), 'comentario': comentarios.get(cid, '')})
    return out


def avaliacao(uid='AV-0001', pessoa=PESSOAS[0], estado='PREENCHIMENTO', resultado='', modulo='M14.1',
              modulo_nome='Classificação e liberação de lotes', tipo='QUALIFICACAO', docs=None, metodo=METODO,
              respostas=None, comentarios=None, parecer='', obs='', inicio='2026-10-07T09:00:00', conclusao=None,
              avaliador=USUARIO, area='PE9', tentativa=1, snaps=True, n_crit=6):
    docs = DOCS if docs is None else docs
    snap = {'pessoaNome': pessoa['Nome'], 'cargo': pessoa['Cargo'], 'grupo': pessoa['Grupo'], 'perfil': pessoa['Perfil'],
            'metodo': metodo, 'versao': 'R4-LIBERADO-OPERACIONAL-2026.10', 'criterios': crit_json(respostas, comentarios, n_crit)}
    if not snaps:
        snap.pop('pessoaNome'); snap.pop('cargo'); snap.pop('grupo')
    return {
        'ID': int(''.join(ch for ch in uid if ch.isdigit()) or 1), 'Uid': uid, 'Ciclo': 'CIC-7f3a2c19-5d0e-4b8a-9c41-2e6f1a0b9d77',
        'Pessoa': pessoa['Codigo'], 'Area': area, 'Tipo': tipo, 'TipoRotulo': tipo.title(), 'Modulo': modulo, 'ModuloNome': modulo_nome,
        'Tentativa': tentativa, 'Estado': estado, 'Resultado': resultado, 'Avaliador': avaliador['Codigo'], 'AvaliadorNome': avaliador['Nome'],
        'Inicio': inicio, 'Conclusao': conclusao, 'CriteriosJson': json.dumps(snap, ensure_ascii=False),
        'DocumentosJson': json.dumps({'documentos': docs}, ensure_ascii=False), 'Parecer': parecer, 'Observacoes': obs,
        'PessoaNomeSnap': snap.get('pessoaNome', ''), 'CargoSnap': snap.get('cargo', ''), 'GrupoSnap': snap.get('grupo', ''),
        'PerfilSnap': snap['perfil'], 'MetodoSnap': metodo, 'VersaoSnap': snap['versao'],
    }


BASE_GLOBALS = {
    'varUsuario': USUARIO, 'varAtivoSGC': True, 'varCarregado': True, 'varPodeGestao': True, 'varPodePessoas': True,
    'colPessoas': PESSOAS, 'locAjuda': False, 'locModalCanc': False, 'locProcAva': False,
    'SGCIdentidadeLateral': 'asset:sgc-identidade-lateral.png', 'FaixaCabecalhoLCQ': 'asset:a0ae92ce-e660-538d-ac0a-9a967a99c149.png',
    'varHistoricoPossivelmenteIncompleto': False,
}
DATE_FIELDS = ['Inicio', 'Conclusao', 'Data']


def scen_avaliacao(av, w=1366, h=768, parecer_txt=None, probes=None, extra_avs=()):
    g = copy.deepcopy(BASE_GLOBALS)
    g['colAvaliacoes'] = [av] + list(extra_avs)
    g['varAvalUid'] = av['Uid']
    sc = {'screenW': w, 'screenH': h, 'dateFields': DATE_FIELDS, 'globals': g,
          'derive': [{'name': 'locAv', 'expr': 'LookUp(colAvaliacoes, Uid = varAvalUid)'},
                     {'name': 'colCritAva', 'fromOnVisible': 'colCritAva'},
                     {'name': 'colDocsAva', 'fromOnVisible': 'colDocsAva'}],
          'inputs': {}, 'probes': probes or []}
    if parecer_txt is not None:
        sc['inputs']['txtParecerAva'] = parecer_txt
    return sc


def scen_historico(avs, w=1366, h=768, evento='', filtros=None, inputs=None, tec=False, probes=None, gestao=True):
    g = copy.deepcopy(BASE_GLOBALS)
    g.update({'colAvaliacoes': avs, 'locEvento': evento, 'locAbaEv': 1, 'locEvTec': tec, 'locFArea': '', 'locFTipo': '',
              'locFEst': '', 'locFRes': '', 'locPaginaHis': 1, 'varPodeGestao': gestao})
    g.update(filtros or {})
    return {'screenW': w, 'screenH': h, 'dateFields': DATE_FIELDS, 'globals': g, 'inputs': inputs or {}, 'probes': probes or []}


def historico_dataset():
    P = {p['Codigo']: p for p in PESSOAS}
    at = {c[0]: 'Atendeu' for c in CRITERIOS}
    com = {c[0]: 'Evidência conferida no registro do lote.' for c in CRITERIOS}
    rows = [
        avaliacao('AV-0016', P['P001'], 'PREENCHIMENTO', '', inicio='2026-10-07T09:00:00', respostas={'C01': 'Atendeu', 'C02': 'Atendeu'}, comentarios={'C01': 'Conferido lote 26-118.'}),
        avaliacao('AV-0015', P['P003'], 'CONCLUIDA', 'ATENDEU', modulo='M09.2', modulo_nome='CROMATOGRAFIA GASOSA PARA DETERMINAÇÃO DE VOLÁTEIS RESIDUAIS EM POLIETILENO',
                  inicio='2026-10-01T08:00:00', conclusao='2026-10-06T16:30:00', respostas=at, comentarios=com,
                  parecer='Domínio técnico adequado; executou a análise e interpretou os resultados corretamente.', avaliador=P['P005']),
        avaliacao('AV-0014', P['P004'], 'CONCLUIDA', 'NAO_ATENDEU', modulo='M03.1', modulo_nome='Densidade e índice de fluidez', area='PP5',
                  inicio='2026-09-28T08:00:00', conclusao='2026-10-02T10:00:00', respostas={**at, 'C04': 'Não atendeu'}, comentarios={**com, 'C04': 'Classificou o lote fora da faixa especificada.'},
                  parecer='Necessita reforço na interpretação de resultados frente à especificação.', tentativa=2),
        avaliacao('AV-0013', P['P005'], 'CANCELADA', '', modulo='M07.4', modulo_nome='Umidade por Karl Fischer', area='Q4', tipo='REQUALIFICACAO',
                  inicio='2026-09-20T08:00:00', conclusao='2026-09-22T09:15:00', obs='Avaliação aberta para o módulo incorreto; será reaberta no ciclo correto.'),
        avaliacao('AV-0012', P['P001'], 'CONCLUIDA', 'ATENDEU', modulo='M14.1', inicio='2026-09-10T08:00:00', conclusao='2026-09-12T11:00:00',
                  respostas=at, comentarios=com, parecer='Atende plenamente aos critérios do módulo.', tipo='EXTRAORDINARIA', snaps=False),
    ]
    extra = [('P002', 'PE9', 'QUALIFICACAO'), ('P004', 'PP5', 'REQUALIFICACAO'), ('P005', 'Q4', 'QUALIFICACAO'), ('P001', 'PP5', 'QUALIFICACAO')]
    for i in range(11):
        pc, ar, tp = extra[i % 4]
        rows.append(avaliacao(f'AV-{11 - i:04d}', P[pc], 'CONCLUIDA', 'ATENDEU', modulo=f'M0{i % 9 + 1}.1', modulo_nome='Preparo e padronização de soluções',
                              area=ar, tipo=tp, inicio=f'2026-08-{20 - i:02d}T08:00:00', conclusao=f'2026-08-{21 - i:02d}T15:00:00',
                              respostas=at, comentarios=com, parecer='Atende aos critérios.', avaliador=P['P002'] if i % 2 else P['P005']))
    return rows
