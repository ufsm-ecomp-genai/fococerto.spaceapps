# Síntese dos Treinamentos Oficiais NASA ARSET: Monitoramento de Queimadas
## (Applied Remote Sensing Training: Satellite Remote Sensing of Wildfires & Air Quality)

---

### 1. Sobre o Programa NASA ARSET

O **NASA ARSET (Applied Remote Sensing Training)** é o programa oficial da NASA para capacitar gestores de desastres ambientais, brigadistas, tomadores de decisão governamentais e pesquisadores no uso prático dos dados de Observação da Terra.

---

### 2. Tópicos Centrais dos Módulos de Incêndios Florestais

#### Módulo 1: Detecção de Anomalias Térmicas e Ciclo Diurno do Fogo
* **O Ciclo Diurno:** Na maior parte dos ecossistemas terrestres, a intensidade do fogo e a taxa de queima atingem o pico entre **13:00 e 15:00** (horário solar local), quando a temperatura do ar é mais alta e a umidade relativa do ar é mínima.
* **Cobertura Polar:**
  * O satélite **Terra (MODIS)** passa pela manhã (~10:30), capturando o início da ignição e da propagação.
  * O satélite **Aqua (MODIS)** e os satélites **Suomi-NPP / NOAA-20 / NOAA-21 (VIIRS)** passam no início da tarde (~13:30), registrando o pico térmico de comportamento extremo.
* **Passagens Noturnas (~01:30):**
  * Fundamentais para detectar **reignições** e avaliar se o incêndio continuou ativo mesmo sob inversão térmica ou arrefecimento noturno. O VIIRS se destaca na detecção noturna devido à ausência total de contaminação por reflexão solar.

#### Módulo 2: Limitações Físicas que Todo Gestor Precisa Saber
1. **Nuvens Espessas e Chuva:** Sensores ópticos e térmicos infravermelhos (MIR/TIR) **não enxergam através de nuvens densas**. Um dia com zero focos detectados pode significar apenas que a região estava encoberta por tempestades.
2. **Fumaça Densa:** Fumaça leve ou névoa seca não bloqueia a janela de $4\text{ µm}$, mas colunas densas de fumaça convectiva pirocumulonimbus (*pyrocumulonimbus*) atenuam o sinal de radiância, subestimando o FRP no nadir.
3. **Focos Sob Dossel Florestal Fechado:** Em florestas tropicais primárias densas (Amazônia), o fogo de sub-bosque rasteiro pode ter parte de sua radiação térmica retida pelas copas das árvores, sendo detectado com menor FRP do que incêndios em campos abertos ou savanas (Cerrado/Pantanal).

#### Módulo 3: Da Detecção ao Alerta Operacional
* A NASA enfatiza que um foco de calor em um mapa não é uma recomendação de ação.
* O valor de um sistema de alerta reside em cruzar a detecção térmica com:
  1. **Vulnerabilidade e Bens a Proteger:** Proximidade de vilas rurais, unidades de conservação, terras indígenas e infraestruturas críticas.
  2. **Condições Meteorológicas:** Velocidade e direção do vento, e déficit de pressão de vapor (VPD).
  3. **Histórico e Recorrência:** Saber se o fogo atual é uma queimada agrícola sazonal autorizada ou um incêndio descontrolado e anômalo.

---

### 3. Aplicação no Projeto
* O FocoCerto implementa exatamente essa ponte exigida pela NASA ARSET: não apenas mostrar os focos no mapa, mas contextualizar o risco frente à vulnerabilidade humana e recomendar a alocação de brigadas com base na severidade e anomalia do evento.
