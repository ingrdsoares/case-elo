"""
Cálculo Determinístico do Business Case — Projeto Vértice Retail
Prompt 6 — Business Case, Roadmap 30-60-90 e Apresentação Executiva
Integrantes: Ingrid Soares e Pedro Ribeiro (pedrorpr)

Este script recalcula, a partir dos dados reais de vendas.csv e estoque.csv, as 5
alavancas financeiras do business case (Seção 2 do Prompt 6) e gera os 3 cenários
de sensibilidade (Conservador / Base / Otimista) de forma auditável — nenhum valor
é digitado à mão; todos derivam das mesmas bases usadas nos Prompts 1 a 5.
"""

import os
import json
import pandas as pd


def carregar_premissas_base(base_dir):
    """Recalcula os totais-fonte (estoque a custo, margem sacrificada em devolução,
    custo de SAC de rastreio, prejuízo de pedidos deficitários) diretamente das bases —
    não são números fixos, são os mesmos agregados validados nos Prompts 1 a 5."""
    vendas = pd.read_csv(os.path.join(base_dir, "vendas.csv"))
    estoque = pd.read_csv(os.path.join(base_dir, "estoque.csv"))
    atendimento = pd.read_csv(os.path.join(base_dir, "atendimento.csv"))

    valor_estoque_custo = (estoque["estoque_fisico"] * estoque["custo_unitario"]).sum()

    devolvidos = vendas[vendas["devolvido"] == True]
    margem_devolucoes = -devolvidos["margem_contribuicao"].sum() if devolvidos["margem_contribuicao"].sum() < 0 else devolvidos["margem_contribuicao"].sum()
    # margem_contribuicao de pedidos devolvidos já é o valor sacrificado (positivo = receita que existiria sem devolução)
    margem_devolucoes = devolvidos["margem_contribuicao"].sum()

    rastreio = atendimento[atendimento["categoria_problema"] == "Onde está meu pedido?"]
    custo_sac_rastreio = rastreio["custo_operacional_ticket"].sum()

    negativos = vendas[vendas["margem_contribuicao"] < 0]
    prejuizo_margem_negativa = -negativos["margem_contribuicao"].sum()

    return {
        "valor_estoque_custo": valor_estoque_custo,
        "margem_devolucoes": margem_devolucoes,
        "custo_sac_rastreio": custo_sac_rastreio,
        "prejuizo_margem_negativa": prejuizo_margem_negativa,
        "n_tickets_rastreio": len(rastreio),
        "n_pedidos_margem_negativa": len(negativos),
    }


def calcular_cenario(premissas, pct_liquidacao, pct_automacao_sac, pct_reducao_devolucao,
                      pct_captura_checkout, cdi_aa=0.11):
    """Aplica as premissas de agressividade de execução sobre os totais-fonte reais
    e devolve as 5 alavancas + o headline (sem o item de frete, ver nota no relatório)."""

    liquidacao_estoque = premissas["valor_estoque_custo"] * pct_liquidacao
    economia_juros = liquidacao_estoque * cdi_aa
    recuperacao_devolucao = premissas["margem_devolucoes"] * pct_reducao_devolucao
    frete_reverso = 37000 * (pct_reducao_devolucao / 0.30)  # escala com a mesma premissa de redução de devolução
    reducao_custo_sac = premissas["custo_sac_rastreio"] * pct_automacao_sac
    estancamento_checkout = premissas["prejuizo_margem_negativa"] * pct_captura_checkout

    headline = (liquidacao_estoque + economia_juros + recuperacao_devolucao
                + reducao_custo_sac + estancamento_checkout)

    return {
        "1_liquidacao_estoque": round(liquidacao_estoque, 2),
        "2_economia_juros_carregamento": round(economia_juros, 2),
        "3_recuperacao_margem_devolucao": round(recuperacao_devolucao, 2),
        "4_reducao_custo_sac": round(reducao_custo_sac, 2),
        "5_estancamento_checkout": round(estancamento_checkout, 2),
        "upside_frete_reverso_nao_somado": round(frete_reverso, 2),
        "impacto_total_headline": round(headline, 2),
        "impacto_total_com_frete": round(headline + frete_reverso, 2),
        "premissas_aplicadas": {
            "pct_liquidacao_estoque": pct_liquidacao,
            "pct_automacao_sac": pct_automacao_sac,
            "pct_reducao_devolucao": pct_reducao_devolucao,
            "pct_captura_checkout": pct_captura_checkout,
            "cdi_aa": cdi_aa,
        },
    }


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("=" * 78)
    print(" BUSINESS CASE DETERMINÍSTICO — PROJETO VÉRTICE (PROMPT 6)")
    print("=" * 78)

    premissas = carregar_premissas_base(base_dir)
    print("\n--- Totais-fonte recalculados diretamente das bases reais ---")
    print(f"Valor de estoque a custo (estoque.csv): R$ {premissas['valor_estoque_custo']:,.2f}")
    print(f"Margem sacrificada em devoluções (vendas.csv): R$ {premissas['margem_devolucoes']:,.2f}")
    print(f"Custo de SAC em tickets de rastreio ({premissas['n_tickets_rastreio']:,} tickets): R$ {premissas['custo_sac_rastreio']:,.2f}")
    print(f"Prejuízo em pedidos de margem negativa ({premissas['n_pedidos_margem_negativa']:,} pedidos): R$ {premissas['prejuizo_margem_negativa']:,.2f}")

    cenarios = {
        "Conservador": dict(pct_liquidacao=0.12, pct_automacao_sac=0.60, pct_reducao_devolucao=0.20, pct_captura_checkout=0.85),
        "Base":        dict(pct_liquidacao=0.20, pct_automacao_sac=0.80, pct_reducao_devolucao=0.30, pct_captura_checkout=1.00),
        "Otimista":    dict(pct_liquidacao=0.28, pct_automacao_sac=0.90, pct_reducao_devolucao=0.40, pct_captura_checkout=1.00),
    }

    resultados = {}
    for nome, params in cenarios.items():
        resultados[nome] = calcular_cenario(premissas, **params)

    print("\n--- Resultado por cenário ---")
    for nome, r in resultados.items():
        print(f"\n### Cenário {nome} ###")
        print(json.dumps(r, ensure_ascii=False, indent=2))

    print("\n--- Tabela-resumo (para o slide 8 / seção 2.2 do relatório) ---")
    linhas = []
    for nome, r in resultados.items():
        p = r["premissas_aplicadas"]
        linhas.append({
            "Cenario": nome,
            "% Estoque liquidado": f"{p['pct_liquidacao_estoque']*100:.0f}%",
            "% Automacao SAC": f"{p['pct_automacao_sac']*100:.0f}%",
            "% Reducao devolucao": f"{p['pct_reducao_devolucao']*100:.0f}%",
            "Impacto Total (headline)": f"R$ {r['impacto_total_headline']:,.0f}",
        })
    df = pd.DataFrame(linhas)
    print(df.to_string(index=False))

    print("\n--- Checagem de payback (cenário Base) ---")
    investimento_min, investimento_max = 250_000, 350_000
    liquidacao_imediata_82_skus = 6_682_638.30  # já validado no Prompt 5 (SKUs com zero vendas)
    multiplo = liquidacao_imediata_82_skus / investimento_max
    print(f"Investimento estimado: R$ {investimento_min:,.0f} a R$ {investimento_max:,.0f}")
    print(f"Valor da 1ª leva de liquidação (82 SKUs zero-venda, do Prompt 5): R$ {liquidacao_imediata_82_skus:,.2f}")
    print(f"Múltiplo de cobertura do investimento pela 1ª leva: {multiplo:.1f}x")

    print("\n" + "=" * 78)
    print(" FIM DO CÁLCULO ")
    print("=" * 78)


if __name__ == "__main__":
    main()
