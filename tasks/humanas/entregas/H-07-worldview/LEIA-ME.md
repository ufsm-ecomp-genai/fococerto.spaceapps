# H-07: Imagens do NASA Worldview

Obtidas pela API pública de snapshots do Worldview (`wvs.earthdata.nasa.gov/api/v1/snapshot`), sem edição além do
recorte e da ampliação (vizinho mais próximo, para não borrar os pixels).

| Arquivo | Camadas | Área (lat, lon) |
|---|---|---|
| `..._tocantins_VIIRS_visao_geral.png` | Terra true color + VIIRS S-NPP 375 m | bbox do Tocantins (-13..-8, -49.5..-45.5) |
| `..._jalapao_MODIS.png` / `_VIIRS.png` | Aqua true color + MODIS (Terra+Aqua) / VIIRS S-NPP | -10.45..-9.85, -46.2..-45.6 |
| `..._jalapao_zoom_MODIS.png` / `_VIIRS.png` | idem | -10.24..-10.04, -46.04..-45.84 |

- **Data:** 15/09/2024, a mesma das amostras em `data/samples_firms/`.
- **Contagem no recorte ampliado (arquivo FIRMS, mesmo dia):** MODIS 7 detecções, VIIRS 28, ou seja 4×.
- **Crédito obrigatório no slide:** "Imagery: NASA Worldview". Sem logo da NASA.
- **Para refazer no navegador:** worldview.earthdata.nasa.gov, data 2024-09-15, camadas "Corrected Reflectance (True Color)
  Aqua/MODIS" + "Fires and Thermal Anomalies" MODIS e VIIRS S-NPP, zoom em 10,1°S 45,9°W.
