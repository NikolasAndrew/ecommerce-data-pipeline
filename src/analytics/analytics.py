from typing import Dict
from pyspark.sql import SparkSession, DataFrame, Window
from pyspark.sql.functions import (
    sum,
    count,
    avg,
    row_number,
    desc,
    rank,
    lag
)

from src.utils.logger import setup_logger

logging = setup_logger("analytics")

spark = SparkSession.builder.appName("Analytics").getOrCreate()


# =========================
# FUNÇÃO 1
# =========================
def vendas_por_categoria(
    fato_vendas: DataFrame,
    dim_produtos: DataFrame
) -> DataFrame:

    logging.info("Executando análise: vendas_por_categoria")

    df = fato_vendas.join(
        dim_produtos,
        on="produto_sk",
        how="inner"
    )

    resultado = (
        df
        .groupBy("categoria")
        .agg(
            sum("valor_total").alias("soma_valor_total"),
            count("*").alias("quantidade_de_registros"),
            avg("preco_produto").alias("media_preco")
        )
        .orderBy(desc("soma_valor_total"))
    )

    logging.info("Análise vendas_por_categoria concluída")

    return resultado


# =========================
# FUNÇÃO 2
# =========================
def top_clientes(
    fato_vendas: DataFrame,
    dim_clientes: DataFrame
) -> DataFrame:

    logging.info("Executando análise: top_clientes")

    df = fato_vendas.join(
        dim_clientes,
        on="cliente_sk",
        how="inner"
    )

    df_agg = (
        df
        .groupBy("cliente_id", "nome_cliente")
        .agg(
            sum("valor_total").alias("total_gasto"),
            count("*").alias("qtd_itens")
        )
    )

    window_spec = Window.orderBy(desc("total_gasto"))

    df_rank = df_agg.withColumn(
        "ranking",
        row_number().over(window_spec)
    )

    resultado = df_rank.filter("ranking <= 10")

    logging.info("Análise top_clientes concluída")

    return resultado


# =========================
# FUNÇÃO 3
# =========================
def top_produtos(
    fato_vendas: DataFrame,
    dim_produtos: DataFrame
) -> DataFrame:

    logging.info("Executando análise: top_produtos")

    df = fato_vendas.join(
        dim_produtos,
        on="produto_sk",
        how="inner"
    )

    df_agg = (
        df
        .groupBy("produto_id", "categoria")
        .agg(
            sum("valor_total").alias("total_receita"),
            sum("quantidade").alias("quantidade_produtos")
        )
    )

    window_spec = Window.orderBy(desc("total_receita"))

    df_rank = df_agg.withColumn(
        "ranking",
        rank().over(window_spec)
    )

    resultado = df_rank.filter("ranking <= 10")

    logging.info("Análise top_produtos concluída")

    return resultado


# =========================
# FUNÇÃO 4
# =========================
def ranking_com_window(
    fato_vendas: DataFrame,
    dim_produtos: DataFrame
) -> DataFrame:

    logging.info("Executando análise: ranking_com_window")

    df = fato_vendas.join(
        dim_produtos,
        on="produto_sk",
        how="inner"
    )

    df_agg = (
        df
        .groupBy("categoria", "produto_id")
        .agg(
            sum("valor_total").alias("total_receita")
        )
    )

    window_spec = (
        Window
        .partitionBy("categoria")
        .orderBy(desc("total_receita"))
    )

    df_rank = df_agg.withColumn(
        "ranking",
        row_number().over(window_spec)
    )

    resultado = df_rank.filter("ranking <= 3")

    logging.info("Análise ranking_com_window concluída")

    return resultado


# =========================
# FUNÇÃO 5
# =========================
def evolucao_vendas_cliente(
    fato_vendas: DataFrame,
    dim_clientes: DataFrame
) -> DataFrame:

    logging.info("Executando análise: evolucao_vendas_cliente")

    df = fato_vendas.join(
        dim_clientes,
        on="cliente_sk",
        how="inner"
    )

    window_spec = (
        Window
        .partitionBy("cliente_id")
        .orderBy("data_sk")
    )

    df_lag = df.withColumn(
        "valor_anterior",
        lag("valor_total").over(window_spec)
    )

    resultado = df_lag.withColumn(
        "diferenca",
        df_lag["valor_total"] - df_lag["valor_anterior"]
    )

    logging.info("Análise evolucao_vendas_cliente concluída")

    return resultado


# =========================
# ORQUESTRADOR PRINCIPAL
# =========================
def executar_analytics(
    fato_vendas: DataFrame,
    dim_clientes: DataFrame,
    dim_produtos: DataFrame
) -> Dict[str, DataFrame]:

    logging.info("Iniciando execução das análises")

    resultado_vendas_categoria = vendas_por_categoria(
        fato_vendas,
        dim_produtos
    )

    resultado_top_clientes = top_clientes(
        fato_vendas,
        dim_clientes
    )

    resultado_top_produtos = top_produtos(
        fato_vendas,
        dim_produtos
    )

    resultado_ranking = ranking_com_window(
        fato_vendas,
        dim_produtos
    )

    resultado_evolucao = evolucao_vendas_cliente(
        fato_vendas,
        dim_clientes
    )

    logging.info("Todas as análises foram executadas com sucesso")

    return {
        "vendas_por_categoria": resultado_vendas_categoria,
        "top_clientes": resultado_top_clientes,
        "top_produtos": resultado_top_produtos,
        "ranking_categoria": resultado_ranking,
        "evolucao_clientes": resultado_evolucao
    }