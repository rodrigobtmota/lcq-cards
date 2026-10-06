# Diff exato — nova build × 3d5cfb

- Base: `3d5cfb3a455351cb085df2d6bae86d08a7ab82db8f656cb05964bf17b551a7ce`
- Nova: `98168d77c5d2fdb036c4e04c57c4f18ba43b6ac07ce4b9882aec02319661fe17`

## Inventário de arquivos (SHA-256 do conteúdo, caminhos normalizados)

| Arquivo | 3d5cfb | Nova | Situação |
|---|---|---|---|
| `Controls/1.json` | 1c1b5b5fee6f0ed7 | 1c1b5b5fee6f0ed7 | idêntico |
| `Controls/322.json` | 81bf346f8dfbd0ae | 81bf346f8dfbd0ae | idêntico |
| `Controls/364.json` | 204587320f0112fd | 204587320f0112fd | idêntico |
| `Controls/451.json` | 467fc5fac9ee5140 | 467fc5fac9ee5140 | idêntico |
| `Controls/489.json` | b559ee7deed56431 | b559ee7deed56431 | idêntico |
| `Controls/565.json` | 01ff5c01ce3e259c | 01ff5c01ce3e259c | idêntico |
| `Controls/630.json` | af6b39f1c1aff95a | af6b39f1c1aff95a | idêntico |
| `Controls/690.json` | d221651fd3f11643 | d221651fd3f11643 | idêntico |
| `Controls/759.json` | bb6dab3cdbb9e5f2 | bb6dab3cdbb9e5f2 | idêntico |
| `References/DataSources.json` | 340e3f24c86786e8 | 1ef93145a8387f31 | **ALTERADO** |
| `Src/App.pa.yaml` | 175ca1091e47608a | 175ca1091e47608a | idêntico |
| `Src/Components/Header_PT_4.pa.yaml` | f91acbda1592508f | f91acbda1592508f | idêntico |
| `Src/TelaAdministracao.pa.yaml` | f98d0e4e7092b570 | f98d0e4e7092b570 | idêntico |
| `Src/TelaAuditoria.pa.yaml` | 4f09b797ab46a67a | 4f09b797ab46a67a | idêntico |
| `Src/TelaCapacidade.pa.yaml` | 15d1e8c361fbbe56 | 15d1e8c361fbbe56 | idêntico |
| `Src/TelaCockpit.pa.yaml` | 92ca4013f3d9679f | 92ca4013f3d9679f | idêntico |
| `Src/TelaDecisoesEncaminhamentos.pa.yaml` | 135cf4db55454a6c | 135cf4db55454a6c | idêntico |
| `Src/TelaDemandas.pa.yaml` | cc2bb0ad3e471cde | cc2bb0ad3e471cde | idêntico |
| `Src/TelaEquipamentos.pa.yaml` | 827f90ac94bf047f | 827f90ac94bf047f | idêntico |
| `Src/TelaRadarSemanal.pa.yaml` | 5aacf2294e0da8df | 5aacf2294e0da8df | idêntico |
| `Src/_EditorState.pa.yaml` | 8b7a1285b032d2a2 | 8b7a1285b032d2a2 | idêntico |
| `packed.json` | — | 5c0feb9c8f5d3b0e | **ADICIONADO** |

Demais arquivos (Components, Assets, Resources, References exceto DataSources, Properties, Header, checksum.json, SARIF): idênticos byte a byte. Total idênticos: **102 de 103**.

## `References/DataSources.json` — diff unificado (CRLF preservado)

```diff
--- 3d5cfb/References/DataSources.json
+++ nova/References/DataSources.json
@@ -11,4 +11,19 @@
       },
       "WorkflowEntityId": "6ed5bc31-b338-ef11-8409-000d3a30f94e"
+    },
+    {
+      "Data": "[{\"Value1\":\"Item 1\",\"Value2\":1,\"Value3\":10},{\"Value1\":\"Item 2\",\"Value2\":2,\"Value3\":20},{\"Value1\":\"Item 3\",\"Value2\":3,\"Value3\":30},{\"Value1\":\"Item 4\",\"Value2\":4,\"Value3\":40},{\"Value1\":\"Item 5\",\"Value2\":5,\"Value3\":50},{\"Value1\":\"Item 6\",\"Value2\":6,\"Value3\":60},{\"Value1\":\"Item 7\",\"Value2\":7,\"Value3\":70},{\"Value1\":\"Item 8\",\"V …[linha truncada no relatório; 802 caracteres; conteúdo íntegro no arquivo]
+      "IsSampleData": true,
+      "IsWritable": false,
+      "Name": "ComboBoxSample",
+      "OrderedColumnNames": [
+        "Value1",
+        "Value2",
+        "Value3"
+      ],
+      "OriginalName": "ComboBoxSample",
+      "OriginalSchema": "*[Value1:s, Value2:n, Value3:n]",
+      "Schema": "*[Value1:s, Value2:n, Value3:n]",
+      "Type": "StaticDataSourceInfo"
     },
     {
```

## `packed.json` — adicionado pelo PAC 2.12.2

```json
{
  "PackedStructureVersion": "0.1",
  "LastPackedDateTimeUtc": "2026-10-06 07:53:29Z",
  "PackingClient": {
    "Name": "Pac CLI",
    "Version": "2.12.2"
  },
  "LoadConfiguration": {
    "LoadFromYaml": false
  }
}
```

`LoadFromYaml: false` (opção oficial `--disable-load-from-yaml`) preserva o modo de carga da 3d5cfb, que não tinha `packed.json` e é carregada pelos `Controls/*.json`.
