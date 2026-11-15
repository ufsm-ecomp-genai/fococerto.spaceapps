# Task Agente 04: Testes Automatizados e Modo Sample
## Tipo de Tarefa: Executável por Agente de Código (Claude Code ou Antigravity)

---

### 1. Objetivo da Tarefa
Garantir que a suíte de testes automatizados com `pytest` cubra os novos módulos de harmonização e calendário, e que o modo offline determinístico (`--sample`) execute sem falhas em menos de 5 segundos.

---

### 2. Arquivos Envolvidos
* `tests/test_harmonizacao.py` (a criar)
* `app/cli.py` (garantir suporte a flag de harmonização)
* `data/samples_firms/` (massa de teste)

---

### 3. Checklist de Implementação
- [x] Criar `tests/test_harmonizacao.py` com testes para:
  * Leitura e padronização dos CSVs de MODIS e VIIRS.
  * Agregação em células de grade uniforme.
  * Equivalência de contagem e conservação de FRP.
  * Detecção correta de períodos anômalos.
- [ ] Testar a CLI local:
  ```bash
  python3 -m app.cli run --sample --regiao tocantins
  ```
- [x] Executar o pytest completo:
  ```bash
  pytest tests/test_harmonizacao.py -v
  ```

---

### 4. Critério de Aceite
Todos os testes passam com status verde (100% pass) sem dependência de chaves de API externas ou conexão com a internet.
