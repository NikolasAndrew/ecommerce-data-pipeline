from src.utils.logger import setup_logger
from config.settings import DATABASE_URL
from src.utils.exceptions import PipelineError
from src.utils.exceptions import DataExtractionError
from sqlalchemy import create_engine
import pandas as pd


logging = setup_logger("extract")

engine = create_engine(DATABASE_URL)

import pandas as pd

def extrair_dados_oltp() -> tuple[
    pd.DataFrame | None,
    pd.DataFrame | None,
    pd.DataFrame | None,
    pd.DataFrame | None
]:

    logging.info("Iniciando extração dos dados...")

    df_clientes = pd.read_sql("SELECT * FROM dbo.clientes", engine)
    logging.info(f"Tabela de clientes extraida com sucesso, trazendo um total de {len(df_clientes)}")

    df_pedidos = pd.read_sql("SELECT * FROM dbo.pedidos", engine)
    logging.info(f"Tabela de pedidos extraida com sucesso, trazendo um total de {len(df_pedidos)}")

    df_itenspedido = pd.read_sql("SELECT * FROM dbo.itens_pedido", engine)
    logging.info(f"Tabela de itens_pedido extraida com sucesso, trazendo um total de {len(df_itenspedido)}")

    df_produtos = pd.read_sql("SELECT * FROM dbo.produtos", engine)
    logging.info(f"Tabela de produtos extraida com sucesso, trazendo um total de {len(df_produtos)}")

    return df_clientes, df_pedidos, df_itenspedido, df_produtos

