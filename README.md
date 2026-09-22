# Case Vértice Retail — AI Consulting Lab
## BootCamp Nova Geração | EloGroup (2026)

Repositório oficial do projeto final de consultoria estratégica com Inteligência Artificial e Analytics para a **Vértice Retail**, desenvolvido pelo **Grupo 18**.

---

## 👥 Integrantes — Grupo 18

| Nome | Função no Projeto | Perfil GitHub |
| :--- | :--- | :--- |
| **Ingrid Soares** | Strategy & AI Consultant | [@ingrdsoares](https://github.com/ingrdsoares) |
| **Pedro Ribeiro** | Strategy & Analytics Consultant | [@pedrorpr](https://github.com/pedrorpr) |

* **Mentoria Técnica:** Coutinho, EloGroup
* **Data da Banca / Pitch Final:** 23 de Setembro de 2026

---

## 🎯 Contexto e Pergunta Central do Case

A **Vértice Retail** é uma marca digital de moda, beleza e lifestyle voltada para jovens adultos. A empresa cresceu fortemente por meio de e-commerce, redes sociais, influenciadores e marketplaces, alcançando mais de **R$ 20,5 milhões** em faturamento bruto anual.

Entretanto, a rentabilidade começou a sofrer forte pressão, dados encontram-se fragmentados e a tomada de decisão ainda depende de processos manuais e intuição. 

A diretoria do cliente (CEO, CFO, CMO e COO) contratou a consultoria para responder à questão:
> *"Como podemos usar dados e IA para melhorar rentabilidade, eficiência operacional e qualidade da tomada de decisão nos próximos 90 dias?"*

---

## 🧭 Metodologia & Pipeline dos Prompts

A squad adota uma abordagem consultiva estruturada em etapas consecutivas, garantindo rastreabilidade analítica rigorosa:

```mermaid
flowchart LR
    P1["Prompt 1<br><b>Data Audit & Exploração</b>"] --> P2["Prompt 2<br><b>Investigação & Hipóteses</b>"]
    P2 --> P3["Prompt 3<br><b>Teste de Causalidade</b>"]
    P3 --> P4["Prompt 4<br><b>Diagnóstico Executivo</b>"]
    P4 --> P5["Prompt 5<br><b>Solução IA & Protótipo</b>"]
    P5 --> P6["Prompt 6<br><b>Business Case & Pitch</b>"]
```

1. **[Prompt 1 — Data Audit e Exploração Inicial](diagnostico/01_prompt1_data_audit.md):** Auditoria das 5 bases, completude, consistência, período comum e matriz de integração.
2. **[Prompt 2 — Investigação Aprofundada e Hipóteses](diagnostico/02_prompt2_investigacao_hipoteses.md):** Reconstrução do problema, issue tree, investigação aprofundada de estoque desproporcional e devoluções.
3. **[Prompt 3 — Teste de Hipóteses e Causa Raiz](diagnostico/03_prompt3_teste_hipoteses_causa_raiz.md):** Teste de falseabilidade, diferenciação de causa vs. sintoma vs. anomalia de dados.
4. **[Prompt 4 — Síntese Executiva do Diagnóstico](diagnostico/04_prompt4_sintese_executiva.md):** Cadeia causal quantificada, formulação definitiva do problema e decisões críticas.
5. **[Sugestões para Prompts 5 e 6](sugestoes_prompts_5_e_6.md):** Propostas estruturadas para o desenho da solução de IA (Módulos A/B/C/D), protótipo, business case, roadmap 30-60-90 e roteiro da apresentação final.

---

## 📊 Principais Achados & Números-Chave

* **Estoque Imobilizado Crítico:** O valor de estoque físico a custo soma **R$ 348,70 milhões** (vs. faturamento líquido anual de R$ 18,89 milhões e CMV anual de R$ 8,28 milhões). O giro anual mediano é de apenas **0,06x** (~16,8 anos de estoque na velocidade atual de vendas), concentrando 864 mil peças em Moda.
* **Perda Operacional em Devoluções:** **4.127 pedidos devolvidos (14,87%)**, destruindo **R$ 2,82 milhões em receita bruta** e **R$ 1,52 milhão em margem de contribuição**. 69,6% das devoluções decorrem de falhas operacionais: *Produto com defeito (25,2%)*, *Tamanho errado (24,8%)* e *Atraso na entrega (19,6%)*.
* **Gargalo no Customer Service:** **35.841 chamados de atendimento** totalizando **R$ 532.260 em custo operacional**, onde **30,0% (10.765 chamados)** são simples consultas de *"Onde está meu pedido?"* com tempo médio de resposta de 135 minutos — plenamente automatizáveis com agentes de IA.
* **Anomalia de Pipeline / Guest Checkout:** Concentração severa em IDs genéricos (`CLI-11830` com 11.282 pedidos e `CLI-01729` com 5.664 pedidos), indicando agregação de compras anônimas ou falha no rastreio de checkout.

---

## 📁 Estrutura do Repositório

```text
case-elo/
├── README.md                                  # Apresentação do projeto e integrantes
├── .gitignore                                 # Regras de exclusão git
├── orientacoes.md                             # Diretrizes oficiais de entrega da coordenação
├── Case Vértice 1.html                        # Briefing executivo interativo do case
├── sugestoes_prompts_5_e_6.md                 # Recomendações e arquitetura para Prompts 5 e 6
│
├── diagnostico/                               # Relatórios dos Prompts 1 a 4
│   ├── 01_prompt1_data_audit.md               # Prompt 1: Auditoria e Inventário de Dados
│   ├── 02_prompt2_investigacao_hipoteses.md   # Prompt 2: Investigação e Issue Tree
│   ├── 03_prompt3_teste_hipoteses_causa_raiz.md # Prompt 3: Teste Causal e Refutação
│   └── 04_prompt4_sintese_executiva.md        # Prompt 4: Síntese e Problema de Negócio
│
├── scripts/                                   # Scripts de automação e modelagem
│   └── analise_vertice.py                     # Pipeline determinístico de cálculos e visualizações
│
├── charts/                                    # Gráficos analíticos gerados
│   ├── chart_estoque_vs_vendas.png
│   ├── chart_motivos_devolucao.png
│   ├── chart_atendimento_tickets.png
│   └── chart_margem_desconto_canal.png
│
├── atendimento.csv                            # Base transacional de tickets de suporte
├── clientes.csv                               # Base cadastral e RFM de clientes
├── estoque.csv                                # Base de SKUs, estoque físico e custos
├── marketing.csv                              # Base de campanhas, investimento e canais
└── vendas.csv                                 # Base transacional de pedidos e margens
```

---

## 🚀 Como Reproduzir as Análises

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/ingrdsoares/case-elo.git
   cd case-elo
   ```

2. **Instalar dependências (Python 3.8+):**
   ```bash
   pip install pandas numpy matplotlib
   ```

3. **Executar pipeline analítico:**
   ```bash
   python3 scripts/analise_vertice.py
   ```
   Os gráficos serão gerados na pasta `charts/` e todas as métricas validadas no console.

---

## 📦 Conformidade com as Orientações de Entrega

Conforme estipulado em `orientacoes.md`:
* **Código & Rastreabilidade:** Versionado via Git no repositório oficial [github.com/ingrdsoares/case-elo](https://github.com/ingrdsoares/case-elo).
* **Documentação & Materiais Complementares:** Pacote consolidado em formato `.zip` com os documentos técnicos em Markdown (`.md`), relatórios gerenciais e visualizações.
* **Pitch Final (23/09):** Apresentação executiva em conformidade com o roteiro de 11 slides previsto no briefing.
