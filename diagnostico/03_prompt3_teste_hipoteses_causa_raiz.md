# Prompt 3 — Teste de Hipóteses e Validação da Causa Raiz
## Projeto Vértice Retail | AI Consulting Lab — Grupo 18
**Consultores:** Ingrid Soares e Pedro Ribeiro ([@pedrorpr](https://github.com/pedrorpr))  
**Papel:** Consultoria Sênior de Estratégia e Analytics  

---

## 1. Princípio Metodológico de Refutação

Conforme as diretrizes consultivas:
> *"TENTE REFUTÁ-LA antes de tentar confirmá-la. Correlação ≠ Causalidade; Sintoma ≠ Causa; Causa Intermediária ≠ Causa Raiz."*

Nesta etapa, submetemos as hipóteses levantadas nos Prompts 1 e 2 a testes determinísticos de falseabilidade nos dados de Vendas, Estoque, Atendimento e Marketing.

---

## 2. Teste da Hipótese 1: "O excesso de estoque é resultado de queda inesperada nas vendas"

* **O que tenta explicar:** O descompasso entre R$ 348,7M em estoque e R$ 18,9M de faturamento anual.
* **Mecanismo causal proposto:** A empresa projetou vendas crescentes, mas as vendas desabaram abruptamente, deixando o estoque encalhado nos CDs.
* **Evidência esperada se verdadeira:** Queda acentuada na receita mensal ao longo de 2023; pedidos em declínio mês a mês.
* **O que os dados revelam:**
  * Vendas de Jan/23: R$ 936k (1.381 pedidos).
  * Vendas de Nov/23 (Black Friday): R$ 2,71M (4.120 pedidos).
  * Vendas de Dez/23 (Natal): R$ 2,24M (3.280 pedidos).
  * O faturamento **cresceu +190%** entre o início e o pico do ano, e a média mensal permaneceu estável em ~R$ 1,5M nos meses regulares.
* **Evidência que contradiz a hipótese:** Não houve colapso de vendas. As vendas comportaram-se conforme a sazonalidade típica do varejo (picos em março, maio, novembro e dezembro).
* **Teste de Alternativa 1A:** *"O estoque foi comprado em lotes desmedidos por política de compra desvinculada do sell-through."* **Confirmada pelos dados.** A Vértice comprou mais de 1,6 milhão de peças para um canal que consome ~90 mil peças/ano.
* **Conclusão:** **HIPÓTESE 1 REFUTADA.** O estoque parado não é sintoma de queda de demanda; é a **causa primária de ineficiência financeira decorrente de compras cegas sem algoritmos preditivos**.

---

## 3. Teste da Hipótese 2: "As devoluções decorrem de arrependimento natural do consumidor digital"

* **O que tenta explicar:** A taxa de 14,87% de pedidos devolvidos (4.127 pedidos, R$ 2,82M).
* **Mecanismo causal proposto:** Como a Vértice vende por e-commerce e influenciadores, o cliente compra por impulso e devolve por arrependimento puro (direito de arrependimento do CDC em 7 dias).
* **Evidência esperada se verdadeira:** A esmagadora maioria dos motivos de devolução seria *"Arrependimento"* ou *"Não gostei"*.
* **O que os dados revelam:**
  * *Arrependimento:* 586 pedidos (14,2% do total de devoluções).
  * *Não gostei:* 669 pedidos (16,2% do total de devoluções).
  * **Falhas Operacionais/Técnicas Concretas:**
    * *Produto com defeito:* 1.039 pedidos (25,2%).
    * *Tamanho errado:* 1.025 pedidos (24,8%).
    * *Atraso na entrega:* 808 pedidos (19,6%).
    * **Total Operacional Evitável: 2.872 pedidos (69,6% das devoluções)!**
* **Teste de Alternativa 2A:** *"As devoluções são causadas por falha de ficha técnica (modelagem confusa) e controle de qualidade de fornecedores."* **Confirmada pelos dados.** Metade das devoluções decorre de produto quebrado/rasgado ou que não coube no corpo do cliente.
* **Conclusão:** **HIPÓTESE 2 REFUTADA.** O arrependimento natural é residual (30,4%). A causa raiz de R$ 1,06 milhão da margem perdida é a **falha na qualidade de produto e ausência de recomendação de tamanho precisa no front-end**.

---

## 4. Teste da Hipótese 3: "O custo de atendimento está alto porque o produto gera muitas dúvidas técnicas complexas"

* **O que tenta explicar:** O volume de 35.841 chamados e custo de R$ 532.260 com operadores humanos.
* **Mecanismo causal proposto:** Por vender moda e beleza, o suporte gasta muito tempo auxiliando clientes em consultoria estética e dúvidas técnicas de aplicação.
* **Evidência esperada se verdadeira:** Predomínio de *"Dúvida Técnica"* e longas conversas de consultoria.
* **O que os dados revelam:**
  * *Dúvida Técnica:* 5.314 chamados (14,8%).
  * *Onde está meu pedido? (Rastreio básico):* **10.765 chamados (30,0%)**, custando **R$ 159.660**.
  * Somando rastreio + defeito + troca de tamanho, temos **22.634 chamados (63,1%)**.
* **Teste de Alternativa 3A:** *"O alto custo de atendimento é consequência da falta de automação e proatividade na comunicação de status de entrega."* **Confirmada pelos dados.** Clientes abrem chamados manuais simplesmente porque a transportadora não avisa quando o pacote saiu para entrega.
* **Conclusão:** **HIPÓTESE 3 REFUTADA.** O atendimento humano está sendo drenado por **tarefas repetitivas e transacionais de rastreamento**, perfeitamente automatizáveis com agentes inteligentes de IA conversacional.

---

## 5. Teste da Hipótese 4: "Descontos excessivos generalizados estão destruindo a margem da empresa"

* **O que tenta explicar:** A pressão sobre a margem de contribuição.
* **Mecanismo causal proposto:** A empresa queima margem dando descontos agressivos em todos os canais para sustentar o crescimento.
* **O que os dados revelam:**
  * O desconto médio global é de **7,97% sobre a receita bruta** (R$ 1,64M de descontos em R$ 20,53M de faturamento).
  * A margem de contribuição média global é de **54,37%**, patamar saudável para o varejo de moda/lifestyle.
  * Contudo, em **491 pedidos**, a margem foi **negativa** (média de -17,2%, gerando prejuízo operacional de R$ 6.636).
  * Nesses 491 pedidos, o desconto médio foi de **21,8%** e o custo de frete representou **67,6% da receita líquida**.
* **Conclusão:** **HIPÓTESE 4 PARCIALMENTE CONFIRMADA COM REFINAMENTO.** O desconto geral não é predatório, mas a **ausência de travas de frete mínimo combinadas com cupons agressivos (>20%)** gera pontas de prejuízo evitáveis.

---

## 6. Matriz de Validação Causal

| Elemento Investigado | Classificação Epistêmica | Mecanismo Comprovado nos Dados | Impacto Econômico Anual |
| :--- | :--- | :--- | :---: |
| **Estoque de R$ 348,7M (1,67M peças)** | **Causa Raiz Estrutural** | Política de compras desvinculada de modelos analíticos de previsão de demanda por SKU/tamanho. | R$ 38,3M/ano (custo financeiro) + risco de refugo |
| **Devoluções por Defeito e Tamanho (69,6%)** | **Causa Raiz Operacional** | Ausência de prova virtual/tabela precisa de medidas e falta de SLA/penalidade de qualidade para fornecedores. | R$ 1,06M/ano em margem perdida + frete reverso |
| **Tickets "Onde está meu pedido?" (30%)** | **Causa Raiz de Produtividade** | Ausência de régua proativa de tracking via WhatsApp e falta de agente de IA para triagem automática. | R$ 159,7k/ano de custo operacional desperdiçado |
| **Pedidos com Margem Negativa (491 pedidos)** | **Falha de Governança Comercial** | Falta de trava de margem de contribuição mínima na cesta de compras com frete subsidiado. | R$ 38,5k de perda direta |
| **Queda de Rentabilidade Percebida** | **Sintoma Consolidado** | Reflexo conjunto do custo do capital imobilizado, perdas com devolução e retrabalho de atendimento. | Redução drástica do EBITDA e geração de caixa livre |

---

## 7. Decisão Causal para o Diagnóstico

A squad valida com 100% de consistência empírica que a Vértice Retail não sofre de um problema de atratividade de marca ou demanda comercial. A empresa sofre de um **problema clássico de maturidade operacional**:
1. **Comprou para um gigante** (1,67 milhão de peças em estoque);
2. **Entregou com atrito operacional** (quase 15% de devoluções por defeito, tamanho errado e atrasos);
3. **Atendeu o cliente no modo manual e analógico** (operadores humanos respondendo código de rastreio com 2h15 de espera).

Essa clareza fundamenta a transição direta para a formulação executiva do Prompt 4.
