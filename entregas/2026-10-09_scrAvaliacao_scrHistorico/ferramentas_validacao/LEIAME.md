# Ferramentas de validação offline

Scripts usados para gerar e validar esta entrega. Não fazem parte do aplicativo.

| Arquivo | Função |
|---|---|
| `pa_edit.py` | Edita `Controls/<n>.json` (o que o Studio carrega) e espelha a mesma fórmula no `Src/<tela>.pa.yaml`, registrando cada propriedade alterada. |
| `changes_avaliacao.py`, `changes_historico.py` | Todas as alterações das duas telas, propriedade por propriedade. |
| `build.py` | Parte do `.msapp` recebido, aplica as alterações e monta o `.msapp` e o ZIP importável, preservando a estrutura original. |
| `validate.py` | Integridade ZIP, manifest/identity, JSON, parser Power Fx em todas as fórmulas, comparação semântica com o original, propriedades protegidas, YAML⇄JSON, pack/unpack. |
| `pfxcheck/` | Verificador sintático com `Microsoft.PowerFx.Core` (cultura invariante ou pt-BR). |
| `screensim/` | Simulador: executa as fórmulas reais das telas com `Microsoft.PowerFx.Interpreter` sobre dados de teste. |
| `fixtures.py` | Dados **fictícios** de teste. |
| `render.py`, `render/shot.js` | Convertem a tela simulada em HTML e capturam PNG com Chromium (aproximação visual). |
| `run_tests.py` | Cenários TC-A01…A19, TC-H01…H12 e complementares. |
| `pac_check.py` | `pac canvas unpack/pack` (Power Platform CLI) com roundtrip. |
| `ptbr.py`, `gen_docs.py`, `relatorio_modelo.md` | Notação pt-BR, relatório, CSV e manifesto. |

Ordem de execução: `build.py` → `validate.py` → `run_tests.py` → `pac_check.py` → `gen_docs.py` (cada um recebe o diretório de trabalho como argumento).
Requisitos: Python 3 + PyYAML, .NET 8 SDK (pacotes NuGet Microsoft.PowerFx.* 1.8.1), Node + playwright-core, Power Platform CLI 2.13.1 (.NET 10).
