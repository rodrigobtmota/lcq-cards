# Correção pontual — `ComboBoxSample` na build 3d5cfb

**Status: `APROVADO_OFFLINE`** — importação no Studio: `PENDENTE_VALIDACAO_TENANT`

| Item | SHA-256 |
|---|---|
| Base (confirmada antes de qualquer alteração) | `3d5cfb3a455351cb085df2d6bae86d08a7ab82db8f656cb05964bf17b551a7ce` |
| **Nova build** `Radar_de_Liderancas_LCQ_V2_FINAL_BUILD_3D5CFB_CBX.msapp` | `98168d77c5d2fdb036c4e04c57c4f18ba43b6ac07ce4b9882aec02319661fe17` |
| Fontes `…_CBX_FONTES.zip` | `9c1c851f95dc6227481c0a9f03e14a8eb6487941d30e58ac73cb91d6ab975289` |

Base usada: exclusivamente o `.msapp` 3d5cfb anexado. O ZIP de entrega anexado junto, a build 6062bd e a r2 não foram usados.

## O que foi feito

1. `pac canvas unpack --layout SourceCode` da build 3d5cfb.
2. No `.msapr`, em `msapp/References/DataSources.json`, inserção da definição de `ComboBoxSample` **idêntica à do `.msapp` original** (`StaticDataSourceInfo`, `IsSampleData=true`, `IsWritable=false`, 15 linhas fictícias `Value1..3`). A posição respeita a ordem alfabética e a formatação do arquivo (CRLF, 2 espaços). O arquivo foi reserializado byte a byte antes da inserção.
3. `pac canvas pack --layout SourceCode --disable-load-from-yaml` → `pac canvas unpack`.

Nenhum `Src/*.pa.yaml`, `Controls/*.json` ou outro arquivo foi editado.

## Provas (após o round-trip)

| Requisito | Resultado |
|---|---|
| `Src/*.pa.yaml` byte a byte iguais à 3d5cfb | **11/11 idênticos** (no `.msapp` e no 2º unpack) |
| Única alteração funcional/estrutural | `References/DataSources.json`: **+15 linhas, 0 removidas**, todas do bloco `ComboBoxSample`. As outras 11 fontes têm definição idêntica. 102 de 103 arquivos idênticos. |
| Fórmula autoral usando `ComboBoxSample` | 0 (e 0 `SearchItems` em `Src`) |
| Os 4 `SearchItems` ocultos | `DataCardValue3`, `DataCardValue12`, `DataCardValueCriticidade`, `cmbResponsavelEquipamento` → fonte **disponível** |
| Os 4 ComboBox | `Items`, `DefaultSelectedItems`, `SearchFields` e `IsSearchable` inalterados: `Controls/*.json` e `Src` são idênticos à base |
| `RadioSample` | 0 ocorrências no pacote inteiro |
| `CustomGallerySample` / `DropDownSample` | Não reintroduzidas. Aparecem só nas definições de template (`Templates.json`), e nenhuma regra de controle as usa. |
| Referência ativa a fonte ausente | Nenhuma (varredura de todas as regras em `Controls/` e `Components/`) |
| Não reversão para 6062bd | Os 11 `Src` da 3d5cfb diferem da 6062bd. Na nova build, **11 são iguais à 3d5cfb e 0 iguais à 6062bd**. |
| Sintaxe e schema (2º unpack) | 6.348 fórmulas, 0 erros de sintaxe, 0 erros de schema. Igual à base. |

## Diferenças de contêiner geradas pelo PAC (sem efeito no app)

| Item | Explicação |
|---|---|
| `packed.json` (novo) | Grava `LoadFromYaml: false`. A 3d5cfb não tinha esse arquivo e é carregada pelos `Controls/*.json`; a opção `--disable-load-from-yaml` mantém esse mesmo modo de carga. |
| Separador de caminho no ZIP | A base usa `\`, o PAC grava `/`. O conteúdo dos arquivos é o mesmo. |
| `checksum.json` | Mantido sem alteração. Ele vem do empacotador que gerou a 3d5cfb e, portanto, não reflete o novo `DataSources.json`. Editá-lo à mão seria mexer em cache, o que você vetou. |

## Pendência de tenant

Importar a nova build, abrir no Studio e confirmar 0 erros: `PENDENTE_VALIDACAO_TENANT`. Se o Studio acusar algo relacionado ao `checksum.json`, o próximo passo é reempacotar sem esse arquivo, como decisão explícita sua.

Evidência completa: `prova_3d5cfb_cbx.txt`. Diff exato: `DIFF_EXATO_vs_3D5CFB.md`.
