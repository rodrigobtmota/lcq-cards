# REV02.1 — Correção pontual sobre a REV02

Data: 18/09/2026 · Base única: `SGC_LCQ_RJ_VISUAL_RADAR_REV02.msapp`. Nenhuma migração refeita, nenhuma regra de negócio ou fórmula funcional alterada, nenhuma tela redesenhada.

## 1. Correções executadas

| # | Pedido | O que foi feito |
|---|---|---|
| 1 | Reprodutibilidade das ferramentas | `design.py` não carrega mais `navbg_datauri.txt` — a dependência foi **removida do pipeline**, já que a REV02 usa a faixa como recurso local e não mais como data URI. Além disso, o pacote de fontes passou a conter as **entradas** (`entrada/sgc`, `entrada/pkg`, `entrada/build_rev01`, `entrada/build_rev01_prefaixa`), um resolvedor de caminhos (`caminhos.py`) e o `REPRODUZIR.md`. Os comandos documentados foram executados a partir do ZIP entregue, em pasta limpa (seção 3) |
| 2 | `verify_rev02.py` reconhecer todas as alterações autorizadas | Passou a aceitar explicitamente: inclusão de **1** controle `imgNav*` por tela (mais de um é erro), remoção do `data:image` do `HtmlText` dos `htmlCabecalho*`, `Image = FaixaCabecalhoLCQ`, `ImagePosition`, `AccessibleLabel` e geometria da imagem, alterações de `Fill`/`HoverFill`/`PressedFill`/`Color`/`BorderColor` dos `btnAjuda*`, e o reflow de rótulos da tela inicial. A linha de base virou parâmetro de linha de comando |
| 3 | Textos cortados na tela inicial | 50 propriedades de geometria ajustadas em 30 controles, sem alterar um único texto ou fórmula |
| 4 | Faixa institucional | Avaliado e **mantido `ImagePosition.Stretch`**, com a justificativa técnica na seção 5 |

## 2. Reflow da tela inicial (item 3)

Apenas `X`/`Y`/`Width`/`Height`. A altura dos cards (136 px nos KPIs, 160 px nas ações) **não mudou**, e os cinco KPIs seguem alinhados.

| Controle | Antes | Depois |
|---|---|---|
| `lblCard*Titulo` (5) | `Y=16`, `H=20` | `Y=14`, `H=36`, `Width=Parent.Width - 40` — cabem duas linhas ("Pessoas em escopo técnico", "Minhas avaliações abertas") |
| `lblQtd*` (5) | `Y=38`, `H=46` | `Y=52`, `H=46` |
| `lblKpiLegenda*` (5) | `Y=Parent.Height - 42`, `H=36` | `Y=Parent.Height - 36`, `H=32` |
| `lblAcao*Titulo` (5) | `Y=20`, `H=28` | `Y=18`, `H=28` |
| `lblAcao*Texto` (5) | `Y=56`, `H=66`, `Width=Parent.Width - 72` | `Y=50`, `H=80`, `Width=Parent.Width - 40` — os cinco textos descritivos cabem por inteiro |
| `icoAcao*` (5) | `Y=Parent.Height - 38` | `Y=Parent.Height - 32` |

Evidência: `evidencias/PREVIEW_scrInicio_REV02_1.png`.

## 3. Resultado real dos scripts (executados a partir do ZIP entregue)

Sequência executada em pasta limpa, após descompactar `SGC_LCQ_RJ_VISUAL_RADAR_REV02_1_FONTES.zip`, sem nenhum ajuste manual e sem arquivo ausente:

```
python3 ferramentas/migrate.py
python3 ferramentas/verify.py
python3 ferramentas/verify_rev02.py
python3 ferramentas/verify_rev02.py build_rev01_prefaixa
python3 ferramentas/pack_rev021.py
```

**Saída real de `verify_rev02.py` (base: REV01 entregue):**

```
base -> REV02
  AccessibleLabel adicionados : 38
  literais -> variaveis       : 534 propriedades
  raios padronizados em 14    : 340 propriedades
  colunas internas reescaladas: 106 propriedades
  faixa institucional         : 16 propriedades/controles
  cabecalho sem data URI      : 0 propriedades
  contraste do botao Ajuda    : 0 propriedades
  reflow de rotulos (inicio)  : 50 propriedades
  controles tocados           : 387
  propriedades visuais mudadas: 1084
formulas funcionais identicas ao SGC original: 113

ERROS (0):
```

**Saída real com a base anterior à faixa** (`build_rev01_prefaixa`, recuperada do histórico do repositório): **1.108 propriedades**, incluindo `cabecalho sem data URI: 8` e `contraste do botao Ajuda: 24` — **ERROS (0)**.

**`verify.py` (REV02.1 × SGC original):** ERROS (0), AVISOS (0).

**Contagem oficial desta revisão: 1.084 propriedades visuais em 387 controles** (o relatório da REV02 trazia 1.034; a diferença são as 50 propriedades do reflow). Nenhum número deste relatório foi estimado: todos vêm da saída dos scripts entregues.

**Reprodutibilidade verificada:** o `.msapp` regerado dentro do teste é **byte a byte idêntico** ao entregue nos 30 arquivos internos (só os carimbos de data/hora do ZIP diferem).

## 4. Correções que o verificador agora reconhece explicitamente

Categorias autorizadas — qualquer diferença fora delas é reprovada:

1. `AccessibleLabel` novo em `btnNav*` / `btnAjuda*`.
2. Literal de cor → variável de tema (conferindo o valor contra o `App.OnStart`).
3. Colunas fixas reescaladas (`X`/`Width` numéricos, sempre para valor menor ou igual).
4. Raio de card/botão para 14 ou 10.
5. Faixa institucional: até **um** controle `imgNav*` novo por tela, `Image`, `ImagePosition`, `AccessibleLabel` e geometria.
6. `HtmlText` do cabeçalho perdendo o `data:image` (fundo passa a ser o `imgNav*`).
7. Contraste do botão Ajuda sobre a faixa.
8. Reflow de rótulos da tela inicial (somente geometria de `lblCard*`, `lblQtd*`, `lblKpiLegenda*`, `lblAcao*`, `icoAcao*`).

## 5. Faixa institucional — decisão mantida (item 4)

**Mantido o asset original 1440 × 90 com `ImagePosition.Stretch`.** Motivo técnico verificado nos metadados do próprio aplicativo:

- `Properties.json` traz `DocumentLayoutScaleToFit = False`. Com isso o aplicativo **não** trabalha numa largura fixa: `Parent.Width` acompanha a janela do navegador. Um asset preparado em 1366 px só seria pixel-perfeito exatamente nessa largura e continuaria esticado em 1920 px (caso mais comum) ou em qualquer outra.
- O ganho seria, portanto, restrito a uma única largura, ao custo de descartar 74 px do desenho em todas as demais.
- A deformação atual é pequena e mensurável: em 1366 px, 5,1 % de compressão horizontal (1440 → 1366); o símbolo institucional passa de 21 px para ~19,9 px de largura — cerca de 1 px.
- `Fill` foi descartado: recorta ~37 px de cada lado e atinge o símbolo à esquerda. `Fit` foi descartado: deixa ~4,6 px de faixa vazia na vertical.

Se em algum momento o aplicativo passar a operar em largura fixa, a troca por um asset recortado é de uma linha (`rev02.registrar_faixa`).

## 6. O que não foi alterado

8 telas, nomes de tela, `References/DataSources.json` (`SGC_Pessoas`, `SGC_Competencias`, `SGC_Qualificacoes`, `SGC_Avaliacoes`, `SGC_Certificados`), IDs existentes, e todas as fórmulas com `Patch`, `Navigate`, `Set`, `Filter`, `LookUp`, `UpdateContext`, `Reset`, `With` e `Concurrent` — 113 delas conferidas uma a uma contra o SGC original e **idênticas**. Regras de qualificação, avaliação, cobertura, histórico, rascunho, conclusão e cancelamento intocadas. Canvas em 1366 × 768.

## 7. Validações realmente executadas neste ambiente

- Round-trip do `.msapp` (gerar → reabrir → reparsear `Src` e `Controls`).
- Paridade `Src` × `Controls`, sem controle duplicado e sem referência órfã (`Parent` confere com o pai real).
- Comparação propriedade a propriedade contra **duas** linhas de base (REV01 entregue e REV01 pré-faixa).
- Comparação de fórmulas funcionais contra o SGC original.
- `DataSources` idêntico; nenhuma ocorrência de `Radar_`, `Nav_bg`, GUID do asset do Radar, `blob.core.windows.net` ou `data:image` nos fontes.
- Recurso `FaixaCabecalhoLCQ` registrado como `LocalFile`, `RootPath` vazio, arquivo presente em `Assets/Images/`.
- Sintaxe estrutural de todas as propriedades (strings fechadas, parênteses balanceados, nenhum HTML fora de literal).
- Geometria em 1366 × 768, **recursiva**: nenhum controle estoura o container que o contém, o menu, o cabeçalho, o rodapé ou o canvas.
- Coerência de cada `varCor*` com o valor definido no `App.OnStart`.
- Execução completa do pipeline a partir do ZIP entregue, em pasta limpa.

## 8. Limitações que continuam dependendo do Power Apps Studio

- **Importação real** do pacote — não executada aqui.
- **Execução no runtime** e comportamento com dados reais do SharePoint — não executados aqui.
- **App Checker** — não executado após a REV02.1. O `AppCheckerResult.sarif` do pacote pertence a uma versão anterior e será regravado pelo Studio na primeira abertura/salvamento. Ele não é evidência desta versão.
- **Publicação** e conexão online com o SharePoint — não executadas aqui.
- **Renderização tipográfica final**: as evidências são geradas em navegador a partir dos fontes; a quebra de linha real dos rótulos no Power Apps pode variar em 1–2 px conforme a fonte instalada. O reflow da seção 2 foi dimensionado com folga, mas a conferência definitiva é no Studio.

## 9. Conferir no Studio

1. Importar `SGC_LCQ_RJ_VISUAL_RADAR_REV02_1_IMPORT.zip` em ambiente de desenvolvimento, opção **Atualizar**.
2. Tela inicial: conferir que os cinco títulos de KPI e os cinco textos das ações rápidas aparecem completos.
3. Conferir a faixa institucional nas 8 telas, sem marca duplicada.
4. Rodar o App Checker e salvar.
5. Percorrer: nova avaliação → rascunho → conclusão → cancelamento → somente leitura → histórico → detalhe → cobertura.
6. Testar navegação por teclado no menu lateral.
