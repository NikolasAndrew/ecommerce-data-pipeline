from src.utils.logger import setup_logger
from src.extraction.extract import extrair_dados_oltp
from src.validation.quality import validar_dados_oltp
from src.transformation.transform import transformar_com_spark
from src.modeling.dwh import criar_star_schema
from src.analytics.analytics import executar_analytics

logging = setup_logger("main")


def main():

    try:

        # =========================
        # EXTRAÇÃO
        # =========================
        logging.info("Extraindo dados...")

        df_clientes, df_pedidos, df_itenspedido, df_produtos = extrair_dados_oltp()

        if (
            df_clientes is None or
            df_pedidos is None or
            df_itenspedido is None or
            df_produtos is None
        ):

            logging.error("Erro ao extrair os dados")
            return

        logging.info("Extração concluída com sucesso")

        # =========================
        # VALIDAÇÃO
        # =========================
        logging.info("Validando dados...")

        resultado_validacao = validar_dados_oltp(
            df_clientes,
            df_pedidos,
            df_itenspedido,
            df_produtos
        )

        # verifica se existe alguma validação falsa
        if not all(resultado_validacao.values()):

            logging.error("Falha na validação dos dados")
            return

        logging.info("Dados validados com sucesso")

        # =========================
        # TRANSFORMAÇÃO
        # =========================
        logging.info("Transformando os dados...")

        df_vendas = transformar_com_spark(
            df_clientes,
            df_pedidos,
            df_itenspedido,
            df_produtos
        )

        if df_vendas is None:

            logging.error("Erro ao transformar os dados")
            return

        logging.info("Dados transformados com sucesso")

        # =========================
        # MODELAGEM DWH
        # =========================
        logging.info("Criando Star Schema...")

        dim_clientes, dim_produtos, dim_tempo, dim_status, fato_vendas = criar_star_schema(df_vendas)

        logging.info("Star Schema criado com sucesso")

        # =========================
        # ANALYTICS
        # =========================
        logging.info("Executando análises...")

        resultados = executar_analytics(
            fato_vendas,
            dim_clientes,
            dim_produtos
        )

        # =========================
        # EXIBIÇÃO DOS RESULTADOS
        # =========================
        logging.info("Exibindo resultados...")

        resultados["vendas_por_categoria"].show()

        resultados["top_clientes"].show()

        resultados["top_produtos"].show()

        resultados["ranking_categoria"].show()

        resultados["evolucao_clientes"].show()

        # =========================
        # FINALIZAÇÃO
        # =========================
        logging.info("PIPELINE CONCLUÍDO COM SUCESSO")

    except Exception as e:

        logging.error(f"Erro no pipeline: {e}")


if __name__ == "__main__":

    main()