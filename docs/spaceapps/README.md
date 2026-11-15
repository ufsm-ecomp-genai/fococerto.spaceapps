# Central de Orquestração: NASA Space Apps Challenge 2026
## Time ECOMP - UFSM | Desafio: Harmonization of MODIS and VIIRS Hot Spots

Bem-vindo ao centro de comando e documentação da equipe para o **NASA International Space Apps Challenge 2026**. Esta pasta centraliza todas as informações oficiais do desafio, regras de submissão, fundamentação científica e os guias operacionais divididos para os **5 integrantes** do time.

---

### 1. Mapa Rápido da Documentação

A documentação está organizada em 5 módulos temáticos:

```
docs/spaceapps/
├── README.md                           <- Você está aqui (Guia Mestre de Orquestração)
│
├── 01-desafio/                         <- Detalhes Oficiais do Desafio
│   ├── 01-enunciado-e-detalhes.md      (Contexto, background e objetivos da NASA)
│   ├── 02-recursos-e-dados-nasa.md     (APIs do FIRMS, satélites e agência parceira CONAE)
│   ├── 03-guia-evento-universal.md     (Regra crítica: equipes de 2 a 6 membros)
│   └── desafio-oficial-nasa.pdf        (Documento original em PDF)
│
├── 02-regras-e-diretrizes/             <- Regras Oficiais e Critérios de Julgamento
│   ├── 01-guia-submissao-projetos.md   (Prazos, limites de demo e campos obrigatórios)
│   ├── 02-rubricas-e-criterios.md      (Impacto, Criatividade, Validade, Relevância e Pitch)
│   ├── 02-checklist-avaliacao.md       (Checklist para buscar nota máxima)
│   ├── 03-termos-participante.md       (Termos e condições oficiais da NASA)
│   ├── 04-diretrizes-marca-nasa.md     (Uso legal de nomes e logotipos)
│   ├── 05-licenciamento-apache2.md     (Licença Open Source exigida pelo evento)
│   └── 06-parceiros-espaciais.md       (Lista das 17 agências parceiras, incluindo CONAE e AEB)
│
├── 03-papeis-equipe/                   <- Divisão de Trabalho das 5 Pessoas
│   ├── papel-1-coordenacao.md          (Líder: Integração, Git, arquitetura e core)
│   ├── papel-2-claude-code.md          (Backend: Guia pronto para o amigo usar Claude Code)
│   ├── papel-3-frontend-web.md         (Frontend: Matriz do Fire Activity Calendar em React)
│   ├── papel-4-slides-7paginas.md      (Design: Textos em inglês e layout dos 7 slides)
│   └── papel-5-submissao-e-video.md    (Submissão: Textos do formulário e vídeo de 30s)
│
├── 04-fundamentacao-cientifica/        <- Teoria, Manuais e Literatura Seminal
│   ├── 01-metodologia-harmonizacao.md  (Fórmulas matemáticas e normalização espaço-temporal)
│   ├── manual_modis_c6.md              (Manual do MODIS C6.1: canais, saturação, efeito bow-tie)
│   ├── manual_viirs_375m.md            (Manual do VIIRS 375m: bandas I/M, agregação 3 zonas)
│   ├── artigo_giglio_2016_resumo.md    (Paper da Collection 6 e FRP)
│   ├── artigo_schroeder_2014_resumo.md (Paper da resolução e sensibilidade do VIIRS 375m)
│   ├── artigo_wooster_2005_frp_resumo.md (Física do FRP e taxa de queima de biomassa)
│   ├── artigo_sofiev_2020_harmonizacao.md (Operador analítico de observação para cross-calibration)
│   ├── transcricao_arset_wildfires.md  (Treinamentos oficiais da NASA ARSET)
│   └── firms_api_e_dados.md            (Especificação técnica dos endpoints do FIRMS)
│
└── 05-materiais-apoio/                 <- FAQs, Comunidade e Apoio
    ├── faq-participantes.md            (Perguntas frequentes da NASA Space Apps)
    ├── guia-formacao-equipes.md        (Orientações para formação de equipes)
    ├── guia-space-apps-connect.md      (Uso dos canais oficiais de comunicação)
    ├── playbook-vencedores-globais.md  (Exemplos e boas práticas de projetos premiados)
    └── guia-recrutamento.pdf           (Material gráfico oficial de recrutamento)
```

---

### 2. Atribuições da Equipe (5 Integrantes)

| Integrante | Papel | Onde Trabalha | Arquivo Guia |
|---|---|---|---|
| **Pessoa 1** | **Líder & Integração** | Antigravity / Git / Core | [`03-papeis-equipe/papel-1-coordenacao-e-integracao.md`](03-papeis-equipe/papel-1-coordenacao-e-integracao.md) |
| **Pessoa 2** | **Backend & Algoritmo** | Terminal (Claude Code) / Python | [`03-papeis-equipe/papel-2-claude-code-harmonizacao.md`](03-papeis-equipe/papel-2-claude-code-harmonizacao.md) |
| **Pessoa 3** | **Frontend Web** | React / Vite / Tailwind (`web/`) | [`03-papeis-equipe/papel-3-frontend-calendario-web.md`](03-papeis-equipe/papel-3-frontend-calendario-web.md) |
| **Pessoa 4** | **Pitch Deck (7 Slides)** | Google Slides / Canva | [`03-papeis-equipe/papel-4-design-e-slides-7paginas.md`](03-papeis-equipe/papel-4-design-e-slides-7paginas.md) |
| **Pessoa 5** | **Formulário NASA & Vídeo 30s** | Portal Space Apps / Edição | [`03-papeis-equipe/papel-5-submissao-video-e-formulario.md`](03-papeis-equipe/papel-5-submissao-video-e-formulario.md) |

---

### 3. Prazos e Marcos Críticos

* **Prazo Final:** Domingo, 15 de novembro às **23:59 (horário local)**.
* **Congelamento de Código (Code Freeze):** **22:45** — a partir daqui, foco exclusivo na exportação dos slides, link do vídeo e preenchimento final do formulário.
* **Validação dos Links:** O link dos slides/vídeo e do GitHub deve abrir perfeitamente em uma janela anônima (sem exigir login).
* **Envio da Submissão:** Realizado até **23:30** para evitar instabilidade nos minutos finais da plataforma.
