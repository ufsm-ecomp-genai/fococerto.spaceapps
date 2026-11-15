# Metodologia Científica de Harmonização MODIS e VIIRS
## Fundamentação Matemática, Calibração de FRP e Métricas de Anomalia

Este documento descreve a base científica adotada pelo **FocoCerto Harmonizer** para reconciliar as séries temporais de queimadas dos sensores MODIS (2000–presente) e VIIRS (2012–presente) do NASA FIRMS.

---

### 1. O Desafio Físico e Espacial

#### A. A Discrepância de Footprint do Pixel
* **MODIS:** Pixel nominal de $1.000\text{ m} \times 1.000\text{ m}$ ($1\text{ km}^2$) no nadir. Nas bordas da faixa de varredura (*scan edge*), devido à geometria óptica e curvatura da Terra, o pixel deforma-se e expande para até $4.8\text{ km} \times 2.0\text{ km}$ ($~9.6\text{ km}^2$).
* **VIIRS:** Pixel de $375\text{ m} \times 375\text{ m}$ ($0.14\text{ km}^2$) nas bandas I. O VIIRS aplica um esquema de agregação em 3 zonas ao longo da varredura, mantendo o tamanho do pixel quase uniforme até o final da faixa (no máximo $~0.8\text{ km} \times 0.8\text{ km}$).

$$\text{Razão de Área no Nadir: } \frac{\text{Área MODIS}}{\text{Área VIIRS}} = \frac{1.0\text{ km}^2}{0.1406\text{ km}^2} \approx 7.1$$

#### B. Sensibilidade e Contagem de Focos
Devido à sua área muito menor, o pixel do VIIRS detecta frentes de fogo menores, fogos agrícolas e queimadas fragmentadas com menor intensidade térmica (baixo FRP). 
* **Efeito na contagem bruta:** O VIIRS detecta historicamente entre **3 e 4 vezes mais focos pontuais** do que o MODIS na mesma área e momento.
* **Conclusão:** **Contagens brutas de detecções NÃO podem ser concatenadas diretamente.**

---

### 2. Nossa Metodologia de Harmonização em 3 Camadas

Para produzir um **Calendário de Atividade de Queimadas Contínuo e Estável (2000–2026)**, aplicamos:

```
[Pontos MODIS 1km (2000+)]   \
                               --> [Agregação em Grade Espacial 0.1°] --> [Calibração de FRP & Counts] --> [Série Harmonizada]
[Pontos VIIRS 375m (2012+)]  /
```

#### Camada 1: Agregação em Grade Espacial Regular (Spatial Binning)
Em vez de comparar pontos vetoriais discretos, agregamos os eventos em uma grade espacial uniforme de $0.1^\circ \times 0.1^\circ$ (~$11\text{ km} \times 11\text{ km}$) ou por polígono de Área de Interesse (AOI), agrupados por janela temporal semanal/mensal:

* $N_{\text{MODIS}}(t)$: contagem de focos MODIS no período $t$.
* $N_{\text{VIIRS}}(t)$: contagem de focos VIIRS no período $t$.
* $FRP_{\text{MODIS}}(t)$: energia radiativa acumulada medida pelo MODIS (MW).
* $FRP_{\text{VIIRS}}(t)$: energia radiativa acumulada medida pelo VIIRS (MW).

#### Camada 2: Modelo de Calibração Empírica Cruzada (Overlap 2012–2026)
Durante o período de sobreposição (2012 a 2026), ambos os sensores observam a Terra simultaneamente. Ajustamos uma relação de equivalência entre o sinal do VIIRS e a escala histórica do MODIS:

$$N_{\text{harmonizado}}(t) = 
\begin{cases} 
N_{\text{MODIS}}(t), & \text{se } t < 2012 \text{ (era pré-VIIRS)} \\
\alpha \cdot N_{\text{VIIRS}}(t) + (1 - \alpha) \cdot \beta \cdot N_{\text{MODIS}}(t), & \text{se } t \ge 2012 \text{ (período de sobreposição)}
\end{cases}$$

Onde $\beta$ é o fator de escala de contagem derivado da regressão na sobreposição ($\beta \approx 0.28 - 0.32$), normalizando a contagem do VIIRS para a escala equivalente do MODIS histórico.

Para a **Potência Radiativa do Fogo (FRP)**, a convergência é ainda mais consistente:

$$FRP_{\text{harmonizado}}(t) = \sum_{i \in \text{focos}} FRP_i \cdot \omega_{\text{sensor}}$$

Onde $\omega_{\text{sensor}}$ compensa o limite inferior de detecção do VIIRS para fontes fracas de baixa temperatura.

---

### 3. Cálculo da Linha de Base Histórica e Detecção de Anomalias

Para que o **Fire Activity Calendar** responda se a queima observada em uma semana do ano é normal ou crítica:

#### A. Linha de Base Climatológica Multi-decenal
Para cada semana do ano $w \in [1, 52]$ na Área de Interesse (AOI):
* **Mediana Histórica:** $\tilde{\mu}(w) = \text{mediana}\{ X(y, w) \mid y \in [2000, 2025] \}$
* **Percentil 90 (Alerta de Atenção):** $P_{90}(w)$
* **Percentil 95 (Alerta Crítico / Emergência):** $P_{95}(w)$
* **Desvio Absoluto da Mediana (MAD):** Para tratamento robusto contra outliers extremos.

#### B. Índice de Anomalia Térmica Normalizada ($Z_{\text{fire}}$)

$$Z_{\text{fire}}(y, w) = \frac{X(y, w) - \tilde{\mu}(w)}{\sigma_w}$$

* **Condição Normal ($Z < 1.0$):** Atividade dentro do padrão sazonal esperado.
* **Condição Incomum Moderada ($1.0 \le Z < 2.0$):** Atividade acima do percentil 75.
* **Condição Crítica / Extrema ($Z \ge 2.0$ ou $X > P_{95}$):** Picos severos de calor que demandam ativação imediata de brigadas e alerta de defesa civil.
