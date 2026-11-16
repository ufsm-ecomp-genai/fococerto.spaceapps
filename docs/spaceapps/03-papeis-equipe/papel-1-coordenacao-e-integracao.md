# Guia de Trabalho — Papel 1: Líder, Coordenação e Integração
**Responsável:** Fernando Dorneles da Silva  
**Foco:** Arquitetura Geral, Repositório Git, Antigravity e Revisão Final

---

### 1. Sua Missão no Time
Você é o ponto focal da equipe. Seu objetivo é garantir que o trabalho dos outros 4 integrantes se conecte perfeitamente, que o repositório git fique limpo e profissional, e que nenhuma regra eliminatória da NASA seja violada.

---

### 2. Suas Atribuições Específicas

1. **Gestão do Repositório Git:**
   * Garantir que as alterações da Pessoa 2 (Backend) e Pessoa 3 (Frontend) sejam integradas sem conflitos.
   * Manter o histórico de commits organizado com mensagens convencionais (`feat: ...`, `fix: ...`, `docs: ...`).
   * Configurar a licença oficial **Apache 2.0** no arquivo `LICENSE` da raiz.
2. **Supervisão do Modo de Demonstração / Sample (`--sample`):**
   * Garantir que os jurados possam rodar o projeto com 1 comando, sem precisar de credenciais ou bancos pesados:
     ```bash
     python3 -m app.cli --sample --cenario tocantins-escasso
     ```
   * Integrar a camada de harmonização para que ela também possa rodar sobre os dados locais de `data/samples_firms/`.
3. **Conexão com os Agentes de Raciocínio (O Diferencial do FocoCerto):**
   * Assegurar que, quando o calendário detectar um período anômalo/crítico, a chamada para o motor de raciocínio (Planner + Critic) funcione e gere a justificativa operacional de despacho de brigadas.
4. **Alinhamento do Time e Prazos:**
   * Monitorar o relógio: alertar a equipe para congelar código às **22:45**, para que a Pessoa 4 e Pessoa 5 tenham tempo hábil de fechar os links e o formulário sem desespero.
   * Verificar com a Pessoa 5 se todos os 5 membros estão oficialmente confirmados na aba "Membros" da equipe no portal da NASA.

---

### 3. Checklist de Entrega do Líder
- [ ] Licença `LICENSE` (Apache-2.0) criada na raiz do repositório.
- [ ] Código backend integrado com o frontend.
- [ ] Testes locais rodando limpos.
- [ ] Link do repositório GitHub público (quando você autorizar o push) configurado para a Pessoa 5 colar no portal.
