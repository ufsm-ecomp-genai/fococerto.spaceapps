# Documentação da API do NASA FIRMS & Protocolos de Acesso
## Especificação de Endpoints, Autenticação e Formatos de Saída

---

### 1. Visão Geral da API REST do FIRMS

O **FIRMS (Fire Information for Resource Management System)** fornece endpoints REST para consulta programática de focos ativos recentes (últimos 1 a 10 dias) e um serviço de download em lote para o arquivo histórico completo de 2000 até hoje.

* **Base URL da API NRT:** `https://firms.modaps.eosdis.nasa.gov/api/`
* **Autenticação:** Requer uma chave gratuita de 32 caracteres (`MAP_KEY`), obtida via cadastro no portal NASA Earthdata.

---

### 2. Endpoints Principais

#### A. Consulta por Área Geográfica (Bounding Box)
Retorna todos os focos detectados dentro de uma caixa delimitadora em um intervalo recente:

```http
GET /api/area/csv/{MAP_KEY}/{SOURCE}/{BBOX}/{DAYS}
```

* **Parâmetros:**
  * `{MAP_KEY}`: Chave de API de 32 caracteres.
  * `{SOURCE}`: Fonte do sensor:
    * `MODIS_NRT`: MODIS Terra e Aqua Collection 6.1 (1 km).
    * `VIIRS_SNPP_NRT`: VIIRS 375m a bordo do Suomi-NPP.
    * `VIIRS_NOAA20_NRT`: VIIRS 375m a bordo do NOAA-20 (J1).
    * `VIIRS_NOAA21_NRT`: VIIRS 375m a bordo do NOAA-21 (J2).
    * `LANDSAT_NRT`: Landsat 8/9 Operational Land Imager (30m).
  * `{BBOX}`: Coordenadas em graus decimais (WGS84): `minLon,minLat,maxLon,maxLat`. Exemplo Tocantins/Cerrado: `-51,-14,-46,-5`.
  * `{DAYS}`: Número de dias retroativos a consultar (inteiro de `1` a `10`).

#### B. Consulta por País (Country Code ISO-3166)
```http
GET /api/country/csv/{MAP_KEY}/{SOURCE}/{COUNTRY_CODE}/{DAYS}
```
Exemplo para o Brasil: `/api/country/csv/{MAP_KEY}/MODIS_NRT/BRA/3`

#### C. Disponibilidade de Dados em Tempo Real (Disponibility Feed)
```http
GET /api/data_availability/csv/{MAP_KEY}/{SOURCE}
```
Informa os grânulos de satélite mais recentes processados e disponíveis no sistema.

---

### 3. Feeds Públicos Abertos sem Necessidade de MAP_KEY

Para acesso rápido a dados globais das últimas 24h, 48h ou 7 dias, a NASA mantém arquivos CSV públicos e compactados atualizados continuamente:

* **VIIRS Suomi-NPP 375m:**
  `https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_{janela}.csv`
* **MODIS Collection 6.1 (1km):**
  `https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_Global_{janela}.csv`
* **VIIRS NOAA-20 375m:**
  `https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_Global_{janela}.csv`
* *Onde `{janela}` pode ser `24h`, `48h` ou `7d`.*

---

### 4. Camadas de Visualização Cartográfica (WMS / WMTS)

Para integração direta em mapas web (Leaflet / OpenLayers):
* **Endpoint WMS:**
  `https://firms.modaps.eosdis.nasa.gov/wms/key/{MAP_KEY}/?SERVICE=WMS&REQUEST=GetMap&LAYERS=fires_viirs_24,fires_modis_24&FORMAT=image/png`
* Permite sobrepor as detecções das últimas 24 horas diretamente sobre mapa base cartográfico.
