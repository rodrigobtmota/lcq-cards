# SGC LCQ RJ — Relatório de alterações: `scrAvaliacao` e `scrHistoricoAvaliacoes`

**Status: CANDIDATO VISUAL E FUNCIONAL À HOMOLOGAÇÃO NO TENANT**

Esta versão **não** foi aberta no Power Apps Studio nem testada no tenant Microsoft. A validação descrita aqui é offline. Ela inclui parser e interpretador oficiais do Power Fx, PAC CLI da Microsoft, simulação das telas e testes de cenário. Isso não substitui a homologação no ambiente real. Não declarar como aprovado para produção antes disso.

---

## 1. Resumo executivo

| Item | Resultado |
|---|---|
| Telas alteradas | `scrAvaliacao` e `scrHistoricoAvaliacoes`. As outras 7 telas e o `App` não tiveram nenhuma alteração semântica (verificado). |
| Propriedades alteradas | {n_alt} propriedades, em {n_ctrl_alt} controles existentes e {n_criados} controles novos |
| Controles removidos | 0 |
| DataSources / schema SharePoint / JSON persistidos | Inalterados (verificado byte a byte em `References/DataSources.json`; nenhuma fórmula de gravação nova) |
| Alterações funcionais não autorizadas | **{nao_aut}** |
| Validação de pacote | {val_ok}/{val_n} verificações OK |
| Testes de cenário (TC-A01…A19, TC-H01…H12 e complementares) | {tc_ok}/{tc_n} verificações OK |
| Fórmulas do TXT em notação pt-BR | {ptbr} |

**O que muda para o avaliador.** Ao abrir a avaliação, ele vê num único card quem está sendo avaliado, a área, o módulo, o tipo, quem avalia e o estado. No mesmo card ficam os documentos de referência e o método de avaliação, antes de qualquer critério. Os critérios ganharam largura (66% da área útil), e a coluna da direita ficou só com o parecer e a barra de ações. A barra passou a explicar por que **Concluir** está bloqueado, por exemplo "Parecer técnico pendente · 2 de 30 caracteres". Esse texto só traduz as regras que já existiam no `DisplayMode`.

**O que muda no Histórico.** A lista deixou de mostrar identificadores técnicos (UID e M14.1). No lugar, mostra cargo · grupo, o nome do módulo legível e datas em linguagem natural ("Desde 07/10/2026"). O painel de detalhe virou uma ficha da avaliação. Ele mostra pessoa, módulo · área, tipo e estado, um resumo (avaliador, início, conclusão, resultado, tentativa), os documentos preservados, os critérios com resposta, comentário e referência, o parecer e as observações. UID, ciclo e versão do catálogo ficam numa seção **Informações técnicas**, recolhida por padrão.

---

## 2. Fontes utilizadas e decisões

1. **Fonte de verdade funcional: `SGC LCQ RJ (3).msapp`** (salvo em 09/10/2026 06:01 UTC).
2. **O `.msapp` que estava dentro do ZIP é uma versão anterior** (salvo em 08/10/2026 00:57 UTC). Ele difere do `.msapp` avulso em 13 arquivos internos, incluindo `scrAvaliacao`. Usei o ZIP **apenas como estrutura de importação**: manifesto, definição do app (identity), logo e nomes de entradas. O `document.msapp` interno foi substituído pelo `.msapp` novo. `manifest.json`, `5251408842339445888.json` e o logo estão **idênticos** aos originais (verificado).
3. **Imagens recebidas:** chegou apenas uma imagem, a de referência do novo layout (Contexto + Base documental + Método no topo). A imagem da tela atual não veio nos anexos. As imagens "antes" deste pacote foram geradas executando o `.msapp` original no mesmo simulador, com os mesmos dados de teste.
4. **Técnica de montagem do card Contexto.** `conDocAva` e `conMetAva` continuam no nível da tela, como já eram. Foram posicionados sobre a faixa inferior de `conIdAva`, sem borda e sem fundo próprios, e por isso formam visualmente um único card. Escolhi não mover controles entre contêineres (reparentar no JSON) para reduzir o risco de importação. Nenhum controle mudou de pai (verificado).
5. **Painel técnico do Histórico.** O conteúdo técnico foi para um rótulo visual novo (`lblEvTecHis`) no topo da pilha de camadas. A alternativa seria reordenar camadas de controles existentes. `lblEvV7His` ficou oculto.

---

## 3. `scrAvaliacao` — o que foi feito

**Card "Contexto da avaliação" (`conIdAva`)**
- Título "Contexto da avaliação" (`lblCtxTitAva`, novo). Faixa com PESSOA, ÁREA, MÓDULO, TIPO, AVALIADOR e ESTADO.
- **Módulo:** nome amigável em destaque, em até 2 linhas, com o nome completo no tooltip. "Módulo 14.1" foi removido da tela (`lblIdS2Ava` oculto); o código continua no backend.
- **Avaliador:** nome em até 2 linhas. O cargo aparece quando o nome cabe em 1 linha (estimativa conservadora de largura).
- **Ciclo:** coluna removida do resumo (`lblIdR5Ava`, `lblIdV5Ava` e `lblIdS5Ava` ocultos). "Tentativa N" ficou só no tooltip do selo de estado. GUID não aparece. `locAv.Ciclo` e `locAv.Tentativa` não foram tocados.
- Divisor horizontal leve (`recCtxLinhaAva`, novo). A altura do card é dinâmica: 98 + maior altura entre Base documental e Método + 10.

**Base documental (no topo, cerca de 66% da faixa)**
- Título, subtítulo "Documentos utilizados como referência para esta avaliação." e contagem real: "2 documentos aplicáveis" ou "1 documento aplicável".
- Grade de 2 colunas (`galDocAva`, `WrapCount` 2, `Items = colDocsAva` inalterado). Cada documento mostra o código em semibold, o nome em até 2 linhas e "Versão X · validade dd/mm/aaaa".
- **Datas:** conversão textual `aaaa-mm-dd` → `dd/mm/aaaa`, sem conversão de fuso, portanto sem risco de "voltar um dia". Valor fora desse padrão é exibido como veio.
- Sem versão: não mostra "Versão —". Sem validade: não mostra validade. Sem título: mostra só o código, sem repeti-lo.
- 0 documentos: "Nenhum documento de referência disponível.". Até 4 documentos: exibidos diretamente. 5 ou mais: a altura fica limitada a 2 linhas e a galeria rola na vertical. Não há rolagem horizontal.

**Método de avaliação (no topo, cerca de 34%)**
- Mostra `locAv.MetodoSnap` em texto normal. A versão interna (`VersaoSnap`) não aparece; ficou só no tooltip do título "Método de avaliação". Divisor vertical leve entre Base documental e Método. A altura acompanha o texto até 6 linhas; acima disso, o texto rola dentro do bloco.

**Corpo**
- Critérios ocupam 66% e Parecer 34% (antes, 58% e 42%). `conMetAva` e `conDocAva` saíram da lateral.
- **Card de critério:** botões Atendeu / Não atendeu / N/A na linha do título, como na imagem de referência. Borda neutra `#E1E8F0`; o resultado aparece pela cor do botão e por uma barra lateral fina (verde, vermelha ou cinza). A altura da descrição é calculada para dispensar rolagem interna. Mantidos: título amigável, descrição, comentário/evidência, aviso "Obrigatório para Não atendeu…" e Referência técnica. `lblCritEvAva` continua invisível. Nada de nível, perfil ou código de critério em destaque.
- **Parecer técnico e observações** (`conParAva`) passou a ser o único card fixo da lateral. Novo hint: "Registre aqui o parecer técnico sobre o resultado da avaliação.". O contador foi mantido.

**Barra inferior (`conBarraAva`)**
- Mantidos: X de Y critérios respondidos, barra de progresso, Resultado atual, Salvar rascunho, Cancelar avaliação e Concluir avaliação.
- **Nova linha de pendência**, uma mensagem por vez, nesta prioridade:
  1. "Falta 1 critério / Faltam X critérios para responder"
  2. "Há X critério(s) Não atendeu aguardando comentário"
  3. "Há X critério(s) N/A sem justificativa"
  4. "Não é possível concluir com todos os critérios como N/A" (regra que já existia)
  5. "Parecer técnico pendente · N de 30 caracteres"
  6. "X comentário(s) pendente(s)" (lembrete em cinza, não bloqueia)
  7. "Pronto para concluir"
- Em colunas estreitas (abaixo de 470 px, caso de 1366), os botões ocupam duas linhas: Salvar e Cancelar lado a lado, Concluir na largura inteira. Em 1920, os três ficam em uma linha.
- `btnConcluirAva.DisplayMode` e todos os `OnSelect` de Concluir e Cancelar estão **byte a byte iguais** ao original.

**Rascunho (itens 38–43)**
- `btnSalvarAva.OnSelect`: o Patch e todo o restante foram preservados. Só a notificação de sucesso passou a depender de um contador. Sem pendência, mantém "Rascunho salvo com sucesso." (Success). Com pendência, mostra "Rascunho salvo. Aguardando comentário em 1 critério." ou "… em X critérios." (Warning). O salvamento nunca é bloqueado. Comentário em Atendeu continua opcional.

**Somente leitura (concluída/cancelada):** o banner foi preservado ("…Os critérios e documentos desta avaliação foram preservados conforme estavam no início da avaliação."), sem a palavra *snapshot*. A barra de ações continua oculta e os botões de resposta continuam desabilitados.

## 4. `scrHistoricoAvaliacoes` — o que foi feito

- **Subtítulo:** "Consulte e acompanhe as avaliações técnicas do laboratório." O texto com "snapshot" saiu da interface.
- **Filtros:** os mesmos campos e botões; o card ficou mais compacto (de 160 para 136 px de altura, rótulos de 9 pt, controles de 34/30 px). Nenhum `OnSelect`/`OnChange` foi alterado.
- **Tabela:** título "Registros de avaliação". Contador com plural correto ("1 registro encontrado" / "16 registros encontrados"). Larguras rebalanceadas, priorizando Pessoa, Módulo e Avaliador. Linha de 44 px, mantendo 7 registros por página.
- **Pessoa:** nome + "Cargo · Grupo", vindos primeiro dos dados registrados na avaliação (`CargoSnap`, `GrupoSnap`), com o cadastro atual só como alternativa. **UID removido** da lista; ele continua em `ThisItem.Uid` e em `locEvento`.
- **Módulo:** nome em até 2 linhas, com código no tooltip ("Módulo 14.1"). `lblModCodHis` ficou oculto. Nomes em CAIXA ALTA são normalizados **só quando é seguro**: sem dígitos e sem siglas de até 3 letras. Exemplo: "CROMATOGRAFIA GASOSA PARA…" vira "Cromatografia Gasosa para…".
- **Data:** em preenchimento, "Desde 07/10/2026" com tooltip "Início da avaliação: 07/10/2026". Concluída, "09/10/2026" com tooltip "Concluída em …". Cancelada, data de cancelamento com tooltip "Cancelada em …".
- **Ação:** "Ver detalhes". Os `OnSelect` de `btnRowHis` e `R3btnAbrirEventoHis` não foram alterados. O tooltip da linha não exibe mais o UID.
- **Rodapé:** "Exibindo todas as avaliações do laboratório" ou "Exibindo as avaliações em que você é avaliado ou avaliador". A contagem ficou só no cabeçalho da tabela.
- **Painel de detalhe (`conEvHis`, continua lateral):**
  - "Detalhes da avaliação", Pessoa (nome, cargo · grupo), "Módulo · Área" e chips de Tipo e Estado.
  - Faixa de situação: "Avaliação em andamento", "Avaliação concluída" ou "Avaliação cancelada", com "Informações registradas no momento da avaliação." Quando faltam dados da pessoa no registro original, aparece "Algumas informações deste registro não estavam disponíveis no histórico original.".
  - Resumo com avaliador, início, conclusão (ou cancelamento), resultado e tentativa.
  - **Documentos de referência** lidos de `DocumentosJson` da própria avaliação, nunca do catálogo atual, com código, nome, versão e validade.
  - **Critérios e respostas** com título amigável, descrição, resposta, comentário (ou "Sem comentário registrado.") e referência técnica.
  - Parecer técnico e Observações complementares mostram "Não informado." quando vazios. Em canceladas, o rótulo passa a ser "Justificativa do cancelamento" (texto que o app já grava em `Observacoes`).
  - **Informações técnicas** (avaliação, ciclo, tentativa, versão do catálogo) ficam recolhidas e abrem sob demanda num bloco sobreposto acima do botão.

---

## 5. Alterações por categoria

### scrAvaliacao
{resumo_ava}

### scrHistoricoAvaliacoes
{resumo_his}

### ALTERAÇÕES VISUAIS
Cores, bordas, preenchimentos e visibilidade: card de contexto unificado, sem borda/fundo próprios em `conDocAva`/`conMetAva`, borda neutra nos critérios com barra lateral semântica, selos e chips, e mensagens de pendência em âmbar (bloqueio), cinza (lembrete) ou verde (pronto).

### ALTERAÇÕES DE TEXTO
Contexto da avaliação; Base documental + subtítulo + contagem; hint do parecer; mensagens de pendência; subtítulo e título da tabela do Histórico; "Ver detalhes"; "AÇÃO"; datas "Desde…"; contador com plural; rodapé; textos do painel de detalhe ("Detalhes da avaliação", situação, "Não informado.", "Justificativa do cancelamento", "Informações técnicas"). A palavra *snapshot* não aparece mais nas duas telas.

### ALTERAÇÕES DE GEOMETRIA
X, Y, Width, Height, TemplateSize e WrapCount: novo topo, proporção 66/34, card de critério compacto, barra inferior com quebra responsiva, filtros mais compactos, colunas da tabela e painel de detalhe.

### ALTERAÇÕES FUNCIONAIS
**{nao_aut} alterações funcionais não autorizadas.**

Alterações de comportamento autorizadas (todas sem gravação nova de dados):

| Controle | Propriedade | Motivo |
|---|---|---|
| `btnSalvarAva` (scrAvaliacao) | OnSelect | Itens 38–43: aviso de comentários pendentes **depois** do Patch bem-sucedido. Patch, validações e mensagens de erro preservados (verificado por comparação de prefixo e sufixo da fórmula). |
| `btnEvTecHis` (Histórico, **novo**) | OnSelect | Item 24: `UpdateContext(locEvTec)` só mostra ou oculta "Informações técnicas". |
| `galEvCritHis` (Histórico) | Items | Item 25: lê o mesmo `CriteriosJson` preservado e expõe também `dimensao` e `fontes`, para exibir título e referência técnica. Somente leitura. |

Propriedades funcionais protegidas e conferidas como **idênticas** ao original incluem `scrAvaliacao.OnVisible`, `btnAtAva`/`btnNaoAva`/`btnNaAva`.OnSelect e DisplayMode, `btnNaAva.Visible`, `txtComAva.OnChange`/Default/DisplayMode, `btnCancAva.OnSelect`, `btnConcluirAva.OnSelect` e DisplayMode, `btnCancOkAva.OnSelect`, `txtParecerAva`/`txtObsAva` (Default, DisplayMode, Mode), `galCritAva.Items` e `galDocAva.Items`. No Histórico: `OnVisible`, `galHis.Items`, `btnCopiarHis`, `btnLimparHis`, `btnRowHis`, `R3btnAbrirEventoHis`, fechar painel, `btnEvAbrirHis`, paginação e todos os botões e campos de filtro. A lista completa está na seção 7.

---

## 6. Controles criados, ocultados e removidos

**Criados (somente visuais, exceto o botão de alternância já descrito):**

| Controle | Tela | Tipo | Pai | Modelo copiado |
|---|---|---|---|---|
{criados}

**Ocultados (Visible = false; dados e lógica preservados):**
{ocultos}

**Visibilidade condicional nova em controles existentes:**
{condicionais}

**Removidos:** nenhum.

### Relação de propriedades alteradas — scrAvaliacao
{tab_ava}

### Relação de propriedades alteradas — scrHistoricoAvaliacoes
{tab_his}

A planilha `CONTROLES_PROPRIEDADES_ALTERADAS.csv` traz cada propriedade com a fórmula anterior e a nova (notação invariante).

---

## 7. Validação offline do pacote

Ferramentas: Python (estrutura ZIP/JSON/YAML), **Microsoft.PowerFx.Core 1.8.1** (parser oficial), **Microsoft.PowerFx.Interpreter 1.8.1** (execução das fórmulas) e **Power Platform CLI 2.13.1** (`pac canvas unpack/pack`).

{val_tab}

**PAC CLI (Microsoft) — pack/unpack independente:**
{pac_tab}

**Notação pt-BR:** as {n_alt} fórmulas do TXT foram convertidas para a notação do Studio pt-BR e passaram no parser oficial com cultura pt-BR: {ptbr}. Contraprova: as mesmas fórmulas em notação invariante falham no parser pt-BR, o que confirma que a verificação é efetiva.

---

## 8. Testes de cenário (execução real das fórmulas)

Um simulador executa as fórmulas reais dos controles (`Controls/*.json`) no interpretador oficial do Power Fx. Os dados de teste são **fictícios**, modelados na imagem enviada e na estrutura de `colAvaliacoes`/`colPessoas` montada pelo app. `colCritAva` e `colDocsAva` são geradas pelas **próprias fórmulas do `OnVisible`** da tela. O texto da notificação do rascunho foi obtido executando o trecho real inserido em `btnSalvarAva.OnSelect`. Os filtros do Histórico foram executados na fórmula original de `galHis.Items` e comparados com um cálculo independente.

{tc_tab}

**Critérios visíveis por vez** (altura da lista ÷ altura do card de critério):
- 1366×768: antes 1,40, depois 1,33. Em somente leitura, com banner: 1,10. É uma pequena perda em 768 px de altura, preço de trazer contexto, documentos e método para o topo, como pedido; o card de critério foi compactado para compensar.
- 1920×1080: antes 2,38, depois 2,71.

---

## 9. Limitações e riscos

1. **Sem Studio/tenant:** não foi possível abrir no Power Apps Studio. A checagem de tipos contra o schema real do SharePoint e o App Checker só acontecem lá. O `AppCheckerResult.sarif` do pacote é o anterior; o Studio regenera ao salvar.
2. **As imagens são simulação**, não captura do Power Apps. Controles clássicos foram aproximados em HTML. A fonte usada foi **Open Sans** (Segoe UI não está disponível no ambiente); como ela é mais larga, a medição de cortes de texto é conservadora.
3. **CSS no HtmlText:** o controle pode ignorar `-webkit-line-clamp`/`display:-webkit-box` e `box-shadow`. Se isso acontecer, os textos de 2 linhas continuam limitados por `max-height` (cortam sem reticências) e o card de critério perde só a barra lateral colorida. O comportamento funcional não é afetado. Conferir no tenant.
4. **Fórmulas de gravação** (Patch no SharePoint, concluir, cancelar, atualização de ciclo e qualificação, reconstrução de `colQualificacoesFormais`/`colCobertura`, validade de 36 meses) não foram executadas offline. Elas estão **preservadas byte a byte**.
5. **Larguras de texto estimadas:** a altura da linha de documento e a decisão de mostrar o cargo do avaliador usam estimativa de largura por caractere. Um título muito próximo do limite pode quebrar diferente no navegador real; o tooltip mostra o texto completo.
6. **Nomes muito longos** de pessoa na lista do Histórico continuam truncados com reticências e tooltip (coluna de 16%).
7. **Fora do escopo, sem alteração:**
   - O nome do usuário no cabeçalho é truncado em 1366 (comportamento já existente).
   - Em avaliação **cancelada**, o cabeçalho dos critérios mostra "Resultado atual: Atendeu", calculado pelas respostas (`lblCritAuxAva`, já existente). Sugiro ajustar numa próxima rodada.
   - No Histórico, o botão "Em preenchimento" do filtro quebra em 2 linhas (já existente).

## 10. Próximos passos para homologação

1. Importar `SGC_LCQ_RJ_AVALIACAO_CONTEXTO_FINAL_IMPORTAVEL.zip` como **Atualizar** o app existente, ou abrir o `.msapp` no Studio.
2. No Studio, conferir o App Checker: 0 erros de fórmula nas duas telas.
3. Repetir no tenant, com uma avaliação de teste: TC-A08, A09, A10, A11, A14, A18 e A19, em seguida concluir e cancelar uma avaliação de teste.
4. Conferir a renderização do HtmlText (2 linhas com reticências e barra lateral do critério) em 1366×768 e 1920×1080.
5. No Histórico: filtros, paginação, Copiar para Excel e painel de uma avaliação concluída e de uma cancelada.
6. Só depois disso publicar.

## 11. Arquivos entregues

- `SGC_LCQ_RJ_AVALIACAO_CONTEXTO_FINAL.msapp` (aplicativo consolidado com as duas telas)
- `SGC_LCQ_RJ_AVALIACAO_CONTEXTO_FINAL_IMPORTAVEL.zip` (estrutura original do pacote, com o `document.msapp` substituído)
- `CODIGOS_AVALIACAO_CONTEXTO_FINAL_ptBR.txt` (todas as fórmulas alteradas, notação pt-BR)
- `CONTROLES_PROPRIEDADES_ALTERADAS.csv` (antes/depois de cada propriedade)
- `RELATORIO_AVALIACAO_CONTEXTO_FINAL.md` (este relatório)
- `MANIFESTO_SHA256.txt`
- `imagens/`: `scrAvaliacao` antes/depois em 1366×768 e 1920×1080, composição antes/depois, concluída e cancelada; `scrHistorico` antes/depois em 1366 e 1920, composição antes/depois, detalhe aberto em 1366 e 1920, e detalhe com Informações técnicas
- `evidencias/` (resultados das validações em JSON) e `ferramentas_validacao/` (scripts usados, para reprodução)
