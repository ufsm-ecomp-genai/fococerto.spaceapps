# Guia Local de Contexto: Módulo web/
## FocoCerto Harmonizer (Interface Web & Fire Activity Calendar)

Este diretório contém a aplicação web interativa em React + Vite + Tailwind CSS.

1. **Objetivo Principal:**
   * Implementar o componente `FireCalendar.jsx` que exibe a matriz visual anual x mensal/semanal de queimadas harmonizadas.
2. **Diretrizes de Design e Acessibilidade:**
   * Usar tons acessíveis para o mapa de calor (baixo = amarelo claro, moderado = laranja, alto = vermelho escuro, crítico/anomalia = roxo/magenta).
   * Tooltip informativo ao passar o cursor sobre qualquer mês/semana.
   * Botão de ação direta: *"Gerar Plano Tático com IA"* ao clicar em períodos críticos.
3. **Dados:**
   * Consumir o arquivo `web/app/src/assets/dados_calendario.json` (gerado por `app/data/calendario.py`).
4. **Comandos:**
   ```bash
   cd web/app
   npm run dev      # Servidor local de desenvolvimento (http://localhost:5173)
   npm run build    # Build de produção em web/dist/
   ```
