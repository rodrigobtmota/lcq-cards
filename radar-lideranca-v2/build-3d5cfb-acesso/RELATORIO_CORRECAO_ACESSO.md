# Correção — tela presa em "Carregando acesso ao Radar…"

**Status: `APROVADO_OFFLINE`** · abertura no Studio: `PENDENTE_VALIDACAO_TENANT`

| Item | SHA-256 |
|---|---|
| **Nova build** `Radar_de_Liderancas_LCQ_V2_FINAL_BUILD_3D5CFB_CBX_ACESSO.msapp` | `a1c72acfb7bed2fe703eacfa73bf9abf60aa7483d387b3b38fac4990314a2ac5` |
| Fontes `…_ACESSO_FONTES.zip` | `fca4d67eefa148fcf90c93f0a7ccf58a12e264f6b0deef625622bcd789b7078b` |
| Base | CBX `98168d77…`, que é a 3d5cfb com `ComboBoxSample` |

## Causa (evidência no arquivo)

Na linhagem 3d5cfb, o conteúdo das 7 telas fica oculto por `Coalesce(varCargaInicialConcluida, false) && varUsuarioCadastrado …`. A variável só passa a `true` no **último comando** do `App.OnStart`.
Enquanto o `OnStart` não roda até o fim, o `Coalesce(…, false)` trata "nunca executado" (vazio) igual a "carregando" (`false`). O resultado é exatamente a imagem: o container principal fica oculto (a faixa azul do Header está dentro dele, por isso o título branco aparece sobre fundo branco) e só o aviso "Carregando acesso ao Radar…" fica visível. Isso acontece no Studio quando o `OnStart` não foi executado, ainda está rodando ou aguarda a autorização das conexões após importar o arquivo.

Foram descartadas outras causas: o `OnStart` está íntegro (0 erros de sintaxe), `Controls/*.json` e YAML são coerentes (5.836 regras em comum, 0 divergentes) e não há construção inválida no escopo do App.

## Correção (mínima)

Apenas as **37 regras `Visible`** do bloqueio de acesso, nas 7 telas, passam a distinguir os dois estados:

| Estado de `varCargaInicialConcluida` | Antes | Depois |
|---|---|---|
| vazio (`OnStart` não executado, ex.: editor) | tudo oculto + "Carregando…" | **layout visível**; aviso oculto; painéis e ajudas seguem as próprias variáveis |
| `false` (carregando, em runtime) | oculto + "Carregando…" | **idêntico** |
| `true` (acesso resolvido) | conteúdo conforme cadastro/perfil, ou "Sem acesso…" | **idêntico** |

Ficaram sem alteração: os 7 textos dos avisos, o `App.OnStart`, o `OnVisible` do Cockpit, a `TelaDecisoesEncaminhamentos` (que não tem esse bloqueio), `ComboBoxSample` e todo o resto.

**Segurança:** a proteção de runtime continua fechada. O `OnStart` grava `varCargaInicialConcluida = false` no seu primeiro comando, e as coleções e o menu só são preenchidos por ele. No estado vazio, portanto, não há dados carregados para exibir.

## Provas

| Verificação | Resultado |
|---|---|
| Equivalência no interpretador oficial do Power Fx: fórmula antiga × nova, todas as combinações das variáveis, estados `false` e `true` | **810/810 PASS** (`evidencias/gate_tests_result.txt`) |
| Estado vazio | Conteúdo segue as próprias variáveis e o aviso fica oculto (incluído nos 810) |
| Arquivos × CBX | 8 diferentes: 7 `Src` com as regras + `packed.json`. Os demais, idênticos byte a byte. CRLF preservado. |
| Arquivos × 3d5cfb | Os mesmos 8 + `DataSources.json` (a `ComboBoxSample` da entrega anterior). `App.pa.yaml`, `_EditorState`, Header e `TelaDecisoesEncaminhamentos` são idênticos à 3d5cfb. |
| PAC pack → unpack | `Src` idêntico; 6.348 fórmulas com 0 erros de sintaxe; schema e referências com 0 erros |
| `ComboBoxSample` / `RadioSample` | presente / 0 ocorrências |

**Modo de carga:** `packed.json` passa a `LoadFromYaml: true`, o pack padrão do PAC e o caminho suportado para o Studio aplicar fórmulas alteradas no YAML. Isso é seguro aqui porque `Controls/*.json` e YAML desta build são coerentes.

## No Studio

1. Importe a nova build e autorize as conexões (SharePoint e fluxo) quando o Studio pedir.
2. O layout das telas fica visível para edição sem depender do `OnStart`.
3. Para ver dados e testar o perfil, use **App › … › Executar OnStart** ou o modo de reprodução (F5). Se o aviso "Carregando…" continuar depois disso, o `OnStart` não está terminando, normalmente por conexão não autorizada. Nesse caso, me envie a mensagem de erro exibida.
