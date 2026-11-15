# Playbook de Projetos Vencedores Globais (Global Winners Playbook)
## Estrutura Recomendada para a Demonstração (7 Slides ou Vídeo de 30s)

A demonstração (*demo*) é o primeiro contato dos jurados da NASA com o projeto. Jurados avaliam dezenas de projetos por hora; por isso, a clareza, concisão e impacto visual definem a passagem para as etapas finais de premiação.

---

### Opção A: Apresentação de Slides (Máximo de 7 Slides)

> [!WARNING]
> O limite de 7 slides é absoluto (inclui capa e introdução). Apresentações com 8 ou mais slides são automaticamente desclassificadas da avaliação global.

A estrutura recomendada pelos projetos vencedores históricos da NASA:

| Slide | Título / Foco | Conteúdo Essencial |
|---|---|---|
| **Slide 1** | **Capa & Identidade** | • Nome do Projeto (ex: *FocoCerto Harmonizer: Fire Activity Calendar & Decision Support*)<br>• Nome da Equipe: *ECOMP - UFSM*<br>• Desafio: *Harmonization of MODIS and VIIRS Hot Spots*<br>• Slogan / Frase de Impacto (1 linha). |
| **Slide 2** | **O Problema (The Problem)** | • A quebra histórica entre MODIS (1 km, desde 2000) e VIIRS (375 m, desde 2012).<br>• O dilema do gestor de terras e brigadista: falta de uma visão temporal contínua e risco de falsas tendências causadas pela diferença de sensibilidade dos sensores. |
| **Slide 3** | **A Solução & Arquitetura (The Solution)** | • Visão geral da plataforma web e do fluxo de harmonização.<br>• Como os dados brutos de anomalias térmicas do NASA FIRMS se tornam um calendário contínuo de queima.<br>• Diagrama visual simples do pipeline (NASA Data $\to$ Harmonization $\to$ Calendar $\to$ Action). |
| **Slide 4** | **Metodologia Científica (Science & Data Validity)** | • Como resolvemos a discrepância espacial: agregação em células padronizadas (ex: 0.1° / H3).<br>• Calibração de equivalência de FRP (Fire Radiative Power) e contagem de focos.<br>• Linha de base multi-decenal (mediana histórica) e identificação de anomalias críticas (Percentil 95 / Z-score). |
| **Slide 5** | **A Aplicação Web: Fire Activity Calendar** | • Screenshots reais da interface web interativa.<br>• Destaque para: Seletor de Área de Interesse (AOI), matriz temporal (anos x semanas) e detecção de períodos anômalos. |
| **Slide 6** | **Impacto Operacional & Diferencial Único** | • Não apenas um gráfico passivo: a ponte entre detecção espacial e resposta em campo.<br>• Como equipes de emergência e bombeiros utilizam o calendário para pré-posicionar brigadas antes que o fogo fuja do controle. |
| **Slide 7** | **Futuro, Dados Utilizados & Conclusão** | • Resumo dos dados da NASA utilizados (FIRMS MODIS C6.1, VIIRS S-NPP / NOAA-20 / NOAA-21).<br>• Parceiro de agência espacial: CONAE e relevância para biomas sul-americanos.<br>• Próximos passos e links públicos (GitHub / Demo). |

---

### Opção B: Vídeo de Pitch (Máximo de 30 Segundos)

Se a equipe optar pelo vídeo, a divisão exata dos 30 segundos deve ser:

* **[0:00 - 0:03] Gancho & Apresentação:**
  *"We are ECOMP-UFSM presenting FocoCerto Harmonizer for the NASA Space Apps Challenge."*
* **[0:03 - 0:08] O Problema:**
  *"For over 20 years, satellites tracked fires, but MODIS and VIIRS data cannot be compared directly—leaving emergency managers without a consistent historical picture."*
* **[0:08 - 0:18] A Solução & Demo Visual:**
  *(Mostrando a tela do app)* *"We built a web-based Fire Activity Calendar that cross-calibrates MODIS and VIIRS into a unified multi-decadal time series, detecting seasonal baselines and extreme thermal anomalies in real time."*
* **[0:18 - 0:25] O Diferencial Operacional:**
  *"When a critical period is detected, our reasoning engine generates actionable dispatch recommendations for ground brigades."*
* **[0:25 - 0:30] Encerramento:**
  *"Transforming raw NASA Earth observation into lifesaving tactical response. Thank you!"*
