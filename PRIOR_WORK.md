# Declaração Formal de Trabalho Prévio (Prior Work Disclosure)
## NASA International Space Apps Challenge 2026
**Desafio:** Harmonization of MODIS and VIIRS Hot Spots  
**Equipe:** ECOMP - UFSM (Universidade Federal de Santa Maria, RS, Brasil)  
**Integrantes:** Fernando Dorneles da Silva, Enzo Augusto Mucha Domingues, Gabriel Mazui Azevedo, Eduardo Jacques Pereira, Lucas Lima Mendes  
**Licença do Projeto:** Apache License 2.0 (Open Source / OSI-compliant)

---

### 1. Declaração de Conformidade com as Regras da NASA

Em estrito cumprimento às **Regras Oficiais do NASA International Space Apps Challenge** (Seção *Project Submission and Open Source Requirements*), esta declaração estabelece de forma pública, inequívoca e auditável a fronteira exata entre o código/arquitetura pré-existente e os avanços, algoritmos e componentes desenvolvidos exclusivamente durante o hackathon de 2026.

---

### 2. Matriz de Demarcação de Autoria

| Componente / Módulo | Origem / Trabalho Prévio (Base) | Desenvolvido no Hackathon NASA Space Apps 2026 |
| :--- | :--- | :--- |
| **Pipeline de Harmonização Espacial e Radiativa** (`app/data/harmonizacao.py`) | *Nenhum.* Inexistente no projeto original. | **100% NOVO:** Algoritmo de discretização em grade espacial $0.1^\circ \times 0.1^\circ$, mapeamento de confiança multinível (MODIS numérico para float; VIIRS categórico low/nominal/high), fator de escala empírico ($0.30 \cdot N_{\text{VIIRS}}$) para equivalência de contagem e fusão conservativa de Fire Radiative Power ($\text{FRP}_{\text{harm}} = \sum \text{FRP}_{\text{MODIS}} + \sum \text{FRP}_{\text{VIIRS}}$). |
| **Motor de Séries Temporais e Climatologia** (`app/data/calendario.py`) | *Nenhum.* Inexistente no projeto original. | **100% NOVO:** Matriz temporal multidecenal (2000–2026, 24 anos), cálculo da mediana climatológica por semana ($\tilde{\mu}_w$), Desvio Absoluto da Mediana (MAD), limiares de percentil ($P_{90}$, $P_{95}$) e cálculo do índice de anomalia normalizado $Z_{\text{fire}}$. |
| **Fire Activity Calendar Web UI** (`web/app/src/FireCalendar.jsx`) | *Nenhum.* Inexistente no projeto original. | **100% NOVO:** Interface de matriz térmica (heatmap interativo 2000–2026), filtros de granularidade (semanal/mensal), curvas de linha de base histórica vs. ano atual e botão de acionamento tático que injeta cenários de queima crítica no grafo de despacho. |
| **Scripts de Ingestão e Amostragem FIRMS** (`scripts/ingestao_firms.py`, `data/samples_firms/`) | *Nenhum.* Inexistente no projeto original. | **100% NOVO:** Pipelines de download e processamento de dados brutos do NASA FIRMS API / NRT para MODIS C6.1 e VIIRS 375m (Suomi-NPP, NOAA-20, NOAA-21). |
| **Suite de Testes Científicos** (`tests/test_harmonizacao.py`) | *Nenhum.* Inexistente no projeto original. | **100% NOVO:** Testes unitários com `pytest` cobrindo consistência de grade, conservação de FRP e detecção de anomalias com dados reais do Cerrado/Tocantins. |
| **Orquestrador Multi-Agente de Raciocínio Tático** (`app/agentes/`) | **Código Base Pré-Existente:** Estrutura geral de agentes de raciocínio autônomo (Planner, Critic, Tool-Calling) desenvolvida para alocação de recursos em brigadas de incêndio florestal. | **ADAPTADO:** Enriquecimento do prompt do Planner e do Critic para consumir o índice $Z_{\text{fire}}$ e o FRP harmonizado do Calendário de Atividades como gatilhos primários de severidade no despacho. |
| **Servidor de API e Rotas Base** (`app/api.py`, `app/tipos.py`) | **Código Base Pré-Existente:** Esqueleto FastAPI para servir respostas do orquestrador de agentes e modelos Pydantic básicos. | **EXPANDIDO:** Novas rotas dedicadas (`/api/calendario`, `/api/harmonizacao`) e modelos de dados para séries temporais do FIRMS. |

---

### 3. Licenciamento e Acesso Aberto

* O projeto é distribuído integralmente sob os termos da **Apache License, Version 2.0**.
* O texto completo da licença encontra-se no arquivo [`LICENSE`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/LICENSE) na raiz do repositório, atribuído a:
  ```
  Copyright 2026 Team ECOMP - UFSM (Universidade Federal de Santa Maria, Brazil)
  ```
* Todo o código-fonte, dados abertos e documentação são públicos e auditáveis no repositório GitHub da equipe.
