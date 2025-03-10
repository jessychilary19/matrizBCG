from google.cloud import bigquery
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configurar o cliente do BigQuery
client = bigquery.Client()

# Consulta SQL para pegar os dados
query = """
    WITH bcg_data AS (
        SELECT 
            produto,
            SUM(faturamento) AS total_faturamento,
            (SUM(faturamento) * 100.0 / SUM(SUM(faturamento)) OVER ()) AS participacao_mercado,
            (SUM(faturamento) - LAG(SUM(faturamento)) OVER (PARTITION BY produto ORDER BY ano)) / LAG(SUM(faturamento)) OVER (PARTITION BY produto ORDER BY ano) * 100 AS taxa_crescimento
        FROM `seu_projeto.sua_dataset.vendas`
        WHERE ano BETWEEN EXTRACT(YEAR FROM CURRENT_DATE()) - 1 AND EXTRACT(YEAR FROM CURRENT_DATE())
        GROUP BY produto, ano
    )
    SELECT *,
        CASE 
            WHEN participacao_mercado >= 10 AND taxa_crescimento >= 10 THEN 'Estrela'
            WHEN participacao_mercado >= 10 AND taxa_crescimento < 10 THEN 'Vaca Leiteira'
            WHEN participacao_mercado < 10 AND taxa_crescimento >= 10 THEN 'Interrogação'
            ELSE 'Abacaxi'
        END AS categoria_bcg
    FROM bcg_data;
"""

# Executar a consulta
bcg_df = client.query(query).to_dataframe()

# Criar o gráfico da Matriz BCG
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=bcg_df,
    x="participacao_mercado",
    y="taxa_crescimento",
    size="total_faturamento",
    hue="categoria_bcg",
    sizes=(50, 1000),
    palette={"Estrela": "gold", "Vaca Leiteira": "green",
             "Interrogação": "blue", "Abacaxi": "red"}
)

# Linha horizontal para separar crescimento alto/baixo
plt.axhline(y=10, color='gray', linestyle='--')
# Linha vertical para separar alta/baixa participação
plt.axvline(x=10, color='gray', linestyle='--')
plt.xlabel("Participação de Mercado (%)")
plt.ylabel("Taxa de Crescimento (%)")
plt.title("Matriz BCG - BigQuery")
plt.legend(title="Categoria BCG")
plt.show()
