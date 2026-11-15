# Manual Técnico: Produto de Fogo Ativo MODIS Collection 6.1 (MCD14 / MOD14 / MYD14)
## Referência Técnica Completa e Especificação de Dados da NASA

---

### 1. Visão Geral da Missão e Plataformas

* **Sensores:** MODIS (Moderate Resolution Imaging Spectroradiometer).
* **Satélites:**
  * **Terra (EOS AM-1):** Órbita heliossíncrona, cruzamento descendente no equador às ~10:30 (dia) e ~22:30 (noite).
  * **Aqua (EOS PM-1):** Órbita heliossíncrona, cruzamento ascendente no equador às ~13:30 (dia) e ~01:30 (noite).
* **Faixa de Varredura (Swath):** $2.330\text{ km}$ transversal à trajetória de órbita.
* **Resolução Espacial:** $1\text{ km}$ nominal no nadir ($1\text{ km} \times 1\text{ km}$).

---

### 2. Geometria de Varredura e o Efeito *Bow-Tie* (Distorção Geométrica)

O MODIS utiliza um espelho de varredura bilateral de rotação contínua. À medida que o ângulo de visada do sensor ($\theta$) aumenta em direção à borda da faixa (atingindo até $\pm 55^\circ$):

1. **Crescimento do Pixel no Eixo Transversal (Scan):**
   $$p_{\text{scan}} = p_0 \cdot \sec^2(\theta)$$
2. **Crescimento do Pixel no Eixo Longitudinal (Track):**
   $$p_{\text{track}} = p_0 \cdot \sec(\theta)$$
3. **Área do Pixel ($A$):**
   $$A(\theta) \approx A_0 \cdot \sec^3(\theta)$$

* No nadir ($\theta = 0^\circ$): $A = 1.0\text{ km}^2$.
* Na borda ($\theta = 55^\circ$): o pixel expande para $4.8\text{ km} \times 2.0\text{ km} \approx 9.6\text{ km}^2$.
* **Consequência para Detecção:** Nas bordas da imagem, múltiplos pixels se sobrepõem no chão (*bow-tie effect*), o que pode gerar duplicações aparentes de focos ou diluição de sinais fracos em áreas muito amplas.

---

### 3. Canais Espectrais Utilizados no Algoritmo

| Canal MODIS | Comprimento de Onda Central ($\lambda$) | Finalidade no Algoritmo de Fogo | Saturação |
|---|---|---|---|
| **Banda 21** | $3.959\text{ µm}$ (MIR - baixo ganho) | Medição de anomalias térmicas intensas e cálculo de FRP | Satura a ~$500\text{ K}$ |
| **Banda 22** | $3.959\text{ µm}$ (MIR - alto ganho) | Detecção de fogo sensível e medição de fundo | Satura a ~$331\text{ K}$ |
| **Banda 31** | $11.03\text{ µm}$ (TIR) | Temperatura de brilho da superfície e do topo das nuvens | Satura a ~$400\text{ K}$ |
| **Banda 32** | $12.02\text{ µm}$ (TIR) | Correção atmosférica e discriminação de nuvens | Satura a ~$400\text{ K}$ |
| **Banda 1** | $0.645\text{ µm}$ (Vermelho) | Rejeição de reflexão solar (*sun glint*) e nuvens | Não aplicável |
| **Banda 2** | $0.858\text{ µm}$ (NIR) | Detecção de corpos d'água e reflexão | Não aplicável |

---

### 4. Lógica de Detecção Contextual (Collection 6.1)

O algoritmo MODIS C6 avalia cada pixel através de dois testes principais:

#### A. Teste de Limiar Absoluto
Um pixel é classificado imediatamente como fogo potencial se:
* $T_{21} > 360\text{ K}$ (de dia) ou $T_{21} > 320\text{ K}$ (de noite).

#### B. Teste Contextual Bi-espectral Relativo
Se o pixel não atinge o limiar absoluto mas supera o ruído de fundo:
1. Define-se uma janela de contexto variável ($k \times k$, iniciando em $3 \times 3$ até $21 \times 21$ pixels válidos livres de água e nuvens).
2. Calcula-se a média ($\bar{T}_{21}$, $\bar{\Delta T}$) e o desvio absoluto da mediana ($\text{MAD}$) da vizinhança.
3. O pixel é classificado como fogo se:
   $$\Delta T > \bar{\Delta T} + 3.5 \cdot \text{MAD}(\Delta T) \quad \text{e} \quad \Delta T > \bar{\Delta T} + 6\text{ K}$$
   $$T_{21} > \bar{T}_{21} + 3.0 \cdot \text{MAD}(T_{21})$$
   $$T_{31} > \bar{T}_{31} + \text{MAD}(T_{31}) - 4\text{ K}$$

---

### 5. Cálculo do Fire Radiative Power (FRP)

No MODIS Collection 6.1, o FRP é calculado com base na formulação de radiação média empírica:

$$\text{FRP}_{\text{MODIS}} = \left(\frac{A_{\text{pixel}} \cdot \sigma}{a}\right) \cdot \left(L_{21} - \bar{L}_{21, \text{fundo}}\right) \quad [\text{MW}]$$

* $A_{\text{pixel}}$: área real do pixel calculada com base no ângulo de visada (em $\text{km}^2$).
* $\sigma$: constante de Stefan-Boltzmann ($5.6704 \times 10^{-8}\text{ W m}^{-2}\text{ K}^{-4}$).
* $a$: constante de conversão de radiância espectral ($a \approx 3.0 \times 10^{-9}\text{ W m}^{-2}\text{ sr}^{-1}\text{ µm}^{-1}\text{ K}^{-4}$).
* $L_{21}$: radiância espectral medida pelo canal 21.

---

### 6. Estrutura das Colunas nos Feeds CSV do NASA FIRMS

```csv
latitude,longitude,brightness,scan,track,acq_date,acq_time,satellite,confidence,version,bright_t31,frp,daynight
-10.1834,-48.3331,328.4,1.2,1.1,2024-09-15,1345,A,85,6.1NRT,298.2,34.7,D
```

* `confidence`: 0 a 100% (geralmente filtrado em $>30\%$ para nominal e $>80\%$ para alta confiança).
* `frp`: expresso em Megawatts (MW).
