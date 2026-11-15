# Resumo Analítico: Schroeder et al. (2014)
## "The New VIIRS 375 m active fire detection data product: Algorithm description and initial assessment"
*Remote Sensing of Environment*, 143, 85-96.

---

### 1. Contexto e Motivação do Artigo

Com o envelhecimento dos satélites Terra e Aqua da missão EOS, a NASA e a NOAA projetaram o sensor VIIRS a bordo da nave Suomi-NPP para assegurar a continuidade dos registros climáticos globais. 
Wilfrid Schroeder e equipe desenvolveram o algoritmo pioneiro que utiliza os canais de imagem (*I-bands*) com resolução espacial de **$375\text{ m}$**, superando a resolução padrão de $750\text{ m}$ (bandas M) e de $1\text{ km}$ do MODIS.

---

### 2. Resultados Chave e Descobertas Quantitativas

1. **Aumento na Taxa de Detecção Global:**
   * Em ecossistemas savânicos e de transição agrícola (como o Cerrado brasileiro e o Gran Chaco argentino), o produto VIIRS 375m detectou consistentemente **entre 3 e 4 vezes mais focos ativos** do que o produto MODIS 1km na mesma órbita coincidentemente observada.
2. **Capacidade de Detecção de Frentes de Fogo Sub-quilométricas:**
   * Enquanto o MODIS exige frentes de fogo ativas da ordem de $100\text{ m}^2$ para que o sinal térmico supere o limiar de fundo de um pixel de $1.000.000\text{ m}^2$, o VIIRS 375m é capaz de identificar chamas de apenas **$10\text{ m}^2$ a $20\text{ m}^2$**, permitindo intervenção em estágio muito mais inicial.
3. **Mapeamento de Linhas de Fogo Contínuas:**
   * O VIIRS 375m foi capaz de delinear o perímetro e a geometria do avanço de incêndios florestais (linhas de queima estreitas), permitindo estimar a velocidade de propagação do fogo, algo impraticável com o pixel de 1 km do MODIS.

---

### 3. O Desafio de Saturação da Banda I4

* O canal I4 ($3.74\text{ µm} - 3.93\text{ µm}$) possui uma faixa dinâmica restrita e satura a uma temperatura de brilho relativamente baixa (**$367\text{ K}$**).
* Para contornar essa saturação em grandes queimadas florestais, o algoritmo do VIIRS 375m recorre aos dados da banda M13 ($750\text{ m}$, que satura apenas a $634\text{ K}$) para estimar a energia radiativa real sem subestimar o FRP de incêndios catastróficos.

---

### 4. Relevância Direta para o Nosso Projeto

* Este paper é a prova científica cabal de que a disparidade entre MODIS e VIIRS decorre da **sensibilidade física do sensor**, e não de um aumento repentino no número de queimadas no planeta.
* A validação apresentada por Schroeder fornece os parâmetros de sensibilidade que utilizamos na nossa camada de conversão e harmonização de dados.
