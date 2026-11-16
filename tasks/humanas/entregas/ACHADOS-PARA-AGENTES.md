# Achados da trilha humana que afetam o código (para a Trilha dos Agentes)

Nada fora de `tasks/humanas/` foi alterado. Estes são os pontos para quem mexe em `app/` e em `CLAUDE.md` decidir.
Todos os números vêm de `H-08-firms/resultados/`, calculados sobre o arquivo anual real do NASA FIRMS para a bbox
do Tocantins (`config/regioes/tocantins.yaml`): 611.797 detecções MODIS (2000–2025) e 1.328.777 VIIRS S-NPP (2012–2025).

## 1. A fórmula de contagem do `CLAUDE.md` cria um degrau artificial em 2012
`N_harm = N_MODIS + 0.30·N_VIIRS` **soma** os dois sensores a partir de 2012, mas antes de 2012 só existe MODIS.

| Média anual de detecções | 2003–2011 | 2013–2021 |
|---|---|---|
| Fórmula do `CLAUDE.md` | 26.662 | **50.454 (+89%)** |
| `½ (N_MODIS + k·N_VIIRS)`, k = 0,252 medido | 26.662 | 23.047 |

Efeito no calendário: com a fórmula atual, **160 das 168 semanas "críticas" de 2001–2025 caem depois de 2012**.
É justamente a descontinuidade que o desafio pede para eliminar.

- O fator 0,30 está perto do empírico (k = 0,252, ou seja, VIIRS/MODIS ≈ 4,0). O problema é *somar*, não o fator.
- Correções possíveis, da mais simples para a mais completa: (a) média `½ (N_MODIS + 0.30·N_VIIRS)`;
  (b) usar só `0.30·N_VIIRS` a partir de 2012; (c) k por célula ou por estação, medido na sobreposição.
- **O mesmo vale para o FRP:** `FRP_MODIS + FRP_VIIRS` conta duas vezes a mesma energia radiativa a partir de 2012.
  Usar a média dos dois ou um só sensor, com fator de escala.

O deck e os textos do portal (`H-01`, `H-03`) já usam a opção (a) com k medido. Se o código mantiver a fórmula
atual, os textos precisam voltar à fórmula original, e o degrau fica visível para os jurados.

## 2. O calendário do app é sintético
`app/data/calendario.py::construir_matriz_temporal` preenche todo (ano, semana) sem dado de entrada com
`estimar_linha_base_sazonal_cerrado` (gaussiana), multiplicadores fixos por ano e `sin()`. Duas coisas contradizem os dados reais:
- os multiplicadores dizem que **2024 foi o pior ano (×1,85)**. No arquivo real, 2024 teve 23.750 detecções
  MODIS-equivalentes, abaixo da média; os anos extremos foram **2007 (46.421) e 2010 (48.937)**;
- a docstring promete "calibrada de 24 anos", mas nenhum dado real calibra a curva.

`H-08-firms/resultados/calendario_semanal.csv` tem a série real pronta (ano, semana, N_MODIS, N_VIIRS, FRP,
as duas séries harmonizadas, mediana, Z e a marca de crítico) e pode alimentar o `FireCalendar.jsx` direto.
Para regerar: `baixar_firms_tocantins.sh <pasta>` e `analisar_calendario.py <pasta> <saida>` (só stdlib).
Os CSVs anuais por país do FIRMS são públicos e não pedem MAP_KEY:
`https://firms.modaps.eosdis.nasa.gov/data/country/{modis|viirs-snpp}/{ano}/{produto}_{ano}_Brazil.csv`.
O ano de 2026 ainda não existe nesse formato (precisa da API NRT/área com MAP_KEY).

## 3. Achados menores
- **Semanas de chuva com poucos focos** (jan–abr) dão Z alto com números pequenos (ex.: semana 4 de 2006, 99 contra
  mediana 12, Z = 8,4). Para o calendário, considerar um piso no denominador (ex.: `max(10, 1.4826·MAD)`) ou um mínimo de detecções.
- **Deriva de órbita do Terra/Aqua** (desde ~2020–2022) reduz um pouco a contagem MODIS dos anos recentes. Vale uma linha nas limitações.
- **`README.md` linha 632:** diz "All other code was written during the hackathon build window (first commit 24 Oct 2026)".
  Essa janela é a do hackathon anterior, não a do Space Apps (14–15 nov). Conflita com a declaração de prior work.
- **`README.md` > AI and Model Usage:** cita só o Claude Code. Os textos do portal citam também o Google Antigravity.
  Alinhar os dois.
- A análise de `H-08` agrega por região (bbox inteira), não por célula de 0,1°. Para totais regionais isso não muda nada,
  mas o texto do portal fala em grade de 0,1°, que é a do `harmonizacao.py`.
