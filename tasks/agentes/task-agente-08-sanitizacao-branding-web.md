# Task Agente 08: Sanitização e Branding da Aplicação Web
## Tipo de Tarefa: Executável por Agente de Código (Frontend / Branding)

---

### 1. Objetivo da Tarefa
Atualizar a interface do frontend em [`web/app/`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/web/app/) para alinhar títulos, rodapés, logos e metadados ao **NASA Space Apps Challenge 2026** e remover textos residuais de eventos anteriores.

---

### 2. O que Atualizar em `web/app/`:
1. **`web/app/index.html`:**
   * `<title>`: Alterar para `FocoCerto Harmonizer | NASA Space Apps Challenge 2026`.
   * Meta tags e descrições para refletir o desafio *Harmonization of MODIS and VIIRS Hot Spots*.
2. **Cabeçalho e Navegação (`AppNovo.jsx` / `main.jsx`):**
   * Exibir o título: **FocoCerto Harmonizer**.
   * Adicionar a aba / botão de navegação: **Fire Activity Calendar** (Calendário de Queimadas) ao lado da aba de Operações/Plano.
3. **Rodapé e Créditos:**
   * Incluir crédito: *"Powered by NASA FIRMS (MODIS Collection 6.1 & VIIRS 375m) & CONAE Space Agency Partnership"*.
   * Licença: *Open Source Apache License 2.0*.

---

### 3. Checklist de Execução
- [x] Atualizar `web/app/index.html`
- [x] Atualizar textos de cabeçalho e rodapé em `AppNovo.jsx`
- [x] Garantir que o build de produção gere os arquivos corretos em `web/dist/`
