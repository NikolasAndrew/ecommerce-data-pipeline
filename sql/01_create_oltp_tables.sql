CREATE TABLE clientes (
    cliente_id BIGINT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(150),
    cidade VARCHAR(100),
    data_cadastro DATE,
    ativo BIT
);

CREATE TABLE produtos (
    produto_id BIGINT PRIMARY KEY,
    nome VARCHAR(100),
    categoria VARCHAR(100),
    preco DECIMAL(10,2),
    estoque BIGINT
);

CREATE TABLE pedidos (
    pedido_id BIGINT PRIMARY KEY,
    cliente_id BIGINT,
    data_pedido DATE,
    status VARCHAR(50),

    FOREIGN KEY (cliente_id)
        REFERENCES clientes(cliente_id)
);

CREATE TABLE itens_pedido (
    item_id BIGINT PRIMARY KEY,
    pedido_id BIGINT,
    produto_id BIGINT,
    quantidade BIGINT,
    preco_unitario DECIMAL(10,2),

    FOREIGN KEY (pedido_id)
        REFERENCES pedidos(pedido_id),

    FOREIGN KEY (produto_id)
        REFERENCES produtos(produto_id)
);