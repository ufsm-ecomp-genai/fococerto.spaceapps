# Desafio Oficial NASA Space Apps 2026
## Harmonization of MODIS and VIIRS Hot Spots (Desafio 15)

**Categoria:** Earth Science / Software  
**Nível de Dificuldade:** Advanced / Intermediate  
**Agências Parceiras:** NASA & CONAE (Comisión Nacional de Actividades Espaciales, Argentina)  

---

### 1. Resumo do Desafio (Challenge Statement)

Compreender como a atividade de queimadas se distribui pelo planeta ao longo do tempo — incluindo incêndios florestais e queimadas agrícolas intensas o suficiente para serem detectadas por sensores orbitais — permite antecipar períodos críticos, orientar esforços de monitoramento e melhorar a resposta a emergências.

Satélites rastreiam anomalias térmicas (*hot spots*) há mais de duas décadas, mas o registro histórico está dividido entre sensores cujos dados não podem ser comparados diretamente (MODIS e VIIRS), deixando os gestores sem uma visão histórica consistente.

**O Desafio:** Construir uma aplicação web que harmonize esses registros em um **Calendário de Atividade de Fogo (Burning Activity Calendar)** baseado em focos de calor ativos, permitindo que socorristas, cientistas e gestores ambientais examinem padrões históricos de fogo, condições incomuns e períodos críticos em uma área de interesse selecionada.

---

### 2. Contexto Científico (Background)

#### Regimes de Fogo
Alguns ecossistemas necessitam de fogo periódico para manter sua função e estrutura ecológica. No entanto, mudanças na intensidade, extensão e frequência do fogo causam impactos negativos severos no clima, na sociedade e na biodiversidade. Com o avanço das mudanças climáticas, condições meteorológicas propícias ao fogo (*fire weather*) tornam-se cada vez mais comuns e extremas.

#### Detecção e Monitoramento por Satélite
Satélites de Observação da Terra (EO) operando no infravermelho médio (MIR) e termal (TIR) detectam a radiação emitida pela combustão ativa na superfície terrestre. Sensores como MODIS e VIIRS fornecem detecção de anomalias térmicas em tempo quase real (NRT).

#### A Descontinuidade MODIS vs. VIIRS
* **MODIS (Terra e Aqua):** Fornece mais de duas décadas de observações contínuas desde 2000 (resolução espacial de 1 km), mas seus satélites estão sofrendo deriva orbital e se aproximando do fim da vida operacional.
* **VIIRS (Suomi-NPP, NOAA-20, NOAA-21):** É o sucessor operacional com resolução espacial de 375 m (área de pixel ~7.1x menor), detectando cerca de 3x a 4x mais focos para o mesmo evento.
* **O Problema:** Os registros não podem ser comparados diretamente sem uma metodologia formal de harmonização espacial, calibração radiativa e reconciliação temporal.

---

### 3. Objetivos do Projeto (Objectives)

O desafio divide-se em duas grandes frentes integradas:

1. **Harmonização de Dados MODIS + VIIRS:**
   * Agregar e compatibilizar as observações do NASA FIRMS de modo que o sensor de origem seja reconciliado e a análise de tendências, padrões e anomalias torne-se contínua de 2000 até o presente.
2. **Aplicação Web Interativa (Fire Activity Calendar):**
   * Desenvolver uma ferramenta visual onde o usuário seleciona uma região (AOI) e visualiza uma matriz temporal (anos × semanas/meses).
   * Identificar visualmente desvios em relação à mediana histórica multi-anual e sinalizar períodos críticos de anomalia extrema.
   * Oferecer exportação dos dados harmonizados e filtrados em formato tabular (CSV).

---

### 4. Considerações de Design e Funcionalidade
* **Público-alvo:** Brigadistas, socorristas de defesa civil, cientistas, gestores de unidades de conservação e tomadores de decisão em salas de situação.
* **Paleta de Cores Acessível:** Uso de rampas cromáticas acessíveis para daltônicos (ex.: escala viridis, cividis ou paleta perceptualmente uniforme de alerta).
* **Métricas Relevantes:** Comparação de anomalias contra médias e medianas históricas multi-anuais, desvio absoluto e contagem de focos ativos.
