# Como reproduzir e auditar a REV02.1

Tudo o que os comandos abaixo precisam está neste pacote. Requer apenas Python 3
(sem bibliotecas externas). A partir da raiz da pasta descompactada:

```bash
python3 ferramentas/migrate.py        # regenera build/ a partir de entrada/sgc
python3 ferramentas/verify.py         # build/ x aplicativo original (entrada/sgc)
python3 ferramentas/verify_rev02.py   # build/ x REV01 entregue (entrada/build_rev01)
python3 ferramentas/verify_rev02.py build_rev01_prefaixa   # x REV01 anterior à faixa
python3 ferramentas/pack_rev021.py    # regera os três artefatos em dist_rev02_1/
```

Para regerar as evidências (requer Playwright + Chromium; opcional):

```bash
python3 ferramentas/render_evidencias.py   # gera os .html em evidencias/
```

## Conteúdo

| Pasta | O que é |
|---|---|
| `Src/`, `Controls/`, `References/`, `Assets/`, `Resources/`, `packed.json`, … | O aplicativo da REV02.1, desempacotado |
| `ferramentas/` | Scripts da transformação e da validação |
| `evidencias/` | Renderizações derivadas dos fontes + `LEIA-ME.md` |
| `entrada/sgc/` | Aplicativo SGC original desempacotado (base funcional) |
| `entrada/pkg/` | Pacote de importação original (identidade, manifest, logo) |
| `entrada/build_rev01/` | REV01 entregue — linha de base da comparação |
| `entrada/build_rev01_prefaixa/` | REV01 anterior à inclusão da faixa institucional |

`build/` é recriado do zero por `migrate.py`; a pasta na raiz deste pacote é o
resultado já gerado, idêntico ao conteúdo do `.msapp` entregue.
