"""
Protótipo Funcional — Módulo B (Agente de Atendimento) e Módulo C (Motor de Margem e Estoque)
Projeto Vértice Retail | AI Consulting Lab — Grupo 18
Prompt 5 — Solução, Arquitetura de IA e Protótipo
Integrantes: Ingrid Soares e Pedro Ribeiro (pedrorpr)

Este script roda sobre os dados reais de vendas.csv e estoque.csv do case e demonstra,
de forma determinística e auditável, a lógica de decisão que em produção seria executada
por um LLM (function calling) e por um motor de regras de precificação/estoque.
"""

import os
import json
import numpy as np
import pandas as pd


# =====================================================================
# MÓDULO B — CUSTOMER SERVICE AGENT
# =====================================================================

class CustomerServiceAgent:
    """
    Reproduz o pipeline de triagem descrito no System Prompt (Seção 4.2):
    classificação de intenção -> sentimento -> risco de churn -> seleção de
    ferramenta (function calling) -> resposta humanizada + payload JSON.

    Em produção, os passos de classificação seriam delegados a uma chamada
    real ao LLM com o system prompt oficial; aqui a lógica é reproduzida de
    forma determinística (regras + simulação de API) para permitir testes
    automatizados e demonstração offline à banca avaliadora.
    """

    def __init__(self, tracking_api=None):
        self.tracking_api = tracking_api or self._mock_tracking_api

    # ---- Ferramentas disponíveis para o agente (function calling) ----
    def consultar_status_transportadora(self, order_id):
        return self.tracking_api(order_id)

    def gerar_voucher_logistica_reversa(self, order_id, motivo):
        codigo = f"VLR-{order_id[-5:]}-{motivo[:3].upper()}"
        return {
            "voucher_id": codigo,
            "order_id": order_id,
            "motivo": motivo,
            "status": "gerado",
            "prazo_postagem_dias": 5,
        }

    def escalar_operador_humano_n2(self, ticket_id, resumo, prioridade):
        return {
            "ticket_id": ticket_id,
            "fila": "N2",
            "prioridade": prioridade,
            "resumo": resumo,
            "status": "escalado",
        }

    def _mock_tracking_api(self, order_id):
        # Simulação da API real de transportadora — em produção, chamada HTTP autenticada.
        base = {
            "ORD-058083": {
                "status": "Em trânsito",
                "local_atual": "CD Extrema/MG",
                "previsao_entrega": "2026-09-24",
                "tracking_url": f"https://rastreio.correios.com.br/{'ORD-058083'}",
            }
        }
        return base.get(order_id, {
            "status": "Em trânsito",
            "local_atual": "Centro de distribuição regional",
            "previsao_entrega": "consultar API de transportadora",
            "tracking_url": f"https://rastreio.correios.com.br/{order_id}",
        })

    # ---- Classificação (proxy determinístico do LLM) ----
    def classificar(self, texto_cliente):
        t = texto_cliente.lower()
        irritado = any(p in t for p in ["péssimo", "absurdo", "inaceitável", "revoltante", "!!"])

        if any(p in t for p in ["rasgad", "defeito", "quebrad", "manchad", "com defeito", "veio com"]):
            intencao = "Defeito"
            sentimento = "Critico/Irritado" if irritado else "Negativo"
            risco = "Alto"
        elif any(p in t for p in ["tamanho", "numeração", "trocar por um", "maior", "menor"]):
            intencao = "Troca de Tamanho"
            sentimento = "Neutro"
            risco = "Baixo"
        elif any(p in t for p in ["onde est", "rastre", "nada até agora", "não chegou", "não atualiza"]):
            intencao = "Rastreamento"
            sentimento = "Critico/Irritado" if irritado else "Negativo"
            risco = "Alto" if irritado else "Medio"
        elif any(p in t for p in ["obrigad", "adorei", "parabéns", "excelente"]):
            intencao, sentimento, risco = "Elogio", "Positivo", "Baixo"
        else:
            intencao, sentimento, risco = "Outros", "Neutro", "Baixo"

        return intencao, sentimento, risco

    def processar(self, texto_cliente, order_id, canal_entrada, ticket_id=None):
        intencao, sentimento, risco = self.classificar(texto_cliente)
        acao_tomada = None
        dados_acao = {}

        if intencao == "Rastreamento":
            dados_acao = self.consultar_status_transportadora(order_id)
            acao_tomada = "consultar_status_transportadora"
            mensagem = (
                f"Encontrei seu pedido {order_id}! Ele está \"{dados_acao['status']}\" em "
                f"{dados_acao['local_atual']}, com previsão de entrega em {dados_acao['previsao_entrega']}. "
                f"Você acompanha em tempo real aqui: {dados_acao['tracking_url']}."
            )
        elif intencao == "Defeito":
            dados_acao = self.gerar_voucher_logistica_reversa(order_id, "defeito")
            acao_tomada = "gerar_voucher_logistica_reversa"
            mensagem = (
                f"Sinto muito pelo transtorno! Já gerei o voucher {dados_acao['voucher_id']} para devolução sem "
                f"custo — a etiqueta chega por e-mail em até {dados_acao['prazo_postagem_dias']} dias úteis. Assim que "
                f"recebermos o item, processamos o reembolso ou a troca imediatamente."
            )
        elif intencao == "Troca de Tamanho":
            dados_acao = self.gerar_voucher_logistica_reversa(order_id, "troca de tamanho")
            acao_tomada = "gerar_voucher_logistica_reversa"
            mensagem = (
                f"Sem problema! Gerei o voucher {dados_acao['voucher_id']} para a troca — envie o item com a "
                f"etiqueta que chega em até {dados_acao['prazo_postagem_dias']} dias úteis, e já deixamos o novo "
                f"tamanho reservado assim que a postagem for confirmada."
            )
        else:
            mensagem = "Obrigado pela mensagem! Um de nossos especialistas vai analisar e retornar em instantes."

        if risco == "Alto":
            resumo = f"Cliente relata '{intencao}' com tom {sentimento}. Pedido {order_id}. Ação automática: {acao_tomada}."
            self.escalar_operador_humano_n2(ticket_id or order_id, resumo, "Alta")
            mensagem += " Também priorizei seu atendimento com um especialista humano, que vai te acompanhar de perto até a solução final."
            acao_tomada = f"{acao_tomada} + escalar_operador_humano_n2"

        return {
            "order_id": order_id,
            "canal_entrada": canal_entrada,
            "intencao": intencao,
            "sentimento": sentimento,
            "risco_churn": risco,
            "acao_executada": acao_tomada,
            "dados_ferramenta": dados_acao,
            "mensagem_cliente": mensagem,
        }


# =====================================================================
# MÓDULO C — MARGIN AND INVENTORY OPTIMIZER
# =====================================================================

class MarginAndInventoryOptimizer:
    def __init__(self, vendas_path, estoque_path):
        self.vendas = pd.read_csv(vendas_path)
        self.estoque = pd.read_csv(estoque_path)
        self.full = None
        self.med_giro = None
        self.med_margem = None

    def preparar_base(self):
        agg = self.vendas.groupby("sku_id").agg(
            qtd_vendida=("quantidade", "sum"),
            receita_liquida=("receita_liquida", "sum"),
            margem_contribuicao=("margem_contribuicao", "sum"),
        ).reset_index()

        full = self.estoque.merge(agg, on="sku_id", how="left")
        cols = ["qtd_vendida", "receita_liquida", "margem_contribuicao"]
        full[cols] = full[cols].fillna(0)

        full["valor_estoque_custo"] = full["estoque_fisico"] * full["custo_unitario"]
        full["giro_anual"] = np.where(full["estoque_fisico"] > 0, full["qtd_vendida"] / full["estoque_fisico"], 0)

        # Margem realizada (quando houve venda) com fallback para margem de tabela
        # (preco_venda_sugerido vs custo_unitario) para SKUs sem nenhuma venda no período.
        full["margem_pct_realizada"] = np.where(full["receita_liquida"] > 0,
                                                 full["margem_contribuicao"] / full["receita_liquida"], np.nan)
        full["margem_pct_tabela"] = (full["preco_venda_sugerido"] - full["custo_unitario"]) / full["preco_venda_sugerido"]
        full["margem_pct"] = full["margem_pct_realizada"].fillna(full["margem_pct_tabela"])

        self.full = full
        return full

    def classificar_quadrantes(self):
        if self.full is None:
            self.preparar_base()

        self.med_giro = self.full["giro_anual"].median()
        self.med_margem = self.full["margem_pct"].median()

        def classifica(row):
            giro_alto = row["giro_anual"] >= self.med_giro
            margem_alta = row["margem_pct"] >= self.med_margem
            if not giro_alto and margem_alta:
                return "Q1 - Joias Escondidas"
            if not giro_alto and not margem_alta:
                return "Q2 - Estoque Critico / Risco de Obsolescencia"
            if giro_alto and not margem_alta:
                return "Q3 - Vampiros de Margem"
            return "Q4 - Campeoes de Rentabilidade"

        self.full["quadrante"] = self.full.apply(classifica, axis=1)
        return self.full

    def resumo_quadrantes(self):
        if self.full is None or "quadrante" not in self.full.columns:
            self.classificar_quadrantes()
        resumo = self.full.groupby("quadrante").agg(
            n_skus=("sku_id", "count"),
            pecas=("estoque_fisico", "sum"),
            valor_custo=("valor_estoque_custo", "sum"),
        ).reset_index()
        resumo["pct_valor_estoque"] = resumo["valor_custo"] / resumo["valor_custo"].sum() * 100
        return resumo.sort_values("valor_custo", ascending=False)

    def skus_parados_para_liquidacao(self, top_n=10):
        """
        SKUs com zero unidades vendidas no período E estoque físico > 0 — ou seja,
        estoque genuinamente parado (obsolescência), não confundir com SKUs esgotados
        (estoque_fisico == 0 apesar de terem vendido, que é sinal de ruptura, não de excesso).
        """
        if self.full is None or "quadrante" not in self.full.columns:
            self.classificar_quadrantes()
        candidatos = self.full[(self.full["qtd_vendida"] == 0) & (self.full["estoque_fisico"] > 0)].copy()
        candidatos = candidatos.sort_values("valor_estoque_custo", ascending=False)
        cols = ["sku_id", "nome_produto", "categoria", "estoque_fisico", "custo_unitario",
                "valor_estoque_custo", "quadrante"]
        return candidatos[cols].head(top_n), len(candidatos), candidatos["valor_estoque_custo"].sum()

    def preco_minimo_liquidacao(self, sku_id, desconto_pretendido_pct):
        """Trava algorítmica: preco_venda >= custo_unitario (nunca vender abaixo do custo contábil)."""
        row = self.estoque[self.estoque["sku_id"] == sku_id].iloc[0]
        preco_base = row["preco_venda_sugerido"]
        custo = row["custo_unitario"]
        preco_com_desconto = preco_base * (1 - desconto_pretendido_pct)
        preco_final = max(preco_com_desconto, custo)
        return {
            "sku_id": sku_id,
            "preco_base": round(preco_base, 2),
            "desconto_solicitado_pct": round(desconto_pretendido_pct * 100, 1),
            "preco_com_desconto_solicitado": round(preco_com_desconto, 2),
            "custo_unitario": round(custo, 2),
            "preco_final_aplicado": round(preco_final, 2),
            "trava_de_margem_acionada": bool(preco_com_desconto < custo),
        }


def avaliar_margem_checkout(receita_bruta, desconto_reais, custo_produto, custo_frete_real):
    """
    Guardrail de checkout (Seção 5.2):
    Margem Estimada = Receita Bruta - Descontos - Custo dos Produtos - Custo de Frete Real
    Se negativa, o checkout é bloqueado/ajustado antes da confirmação do pedido.
    """
    margem_estimada = receita_bruta - desconto_reais - custo_produto - custo_frete_real
    aprovado = margem_estimada >= 0
    ajuste_sugerido = None
    if not aprovado:
        desconto_maximo_permitido = max(receita_bruta - custo_produto - custo_frete_real, 0)
        frete_subsidiado_maximo = max(receita_bruta - desconto_reais - custo_produto, 0)
        ajuste_sugerido = {
            "desconto_maximo_permitido": round(desconto_maximo_permitido, 2),
            "frete_subsidiado_maximo": round(frete_subsidiado_maximo, 2),
        }
    return {
        "receita_bruta": receita_bruta,
        "desconto_reais": desconto_reais,
        "custo_produto": custo_produto,
        "custo_frete_real": custo_frete_real,
        "margem_estimada": round(margem_estimada, 2),
        "checkout_aprovado": aprovado,
        "ajuste_sugerido": ajuste_sugerido,
    }


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("=" * 78)
    print(" PROTÓTIPO PROMPT 5 — MÓDULO B (AGENTE DE ATENDIMENTO) E MÓDULO C (MARGEM/ESTOQUE)")
    print("=" * 78)

    # ------------------------------------------------------------
    # MÓDULO B — 3 casos de teste sobre order_ids reais do dataset
    # ------------------------------------------------------------
    print("\n### MÓDULO B — AGENTE DE ATENDIMENTO: CASOS DE TESTE ###\n")
    agent = CustomerServiceAgent()

    casos = [
        {
            "rotulo": "CASO A — Rastreio básico (30% da dor de SAC)",
            "texto_cliente": "Comprei semana passada e nada até agora. Péssimo.",
            "order_id": "ORD-058083",
            "canal_entrada": "WhatsApp",
            "ticket_id": "TKT-000016",
        },
        {
            "rotulo": "CASO B — Produto com defeito (25,2% das devoluções)",
            "texto_cliente": "Comprei o Protetor Solar Oversize Verde e o produto chegou com o frasco rasgado e vazando. Um absurdo!",
            "order_id": "ORD-049533",
            "canal_entrada": "WhatsApp",
            "ticket_id": "TKT-100049",
        },
        {
            "rotulo": "CASO C — Troca de tamanho (24,8% das devoluções)",
            "texto_cliente": "Oi, comprei a Blusa de Tricô Oversize Branco mas veio pequena. Consigo trocar por um tamanho maior?",
            "order_id": "ORD-039721",
            "canal_entrada": "Webchat",
            "ticket_id": "TKT-100050",
        },
    ]

    resultados_agente = []
    for caso in casos:
        print("-" * 78)
        print(caso["rotulo"])
        print(f"Cliente disse: \"{caso['texto_cliente']}\"")
        resultado = agent.processar(
            texto_cliente=caso["texto_cliente"],
            order_id=caso["order_id"],
            canal_entrada=caso["canal_entrada"],
            ticket_id=caso["ticket_id"],
        )
        resultados_agente.append(resultado)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))

    # ------------------------------------------------------------
    # MÓDULO C — Quadrantes de margem/estoque sobre a base real
    # ------------------------------------------------------------
    print("\n" + "=" * 78)
    print("### MÓDULO C — MOTOR DE MARGEM E ESTOQUE ###\n")

    optimizer = MarginAndInventoryOptimizer(
        vendas_path=os.path.join(base_dir, "vendas.csv"),
        estoque_path=os.path.join(base_dir, "estoque.csv"),
    )
    optimizer.classificar_quadrantes()
    resumo = optimizer.resumo_quadrantes()

    print(f"Mediana de giro anual (corte dos quadrantes): {optimizer.med_giro:.4f}x")
    print(f"Mediana de margem de contribuição (corte dos quadrantes): {optimizer.med_margem*100:.2f}%\n")
    print(resumo.to_string(index=False, formatters={
        "valor_custo": lambda x: f"R$ {x:,.2f}",
        "pct_valor_estoque": lambda x: f"{x:.1f}%",
    }))

    print("\n--- Fila prioritária de desmobilização (SKUs com zero vendas no período) ---")
    top10, n_total, valor_total = optimizer.skus_parados_para_liquidacao(top_n=10)
    print(f"Total de SKUs parados (zero vendas, com estoque físico > 0): {n_total} | Valor imobilizado a custo: R$ {valor_total:,.2f}\n")
    print(top10.to_string(index=False, formatters={
        "custo_unitario": lambda x: f"R$ {x:,.2f}",
        "valor_estoque_custo": lambda x: f"R$ {x:,.2f}",
    }))

    print("\n--- Trava de preço mínimo de liquidação (exemplo) ---")
    exemplo_sku = top10.iloc[0]["sku_id"]
    print(json.dumps(optimizer.preco_minimo_liquidacao(exemplo_sku, desconto_pretendido_pct=0.85), ensure_ascii=False, indent=2))

    # ------------------------------------------------------------
    # MÓDULO C — Guardrail de checkout contra margem negativa
    # ------------------------------------------------------------
    print("\n--- Guardrail de checkout: 3 pedidos reais com margem negativa da base ---")
    vendas = optimizer.vendas
    exemplos_negativos = vendas[vendas["margem_contribuicao"] < 0].head(3)
    for _, pedido in exemplos_negativos.iterrows():
        avaliacao = avaliar_margem_checkout(
            receita_bruta=pedido["receita_bruta"],
            desconto_reais=pedido["desconto_reais"],
            custo_produto=pedido["custo_produto"],
            custo_frete_real=pedido["custo_frete"],
        )
        print(f"\nPedido {pedido['order_id']} ({pedido['produto']}):")
        print(json.dumps(avaliacao, ensure_ascii=False, indent=2))

    print("\n" + "=" * 78)
    print(" FIM DA EXECUÇÃO DO PROTÓTIPO ")
    print("=" * 78)


if __name__ == "__main__":
    main()
