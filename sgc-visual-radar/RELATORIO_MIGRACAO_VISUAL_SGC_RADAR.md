# Migração do padrão visual do Radar de Lideranças para o SGC LCQ RJ

Data: 18/09/2026 · Base funcional: `SGC_LCQ_RJ.msapp` · Base visual: `Radar_de_Liderancas_LCQ_V2_CORRIGIDO_FINAL_V2.msapp`

## 1. O que foi feito

Refatoração visual do Sistema de Gestão de Competências (SGC) para o design system do Radar de Lideranças, preservando integralmente a arquitetura funcional do SGC. Nenhuma regra de negócio, fonte de dados, fórmula de gravação, filtro ou navegação funcional foi alterada.

A edição foi feita diretamente no código-fonte do aplicativo (`Src/*.pa.yaml` e `Controls/*.json` dentro do `.msapp`), com um conjunto de scripts determinísticos (pasta `ferramentas/`) que aplica a mesma operação nas duas representações, mantendo-as equivalentes.

## 2. Telas alteradas (8 de 8, nenhuma perdida)

| Tela | Referência visual do Radar | Principais mudanças |
|---|---|---|
| `scrInicio` | TelaCockpit | Cabeçalho institucional, menu lateral, título executivo, KPIs em card branco com barra de situação, rodapé |
| `scrQualificacoes` | Demandas / Auditoria | Card de filtros, cabeçalho de lista, linhas limpas, badges de status pill |
| `scrHistoricoAvaliacoes` | Demandas | Filtros, contagem, lista e badges no padrão Radar |
| `scrModulos` | Equipamentos | Lista + painel de detalhe com cards brancos, raio 14, borda discreta |
| `scrCobertura` | TelaCapacidade | KPIs de cobertura, matriz e legenda no padrão de cards do Radar |
| `scrNovaAvaliacao` | Formulários do Radar | Formulário em card branco centralizado na área de conteúdo |
| `scrAvaliacao` | Telas operacionais | Seções em cards, barra de ações inferior, badges de estado |
| `scrDetalheQualificacao` | Detalhamento executivo | Resumo, progresso e módulos com o mesmo acabamento |

## 3. Componentes criados (por tela, 5 controles novos)

- `imgNav<Suf>` — `Image` com o recurso **`Nav`** do Radar (faixa institucional Braskem 1440×90, com a marca), sobre base `#0E2A4A`.
- `htmlCabecalho<Suf>` — `HtmlViewer` transparente sobre a faixa, com o título **Sistema de Gestão de Competências** e a subidentificação **LCQ-RJ** (31 px/800 e 16 px/700, como no Radar).
- `htmlMenu<Suf>` — `HtmlViewer` dentro da galeria de navegação, reproduzindo item a item o `galMenuLateralNovo` (estado selecionado, barra lateral, caixa de sigla, tipografia e raios).
- `htmlTitulo<Suf>` — bloco de título executivo (26 px / peso 800) com barra vertical `#1C5582` e subtítulo 16 px. Onde o subtítulo era dinâmico, a fórmula original foi preservada e apenas embutida na concatenação.
- `htmlRodape<Suf>` — rodapé "Idealizado e implementado por Rodrigo Barbosa Tavares da Mota | LCQ RJ — Braskem", com o mesmo tratamento tipográfico do Radar.

Controles removidos (apenas decoração antiga, sem fórmula): `lblMarca*`, `recDivisorHeader*`, `recNavAtivo*`, `lblTitulo*`/`lblSub*` (substituídos pelo bloco HTML). Saldo: neutro (5 removidos, 5 criados por tela).

## 4. Shell principal

- **Cabeçalho**: 90 px, faixa institucional `Nav` (com a marca Braskem) sobre base `#0E2A4A`, usuário conectado à direita, CTA **+ Nova avaliação** em pill branco e botão **Ajuda** em pill com fundo sólido para contraste sobre a área laranja.
- **Menu lateral**: faixa de 260 px (galeria `X=8`, largura 252, `TemplateSize=68`, `TemplatePadding=3`), itens `IN / QL / HI / MD / CB`, item ativo com fundo `#E5EEF9`, barra `#143A66`, borda `#D7E3F1`, raio 13 px; hover `RGBA(14,42,74,0.06)` sobre botão transparente — apresentação em HTML, interação em controle real.
- **Conteúdo**: deslocado 260 px à direita; larguras e alturas relativas recalculadas (`Parent.Width - 64` → `- 324`, etc.).
- **Rodapé**: 30 px, largura total.
- A navegação horizontal anterior foi convertida na galeria lateral — a galeria, seu `Items` e as fórmulas de `OnSelect` continuam sendo as do SGC.

## 5. Design tokens aplicados

| Token | Valor |
|---|---|
| Primária | `RGBA(14, 42, 74, 1)` — #0E2A4A |
| Secundária | `RGBA(28, 85, 130, 1)` — #1C5582 |
| Fundo | `RGBA(245, 247, 250, 1)` — #F5F7FA |
| Card | #FFFFFF |
| Texto | #202A35 · Texto suave #657384 |
| Borda | #D8E1EA |
| Verde / Amarelo / Laranja / Vermelho | #2E7D32 · #CA8A04 · #B45309 · #B91C1C |
| Badges | texto/fundo #256B35/#E7F3E9, #806000/#FFF7D8, #A14E08/#FFF0DF, #A91515/#FBE7E7, #52657A/#EEF2F6 |

Outros ajustes: tipografia `Font.Lato` → `Font.'Open Sans'` em todo o app (Segoe UI nos blocos HTML, como no Radar); raios 4 → 10 e 8 → 14; barra de acento dos cards de situação 4 → 5 px; badges em pill; campos de texto com raio 10 e borda `#D8E1EA`; modal de ajuda com raio 18, sombra marcada e overlay `RGBA(14,42,74,0.34)`.

`App.OnStart` recebeu, **após** todo o bloco funcional existente (preservado integralmente), as variáveis de tema: `varCorPrimaria`, `varCorSecundaria`, `varCorFundo`, `varCorCard`, `varCorTexto`, `varCorTextoSuave`, `varCorBorda`, `varCorVerde`, `varCorAmarelo`, `varCorLaranja`, `varCorVermelho`.

## 6. Assets

- A faixa institucional **`Nav`** (PNG 1440×90 com a marca Braskem, byte a byte o mesmo recurso do Radar) foi portada como recurso real do app: arquivo em `Assets/Images/`, entrada em `References/Resources.json` e controle `Image` no cabeçalho de cada tela.
- Nenhuma foto, imagem de conteúdo, lista, conexão ou fonte de dados do Radar foi copiada.
- Os templates `htmlViewer` e `image` foram adicionados a `References/Templates.json` (o estilo `defaultHtmlViewerStyle` já existia no tema do SGC).

## 7. Canvas

Mantido em **1366 × 768**, `ScaleToFit`/`MaintainAspectRatio` inalterados. As proporções do Radar (1440 × 800) foram adaptadas ao canvas do SGC; nenhum metadado global de layout foi alterado.

## 8. Validações executadas

Round-trip: geração do `.msapp` → reabertura do pacote → releitura de todos os `Src/*.pa.yaml` e `Controls/*.json`.

Resultados (script `ferramentas/verify.py`, execução final — **0 erros, 0 avisos**):

- 8 telas presentes, nenhuma perdida.
- Paridade total entre `Src/*.pa.yaml` e `Controls/*.json` (mesmo conjunto de controles em cada tela).
- Fórmulas críticas comparadas controle a controle, propriedade a propriedade (`OnSelect`, `OnVisible`, `OnHidden`, `OnChange`, `Items`, `Text`, `Default`, `DefaultSelectedItems`, `DisplayMode`, `Visible`, `Tooltip`): nenhuma fórmula contendo `Patch`, `Navigate`, `Set`, `UpdateContext`, `Collect`, `Filter`, `LookUp`, `SortByColumns` ou `Reset` foi alterada.
- `App.OnStart`: bloco funcional original íntegro (`Refresh(SGC_*)`, coleções, `varModoSomenteLeitura`) + bloco de tema.
- Fontes de dados: `SGC_Pessoas`, `SGC_Competencias`, `SGC_Qualificacoes`, `SGC_Avaliacoes`, `SGC_Certificados` preservadas; nenhuma fonte ou referência `Radar_*` introduzida.
- Sanidade sintática de **todas** as propriedades de todas as telas: strings fechadas, parênteses balanceados, nenhum HTML fora de literal.
- Verificação de layout em 1366 × 768 para todos os controles de primeiro nível: nenhum estouro à direita, nenhuma invasão do rodapé, nenhum controle sobreposto ao menu lateral.
- Renderização real dos blocos HTML (cabeçalho, itens de menu, rodapé, título) em navegador — evidências em `PREVIEW_CABECALHO_RODAPE.png` e `PREVIEW_SHELL_SGC.png`.

## 9. Limitações reais (fatos, não hipóteses)

1. **Importação no ambiente não foi testada.** Não há `pac CLI` neste ambiente; o `.msapp` foi gerado com empacotamento equivalente ao do `pac canvas pack` (inclui `packed.json` com `LoadConfiguration.LoadFromYaml = true`, exatamente como o arquivo do Radar fornecido). A validação feita é estrutural e de round-trip, não uma importação real no Power Apps. **Teste em ambiente de desenvolvimento antes de atualizar o app de produção.**
2. **App Checker não foi executado** (depende do Studio). O `AppCheckerResult.sarif` do pacote é o do arquivo original e está desatualizado — será regravado no próximo salvamento no Studio.
3. **Recurso de imagem novo.** O cabeçalho passou a depender do recurso `Nav` (83 KB), incluído no pacote. Confirme no Studio, após a importação, que a imagem aparece nas 8 telas — é o único asset importado e o único ponto do pacote que depende do mecanismo de recursos do Power Apps.
4. **Os KPIs e os cards permanecem em controles nativos**, com o acabamento do Radar (fundo branco, raio 14, borda #D8E1EA, barra de situação 5 px, tipografia e paleta). A conversão dos números para HTML foi evitada de propósito: manteria a estética, mas reescreveria fórmulas de cálculo — risco desnecessário frente ao ganho.
5. O rótulo decorativo antigo do cabeçalho (`lblFaixa*`/`recHeader*`) foi mantido atrás do bloco HTML como fundo de segurança; é inerte.

## 10. Como usar

- `SGC_LCQ_RJ_VISUAL_RADAR.msapp` — abrir/importar direto no Power Apps Studio.
- `SGC_LCQ_RJ_VISUAL_RADAR_IMPORT.zip` — pacote de importação preservando `manifest.json`, identidade do app, logo e a dependência do conector SharePoint do pacote original (`SGC_LCQ_RJ_20260918093306.zip`). Use a opção **Atualizar** ao importar para manter o app existente.
- `SGC_LCQ_RJ_VISUAL_RADAR_FONTES.zip` — fontes desempacotadas usadas para gerar o `.msapp`.
- `ferramentas/` — scripts da migração (`payaml.py`, `jsonctl.py`, `ops.py`, `design.py`, `migrate.py`, `verify.py`, `pack.py`), reexecutáveis e auditáveis.

## 11. Próximos passos sugeridos

1. Importar em ambiente de teste e rodar o App Checker.
2. Percorrer os fluxos críticos: nova avaliação → rascunho → conclusão → cancelamento → modo somente leitura → histórico.
3. Conferir a leitura dos KPIs e da matriz de cobertura em tela real (1366 × 768 e resolução do parque).
4. Se aprovado, publicar e, opcionalmente, incluir a logomarca no cabeçalho.
