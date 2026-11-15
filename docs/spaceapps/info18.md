# Recursos Oficiais do Desafio: Harmonização de Pontos Críticos MODIS e VIIRS
## (Challenge Resources: Harmonization of MODIS and VIIRS Hot Spots)

Este documento compila os recursos, links de dados, APIs e documentações científicas oficiais fornecidos pela **NASA**, **FIRMS**, **LANCE** e pela agência parceira **CONAE** (Comisión Nacional de Actividades Espaciales) para o desafio.

---

### 1. Plataforma Central de Dados: NASA FIRMS
O **FIRMS (Fire Information for Resource Management System)** é a fonte primária de dados de anomalias térmicas e focos de calor ativos (*active fires*):

* **Portal Principal:** [https://firms.modaps.eosdis.nasa.gov/](https://firms.modaps.eosdis.nasa.gov/)
* **Serviço de Download de Dados Históricos (Archive Download):**
  * Permite baixar a série temporal completa em CSV ou Shapefile por país ou caixa delimitadora (bounding box).
  * [https://firms.modaps.eosdis.nasa.gov/download/](https://firms.modaps.eosdis.nasa.gov/download/)
* **API de Dados em Tempo Quase Real (FIRMS NRT / MAP_KEY API):**
  * Acesso programático a focos ativos das últimas 24h a 7 dias em JSON/CSV.
  * Endpoint: `https://firms.modaps.eosdis.nasa.gov/api/area/csv/[MAP_KEY]/[SOURCE]/[EXTENT]/[DAYS]`
* **Serviços WMS / WFS / WMTS:**
  * Camadas OGC prontas para integração em mapas web (Leaflet, Mapbox, OpenLayers).

---

### 2. Coleções de Sensores e Detalhes dos Produtos

#### A. MODIS (Moderate Resolution Imaging Spectroradiometer)
* **Satélites:** Terra (passagem descendente matutina ~10:30) e Aqua (passagem ascendente vespertina ~13:30).
* **Coleção Oficial:** Collection 6.1 (MCD14DL / MOD14 / MYD14).
* **Resolução Espacial:** 1 km no nadir (expande em direção às bordas da faixa de varredura).
* **Série Histórica:** Novembro de 2000 até o presente (> 24 anos contínuos).
* **Atributos Chave:**
  * `latitude`, `longitude`: coordenadas do centro do pixel.
  * `brightness`: temperatura de brilho da banda 21/22 (em Kelvin).
  * `scan`, `track`: tamanho do pixel no momento da captura.
  * `acq_date`, `acq_time`: data e hora UTC da passagem.
  * `satellite`: `T` (Terra) ou `A` (Aqua).
  * `confidence`: confiança da detecção (0 a 100%).
  * `frp`: Fire Radiative Power (MW - Megawatts).
  * `daynight`: `D` (dia) ou `N` (noite).

#### B. VIIRS (Visible Infrared Imaging Radiometer Suite)
* **Satélites:**
  * Suomi-NPP (S-NPP, lançado em 2011, dados operacionais desde 2012).
  * NOAA-20 / JPSS-1 (lançado em 2017, dados desde 2018).
  * NOAA-21 / JPSS-2 (lançado em 2022, dados recentes).
* **Coleção Oficial:** 375 m Active Fire Product (VNP14IMGTDL para S-NPP; VJ114IMGTDL para NOAA-20; VJ214IMGTDL para NOAA-21).
* **Resolução Espacial:** 375 m (bandas I - Imagery) constante ao longo da faixa de varredura (*aggregation mode*).
* **Série Histórica:** Janeiro de 2012 até o presente (~14 anos).
* **Atributos Chave:**
  * `latitude`, `longitude`: coordenadas do centro do pixel de 375m.
  * `bright_ti4`: temperatura de brilho do canal I4 (em Kelvin).
  * `confidence`: categorizada em `low` (baixa), `nominal` (nominal) ou `high` (alta).
  * `frp`: Fire Radiative Power (MW).
  * `satellite`: `N` (Suomi-NPP), `1` (NOAA-20), `2` (NOAA-21).

---

### 3. Ferramentas de Visualização e Validação da NASA

* **NASA Worldview:**
  * Ferramenta interativa de mapeamento global com sobreposição de imagens de satélite reais e camadas de anomalias térmicas.
  * Link: [https://worldview.earthdata.nasa.gov/](https://worldview.earthdata.nasa.gov/)
  * *Uso no projeto:* Útil para validação visual de áreas com sobreposição simultânea de passagens MODIS e VIIRS.
* **Google Earth Engine (GEE) FIRMS Catalogs:**
  * `FIRMS: NASA/FIRMS/MODIS/C6_1`
  * `FIRMS: NASA/FIRMS/VIIRS/SNPP/C1`
  * Permite consultar a série temporal multi-decenal em nuvem via Python ou Javascript.

---

### 4. Guias de Usuário e Referências Científicas Oficiais

1. **MODIS Active Fire User Guide:**
   * Giglio, L., et al. *Collection 6 MODIS Active Fire Detection and Fire Radiative Power Assessment*. Remote Sensing of Environment.
2. **VIIRS 375 m Active Fire Algorithm:**
   * Schroeder, W., et al. *The New VIIRS 375 m Active Fire Detection Data Product: Algorithm Description and Initial Assessment*. Remote Sensing of Environment, 2014.
3. **Harmonização e Intercalibração de FRP:**
   * Papers de referência mostram que a relação de contagem de focos entre VIIRS 375m e MODIS 1km segue uma razão média entre 3:1 e 4:1 (devido à sensibilidade do pixel de 375m para fogos menores), mas o FRP integrado em células agregadas converge de forma muito mais estável.

---

### 5. Contribuição da Agência Parceira: CONAE (Argentina)
* A **CONAE** (Comisión Nacional de Actividades Espaciales) é a agência espacial parceira deste desafio no Space Apps 2026.
* A CONAE atua fortemente no monitoramento de risco e emergências ambientais na América do Sul, utilizando dados do FIRMS integrados com previsão meteorológica e índices de vegetação para o combate aos incêndios florestais no Gran Chaco, Pantanal e Patagônia.
* Citar a relevância e aplicação em biomas sul-americanos atende perfeitamente ao contexto da agência parceira.
