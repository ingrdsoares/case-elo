"""
Pipeline Determinístico de Análise e Diagnóstico: Case Vértice Retail
BootCamp Nova Geração | EloGroup - Grupo 18
Integrantes: Ingrid Soares e Pedro Ribeiro (pedrorpr)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print(" INICIANDO PIPELINE DE ANÁLISE — PROJETO VÉRTICE RETAIL ")
    print("=" * 70)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    charts_dir = os.path.join(base_dir, 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    # 1. Carregando dados
    vendas_path = os.path.join(base_dir, 'vendas.csv')
    mkt_path = os.path.join(base_dir, 'marketing.csv')
    cli_path = os.path.join(base_dir, 'clientes.csv')
    atend_path = os.path.join(base_dir, 'atendimento.csv')
    est_path = os.path.join(base_dir, 'estoque.csv')
    
    vendas = pd.read_csv(vendas_path)
    mkt = pd.read_csv(mkt_path)
    cli = pd.read_csv(cli_path)
    atend = pd.read_csv(atend_path)
    est = pd.read_csv(est_path)
    
    # 2. Resumo de Vendas
    print("\n--- 1. INDICADORES DE VENDAS ---")
    rec_bruta = vendas['receita_bruta'].sum()
    rec_liq = vendas['receita_liquida'].sum()
    desc_total = vendas['desconto_reais'].sum()
    cmv_total = vendas['custo_produto'].sum()
    frete_total = vendas['custo_frete'].sum()
    margem_total = vendas['margem_contribuicao'].sum()
    total_pedidos = len(vendas)
    
    print(f"Total de Pedidos: {total_pedidos:,}")
    print(f"Receita Bruta: R$ {rec_bruta:,.2f}")
    print(f"Receita Líquida: R$ {rec_liq:,.2f}")
    print(f"Descontos Concedidos: R$ {desc_total:,.2f} ({desc_total/rec_bruta*100:.2f}% da receita bruta)")
    print(f"Custo das Mercadorias Vendidas (CMV): R$ {cmv_total:,.2f}")
    print(f"Custo de Frete Total: R$ {frete_total:,.2f}")
    print(f"Margem de Contribuição: R$ {margem_total:,.2f} ({margem_total/rec_liq*100:.2f}% da receita líquida)")
    
    # Devoluções
    devolvidos = vendas[vendas['devolvido'] == True]
    print(f"\nDevoluções Totais: {len(devolvidos):,} pedidos ({len(devolvidos)/total_pedidos*100:.2f}% da base)")
    print(f"Receita Bruta Devolvida: R$ {devolvidos['receita_bruta'].sum():,.2f}")
    print(f"Margem Bruta Comprometida: R$ {devolvidos['margem_contribuicao'].sum():,.2f}")
    print("Motivos de Devolução:")
    for motivo, cnt in devolvidos['motivo_devolucao'].value_counts().items():
        print(f"  - {motivo}: {cnt:,} ({cnt/len(devolvidos)*100:.1f}%)")
        
    # 3. Resumo de Estoque
    print("\n--- 2. INDICADORES DE ESTOQUE & GIRO ---")
    est['valor_custo'] = est['estoque_fisico'] * est['custo_unitario']
    est['valor_venda'] = est['estoque_fisico'] * est['preco_venda_sugerido']
    
    total_pecas_est = est['estoque_fisico'].sum()
    total_valor_custo_est = est['valor_custo'].sum()
    total_valor_venda_est = est['valor_venda'].sum()
    
    print(f"SKUs Cadastrados: {len(est):,}")
    print(f"Peças Físicas em Estoque: {total_pecas_est:,}")
    print(f"Valor do Estoque a Custo: R$ {total_valor_custo_est:,.2f}")
    print(f"Valor do Estoque a Preço de Venda: R$ {total_valor_venda_est:,.2f}")
    print(f"Relação Estoque a Custo / CMV Anual de Vendas: {total_valor_custo_est / cmv_total:.1f}x")
    
    # 4. Atendimento
    print("\n--- 3. INDICADORES DE ATENDIMENTO ---")
    total_tkt = len(atend)
    custo_tkt = atend['custo_operacional_ticket'].sum()
    print(f"Total de Tickets: {total_tkt:,}")
    print(f"Custo Operacional Total de Atendimento: R$ {custo_tkt:,.2f}")
    print("Principais Demandas de Clientes:")
    for cat, cnt in atend['categoria_problema'].value_counts().items():
        print(f"  - {cat}: {cnt:,} ({cnt/total_tkt*100:.1f}%)")
        
    # 5. Geração de Gráficos
    print("\n--- 4. GERANDO VISUALIZAÇÕES E GRÁFICOS ---")
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    # Gráfico 1: Estoque vs Vendas por Categoria
    v_cat = vendas.groupby('categoria')['quantidade'].sum()
    e_cat = est.groupby('categoria')['estoque_fisico'].sum()
    cat_df = pd.DataFrame({'Vendas (13m)': v_cat, 'Estoque Fisico': e_cat}).fillna(0)
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = np.arange(len(cat_df))
    width = 0.35
    ax1.bar(x - width/2, cat_df['Vendas (13m)'], width, label='Peças Vendidas (13 meses)', color='#3947f3')
    rects = ax1.bar(x + width/2, cat_df['Estoque Fisico'], width, label='Estoque Físico Atual', color='#ef4444')
    ax1.set_ylabel('Quantidade de Peças')
    ax1.set_title('Desproporção de Estoque Físico vs. Vendas por Categoria', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(cat_df.index, fontsize=10)
    ax1.legend(loc='upper left')
    for r in rects:
        h = r.get_height()
        ax1.annotate(f'{int(h):,}', xy=(r.get_x() + r.get_width()/2, h),
                     xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'chart_estoque_vs_vendas.png'), dpi=300)
    plt.close()
    
    # Gráfico 2: Motivos de Devolução
    motivos = devolvidos['motivo_devolucao'].value_counts()
    fig, ax = plt.subplots(figsize=(9, 5))
    motivos.plot(kind='barh', color='#8575ff', ax=ax)
    ax.set_title('Distribuição de Motivos de Devolução (Total: 4.127 pedidos)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Quantidade de Pedidos Devolvidos')
    for i, v in enumerate(motivos):
        ax.text(v + 15, i, f'{v} ({v/len(devolvidos)*100:.1f}%)', va='center', fontweight='bold', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'chart_motivos_devolucao.png'), dpi=300)
    plt.close()
    
    # Gráfico 3: Atendimento Pareto
    tkt_cat = atend['categoria_problema'].value_counts(dropna=False).dropna()
    fig, ax = plt.subplots(figsize=(9, 5))
    tkt_cat.plot(kind='barh', color='#4200db', ax=ax)
    ax.set_title('Chamados de Atendimento por Categoria (35.841 tickets)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Volume de Tickets')
    for i, v in enumerate(tkt_cat):
        ax.text(v + 100, i, f'{v:,} ({v/len(atend)*100:.1f}%)', va='center', fontweight='bold', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'chart_atendimento_tickets.png'), dpi=300)
    plt.close()
    
    # Gráfico 4: Margem vs Desconto por Canal
    c_stats = vendas.groupby('canal').agg(
        rec_liq=('receita_liquida', 'sum'),
        margem=('margem_contribuicao', 'sum'),
        desc=('desconto_reais', 'sum'),
        rec_bruta=('receita_bruta', 'sum')
    )
    c_stats['margem_pct'] = c_stats['margem'] / c_stats['rec_liq'] * 100
    c_stats['desc_pct'] = c_stats['desc'] / c_stats['rec_bruta'] * 100
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(c_stats))
    ax.bar(x - width/2, c_stats['margem_pct'], width, label='Margem Contribuição (%)', color='#10b981')
    ax.bar(x + width/2, c_stats['desc_pct'], width, label='Desconto Médio (%)', color='#f59e0b')
    ax.set_ylabel('Percentual (%)')
    ax.set_title('Margem de Contribuição vs. Desconto Concedido por Canal', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(c_stats.index, rotation=20, ha='right', fontsize=10)
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'chart_margem_desconto_canal.png'), dpi=300)
    plt.close()
    
    print("Gráficos salvos com sucesso em 'charts/'!")
    print("=" * 70)
    print(" PIPELINE CONCLUÍDO COM SUCESSO ")
    print("=" * 70)

if __name__ == '__main__':
    main()
