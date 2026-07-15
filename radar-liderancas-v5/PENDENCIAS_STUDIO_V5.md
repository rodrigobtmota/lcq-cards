# Pendências no Power Apps Studio — V5 FINAL VALIDADO

Este ambiente não tem Power Apps Studio, PAC CLI nem conexão real com o SharePoint. Tudo abaixo só pode ser concluído por alguém com acesso ao Studio e ao ambiente do Radar de Lideranças LCQ V2.

## 1. Executar o App Checker real

`AppCheckerResult.sarif` e `Properties.json` (`BindingErrorCount = 4`) estão desatualizados — os 4 erros registrados correspondem a problemas já corrigidos antes desta rodada (`Header_EN.FAQ()`, `.Width` do cabeçalho, dois erros de tipo em `TelaAuditoria.OnVisible`). Eles não foram editados manualmente, conforme instrução.

**Ação necessária**: abrir o `.msapp` final no Studio e rodar o App Checker (Ctrl+F5 / painel "Verificação do Aplicativo") para gerar um resultado atualizado. Confirmar:
- `ParserErrorCount = 0`
- `BindingErrorCount = 0`
- Nenhum erro de severidade alta remanescente, especialmente nos três botões corrigidos nesta rodada (`btnSalvarAuditoria`, `btnSalvarIntegranteAdmin`, `btnSalvarParametroAdmin`).

## 2. Regenerar os espelhos Src/*.pa.yaml

Ao salvar o app no Studio, os arquivos `.pa.yaml` são regenerados a partir de `Controls/*.json`. Confirmar que, após salvar:
- `Src\TelaAuditoria.pa.yaml` passa a refletir as novas fórmulas de `btnSalvarAuditoria`.
- `Src\TelaAdministracao.pa.yaml` passa a refletir as novas fórmulas de `btnSalvarIntegranteAdmin` e `btnSalvarParametroAdmin`.
- `Src\TelaDemandas.pa.yaml` e `Src\TelaCockpit.pa.yaml` passam a refletir os controles que já estavam divergentes antes desta rodada (divergência pré-existente, não introduzida agora).

Se o Studio não regenerar algum desses arquivos automaticamente, registrar o fato e investigar antes do piloto.

## 3. Remover os componentes de cabeçalho órfãos

Quatro componentes de cabeçalho existem no pacote mas não estão instanciados em nenhuma tela: `Header_EN`, `Header_PT`, `Header_EN_1` e `Header_PT_6`. O único cabeçalho realmente usado nas 7 telas é `Header_PT_4`.

**Ação necessária**: no painel de Componentes do Studio, confirmar que nenhum deles é referenciado, e excluí-los pela interface oficial (não por edição manual de JSON). `Header_PT` e `Header_PT_6` também contêm uma auto-chamada inválida (`Header_PT.FAQ()` / `Header_PT_6.FAQ()`) num controle `Contact_*` interno — mesma classe do antigo erro de `Header_EN_1`, mas inerte, pois o componente nunca é instanciado. Excluir os quatro elimina esse código morto e reduz a chance de reaparecerem em uma versão futura.

## 4. Testes funcionais completos

Nenhum teste funcional foi executado neste ambiente. Antes do piloto, executar:

### Perfil Integrante
- [ ] Criar demanda (confirmar que Criticidade não aparece durante a criação).
- [ ] Editar demanda própria (confirmar Criticidade somente leitura).
- [ ] Visualizar demanda de terceiro (confirmar ausência do botão Salvar).
- [ ] Registrar Rotina Semanal.

### Perfil Liderança
- [ ] Editar qualquer demanda, incluindo Criticidade.
- [ ] Fazer curadoria semanal.
- [ ] Criar e editar avaliação de Auditoria — **validar especificamente a correção desta rodada**.
- [ ] Visualizar capacidade da equipe.
- [ ] Confirmar que Administração está acessível (conforme regra atual de `varEhLideranca || varEhAdmin`).

### Perfil Administrador
- [ ] Confirmar acesso total.
- [ ] Confirmar tela de Administração.
- [ ] Alterar parâmetros permitidos (`Radar_Config`) — **validar a correção desta rodada em `btnSalvarParametroAdmin`**.
- [ ] Cadastrar/editar integrante — **validar a correção desta rodada em `btnSalvarIntegranteAdmin`**.

### Falhas simuladas (o mais importante desta rodada)
- [ ] Falha no `Patch()` da Auditoria (ex.: desconectar a rede momentaneamente durante o salvamento) — confirmar mensagem "Não foi possível salvar a avaliação." e que o painel **não fecha**.
- [ ] Falha isolada no `Refresh()`/recarga pós-gravação da Auditoria — confirmar mensagem "A avaliação foi salva, mas a lista não pôde ser atualizada agora." e que o painel **fecha** (porque o `Patch()` teve sucesso).
- [ ] Duplo clique em Salvar (Auditoria, Integrante, Parâmetro) — confirmar que o segundo clique não duplica o registro nem reenvia o `Patch()`.
- [ ] Repetir os três testes acima para `btnSalvarIntegranteAdmin` e `btnSalvarParametroAdmin`.
- [ ] Falha parcial no envio semanal (alguns itens salvam, outros não) — já validado estaticamente como correto; confirmar em ambiente real.
- [ ] Falha na carga do Cockpit (banner + toast).
- [ ] Falha na carga da Auditoria (tela em branco vs. mensagem de erro).

### Segurança
- [ ] Tentar acessar `TelaAuditoria`/`TelaAdministracao` diretamente (fora do menu) como Integrante e confirmar que o botão Salvar permanece desabilitado (`DisplayMode.View`) mesmo que o painel seja aberto.

## 5. Lacunas de escopo já conhecidas (não são bugs)

Os seguintes módulos aparecem apenas como conceito/possível item futuro, sem tela implementada: **Bloqueios**, **Encaminhamentos**, **Decisões**, **Guia do Radar**. Nenhum deles tem entrada em `colMenu` visível de forma quebrada — "Guia do Radar" está no menu com mensagem explícita "ainda está em construção." Nenhuma implementação parcial foi inventada para esses módulos nesta rodada, conforme instrução.

## 6. Conexões e publicação

- As conexões do SharePoint em `References/DataSources.json` foram preservadas byte a byte — não precisam ser reconfiguradas, mas ainda assim é recomendável reconectar/republicar pelo Studio antes do piloto, como prática padrão ao mover um `.msapp` entre ambientes.
