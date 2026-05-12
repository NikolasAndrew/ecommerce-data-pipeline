from typing import Tuple
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import (
    row_number, col, lit, current_date, year, month,
    dayofmonth, quarter, weekofyear, when, date_format, to_date
)
from src.utils.logger import setup_logger

logging = setup_logger("dwh")


spark = SparkSession.builder.appName("Schema").getOrCreate()


# =========================
# DIM CLIENTE
# =========================
def criar_dim_cliente(df: DataFrame) -> DataFrame:
    logging.info("Criando DIM_CLIENTE")

    df_dim = (
        df
        .select("cliente_id", "nome_cliente", "email", "cidade")
        .dropDuplicates(["cliente_id"])
    )

    df_dim = df_dim.withColumn(
        "cliente_sk",
        row_number().over(Window.orderBy("cliente_id"))
    )

    df_dim = (
        df_dim
        .withColumn("ativo", lit(1))
        .withColumn("data_inicio", current_date())
        .withColumn("data_fim", to_date(lit("2999-12-31")))
        .withColumn("flag_ativo", lit(1))
    )

    logging.info(f"DIM_CLIENTE criada com {df_dim.count()} registros")
    return df_dim


# =========================
# DIM PRODUTO
# =========================
def criar_dim_produto(df: DataFrame) -> DataFrame:
    logging.info("Criando DIM_PRODUTO")

    df_dim = (
        df
        .select("produto_id", "nome_produto", "categoria", "preco_produto")
        .dropDuplicates(["produto_id"])
    )

    df_dim = df_dim.withColumn(
        "produto_sk",
        row_number().over(Window.orderBy("produto_id"))
    )

    df_dim = (
        df_dim
        .withColumn("data_inicio", current_date())
        .withColumn("data_fim", to_date(lit("2999-12-31")))
        .withColumn("flag_ativo", lit(1))
    )

    logging.info(f"DIM_PRODUTO criada com {df_dim.count()} registros")
    return df_dim


# =========================
# DIM TEMPO
# =========================
def criar_dim_tempo(df: DataFrame) -> DataFrame:
    logging.info("Criando DIM_TEMPO")

    df_dim = (
        df
        .select("data_pedido")
        .dropDuplicates()
    )

    df_dim = df_dim.select(
        date_format(col("data_pedido"), "yyyyMMdd").cast("int").alias("data_sk"),
        col("data_pedido").alias("data_completa"),
        year("data_pedido").alias("ano"),
        month("data_pedido").alias("mes"),
        dayofmonth("data_pedido").alias("dia"),
        quarter("data_pedido").alias("trimestre"),
        weekofyear("data_pedido").alias("semana"),
        when(
            date_format(col("data_pedido"), "MM-dd").isin("01-01", "12-25"),
            lit(1)
        ).otherwise(lit(0)).alias("eh_feriado")
    )

    logging.info(f"DIM_TEMPO criada com {df_dim.count()} registros")
    return df_dim


# =========================
# DIM STATUS
# =========================
def criar_dim_status(df: DataFrame) -> DataFrame:
    logging.info("Criando DIM_STATUS")

    df_dim = (
        df
        .select("status")
        .dropDuplicates()
    )

    df_dim = df_dim.withColumn(
        "status_sk",
        row_number().over(Window.orderBy("status"))
    )

    df_dim = df_dim.withColumn(
        "descricao",
        when(col("status") == "ENTREGUE", "Pedido concluído")
        .when(col("status") == "PENDENTE", "Aguardando processamento")
        .otherwise("Pedido cancelado pelo cliente")
    )

    logging.info(f"DIM_STATUS criada com {df_dim.count()} registros")
    return df_dim


# =========================
# FATO VENDAS
# =========================
def criar_fato_vendas(
    df: DataFrame,
    dim_clientes: DataFrame,
    dim_produtos: DataFrame,
    dim_tempo: DataFrame,
    dim_status: DataFrame
) -> DataFrame:

    logging.info("Criando FATO_VENDAS")

    ft = df \
        .join(dim_clientes, "cliente_id", "left") \
        .join(dim_produtos, "produto_id", "left") \
        .join(dim_tempo, col("data_pedido") == col("data_completa"), "left") \
        .join(dim_status, "status", "left")

    fato = ft.select(
        row_number().over(Window.orderBy("item_id")).alias("venda_sk"),
        col("cliente_sk"),
        col("produto_sk"),
        col("data_sk"),
        col("status_sk"),
        col("pedido_id"),
        col("item_id"),
        col("quantidade"),
        col("valor_total"),
        col("lucro")
    )

    fato = fato.withColumn("data_processamento", current_date())

    logging.info(f"FATO_VENDAS criada com {fato.count()} registros")
    return fato


# =========================
# ORQUESTRADOR
# =========================
def criar_star_schema(df_vendas: DataFrame) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]:

    logging.info("Iniciando criação do Star Schema")

    dim_clientes = criar_dim_cliente(df_vendas)
    dim_produtos = criar_dim_produto(df_vendas)
    dim_tempo = criar_dim_tempo(df_vendas)
    dim_status = criar_dim_status(df_vendas)

    fato_vendas = criar_fato_vendas(
        df_vendas,
        dim_clientes,
        dim_produtos,
        dim_tempo,
        dim_status
    )

    logging.info("Star Schema criado com sucesso")

    return dim_clientes, dim_produtos, dim_tempo, dim_status, fato_vendas