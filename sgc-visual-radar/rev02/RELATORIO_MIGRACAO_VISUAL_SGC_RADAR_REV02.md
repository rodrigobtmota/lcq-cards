# REV02 — Endurecimento técnico e acabamento visual do SGC LCQ RJ

Data: 18/09/2026 · Escopo: correção pontual dos achados da auditoria. Não houve nova migração, redesenho de telas, mudança de regra de negócio nem de arquitetura de dados.

## 1. Base utilizada

| Papel | Arquivo |
|---|---|
| Base oficial da REV02 | Resultado da migração anterior (`SGC_LCQ_RJ_VISUAL_RADAR.msapp`), preservado em `build_rev01/` como linha de comparação |
| Referência funcional | `SGC_LCQ_RJ.msapp` (original), usado apenas para comparação de fórmulas |
| Referência visual | `Radar_de_Liderancas_LCQ_V2_CORRIGIDO_FINAL_V2.msapp`, usado apenas para leitura de padrões |
| Faixa do cabeçalho | Imagem institucional enviada por você (PNG 1440 × 90 real; 1536 × 96 é o tamanho de exibição) |

## 2. Correções executadas

| # | Achado da auditoria | O que foi feito |
|---|---|---|
| 1 | Botões do menu sem identificação acessível | `AccessibleLabel` explícito em 38 propriedades: `btnNav*` = `ThisItem.Rotulo`, CTA, Ajuda e botões de fechar do modal com rótulo textual |
| 2 | Variáveis de tema declaradas mas não usadas | 534 propriedades de cor passaram a usar `varCor*` |
| 3 | Padronização de raios não aplicada aos controles nativos | 340 propriedades de raio corrigidas (a regra da REV01 comparava o valor sem o prefixo `=` e, na prática, não alterava nada — falha corrigida) |
| 4 | Logomarca ausente | A faixa enviada **já contém o símbolo institucional**; registrada como recurso local do SGC. Nenhuma segunda logo foi inserida, para não duplicar a marca |
| 5 | `packed.json` declarava Pac CLI sem ter sido usado | Proveniência corrigida para `Custom Canvas Package Builder (scripts do projeto SGC LCQ RJ)`, versão `REV02`. `LoadConfiguration.LoadFromYaml` preservado |
| 6 | SARIF antigo apresentado como evidência | Mantido apenas por estrutura e declarado como desatualizado (seção 19) |
| 7 | Scripts citados mas ausentes do ZIP | `ferramentas/` agora existe de fato no pacote de fontes |
| 8 | Evidências citadas mas ausentes | `evidencias/` agora existe de fato, com renderizações derivadas dos fontes |
| + | **Achado novo, encontrado nesta rodada** | Colunas de posição fixa estouravam os containers estreitados pelo menu lateral (listas de Qualificações, Histórico, Cobertura e Detalhe). 106 propriedades `X`/`Width` reescaladas proporcionalmente. Verificação recursiva incorporada ao validador |

## 3. As 8 telas (todas preservadas)

`scrInicio` · `scrQualificacoes` · `scrDetalheQualificacao` · `scrNovaAvaliacao` · `scrAvaliacao` · `scrHistoricoAvaliacoes` · `scrModulos` · `scrCobertura`

## 4. Arquivos modificados

| Arquivo | Alteração |
|---|---|
| `Src/scr*.pa.yaml` (8) | Acessibilidade, variáveis de tema, raios, colunas, faixa |
| `Src/App.pa.yaml` | Bloco de tema (inalterado nesta rodada; funcional preservado) |
| `Controls/*.json` (9) | As mesmas alterações, aplicadas em paralelo pela camada `ops.Screen` |
| `References/Resources.json` | Recurso local `FaixaCabecalhoLCQ` (substitui o registro herdado do Radar) |
| `References/Templates.json` | Templates `htmlViewer` e `image` |
| `Assets/Images/a0ae92ce-…-9a967a99c149.png` | Faixa institucional (83 KB) |
| `packed.json` | Proveniência corrigida |

## 5 e 6. Volume de alteração (REV01 → REV02)

- **380 controles** tocados
- **1.034 propriedades visuais** alteradas, distribuídas em:

| Categoria | Propriedades |
|---|---|
| `AccessibleLabel` adicionados | 38 |
| Literais de cor → variáveis de tema | 534 |
| Raios padronizados | 340 |
| Colunas internas reescaladas (`X`/`Width`) | 106 |
| Faixa institucional (`Image`, `ImagePosition`, `AccessibleLabel`) | 16 |

Nenhuma outra categoria de alteração foi aceita: o validador reprova qualquer diferença REV01 → REV02 que não se enquadre nessas cinco.

## 7. Confirmação de `AccessibleLabel`

- 8 botões de item do menu lateral: `AccessibleLabel = ThisItem.Rotulo` (um por tela), com `OnSelect`, `Tooltip`, `Visible`, `DisplayMode`, `Fill`, `HoverFill` e `PressedFill` intactos.
- 6 CTAs "+ Nova avaliação": `"Iniciar nova avaliação"`.
- 8 botões "Ajuda": `"Abrir a ajuda desta tela"`.
- 16 botões de fechar do modal de ajuda: `"Fechar a ajuda"` / `"Fechar a janela de ajuda"`.

Verificação automática: nenhum `btnNav*` ou `btnAjuda*` sem `AccessibleLabel`.

## 8. Design tokens

| Variável | Valor | Ocorrências nos fontes |
|---|---|---|
| `varCorPrimaria` | `RGBA(14, 42, 74, 1)` | 72 |
| `varCorSecundaria` | `RGBA(28, 85, 130, 1)` | 145 |
| `varCorFundo` | `RGBA(245, 247, 250, 1)` | 10 |
| `varCorCard` | `RGBA(255, 255, 255, 1)` | 45 |
| `varCorTexto` | `RGBA(32, 42, 53, 1)` | 48 |
| `varCorTextoSuave` | `RGBA(101, 115, 132, 1)` | 101 |
| `varCorBorda` | `RGBA(216, 225, 234, 1)` | 115 |
| `varCorVerde` | `RGBA(46, 125, 50, 1)` | 6 |
| `varCorAmarelo` | `RGBA(202, 138, 4, 1)` | 5 |
| `varCorLaranja` | `RGBA(180, 83, 9, 1)` | 1 |
| `varCorVermelho` | `RGBA(185, 28, 28, 1)` | 4 |

O validador confere que cada variável é definida no `App.OnStart` exatamente com o valor que ela substituiu.

## 9. Substituições hardcoded → variáveis

534 propriedades, apenas em propriedades de cor (`*Fill`, `*Color`). **Não** foram tocados: fórmulas de cálculo, comparações, condicionais de regra de status, campos SharePoint, nem strings HTML (os blocos `HtmlViewer` continuam com CSS literal, por segurança de formato).

Branco → `varCorCard` só onde o branco é o fundo de um card institucional (container com borda e raio). Branco de texto e de outros usos permaneceu literal.

Literais remanescentes são intencionais: transparência (`RGBA(0,0,0,0)`), tons de badge/status (`#256B35`, `#A91515`, `#806000`, `#A14E08` e seus fundos) e tons auxiliares de lista, que não têm variável equivalente declarada.

## 10. Raios aplicados

| Valor | Uso | Controles |
|---|---|---|
| 14 px | Cards institucionais (containers e sobreposições que cobrem o card) | 42 |
| 13 px | Itens do menu lateral | 24 |
| 10 px | Botões e campos secundários | 68 |
| 18 px | Modais de ajuda | 8 |
| 0 px | Barras, divisores e elementos técnicos | 8 |

Badges pill, barras de progresso, acentos de card, divisores e ícones foram explicitamente excluídos da padronização.

## 11. Método usado para a faixa/logo

- Arquivo copiado para `Assets/Images/` com **nome próprio do SGC** (GUID derivado do namespace do projeto), não o identificador do Radar.
- Entrada em `References/Resources.json`: `Name = FaixaCabecalhoLCQ`, `ResourceKind = LocalFile`, `RootPath = ""` (sem URL externa, sem SAS, sem vínculo com o ambiente do Radar).
- Controle `Image` (`imgNav<Suf>`) no cabeçalho das 8 telas: `X=0`, `Y=0`, `Width=Parent.Width`, `Height=90`, atrás dos controles funcionais.
- O texto do cabeçalho é um `HtmlViewer` transparente sobre a faixa; o data URI SVG usado na versão anterior foi **removido** (o validador reprova a string `data:image` nos fontes).
- Como a faixa já traz o símbolo institucional, **nenhuma logo adicional** foi inserida.
- `ImagePosition = Stretch`: cobre toda a largura sem cortar o símbolo. Em 1366 px isso comprime a imagem em 5,1 % na horizontal (1440 → 1366), imperceptível em gradiente e onda. `Fill` cortaria ~37 px de cada lado, atingindo o símbolo; `Fit` deixaria faixa vazia de ~4,6 px na vertical.

## 12. Comparação de fórmulas funcionais

- **REV01 → REV02**: comparação propriedade a propriedade em todos os controles das 8 telas. Qualquer diferença fora das cinco categorias autorizadas (seção 5) é reprovada pelo validador. Resultado: **0 divergências**.
- **SGC original → REV02**: 113 fórmulas contendo `Patch`, `Navigate`, `Set`, `UpdateContext`, `Collect`, `Filter`, `LookUp`, `SortByColumns`, `Reset`, `With` ou `Concurrent` conferidas em `OnSelect`, `OnVisible`, `OnHidden`, `OnChange`, `Items`, `Text`, `Default`, `DefaultSelectedItems`, `DisplayMode`, `Visible` e `Tooltip` — **todas idênticas**.

## 13. Comparação Src × Controls

Para cada tela: mesmo conjunto de controles, sem nomes duplicados e sem referência órfã (o campo `Parent` de cada nó do JSON confere com o pai real). Resultado: **0 divergências**.

## 14. Fontes de dados

`References/DataSources.json` idêntico ao do aplicativo original. Presentes: `SGC_Pessoas`, `SGC_Competencias`, `SGC_Qualificacoes`, `SGC_Avaliacoes`, `SGC_Certificados`.

## 15. Ausência de `Radar_*`

Busca em `Src/*.pa.yaml` e `References/*.json` por `Radar_`, `Nav_bg`, o GUID do asset do Radar, `blob.core.windows.net` e `data:image`: **nenhuma ocorrência**. `Assets/Images/` contém exatamente um arquivo, o da faixa registrada localmente.

## 16. Assets introduzidos

| Asset | Origem | Tamanho |
|---|---|---|
| `FaixaCabecalhoLCQ` (`a0ae92ce-…png`) | Imagem institucional enviada por você | 83 KB |

## 17. Ferramentas realmente incluídas

Em `ferramentas/`, dentro do pacote de fontes — todas foram usadas nesta transformação:

| Script | Função |
|---|---|
| `payaml.py` | Parser/serializador de `*.pa.yaml` (round-trip byte a byte verificado) |
| `jsonctl.py` | Edição de `Controls/*.json` |
| `ops.py` | Camada que aplica cada operação nas duas representações |
| `design.py` | Tokens e blocos HTML do design system |
| `migrate.py` | Pipeline da migração |
| `rev02.py` | Correções desta revisão |
| `verify.py` | Validação contra o SGC original |
| `verify_rev02.py` | Validação REV01 → REV02 e checagens estruturais |
| `render_evidencias.py` | Geração das evidências a partir dos fontes |
| `pack.py`, `pack_rev02.py` | Empacotamento |
| `proto_*.json`, `faixa_cabecalho_lcq.png` | Insumos (protótipos de controle/template e a imagem) |

Reprodução: `python3 ferramentas/migrate.py && python3 ferramentas/verify.py && python3 ferramentas/verify_rev02.py && python3 ferramentas/pack_rev02.py` (requer as pastas de entrada do projeto).

## 18. Evidências realmente incluídas

Em `evidencias/`: `PREVIEW_CABECALHO_RODAPE_REV02.png`, `PREVIEW_scrInicio_REV02.png`, `PREVIEW_scrQualificacoes_REV02.png`, `PREVIEW_scrAvaliacao_REV02.png`, `PREVIEW_scrCobertura_REV02.png`, os `.html` que as originam e um `LEIA-ME.md`.

São renderizações geradas **a partir de `Src/*.pa.yaml`** (geometria, cores, raios, tipografia, textos estáticos e HTML reais; a faixa é o arquivo real do recurso). **Não são capturas do Power Apps**: fora do Studio não há como resolver dados do SharePoint nem `ThisItem` de galerias ligadas a dados — esses valores aparecem como `—`.

## 19. O que foi e o que não foi validado

**Validado por inspeção automatizada neste ambiente**

- Estrutura do ZIP e round-trip do `.msapp` (reabertura e releitura de todos os fontes).
- Paridade `Src` × `Controls`, ausência de duplicados e de referência órfã.
- Comparação de fórmulas REV01 → REV02 e SGC original → REV02.
- Fontes de dados e ausência de `Radar_*`.
- Registro do recurso local e existência física do arquivo em `Assets/Images/`.
- Sintaxe estrutural das propriedades (strings fechadas, parênteses balanceados, nenhum HTML fora de literal).
- Geometria calculada em 1366 × 768, inclusive **recursiva** (nenhum controle estoura o container que o contém, o menu, o cabeçalho, o rodapé ou o canvas).
- Canvas mantido em 1366 × 768.
- Coerência entre cada `varCor*` e o valor definido no `App.OnStart`.

**Não validado neste ambiente**

- Importação real no Power Apps Studio.
- Execução no runtime.
- App Checker. **O App Checker não foi executado após a REV02. O arquivo SARIF existente pertence a uma versão anterior e será atualizado pelo Power Apps Studio após abertura/salvamento.** Ele não é evidência desta versão.
- Publicação.
- Conexão online com o SharePoint.

## 20. Validação no Studio (o que conferir)

1. Importar `SGC_LCQ_RJ_VISUAL_RADAR_REV02_IMPORT.zip` em ambiente de desenvolvimento, opção **Atualizar**.
2. Conferir a faixa institucional nas 8 telas, sem deformação e sem marca duplicada.
3. Rodar o App Checker e salvar (isso regrava o SARIF).
4. Percorrer: nova avaliação → rascunho → conclusão → cancelamento → modo somente leitura → histórico → detalhe da qualificação → cobertura.
5. Conferir as listas de Qualificações e Histórico na largura real (colunas reescaladas nesta revisão).
6. Testar navegação por teclado no menu lateral (leitor de tela deve anunciar o rótulo do item).

## Observação técnica pendente (pré-existente, não introduzida pela REV02)

Nos cards de KPI da tela inicial, o rótulo mais longo ("Pessoas em escopo técnico") não cabe em uma linha na largura do card, com o `Height` de 20 px herdado do aplicativo original — o texto é cortado. O comportamento já existia no SGC antes da migração. Corrigir exige mudar altura/posição do rótulo ou encurtar o texto, o que é decisão sua; por isso não foi alterado nesta revisão.
