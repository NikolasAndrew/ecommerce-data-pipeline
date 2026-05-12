from typing import Dict
import pandas as pd
from src.utils.logger import setup_logger

logging = setup_logger("quality")


def validar_dados_oltp(
    df_clientes,
    df_pedidos,
    df_itens_pedido,
    df_produtos
) -> Dict[str, bool]:

    logging.info("Iniciando validação dos dados...")

    # =========================
    # VALIDAÇÃO DE NULOS
    # =========================
    logging.info("Validando valores nulos...")

    clientes_nulos = df_clientes[['cliente_id', 'nome']].isna().any(axis=1)
    clientes_qtd_nulos = clientes_nulos.sum()
    logging.info(f'Clientes com nulos: {clientes_qtd_nulos}')

    pedidos_nulos = df_pedidos[['pedido_id', 'cliente_id']].isna().any(axis=1)
    pedidos_qtd_nulos = pedidos_nulos.sum()
    logging.info(f'Pedidos com nulos: {pedidos_qtd_nulos}')

    itens_pedido_nulos = df_itens_pedido[['item_id', 'pedido_id']].isna().any(axis=1)
    itens_qtd_nulos = itens_pedido_nulos.sum()
    logging.info(f'Itens pedido com nulos: {itens_qtd_nulos}')

    produtos_nulos = df_produtos[['produto_id']].isna().any(axis=1)
    produtos_qtd_nulos = produtos_nulos.sum()
    logging.info(f'Produtos com nulos: {produtos_qtd_nulos}')

    # =========================
    # VALORES FORA DO INTERVALO
    # =========================
    logging.info("Validando valores fora do intervalo...")

    itens_pedido_intervalo = df_itens_pedido['quantidade'] > 0
    itens_invalidos = (~itens_pedido_intervalo).sum()
    logging.info(f'Itens inválidos (quantidade <= 0): {itens_invalidos}')

    produtos_intervalo = (
        (df_produtos['preco'] > 0) &
        (df_produtos['estoque'] >= 0)
    )
    produtos_invalidos = (~produtos_intervalo).sum()
    logging.info(f'Produtos inválidos: {produtos_invalidos}')

    clientes_intervalo = df_clientes['ativo'].isin([0, 1])
    clientes_invalidos = (~clientes_intervalo).sum()
    logging.info(f'Clientes inválidos no campo ativo: {clientes_invalidos}')

    # =========================
    # INTEGRIDADE REFERENCIAL
    # =========================
    logging.info("Validando integridade referencial...")

    cliente_ref = df_pedidos['cliente_id'].isin(df_clientes['cliente_id'])
    cliente_ref_invalidos = (~cliente_ref).sum()
    logging.info(f'Pedidos com cliente inexistente: {cliente_ref_invalidos}')

    produto_ref = df_itens_pedido['produto_id'].isin(df_produtos['produto_id'])
    produto_ref_invalidos = (~produto_ref).sum()
    logging.info(f'Itens com produto inexistente: {produto_ref_invalidos}')

    pedido_ref = df_itens_pedido['pedido_id'].isin(df_pedidos['pedido_id'])
    pedido_ref_invalidos = (~pedido_ref).sum()
    logging.info(f'Itens com pedido inexistente: {pedido_ref_invalidos}')

    # =========================
    # OUTLIERS / VALORES SUSPEITOS
    # =========================
    logging.info("Validando outliers e valores suspeitos...")

    preco_outlier = df_produtos['preco'] > 100000
    preco_qtd_outlier = preco_outlier.sum()
    logging.info(f'Produtos com preço outlier: {preco_qtd_outlier}')

    quantidade_outlier = df_itens_pedido['quantidade'] > 1000
    quantidade_qtd_outlier = quantidade_outlier.sum()
    logging.info(f'Itens com quantidade outlier: {quantidade_qtd_outlier}')

    emails_invalidos = ~df_clientes['email'].str.contains('@', na=False)
    emails_qtd_invalidos = emails_invalidos.sum()
    logging.info(f'Emails inválidos: {emails_qtd_invalidos}')

    cidades_branco = (
        df_clientes['cidade'].isna() |
        (df_clientes['cidade'].str.strip() == '')
    )
    cidades_branco_qtd = cidades_branco.sum()
    logging.info(f'Cidades em branco: {cidades_branco_qtd}')

    # =========================
    # DUPLICATAS
    # =========================
    logging.info("Validando duplicatas...")

    cliente_duplicado = (
        df_clientes.duplicated(subset=['cliente_id'], keep=False) &
        ~df_clientes.duplicated(subset=['cliente_id', 'email'], keep=False)
    )

    cliente_duplicado_qtd = cliente_duplicado.sum()
    logging.info(f'Clientes duplicados inconsistentes: {cliente_duplicado_qtd}')

    pedido_duplicado = df_pedidos.duplicated(subset=['pedido_id'], keep=False)
    pedido_duplicado_qtd = pedido_duplicado.sum()
    logging.info(f'Pedidos duplicados: {pedido_duplicado_qtd}')

    # =========================
    # RESULTADO FINAL
    # =========================
    resultado_validacao = {
        "clientes_nulos": not clientes_nulos.any(),
        "pedidos_nulos": not pedidos_nulos.any(),
        "itens_pedido_nulos": not itens_pedido_nulos.any(),
        "produtos_nulos": not produtos_nulos.any(),

        "itens_pedido_intervalo": itens_pedido_intervalo.all(),
        "produtos_intervalo": produtos_intervalo.all(),
        "clientes_intervalo": clientes_intervalo.all(),

        "cliente_ref": cliente_ref.all(),
        "produto_ref": produto_ref.all(),
        "pedido_ref": pedido_ref.all(),

        "preco_outlier": not preco_outlier.any(),
        "quantidade_outlier": not quantidade_outlier.any(),
        "emails_invalidos": not emails_invalidos.any(),
        "cidades_branco": not cidades_branco.any(),

        "cliente_duplicado": not cliente_duplicado.any(),
        "pedido_duplicado": not pedido_duplicado.any()
    }

    logging.info("Resumo das validações:")

    for nome, status in resultado_validacao.items():

        if status:
            logging.info(f'{nome}: OK')
        else:
            logging.error(f'{nome}: FALHOU')

    return resultado_validacao