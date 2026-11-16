# Guia de Trabalho — Papel 3: Frontend Web & Calendário de Queimadas
**Responsável:** Gabriel Mazui Azevedo  
**Foco:** Interface do Fire Activity Calendar (React / Vite / Tailwind) em `web/app/`

---

### 1. Sua Missão no Time
Criar a interface visual exigida pelo desafio da NASA: o **Fire Activity Calendar** interativo na aplicação web do FocoCerto (localizada em `web/app/`).

---

### 2. O Que a NASA Exige na Interface Web (Conforme `info22.md`)
1. **Seletor de Área de Interesse (AOI):**
   * Permitir que o usuário selecione a região (ex: Tocantins, Pantanal, Cerrado, Ibéria) ou insira coordenadas.
2. **Visualização do Calendário de Atividade (Heatmap Matrix):**
   * Uma matriz com os **Anos nas linhas (2000 a 2026)** e os **Meses (Jan a Dez) ou Semanas nas colunas**.
   * Células coloridas representando a intensidade harmonizada de fogo.
   * **Rampa de cores acessível:** tons suaves de amarelo para baixa queima, laranja para moderada, vermelho escuro para intensa, e roxo/magenta para anomalia crítica.
3. **Indicadores de Condição Incomum / Período Crítico:**
   * Destacar visualmente na matriz quando um mês/semana ultrapassa a mediana histórica multi-decenal ou entra no percentil 95 de emergência.
4. **Exportação de Dados:**
   * Botão simples de "Download CSV" da série harmonizada da região.
5. **Botão de Despacho Operacional (O Diferencial do FocoCerto):**
   * Um botão de destaque: *"Gerar Plano Tático de Resposta com IA"*, que exibe a alocação de brigadas e a análise dos agentes para o período crítico selecionado.

---

### 3. Como Implementar na Prática no Projeto

O projeto já possui uma aplicação React funcional em `web/app/`.

#### Componente Sugerido: `web/app/src/FireCalendar.jsx`
* Crie o componente que lê os dados (do arquivo `dados_calendario.json` entregue pela Pessoa 2 ou de uma mock inicial).
* Renderize:
  * **Header:** Seletor de Região + Filtro de Ano + Legenda de Cores (Normal, Atenção, Crítico).
  * **Matriz Visual:**
    ```jsx
    // Exemplo de estrutura de renderização da matriz:
    <div className="grid grid-cols-13 gap-1 p-4 bg-slate-900 rounded-lg text-xs">
      <div className="font-bold text-slate-400">Ano</div>
      {meses.map(m => <div key={m} className="font-semibold text-center text-slate-400">{m}</div>)}
      
      {anos.map(ano => (
        <React.Fragment key={ano}>
          <div className="font-mono text-slate-400 py-1">{ano}</div>
          {meses.map(mes => {
            const dado = getDado(ano, mes);
            return (
              <div 
                key={mes}
                title={`${ano}/${mes}: ${dado.focos} focos harmonizados (${dado.status})`}
                className={`h-6 rounded cursor-pointer transition-all hover:scale-110 ${corPorStatus(dado.status, dado.focos)}`}
                onClick={() => selecionarPeriodo(ano, mes)}
              />
            );
          })}
        </React.Fragment>
      ))}
    </div>
    ```
  * **Painel de Detalhes:** Ao clicar em um mês anômalo, exibir cards com:
    * Focos Harmonizados vs. Mediana Histórica (ex: `+240% acima da mediana`).
    * FRP Total (Megawatts).
    * Alerta de Período Crítico e botão para acionar o plano do FocoCerto.

---

### 4. Como Rodar e Testar Localmente
```bash
cd web/app
npm install
npm run dev
```
Acesse `http://localhost:5173` no navegador.

---

### 5. O Que Entregar para o Time
1. **Screenshots em Alta Resolução:** Tirar fotos nítidas do calendário exibindo o histórico de queimadas e os destaques de períodos críticos para a **Pessoa 4 (Slides)**.
2. **Gravação de Tela Limpa (10 a 15 segundos):** Gravar navegando na matriz do calendário e clicando no botão para a **Pessoa 5 (Vídeo de 30s)**.
