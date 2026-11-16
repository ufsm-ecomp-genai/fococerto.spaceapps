# Guia de Trabalho — Papel 2: Backend & Harmonização Científica
**Responsável:** Enzo Augusto Mucha Domingues  
**Foco:** Engenharia de Dados, Claude Code, Harmonização MODIS/VIIRS e Motor Climatológico

> [!TIP]
> **Instrução para o desenvolvedor:** Você pode passar este documento diretamente como contexto ou prompt inicial para o **Claude Code**. Ele contém todos os contratos, fórmulas matemáticas, arquivos de entrada e saídas esperadas.

---

### 1. Sua Missão no Time
Implementar a **Camada de Harmonização Científica** e o **Motor do Calendário de Atividade de Queimadas (*Fire Activity Calendar*)** em Python, integrando os dados de anomalias térmicas do MODIS (1 km) e VIIRS (375 m) da NASA.

---

### 2. Contexto Científico e Regras do Desafio
* **O Problema:** O MODIS tem dados desde 2000 com pixel de 1 km. O VIIRS opera desde 2012 com pixel de 375 m. O VIIRS detecta entre $3\text{x}$ e $4\text{x}$ mais focos que o MODIS no mesmo incêndio. Somar as contagens cria uma quebra artificial no histórico.
* **A Solução:**
  1. Agregar espacialmente os focos em células de grade uniforme de $0.1^\circ \times 0.1^\circ$ (ou por polígono de região) agrupados por semana/mês.
  2. Aplicar calibração cruzada de FRP (Fire Radiative Power) e fator de escala de contagem ($\beta \approx 0.30$) no período de sobreposição (2012–presente), unificando com a série do MODIS (2000–2012).
  3. Calcular a linha de base histórica (mediana climática de 20+ anos para cada semana do ano) e o índice de anomalia ($Z_{\text{fire}}$ e Percentil 95).

---

### 3. Arquivos que Você Deve Criar / Modificar

#### A. Criar: `app/data/harmonizacao.py`
Módulo responsável por ler detecções brutas do MODIS e VIIRS e produzir o dataset harmonizado.
* **Entradas:** 
  * Feeds CSV do FIRMS (usar dados de teste em `data/samples_firms/modis_sample_c6.csv` e `data/samples_firms/viirs_sample_375m.csv`).
* **Funções Obrigatórias:**
  * `carregar_e_padronizar_focos(caminho_csv: Path, sensor: str) -> list[dict]`:
    * Normaliza colunas para: `lat, lon, data_hora_utc, data, sensor, confianca_num, frp, satelite`.
    * No VIIRS, converte `confidence` (`low` $\to 30$, `nominal` $\to 65$, `high` $\to 90$).
  * `agregar_grade_espacial(focos: list[dict], tamanho_grade_graus: float = 0.1) -> dict`:
    * Agrupa por célula `(round(lat / step) * step, round(lon / step) * step)` e por período.
  * `harmonizar_series(focos_modis: list[dict], focos_viirs: list[dict]) -> list[dict]`:
    * Aplica a fórmula de equivalência:
      * Para períodos anteriores a 2012: usa o sinal MODIS direto.
      * Para períodos de 2012 em diante: calcula o FRP integrado e a contagem calibrada:
        $$\text{FRP}_{\text{harm}} = \sum \text{FRP}_{\text{MODIS}} + \sum \text{FRP}_{\text{VIIRS}}$$
        $$N_{\text{harm}} = N_{\text{MODIS}} + 0.30 \cdot N_{\text{VIIRS}}$$

#### B. Criar: `app/data/calendario.py`
Módulo que processa a série harmonizada e gera os dados estruturados do calendário para a web.
* **Funções Obrigatórias:**
  * `calcular_matriz_calendario(focos_harmonizados: list[dict], ano_inicio=2000, ano_fim=2026) -> dict`:
    * Retorna uma matriz indexada por ano e semana do ano (1 a 52) ou mês (1 a 12).
    * Para cada célula da matriz:
      * `ano`: int
      * `periodo`: int (mês 1-12 ou semana 1-52)
      * `focos_harmonizados`: float
      * `frp_total_mw`: float
      * `mediana_historica`: float (mediana dos anos para aquele mesmo período)
      * `status`: `"NORMAL"`, `"ATENCAO"` (acima do P75), `"CRITICO"` (acima do P95 ou $Z \ge 2.0$)
  * `gerar_json_para_frontend(resultado_calendario: dict, caminho_saida: Path) -> None`:
    * Salva em `web/app/src/assets/dados_calendario.json` para o frontend consumir diretamente.

#### C. Adicionar Endpoint na API: `app/api.py` (Se houver tempo)
* `GET /api/v1/calendario?regiao={regiao}&ano_inicio=2000&ano_fim=2026`:
  * Retorna o JSON estruturado do calendário para a região solicitada.

---

### 4. Como Testar e Validar seu Código
Crie um teste unitário em `tests/test_harmonizacao.py`:
```bash
python3 -m pytest tests/test_harmonizacao.py -v
```
E um script rápido de demonstração:
```bash
python3 -c "from app.data.harmonizacao import harmonizar_series; print('Harmonização OK')"
```

---

### 5. O que Entregar para o Time
1. O arquivo `dados_calendario.json` (gerado para a região de Tocantins/Cerrado) entregue para a **Pessoa 3** plugar no mapa e gráficos.
2. 1 parágrafo com as métricas obtidas (ex: *"A correlação de FRP integrado pós-harmonização atingiu R² = 0.88, reduzindo a discrepância de contagem de 340% para menos de 5%"*) para a **Pessoa 4** colocar no Slide 4 da apresentação!
