# Relatório de Validação Final — Radar de Lideranças LCQ V2 (V5)

Arquivo auditado: `Radar_de_Liderancas_LCQ_V2_V5_CORRIGIDO_v3.msapp`
Arquivo entregue: `Radar_de_Liderancas_LCQ_V2_V5_FINAL_VALIDADO.msapp`
Data da auditoria: 2026-07-15

Este relatório documenta uma auditoria e correção **estática** do arquivo `.msapp` real (ZIP + JSON internos), sem acesso a Power Apps Studio, PAC CLI ou conexão real com o SharePoint neste ambiente. Todas as conclusões abaixo são baseadas em leitura e edição direta dos arquivos internos do pacote, não em execução do aplicativo.

---

## 1. Estado base da V3 (10 pontos de partida) — confirmação direta no arquivo

| # | Item | Resultado |
|---|------|-----------|
| 1 | ZIP válido | ✅ Confirmado (`unzip -t` e `zipfile.testzip()`, sem erros) |
| 2 | 99 entradas internas | ✅ Confirmado (`unzip -l` = 99 arquivos) |
| 3 | Todos os JSONs interpretáveis | ✅ Confirmado (63/63 arquivos `.json` parseados sem erro) |
| 4 | Separador entre último `Set()` e `If()` em `TelaCockpit.OnVisible` | ✅ Confirmado — há `;` entre o `Set(varCarregandoCockpit, false)` e o `If(varFalhaCargaCockpit, Notify(...))` |
| 5 | `Criticidade_DataCard.Update` usa `ThisItem.Criticidade` no ramo sem permissão | ✅ Confirmado — fórmula idêntica à especificada |
| 6 | `colPrioridadesSemana` ausente | ✅ Confirmado — zero ocorrências em todo o pacote |
| 7 | `colPontosPautaSemana` é a coleção oficial | ✅ Confirmado — usada em `App.OnStart`, `TelaRadarSemanal` e `btnEnviarRotina` |
| 8 | Banner `htmlAvisoCockpit` existe | ✅ Confirmado |
| 9 | `Criticidade_DataCard` existe dentro de `frmDemanda` | ✅ Confirmado |
| 10 | Curadoria semanal separa Patch() da recarga | ✅ Confirmado — `btnSalvarCuradoriaRotina` já isola gravação, recarga e mensagem em blocos distintos |

Nenhuma divergência foi encontrada em relação ao estado declarado da V3. A auditoria prosseguiu com correções sobre esse estado confirmado.

---

## 2. Achado central confirmado: salvamento da Auditoria

Confirmado exatamente como descrito: em `TelaAuditoria`, `btnSalvarAuditoria.OnSelect` mantinha `Patch()`, `Select(btnAtualizarAuditoria)` (recarga), fechamento do painel e mensagem de sucesso **dentro do mesmo `IfError()`**. Qualquer falha na recarga (mesmo com o registro já gravado no SharePoint) era relatada ao usuário como "Não foi possível salvar a avaliação." — uma falsa negativa que podia levar a nova tentativa e duplicidade.

Adicionalmente, a auditoria de todos os fluxos de gravação (`Patch`/`SubmitForm`) do aplicativo revelou que **o mesmo padrão de falha** existia em dois botões de `TelaAdministracao`: `btnSalvarIntegranteAdmin` e `btnSalvarParametroAdmin`. Ambos foram corrigidos com a mesma técnica, por se tratar de uma incompatibilidade real e confirmada, e por a Administração estar explicitamente no escopo de auditoria de fluxos de gravação.

Os demais fluxos de gravação do aplicativo (Demandas, Equipamentos, Rotina Semanal, Curadoria Semanal) **já implementavam corretamente** a separação entre gravação, recarga e mensagem — nenhuma alteração foi necessária neles. Ver detalhes na tabela da Seção 3.

---

## 3. Tabela de auditoria e correção

| Tela | Controle | Propriedade | Situação anterior | Correção | Validação |
|------|----------|-------------|--------------------|----------|-----------|
| TelaAuditoria | btnSalvarAuditoria | OnSelect | `Patch()`, `Select(btnAtualizarAuditoria)`, fechamento do painel e `Notify()` de sucesso dentro do mesmo `IfError()` que envolvia o `Patch()`. Falha de recarga era reportada como falha de gravação. Sem verificação de permissão no início do `OnSelect`. | Reescrito: `Patch()` isolado em `IfError()` próprio (`varAuditoriaSalva`); recarga isolada via `Select(btnAtualizarAuditoria)` + checagem de `varErroAuditoria` (`varFalhaRecargaAuditoria`); painel só fecha após sucesso real do `Patch()`; mensagem diferencia "não foi salvo" de "foi salvo, mas não foi recarregado"; checagem de permissão (`varEhLideranca \|\| varEhAdmin`) como primeira condição do `If()`; bloqueio contra duplo clique via `varSalvandoAuditoria`. | JSON válido; parênteses/chaves balanceados (33/33, 6/6); variáveis referenciadas já existiam no app (`varEhLideranca`, `varEhAdmin` setadas em `App.OnStart`) |
| TelaAuditoria | btnSalvarAuditoria | DisplayMode | `If(varSalvandoAuditoria, DisplayMode.Disabled, DisplayMode.Edit)` — sem checagem de permissão. | `If(!(varEhLideranca \|\| varEhAdmin), DisplayMode.View, If(varSalvandoAuditoria, DisplayMode.Disabled, DisplayMode.Edit))` — defesa em profundidade independente do menu. | JSON válido; parênteses balanceados (3/3) |
| TelaAdministracao | btnSalvarIntegranteAdmin | OnSelect | Mesmo padrão de falha do item acima: `Patch()` + `Select(btnAtualizarAdministracao)` + fechamento de painel + `Notify()` de sucesso no mesmo `IfError()`. Sem checagem de permissão. | Mesma técnica de separação (`varIntegranteAdminSalvo`, `varFalhaRecargaIntegranteAdmin`); checagem de permissão (`varEhLideranca \|\| varEhAdmin`, consistente com a regra já usada em `TelaAdministracao.OnVisible`) no início do `OnSelect`; bloqueio de duplo clique via `varSalvandoIntegranteAdmin`. | JSON válido; parênteses balanceados (34/34, 2/2) |
| TelaAdministracao | btnSalvarIntegranteAdmin | DisplayMode | `DisplayMode.Edit` fixo, sem qualquer checagem. | `If(!(varEhLideranca \|\| varEhAdmin), DisplayMode.View, If(varSalvandoIntegranteAdmin, DisplayMode.Disabled, DisplayMode.Edit))` | JSON válido; parênteses balanceados (3/3) |
| TelaAdministracao | btnSalvarParametroAdmin | OnSelect | Mesmo padrão de falha. Sem checagem de permissão. | Mesma técnica de separação (`varParametroAdminSalvo`); checagem de permissão; bloqueio de duplo clique via `varSalvandoParametroAdmin`. | JSON válido; parênteses balanceados (29/29, 1/1) |
| TelaAdministracao | btnSalvarParametroAdmin | DisplayMode | `DisplayMode.Edit` fixo. | `If(!(varEhLideranca \|\| varEhAdmin), DisplayMode.View, If(varSalvandoParametroAdmin, DisplayMode.Disabled, DisplayMode.Edit))` | JSON válido; parênteses balanceados (3/3) |
| TelaAuditoria | TelaAuditoria (tela) | OnVisible | — | Nenhuma alteração — fórmula já correta (ver Seção 4). | Tipos do `IfError()` compatíveis (booleano/booleano); `varCarregandoAuditoria` sempre finaliza `false`; `colAuditoriaTela` só é limpa quando a carga falha |
| TelaDemandas | Criticidade_DataCard | DataField/Default/Update | — | Nenhuma alteração — já correto (ver Seção 5). | `Update` idêntico à fórmula exigida; `X=1, Y=2`; sem sobreposição com `Status_DataCard1` (`X=0, Y=2`) |
| TelaCockpit | htmlAvisoCockpit | Visible/HtmlText | — | Nenhuma alteração — já correto (ver Seção 6). | `Visible = varFalhaCargaCockpit`; texto usa `varErroCockpit`; primeiro filho do container `cntConteudoNovo` (auto-layout vertical) |
| TelaDemandas | frmDemanda | OnSuccess | — | Nenhuma alteração — já correto. | `Patch()` do IPD isolado (`varErroSalvarIPD`); recarga isolada (`varFalhaRecargaDemandas`); falha do segundo `Patch()` reabre o formulário em modo edição em vez de duplicar o registro |
| TelaEquipamentos | btnSalvarEquipamento | OnSelect | — | Nenhuma alteração — já correto. | `Patch()` isolado (`varEquipamentoSalvo`); recarga isolada com mensagem própria; `varSalvandoEquipamento` liberado em todos os caminhos |
| TelaRadarSemanal | btnEnviarRotina | OnSelect | — | Nenhuma alteração — já correto. | Gravação por item com `Sucesso` individual; recarga isolada (`varFalhaRecargaRotina`); mensagens diferenciam sucesso total, sucesso parcial e falha de recarga |
| TelaRadarSemanal | btnSalvarCuradoriaRotina | OnSelect | — | Nenhuma alteração — já correto (é o padrão de referência replicado nas correções acima). | `Patch()` isolado (`varCuradoriaSalva`); recarga isolada (`varFalhaRecargaCuradoria`); checagem de permissão já presente no início do `OnSelect` |

---

## 4. TelaAuditoria.OnVisible

Não foi reescrita — a fórmula já estava correta e foi apenas validada:

- Liderança/Administrador carregam os registros: `If(varEhLideranca || varEhAdmin, Set(varCargaAuditoriaOk, IfError(...)), Clear(colAuditoriaTela))`.
- Integrante não autorizado recebe `colAuditoriaTela` vazia (`Clear`, sem tentativa de carga).
- `varCarregandoAuditoria` termina sempre `false` (última instrução da fórmula, incondicional).
- `varErroAuditoria` recebe mensagem via `Coalesce(FirstError.Message, "...")` em caso de falha.
- `colAuditoriaTela` só é limpa novamente se `varCargaAuditoriaOk = false` — não é limpa após uma carga bem-sucedida.
- O `IfError()` retorna booleano em ambos os ramos (`true`/`false`) — sem mistura de tipos tabela/booleano ou registro/texto.

---

## 5. Criticidade_DataCard (TelaDemandas → frmDemanda)

Confirmado, sem alterações:

- `DataField = "Criticidade"`, `Default = ThisItem.Criticidade`, `Required = false`.
- `Update`:
  ```
  If(
      varEhLideranca || varEhAdmin,
      DataCardValueCriticidade.Selected,
      ThisItem.Criticidade
  )
  ```
- ComboBox `DataCardValueCriticidade`: `Items = Choices(Radar_Demandas.Criticidade)`, `SelectMultiple = false`, `DisplayMode = Parent.DisplayMode`.
- `Visible = varModoDemanda <> "Nova" || varEhLideranca || varEhAdmin` — oculto para Integrante ao criar nova demanda; visível para Liderança/Administrador mesmo na criação.
- `DisplayMode = If(varModoDemanda = "Visualizar", DisplayMode.View, varEhLideranca || varEhAdmin, DisplayMode.Edit, DisplayMode.View)` — Integrante nunca edita, mesmo em modo "Editar" da própria demanda.
- Nenhum valor padrão "Média" é atribuído automaticamente.
- Layout: `Status_DataCard1` em `X=0, Y=2`; `Criticidade_DataCard` em `X=1, Y=2` — colunas distintas na mesma linha, sem sobreposição. `ControlUniqueId` de ambos (399 e 706) distintos.

---

## 6. Banner htmlAvisoCockpit

Confirmado, sem alterações:

- `Visible = varFalhaCargaCockpit`.
- `HtmlText` concatena `varErroCockpit` dentro de um `<div>` com borda/fundo de alerta.
- É o **primeiro filho** do container `cntConteudoNovo`, que usa `LayoutMode.Auto` + `LayoutDirection.Vertical` — quando visível, empurra título e KPIs para baixo automaticamente, sem sobreposição e sem posicionamento manual.
- `TelaCockpit.OnVisible` termina com separador válido entre o último `Set()` e o `If(... Notify(...))` (ver item 4 da Seção 1).
- Banner persistente e `Notify()` (toast) disparam juntos na mesma condição (`varFalhaCargaCockpit`). Avaliação: para uma tela de decisão executiva (Cockpit), manter os dois reforça a segurança da decisão — o toast chama atenção imediata, o banner mantém o alerta visível enquanto o usuário navega pela tela. Não foi alterado; registrado como decisão de design, não como bug.
- Observação menor (não bloqueante): `AutoHeight = false`, altura fixa de 56px. Mensagens muito longas podem não quebrar linha de forma ideal dentro dessa altura. Não foi alterada por não haver confirmação de estouro real sem teste visual no Studio.

---

## 7. Auditoria de todos os IfError()

Foram inspecionados todos os `IfError()` das telas listadas no escopo (`App.OnStart`, `TelaCockpit.OnVisible`, `TelaDemandas.OnVisible`/`frmDemanda.OnSuccess`, `TelaCapacidade.OnVisible`, `TelaEquipamentos.OnVisible`, `TelaRadarSemanal.OnVisible`, `btnEnviarRotina.OnSelect`, `btnSalvarCuradoriaRotina.OnSelect`, `TelaAuditoria.OnVisible`, `btnSalvarAuditoria.OnSelect`, `TelaAdministracao`).

- `IfError(Concurrent(...), ...)` em `App.OnStart` e `TelaCockpit.OnVisible`: ambos os ramos retornam o resultado de `Set()` (sem tipo de retorno relevante — usados como comando, não como expressão). Sem incompatibilidade de tipos.
- Nenhum `IfError()` mistura tabela com booleano ou registro com texto nos formulários auditados.
- Nenhuma falha de `Refresh()` é tratada como falha de `Patch()`, exceto o caso já corrigido (Seção 2).
- `varCarregandoX`/`varSalvandoX` são liberados em todos os caminhos nos fluxos auditados.

Nenhuma alteração foi feita nesta seção além das descritas na Seção 3 — não foram encontradas outras incompatibilidades reais de tipo que justificassem mudança.

---

## 8. Segurança por perfil

- `varPerfilAtual`, `varEhLideranca`, `varEhAdmin` são definidas em `App.OnStart` (Bloco 4) e recalculadas em `TelaCockpit.OnVisible` — disponíveis em todo o app desde o carregamento inicial.
- Comparação de e-mail usa `Lower()` de forma consistente (`varUsuarioAtual = Lower(User().Email)`, `Lower(Email) = Lower(User().Email)`, etc.).
- Campos de pessoa (`Responsavel`, `ResponsavelAcompanhamento`) são comparados por `.Email`, nunca diretamente.
- Campos Choice (`Status`, `Criticidade`, `Perfil`, etc.) são comparados por `.Value` de forma consistente em todo o código auditado.
- **Achado corrigido**: `btnSalvarAuditoria`, `btnSalvarIntegranteAdmin` e `btnSalvarParametroAdmin` não verificavam permissão nem em `DisplayMode` nem no início do `OnSelect` — dependiam apenas do botão estar em uma tela cujo item de menu ficava oculto para quem não tinha permissão. Corrigido nas três (Seção 3). Isso fecha o acesso direto a essas ações de gravação para quem não é Liderança/Administrador, mesmo que a tela seja alcançada por navegação direta.
- Os demais botões administrativos de leitura/abertura de painel (`btnAtualizarAdministracao`, `btnNovoIntegranteAdmin`, `btnNovoParametroAdmin`, `btnAbrirAuditoria`, `btnNovoRegistroAuditoria`) continuam com `DisplayMode.Edit` fixo — abrir um painel de edição não grava dados por si só (a gravação real agora está protegida no botão Salvar), portanto não foi alterado por estar fora do escopo confirmado como bug real; fica registrado como observação de reforço futuro, não como falha corrigida nesta rodada.

---

## 9. Coleções e variáveis

- `colHighlightsSemana`, `colLowlightsSemana`, `colMelhoriasSemana`, `colPontosPautaSemana`: todas criadas via `ClearCollect()` com schema completo (`IDLocal`, `Ordem`, `Texto`, `Obrigatorio`, `Salvo`) e só então esvaziadas com `Clear()` — nenhuma delas recebe `Clear()` antes de ter schema definido.
- `colResultadoEnvioRotina`: schema `Categoria`, `IDLocal`, `Sucesso` confirmado.
- Zero ocorrências de `colPrioridadesSemana` em todo o pacote.
- Variáveis textuais de estado (`varErroCockpit`, `varErroAuditoria`, etc.) inicializam com `""`, não `Blank()`.
- Variáveis booleanas mantêm tipo booleano de forma consistente nos fluxos auditados.
- Não foram encontrados usos indevidos de `UpdateContext()` no lugar de `Set()` global nos formulários auditados (o único uso de `UpdateContext()` encontrado, em `frmDemanda.OnSuccess`, é proposital para variáveis de contexto de tela, coexistindo com `Set()` para variáveis globais, de forma consistente).

---

## 10. SharePoint e Power Fx

- Coluna nativa `Title` usada em todos os `Patch()`/`ClearCollect()` para os itens do SharePoint. `References/DataSources.json` confirma `"Title": "Título"` apenas como **rótulo de exibição em pt-BR** da coluna nativa `Title` (`ConnectedDataSourceInfoNameMapping`) — não é uma coluna separada chamada "Titulo"/"Título". As ocorrências de `Titulo:`/`vTitulo:` encontradas no código são nomes de variáveis locais (`With()`) ou chaves da coleção local `colMenu` (não são colunas do SharePoint).
- `Choice` comparado por `.Value` de forma consistente (confirmado por amostragem em `Status`, `Criticidade`, `Perfil`).
- `Pessoa` comparado por `.Email`, e-mails normalizados com `Lower()`.
- Nenhuma ocorrência de `GroupBy()` sobre campos de pessoa.
- `Radar_Config.Valor` convertido com `Value(cfg.Valor, "en-US")`.
- IPD calculado no Power Apps (`AddColumns(..., IPDCalculado, ...)` em `TelaCockpit.OnVisible` e `frmDemanda.OnSuccess`) e gravado em `CargaReal` via `Patch()`.
- Pesos oficiais confirmados como padrão em `App.OnStart`: Esforço 0,40; Impacto 0,30; Urgência 0,20; Risco 0,10 (sobrescritos por `Radar_Config` quando configurado).
- Cockpit calcula KPIs ao vivo (`ClearCollect`/`AddColumns` em `TelaCockpit.OnVisible`); `Radar_SnapshotsKPI` é usado exclusivamente para `colTendenciaKPI`/`colTendenciaOrdenada` (tendência histórica).
- Coluna `FaixaSustentavel` preservada e em uso (`Radar_Integrantes.FaixaSustentavel`).
- Termos legados proibidos: `PesoCargaOperacional` e `DataHoraNormalizacao` — zero ocorrências no código ativo (aparecem apenas dentro de `AppCheckerResult.sarif`, que é um relatório histórico desatualizado, não código executável — ver Seção 12). `colPrioridadesSemana` — zero ocorrências confirmadas. `Header_EN.FAQ()` — zero ocorrências no código ativo (ver Seção 11).

---

## 11. Navegação, menus e Header_EN_1

- `colMenu` (App.OnStart) tem 8 chaves: `Cockpit`, `Demandas`, `Capacidade`, `Equipamentos`, `Rotina`, `Auditoria`, `Guia`, `Administracao`.
- O `Switch()` de navegação (idêntico nas 7 telas, verificado por amostragem completa) cobre as 8 chaves, incluindo `"Guia" → Notify("O Guia do Radar ainda está em construção.", NotificationType.Information)` — não cai no `Notify("Opção de menu não reconhecida.")`. Bloqueios, Encaminhamentos e Decisões não têm entrada em `colMenu` (não estão visíveis) — lacuna de escopo já esperada, sem tela fantasma ou item quebrado.
- Todos os destinos `Navigate()` (`TelaCockpit`, `TelaDemandas`, `TelaCapacidade`, `TelaEquipamentos`, `TelaRadarSemanal`, `TelaAuditoria`, `TelaAdministracao`) correspondem a telas reais existentes no pacote.

### Header_EN_1

- **Zero instâncias** em qualquer tela (`Controls/*.json`) — confirmado por busca em todas as 8 telas.
- Existe apenas como definição de componente (`Components\166.json`), registrado em `ComponentsMetadata.json`, e referenciado em `Src\_EditorState.pa.yaml` (estado do editor, não é fonte ativa).
- **Achado adicional durante a investigação**: o único componente de cabeçalho realmente instanciado nas 7 telas é `Header_PT_4` (`Components\318.json`, `TemplateName c89ea42e826c4ef092b008a8e4af5eb1`), com uma instância por tela (`Header_PT_7`, `Header_PT_8`, `Header_PT_Capacidade`, `Header_PT_Equipamentos`, `Header_PT_Rotina`, `Header_PT_Auditoria`, `Header_PT_Administracao`). `Header_PT_4` não apresenta a auto-chamada `.FAQ()` nem problema de `.Width` — os dois erros históricos ligados a cabeçalho já estão resolvidos no componente realmente em uso.
- Além de `Header_EN_1`, também estão **órfãos** (definidos mas não instanciados em nenhuma tela): `Header_EN` (`Components\55.json`), `Header_PT` (`Components\87.json`) e `Header_PT_6` (`Components\233.json`). `Header_PT` e `Header_PT_6` ainda contêm, internamente, uma auto-chamada inválida (`Header_PT.FAQ()` e `Header_PT_6.FAQ()`, respectivamente, no `OnSelect` de um controle `Contact_*` interno) — da mesma classe do antigo erro de `Header_EN_1`. Como nenhum desses componentes está instanciado em tela alguma, essas fórmulas nunca são avaliadas em tempo de execução: são código morto, não um risco funcional ativo.
- Não foi tentada exclusão via edição direta de JSON bruto, por não haver PAC CLI ou Power Apps Studio disponíveis neste ambiente e pelo risco de corromper `ComponentsMetadata.json`/referências cruzadas. `Header_EN_1`, `Header_EN`, `Header_PT` e `Header_PT_6` permanecem neutralizados (nunca instanciados) e íntegros no pacote. Remoção registrada como pendente — ver `PENDENCIAS_STUDIO_V5.md`.

---

## 12. Sincronização Src/*.pa.yaml e App Checker

- `Src/*.pa.yaml` não foi tratado como fonte ativa e não foi editado manualmente.
- Divergência pré-existente confirmada: `Src\TelaDemandas.pa.yaml` e `Src\TelaCockpit.pa.yaml` não refletem todos os controles novos de `Controls/*.json` (conforme já relatado antes desta rodada).
- Nova divergência esperada, decorrente das correções desta rodada: `Src\TelaAuditoria.pa.yaml` e `Src\TelaAdministracao.pa.yaml` também não refletem as fórmulas corrigidas de `btnSalvarAuditoria`, `btnSalvarIntegranteAdmin` e `btnSalvarParametroAdmin`, porque `Controls/*.json` é a fonte ativa carregada pelo Studio e foi editada diretamente; os espelhos `.pa.yaml` só são regenerados quando o Studio salva o app.
- **App Checker**: `Properties.json` reporta `ParserErrorCount = 0` e `BindingErrorCount = 4`. Os 4 erros de `AppCheckerResult.sarif` (`app-ErrUnknownNamespaceFunction`, `app-ErrInvalidDot`, `app-ErrBadType-ExpectedType-ProvidedType`, `app-ErrInvalidArgs-Func`) correspondem, pelos trechos (`snippet.text`) registrados no próprio relatório, exatamente aos quatro problemas históricos já tratados antes desta rodada: `Header_EN.FAQ()`, `.Width` (Header_PT_4), e dois erros de tipo em `TelaAuditoria.OnVisible` (sintaxe com `;` de uma versão anterior em pt-BR). A auditoria estática confirma que nenhum desses quatro trechos existe mais no código ativo. Isso indica que `AppCheckerResult.sarif`/`Properties.json` estão **desatualizados** (gerados antes das correções já presentes na V3) e não foram regenerados. **Não foram editados manualmente** — nem para zerar, nem por qualquer outro motivo — conforme instrução explícita. A execução real do App Checker permanece **pendente no Power Apps Studio**.

---

## 13. Validações estruturais executadas

| Verificação | Resultado |
|---|---|
| Integridade do ZIP final (`unzip -t`) | ✅ Sem erros |
| Integridade do ZIP final (`zipfile.testzip()`, leitor independente) | ✅ Sem erros |
| Parse de todos os 63 arquivos `.json` no pacote final | ✅ 0 erros |
| Balanceamento de parênteses/chaves nas fórmulas alteradas | ✅ Confirmado (ver Seção 3) |
| Unicidade de `ControlUniqueId` | ✅ 691 controles, 691 IDs únicos, 0 duplicatas |
| Contagem de entradas do pacote final vs. V3 | ✅ 99 = 99, mesmos nomes/caminhos (inclusive barras invertidas) |
| Diferença de conteúdo arquivo a arquivo (V3 vs. Final) | ✅ Apenas `Controls\574.json` e `Controls\626.json` diferem; os outros 97 arquivos são byte-idênticos |
| Termos legados proibidos no código ativo | ✅ Zero ocorrências (`colPrioridadesSemana`, `PesoCargaOperacional`, `DataHoraNormalizacao`, `Header_EN.FAQ()`, `Titulo`/`Título` como coluna SharePoint) |
| Conexões SharePoint (`References/DataSources.json`) | ✅ Preservadas — arquivo byte-idêntico ao original |

---

## 14. Testes funcionais

**Não realizados neste ambiente** — não há Power Apps Studio, PAC CLI nem conexão real com o SharePoint disponíveis nesta sessão. Nenhum dos seguintes testes foi executado:

- Importação do `.msapp` no Power Apps Studio.
- Criação/edição/visualização de demanda pelos três perfis (Integrante, Liderança, Administrador).
- Registro de Rotina Semanal, curadoria semanal, avaliação de Auditoria, alteração de parâmetros de Administração.
- Gravação real no SharePoint (Patch efetivo).
- Simulação de falha de `Patch()`, falha isolada de `Refresh()`, duplo clique em Salvar, falha parcial no envio semanal, falha na carga do Cockpit, falha na carga da Auditoria.
- Execução do App Checker real dentro do Studio.

O que foi feito nesta rodada é uma **auditoria e correção estática completa do código-fonte real do `.msapp`**, com validação estrutural do pacote (ZIP, JSON, IDs, referências) e leitura manual, linha a linha, de todos os fluxos de gravação e das fórmulas em escopo.

---

## 15. Parecer final

**APROVADO ESTATICAMENTE — TESTES NO STUDIO PENDENTES**

As expressões "100% funcional", "100% corrigido", "pronto para produção" e "pronto para piloto" não são usadas neste relatório, pois nenhuma das condições abaixo foi cumprida neste ambiente:

- [ ] Importação comprovada no Power Apps Studio
- [ ] App Checker executado sem erros altos (o `AppCheckerResult.sarif` atual está desatualizado e não reflete o estado corrigido)
- [ ] Teste de gravação real no SharePoint
- [ ] Teste dos três perfis (Integrante, Liderança, Administrador)
- [ ] Teste de falha de recarga isolada
- [ ] Teste de duplo clique

O que está comprovado, com evidência reproduzível neste relatório: o pacote é um ZIP íntegro de 99 entradas, todos os 63 JSONs internos são válidos, as fórmulas corrigidas têm parênteses/chaves balanceados e referenciam apenas variáveis já existentes no app, nenhum arquivo fora do escopo foi alterado, e as conexões de dados foram preservadas byte a byte.

Antes do piloto, é necessário: abrir o `.msapp` final no Power Apps Studio, deixar os `Src/*.pa.yaml` e o App Checker serem regenerados, executar o App Checker real, e rodar os testes funcionais listados na Seção 14 e em `PENDENCIAS_STUDIO_V5.md`.
