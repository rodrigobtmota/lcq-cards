# REV02.2 — Correção bloqueante PA2108 (`AccessibleLabel` em `Classic/Button@2.2.0`)

Data: 18/09/2026 · Base única: `SGC_LCQ_RJ_VISUAL_RADAR_REV02_1.msapp`. Escopo estritamente pontual: eliminar o erro observado na importação real. Nenhuma melhoria visual, nenhuma refatoração, nenhum outro item aproveitado.

## 1. O que aconteceu

A REV02 e a REV02.1 adicionaram `AccessibleLabel` a 38 botões clássicos, para dar identificação acessível ao menu lateral e aos botões sem rótulo visível.

**A importação real no Power Apps revelou o erro `PA2108: Unknown property 'AccessibleLabel' for control type 'Classic/Button@2.2.0'`** — 38 erros, um por botão. Essa propriedade não é aceita para esse tipo no Source Code schema utilizado, e o pacote não importava.

Confirmação estrutural feita aqui, no próprio aplicativo original: o template `button` (versão 2.2.0) **não possui** a regra `AccessibleLabel`, enquanto `rectangle`, `text`, `combobox`, `gallery` e `image` a possuem com valor padrão. O erro era, portanto, legítimo e previsível — e os validadores offline não o pegaram, porque conferiam a *presença* da propriedade, nunca se o tipo de controle a aceita.

## 2. Correção aplicada

| Alvo | Ação |
|---|---|
| **38 `Classic/Button@2.2.0`** | `AccessibleLabel` **removido**, em `Src/*.pa.yaml` **e** em `Controls/*.json` (regra e `ControlPropertyState`). Nenhuma ação, cor, tamanho ou posição alterada |
| **8 `btnNav*`** (itens do menu) | `Text` passou de `""` para `ThisItem.Rotulo`; `Tooltip` continua `ThisItem.Rotulo`. `Color`, `HoverColor` e `PressedColor` seguem `RGBA(0, 0, 0, 0)`, então o texto permanece invisível — a apresentação continua sendo do `HtmlViewer`, mas o botão agora tem conteúdo textual real para leitores de tela |
| **8 `btnAjudaX*`** (fechar, `Text = "✕"`) | `AccessibleLabel` removido e `Tooltip = "Fechar a ajuda"` garantido. Símbolo e `OnSelect` intactos |
| **6 `btnNavNova*`** (+ Nova avaliação), **8 `btnAjuda<Tela>`** (Ajuda), **8 `btnAjudaFechar*`** (Entendi) | Apenas remoção do `AccessibleLabel`. O `Text` visível já cumpre o papel de rótulo acessível |
| **8 `Image@2.2.3`** (`imgNav*`) e **8 `Gallery@2.15.0`** (`galNav*`) | `AccessibleLabel` **mantido** — tipos que aceitam a propriedade e que não apareceram nos erros |

Nenhuma versão de controle foi alterada: os botões continuam `Classic/Button@2.2.0`. Nenhum controle foi recriado, substituído ou modernizado.

## 3. `AccessibleLabel` — situação atual (não são mais 38 em botões)

| Tipo de controle | Quantidade | Observação |
|---|---|---|
| `Classic/Button@2.2.0` | **0** | removidos nesta revisão (PA2108) |
| `Image@2.2.3` (`imgNav*`) | 8 | `"Faixa institucional do cabecalho"` |
| `Gallery@2.15.0` (`galNav*`) | 8 | `"Menu principal do SGC LCQ RJ"` |

A acessibilidade dos botões clássicos passou a ser atendida por `Text` + `Tooltip`, que são propriedades válidas para o tipo.

## 4. Teste bloqueante (estrutural, por tipo de controle)

`ferramentas/verify_rev022.py` percorre cada controle, lê o **tipo** e reprova qualquer `Classic/Button@2.2.0` que tenha `AccessibleLabel` — nas duas representações, inclusive no `ControlPropertyState` do JSON. O script sai com código 1 em caso de falha.

Saída real, executada a partir do pacote de fontes entregue:

```
Classic/Button@2.2.0 com AccessibleLabel: 0 (Src) / 0 (Controls)
AccessibleLabel mantido em Gallery@2.15.0    : 8
AccessibleLabel mantido em Image@2.2.3       : 8
botoes de menu com Text/Tooltip = ThisItem.Rotulo: 8
AccessibleLabel removido  : 38
Text do menu              : 8
Tooltip de fechar         : 8
paridade Src x Controls conferida
formulas funcionais identicas ao SGC original: 113
OnSelect conferidos (identicos ao original): 81

ERROS (0):
```

## 5. Validadores corrigidos

A lacuna apontada foi fechada em dois pontos:

1. **`verify_rev022.py`** (novo, bloqueante): reprova `Classic/Button@2.2.0` + `AccessibleLabel`; confere `Text` e `Tooltip` dos 8 `btnNav*` e as três cores transparentes; confere `OnSelect` de **todos** os 81 botões contra o SGC original; confere paridade `Src` × `Controls`; confere as 113 fórmulas funcionais; reprova qualquer controle novo ou removido.
2. **`verify_rev02.py`** (atualizado): deixou de exigir `AccessibleLabel` em botões — agora exige o contrário (nenhum em botão clássico) e passou a reconhecer `Text`/`Tooltip` como a forma válida de rótulo no menu. Sem isso, o pacote seguiria com um script que falha.

## 6. Resultado das validações (execução real, a partir do ZIP entregue, em pasta limpa)

| Script | Comparação | Resultado |
|---|---|---|
| `verify.py` | REV02.2 × SGC original | **0 erros, 0 avisos** |
| `verify_rev02.py` | REV02.2 × REV01 entregue | **0 erros** — 1.062 propriedades visuais em 379 controles |
| `verify_rev02.py build_rev01_prefaixa` | REV02.2 × REV01 anterior à faixa | **0 erros** |
| `verify_rev022.py` | REV02.2 × REV02.1 | **0 erros** (saída acima) |
| `pack_rev022.py` | regeração do pacote | `.msapp` **byte a byte idêntico** nos 30 arquivos internos |

## 7. Critérios de aceite conferidos

| Critério | Resultado |
|---|---|
| `Classic/Button@2.2.0` com `AccessibleLabel` | **0** |
| 8 telas | presentes, mesmos nomes |
| Controles | 563 antes, 563 depois — **nenhum novo, nenhum removido** |
| IDs (`MetaDataIDKey`), templates e versões | **nenhum alterado** |
| Ocorrências de `Radar_` | **0** |
| `References/DataSources.json` | **idêntico** ao do aplicativo original |
| 113 fórmulas funcionais (`Patch`, `Navigate`, `Set`, `Filter`, `LookUp`, `UpdateContext`, `Reset`, `With`, `Concurrent`, `Collect`) | **idênticas** |
| `OnSelect` de todos os botões | **idênticos** ao original (81 conferidos) |
| `Src` × `Controls` | equivalentes |

## 8. REV02.1 preservada

Faixa institucional local (`FaixaCabecalhoLCQ`), 8 telas, menu lateral, reflow dos KPIs e das ações rápidas, variáveis de tema, raios, correção das colunas das listas, canvas 1366 × 768, `DataSources`, IDs e `App.OnStart` — tudo intacto. Regras de qualificação, avaliação, rascunho, conclusão, cancelamento, histórico e cobertura não foram tocadas.

A única diferença visual possível é no menu lateral: o `Text` do botão agora existe, mas é renderizado com cor totalmente transparente, sobre o `HtmlViewer` que desenha o item. Evidência: `evidencias/PREVIEW_scrInicio_REV02_2.png`.

## 9. Validado aqui × dependente do Studio

**Executado neste ambiente:** round-trip do `.msapp`; checagem estrutural PA2108 por tipo de controle nas duas representações; comparação propriedade a propriedade contra REV02.1, REV01 e REV01 pré-faixa; comparação das fórmulas contra o SGC original; paridade `Src` × `Controls`; `DataSources`; ausência de `Radar_*`; IDs e templates; reprodução completa do pipeline a partir do ZIP entregue.

**Continua dependendo do Power Apps:** a importação em si. Esta revisão corrige o erro `PA2108` que foi observado e reproduzido estruturalmente aqui, mas **não posso afirmar que a importação passa** — só a sua tentativa no Studio confirma isso. Se aparecer outro `PA####` para propriedade/tipo diferente, me mande a lista: o validador já está preparado para receber a regra por tipo de controle. Também seguem fora deste ambiente: execução no runtime, App Checker (o SARIF do pacote é de versão anterior e será regravado pelo Studio), publicação e conexão com o SharePoint.

## 10. Conferir no Studio

1. Importar `SGC_LCQ_RJ_VISUAL_RADAR_REV02_2_IMPORT.zip`, opção **Atualizar**.
2. Confirmar que não há mais erros `PA2108`.
3. Menu lateral: aparência idêntica (o texto do botão deve continuar invisível) e navegação funcionando nas 5 áreas.
4. Leitor de tela / navegação por teclado: o item do menu deve anunciar o rótulo.
5. Percorrer: nova avaliação → rascunho → conclusão → cancelamento → somente leitura → histórico → detalhe → cobertura.
