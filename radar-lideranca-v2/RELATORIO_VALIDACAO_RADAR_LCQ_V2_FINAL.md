# Relatório de validação — Radar de Lideranças LCQ V2

**Status final: `APROVADO_OFFLINE`**
Código, estrutura, escopo e round-trip aprovados offline. Falta teste real no tenant (SharePoint, Pessoa, permissões, Power Automate). Não há evidência de execução no tenant, portanto **não** é `APROVADO_TENANT`.

| Item | Valor |
|---|---|
| Arquivo original | `Radar de Lideranças LCQ.msapp` — SHA-256 `59743753b94fa9649ce064265c4afe7e51210de3028f2d89e0d1a21815d6382c` |
| Arquivo final | `Radar_de_Liderancas_LCQ_V2_VALIDADO_FINAL.msapp` — SHA-256 `6062bd18454d8b0d68f152858d31e4540700dbe4317fe3a088dc0c76dd9ef501` |
| Ferramenta oficial | Power Platform CLI 2.12.2 (`pac canvas unpack/pack --layout SourceCode`) |
| Formato | DocVersion 1.349 · `packed.json` → `LoadFromYaml: true` (o Studio reconstrói o app a partir de `Src/*.pa.yaml`) |
| Sintaxe das fórmulas | Invariante (`,` e `;`), que é como o Power Apps grava; o Studio exibe em pt-BR (`;` e `;;`). Nada foi convertido. |

---

## 1. Estado inicial (evidência do arquivo)

| Item | Achado |
|---|---|
| Telas | 7: Cockpit, Demandas, Capacidade, Equipamentos, Radar Semanal, Auditoria, Administração. Guia integrado ao Cockpit. Confere com o histórico. |
| Data Sources | As 10 listas oficiais conectadas, mais o fluxo `ClickabuttoninPowerAppstosendanemail` e 4 fontes Sample. |
| Listas sem uso funcional | `Radar_Bloqueios`, `Radar_Decisoes` e `Radar_Encaminhamentos`: 0 referências. `Radar_SnapshotsKPI`: só `Refresh` no OnStart. |
| Erros salvos pelo Studio | `ParserErrorCount 0`, `BindingErrorCount 0` |
| SARIF existente | 274 itens, nenhum erro de fórmula: 219 de acessibilidade (109 em componentes de biblioteca sem uso), 23 variáveis sem uso, 17 mídias órfãs, 11 dicas de delegação e 1 `ForAllWithMutation`. Não estava desatualizada em relação às telas. |
| Schema real | `Radar_Demandas` **não possui** `PercentualProgresso` nem `Aprendizado`. Capacidade usa `FaixaSustentavel`. Equipamentos usa `DataHoraEncerramento`. |

## 2. Problemas encontrados e corrigidos

| # | Tela | Problema | Correção |
|---|---|---|---|
| 1 | Demandas | O salvamento fazia `SubmitForm` e depois um segundo `Patch` (IPD/CargaReal), o que permitia estado parcial. O formulário também não tem os campos obrigatórios Esforco/Impacto/Urgencia. | Um único `Patch` atômico: `frmDemanda.Updates` mais o registro calculado. Os 16 campos graváveis do schema são cobertos (prova em `evidencias/patch_coverage.txt`). Inclui guarda de permissão, anti-duplo-clique e erro com `IfError`/`FirstError`, sem gravação parcial. `OnSuccess`/`OnFailure` foram removidos porque não são mais acionados. |
| 2 | Auditoria | `btnNovoRegistroAuditoria.Visible = false`. Foi comprovado que não havia outro caminho para `varModoAuditoria = "Novo"`, então não era possível criar avaliações. | O botão passa a ficar visível para Liderança e Administrador. |
| 3 | Auditoria | A duplicidade mês+dimensão contava registros cancelados e bloqueava o próprio cancelamento. | Registros `Cancelado` ficam fora da regra, e salvar como Cancelado não sofre bloqueio. `Trim` aplicado no filtro do mês. |
| 4 | Administração | Liderança podia conceder o perfil Administrador, inclusive a si mesma. | Qualquer mudança que envolva o perfil Administrador (conceder, editar ou desativar) fica exclusiva de `varEhAdmin`. A Liderança mantém a administração normal dos integrantes. |
| 5 | Administração | `Select(btnAtualizar…)` roda depois da fórmula, então a checagem de falha lia um estado antigo. | Recarga síncrona com `IfError`. Ao salvar parâmetro, pesos e limites são recalculados na hora. |
| 6 | Administração | Não havia guarda no servidor para Liderança criar parâmetro ou alterar chave não permitida. Faltava validar e-mail e faixa maior que 0. | Guardas adicionadas na ação, não só na visibilidade. |
| 7 | App.OnStart | A soma dos pesos não era validada. | Se a soma for diferente de 1.00, o IPD usa os pesos oficiais 0.40/0.30/0.20/0.10 e a Liderança recebe aviso. |
| 8 | App/Menu | Usuário não cadastrado (`SemAcesso`) via e operava as telas operacionais. | O menu mostra só Cockpit e Guia. Há aviso no início, e os botões de criação (Demandas, Rotina, Bloqueios) têm guarda. |
| 9 | App.OnStart | `varUsuarioAtual` era definida duas vezes. | Duplicata removida. A ordem integrantes → usuário → integrante → cadastro → perfil → flags foi preservada. |
| 10 | Radar Semanal | Código residual de `MelhoriaIdentificada`: coleção, 13 ramos de `Switch`, `ForAll` com `false &&` e um KPI calculado e não exibido. | Removido com precisão sintática (diff por tokens em `DIFF_…md`). Nenhum dado histórico ou Choice foi alterado. |
| 11 | Radar Semanal | Envio da pauta sem trava de duplo clique. Botão com nome legado `btnAbaMelhoriaRotina`. | Trava em `OnSelect` e em `DisplayMode`. Botão renomeado para `btnEnviarPautaRotina`; a lógica do envio é idêntica. |
| 12 | Radar Semanal | O máximo de 6 valia só por envio. Um segundo envio na mesma semana passava do limite. | Máximo de 6 por **autor + semana + categoria**, somando os registros já gravados e os itens locais. Não há máximo global da equipe. O mínimo de 3 foi preservado. |
| 13 | Capacidade | `colCargaPorPessoa` era gravada com `CapacidadeMaxima` nesta tela e com `FaixaSustentavel` nas demais. | Unificada em `FaixaSustentavel`, nome do schema real. |
| 14 | Guia/Cockpit | O exemplo de IPD usava **Impacto 5**, fora da escala oficial 1–4. | Exemplo corrigido: 4/3/3/2 = 3,30. |
| 15 | Acessibilidade | 54 rótulos estáticos estavam focáveis. `togCuradoriaRotina` não tinha `AccessibleLabel` e `galHighlightsSemana` não tinha `TabIndex`. | `TabIndex=-1` nos rótulos, rótulo acessível e TabIndex adicionados. Os controles novos já têm `AccessibleLabel`, `TabIndex` e `FocusedBorder`. |
| 16 | Data Source | `RadioSample` sem nenhuma referência. | Removida. `ComboBoxSample` foi **preservada** porque o `SearchItems` padrão dos 4 ComboBox depende dela. `CustomGallerySample` e `DropDownSample` foram **preservadas** porque são referenciadas pelos padrões de `Templates.json`. |

## 3. Módulos implementados

| Módulo | Onde | Funcionalidade |
|---|---|---|
| **Bloqueios** (`Radar_Bloqueios`) | `TelaEquipamentos`, agora chamada **Ocorrências Operacionais**, com as abas **Equipamentos \| Bloqueios** | Listar (busca + Ativos/Encerrados/Todos), indicadores, criar, editar, concluir, cancelar, responsável, nível de impacto, demanda relacionada opcional (ID validado em `Radar_Demandas`), datas de abertura e resolução e motivo da resolução (obrigatório para encerrar). Integrante edita o que criou ou do qual é responsável; Liderança e Admin editam tudo. |
| **Decisões e Encaminhamentos** | Tela única `TelaDecisoesEncaminhamentos` com 2 abas | **Decisões** = memória da gestão, com os tipos Decisão/Alinhamento/Pendência de definição, semana AAAA-Sxx, contexto, resultado, prazo e data de fechamento automática. **Encaminhamentos** = ação executável, com responsável, prazo, status, observação/acompanhamento, atrasados em destaque e o botão Concluir. As duas listas ficam separadas. `IDPontoOrigem` é opcional e validado em `Radar_RegistrosRotina`. Liderança e Admin criam e editam. O integrante responsável atualiza status e acompanhamento. |
| **Cockpit — exceções de gestão** | Faixa enxuta com 3 indicadores | Bloqueios ativos (com quantos têm impacto alto), encaminhamentos atrasados e auditoria do mês (vulneráveis e em atenção, visível só para Liderança e Admin). Tudo calculado **ao vivo** em um bloco `IfError` isolado. Snapshot não é usado. |
| Menu | 7 telas + nova entrada "Decisões e Encaminhamentos" | O título "Equipamentos Críticos" passou a "Ocorrências Operacionais". |
| Guia e ajudas | Cockpit, Equipamentos, Administração e nova tela | Textos atualizados para telas, perfis, regras, categorias e novos módulos. |

**Choices com catálogo ausente no metadata:** as opções de Status, NivelImpacto e TipoRegistro de Bloqueios, Decisões e Encaminhamentos não vêm no `.msapp`. Os seletores usam `Choices(Fonte.Campo)`. As ações Concluir e Cancelar e o status inicial fazem `LookUp` **exato e ordenado** por valores esperados (por exemplo, Concluir: `Resolvido`, `Resolvida`, `Concluido`, `Concluído`…; Cancelar: `Cancelado`, `Cancelada`). Se o valor não existir, o `Patch` **não** é executado e aparece uma mensagem clara. Não há correspondência parcial por palavra-chave.

## 4. Snapshots (`Radar_SnapshotsKPI`)

Não há gravação, consumo, gráfico nem histórico no app. **Não foi implementado**: gravar a partir do app depende de qual usuário abre a tela e permite duplicidade no mesmo dia. **Dependência: `PENDENTE_VALIDACAO_TENANT`.** O caminho recomendado é um fluxo agendado no Power Automate, rodando uma vez por dia, que grave `DataSnapshot`, `DemandasAbertas`, `DemandasAtrasadas`, `BloqueiosAtivos`, `EquipamentosIndisponiveis`, `DemandasConcluidasSemana` e `IPDMedioEquipe`. O Cockpit continua 100% ao vivo.

## 5. Testes executados (offline)

| Camada | Ferramenta | Resultado |
|---|---|---|
| Schema YAML | Schema oficial `pa.schema.yaml` v3.0 (microsoft/PowerApps-Tooling) + jsonschema | **0 erros** (9 arquivos) |
| Sintaxe Power Fx | Parser oficial `Microsoft.PowerFx.Core` 1.8.1, cultura invariante | **6.391 fórmulas, 0 erros**. Controle negativo detectou erros plantados. |
| Referências | Script próprio: controles entre telas, `Navigate`, variáveis, coleções, fontes e chaves de `Patch` contra o schema real | **0 problemas**. Controle negativo detectou 6 de 6 defeitos plantados. |
| Lógica crítica | Interpretador oficial `Microsoft.PowerFx.Interpreter` 1.8.1 com expressões **extraídas do YAML final** | **74/74 PASS** (detalhe na matriz) |
| Cobertura de Patch | Comparação com o schema | Demandas 16/16. Bloqueios, Decisões, Encaminhamentos e Auditoria 100%. |
| Round-trip | `pac pack` → `pac unpack` → diff | `Src` idêntico, 8 telas, 552 controles em telas, 14 Data Sources, conexões idênticas, 27 assets byte a byte |

## 6. App Checker

Não há ferramenta offline que execute o App Checker. A `AppCheckerResult.sarif` do pacote é a **original** e fica desatualizada após as mudanças; o Studio a regenera ao salvar. Situação dos itens antigos:
- Erros de fórmula e referências inválidas: 0 pelos validadores acima.
- Acessibilidade nas telas: rótulos e toggle corrigidos. Os itens em componentes de biblioteca não usados (Header_EN, Header_PT etc.) não foram alterados porque não aparecem nas telas.
- `ForAllWithMutation` (envio semanal): mantido. O `ForAll` itera uma coleção e grava em **outra**, com resultado por `IDLocal`, o que torna a ordem irrelevante. A retentativa parcial é preservada.
- Variáveis sem uso e 17 mídias órfãs: classificadas como aviso, sem efeito funcional. As mídias não foram removidas para não mexer em binários.
- **Pendente:** abrir no Studio, rodar o App Checker e salvar (`PENDENTE_VALIDACAO_TENANT`).

## 7. Riscos remanescentes

| Risco | Nível | Tratamento |
|---|---|---|
| A carga a partir do YAML depende de o Studio aceitar o pacote. O PAC avisa: *"must be validated first by opening the app for edit"*. | Médio | Primeiro passo no tenant: importar, abrir para edição, conferir 0 erros e salvar. |
| Os valores reais dos Choices das 3 listas novas podem diferir dos esperados. | Médio | O app recusa a gravação com mensagem clara. Basta ajustar as opções ou a lista de valores esperados. |
| Delegação: limite de 500 linhas por consulta. As cargas usam filtro delegável `Criado >= hoje-730d` (Bloqueios, Decisões, Encaminhamentos) ou 180d (Rotina) e depois filtros locais. `Lower()` em LookUp de Integrantes e Config não delega, mas as listas são pequenas. | Baixo | Se alguma janela passar de 500 itens, elevar o limite para 2000 ou reduzir a janela. Nenhum uso de `Gallery.AllItems`. |
| A `CargaReal` gravada fica divergente quando os pesos mudam, até a demanda ser salva de novo. | Baixo (comportamento existente) | O Cockpit já sinaliza `CargaDivergente`. |
| `ImpactoOperacional` de Equipamentos não é gravado (campo oculto na versão original). | Baixo | Mantido. É decisão de produto. |
| `PercentualProgresso` e `Aprendizado` não existem em `Radar_Demandas`. | — | Não foram criados nem referenciados. Para usar, é preciso criar as colunas na lista. |

## 8. Dependências de tenant (`PENDENTE_VALIDACAO_TENANT`)

1. Importação e abertura no Studio (carga do YAML), App Checker e publicação.
2. Gravação real em todas as listas (Create, Edit, Concluir, Cancelar) e opções reais dos Choices.
3. Campo Pessoa (`Responsavel`, `ResponsavelAcompanhamento`) e `User().Email` com e-mails reais.
4. Permissões reais de lista no SharePoint (o app controla a interface e as ações, mas não substitui a permissão da lista).
5. Fluxo `ClickabuttoninPowerAppstosendanemail` (assinatura com 3 parâmetros e conexão Office 365).
6. Fluxo agendado de snapshots (não existe).

## 9. Respostas objetivas

| # | Pergunta | Resposta |
|---|---|---|
| 1 | O .msapp final é importável estruturalmente? | Sim no nível offline: empacotado pela ferramenta oficial, schema 0 erros, round-trip idêntico. Importação real: PENDENTE_VALIDACAO_TENANT. |
| 2 | Existem erros Power Fx conhecidos? | Não. 0 erros de sintaxe; a checagem de tipos completa só ocorre no Studio. |
| 3 | Existem referências inválidas? | Não (0). |
| 4 | Existem navegações quebradas? | Não. As 8 telas existem e o menu foi atualizado nas 8. |
| 5 | Os três perfis estão coerentes? | Sim. Menu e guardas foram testados por perfil, mais `SemAcesso`. |
| 6 | Demandas está funcional? | Sim offline: Patch atômico com 16/16 campos. Gravação real pendente. |
| 7 | O IPD está correto? | Sim. Escala 1–4 e pesos 0.40/0.30/0.20/0.10, com 5 casos de teste. |
| 8 | A Capacidade está correta? | Sim. Schema unificado em `FaixaSustentavel`; regra sem alteração. |
| 9 | Equipamentos está funcional? | Sim. Sem alteração de lógica; usa `DataHoraEncerramento`. |
| 10 | Bloqueios está implementado e funcional? | Implementado e testado offline. Choices reais pendentes. |
| 11 | A Rotina Semanal está funcional? | Sim. Mínimo 3, máximo 6 por autor, semana e categoria, com 11 casos de teste. |
| 12 | A Curadoria está funcional? | Sim. Sem alteração; restrita a Liderança e Admin na ação e na interface. |
| 13 | O envio da pauta está conectado? | A conexão e o fluxo foram preservados, com anti-duplo-clique. A execução real está pendente. |
| 14 | Decisões está implementado? | Sim. |
| 15 | Encaminhamentos está implementado? | Sim. |
| 16 | Auditorias está funcional? | Sim. A criação foi restaurada e a duplicidade corrigida, com 9 casos de teste. |
| 17 | A Administração está funcional? | Sim. Inclui proteção contra elevação de privilégio, com 9 casos de teste. |
| 18 | O Guia está coerente? | Sim. As 6 seções são botões reais e o conteúdo foi atualizado. |
| 19 | O Cockpit responde à pergunta central? | Sim. Atrasos, capacidade, equipamentos, bloqueios, encaminhamentos e auditoria, ao vivo. |
| 20 | O snapshot está restrito à tendência? | Sim, porque não é usado como número atual. A gravação de tendência não existe (pendente de fluxo). |
| 21 | Existem riscos de delegação? | Baixos e documentados (seção 7). |
| 22 | Existem riscos de segurança? | Sem risco conhecido na lógica do app. A segurança real depende da permissão das listas (tenant). |
| 23 | O round-trip passou? | Sim. |
| 24 | O que ainda depende do tenant? | Seção 8. |

## 10. Próximos passos recomendados (em ordem)

1. Importar `Radar_de_Liderancas_LCQ_V2_VALIDADO_FINAL.msapp`, abrir no Studio, conferir que não há erros, rodar o App Checker e salvar.
2. Confirmar as opções de Choice de `Radar_Bloqueios`, `Radar_Decisoes` e `Radar_Encaminhamentos` contra os valores esperados (seção 3).
3. Executar a `MATRIZ_TESTES_RADAR_LCQ_V2_FINAL.md` com um usuário de cada perfil.
4. Testar o envio da pauta com destinatário restrito antes de usar com a equipe.
5. Decidir sobre o fluxo de snapshots.
