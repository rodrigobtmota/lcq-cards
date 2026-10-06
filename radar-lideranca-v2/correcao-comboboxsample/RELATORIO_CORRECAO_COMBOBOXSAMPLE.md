# Correção pontual — dependência de `ComboBoxSample` nos Classic/ComboBox

**Status: `APROVADO_OFFLINE`** (sem alteração funcional; importação no Studio: `PENDENTE_VALIDACAO_TENANT`)

| Item | Valor |
|---|---|
| Nova build | `Radar_de_Liderancas_LCQ_V2_VALIDADO_FINAL_r2.msapp` — SHA-256 `333525f28d1383252bca2f8cdb9bd65a08d95b95f0f4c7f21c66eb6235067e82` |
| Fontes | `Radar_de_Liderancas_LCQ_V2_FONTES_VALIDADO_FINAL_r2.zip` — SHA-256 `a96617d3415572bb522f9109290aac4a22cbd6fa011368ce4444a92911ca04fc` |
| Build anterior entregue | `6062bd18…` (commit `fcec96a`) |

## 1. Divergência com o relato

A build citada (`3d5cfb…`) **não é a que entreguei**. Na build entregue (`6062bd18…`), `ComboBoxSample` **não** havia sido removida de `References/DataSources.json`. Ela foi mantida de propósito, como consta no relatório anterior (seção 2, item 16). Por isso, a inconsistência "regra presente com a fonte ausente" não existe nessa build. A análise abaixo vale para qualquer build derivada dos mesmos fontes.

## 2. Origem da regra

A regra vem da **definição oficial do controle `combobox` 2.4.0** da Microsoft, embutida em `References/Templates.json`. Não foi escrita pelo app:

| Propriedade do template | Definição |
|---|---|
| `SearchItems` | `hidden="true"` · `defaultValue="Search(ComboBoxSample, Self.SearchText, Value1)"` |
| `Items` | `<appMagic:sampleDataSource name="ComboBoxSample">` (o template declara essa fonte como sua amostra) |
| `DefaultSelectedItems` | padrão `First(ComboBoxSample)`, sobrescrito nos 4 controles |

Como `SearchItems` é **oculta**, ela não aparece no painel nem na barra de fórmulas do Studio, e o `pa.yaml` não a grava. A cada carga do YAML, o Studio reaplica o valor padrão do template e regenera `Controls/*.json` com essa regra. Os `Controls/*.json` são cache: com `LoadFromYaml: true`, eles não são a fonte.

## 3. Decisão

Não existe método suportado (Studio ou PAC) para sobrescrever uma propriedade oculta de template. Além disso, o template declara `ComboBoxSample` como fonte de amostra do controle. Remover a fonte só faria o Studio reinjetá-la ou acusar referência quebrada.
**Decisão: manter `ComboBoxSample` como fonte interna do Classic/ComboBox.** Ela já estava presente, então não houve "restauração" nem alteração de fontes. Nenhuma outra fonte Sample foi reintroduzida (`RadioSample` continua removida).

## 4. Prova de que não interfere nos dados reais

| Verificação | Resultado |
|---|---|
| Tipo da fonte | `StaticDataSourceInfo`, `IsSampleData=True`, `IsWritable=False`. São 15 linhas fictícias embutidas (`Value1..Value3`). |
| Conexão real | Não aparece em `LocalConnectionReferences`. Não faz chamada ao SharePoint nem a outro serviço. |
| Uso em fórmulas do app (`Src`) | 0 ocorrências de `ComboBoxSample` e de `SearchItems`. Nenhum `Patch`, `Collect`, `Refresh` ou `Filter` sobre ela. |
| Os 4 ComboBox | `Items`, `DefaultSelectedItems` e `SearchFields` estão explícitos e apontam para fontes reais (detalhe abaixo). `IsSearchable` usa o padrão (true). |
| Comparação com o original em produção | Mesmas 4 regras e definição de `ComboBoxSample` **idêntica** ao `.msapp` original. A experiência dos ComboBox não muda. |

| Controle | Items | SearchFields | DefaultSelectedItems |
|---|---|---|---|
| TelaDemandas.DataCardValue3 | `Choices([@Radar_Demandas].Responsavel)` (Pessoa) | `["Claims"]` | `Parent.Default` |
| TelaDemandas.DataCardValue12 | `Choices(Radar_Demandas.Status)` | `["Value"]` | LookUp "Aberta" em Novo / `Parent.Default` |
| TelaDemandas.DataCardValueCriticidade | `Choices(Radar_Demandas.Criticidade)` | `["Value"]` | `Parent.Default` |
| TelaEquipamentos.cmbResponsavelEquipamento | Choices de `ResponsavelAcompanhamento` (Pessoa), ordenado | `["DisplayName","Email"]` | Por e-mail do responsável |

## 5. Verificação após PAC pack → unpack (r2)

| Verificação | Resultado |
|---|---|
| Round-trip | `Src` idêntico; sintaxe 6.391 fórmulas / 0 erros; schema 0 erros; referências 0 problemas |
| Diferença r2 × build anterior | Só `packed.json`, que contém o horário do empacotamento. O conteúdo funcional é idêntico. |
| Varredura no `.msapp` inteiro (Src, Controls, Components, References, 1.131 blocos DynamicProperties, Templates) | `ComboBoxSample`: Controls 364 (3) e 489 (1), DataSources, Templates. `RadioSample`: **0**. `CustomGallerySample` / `DropDownSample`: só DataSources e Templates. |
| Regras ativas que dependem de fonte Sample **ausente** | **Nenhuma** |

Evidências: `evidencias/prova_comboboxsample.txt` e `evidencias/roundtrip_r2.txt` no ZIP de fontes.

## 6. Pendência

`PENDENTE_VALIDACAO_TENANT`: abrir a build r2 no Studio e confirmar 0 erros. É a mesma pendência da build anterior.
