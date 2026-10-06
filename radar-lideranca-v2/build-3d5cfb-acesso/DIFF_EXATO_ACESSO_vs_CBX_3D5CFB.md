# Diff exato — correção do bloqueio de acesso (base: CBX `98168d77…` / 3d5cfb)

- Nova build: `a1c72acfb7bed2fe703eacfa73bf9abf60aa7483d387b3b38fac4990314a2ac5`
- Base direta: CBX `98168d77c5d2fdb036c4e04c57c4f18ba43b6ac07ce4b9882aec02319661fe17` (= 3d5cfb + ComboBoxSample)

## Arquivos

| Arquivo | Situação |
|---|---|
| `Src/TelaAdministracao.pa.yaml` | **alterado** |
| `Src/TelaAuditoria.pa.yaml` | **alterado** |
| `Src/TelaCapacidade.pa.yaml` | **alterado** |
| `Src/TelaCockpit.pa.yaml` | **alterado** |
| `Src/TelaDemandas.pa.yaml` | **alterado** |
| `Src/TelaEquipamentos.pa.yaml` | **alterado** |
| `Src/TelaRadarSemanal.pa.yaml` | **alterado** |
| `packed.json` | **alterado** |
| demais 96 arquivos | idênticos byte a byte |

`packed.json`: `LoadFromYaml` passa de `false` para `true` (pack padrão do PAC). É o modo suportado para que o Studio aplique fórmulas alteradas no YAML. Antes, verifiquei que nesta build `Controls/*.json` e `Src` são coerentes: 5.836 regras em comum e 0 divergentes.

## Diff unificado dos `Src/*.pa.yaml` (todas as linhas alteradas)

```diff
--- CBX/Src/TelaAdministracao.pa.yaml
+++ nova/Src/TelaAdministracao.pa.yaml
@@ -50 +50 @@
-          Visible: =(true) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =(true) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -614 +614 @@
-            varMostrarPainelIntegranteAdmin) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+            varMostrarPainelIntegranteAdmin) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -851 +851 @@
-          Visible: =((varEhAdmin || varEhLideranca) && varMostrarPainelParametroAdmin) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =((varEhAdmin || varEhLideranca) && varMostrarPainelParametroAdmin) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -1107 +1107 @@
-          Visible: =(varMostrarAjudaRadar) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =(varMostrarAjudaRadar) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -1130 +1130 @@
-          Visible: =(varMostrarAjudaRadar) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =(varMostrarAjudaRadar) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -1365 +1365 @@
-          Visible: =!(Coalesce(varCargaInicialConcluida,false) && (varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
+          Visible: =!IsBlank(varCargaInicialConcluida) && !(varCargaInicialConcluida && (varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
--- CBX/Src/TelaAuditoria.pa.yaml
+++ nova/Src/TelaAuditoria.pa.yaml
@@ -183 +183 @@
-          Visible: =(true) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =(true) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -1689 +1689 @@
-          Visible: =((varEhLideranca || varEhAdmin) && varMostrarPainelAuditoria) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =((varEhLideranca || varEhAdmin) && varMostrarPainelAuditoria) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -2551 +2551 @@
-          Visible: =(varMostrarAjudaRadar) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =(varMostrarAjudaRadar) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -2574 +2574 @@
-          Visible: =(varMostrarAjudaRadar) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =(varMostrarAjudaRadar) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -2829 +2829 @@
-          Visible: =!(Coalesce(varCargaInicialConcluida,false) && (varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
+          Visible: =!IsBlank(varCargaInicialConcluida) && !(varCargaInicialConcluida && (varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
--- CBX/Src/TelaCapacidade.pa.yaml
+++ nova/Src/TelaCapacidade.pa.yaml
@@ -420 +420 @@
-          Visible: =(true) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =(true) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -2279 +2279 @@
-          Visible: =(varMostrarAjudaCapacidade) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =(varMostrarAjudaCapacidade) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -2301 +2301 @@
-          Visible: =(varMostrarAjudaCapacidade) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)
+          Visible: =(varMostrarAjudaCapacidade) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
@@ -2984 +2984 @@
-          Visible: =!(Coalesce(varCargaInicialConcluida,false) && (varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
+          Visible: =!IsBlank(varCargaInicialConcluida) && !(varCargaInicialConcluida && (varUsuarioCadastrado && (varEhLideranca || varEhAdmin)))
--- CBX/Src/TelaCockpit.pa.yaml
+++ nova/Src/TelaCockpit.pa.yaml
@@ -881 +881 @@
-          Visible: =(true) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(true) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -3559 +3559 @@
-          Visible: =(varMostrarAjudaCockpit) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarAjudaCockpit) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -3584 +3584 @@
-          Visible: =(varMostrarAjudaCockpit) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarAjudaCockpit) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -4272 +4272 @@
-          Visible: =!(Coalesce(varCargaInicialConcluida,false) && (varUsuarioCadastrado))
+          Visible: =!IsBlank(varCargaInicialConcluida) && !(varCargaInicialConcluida && (varUsuarioCadastrado))
@@ -5155 +5155 @@
-          Visible: =varUsuarioCadastrado && Coalesce(varCargaInicialConcluida,false)
+          Visible: =(IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
--- CBX/Src/TelaDemandas.pa.yaml
+++ nova/Src/TelaDemandas.pa.yaml
@@ -621 +621 @@
-          Visible: =(true) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(true) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -2760 +2760 @@
-            !varMostrarPainelDemanda) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+            !varMostrarPainelDemanda) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -2829 +2829 @@
-            !varMostrarPainelDemanda) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+            !varMostrarPainelDemanda) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -3523 +3523 @@
-          Visible: =(varMostrarPainelDemanda) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarPainelDemanda) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -4927 +4927 @@
-          Visible: =!(Coalesce(varCargaInicialConcluida,false) && (varUsuarioCadastrado))
+          Visible: =!IsBlank(varCargaInicialConcluida) && !(varCargaInicialConcluida && (varUsuarioCadastrado))
--- CBX/Src/TelaEquipamentos.pa.yaml
+++ nova/Src/TelaEquipamentos.pa.yaml
@@ -279 +279 @@
-          Visible: =(true) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(true) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -2641 +2641 @@
-          Visible: =(varMostrarPainelEquipamento) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarPainelEquipamento) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -2656 +2656 @@
-          Visible: =(varMostrarPainelEquipamento) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarPainelEquipamento) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -4325 +4325 @@
-          Visible: =(varMostrarAjudaEquipamentos) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarAjudaEquipamentos) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -4348 +4348 @@
-          Visible: =(varMostrarAjudaEquipamentos) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarAjudaEquipamentos) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -4521 +4521 @@
-          Visible: =!(Coalesce(varCargaInicialConcluida,false) && (varUsuarioCadastrado))
+          Visible: =!IsBlank(varCargaInicialConcluida) && !(varCargaInicialConcluida && (varUsuarioCadastrado))
--- CBX/Src/TelaRadarSemanal.pa.yaml
+++ nova/Src/TelaRadarSemanal.pa.yaml
@@ -326 +326 @@
-          Visible: =(true) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(true) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -1406 +1406 @@
-          Visible: =(varMostrarPainelRotina) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarPainelRotina) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -2205 +2205 @@
-          Visible: =(varMostrarPainelCuradoriaRotina) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarPainelCuradoriaRotina) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -2453 +2453 @@
-          Visible: =(varMostrarAjudaRadar) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarAjudaRadar) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -2476 +2476 @@
-          Visible: =(varMostrarAjudaRadar) && Coalesce(varCargaInicialConcluida,false) && varUsuarioCadastrado
+          Visible: =(varMostrarAjudaRadar) && (IsBlank(varCargaInicialConcluida) || (varCargaInicialConcluida && varUsuarioCadastrado))
@@ -2649 +2649 @@
-          Visible: =!(Coalesce(varCargaInicialConcluida,false) && (varUsuarioCadastrado))
+          Visible: =!IsBlank(varCargaInicialConcluida) && !(varCargaInicialConcluida && (varUsuarioCadastrado))
```
