# Guia de Trabalho — Papel 4: Design & Apresentação Oficial (7 Slides)
**Responsável:** Eduardo Jacques Pereira  
**Foco:** Pitch Deck Oficial de 7 Slides (PDF/PPTX) e Narrativa Visual

> [!WARNING]
> **Regra Absoluta da NASA:** A apresentação NÃO PODE ter mais de **7 slides** no total (incluindo capa e encerramento). Slides além do 7º causam desclassificação automática da avaliação global. Todo o texto DEVE estar em **Inglês**.

---

### 1. Sua Missão no Time
Criar a apresentação de slides oficial do projeto no **Google Slides** ou **Canva**, exportar como PDF público / link aberto, e entregar os materiais visuais para a submissão.

---

### 2. Identidade Visual Recomendada
* **Paleta de Cores:**
  * Fundo: Dark Mode elegante (Azul petróleo escuro `#0B132B` ou Cinza escuro `#1E293B`).
  * Destaques de Fogo: Laranja vibrante (`#F97316`) e Âmbar (`#F59E0B`).
  * Textos: Branco (`#FFFFFF`) e Cinza claro (`#E2E8F0`).
  * Alertas Críticos: Carmim/Magenta suave (`#E11D48`).
* **Tipografia:** Sans-serif limpa e moderna (Inter, Roboto ou Montserrat).
* **Importante:** **NUNCA use o logotipo oficial da NASA (o "meatball" azul ou "worm" vermelho)** nem bandeiras dos EUA sem autorização (conforme as Brand Guidelines de `info3.md`). Use o logo da sua equipe ou do Space Apps 2026.

---

### 3. Conteúdo Exato Slide a Slide (Copie e Cole)

#### Slide 1: Capa & Identidade
* **Título:** `FocoCerto Harmonizer`
* **Subtítulo:** `Active Fire Activity Calendar & Tactical Dispatch from NASA FIRMS`
* **Equipe:** `Team ECOMP - UFSM`
* **Desafio:** `NASA Space Apps Challenge 2026 — Harmonization of MODIS and VIIRS Hot Spots`
* **Tagline:** *"Bridging two decades of satellite observations to protect vulnerable ecosystems."*

#### Slide 2: O Problema (The Problem)
* **Título:** `The Two-Decade Satellite Dilemma`
* **Pontos Chave:**
  * **The Split Record:** Satellites tracked fires for 24+ years, but the record is split between MODIS (1 km pixel, 2000–present) and VIIRS (375 m pixel, 2012–present).
  * **The False Trend Trap:** VIIRS detects $3\text{x}$ to $4\text{x}$ more hotspots due to its smaller footprint. Raw aggregation creates artificial spikes, distorting long-term trends.
  * **The Operational Gap:** Fire managers lack a unified baseline to answer: *"Is today's burning an expected seasonal pattern or a critical anomaly demanding emergency dispatch?"*

#### Slide 3: A Solução (The Solution)
* **Título:** `FocoCerto Harmonizer: From Space to Action`
* **Visual:** Diagrama do fluxo: `NASA Data (MODIS & VIIRS) -> Harmonization Engine -> Fire Activity Calendar -> Reasoning Agents -> Tactical Decision`.
* **Destaques:**
  * **Continuous Time Series:** Unified multi-decadal record (2000–2026).
  * **Interactive Web Calendar:** Accessible matrix visualization tracking seasonal baselines, unusual conditions, and critical peak windows.
  * **Operational Decision Support:** Directly triggers tactical brigade allocation when anomalies emerge.

#### Slide 4: Metodologia Científica (Science & Validation)
* **Título:** `Cross-Sensor Harmonization Methodology`
* **Conteúdo:**
  * **Spatial Footprint Normalization:** Agregação em grade uniforme de $0.1^\circ \times 0.1^\circ$ (~11 km), anulando a distorção angular de varredura (*bow-tie effect*).
  * **FRP Energy Conservation:** While pixel counts diverge, integrated Fire Radiative Power (MW) converges physically ($M_b = C_e \cdot \text{FRE}$).
  * **Statistical Baseline & Anomaly Metric:**
    * Multi-year climatological median for every week of the year.
    * Normalized anomaly index: $Z_{\text{fire}} \ge 2.0$ and 95th percentile trigger critical emergency status.

#### Slide 5: Aplicação Web (The Fire Activity Calendar Web App)
* **Título:** `Intuitive, Actionable Web Interface`
* **Visual:** Screenshot grande e nítido da aplicação web mostrando:
  * Seletor de Área de Interesse (AOI - Tocantins / Pantanal).
  * Matriz anual x mensal/semanal colorida por intensidade harmonizada.
  * Card de detalhe de anomalia exibindo: *"September 2024: +240% above 24-year median — CRITICAL ALERT"*.

#### Slide 6: O Diferencial Operacional (Beyond Passive Dashboards)
* **Título:** `Actionable Early Warning & Field Response`
* **Conteúdo:**
  * **Most solutions stop at charts:** We take the next step.
  * **AI Reasoning Engine (Planner + Critic):** When a critical anomaly is flagged on the calendar, our system calculates distance, vulnerable rural communities, wind conditions, and generates an audited brigade dispatch plan.
  * **Human-in-the-Loop:** Clear justifications protecting firefighters and maximizing resource efficiency.

#### Slide 7: Dados da NASA, Parcerias & Conclusão
* **Título:** `Open Science, Global Impact`
* **Conteúdo:**
  * **NASA Earthdata Used:** FIRMS Active Fire (MODIS C6.1 MCD14DL & VIIRS 375m VNP14IMGTDL / VJ114IMGTDL).
  * **Space Agency Partner:** Grounded in regional wildfire monitoring context with CONAE (Argentina) and AEB (Brazil).
  * **Open Source Commitment:** OSI-compliant Apache 2.0 license.
  * **Links:** `GitHub: [Link Público] | Live Demo: [Link]`
  * **Encerramento:** *"Turning satellite data into timely, lifesaving action."*

---

### 4. O Que Entregar para a Pessoa 5 (Formulário)
1. **Link público do Google Slides** (configurado como "Qualquer pessoa com o link pode visualizar").
2. **PDF exportado dos 7 slides** salvo na nuvem como backup.
