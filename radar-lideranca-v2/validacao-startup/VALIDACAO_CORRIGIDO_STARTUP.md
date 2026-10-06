# Validação — `Radar_de_Liderancas_LCQ_V2_CORRIGIDO_STARTUP.msapp`

**Resultado: `APROVADO_OFFLINE` com 1 risco médio a testar no tenant** (sem `APROVADO_TENANT`)

| Item | Valor |
|---|---|
| SHA-256 do arquivo validado | `8d0b5aeebc87675bf7359098a7aa799a59c14035a556c5f0a215614cc81107e5` |
| Origem identificada | Deriva da CBX `98168d77…` (3d5cfb + ComboBoxSample). Só **4 arquivos** diferem: `Src/App.pa.yaml`, `Src/TelaCockpit.pa.yaml`, `Controls/1.json`, `Controls/322.json` |
| Fórmulas alteradas | 3: `App.OnStart`, `TelaCockpit.OnVisible`, `lblAcessoTelaCockpit.Text` |
| Modo de carga | `packed.json` com `LoadFromYaml: false` (o Studio carrega `Controls/*.json`) |

## 1. Estrutura e consistência

| Verificação | Resultado |
|---|---|
| ZIP íntegro / `pac canvas unpack` (PAC 2.12.2) | OK |
| Round-trip `pack` → `unpack` | `Src` idêntico; pacote idêntico, exceto `packed.json` |
| `Controls/*.json` × `Src` (o que o Studio carrega × YAML) | 5.836 regras em comum, **0 divergentes**. As 3 fórmulas alteradas estão iguais nos dois. |
| Sintaxe Power Fx (parser oficial) | 6.348 fórmulas, **0 erros** |
| Schema pa.yaml v3.0 | **0 erros** |
| Referências (telas, controles, variáveis, coleções, fontes, campos de Patch) | **0 problemas** |
| Variáveis que deixaram de ser definidas e ainda são lidas | **nenhuma** (4 removidas sem uso: `varErroCargaInicial`, `varFalhaCargaInicial`, `varFaixaSustentavelAtual`, `varNomeUsuarioAtual`) |
| Coleções que deixaram de ser criadas | nenhuma |
| `ComboBoxSample` / `RadioSample` | presente / 0 ocorrências |
| `checksum.json` | Mantido da 3d5cfb, por isso **não reflete** `App`, `TelaCockpit` e `DataSources` (mesma situação das builds anteriores) |

## 2. O que a correção faz

- `App.OnStart` deixou de ler o SharePoint (44 KB → 4 KB). Agora só define constantes, cores, pesos padrão, o menu (operacional oculto) e marca `varCargaInicialConcluida = true` com o perfil em `SemAcesso`.
- `TelaCockpit.OnVisible` passou a carregar `Radar_Config`, identificar o integrante, definir perfil e menu (`UpdateIf colMenu`) e montar os indicadores. Os `Refresh` de Integrantes, Demandas e Equipamentos foram retirados dessa carga inicial.
- O aviso do Cockpit mostra "Carregando…" enquanto `varCarregandoCockpit` é verdadeiro.

## 3. O que o Cockpit exibe em cada estado (fórmulas reais avaliadas no interpretador oficial Power Fx)

| Estado | Conteúdo | Aviso |
|---|---|---|
| E1 · nada executado (editor sem OnStart/OnVisible) | oculto | "Carregando acesso ao Radar…" |
| E2 · só OnStart executado (editor sem OnVisible) | oculto | **"Sem acesso. Solicite à liderança…"** |
| E3 · OnStart → OnVisible em andamento | oculto | "Carregando acesso ao Radar…" |
| E4 · OnVisible concluído, usuário cadastrado | **visível** | oculto |
| E5 · OnVisible concluído, usuário não cadastrado | oculto | "Sem acesso…" |
| E6 · OnVisible concluído **antes** do OnStart | oculto | **"Sem acesso…"** para usuário cadastrado |

A sequência normal de uso (E3 → E4/E5) está correta.

## 4. Riscos e pendências

| # | Risco | Nível | Evidência / tratamento |
|---|---|---|---|
| R1 | **Corrida OnStart × OnVisible (E6).** O `OnStart` sobrescreve sem condição `varUsuarioCadastrado`, `varPerfilAtual`, `varEhLideranca`, `varEhAdmin` e o `colMenu` (operacional oculto). O app está com `usenonblockingonstartrule = true`, então a tela inicial não espera o OnStart. Se o `OnVisible` do Cockpit terminar antes, um usuário cadastrado vê "Sem acesso" e o menu reduzido até reabrir o Cockpit. | Médio | É pouco provável, porque o OnStart agora não acessa o SharePoint e termina em milissegundos, mas a ordem **não é garantida pelo código**. `PENDENTE_VALIDACAO_TENANT`: abrir o app publicado várias vezes com usuário Integrante e Liderança. Correção sugerida, se ocorrer: o `OnStart` não deve redefinir variáveis de acesso nem `colMenu` já definidos. |
| R2 | **Editor do Studio.** O problema da imagem anterior (layout oculto no editor) **não é resolvido por esta build** em E1/E2. Em E2, o maker vê "Sem acesso", que é uma mensagem enganosa. O layout só aparece depois que o `OnVisible` do Cockpit roda (pré-visualização/F5). | Baixo (só edição) | `PENDENTE_VALIDACAO_TENANT`: confirmar no Studio. |
| R3 | Sem `Refresh` na carga do Cockpit, ao voltar à tela os dados podem vir do cache da sessão. Uma falha de atualização deixou de ser sinalizada (`varAtualizacaoCockpitOk` sempre `true`). | Baixo | Existe o botão "Atualizar cockpit" (`btnAtualizarCockpitV2`) para atualização manual. |
| R4 | O perfil é calculado dentro do `IfError` dos indicadores. Se a leitura de `Radar_Integrantes` falhar, a tela mostra "Sem acesso", acompanhada de um aviso de erro. | Baixo | Comportamento herdado da 3d5cfb. |
| R5 | Integrante com `Perfil` vazio recebe `"SemAcesso"`. | — | **Já existia** na 3d5cfb/CBX; não foi introduzido aqui. |

## 5. Conclusão

A build é estruturalmente válida e coerente: o YAML e o que o Studio carrega são iguais, sem erros de sintaxe, schema ou referência. A refatoração da inicialização está correta na sequência normal.
Para fechar como `APROVADO_TENANT`, falta testar no tenant: R1 (repetir a abertura com perfis diferentes) e R2 (comportamento no editor).
Nenhuma alteração foi feita no arquivo validado.
