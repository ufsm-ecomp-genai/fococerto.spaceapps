# Task Agente 01: Pipeline de Harmonização de Dados MODIS + VIIRS
## Tipo de Tarefa: Executável por Agente de Código (Claude Code ou Antigravity)

---

### 1. Objetivo da Tarefa
Construir o módulo Python [`app/data/harmonizacao.py`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/app/data/harmonizacao.py) para ingerir os registros brutos de anomalias térmicas do MODIS Collection 6.1 (1 km) e do VIIRS 375m do NASA FIRMS, reconciliando a diferença geométrica de footprint e calibração de energia radiativa.

---

### 2. Fundamentação e Parâmetros
* **Dados de entrada para teste:**
  * `data/samples_firms/modis_sample_c6.csv`
  * `data/samples_firms/viirs_sample_375m.csv`
* **Formulação de equivalência:**
  * O pixel do VIIRS cobre uma área $~7.1\text{x}$ menor que o MODIS, detectando cerca de $3\text{x}$ a $4\text{x}$ mais focos.
  * Agregação em grade espacial uniforme de $0.1^\circ \times 0.1^\circ$ (~$11\text{ km}$).
  * Para $t \ge 2012$ (sobreposição):
    $$N_{\text{harmonizado}} = N_{\text{MODIS}} + 0.30 \cdot N_{\text{VIIRS}}$$
    $$\text{FRP}_{\text{harmonizado}} = \sum \text{FRP}_{\text{MODIS}} + \sum \text{FRP}_{\text{VIIRS}}$$

---

### 3. Checklist de Implementação
- [ ] Criar função `carregar_e_padronizar_focos(caminho_csv: Path, sensor: str) -> list[dict]`
- [ ] Tratar mapeamento de `confidence` (MODIS numérico 0-100; VIIRS strings `low`/`nominal`/`high`)
- [ ] Criar função de discretização em grade `agregar_em_grade(focos: list[dict], step: float = 0.1) -> dict`
- [ ] Criar função `harmonizar_series(focos_modis: list[dict], focos_viirs: list[dict]) -> list[dict]`
- [ ] Exportar resultado consolidado para teste

---

### 4. Como Validar
```bash
python3 -c "
from app.data.harmonizacao import carregar_e_padronizar_focos, harmonizar_series
from pathlib import Path
modis = carregar_e_padronizar_focos(Path('data/samples_firms/modis_sample_c6.csv'), 'MODIS')
viirs = carregar_e_padronizar_focos(Path('data/samples_firms/viirs_sample_375m.csv'), 'VIIRS')
harm = harmonizar_series(modis, viirs)
print(f'Harmonização concluída com sucesso: {len(harm)} registros unificados.')
"
```
