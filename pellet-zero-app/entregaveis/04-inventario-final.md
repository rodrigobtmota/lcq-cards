# Entregável 5 — Inventário Final

## Telas (23)

| Tela | Função |
|---|---|
| TelaInicio | Seleção de sala/turno, validação de rodízio/ciclo, criação do registro de checklist, menu (NCs, Relatórios, Indicadores, Auditoria) |
| TelaOrganizacao | Checklist FQ1/FQ2/FQ3/FQ4, Cromatografia 1/2, Processamento de Resinas (etapa Organização/Segurança) |
| TelaPellet | Etapa Pellet Zero (FQ3, FQ4, Processamento de Resinas, Reserva Técnica) |
| TelaReservaTecnica, TelaOficinaAOL, TelaAlmoxarifado, TelaLavagem, TelaShelter, TelaDeposito | Checklists específicos por sala |
| TelaNCOrganizacao, TelaNCPellet, TelaNCReservaTecnica, TelaNCOficinaAOL, TelaNCAlmoxarifado, TelaNCLavagem, TelaNCShelter, TelaNCDeposito, TelaNCUsuario* | Registro das NCs por sala (descrição + classificação pela matriz); *TelaNCUsuario = consulta e tratativa/encerramento |
| TelaFinal | Consolidação e encerramento do checklist |
| scrIndicadoresPrograma | Indicadores oficiais (corrigida/completada) |
| scrRelatorioFiltroFlex | Histórico de inspeções + geração de PDF (corrigida) |
| TelaNovaAuditoria | Conclusão de auditorias programadas (corrigida) |

## Listas SharePoint (site https://braskemsa.sharepoint.com/teams/LCQDCX)

| Lista | Uso |
|---|---|
| Checklist_OrganizacaoPellet2025 | Registro oficial dos checklists (respostas Choice por item, Sala, Turno, Ciclo, StatusGeral, StatusNC, TipoVerificacao, ResponsavelInspecao) |
| NaoConformidadesPorSala | NCs (SalaNC, StatusNC, StatusAtribuicaoNC, ClassificacaoNC, Pilar, OrigemNC, ChecklistID, Ciclo, `'DataCriacao '`, DataLimiteCorrecao, prazos aplicados, responsáveis, tratativa, flags de aviso) |
| MatrizClassificacaoNC | Regras oficiais por item (Campo, Pilar, ClassificacaoPadrao, PrazoDias, PrazoOperacional, ExigeEvidencia, Ativo) |
| RodizioPlanejado | Rodízio por sala (Sala, Ciclo, InicioRodizio, FimRodizio, StatusRodizio, Publicado, ResponsavelSala multi-pessoa) |
| RodizioQuadrimestral, FilaResponsaveisPorSalaRodizio | Apoio ao rodízio (não referenciadas diretamente nas fórmulas das telas auditadas) |
| AuditoriasPrograma | Auditorias (Title, TipoAuditoria, Sala, Ciclo, DataProgramada, StatusAuditoria, Resultado, ResponsavelAuditoria, DescricaoAchados, Encaminhamento, ImpactoSeguranca, PlanoAcaoGerado, DataConclusao) |

## Fluxos Power Automate

| Fluxo | Situação |
|---|---|
| RelatorioPDF_HistoricoInspecoes_JSON_V2 | Chamado pelo botão Gerar PDF. Estrutura TRY/CATCH/FINALLY; GetItems ($top 5000) → HTML → OneDrive → PDF → SharePoint → link organização → resposta JSON. **Filtro OData corrigido.** |
| RelatorioConsolidado_App_ProgramaPZ | **Órfão** (não chamado por nenhuma tela). Mesma estrutura; filtro também corrigido. Decidir integração ou remoção. |

## Conexões

SharePoint (`shared_sharepointonline`), Usuários do Office 365 (`shared_office365users`), Fluxos lógicos (`shared_logicflows`) e, dentro dos fluxos, OneDrive for Business (`shared_onedriveforbusiness` — conexão pessoal, ver Pendência 5).

## Coleções principais

`colMatrizClassificacaoNCAtiva`, `colMapaItens` (mapa item→pilar, 60+ itens), `colSalas`, `colNCtemporarias`(+Enriquecidas), `colNCcriadas`/`colErrosNC`/`colNCDuplicadas`, `colRodizioAtivoSala`/`colRodizioSalaAtual`/`colRodizioPlanejadoLocal`, `colChecklistIndicadoresBase`/`colChecklistTurnoGeral`/`colChecklistAdministrativo`/`colChecklistAdmUnico`/`colUltimoChecklistSala`/`colNCIndicadoresBase`/`colGraficoConformidade`/**`colNCReincidencia` (nova)**, `colRelCheckPreview`/`colRelPerguntasRespostas`/`colRelChecklistAgrupado`/`colMapaPerguntas`, `colNcChecklist`/`colNcPendentesMesmoChecklist` e variantes locais.

## Variáveis-chave

- Identidade: `varUserNome`, `varUserEmail`, `varPessoaLogadaSP`
- Estado/concorrência: `varBusy`, `varBusyIndicadores`, `varBusyRelFlex`, `varBusyPDF`, **`varBusyAuditoria` (nova)** — todas inicializadas no OnStart (**corrigido**)
- Checklist: `varRegistroChecklist`, `varSalaSelecionada`, `varCicloAtual`, `varSalaVaiParaPellet`, `varChecklistSemRodizioAtivo`, `varTemNC_*` (8)
- NC: `varPodeSalvarNC*`, `varResponsavelSalaNC`, `varMatrizClassificacaoNCValida`, `varErroCarregamentoMatrizNC`
- Indicadores: `varPercSalasConformes`, `varAderenciaChecklist(Adm)`, `varTempoMedioTratamentoNC`, `varTotalNCsPeriodo`, `varNCsEncerradasPeriodo`, **novas:** `varNCsVencidas`, `varNCsCriticasPeriodo`, `varSalasComReincidencia`, `varConformidadeSustentada`
- Relatório/PDF: `varParametrosPDF`, `varRetornoPDF`, `varLinkPDF`
- Auditoria: `varResultadoAuditoria`, **`varErroSalvarAuditoria` (nova)**

Variáveis apontadas como não usadas pelo App Checker (mantidas por segurança/contingência): 16 itens, ex.: `varSemInspecaoEscopo`, `varMetaAderenciaAdm`, `varNCsNaoEncerradasPeriodo` (agora recalculada também no botão), `varChecklistInicio`, `varMostraErrosInicio`, `varQtdNCOrganizacao` e análogas por sala.

## Perfis

Não há base de perfis implementada (ver Pendência 4 e Entregável 6-C). Papéis institucionais reconhecidos nas regras: usuário operacional, Equipe de Turno, Equipe Administrativa, Focal do Programa, auditor, Responsável Técnica, Coordenação, administrador.

## Principais regras institucionais implementadas no código

- Ciclos quadrimestrais C1/C2/C3-AAAA (fallback quando não há rodízio ativo)
- Turno = checklist semanal | Equipe ADM = quinzenal (TipoVerificacao gravado no registro)
- NC: sala, ciclo, responsável, descrição obrigatória, classificação pela matriz, prazo, status e histórico rastreável
- Classificação oficial: Baixa 15d, Média 10d, Alta 7d, **Crítica/Segurança = ação imediata** (validação estrita da matriz; contingência Média/10d marcada e justificada — a quantidade de NCs nunca eleva a classificação)
- Encerramento de NC somente com tratativa registrada (`AcaoCorretivaResponsavel`)
- Nenhuma sala sem checklist é considerada conforme (indicador usa apenas salas avaliadas)
- Indicadores calculados somente sobre `Checklist_OrganizacaoPellet2025` e `NaoConformidadesPorSala`
- Histórico jamais apagado: NCs duplicadas são ignoradas (não sobrescritas), contingências são marcadas, `ConclusaoComAtraso` preserva atraso
