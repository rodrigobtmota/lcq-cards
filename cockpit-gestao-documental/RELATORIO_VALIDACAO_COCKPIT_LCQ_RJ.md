# Relatório de Validação — Cockpit de Gestão Documental LCQ RJ

**Arquivo entregue:** `LCQ_RJ_COCKPIT_GESTAO_DOCUMENTAL_EXECUTIVO_FINAL.xlsx`
**Arquivo de entrada:** `LCQ_RJ_COCKPIT_GESTAO_DOCUMENTAL_SUPER_PREMIUM.xlsx`
**Data de referência da validação:** 06/10/2026 (o arquivo usa `=HOJE()`, então os números mudam conforme a data)

---

## 1. Resumo executivo

| Indicador | Valor | Leitura |
|---|---|---|
| Instruções únicas (Código NDocs) | **125** | vêm de 131 linhas de instrução (6 repetições consolidadas) |
| Aprovadas | **117** | 96% das 122 ativas |
| Em processo | **3** | Revisão 2 · Elaboração 1 |
| Ação imediata (vencida e ativa) | **1** | BRK-INS-01-010133-PT — Manual de Segurança do Laboratório (venceu em 13/09/2026) |
| Validar cadastro | **2** | 1 "Não encontrado" + 1 "Avaliação de uso" |
| Vencem em 12 meses | **12** | nenhuma em até 90 dias; concentração em **abr/27 (6)** e **mar/27 (3)** |
| Saúde documental | **95,1%** | 116 de 122 instruções ativas estão aprovadas e dentro da validade |

**Principal risco:** a instrução vencida mais relevante é o Manual de Segurança do Laboratório (COMUM). **Carga futura:** 9 das 12 revisões dos próximos 12 meses caem entre março e abril de 2027.

---

## 2. O que foi alterado

**Abas reconstruídas** (a lógica anterior foi revista e refeita):

| Aba | Mudança principal |
|---|---|
| **INÍCIO** (nova) | Página inicial com acessos agrupados (Cockpit, Base e Auditoria, Instruções por área, Outros controles, Histórico) e mini-indicadores calculados por fórmula |
| **DASHBOARD EXECUTIVO** (era DASHBOARD PREMIUM) | Layout novo em uma tela: cabeçalho, 5 filtros, 6 KPIs, painel Ação Necessária, agenda de 12 meses, carteira por área, matriz Área × Situação, carteira por responsável e faixa de Outros Controles. Nenhuma fórmula de outra aba apontava para o nome antigo, então a troca de nome não quebra nada. |
| **PESQUISA** (nova, substitui a busca do rodapé do dashboard) | A busca antiga trazia só o 1º resultado. A nova lista até 15 resultados por código, número antigo ou trecho do título, sem diferenciar maiúsculas e ignorando NBSP |
| **BASE CONSOLIDADA** | Separação visual entre **A–M (dado original)** e **N–Z (camada analítica)**. Novas colunas: origem rastreável (`aba!linha`), status padronizado, validade analítica, responsável padronizado, horizonte, mês de vencimento, prioridade e ação recomendada |
| **QUALIDADE BASE** | Achados classificados em Crítico / Atenção / Informativo, 8 verificações automáticas que recalculam com a base e regras documentadas |
| **OUTROS CONTROLES** | Contagem por fórmula (coluna-chave) e situação da base (detecta erros legados automaticamente) |
| **_AUX DASH** | Reescrita e documentada. Contém a data de referência, as listas dos filtros e os cálculos dos gráficos |

**Abas de origem** (Q4, PE_PP, AOL, COMUNS, FMG/ANX, Transversais, LPP, AST, RT, MO e as históricas) receberam só padronização visual: fonte, cabeçalho, datas em dd/mm/aaaa, larguras, congelamento, filtro, linhas discretas, link "← Início | Dashboard" e cor de aba por família. **Os valores não foram tocados.**

---

## 3. O que foi preservado (verificado)

- As **6.993 células com valor** das 15 abas de origem foram comparadas uma a uma com o arquivo recebido. **0 dados alterados.** A única diferença são 11 células com o texto de navegação "DASHBOARD PREMIUM" (M1), que viraram links.
- O Status oficial do NDocs continua intacto na coluna E da Base. A Situação Gerencial é uma camada separada.
- Os erros legados (LPP, AST Geral) foram mantidos, apenas destacados.
- Nenhuma validade, versão, status ou responsável foi inventado.

---

## 4. Números finais (recontados a partir das origens)

Foi feita uma contagem independente em Python diretamente das abas de origem e comparada com o resultado das fórmulas. **Os números coincidem.**

| Item | Valor |
|---|---|
| Linhas lidas (Q4 + PE_PP + AOL + COMUNS) | 132 (131 Instruções + 1 LVS, que fica fora do escopo) |
| Códigos únicos | 125 |
| Aprovado / Revisão / Em Elaboração | 117 / 2 / 1 |
| Cancelado / Fora de Uso | 2 / 1 |
| Não encontrado / Avaliação de uso | 1 / 1 |
| Vencidas ativas | 1 |
| Sem validade | 1 (a instrução em elaboração, o que é esperado) |
| Próximos 12 meses | 12 (mar/27 3 · abr/27 6 · mai/27 1 · jul/27 1 · set/27 1) |
| Área consolidada | Q4 58 · AOL 23 · PE 11 · COMUM 11 · PP 10 · PE/PP 9 · Q4/AOL 3 = **125** |
| Responsáveis (nome padronizado) | 20 (eram 22 grafias diferentes) |

### Correções em relação à versão anterior

| Item | Antes | Agora | Motivo |
|---|---|---|---|
| Saúde documental | 95,36 (pesos arbitrários 5/3/2/1) | 95,1% | A regra anterior penalizava "Planejar revisão", que é planejamento normal e não falha. A nova regra é auditável. |
| Filtro de Responsável | 22 nomes (duplicados por grafia) | 20 nomes | Padronização na camada analítica |
| Coluna Qtd. da agenda no _AUX | exibida como data (ex.: 03/01/1900) | número | Erro de formatação |
| Validades gravadas como texto (2 instruções AOL) | ignoradas nas comparações de data | convertidas na coluna analítica | Antes eram contadas como "a validar" |
| OUTROS CONTROLES: FMG/ANX · AST Geral · MO | 39 · 25 · 8 | 38 · 23 · 5 | Antes contavam linhas vazias da tabela e o rótulo "CANCELADOS". Agora conta só células preenchidas na coluna-chave |
| MO: erro VALUE em H8:H10 | registrado como erro | **não se reproduz** | No arquivo recebido essas células retornam " " (validade vazia) |

---

## 5. Inconsistências encontradas (resumo da QUALIDADE BASE)

- **Crítico (1):** BRK-INS-01-016228-PT com status "Não encontrado".
- **Atenção (10):**
  - 3 códigos repetidos na mesma aba (NDocs AOL): 016681, 016231 e 010963.
  - 2 títulos divergentes para o mesmo código: 016238 e 016288.
  - "Avaiação de uso" com erro de grafia, em instrução marcada "Não aplicável ao RJ".
  - 2 validades gravadas como texto.
  - Erros legados em LPP e AST Geral.
- **Informativo (14):**
  - 3 duplicidades esperadas (Q4/AOL).
  - Grafias de responsável e espaços no final do status.
  - "Cancelada" e "Cancelado" coexistindo.
  - Caracteres NBSP.
  - Título "ONTROLE…" (provável "CONTROLE").
  - O registro LVS.
  - As abas históricas.

---

## 6. Erros legados (não corrigidos)

| Local | Erro | Decisão |
|---|---|---|
| LPP!F100:F124 | `=UPPER(#REF!)` (25 células) | Preservados, porque não há fonte segura para reconstruir a referência |
| AST Geral!E42 | `=UPPER(#REF!)` | Preservado |

Esses erros não entram em nenhum KPI de Instruções. Aparecem sinalizados no Dashboard, em Outros Controles e na Qualidade.
**Erros introduzidos por este trabalho: 0.** O recálculo completo (2.232 fórmulas) retornou só esses 26 `#REF!`, todos já existentes no arquivo recebido.

---

## 7. Regras

**Situação Gerencial** (calculada a partir do status padronizado e da validade):

| Situação | Regra |
|---|---|
| Inativo | Cancelado ou Fora de Uso |
| Em tratamento | Revisão ou Em Elaboração |
| Validar cadastro | Status diferente de Aprovado (Não encontrado, Avaliação de uso) ou Aprovado sem validade |
| Ação imediata | Aprovado com validade anterior à data de referência |
| Planejar revisão | Aprovado com vencimento em até 12 meses |
| Regular | Aprovado com vencimento após 12 meses |

**Prioridade no painel Ação Necessária:**

1. vencida ativa
2. não encontrada
3. em revisão
4. em elaboração
5. vence em até 90 dias
6. validar cadastro

Dentro da mesma prioridade, a validade mais próxima vem primeiro. O painel mostra até 8 itens. Hoje aparecem 6.

**Saúde Documental** = (Regular + Planejar revisão) ÷ instruções ativas.
Explicação em uma frase: *"de cada 100 instruções em uso, 95 estão aprovadas e dentro da validade."*
Os inativos ficam fora da conta. A qualidade cadastral é medida separadamente, na aba QUALIDADE BASE.

**Área:** cada código conta uma única vez. A área consolidada é a união das áreas nas origens (Q4 + AOL → Q4/AOL). O filtro "Q4" inclui os compartilhados.

**Agenda:** um mês é marcado como concentração quando tem pelo menos 2× a média mensal e no mínimo 3 documentos. O limite é calculado, sem valor fixo, e hoje marca mar/27 e abr/27.

---

## 8. Decisões de design

- **Paleta curta:**
  - Navy `#1F2A44` e azul `#2F5597` como cores principais.
  - Fundo `#F3F5F8`.
  - Vermelho só para crítico, âmbar para atenção, verde para regular e cinza para inativo.
- **Fonte:** Segoe UI, com hierarquia 17 → 11 → 24 (KPI) → 8–9.
- **Gráficos:** colunas empilhadas para a agenda (o destaque do mês de concentração é dinâmico) e barras horizontais por área. Nada de pizza, 3D ou legenda desnecessária.
- **Matriz e tabelas:** a cor aparece só quando há exceção (> 0 em colunas de risco). Zeros aparecem como "·".
- **Filtros:** listas suspensas, porque são compatíveis com Excel Desktop e Web. Os segmentadores nativos foram descartados porque exigiriam converter a base em tabela dinâmica.
- **Funções:** só funções compatíveis com Excel 2010+ (`COUNTIFS`, `INDEX/MATCH`, `LARGE/SMALL`). Uma única função volátil (`HOJE()` em `_AUX DASH!B3`).
- **Sem VBA, sem macros, sem dependências externas.**

---

## 9. Limitações

1. **Renderização:** a inspeção visual foi feita no LibreOffice, que não tem a fonte Segoe UI. No Excel podem ocorrer pequenas diferenças de largura de texto. **Recomendo abrir uma vez no Excel 365 em 100% de zoom** antes da reunião.
2. **Achados da QUALIDADE BASE:** a tabela de achados é uma fotografia da data de geração. As 8 verificações automáticas recalculam com a base.
3. **Base Consolidada:** os valores foram copiados das origens no momento da geração. **Se as abas NDocs forem atualizadas, a Base precisa ser regenerada** (o processo é por script, não é automático no Excel).
4. **Lista de responsáveis:** a lista do filtro foi gerada a partir dos dados atuais. Um responsável novo precisa ser incluído em `_AUX DASH`.
5. **Última atualização e fonte:** a "última atualização" não foi exibida porque não há campo confiável para calculá-la. A fonte "NDocs Rev.28" foi informada por você e não está registrada no arquivo.
6. **Notebooks:** em telas de 1366 px, o dashboard pede rolagem horizontal leve ou zoom de 90%.

---

## 10. Testes executados

- Contagem independente (Python) × fórmulas: todos os KPIs, a matriz, a área, a agenda e os responsáveis coincidem.
- Recálculo completo: 2.232 fórmulas, 0 erros novos.
- Teste de filtro (Área = Q4, Situação = Planejar revisão): retornou 2, coerente com a matriz.
- Teste de busca: "OXIGÊNIO" retornou 7 resultados. Um termo inexistente retornou 0, sem erro.
- Comparação célula a célula das 15 abas de origem: 0 dados alterados.
- Inspeção visual (PDF renderizado) do Início, Dashboard, Pesquisa e Qualidade. Foram corrigidos:
  - código cortado no painel de ação;
  - rótulos zerados na agenda;
  - data exibida como "###" na pesquisa;
  - nomes longos de responsáveis.
- Integridade do arquivo: 2 gráficos, 5 validações de lista e 7 nomes definidos preservados após o recálculo.

---

## 11. Parecer final

**APROVADO COM RESSALVAS**

Não há problema crítico introduzido por este trabalho, e os números foram validados. As ressalvas são:

1. Abrir uma vez no Excel 365 para confirmar a aparência final, porque a revisão visual foi feita no LibreOffice.
2. Os 26 erros legados de LPP/AST Geral continuam no arquivo de origem.
3. A Base Consolidada não se atualiza sozinha quando as abas NDocs mudam.
4. Antes da reunião, convém tratar no NDocs:
   - o código "Não encontrado" (016228);
   - a instrução vencida (010133);
   - as 3 linhas repetidas na aba AOL.

---

## 12. Revisão 2 — usabilidade e acabamento visual (pedido de ajuste)

| Aba | O que mudou |
|---|---|
| **INÍCIO** | Redesenhada como página de entrada: faixa com data de referência, 5 indicadores do dia, 6 cartões "O que você quer fazer?" (cada um com botão), cartões por área com contagem, guia "Como usar em 3 passos" e legenda de cores |
| **DASHBOARD EXECUTIVO** | Barra de botões na faixa superior, blocos em painéis brancos com título e ícone, cabeçalhos de tabela destacados, nomes curtos na carteira por responsável (sem texto cortado), gráficos ajustados aos painéis |
| **BASE CONSOLIDADA** | Faixa de título com botões, separação visual entre dado original e camada analítica, linhas de altura fixa sem quebra, cores de status discretas, colunas técnicas (W–Z) agrupadas e ocultas (botão "+" acima da coluna para exibir) |
| **QUALIDADE BASE** | Faixa e botões, KPIs em cartões, tabelas em fundo branco |
| **OUTROS CONTROLES** | Grade de cartões por família com contagem, situação da base e botão "Abrir aba" |
| **PESQUISA** | Faixa, botões e caixa de busca maior |
| **Abas de origem** (Q4, PE_PP, AOL, COMUNS, FMG/ANX, Transversais, LPP, AST, RT, MO, históricas) | Faixa superior com logo reposicionado, botões **Início / Dashboard / Pesquisa (ou Outros)** visíveis na primeira tela e fixos ao rolar, resumo automático (registros · vencidos · vencem em 12 meses), cabeçalho azul, linhas zebradas, status e validade destacados só nas exceções |

**Correção:** o Início exibia "06/10/yyyy" no Excel em português, porque a função TEXTO não reconhece "yyyy" nessa configuração. Agora a data usa formato de célula e não depende do idioma.

**Validação da revisão 2:**
- Recálculo completo: 2.281 fórmulas, sem erros novos. Continuam apenas os 26 `#REF!` legados.
- KPIs iguais aos da versão anterior: 125 / 117 / 3 / 1 / 12 / 95,1%.
- Dados das abas de origem a partir da linha 2: 6.968 células comparadas, 0 alteradas.
- Linha 1 das abas de origem: o título foi mantido, só sem os espaços iniciais, e o texto antigo de navegação foi trocado por botões.
- Inspeção visual (LibreOffice) de Início, Dashboard, Pesquisa, Qualidade, Outros e NDocs Q4.
