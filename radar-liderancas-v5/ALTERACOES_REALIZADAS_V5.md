# Alterações Realizadas — V5 FINAL VALIDADO

Este documento lista, arquivo por arquivo, exatamente o que foi alterado dentro do `.msapp` para chegar de `Radar_de_Liderancas_LCQ_V2_V5_CORRIGIDO_v3.msapp` a `Radar_de_Liderancas_LCQ_V2_V5_FINAL_VALIDADO.msapp`.

As fórmulas abaixo são apresentadas em **Power Fx pt-BR** (`;` entre argumentos, `;;` entre comandos encadeados), para leitura humana. Dentro do pacote `.msapp` (`Controls/*.json`), a sintaxe gravada é a **invariant** própria do arquivo (`,` entre argumentos, `;` entre comandos encadeados), conforme exigido — nenhum arquivo interno foi convertido para pt-BR.

## Arquivos internos alterados

Apenas 2 dos 99 arquivos do pacote foram modificados. Os outros 97 são byte-idênticos ao V3 (confirmado por comparação binária arquivo a arquivo).

| Arquivo interno | Tela | O que mudou |
|---|---|---|
| `Controls\574.json` | TelaAuditoria | `btnSalvarAuditoria`: propriedades `OnSelect` e `DisplayMode` |
| `Controls\626.json` | TelaAdministracao | `btnSalvarIntegranteAdmin` e `btnSalvarParametroAdmin`: propriedades `OnSelect` e `DisplayMode` |

Nenhum controle foi adicionado ou removido. Nenhum `ControlUniqueId` foi criado, alterado ou reaproveitado. Nenhuma outra tela, componente, fonte de dados, tema, recurso ou conexão foi tocada.

---

## 1. TelaAuditoria → btnSalvarAuditoria.DisplayMode

**Antes:**
```
If(varSalvandoAuditoria; DisplayMode.Disabled; DisplayMode.Edit)
```

**Depois:**
```
If(
    !(varEhLideranca || varEhAdmin);
    DisplayMode.View;
    If(varSalvandoAuditoria; DisplayMode.Disabled; DisplayMode.Edit)
)
```

Motivo: o botão não verificava permissão em `DisplayMode`, apenas se já estava salvando. Agora, quem não é Liderança nem Administrador nunca vê o botão habilitado, independentemente do menu estar oculto ou não.

---

## 2. TelaAuditoria → btnSalvarAuditoria.OnSelect

**Antes** (resumo do problema): validava campos obrigatórios e, em caso de sucesso, executava `Patch()`, `Select(btnAtualizarAuditoria)`, fechamento do painel e mensagem de sucesso **dentro do mesmo `IfError()`**. Qualquer erro em qualquer uma dessas etapas — inclusive uma falha isolada de rede na recarga — acionava o ramo de erro do `IfError()`, que exibia "Não foi possível salvar a avaliação.", mesmo quando o `Patch()` já havia gravado o registro com sucesso.

**Depois:**
```
If(
    !(varEhLideranca || varEhAdmin);

    Notify(
        "Você não tem permissão para salvar avaliações de auditoria.";
        NotificationType.Error
    );

    varSalvandoAuditoria;

    Notify(
        "A avaliação já está sendo salva.";
        NotificationType.Information
    );

    IsBlank(Trim(txtTituloPainelAuditoria.Text)) || IsBlank(Trim(txtMesPainelAuditoria.Text));

    Notify(
        "Informe o título e o mês de referência.";
        NotificationType.Warning
    );

    Set(varSalvandoAuditoria; true);;
    Set(
        varAuditoriaSalva;
        IfError(
            Patch(
                Radar_GestaoAuditoria_LCQ;
                If(varModoAuditoria = "Novo"; Defaults(Radar_GestaoAuditoria_LCQ); varRegistroAuditoriaSelecionado);
                {
                    Title: Trim(txtTituloPainelAuditoria.Text);
                    DimensaoAvaliada: {Value: ddDimensaoPainelAuditoria.Selected.Value};
                    MesReferencia: Trim(txtMesPainelAuditoria.Text);
                    StatusDimensao: {Value: ddStatusPainelAuditoria.Selected.Value};
                    RiscoAuditoria: {Value: ddRiscoPainelAuditoria.Selected.Value};
                    EvidenciaDisponivel: {Value: ddEvidenciaPainelAuditoria.Selected.Value};
                    Descricao: Trim(txtDescricaoAuditoria.Text);
                    AcaoNecessaria: Trim(txtAcaoAuditoria.Text);
                    EmailResponsavel: Lower(Trim(txtEmailAuditoria.Text));
                    Prazo: dpPrazoAuditoria.SelectedDate;
                    StatusRegistro: {Value: ddStatusRegistroAuditoria.Selected.Value};
                    LinkEvidencia: Trim(txtLinkAuditoria.Text)
                }
            );;
            true;

            false
        )
    );;

    If(
        varAuditoriaSalva;

        Select(btnAtualizarAuditoria);;
        Set(varFalhaRecargaAuditoria; !IsBlank(varErroAuditoria));;
        Set(varMostrarPainelAuditoria; false);;
        Set(varSalvandoAuditoria; false);;
        If(
            varFalhaRecargaAuditoria;
            Notify("A avaliação foi salva, mas a lista não pôde ser atualizada agora."; NotificationType.Warning);
            Notify("Avaliação de auditoria salva com sucesso."; NotificationType.Success)
        );

        Set(varSalvandoAuditoria; false);;
        Notify("Não foi possível salvar a avaliação."; NotificationType.Error)
    )
)
```

O que mudou, item a item:
- **Permissão em profundidade**: primeira condição do `If()` — bloqueia quem não é Liderança/Administrador, mostrando mensagem específica.
- **Duplo clique**: segunda condição — se já está salvando, apenas informa e não reenvia.
- **Gravação isolada**: `Patch()` envolvido em seu próprio `IfError()`, resultado booleano em `varAuditoriaSalva`. Nenhum outro comando dentro desse `IfError()`.
- **Recarga isolada**: só executa depois de `varAuditoriaSalva = true`; usa `Select(btnAtualizarAuditoria)` (que já isola seus próprios erros em `varErroAuditoria`) e registra o resultado em `varFalhaRecargaAuditoria`.
- **Painel só fecha após sucesso real do `Patch()`**: `Set(varMostrarPainelAuditoria, false)` está dentro do ramo `varAuditoriaSalva = true`.
- **Mensagens diferenciadas**: "A avaliação foi salva, mas a lista não pôde ser atualizada agora." (recarga falhou) vs. "Avaliação de auditoria salva com sucesso." (tudo certo) vs. "Não foi possível salvar a avaliação." (o `Patch()` falhou).
- **`varSalvandoAuditoria` liberado em todos os caminhos**: nos dois ramos do `If(varAuditoriaSalva, ...)`.
- **Registro selecionado preservado em caso de falha**: `varRegistroAuditoriaSelecionado` não é tocado no ramo de falha do `Patch()`.

---

## 3. TelaAdministracao → btnSalvarIntegranteAdmin.DisplayMode

**Antes:**
```
DisplayMode.Edit
```

**Depois:**
```
If(
    !(varEhLideranca || varEhAdmin);
    DisplayMode.View;
    If(varSalvandoIntegranteAdmin; DisplayMode.Disabled; DisplayMode.Edit)
)
```

---

## 4. TelaAdministracao → btnSalvarIntegranteAdmin.OnSelect

Mesmo padrão de falha do item 2 (gravação, recarga e mensagem no mesmo `IfError()`, sem checagem de permissão). Corrigido com a mesma técnica:

```
Set(varFaixaIntegranteNumerica; IfError(Value(txtFaixaIntegranteAdmin.Text; "en-US"); Blank()));;
If(
    !(varEhLideranca || varEhAdmin);

    Notify("Você não tem permissão para salvar integrantes."; NotificationType.Error);

    varSalvandoIntegranteAdmin;

    Notify("O salvamento já está em andamento."; NotificationType.Information);

    IsBlank(Trim(txtNomeIntegranteAdmin.Text)) || IsBlank(Trim(txtEmailIntegranteAdmin.Text)) || IsBlank(varFaixaIntegranteNumerica);

    Notify("Informe nome, e-mail e uma faixa sustentável numérica."; NotificationType.Warning);

    Set(varSalvandoIntegranteAdmin; true);;
    Set(
        varIntegranteAdminSalvo;
        IfError(
            Patch(
                Radar_Integrantes;
                If(varModoIntegranteAdmin = "Novo"; Defaults(Radar_Integrantes); varIntegranteAdminSelecionado);
                {
                    Title: Trim(txtNomeIntegranteAdmin.Text);
                    Email: Lower(Trim(txtEmailIntegranteAdmin.Text));
                    Perfil: {Value: ddPerfilIntegranteAdmin.Selected.Value};
                    Ativo: togAtivoIntegranteAdmin.Value;
                    FaixaSustentavel: varFaixaIntegranteNumerica
                }
            );;
            true;

            false
        )
    );;

    If(
        varIntegranteAdminSalvo;

        Select(btnAtualizarAdministracao);;
        Set(varFalhaRecargaIntegranteAdmin; !IsBlank(varErroAdministracao));;
        Set(varMostrarPainelIntegranteAdmin; false);;
        Set(varSalvandoIntegranteAdmin; false);;
        If(
            varFalhaRecargaIntegranteAdmin;
            Notify("O integrante foi salvo, mas a lista não pôde ser atualizada agora."; NotificationType.Warning);
            Notify("Integrante salvo com sucesso."; NotificationType.Success)
        );

        Set(varSalvandoIntegranteAdmin; false);;
        Notify("Não foi possível salvar o integrante."; NotificationType.Error)
    )
)
```

---

## 5. TelaAdministracao → btnSalvarParametroAdmin.DisplayMode

**Antes:**
```
DisplayMode.Edit
```

**Depois:**
```
If(
    !(varEhLideranca || varEhAdmin);
    DisplayMode.View;
    If(varSalvandoParametroAdmin; DisplayMode.Disabled; DisplayMode.Edit)
)
```

---

## 6. TelaAdministracao → btnSalvarParametroAdmin.OnSelect

```
Set(varValorParametroNumerico; IfError(Value(Trim(txtValorParametroAdmin.Text); "en-US"); Blank()));;
If(
    !(varEhLideranca || varEhAdmin);

    Notify("Você não tem permissão para salvar parâmetros."; NotificationType.Error);

    varSalvandoParametroAdmin;

    Notify("O salvamento já está em andamento."; NotificationType.Information);

    IsBlank(Trim(txtChaveParametroAdmin.Text)) || IsBlank(varValorParametroNumerico);

    Notify("Informe a chave e um valor numérico com ponto decimal."; NotificationType.Warning);

    Set(varSalvandoParametroAdmin; true);;
    Set(
        varParametroAdminSalvo;
        IfError(
            Patch(
                Radar_Config;
                If(varModoParametroAdmin = "Novo"; Defaults(Radar_Config); varParametroAdminSelecionado);
                {
                    Title: Trim(txtChaveParametroAdmin.Text);
                    Valor: Trim(txtValorParametroAdmin.Text);
                    Descricao: Trim(txtDescricaoParametroAdmin.Text)
                }
            );;
            true;

            false
        )
    );;

    If(
        varParametroAdminSalvo;

        Select(btnRecarregarParametrosAdmin);;
        Set(varMostrarPainelParametroAdmin; false);;
        Set(varSalvandoParametroAdmin; false);;
        Notify("Parâmetro salvo com sucesso."; NotificationType.Success);

        Set(varSalvandoParametroAdmin; false);;
        Notify("Não foi possível salvar o parâmetro."; NotificationType.Error)
    )
)
```

**Observação registrada, não corrigida**: `btnRecarregarParametrosAdmin` (chamado por `Select()` acima) já dispara seu próprio `Notify()` ("Parâmetros recarregados." ou "Falha ao recarregar os parâmetros."), de forma independente. Isso pode gerar duas notificações visíveis em sequência quando o parâmetro é salvo (a de "Parâmetro salvo com sucesso." e a do próprio botão de recarga). Esse comportamento já existia antes desta correção (o botão de recarga já era chamado da mesma forma) e não foi alterado nesta rodada, por não ser o defeito confirmado em escopo. Fica registrado como possível ajuste futuro de UX.

---

## Novas variáveis introduzidas

Todas seguem a convenção de nomes já usada no restante do app (`varSalvandoX`, `varXSalvo`/`varXSalva`, `varFalhaRecargaX`), que já era usada em `btnSalvarCuradoriaRotina` e `btnSalvarEquipamento`.

| Variável | Tipo | Onde é definida | Propósito |
|---|---|---|---|
| `varAuditoriaSalva` | Booleano | `btnSalvarAuditoria.OnSelect` | Resultado isolado do `Patch()` da Auditoria |
| `varFalhaRecargaAuditoria` | Booleano | `btnSalvarAuditoria.OnSelect` | Resultado isolado da recarga pós-gravação |
| `varIntegranteAdminSalvo` | Booleano | `btnSalvarIntegranteAdmin.OnSelect` | Resultado isolado do `Patch()` de Integrante |
| `varFalhaRecargaIntegranteAdmin` | Booleano | `btnSalvarIntegranteAdmin.OnSelect` | Resultado isolado da recarga pós-gravação |
| `varSalvandoIntegranteAdmin` | Booleano | `btnSalvarIntegranteAdmin.OnSelect`/`DisplayMode` | Bloqueio de duplo clique |
| `varParametroAdminSalvo` | Booleano | `btnSalvarParametroAdmin.OnSelect` | Resultado isolado do `Patch()` de Parâmetro |
| `varSalvandoParametroAdmin` | Booleano | `btnSalvarParametroAdmin.OnSelect`/`DisplayMode` | Bloqueio de duplo clique |

`varSalvandoAuditoria` já existia no app (usada em `TelaAuditoria.OnVisible` e no `DisplayMode` original do botão) e foi reaproveitada, não recriada.

Nenhuma dessas variáveis precisa de inicialização explícita em `OnVisible`/`OnStart`: em Power Fx, uma variável global lida antes do primeiro `Set()` retorna `Blank()`, que se comporta como falso em contextos booleanos e como "não corrigido ainda" nesses fluxos — consistente com o comportamento já usado para `varCuradoriaSalva` e `varFalhaRecargaCuradoria` em `btnSalvarCuradoriaRotina`, que também não são inicializadas em `OnVisible`.

---

## Verificações executadas sobre os arquivos alterados

- `Controls\574.json` e `Controls\626.json` continuam sendo JSON válido após a edição (parse bem-sucedido).
- Parênteses e chaves balanceados em cada `OnSelect`/`DisplayMode` alterado (contagem automática, ver `RELATORIO_VALIDACAO_FINAL_V5.md`, Seção 3).
- Todas as variáveis e controles referenciados nas novas fórmulas (`varEhLideranca`, `varEhAdmin`, `btnAtualizarAuditoria`, `btnAtualizarAdministracao`, `btnRecarregarParametrosAdmin`, `varErroAuditoria`, `varErroAdministracao`, etc.) já existiam no aplicativo antes desta rodada — nenhuma referência a controle ou variável inexistente foi introduzida.
- Nenhum outro arquivo do pacote foi alterado (confirmado por comparação binária dos 99 arquivos entre V3 e V5 FINAL).
