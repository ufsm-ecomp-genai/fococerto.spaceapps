# Guia de Trabalho — Papel 5: Submissão, Vídeo de 30s e Formulário NASA
**Responsável:** Lucas Lima Mendes  
**Foco:** Submissão no Portal NASA Space Apps, Vídeo de 30s e Auditoria de Regras

---

### 1. Sua Missão no Time
Você é o guardião da entrega final. Suas tarefas são:
1. Preencher todos os campos da aba "Projeto" no site oficial da Space Apps em **Inglês**.
2. Garantir que a demonstração (Vídeo de 30s ou os 7 Slides da Pessoa 4) tenha um link público funcional.
3. Fazer a auditoria de conformidade (regras da NASA, licença, transparência de IA).
4. Clicar em **"Submit for Judging"** antes das 23:59.

---

### 2. Textos Oficiais dos Campos da Página do Projeto (Copie e Cole)

#### Project Name (Nome do Projeto)
```text
FocoCerto Harmonizer: Active Fire Calendar & Tactical Dispatch
```

#### High-Level Project Summary (Resumo de Alto Nível)
*(Máximo de impacto e concisão)*
```text
Satellite sensors have tracked active wildfires for over two decades, yet the historical record is split between MODIS (1 km) and VIIRS (375 m), preventing direct comparison and misleading fire managers. FocoCerto Harmonizer bridges this gap by cross-calibrating two decades of NASA FIRMS observations into a unified, continuous Fire Activity Calendar. Through an interactive web application, early warning teams and land managers can examine 24-year seasonal baselines, detect severe climatological anomalies, and instantly trigger AI-reasoned tactical dispatch plans to prioritize scarce brigade resources in field emergencies.
```

#### Detailed Project Description (Descrição Detalhada do Projeto)
*(Aborda o que faz, como funciona e ferramentas usadas)*
```text
### What it does
FocoCerto Harmonizer resolves the historical discontinuity between NASA's MODIS and VIIRS active fire observations. It provides fire managers, civil defense agencies, and scientists with an interactive web-based Burning Activity Calendar for any selected Area of Interest (AOI), highlighting normal seasonal baselines against critical burning periods. Furthermore, when extreme thermal anomalies are detected, the system bridges Earth observation with real-world tactical response by generating an audited dispatch recommendation for firefighting brigades.

### How it works
1. Cross-Sensor Harmonization: Raw thermal anomaly detections from MODIS C6.1 (2000–present) and VIIRS 375m (2012–present) are mapped onto standardized 0.1° spatial grids. Using empirical cross-calibration and radiative energy conservation, our engine reconciles the footprint discrepancy (1 km vs 375 m) and normalizes pixel count biases.
2. Climatological Baseline & Anomaly Detection: For any selected region, the engine calculates multi-decadal median baselines and robust MAD dispersion for every week of the year. Critical periods and unusual conditions are dynamically flagged when activity surpasses the 95th percentile or an anomaly Z-score >= 2.0.
3. Fire Activity Calendar Web UI: An accessible matrix heatmap visualizes multi-year activity, allowing users to spot shifts in fire return intervals, peak season duration, and unusual winter/spring spikes.
4. Operational Tactical Dispatch: Integrated with FocoCerto's multi-agent reasoning architecture (Planner, Critic, Analyst), the system translates anomalous fire clusters into prioritized dispatch routes, calculating travel times, population exposure, and firefighter safety.

### Tools, Languages, and Technologies
- Data & Backend: Python 3.12, NumPy, Pandas, GeoPandas, Scipy Spatial, FastAPI.
- Earth Observation & APIs: NASA FIRMS REST API, NASA Earthdata, Google Earth Engine catalogues.
- Frontend & Visualization: React, Vite, Tailwind CSS, Leaflet.js, D3.js.
- Autonomous Reasoning: Multi-agent LangGraph architecture with structured verification.
```

#### Use of Superintelligence / Artificial Intelligence (Uso de IA / Superinteligência)
*(Transparência exigida pela NASA)*
```text
Artificial Intelligence was used responsibly as an acceleration tool during development. We utilized AI code assistants (Google Antigravity and Claude Code) to assist in mathematical implementation of spatial aggregation grids, frontend component scaffolding, and documentation structuring. Additionally, the project features a multi-agent AI reasoning core (Planner-Critic-Analyst) designed to verify factual citations, compute resource tradeoffs, and assist human commanders with brigade dispatch recommendations. All scientific methodologies, data interpretations, and algorithmic logic were guided and verified by the human team.
```

#### NASA Data Used (Dados da NASA Utilizados)
```text
1. NASA FIRMS (Fire Information for Resource Management System):
   - MODIS Collection 6.1 Active Fire Product (MCD14DL / MOD14 / MYD14) – 1 km resolution (2000–present).
   - VIIRS 375 m Active Fire Product: Suomi-NPP (VNP14IMGTDL, 2012–present) and NOAA-20 / JPSS-1 (VJ114IMGTDL, 2018–present).
   - NASA FIRMS NRT REST API for real-time thermal anomaly streaming.
2. NASA Earthdata Worldview for optical and thermal layer verification.
```

#### Space Agency Partner Data and Other Resources (Dados de Parceiros e Referências)
```text
- Space Agency Partner: CONAE (Comisión Nacional de Actividades Espaciales, Argentina) and AEB (Agência Espacial Brasileira) – contextual reference for regional fire monitoring across the Gran Chaco, Cerrado, and Pantanal biomes.
- OpenStreetMap and Open-Meteo API for road networks and local weather covariates (wind speed, VPD, relative humidity).
- Scientific Literature: Giglio et al. (2016) on MODIS C6; Schroeder et al. (2014) on VIIRS 375m; Wooster et al. (2005) on Fire Radiative Power; Sofiev & Kouznetsov (2020) on observation operators.
- Open Source License: Apache License 2.0.
```

---

### 3. Roteiro do Vídeo de 30 Segundos (Caso Escolham Vídeo)

Se a equipe optar por submeter o vídeo de 30s além dos slides:

* **[0:00 - 0:04] Abertura:**
  *(Tela com logo e integrantes)*
  *"We are Team ECOMP-UFSM, presenting FocoCerto Harmonizer for the NASA Space Apps Challenge."*
* **[0:04 - 0:09] O Desafio:**
  *(Gráfico mostrando a quebra MODIS 1km vs VIIRS 375m)*
  *"For over 20 years, satellites tracked fires, but MODIS and VIIRS records could not be compared directly, blinding fire managers to real trends."*
* **[0:09 - 0:19] A Demonstração do Calendário:**
  *(Gravação da tela do Web App navegando pela matriz de anos)*
  *"We built a harmonized Fire Activity Calendar that cross-calibrates two decades of NASA FIRMS data, revealing 24-year baselines and flagging extreme anomalies in real time."*
* **[0:19 - 0:26] O Diferencial de Despacho:**
  *(Mostrando o clique no botão e o plano de brigadas aparecendo)*
  *"When a critical fire period is detected, our reasoning engine generates tactical brigade dispatch plans to protect vulnerable communities."*
* **[0:26 - 0:30] Encerramento:**
  *"From NASA Earth observation to lifesaving ground response. Thank you!"*

---

### 4. Checklist Final de Submissão (Antes de Clicar em "Submit")

- [ ] Todos os 5 membros confirmados na equipe no site da Space Apps.
- [ ] Link do Projeto Final (GitHub público com código e README em inglês).
- [ ] Link da Demonstração testado em janela anônima (slides ou vídeo sem pedir login/senha).
- [ ] Todos os campos de texto colados em inglês no portal.
- [ ] Caixa de concordância com Termos e Condições marcada.
- [ ] Caixa de "Original Work" marcada.
- [ ] Botão **"Submit for Judging"** clicado com banner de confirmação visível!
