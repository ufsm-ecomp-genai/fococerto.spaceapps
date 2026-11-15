# Task Agente 07: Extensão da CLI com Comandos de Harmonização e Calendário
## Tipo de Tarefa: Executável por Agente de Código (CLI / UX)

---

### 1. Objetivo da Tarefa
Atualizar o ponto de entrada da aplicação [`app/cli.py`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/app/cli.py) para que os jurados da NASA possam invocar a harmonização e a geração do calendário diretamente pela linha de comando.

---

### 2. Novos Argumentos da CLI
* `--calendario`: Gera a matriz histórica do Fire Activity Calendar (2000 a 2026) para a região informada.
* `--harmonizar`: Executa a rotina de intercalibração entre os feeds MODIS e VIIRS e exibe as estatísticas de convergência de FRP e contagem normalizada no terminal.
* Exemplo de uso:
  ```bash
  python -m app.cli --sample --calendario --regiao tocantins
  ```

---

### 3. Saída Formatada Esperada no Terminal
Ao rodar `--calendario`, o terminal deve exibir uma tabela visual limpa (usando caracteres ASCII/Unicode ou Rich/tabulate):
```
================================================================================
   FOCOCERTO HARMONIZER — 24-YEAR FIRE ACTIVITY CALENDAR (NASA FIRMS)
   Area of Interest: Tocantins / Cerrado (2000 - 2026)
================================================================================
Year | Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec | Total FRP
2024 |  .    .    .    .    .    o    o    X   [!]   o    .    .  | 48,210 MW  <- CRITICAL ANOMALY (SEP)
2023 |  .    .    .    .    .    o    o    X    X    o    .    .  | 31,450 MW
...
Legend: [.] Normal  [o] Moderate  [X] High Alert  [!] Critical Anomaly (P95+)
================================================================================
Status: 2024 September fire activity was +240% above the 24-year historical median.
Planner-Critic Tactical Dispatch Triggered: 4 Brigades Assigned.
```

---

### 4. Checklist de Execução
- [ ] Adicionar flags no `argparse` em `app/cli.py`
- [ ] Conectar chamada com `app/data/calendario.py` e `app/data/harmonizacao.py`
- [ ] Garantir que funcione em modo `--sample` sem dependência de serviços externos
- [ ] Testar comandos no terminal
