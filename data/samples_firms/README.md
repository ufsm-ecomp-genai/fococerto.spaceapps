# Datasets de Amostra NASA FIRMS: MODIS C6.1 e VIIRS 375m

Esta pasta contém pares de dados de teste idênticos em formato oficial do **NASA FIRMS** para validação imediata da camada de harmonização e teste do algoritmo sem depender de conexões externas.

---

### Arquivos Disponíveis

1. **`modis_sample_c6.csv`:**
   * 10 detecções pontuais do sensor MODIS (Aqua e Terra).
   * Colunas padrão: `latitude, longitude, brightness, scan, track, acq_date, acq_time, satellite, confidence, version, bright_t31, frp, daynight`.
   * Resolução: pixels de ~$1.1\text{ km} \times 1.2\text{ km}$.
   * FRP médio: ~$35\text{ MW}$ a $70\text{ MW}$.

2. **`viirs_sample_375m.csv`:**
   * 21 detecções pontuais do sensor VIIRS Suomi-NPP cobrindo os **mesmos eventos de queima** na mesma janela espaço-temporal.
   * Colunas padrão: `latitude, longitude, bright_ti4, scan, track, acq_date, acq_time, satellite, confidence, version, bright_ti5, frp, daynight`.
   * Resolução: pixels de ~$0.38\text{ km} \times 0.36\text{ km}$.
   * Relação observável: Cada cluster de 1 ou 2 pixels MODIS é mapeado para 2 a 3 sub-pixels VIIRS, confirmando na prática a proporção teórica de detecção de ~2.1:1 a 3.5:1 e a conservação aproximada do FRP total integrado.
