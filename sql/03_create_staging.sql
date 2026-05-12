CREATE TABLE staging_clientes (
    cliente_id BIGINT,
    nome VARCHAR(100),
    email VARCHAR(150),
    cidade VARCHAR(100),
    data_cadastro DATE,
    ativo BIT,

    data_processamento DATETIME,
    flag_erro BIT,
    motivo_erro VARCHAR(255)
);

CREATE TABLE staging_pedidos (
    pedido_id BIGINT,
    cliente_id BIGINT,
    data_pedido DATE,
    status VARCHAR(50),

    data_processamento DATETIME,
    flag_erro BIT,
    motivo_erro VARCHAR(255)
);

CREATE TABLE staging_itens (
    item_id BIGINT,
    pedido_id BIGINT,
    produto_id BIGINT,
    quantidade BIGINT,
    preco_unitario DECIMAL(10,2),

    data_processamento DATETIME,
    flag_erro BIT,
    motivo_erro VARCHAR(255)
);

CREATE TABLE staging_produtos (
    produto_id BIGINT,
    nome VARCHAR(100),
    categoria VARCHAR(100),
    preco DECIMAL(10,2),
    estoque BIGINT,

    data_processamento DATETIME,
    flag_erro BIT,
    motivo_erro VARCHAR(255)
);