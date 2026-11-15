# Manual Técnico: Produto de Fogo Ativo VIIRS 375 m (VNP14IMGTDL / VJ114IMGTDL)
## Referência Técnica Completa e Comparativo com MODIS

---

### 1. Visão Geral do Sensor e Plataformas

* **Sensor:** VIIRS (Visible Infrared Imaging Radiometer Suite).
* **Satélites Operacionais:**
  * **Suomi-NPP (S-NPP):** Lançado em outubro de 2011; dados de fogo ativos desde janeiro de 2012. Cruzamento no equador às ~13:30 (dia) e ~01:30 (noite).
  * **NOAA-20 (JPSS-1):** Lançado em novembro de 2017; dados operacionais desde 2018. Órbita defasada em 50 minutos em relação ao S-NPP.
  * **NOAA-21 (JPSS-2):** Lançado em novembro de 2022; dados operacionais recentes.
* **Faixa de Varredura (Swath):** $3.040\text{ km}$ (garante cobertura global completa diária sem lacunas equatoriais).
* **Resolução Espacial:**
  * Bandas M (Moderate resolution): $750\text{ m}$.
  * Bandas I (Imagery resolution): **$375\text{ m}$ nominal**.

---

### 2. O Algoritmo de Agregação em 3 Zonas (Mitigação do Efeito *Bow-Tie*)

Ao contrário do MODIS, o sensor VIIRS possui um processamento a bordo de agregação de detectores que atenua o crescimento geométrico do pixel:

1. **Zona 1 (Nadir a $31.7^\circ$ de ângulo de visada):**
   * Agregação de $3 \times 1$ sub-amostras em 1 pixel final de $375\text{ m} \times 375\text{ m}$.
2. **Zona 2 ($31.7^\circ$ a $44.8^\circ$):**
   * Agregação de $2 \times 1$ sub-amostras.
3. **Zona 3 ($44.8^\circ$ até a borda em $56.3^\circ$):**
   * Sem agregação ($1 \times 1$).

* **Resultado Prático:** Enquanto o pixel do MODIS cresce em área até $9.6\text{x}$, o pixel do VIIRS cresce no máximo **$4\text{x}$** ($~800\text{ m} \times 800\text{ m}$ na borda extrema), mantendo uma consistência espacial sem precedentes.

---

### 3. Bandas Espectrais Utilizadas no Algoritmo 375m

| Canal VIIRS | Comprimento de Onda ($\lambda$) | Resolução | Função no Produto de Fogo | Saturação |
|---|---|---|---|---|
| **Banda I4** | $3.74\text{ µm} - 3.93\text{ µm}$ (MIR) | $375\text{ m}$ | Detecção primária de emissão térmica e FRP | Satura a ~$367\text{ K}$ |
| **Banda I5** | $10.5\text{ µm} - 12.4\text{ µm}$ (TIR) | $375\text{ m}$ | Contraste de temperatura superficial e nuvens | Satura a ~$380\text{ K}$ |
| **Banda M13** | $3.97\text{ µm} - 4.13\text{ µm}$ (MIR) | $750\text{ m}$ | Medição de FRP em fogos muito intensos que saturam I4 | Satura a ~$634\text{ K}$ |
| **Banda I1** | $0.60\text{ µm} - 0.68\text{ µm}$ (Visível) | $375\text{ m}$ | Máscara de reflexão solar e água | Não aplicável |

---

### 4. Categorias de Confiança no VIIRS 375m

Ao contrário do MODIS (que emite uma porcentagem numérica contínua de 0 a 100%), o produto VIIRS 375m classifica o fogo ativo em **três categorias discretas**:

1. **`low` (Baixa Confiança):**
   * Focos detectados apenas de dia em condições limítrofes, com alto potencial de reflexão solar ou temperatura próxima ao fundo. Frequentemente associados a queimadas agrícolas residuais ou falsos alarmes em superfícies quentes e nuvens finas.
2. **`nominal` (Confiança Nominal):**
   * A categoria padrão para a maioria dos incêndios florestais ativos e livres de contaminação solar.
3. **`high` (Alta Confiança):**
   * Focos de alta intensidade, tipicamente noturnos (onde não há interferência solar) ou com forte contraste térmico bi-espectral e saturação clara da banda I4.

---

### 5. Comparativo Direto: Por que a Harmonização é Obrigatória

| Característica | MODIS (Terra/Aqua) | VIIRS (S-NPP / NOAA) | Impacto na Análise Histórica |
|---|---|---|---|
| **Área do Pixel no Nadir** | $1.0\text{ km}^2$ | $0.14\text{ km}^2$ | O VIIRS enxerga uma área **$7.1\text{ vezes menor}$**, capturando fogos pequenos invisíveis ao MODIS. |
| **Sensibilidade Mínima de Fogo** | ~$100\text{ m}^2$ de queima ativa | ~$10\text{ m}^2$ de queima ativa | O VIIRS detecta focos com FRP de até $0.1\text{ MW}$, enquanto o MODIS exige $~5\text{ MW}$ para detecção segura. |
| **Proporção de Contagem** | $1.0\text{x}$ (Base) | $3.0\text{x} - 4.5\text{x}$ | Se somadas sem calibração, a série apresentará um salto artificial gigantesco a partir de 2012. |
| **Faixa de Cobertura Global** | Deixa lacunas equatoriais entre faixas adjacentes no mesmo dia | Cobertura global contínua diária | O VIIRS revisita todas as regiões tropicais sem lacunas de faixa. |

---

### 6. Estrutura dos Dados nos Feeds CSV do NASA FIRMS

```csv
latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,confidence,version,bright_ti5,frp,daynight
-10.1834,-48.3331,335.2,0.38,0.36,2024-09-15,1330,N,nominal,2.0NRT,296.8,12.4,D
```
