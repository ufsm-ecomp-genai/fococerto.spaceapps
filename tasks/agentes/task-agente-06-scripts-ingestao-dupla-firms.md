# Task Agente 06: Ingestão Dupla do NASA FIRMS (MODIS + VIIRS)
## Tipo de Tarefa: Executável por Agente de Código (Backend / Ingestão)

---

### 1. Objetivo da Tarefa
Atualizar [`scripts/ingest_firms.py`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/scripts/ingest_firms.py) e [`app/data/fontes.py`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/app/data/fontes.py) para suportar a ingestão combinada de múltiplos sensores do NASA FIRMS, e não apenas o VIIRS Suomi-NPP.

---

### 2. Mudanças Necessárias em `app/data/fontes.py`
Atualmente, o arquivo contém apenas:
```python
FIRMS_URL = ("https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_{janela}.csv")
```
Expandir para suportar dicionário de fontes oficiais da NASA:
```python
FIRMS_URLS = {
    "viirs_snpp": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_Global_{janela}.csv",
    "modis_c6": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_Global_{janela}.csv",
    "viirs_noaa20": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_Global_{janela}.csv"
}
```

---

### 3. Mudanças em `scripts/ingest_firms.py`
* Adicionar o argumento `--sensor` com opções: `modis`, `viirs_snpp`, `viirs_noaa20`, `todos` (default).
* Permitir baixar e processar ambos os feeds salvando arquivos separados em `data/raw/` e consolidando no banco/saída CSV.

---

### 4. Checklist de Execução
- [ ] Atualizar `FIRMS_URLS` em `app/data/fontes.py`
- [ ] Adicionar parser de múltiplos sensores em `scripts/ingest_firms.py`
- [ ] Garantir modo offline com `--arquivo` apontando para `data/samples_firms/`
- [ ] Testar execução sem flags de rede
