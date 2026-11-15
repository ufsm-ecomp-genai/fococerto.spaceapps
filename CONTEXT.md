# CONTEXT.md — Dicionário de Arquitetura, Dados e Fórmulas
## FocoCerto Harmonizer (NASA Space Apps Challenge 2026)

Este documento condensa os esquemas de dados, modelos matemáticos, contratos de código e arquitetura para referência rápida durante o desenvolvimento.

---

### 1. Esquemas de Dados do NASA FIRMS

#### A. MODIS Collection 6.1 (1 km)
* **Arquivo de Amostra:** `data/samples_firms/modis_sample_c6.csv`
* **Colunas Oficiais:**
  * `latitude` (float): Coordenada geográfica WGS84 (-90.0 a 90.0).
  * `longitude` (float): Coordenada geográfica WGS84 (-180.0 a 180.0).
  * `brightness` (float): Temperatura de brilho do canal 21/22 em Kelvin ($T_{21}$).
  * `scan`, `track` (float): Dimensões reais do pixel projetado no chão (em km).
  * `acq_date` (string `YYYY-MM-DD`): Data da aquisição UTC.
  * `acq_time` (string `HHMM`): Horário da aquisição UTC.
  * `satellite` (string): `'T'` (Terra - manhã) ou `'A'` (Aqua - tarde).
  * `confidence` (int): Confiança da detecção (0 a 100%).
  * `bright_t31` (float): Temperatura de brilho do canal 31 em Kelvin ($T_{31}$).
  * `frp` (float): Fire Radiative Power em Megawatts (MW).
  * `daynight` (string): `'D'` (Dia) ou `'N'` (Noite).

#### B. VIIRS 375 m (Suomi-NPP / NOAA-20 / NOAA-21)
* **Arquivo de Amostra:** `data/samples_firms/viirs_sample_375m.csv`
* **Colunas Oficiais:**
  * `latitude`, `longitude` (float): Centro do pixel de 375m.
  * `bright_ti4` (float): Temperatura de brilho da banda I4 em Kelvin ($T_{\text{I4}}$).
  * `scan`, `track` (float): Dimensões do pixel (mantém-se entre 0.36 km e 0.8 km graças à agregação 3 zonas).
  * `acq_date`, `acq_time` (string): Data e hora UTC.
  * `satellite` (string): `'N'` (Suomi-NPP), `'1'` (NOAA-20), `'2'` (NOAA-21).
  * `confidence` (string): `'low'`, `'nominal'`, ou `'high'`.
  * `bright_ti5` (float): Temperatura de brilho da banda I5 em Kelvin ($T_{\text{I5}}$).
  * `frp` (float): Fire Radiative Power em Megawatts (MW).
  * `daynight` (string): `'D'` (Dia) ou `'N'` (Noite).

---

### 2. Contrato do Dataset Padronizado Unificado

Tanto o MODIS quanto o VIIRS devem ser convertidos na memória para uma estrutura homogênea:

```python
{
    "id": str,                 # Hash único: f"{sensor}_{sat}_{lat:.4f}_{lon:.4f}_{data}_{hora}"
    "sensor": str,             # "MODIS" ou "VIIRS"
    "satelite": str,           # "Terra", "Aqua", "Suomi-NPP", "NOAA-20", "NOAA-21"
    "lat": float,
    "lon": float,
    "data_hora_utc": datetime, # Datetime parsed
    "ano": int,
    "mes": int,                # 1 a 12
    "semana": int,             # 1 a 52 (ISO calendar week)
    "dia_noite": str,          # "D" ou "N"
    "confianca_pct": float,    # 0 a 100 (VIIRS: low=30, nominal=65, high=90)
    "frp_mw": float            # Megawatts
}
```

---

### 3. Modelo Matemático da Harmonização

#### A. Célula de Grade Espacial ($0.1^\circ \times 0.1^\circ$)
Agrupamento espacial que neutraliza o efeito da geometria óptica:
```python
def obter_celula_grade(lat: float, lon: float, step: float = 0.1) -> tuple[float, float]:
    return (round(lat / step) * step, round(lon / step) * step)
```

#### B. Fusão e Calibração Temporal
Para cada célula de grade e intervalo temporal $t$ (semanal ou mensal):
* **FRP Harmonizado:** Soma conservativa da energia radiativa total:
  $$\text{FRP}_{\text{harm}}(t) = \sum_{i \in \text{MODIS}} \text{FRP}_i + \sum_{j \in \text{VIIRS}} \text{FRP}_j$$
* **Contagem de Focos Harmonizada (Equivalência MODIS-like):**
  $$N_{\text{harm}}(t) = 
  \begin{cases} 
  N_{\text{MODIS}}(t), & \text{se } t < 2012 \\
  N_{\text{MODIS}}(t) + 0.30 \cdot N_{\text{VIIRS}}(t), & \text{se } t \ge 2012 
  \end{cases}$$

#### C. Linha de Base Climatológica e Detecção de Anomalias ($Z_{\text{fire}}$)
Para cada semana do ano $w \in [1, 52]$:
* **Mediana Histórica Multi-decenal:**
  $$\tilde{\mu}_w = \text{mediana}\{ N_{\text{harm}}(y, w) \mid y \in [2000, 2025] \}$$
* **Desvio Absoluto da Mediana (MAD):**
  $$\text{MAD}_w = \text{mediana}\{ |N_{\text{harm}}(y, w) - \tilde{\mu}_w| \}$$
  $$\sigma_w \approx 1.4826 \cdot \text{MAD}_w$$
* **Índice de Anomalia Normalizado:**
  $$Z_{\text{fire}}(y, w) = \frac{N_{\text{harm}}(y, w) - \tilde{\mu}_w}{\sigma_w}$$
* **Classificação de Status:**
  * $Z < 1.0$: `"NORMAL"`
  * $1.0 \le Z < 2.0$: `"ATENCAO"`
  * $Z \ge 2.0$ ou $> P_{95}$: `"CRITICO"` (Alerta de Emergência)

---

### 4. Contrato da Saída JSON para o Frontend (`dados_calendario.json`)

```json
{
  "regiao": "tocantins",
  "nome_exibicao": "Tocantins / Cerrado",
  "ano_inicio": 2000,
  "ano_fim": 2026,
  "gerado_em_utc": "2026-11-15T19:40:00Z",
  "matriz": [
    {
      "ano": 2024,
      "mes": 9,
      "semana": 37,
      "focos_harmonizados": 3482.4,
      "focos_modis_bruto": 1840,
      "focos_viirs_bruto": 5474,
      "frp_total_mw": 58490.2,
      "mediana_historica": 1024.0,
      "desvio_percentual": 240.1,
      "z_score": 3.84,
      "status": "CRITICO",
      "alerta": "Extreme thermal anomaly: +240% above 24-year historical median"
    }
  ]
}
```
