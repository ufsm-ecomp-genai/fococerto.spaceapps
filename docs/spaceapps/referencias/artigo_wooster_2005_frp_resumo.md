# Resumo Analítico: Wooster et al. (2005)
## "Retrieval of biomass combustion rates and totals from fire radiative power observations: FRP derivation and calibration relationships between radiant energy and burned mass"
*Journal of Geophysical Research: Atmospheres*, 110(D24).

---

### 1. O Problema Fundamental da Estimativa de Queimadas

Historicamente, cientistas tentavam estimar a biomassa consumida e as emissões de gases de efeito estufa multiplicando a **Área Queimada** ($A$) pela **Carga de Combustível** ($B$) e pelo **Fator de Combustão** ($C$):

$$M = A \cdot B \cdot C$$

Essa abordagem tradicional carrega erros cumulativos severos, pois a estimativa da carga de combustível e a fração de queima variam drasticamente em escala de metros. 
Martin Wooster propôs uma revolução metodológica: **medir diretamente o fluxo de energia radiativa liberada pela combustão química**.

---

### 2. A Física do Método de Radiância MIR (Wooster FRP Method)

A energia radiativa total ($E$) emitida por um corpo negro é dada pela integral da Lei de Planck sobre todos os comprimentos de onda:

$$E = \sigma \cdot T^4 \quad [\text{W m}^{-2}]$$

No entanto, sensores de satélite não medem todo o espectro, mas sim bandas estreitas no infravermelho médio (MIR, em torno de $4\text{ µm}$). Wooster demonstrou que, para a faixa de temperaturas típica de chamas vegetais ($700\text{ K} - 1.300\text{ K}$), a radiância espectral na janela MIR pode ser aproximada por uma função de potência de quarta ordem:

$$L_{\text{MIR}}(T) \approx a \cdot T^4$$

Substituindo $T^4$ pela radiância medida, o Fire Radiative Power (FRP) pode ser extraído diretamente da radiância do pixel sem necessidade de conhecer a área sub-pixel da chama nem a sua temperatura absoluta exata:

$$\text{FRP} = \left(\frac{A_{\text{pixel}} \cdot \sigma}{a}\right) \cdot \left(L_{\text{MIR}} - L_{\text{MIR, fundo}}\right)$$

---

### 3. A Constante de Conversão Biofísica ($C_e$)

O resultado mais impactante dos experimentos laboratoriais e de campo de Wooster foi a descoberta de que a **taxa de queima de biomassa seca** ($\dot{M}$, em $\text{kg/s}$) é proporcional à taxa de energia radiativa emitida (FRP, em $\text{MW}$):

$$\dot{M} = C_e \cdot \text{FRP}$$

Integrando a energia radiativa ao longo do tempo (Fire Radiative Energy - FRE, em $\text{MJ}$):

$$M_{\text{total}} = C_e \cdot \text{FRE} = C_e \int_{t_0}^{t_1} \text{FRP}(t) \, dt$$

* **Constante Universal de Combustão ($C_e$):**
  $$C_e \approx 0.368 \pm 0.015 \text{ kg MJ}^{-1}$$
* Independentemente do tipo de combustível vegetal (gramíneas savânicas, floresta tropical, turfa ou agulhas de pinheiro), a razão entre a energia radiativa liberada e a massa seca de biomassa queimada permanece quase constante.

---

### 4. Por que o FRP é o Pilar da Nossa Harmonização

* A **contagem de pixels** de fogo é um artefato da resolução geométrica do satélite (pixels de 375 m geram contagens $4\text{x}$ maiores).
* O **FRP**, por outro lado, é uma **grandeza física extensiva e conservativa**. 
* Se um incêndio libera $100\text{ MW}$ de calor radiativo:
  * O MODIS pode registrar essa energia em $1$ único pixel de 1 km com $\text{FRP} = 100\text{ MW}$.
  * O VIIRS registrará a mesma energia distribuída em $6$ ou $8$ pixels adjacentes de 375 m com $\text{FRP}$ individual de $12\text{ MW}$ a $18\text{ MW}$, mas cuja **soma no espaço continuará sendo $~100\text{ MW}$**.
* Por isso, a agregação espacial de FRP harmonizado é o método mais robusto e cientificamente defensável para unificar MODIS e VIIRS.
