# Índice Sanitizado e Guia de Navegação dos Documentos Space Apps
## Limpeza, Mapeamento de Conteúdo e Eliminação de Duplicatas

Este documento organiza todo o material coletado na pasta `docs/spaceapps/`, eliminando redundâncias e indicando onde encontrar cada informação oficial.

---

### 1. Mapa de Equivalência e Sanitização dos Arquivos Brutos (`info*.md`)

Dos 31 arquivos coletados, identificamos cópias redundantes (raspadas repetidamente do portal). Abaixo está a tabela de higienização indicando o arquivo canônico (*fonte oficial limpa*) e os que são duplicatas descartáveis:

| Tema Principal | Arquivo Canônico Recomendado | Arquivos Duplicados / Secundários | Status |
|---|---|---|---|
| **Guia de Submissão de Projetos** | [`info27.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info27.md) *(Inglês oficial)* e [`info.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info.md) *(Português)* | — | **Ativo (Crítico)** |
| **Guia de Avaliação & Rubricas (Judging)** | [`info26.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info26.md) *(Versão completa)* | `info2.md`, `info7.md` | **Ativo (`info26.md`)** |
| **Termos e Condições do Participante** | [`info5.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info5.md) *(Inglês oficial)* | `info8.md`, `info14.md`, `info28.md` | **Ativo (`info5.md`)** |
| **O Nosso Desafio (Details)** | [`info22.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info22.md) *(Enunciado completo)* | `info20.md` *(lista geral)* | **Ativo (Crítico)** |
| **Recursos Oficiais do Desafio (Resources)** | [`info18.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info18.md) *(APIs, FIRMS, CONAE)* | — | **Ativo (Crítico)** |
| **Regras do Evento Universal (Equipes 2 a 6)** | [`info21.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info21.md) | `info19.md` *(Guia PT)* | **Ativo (Crítico)** |
| **Playbook de Slides (7) e Vídeo (30s)** | [`info29.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info29.md) | — | **Ativo (Crítico)** |
| **Metodologia Científica e Fórmulas** | [`info30.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info30.md) | — | **Ativo (Crítico)** |
| **Checklist de Aprovação dos Jurados** | [`info31.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info31.md) | `info4.md` *(10 prêmios)* | **Ativo (Crítico)** |
| **Uso da Marca NASA (Guidelines)** | [`info3.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info3.md) | — | **Ativo (Regra Legal)** |
| **Licenciamento Open Source (OSI)** | [`info16.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info16.md) e [`info17.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info17.md) *(Apache 2.0)* | — | **Ativo (Licença)** |
| **Agências Parceiras (CONAE / AEB)** | [`info15.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info15.md) | — | **Ativo (Citações)** |
| **FAQs Gerais e Chat Connect** | [`info25.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info25.md) e [`info24.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/info24.md) | `info13.md` | **Secundário (Consulta)** |
| **Páginas Institucionais / Blog** | `info6.md`, `info9.md`, `info10.md`, `info11.md`, `info12.md`, `info23.md` | — | **Contexto Histórico** |

---

### 2. Os Documentos Mestres do Projeto (Onde a equipe deve focar)

Para trabalhar de forma ágil, os 5 membros da equipe devem consultar prioritariamente a pasta `docs/spaceapps/` dividida por papéis:

1. [`00-PLANO-MESTRE-EQUIPE.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/00-PLANO-MESTRE-EQUIPE.md): Cronograma de sprint, metas e dependências entre os 5 membros.
2. [`PAPEL-1-COORDENACAO-E-INTEGRACAO.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/PAPEL-1-COORDENACAO-E-INTEGRACAO.md): Gestão do repositório, branchs, unificação de código e submissão.
3. [`PAPEL-2-CLAUDE-CODE-HARMONIZACAO.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/PAPEL-2-CLAUDE-CODE-HARMONIZACAO.md): **Instruções prontas para o Claude Code** (módulos Python de harmonização, cálculo de grade e API).
4. [`PAPEL-3-FRONTEND-CALENDARIO-WEB.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/PAPEL-3-FRONTEND-CALENDARIO-WEB.md): Construção do componente visual da matriz de queimadas no React/Vite.
5. [`PAPEL-4-DESIGN-E-SLIDES-7PAGINAS.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/PAPEL-4-DESIGN-E-SLIDES-7PAGINAS.md): Conteúdo exato e direcionamento visual dos 7 slides obrigatórios.
6. [`PAPEL-5-SUBMISSAO-VIDEO-E-FORMULARIO.md`](file:///home/dorneles/ecomp-ufsm-genai/fococerto-spaceapps/docs/spaceapps/PAPEL-5-SUBMISSAO-VIDEO-E-FORMULARIO.md): Roteiro de vídeo de 30s, respostas prontas em inglês para o portal e checklist de envio.
