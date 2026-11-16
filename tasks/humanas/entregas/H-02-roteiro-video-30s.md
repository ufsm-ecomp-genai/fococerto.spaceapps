# H-02: Roteiro do vídeo de 30 s (versão enxuta)

O roteiro original (`task-humana-02`) segue intacto. Esta versão:
- segue a ordem do guia oficial: **nome/equipe 0:00 → desafio 0:02 → título 0:05 → ideia 0:10 → futuro 0:20**;
- tem cerca de 75 palavras (dá para falar com calma em ~28 s, a ~2,6 palavras/s);
- tira "two decades of NASA FIRMS data" e "in real time", que não temos como sustentar sem os dados reais.
- Legendas prontas em `H-02-legendas.srt`. Mesmo falando em inglês, legenda ajuda o jurado que assiste sem som.

| Tempo | Tela | Locução (inglês) |
|---|---|---|
| 0:00–0:03 | Título "FocoCerto Harmonizer" + "Team ECOMP-UFSM · [nomes]" | *Hi, we're Team ECOMP-UFSM, from Brazil.* |
| 0:03–0:08 | Imagem do Worldview (H-07): MODIS esparso × VIIRS denso, mesma frente de fogo | *NASA has watched fires from space since 2000, but MODIS and VIIRS count them differently.* |
| 0:08–0:10 | Logo/título do projeto | *This is FocoCerto Harmonizer.* |
| 0:10–0:20 | **Gravação de tela:** calendário do Tocantins, passar o mouse numa semana crítica e abrir o card | *We put both sensors on one grid and build a Fire Activity Calendar: every week compared with its own history, critical weeks in red.* |
| 0:20–0:28 | **Gravação de tela:** clicar para gerar o plano e mostrar o mapa com brigadas | *When a week turns critical, our agents draft a brigade dispatch plan for the coordinator to approve.* |
| 0:28–0:30 | Links (GitHub) | *From NASA data to crews on the ground.* |

## Como gravar a tela
1. `.venv\Scripts\Activate.ps1` e depois `uvicorn app.api:app --port 8000`. Abrir `http://localhost:8000`.
2. Janela em 1920×1080, zoom do navegador 100–110%, esconder barra de favoritos e abas.
3. Gravar cada trecho 2–3 vezes (Xbox Game Bar: `Win+Alt+R`, ou OBS) e escolher o melhor no editor.
4. Se o calendário (A-03) não ficar pronto: o trecho 0:10–0:20 vira um zoom lento na imagem do calendário do Slide 5,
   e a fala muda para *"...and build a Fire Activity Calendar that flags critical weeks."*

## Regras (eliminatórias)
- **≤ 30,0 s** no arquivo final. Conferir a duração no editor, não no YouTube.
- Nenhuma pessoa menor de 18 anos em cena.
- Voz ou imagem gerada por IA → aviso visível na tela ("Voice: AI-generated") e na descrição do YouTube.
- Sem logo da NASA (meatball/worm).
- YouTube **Não listado**, testar em janela anônima.
