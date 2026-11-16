# H-01: Conteúdo dos 7 slides (versão corrigida)

> **O deck já está pronto em `H-01-slides/FocoCerto-Harmonizer.pptx` (PDF ao lado).** Para usar no Google Slides:
> Drive → Novo → Upload do arquivo → abrir com Google Slides. Falta só **pôr os nomes dos integrantes** (slide 1, em vermelho)
> e, se houver, o link do vídeo (slide 7). Para mudar números ou textos, editar `gerador/extra.json` e rodar o `build.js`.
> Este arquivo fica como referência do conteúdo.

O original (`papel-4-design-e-slides-7paginas.md`) segue intacto. Mudanças nesta versão:
- **Slide 1 com os nomes dos integrantes**, que o guia oficial exige.
- **Slide 5** sem o "+240%" inventado. O número vem do calendário de verdade (`H-08-firms/`).
- Menos texto por slide: o guia pede *"limit the number of words"*.
- Cada slide responde uma pergunta do jurado (problema? solução? funciona? por que confiar? o que muda?).

Visual: 16:9, fundo `#0B132B`, cartões `#1E293B`, laranja `#F97316`, âmbar `#F59E0B`, crítico `#E11D48`,
texto `#FFFFFF`/`#E2E8F0`. Fonte Inter ou Montserrat. **Sem logo da NASA.** Imagens do Worldview com crédito.

---

### Slide 1: Capa
- **FocoCerto Harmonizer**
- Fire Activity Calendar & Tactical Dispatch from NASA FIRMS
- Team ECOMP-UFSM · Universidade Federal de Santa Maria, Brazil
- **Fernando Dorneles da Silva · Enzo Augusto Mucha Domingues · Gabriel Mazui Azevedo · Eduardo Jacques Pereira · Lucas Lima Mendes**
- NASA Space Apps Challenge 2026 · Challenge: *Harmonization of MODIS and VIIRS Hot Spots*

### Slide 2: The problem
- **Título:** One fire, two sensors, two different counts
- **Visual:** par Worldview lado a lado, mesma área e dia (`H-07-worldview/`): MODIS 1 km (7 focos) × VIIRS 375 m (28 focos).
- 3 linhas:
  - MODIS (1 km pixels) since 2000 · VIIRS (375 m pixels) since 2012
  - VIIRS detects 3–4× more hot spots for the same fires
  - Raw counts jump when the sensors change: is this season unusual, or is it just the sensor?

### Slide 3: The solution
- **Título:** From space to action
- **Visual:** fluxo de 4 caixas:
  `NASA FIRMS (MODIS + VIIRS)` → `Harmonization (0.1° grid)` → `Fire Activity Calendar` → `Dispatch plan (human-approved)`
- Legenda curta embaixo de cada caixa: *raw detections* · *one comparable record* · *is this week unusual?* · *who goes where, and why*

### Slide 4: Method
- **Título:** How we make the sensors comparable
- 3 blocos:
  1. **Common grid:** 0.1° × 0.1° cells (~11 km) absorb the 1 km vs 375 m footprint and the MODIS bow-tie.
  2. **Count scaling:** N = N_MODIS + 0.30 × N_VIIRS; Fire Radiative Power (MW), a physical quantity, is the cross-check.
  3. **Anomaly:** weekly multi-year median and MAD; Z ≥ 2.0 or above the 95th percentile = **critical week**.
- Rodapé: *Giglio et al. 2016 · Schroeder et al. 2014 · Wooster et al. 2005*

### Slide 5: The Fire Activity Calendar
- **Título:** Is this week normal for this place?
- **Visual (no deck):** gráfico semanal de 2025 contra a mediana 2001–2025, com dados reais do FIRMS (`H-08-firms/`).
  Se o `FireCalendar.jsx` ficar pronto e usar os dados reais, dá para trocar pelo print do app.
- Card: **8.6×** a atividade usual na semana de 12–18/11/2025 (Z = 9,3), quando as chuvas já deveriam ter começado.
- Segundo card: sem degrau na troca de sensor (26,7 mil/ano em 2003–2011, 23,0 mil/ano em 2013–2021).
- **Atenção:** setembro de 2024 foi **normal** no Tocantins (Z = 1,2). Não usar "2024 recorde" para essa região.

### Slide 6: Beyond the dashboard
- **Título:** When a week turns critical, crews need a plan
- **Visual:** `docs/img/overview.jpg` (print real do mapa com prioridades e brigadas).
- 3 linhas:
  - Planner proposes which fires to attend first and with which crew
  - Critic challenges trade-offs; numbers come from deterministic tools, not the model
  - A human coordinator approves every dispatch
- Rodapé: *Tocantins demo: 179 fire occurrences, 6 crews at real stations (crew counts simulated)*

### Slide 7: NASA data, partners, links
- **Título:** Open data, open code
- **NASA data:** FIRMS MODIS C6.1 (Terra/Aqua) · FIRMS VIIRS 375 m (Suomi-NPP) · NASA Worldview
- **Next:** Pantanal and Gran Chaco, regions monitored by AEB/INPE (Brazil) and CONAE (Argentina)
- **Code:** github.com/ufsm-ecomp-genai/fococerto.spaceapps · Apache 2.0
- **Video:** [PREENCHER]
- Fecho: *From NASA data to crews on the ground.*

---

### Checklist antes de exportar
- [x] Exatamente 7 slides (ou menos)
- [x] Nomes dos integrantes no slide 1 (Fernando Dorneles da Silva, Enzo Augusto Mucha Domingues, Gabriel Mazui Azevedo, Eduardo Jacques Pereira, Lucas Lima Mendes)
- [x] Nenhum número sem fonte ("+240%" não pode aparecer)
- [x] Crédito "Imagery: NASA Worldview" no slide 2
- [x] Compartilhamento: *Anyone with the link can view*
- [x] PDF exportado e salvo no Drive
