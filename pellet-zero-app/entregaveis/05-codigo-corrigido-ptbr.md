# Entregável 6 — Código Corrigido (padrão brasileiro)

Tudo o que está no Relatório de Alterações **já foi aplicado dentro do pacote** (`PelletZero_LCQRJ_pacote_corrigido.zip`) — não precisa ser colado manualmente. O Studio exibirá essas fórmulas automaticamente no padrão pt-BR (`;` entre argumentos, `;;` entre instruções).

Este entregável traz o **código completo, pronto para colar**, dos pontos que dependem de decisão/estrutura externa (ver Pendências) e que por isso **não** foram aplicados ao `.msapp`.

---

## 6-A — Iniciar Nova Auditoria (TelaNovaAuditoria)

**Pré-requisito:** confirmar na lista `AuditoriasPrograma` os valores das colunas Choice `TipoAuditoria` e `StatusAuditoria` (o código abaixo assume `"Aberta"`).

**Controles a criar na TelaNovaAuditoria** (bloco "0. NOVA AUDITORIA", acima do bloco atual):

| Controle | Tipo | Propriedade | Valor |
|---|---|---|---|
| dpdTipoNovaAuditoria | Dropdown clássico | Items | `=Choices(AuditoriasPrograma.TipoAuditoria)` |
| dpdSalaNovaAuditoria | Dropdown clássico | Items | `=Choices(AuditoriasPrograma.Sala)` |
| dtpDataNovaAuditoria | Date picker clássico | DefaultDate | `=Hoje()` (exibido como `Today()`) |
| btnIniciarAuditoria | Botão clássico | OnSelect / DisplayMode / Text | abaixo |

**btnIniciarAuditoria.OnSelect** — colar completo:

```powerfx
If(
    varBusyAuditoria;

    Notify(
        "⏳ Aguarde, já existe um registro de auditoria em processamento.";
        NotificationType.Information
    );

    If(
        IsBlank(dpdTipoNovaAuditoria.Selected.Value) ||
        IsBlank(dpdSalaNovaAuditoria.Selected.Value) ||
        IsBlank(dtpDataNovaAuditoria.SelectedDate);

        Notify(
            "Selecione tipo, sala e data para iniciar a auditoria.";
            NotificationType.Warning
        );

        Set(varBusyAuditoria; true);;
        Set(varErroSalvarAuditoria; false);;

        Set(
            varCicloAuditoria;
            Switch(
                true;
                Month(dtpDataNovaAuditoria.SelectedDate) <= 4; "C1-" & Text(Year(dtpDataNovaAuditoria.SelectedDate));
                Month(dtpDataNovaAuditoria.SelectedDate) <= 8; "C2-" & Text(Year(dtpDataNovaAuditoria.SelectedDate));
                "C3-" & Text(Year(dtpDataNovaAuditoria.SelectedDate))
            )
        );;

        IfError(
            Patch(
                AuditoriasPrograma;
                Defaults(AuditoriasPrograma);
                {
                    Title: "AUD - " &
                        dpdTipoNovaAuditoria.Selected.Value & " - " &
                        dpdSalaNovaAuditoria.Selected.Value & " - " &
                        Text(dtpDataNovaAuditoria.SelectedDate; "[$-pt-BR]dd/mm/yyyy");

                    TipoAuditoria: {Value: dpdTipoNovaAuditoria.Selected.Value};
                    Sala: {Value: dpdSalaNovaAuditoria.Selected.Value};
                    Ciclo: varCicloAuditoria;
                    DataProgramada: dtpDataNovaAuditoria.SelectedDate;
                    StatusAuditoria: {Value: "Aberta"};

                    ResponsavelAuditoria: {
                        '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser";
                        Claims: "i:0#.f|membership|" & Lower(Coalesce(varUserEmail; User().Email));
                        DisplayName: Coalesce(varUserNome; User().FullName);
                        Email: Lower(Coalesce(varUserEmail; User().Email));
                        Department: "";
                        JobTitle: "";
                        Picture: ""
                    }
                }
            );

            Set(varErroSalvarAuditoria; true);;
            Set(varBusyAuditoria; false);;
            Notify(
                "❌ Erro ao criar a auditoria: " &
                Coalesce(FirstError.Message; "verifique conexão e permissões.");
                NotificationType.Error
            )
        );;

        If(
            !varErroSalvarAuditoria;

            Notify("✅ Auditoria criada e disponível na lista de auditorias abertas."; NotificationType.Success);;
            Reset(dpdTipoNovaAuditoria);;
            Reset(dpdSalaNovaAuditoria);;
            Reset(dtpDataNovaAuditoria);;
            Set(varBusyAuditoria; false)
        )
    )
)
```

**btnIniciarAuditoria.DisplayMode:**

```powerfx
If(
    varBusyAuditoria;
    DisplayMode.Disabled;
    DisplayMode.Edit
)
```

**Gerar NC a partir da auditoria (opcional, mesma tela):** a lista `NaoConformidadesPorSala` já aceita `OrigemNC = "Auditoria"`. Duplique o padrão do botão de NC das telas de checklist trocando `OrigemNC: {Value: "Checklist"}` por `{Value: "Auditoria"}`, `ChecklistID` por em branco e `SalaNC` pela sala auditada — mantendo a classificação pela `MatrizClassificacaoNC` e a deduplicação.

---

## 6-B — Exigência de evidência no encerramento de NC (TelaNCUsuario)

**Pré-requisito (Pendência 3):** definir o meio de registro da evidência (anexos da lista NC ou biblioteca dedicada) e o momento em que `EvidenciaRegistrada` é marcada como verdadeira.

**Onde colar:** `TelaNCUsuario` → galeria `galNcsUsuario` → botão de concluir NC → `OnSelect`, imediatamente **após** o bloco que valida a ação corretiva (`"❌ Preencha a ação corretiva antes de concluir."`):

```powerfx
If(
    varPodeConcluirNC &&
    ThisItem.ExigeEvidenciaAplicada &&
    !ThisItem.EvidenciaRegistrada;

    Notify(
        "❌ Esta NC exige evidência registrada antes do encerramento. Anexe a evidência e tente novamente.";
        NotificationType.Error
    );;
    Set(varPodeConcluirNC; false)
);;
```

> Atenção: **não ative** este bloco antes de existir a tela/fluxo que grava a evidência, senão nenhuma NC com `ExigeEvidenciaAplicada = true` poderá ser encerrada pelo app.

---

## 6-C — Perfis e proteção de acesso

**Pré-requisito (Pendência 4):** criar a lista SharePoint `PerfisPrograma` no site LCQDCX com colunas: `Title` (e-mail em minúsculas) e `Perfil` (Choice: `Operacional`, `Equipe de Turno`, `Equipe Administrativa`, `Focal`, `Auditor`, `Responsável Técnica`, `Coordenação`, `Administrador`) e adicioná-la como fonte de dados do app.

**1. App.OnStart — colar ao final:**

```powerfx
Set(
    varPerfilUsuario;
    Coalesce(
        LookUp(
            PerfisPrograma;
            Lower(Title) = varUserEmail;
            Perfil.Value
        );
        "Operacional"
    )
);;
Set(varEhAdministrador; varPerfilUsuario = "Administrador");;
Set(
    varEhFocal;
    varPerfilUsuario = "Focal" ||
    varPerfilUsuario = "Coordenação" ||
    varPerfilUsuario = "Responsável Técnica" ||
    varEhAdministrador
);;
Set(varEhAuditor; varPerfilUsuario = "Auditor" || varEhFocal);;
```

**2. TelaInicio — botão do menu de Auditoria → `Visible`:**

```powerfx
varEhAuditor
```

**3. TelaNovaAuditoria — proteção contra navegação alternativa → colar no INÍCIO do `OnVisible` (antes das linhas existentes):**

```powerfx
If(
    !varEhAuditor;
    Notify(
        "Acesso restrito a auditores e ao Focal do Programa.";
        NotificationType.Warning
    );;
    Navigate(TelaInicio; ScreenTransition.Fade)
);;
```

**4. Mesma proteção nas ações de gravação — `btn_Salvar.DisplayMode` (substituir):**

```powerfx
If(
    !varEhAuditor || varBusyAuditoria || IsBlank(dpd_AuditoriaAberta.Selected.ID);
    DisplayMode.Disabled;
    DisplayMode.Edit
)
```

**5. Proteção real na fonte de dados (obrigatória):** aplicar no SharePoint — `AuditoriasPrograma` com edição restrita ao grupo de auditores/Focal; `MatrizClassificacaoNC`, `RodizioPlanejado` e `FilaResponsaveisPorSalaRodizio` somente leitura para operacionais. Esconder botão no app **não** é segurança; a permissão de lista é o que impede gravação por navegação alternativa.

---

## 6-D — Ordem de tabulação (App Checker, acessibilidade)

Para os 355 apontamentos de `TabIndex`: no Studio, defina `TabIndex = 0` nos controles interativos na ordem visual de leitura de cada tela (filtros → botões de ação → navegação) e `TabIndex = -1` em ícones decorativos. Alteração em massa é mais segura pelo próprio Studio (seleção múltipla por tela).
