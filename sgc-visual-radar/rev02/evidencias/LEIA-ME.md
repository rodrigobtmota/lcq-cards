# Evidências visuais — REV02

## O que estas imagens são

Renderizações geradas pelo script `ferramentas/render_evidencias.py` **a partir dos
fontes da REV02** (`Src/*.pa.yaml`). Cada retângulo, cor, raio, espessura de borda,
tamanho de fonte, texto estático e HTML vem das propriedades reais dos controles.
A faixa do cabeçalho é o arquivo real do recurso registrado em `References/Resources.json`.

Servem para conferir: composição do shell, geometria, paleta, tipografia,
raios e o HTML efetivamente presente nos fontes.

## O que estas imagens NÃO são

Não são capturas do Power Apps Studio nem do runtime. Fora do Studio não é possível
resolver dados do SharePoint nem `ThisItem` de galerias ligadas a dados. Portanto:

- valores vindos de dados aparecem como `—`;
- galerias ligadas a dados mostram linhas de amostra com a mesma geometria real;
- controles `ComboBox` aparecem apenas como área, por não terem fundo/texto próprios nos fontes;
- painéis cuja visibilidade depende de digitação do usuário são omitidos;
- diferenças de renderização de fonte entre o navegador e o Power Apps são esperadas.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `PREVIEW_CABECALHO_RODAPE_REV02.png` | Cabeçalho institucional de 90 px e rodapé |
| `PREVIEW_scrInicio_REV02.png` | Painel executivo |
| `PREVIEW_scrQualificacoes_REV02.png` | Tela de listagem com filtros |
| `PREVIEW_scrAvaliacao_REV02.png` | Tela operacional crítica |
| `PREVIEW_scrCobertura_REV02.png` | Cobertura por área e grupo |
| `*.html` | Fonte de cada renderização, reprodutível |
