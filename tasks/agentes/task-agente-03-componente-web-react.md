# Task Agente 03: Componente Visual do Calendário no Frontend (React / Vite)
## Tipo de Tarefa: Executável por Agente de Código (Claude Code ou Antigravity)

---

### 1. Objetivo da Tarefa
Criar o componente interativo de interface `FireCalendar.jsx` em [`web/app/src/`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/web/app/src/) para exibir o **Fire Activity Calendar** exigido pela NASA, consumindo o JSON gerado pelo backend.

---

### 2. Requisitos de Interface e Acessibilidade
* **Matriz de Heatmap:**
  * Linhas: Anos (2000 a 2026).
  * Colunas: Meses (Jan a Dez) ou Semanas.
  * Células: Cores acessíveis (paleta Viridis ou tons amarelo-laranja-vermelho-magenta) representando a intensidade e anomalia.
* **Interatividade:**
  * Tooltip ao passar o cursor com: Ano/Mês, contagem de focos harmonizados, FRP e status.
  * Clique na célula: abre painel lateral com comparativo contra a mediana histórica (+X% acima da média).
* **Botão de Despacho Tático:**
  * Um botão de destaque: *"Gerar Plano Tático de Resposta (FocoCerto AI)"* quando um período crítico é selecionado.

---

### 3. Checklist de Implementação
- [ ] Criar `web/app/src/FireCalendar.jsx`
- [ ] Importar e vincular `dados_calendario.json` (ou mock de fallback)
- [ ] Implementar a grade responsiva com Tailwind CSS
- [ ] Integrar o componente na página principal `web/app/src/AppNovo.jsx`
- [ ] Adicionar botão de exportação "Download CSV"

---

### 4. Como Validar
```bash
cd web/app
npm run build
```
O build deve passar sem erros de lint ou sintaxe.
