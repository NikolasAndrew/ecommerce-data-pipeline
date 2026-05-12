CREATE TABLE DIM_CLIENTE (
    cliente_sk INT PRIMARY KEY,
    cliente_id BIGINT,
    nome_cliente VARCHAR(100),
    email VARCHAR(150),
    cidade VARCHAR(100),
    data_inicio DATE,
    data_fim DATE,
    flag_ativo BIT
);

CREATE TABLE DIM_PRODUTO (
    produto_sk INT PRIMARY KEY,
    produto_id BIGINT,
    nome_produto VARCHAR(100),
    categoria VARCHAR(100),
    preco_produto DECIMAL(10,2),
    data_inicio DATE,
    data_fim DATE,
    flag_ativo BIT
);

CREATE TABLE DIM_TEMPO (
    data_sk INT PRIMARY KEY,
    data_completa DATE,
    ano INT,
    mes INT,
    dia INT,
    trimestre INT,
    semana INT,
    eh_feriado BIT
);

CREATE TABLE DIM_STATUS (
    status_sk INT PRIMARY KEY,
    status VARCHAR(50),
    descricao VARCHAR(150)
);

CREATE TABLE FATO_VENDAS (
    venda_sk INT PRIMARY KEY,

    cliente_sk INT,
    produto_sk INT,
    data_sk INT,
    status_sk INT,

    pedido_id BIGINT,
    item_id BIGINT,

    quantidade BIGINT,
    valor_total DECIMAL(10,2),
    lucro DECIMAL(10,2),

    data_processamento DATE,

    FOREIGN KEY (cliente_sk)
        REFERENCES DIM_CLIENTE(cliente_sk),

    FOREIGN KEY (produto_sk)
        REFERENCES DIM_PRODUTO(produto_sk),

    FOREIGN KEY (data_sk)
        REFERENCES DIM_TEMPO(data_sk),

    FOREIGN KEY (status_sk)
        REFERENCES DIM_STATUS(status_sk)
);

CREATE INDEX idx_fato_cliente
ON FATO_VENDAS(cliente_sk);

CREATE INDEX idx_fato_produto
ON FATO_VENDAS(produto_sk);

CREATE INDEX idx_fato_data
ON FATO_VENDAS(data_sk);

CREATE INDEX idx_fato_status
ON FATO_VENDAS(status_sk);