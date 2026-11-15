# Task Agente 05: Refatoração do README.md Principal da Raiz
## Tipo de Tarefa: Executável por Agente de Código / Documentação

---

### 1. Objetivo da Tarefa
Reescrever o [`README.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/README.md) na raiz do repositório para transformá-lo na vitrine oficial para os jurados do **NASA Space Apps Challenge 2026**.

---

### 2. O que Precisa ser Removido / Atualizado
* **Remover:** Referências residuais a "Open Agent Hackathon", "Track 3", "Meterless Nightshift", "Zetaris" e outros patrocinadores de eventos passados no corpo principal.
* **Adicionar com Destaque:**
  * Banner e identificação do **NASA International Space Apps Challenge 2026**.
  * Desafio: **Harmonization of MODIS and VIIRS Hot Spots**.
  * Identificação da equipe: **ECOMP - UFSM**.
  * **Seção Obrigatória de Prior Work (Transparência Radical da NASA):**
    * *Pre-existing work:* Arquitetura multiagente de raciocínio operacional (Planner-Critic) e interface base.
    * *New work developed during Space Apps:* Algoritmo de harmonização de footprint MODIS (1km) vs VIIRS (375m), conversão de energia radiativa (FRP), motor de série histórica de 24 anos e o componente *Fire Activity Calendar*.
  * **Quick Start em 30 Segundos:** Instruções simples para qualquer jurado rodar a demonstração com 1 comando:
    ```bash
    python3 -m app.cli --sample --calendario
    ```
  * Citação dos dados da NASA utilizados (FIRMS MODIS C6.1, VIIRS 375m) e parceria com CONAE.

---

### 3. Checklist de Execução
- [x] Atualizar cabeçalho e badges
- [x] Escrever a seção de Prior Work conforme regulamento da NASA
- [x] Descrever a arquitetura de harmonização com diagrama Mermaid
- [x] Validar que todos os links apontam para `fococerto.spaceapps.git` e `docs/spaceapps/`
- [x] Garantir texto 100% em Inglês fluído e profissional
