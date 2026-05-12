from src.utils.logger import setup_logger
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
from typing import Optional
import os

logging = setup_logger("transform")

# =========================
# CONFIG PYSPARK
# =========================

os.environ["PYSPARK_PYTHON"] = r"C:\Users\nikol\AppData\Local\Programs\Python\Python311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\nikol\AppData\Local\Programs\Python\Python311\python.exe"

spark = (
    SparkSession.builder
    .appName("Transformar_Ecommerce")
    .master("local[*]")
    .config("spark.driver.memory", "2g")
    .config("spark.executor.memory", "2g")
    .getOrCreate()
)


def transformar_com_spark(
    df_clientes,
    df_pedidos,
    df_itens_pedido,
    df_produtos
) -> Optional[DataFrame]:

    try:

        logging.info("Convertendo DataFrames pandas para Spark...")

        # =========================
        # CONVERSÃO PARA SPARK
        # =========================

        df_clientes = spark.createDataFrame(df_clientes)
        df_pedidos = spark.createDataFrame(df_pedidos)
        df_itens_pedido = spark.createDataFrame(df_itens_pedido)
        df_produtos = spark.createDataFrame(df_produtos)

        logging.info("Criando views temporárias...")

        df_clientes.createOrReplaceTempView("clientes")
        df_pedidos.createOrReplaceTempView("pedidos")
        df_itens_pedido.createOrReplaceTempView("itens_pedido")
        df_produtos.createOrReplaceTempView("produtos")

        logging.info("Criando JOIN completo")

        # =========================
        # JOIN PRINCIPAL
        # =========================

        df_vendas = spark.sql("""

            SELECT
                c.cliente_id,
                c.nome AS nome_cliente,
                c.email,
                c.cidade,
                c.data_cadastro,
                c.ativo,

                p.pedido_id,
                p.data_pedido,
                MONTH(p.data_pedido) AS mes,
                YEAR(p.data_pedido) AS ano,
                p.status,

                i.item_id,
                i.produto_id,
                i.quantidade,
                i.preco_unitario,

                pro.nome AS nome_produto,
                pro.categoria,
                pro.preco AS preco_produto,
                pro.estoque,

                (i.quantidade * i.preco_unitario) AS valor_total,
                (i.quantidade * i.preco_unitario * 0.30) AS lucro

            FROM clientes c

            INNER JOIN pedidos p
                ON c.cliente_id = p.cliente_id

            INNER JOIN itens_pedido i
                ON p.pedido_id = i.pedido_id

            INNER JOIN produtos pro
                ON i.produto_id = pro.produto_id

        """)

        logging.info("Tratando dados")

        # =========================
        # FILTROS
        # =========================

        df_vendas = df_vendas.filter(
            f.col("quantidade").isNotNull()
        )

        df_vendas = df_vendas.filter(
            f.col("cliente_id").isNotNull()
        )

        df_vendas = df_vendas.fillna({
            "preco_produto": 0
        })

        logging.info("Transformação concluída")

        return df_vendas

    except Exception as e:

        logging.error(f"Erro na transformação: {e}")
        return None