# Resumo Analítico: Sofiev & Kouznetsov (2020)
## "Analytical observation operators for MODIS and VIIRS fire radiative power products"
*Atmospheric Chemistry and Physics*, 20(24), 15443-15462.

---

### 1. O Problema da Não-Harmonização em Modelos de Previsão

Modelos de previsão climática e qualidade do ar (como o CAMS da União Europeia e o GEOS-Chem da NASA) dependem de dados de fogo ativo para calcular a injeção diária de fumaça, fuligem e aerossóis na atmosfera.
A substituição paulatina do MODIS pelo VIIRS criava uma grave quebra instrumental nas previsões: sem um operador de observação analítico, os modelos interpretavam a maior sensibilidade do VIIRS como uma explosão real de queima de biomassa.

---

### 2. O Conceito de Operador de Observação Analítico (*Analytical Observation Operator*)

Sofiev & Kouznetsov formularam um modelo matemático rigoroso que calcula a probabilidade de detecção de um fogo ativo como uma função contínua de:
1. **Intensidade Real do Fogo:** Potência radiativa verdadeira da frente de chamas ($P_{\text{real}}$).
2. **Área Instantânea de Visada do Detector:** Pegada elíptica projetada do pixel ($A_{\text{instant}}$).
3. **Ângulo Zenital de Observação ($\theta$):** Efeito de degradação da sensibilidade rumo à borda da varredura.
4. **Ruído e Variabilidade do Fundo Térmico ($\sigma_{\text{bg}}$).**

#### A Função de Sensibilidade do Limiar Mínimo de Detecção
O limite inferior de potência radiativa que um pixel de área $A$ consegue detectar acima do ruído térmico de fundo segue uma relação aproximadamente linear com a área do pixel:

$$P_{\text{limiar}}(A) \propto \gamma \cdot A \cdot \sigma_{\text{bg}}$$

Como a área média do pixel MODIS é cerca de $7$ vezes maior que a do pixel VIIRS no nadir:
* O limiar mínimo de detecção do MODIS é de $~5\text{ MW}$ a $8\text{ MW}$.
* O limiar mínimo do VIIRS é de apenas $~0.5\text{ MW}$ a $1.2\text{ MW}$.

---

### 3. Conclusões e Recomendações dos Autores para Intercalibração

1. **Compensação da Cauda Inferior:** Ao harmonizar o MODIS com o VIIRS, deve-se aplicar um fator de corte (*truncation threshold*) ou um peso de correção na cauda inferior do VIIRS ($<5\text{ MW}$) para alinhar as distribuições cumulativas de energia.
2. **Normalização por Esforço de Observação ($\Omega$):** Satélites polares não têm frequências de revisita idênticas em todas as latitudes. O número de passagens válidas sem nuvens em um dia deve ser usado como denominador para calcular a Densidade Harmonizada Diária de Fogo.
3. **Escalonamento em Grades Regulares:** A integração em grades espaciais regulares (ex: $0.1^\circ \times 0.1^\circ$ ou grades hexagonais) anula grande parte da dispersão geométrica individual e estabiliza a série temporal.

---

### 4. Aplicação no FocoCerto Harmonizer

* Adotamos o princípio do **operador de observação de Sofiev**: discretização em grade espacial $0.1^\circ$, agregação de FRP e calibração da cauda inferior do VIIRS para preservar a comparabilidade perfeita com os 24 anos da série MODIS.
