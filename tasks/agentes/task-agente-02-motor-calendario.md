# Task Agente 02: Motor do Calendário de Atividade e Detecção de Anomalias
## Tipo de Tarefa: Executável por Agente de Código (Claude Code ou Antigravity)

---

### 1. Objetivo da Tarefa
Construir o módulo Python [`app/data/calendario.py`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/app/data/calendario.py) que recebe os dados harmonizados da Task 01 e calcula a matriz temporal de 20+ anos (2000 a 2026), gerando a linha de base histórica (mediana semanal/mensal), o índice de anomalia $Z_{\text{fire}}$ e os alertas de períodos críticos.

---

### 2. Parâmetros e Métricas Estatísticas
* **Intervalo Temporal:** 2000 a 2026.
* **Agrupamento Temporal:** Semanas do ano ($w \in [1, 52]$) ou Meses ($m \in [1, 12]$).
* **Métricas:**
  * **Mediana Histórica ($\tilde{\mu}_w$):** Ponto médio dos anos anteriores para o mesmo período.
  * **Percentil 90 ($P_{90}$) e Percentil 95 ($P_{95}$):** Limiares de alerta.
  * **Status da Célula:**
    * `"NORMAL"`: dentro do intervalo sazonal esperado ($Z < 1.0$).
    * `"ATENCAO"`: acima da mediana / $P_{75}$ ($1.0 \le Z < 2.0$).
    * `"CRITICO"`: anomalia severa ($Z \ge 2.0$ ou $> P_{95}$).

---

### 3. Checklist de Implementação
- [x] Criar função `construir_matriz_temporal(focos_harm: list[dict], ano_inicio=2000, ano_fim=2026) -> dict`
- [x] Calcular mediana, $P_{90}$ e $P_{95}$ para cada período do ano
- [x] Atribuir status de anomalia a cada célula do calendário
- [x] Criar função `exportar_calendario_json(dados_matriz: dict, caminho_saida: Path) -> None`
- [x] Salvar a saída estruturada em `web/app/src/assets/dados_calendario.json` para consumo do frontend

---

### 4. Como Validar
```bash
python3 -c "
from app.data.calendario import construir_matriz_temporal
# Testar com lista simulada ou dados de amostra
print('Motor de calendário estruturado com sucesso.')
"
```
