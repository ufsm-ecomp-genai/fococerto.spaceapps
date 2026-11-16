# H-03: Textos do portal (versão corrigida, pronta para colar)

Esta é a versão revisada dos textos de `docs/spaceapps/03-papeis-equipe/papel-5-submissao-video-e-formulario.md`.
O original não foi alterado. Mudanças em relação a ele:
- **Ferramentas:** saíram NumPy, Pandas, GeoPandas, SciPy, D3, Tailwind e Earth Engine, que o projeto não usa. Entrou o stack real.
- **Dados:** os números vêm do arquivo real do FIRMS para o Tocantins, 2000–2025 (`H-08-firms/resultados/`).
- **Método de escala:** o texto usa `N = ½ (N_MODIS + k·N_VIIRS)`, como o deck, e não a fórmula do `CLAUDE.md`.
  O motivo está em `ACHADOS-PARA-AGENTES.md`. **Se a equipe mantiver a fórmula original, trocar o item 2 de HOW IT WORKS.**
- **A frase sobre o app ([A]/[B] em HOW IT WORKS)** depende de os agentes ligarem o calendário do app aos dados reais.
- **Trabalho prévio:** declarado em uma frase, com link.
- **CONAE/AEB:** citadas como contexto, sem sugerir que ingerimos dados delas.

Os campos `[PREENCHER]` dependem da equipe ou dos links finais.

---

## Project Name
```text
FocoCerto Harmonizer: Fire Activity Calendar & Tactical Dispatch
```

## High-Level Project Summary
```text
NASA has tracked active fires from space for over two decades, but the record is split between MODIS (1 km pixels, since 2000) and VIIRS (375 m pixels, since 2012). In our study area, Tocantins in Brazil's Cerrado, VIIRS records four times more hot spots than MODIS, so raw counts jump when the sensors change and cannot be compared across years. FocoCerto Harmonizer puts both sensors on a common 0.1° grid and rescales VIIRS to MODIS-equivalent units with a factor measured in the 2012–2025 overlap, keeping Fire Radiative Power as the physical cross-check. The result is a Fire Activity Calendar built from 1.9 million real FIRMS detections (2000–2025): each week of each year is compared with its multi-year median, and weeks above the 95th percentile or with a robust anomaly score of 2 or more are flagged as critical. It finds, for example, that the week of 12–18 November 2025 had 8.6 times the usual fire activity, when the rainy season should have started. When a critical period appears, FocoCerto's Planner–Critic agents turn the current detections into a prioritized brigade dispatch plan that a human coordinator approves.
```

## Link to Project Demo
```text
[PREENCHER: link público do Google Slides (ou do vídeo no YouTube)]
```

## Link to Final Project
```text
https://github.com/ufsm-ecomp-genai/fococerto.spaceapps
```

## Detailed Project Description
```text
WHAT IT DOES
FocoCerto Harmonizer answers a question fire managers ask every dry season: is this week normal for this place, or is it a critical period? Raw satellite hot-spot counts cannot answer it across the MODIS-to-VIIRS transition, because the same fire produces more VIIRS detections than MODIS detections. FocoCerto harmonizes both records and shows a Fire Activity Calendar (years × weeks) for an area of interest, with each week colored by how far it sits from its historical baseline. When a period is flagged as critical, it hands the current detections to a reasoning engine that proposes which incidents to attend first and with which crew, with the evidence for each choice. Nothing is dispatched without human approval.

HOW IT WORKS
1. Data: NASA FIRMS active fire detections from MODIS Collection 6.1 (Terra/Aqua) and VIIRS 375 m (Suomi-NPP).
2. Harmonization: detections are aggregated on a regular 0.1° × 0.1° grid (~11 km), which absorbs the different pixel footprints and the MODIS bow-tie effect. Before 2012 only MODIS exists, so the record is kept in MODIS units: in the overlap period the harmonized count is N = ½ (N_MODIS + k × N_VIIRS), where k = 0.25 is measured from the data (sum of MODIS over sum of VIIRS detections, 2012–2025). Simply adding both sensors would double the count after 2012; with this scaling the annual mean stays on one level (26.7k detections per year in 2003–2011, 23.0k in 2013–2021). Fire Radiative Power, a physical quantity both sensors measure, is the cross-check.
3. Calendar and anomalies: for each week of the year we compute the multi-year median and the median absolute deviation (MAD) over 2001–2025. A robust anomaly score Z = (value − median) / (1.4826 × MAD) of 2.0 or more, or activity above the 95th percentile, marks a critical period. In Tocantins the method recovers the known drought years 2007 and 2010, and flags an unusual late-season peak in November 2025.
4. Tactical dispatch: a Planner agent proposes a resource order for the current occurrences, a Critic agent challenges trade-offs and exceptions, and an Analyst answers open questions with stated uncertainty. Deterministic tools compute distances, travel times and exposed population; model text is checked against the data before the human sees it.
Data volume: 611,797 MODIS and 1,328,777 VIIRS detections for Tocantins, from the NASA FIRMS yearly archive (2000–2025).
{APP — escolher uma linha e apagar a outra, conforme o estado do código às 22:45}
[A] The web calendar reads this harmonized archive directly.
[B] The analysis above runs as a standalone script in the repository; wiring it into the web calendar, which currently shows a calibrated reconstruction, is the next step.

BENEFITS
- A comparable fire-activity record across sensor generations, instead of an artificial jump in 2012.
- A plain answer to "is this unusual?", per area and per week, that a non-specialist can read.
- A path from Earth observation to field decisions, with an auditable justification for each dispatch.

WHAT WE HOPE TO ACHIEVE
Give state situation rooms and brigade coordinators in fire-prone biomes (Cerrado, Pantanal, Gran Chaco) an open tool that tells them early when a season is running above normal, and helps them use scarce crews where they protect the most people.

PRIOR WORK
The multi-agent dispatch engine (Planner, Critic, Analyst) existed before the hackathon. The harmonization module, the calendar engine and the calendar interface were built during Space Apps 2026. The full disclosure is in docs/spaceapps/02-regras-e-diretrizes/declaracao-prior-work.md.

TOOLS, LANGUAGES AND TECHNOLOGIES
- Backend and data: Python 3.12, FastAPI, Pydantic, httpx, PostgreSQL, pytest.
- Agents: LangGraph; NVIDIA Nemotron through Meterless Nightshift; Meterless H-MEM for memory; Zetaris for federated SQL views.
- Frontend: React 19, Vite, Leaflet / react-leaflet.
- Data access: NASA FIRMS (archive CSV and NRT API), NASA Worldview for visual checks, Open-Meteo, GeoNames, OpenStreetMap.
- License: Apache 2.0.
```

## Use of Super Intelligence (SI)
```text
Yes. We used AI coding assistants (Claude Code and Google Antigravity) to help write and test code, draft documentation and review our texts; the team chose the approach, checked the math against the cited papers and reviewed every change. The product itself uses a large language model (NVIDIA Nemotron, through Meterless Nightshift) inside the Planner, Critic and Analyst agents that draft brigade dispatch plans; the numbers those agents cite are computed by deterministic code, and a human approves every plan. Code generated with AI assistance is acknowledged in the repository README ("AI and Model Usage"). [PREENCHER se houver: voz ou imagem gerada por IA no vídeo/slides, e onde está a marca d'água.]
```

## NASA Data
```text
- NASA FIRMS (Fire Information for Resource Management System), active fire detections:
  - MODIS Collection 6.1 (Terra and Aqua), 1 km, archive from 2000 onward.
  - VIIRS 375 m (Suomi-NPP, VNP14IMG), archive from 2012 onward, and NRT for current detections.
- NASA Worldview (Corrected Reflectance true color plus MODIS and VIIRS fire layers), for the visual comparison of the two sensors used in our slides.
- Methods follow NASA-funded literature: Giglio et al. (2016) for MODIS C6, Schroeder et al. (2014) for VIIRS 375 m.
```

## Space Agency Partner Data and Other References
```text
Space agency partners: we did not ingest partner datasets. Our use case is regional fire monitoring in South American biomes where the Brazilian Space Agency (AEB, through INPE's fire program) and Argentina's CONAE (National Space Activities Commission) work; extending the calendar to the Pantanal and the Gran Chaco is our next step.

Other data and tools:
- Open-Meteo (weather), GeoNames (localities and population), OpenStreetMap (fire stations).
- Public lists of fire stations: CBMTO (Tocantins Military Fire Brigade), Prevfogo/Ibama (Portaria nº 114/2024), ICMBio.
- Software: Python, FastAPI, LangGraph, React, Vite, Leaflet, PostgreSQL, Zetaris, Meterless Nightshift and H-MEM, NVIDIA Nemotron.

Scientific references:
- Giglio, L., Schroeder, W., Justice, C. O. (2016). The collection 6 MODIS active fire detection algorithm and fire products. Remote Sensing of Environment, 178, 31–41.
- Schroeder, W., Oliva, P., Giglio, L., Csiszar, I. A. (2014). The New VIIRS 375 m active fire detection data product. Remote Sensing of Environment, 143, 85–96.
- Wooster, M. J., Roberts, G., Perry, G. L. W., Kaufman, Y. J. (2005). Retrieval of biomass combustion rates and totals from fire radiative power observations. Journal of Geophysical Research, 110, D24311.
- Sofiev, M., Kouznetsov, R. (2020). Analytical observation operators for MODIS and VIIRS fire radiative power products. Atmospheric Chemistry and Physics, 20(24), 15443–15462.

All code is ours or open source under its own license; see "Credits and third-party components" in the README.
```
