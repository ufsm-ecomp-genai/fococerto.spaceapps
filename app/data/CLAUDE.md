# Guia Local de Contexto: Módulo app/data/
## FocoCerto Harmonizer (NASA FIRMS & Dados Espaciais)

Este diretório é o coração da camada de dados da aplicação. Quando estiver trabalhando aqui:

1. **Princípio Fundamental:**
   * Nunca faça web requests diretos durante a execução de testes unitários ou no modo `--sample`.
   * Sempre teste usando os arquivos de teste locais em `data/samples_firms/`.
2. **Módulos Principais:**
   * `app/data/harmonizacao.py`: Padronização de MODIS (1km) e VIIRS (375m), grade espacial de 0.1° e calibração de contagem ($\beta \approx 0.30$) e FRP integrado.
   * `app/data/calendario.py`: Geração da série de 24 anos (2000–2026), cálculo da mediana climatológica por semana/mês e índice $Z_{\text{fire}}$.
   * `app/data/fontes.py`: Endpoints do NASA FIRMS e download dos feeds CSV.
3. **Contratos:**
   * Consulte [`CONTEXT.md`](../../CONTEXT.md) para as fórmulas matemáticas exatas e formato de saída JSON.
