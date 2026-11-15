# Resumo Analítico: Giglio et al. (2016)
## "The Collection 6 MODIS active fire detection algorithm and fire radiative power assessment"
*Remote Sensing of Environment*, 178, 31-41.

---

### 1. Contexto e Motivação do Artigo

O algoritmo Collection 6 (C6) do MODIS representa a evolução madura e definitiva do monitoramento global de fogo pela NASA após mais de 15 anos de operação das plataformas Terra e Aqua. As principais motivações da transição da Collection 5 (C5) para a C6 foram:
* Reduzir a alta taxa de falsos positivos causados por reflexão solar em superfícies quentes e nuvens brilhantes.
* Aprimorar a detecção de queimadas agrícolas de pequena escala.
* Corrigir a degradação temporal dos detectores dos sensores Terra e Aqua ao longo de sua vida útil estendida.

---

### 2. Principais Inovações Algorítmicas da Collection 6

1. **Janela de Contexto Dinâmica Aprimorada:**
   * O algoritmo inicia com uma janela centrada no pixel de $3 \times 3$ e se expande iterativamente até $21 \times 21$ pixels até encontrar pelo menos 20% de pixels válidos (amostras sem água, sem nuvens e não saturadas) e um mínimo de 10 pixels de fundo.
2. **Rejeição Avançada de Reflexão Solar (*Sun Glint*):**
   * Incorporação da geometria solar-satélite (ângulo de reflexão especular $\theta_{\text{glint}}$) em conjunto com a banda 2 ($0.86\text{ µm}$) para filtrar falsas anomalias térmicas provocadas por corpos d'água brilhantes.
3. **Classificação de Focos em Bordas Costeiras:**
   * Utilização de uma máscara de terra/água estática de alta resolução para evitar falsos alarmes causados por contraste térmico solo-água nas faixas litorâneas e de margens de rios largos.

---

### 3. Avaliação e Validação de Fire Radiative Power (FRP)

* **Calibração Radiométrica:** O artigo demonstra que a radiância da Banda 21 ($3.96\text{ µm}$) tem linearidade excepcional mesmo para temperaturas elevadas até $500\text{ K}$, permitindo estimativas confiáveis de FRP.
* **Incerteza do FRP:** Giglio et al. estimam uma incerteza global média de $\pm 20\%$ na determinação do FRP de focos individuais, causada principalmente pela atenuação atmosférica por fumaça e vapor d'água e pela variação angular do pixel fora do nadir.
* **Degradação do Sensor Terra:** A Collection 6 introduziu coeficientes de calibração dependentes do tempo que neutralizam a perda gradual de sensibilidade do detector ao longo das décadas de operação.

---

### 4. Relevância Direta para o Nosso Projeto

* Fornece a **linha de base histórica padrão-ouro (2000–presente)** contra a qual os dados mais recentes do VIIRS devem ser ancorados.
* A metodologia de MAD (*Median Absolute Deviation*) utilizada por Giglio é exatamente a métrica estatística robusta que adotamos em nosso cálculo de anomalias no **Fire Activity Calendar**.
