# FocoCerto Harmonizer: Guia Operacional para Agentes de IA
## NASA International Space Apps Challenge 2026 — Desafio: Harmonization of MODIS and VIIRS Hot Spots

Este arquivo é a **âncora de contexto estático** lida automaticamente pelo Claude Code e outros agentes de IA no início de cada sessão.

---

### 1. Missão Central do Projeto
Reconciliar mais de duas décadas de dados de anomalias térmicas e queimadas da NASA (2000 a 2026), divididos entre o sensor **MODIS (Terra/Aqua, 1 km)** e o sensor **VIIRS (Suomi-NPP / NOAA-20 / NOAA-21, 375 m)**, construindo um **Fire Activity Calendar** interativo em aplicação web para identificar padrões históricos, condições incomuns e períodos críticos em áreas selecionadas, integrando-o ao motor de raciocínio tático de alocação de brigadas.

---

### 2. Onde Encontrar as Tarefas de Execução
* **Trilha dos Agentes (Código, Backend, Frontend e Testes):** Consulte [`tasks/agentes/`](tasks/agentes/)
  * `task-agente-01-harmonizacao-dados.md`: Algoritmo `app/data/harmonizacao.py`
  * `task-agente-02-motor-calendario.md`: Motor da série temporal `app/data/calendario.py`
  * `task-agente-03-componente-web-react.md`: Interface `web/app/src/FireCalendar.jsx`
  * `task-agente-04-testes-e-integracao.md`: Testes automatizados `pytest`
* **Trilha Humana (Design, Slides, Vídeo, Submissão):** Consulte [`tasks/humanas/`](tasks/humanas/)
* **Dossiê Científico e Manuais Oficiais:** Consulte [`docs/spaceapps/`](docs/spaceapps/)

---

### 3. Fórmulas e Princípios de Engenharia Inegociáveis

1. **Discrepância de Footprint (Área de 1 km vs 375 m):**
   * O pixel de 375m do VIIRS cobre $0.14\text{ km}^2$, enquanto o MODIS cobre $1.0\text{ km}^2$ no nadir (razão de área $~7.1\text{x}$).
   * O VIIRS detecta historicamente entre $3\text{x}$ e $4\text{x}$ mais focos pontuais. **NUNCA some as contagens de focos diretamente.**
2. **Equivalência e Conservação de FRP (Fire Radiative Power):**
   * Agregação em grade espacial regular de $0.1^\circ \times 0.1^\circ$ (~$11\text{ km}$).
   * No período de sobreposição ($t \ge 2012$):
     $$\text{FRP}_{\text{harm}} = \sum \text{FRP}_{\text{MODIS}} + \sum \text{FRP}_{\text{VIIRS}}$$
     $$N_{\text{harm}} = N_{\text{MODIS}} + 0.30 \cdot N_{\text{VIIRS}}$$
3. **Métrica de Anomalia do Calendário:**
   * Mediana histórica multi-decenal por semana do ano ($\tilde{\mu}_w$).
   * $Z_{\text{fire}} \ge 2.0$ ou atividade acima do Percentil 95 ($P_{95}$) sinalizam **Período Crítico / Anomalia Extrema**.

---

### 4. Stack Tecnológica e Comandos Chave

* **Linguagem Principal:** Python 3.12
* **Frontend:** React + Vite + Tailwind CSS (`web/app/`)
* **Execução em Modo Amostra (Offline / Sem chaves externas):**
  ```bash
  python -m app.cli --sample --cenario tocantins-escasso
  ```
* **Rodar Testes Automatizados:**
  ```bash
  pytest tests/ -v
  ```
* **Busca Rápida de Contexto Técnico nos Papers da NASA:**
  ```bash
  python scripts/context_finder.py "<termo de busca>"
  ```

---

### 5. Regras de Conduta do Agente
1. **Passos incrementais testados:** Toda função criada deve ter teste ou verificação real.
2. **Sem alucinação de dados:** Se os dados são simulados ou de amostra, declare como amostra.
3. **Sempre faça commit e envie:** Todo avanço relevante deve ser commitado e sincronizado no repositório `git@github.com:ufsm-ecomp-genai/fococerto.spaceapps.git`.
