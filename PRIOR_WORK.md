# Declaração Formal de Trabalho Prévio (Prior Work Disclosure)
## NASA International Space Apps Challenge 2026
**Desafio:** Harmonization of MODIS and VIIRS Hot Spots
**Equipe:** ECOMP - UFSM (Universidade Federal de Santa Maria, RS, Brasil)
**Integrantes:** Fernando Dorneles da Silva, Enzo Augusto Mucha Domingues, Gabriel Mazui Azevedo, Eduardo Jacques Pereira, Lucas Lima Mendes
**Licença do Projeto:** Apache License 2.0 (Open Source / OSI-compliant)

# Prior Work Disclosure

**NASA International Space Apps Challenge 2026** · Challenge: **Harmonization of MODIS and VIIRS Hot Spots**
Team **ECOMP - UFSM** (Universidade Federal de Santa Maria, RS, Brazil) · License: [Apache 2.0](LICENSE)

This document states which parts of this repository existed before the hackathon and which were built during
it. The boundary is auditable in git: commit `841b7c6` ("initial commit from FocoCerto base") imports the
pre-existing FocoCerto code unchanged, and every later commit is hackathon work.

## Pre-existing work (before Space Apps 2026)

FocoCerto was built by the same team for an earlier 2026 hackathon. It is a decision-support tool that ranks
simultaneous wildfires and orders scarce firefighting resources. It included:

| Component | Where |
|---|---|
| Multi-agent reasoning (Planner, Critic, Analyst) and its graph | `app/agents/` |
| Agent tools: monitor, rule checks, citation checks, simple allocator, queries | `app/tools/` |
| LLM client and offline/sample mode | `app/llm/`, `app/cli.py` (`run`, `nota`, `aprovar`, `avaliar`) |
| Data layer for one VIIRS S-NPP feed, GeoNames, OpenStreetMap and Open-Meteo | `app/data/` (except the files below), `scripts/ingest_firms.py` |
| HTTP API serving the plan | `app/api.py` |
| Web app (plan, map, resources, reasoning views) | `web/app/` |
| Memory service and evaluation scenarios | `services/hmem/`, `eval/` |

The previous README is preserved in git history at commit `841b7c6`.

## New work during Space Apps 2026

| Component | Where | What is new |
|---|---|---|
| MODIS + VIIRS harmonization | `app/data/harmonizacao.py` | Loads MODIS C6.1 and VIIRS 375 m FIRMS CSVs, maps confidence (MODIS 0–100; VIIRS low/nominal/high), aggregates on a 0.1° grid, and for t ≥ 2012 computes `N_harm = N_MODIS + 0.30·N_VIIRS` and `FRP_harm = ΣFRP_MODIS + ΣFRP_VIIRS` (MODIS only before 2012). The 0.30 factor is taken from the literature, not calibrated by the team. |
| Fire activity calendar engine | `app/data/calendario.py` | Year × period matrix 2000–2026, weekly median, MAD, P90/P95, `Z_fire` and NORMAL / ATENCAO / CRITICO status; JSON export for the web app. |
| CLI for judges | `app/cli_calendario.py`, flags in `app/cli.py` | `python3 -m app.cli --sample --harmonizar` and `--calendario`. |
| Multi-sensor FIRMS ingestion | `app/data/fontes.py`, `scripts/ingest_firms.py` | Feeds for MODIS C6.1, VIIRS S-NPP, NOAA-20 and NOAA-21 (`--sensor`), and offline ingestion of several files. Before, only VIIRS S-NPP. |
| Fire Activity Calendar web view | `web/app/src/` | Calendar heatmap in the web app, plus Space Apps branding (title, header, footer credits). |
| Sample data | `data/samples_firms/` | Small FIRMS-format sample (10 MODIS + 21 VIIRS detections, Tocantins, 15–16 Sep 2024) used by tests and the sample mode. |
| Tests | `tests/test_harmonizacao.py`, `tests/test_cli_calendario.py`, `tests/test_ingest_firms_multisensor.py` | Grid aggregation, FRP conservation, pre-2012 behaviour, anomaly status, CLI output and multi-sensor ingestion, all offline. |
| Challenge documentation | `docs/spaceapps/`, `tasks/` | Challenge brief, rules, scientific summaries and team plan. |

## Not yet done / Future Roadmap

These items are part of our future development roadmap:

- **Expanded geographic coverage:** extending the FIRMS multi-sensor harmonization pipeline to the Pantanal and Gran Chaco biomes, in coordination with AEB/INPE and CONAE data initiatives.
- **Direct Real-Time Dispatch Trigger:** automatically piping live critical anomalies from the calendar into the autonomous agent dispatch queue without requiring the user to click the action button.

## License

All code, data and documentation in this repository are released under the [Apache License 2.0](LICENSE),
Copyright 2026 Team ECOMP - UFSM.
