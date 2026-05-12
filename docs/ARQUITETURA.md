# Arquitetura do Projeto

## Visão Geral

Este projeto implementa um pipeline ETL utilizando:

- Python
- PySpark
- SQL Server
- Star Schema
- Data Warehouse
- Camada Staging

O objetivo é extrair dados do ambiente OLTP, transformá-los utilizando regras de negócio e carregá-los em um Data Warehouse analítico.

---

# Fluxo da Arquitetura

```text
             +------------------+
             |   Banco OLTP     |
             | SQL Server       |
             +------------------+
                      |
                      v
             +------------------+
             |    Extraction    |
             | SQLAlchemy       |
             +------------------+
                      |
                      v
             +------------------+
             |     Staging      |
             | Validação Dados  |
             +------------------+
                      |
                      v
             +------------------+
             |   Transformação  |
             |     PySpark      |
             +------------------+
                      |
                      v
             +------------------+
             | Data Warehouse   |
             |  Star Schema     |
             +------------------+
                      |
                      v
             +------------------+
             | Analytics Layer  |
             +------------------+
Fases do Pipeline
1. Extraction

Responsável pela leitura dos dados do banco OLTP utilizando SQLAlchemy e PyODBC.

Tabelas extraídas:

clientes
pedidos
itens_pedido
produtos
2. Staging

Camada intermediária para:

validação
limpeza
auditoria
tratamento de erros

Campos adicionais:

data_processamento
flag_erro
motivo_erro
3. Transformation

Transformações realizadas com PySpark:

joins
limpeza de nulos
cálculo de métricas
criação de surrogate keys
enriquecimento dimensional
4. Data Warehouse

Modelagem Star Schema composta por:

Dimensões:

DIM_CLIENTE
DIM_PRODUTO
DIM_TEMPO
DIM_STATUS

Fato:

FATO_VENDAS
Decisões de Design
Por que Star Schema?

Foi escolhido Star Schema por:

simplicidade analítica
melhor performance para BI
facilidade em agregações
compatibilidade com ferramentas analíticas
redução da complexidade de joins
Problemas Encontrados e Soluções
Problema 1 — Python 3.12 incompatível com Spark

Solução:

downgrade para Python 3.11
Problema 2 — Incompatibilidade Java

Solução:

utilização do Java 17
Problema 3 — Colunas duplicadas em joins

Solução:

renomeação de colunas:
nome_cliente
nome_produto
preco_produto
Problema 4 — Distutils removido no Python 3.12

Solução:

migração para Python 3.11
Performance Considerations
Estratégias utilizadas
utilização de Spark DataFrames
processamento distribuído
filtros antes de joins
uso de surrogate keys
separação OLTP x DW
agregações otimizadas
Melhorias futuras
particionamento
cache persistente
Delta Lake
orquestração com Airflow
processamento incremental

---

# 1️⃣4️⃣ docs/DATA_DICTIONARY.md

```markdown
# Dicionário de Dados

# Tabela: clientes

| Coluna | Tipo | Descrição | Exemplo |
|---|---|---|---|
| cliente_id | BIGINT | Identificador do cliente | 1 |
| nome | VARCHAR(100) | Nome do cliente | João Silva |
| email | VARCHAR(150) | Email do cliente | joao@email.com |
| cidade | VARCHAR(100) | Cidade do cliente | São Paulo |
| data_cadastro | DATE | Data cadastro | 2024-01-01 |
| ativo | BIT | Cliente ativo | 1 |

---

# Tabela: produtos

| Coluna | Tipo | Descrição | Exemplo |
|---|---|---|---|
| produto_id | BIGINT | ID produto | 10 |
| nome | VARCHAR(100) | Nome produto | Notebook |
| categoria | VARCHAR(100) | Categoria produto | Eletrônicos |
| preco | DECIMAL(10,2) | Preço produto | 3500.00 |
| estoque | BIGINT | Quantidade estoque | 50 |

---

# Tabela: pedidos

| Coluna | Tipo | Descrição | Exemplo |
|---|---|---|---|
| pedido_id | BIGINT | ID pedido | 100 |
| cliente_id | BIGINT | Cliente relacionado | 1 |
| data_pedido | DATE | Data pedido | 2025-01-01 |
| status | VARCHAR(50) | Status pedido | ENTREGUE |

---

# Tabela: itens_pedido

| Coluna | Tipo | Descrição | Exemplo |
|---|---|---|---|
| item_id | BIGINT | ID item | 1000 |
| pedido_id | BIGINT | Pedido relacionado | 100 |
| produto_id | BIGINT | Produto relacionado | 10 |
| quantidade | BIGINT | Quantidade vendida | 2 |
| preco_unitario | DECIMAL(10,2) | Preço unitário | 3500.00 |

---

# Data Warehouse

# DIM_CLIENTE

| Coluna | Tipo |
|---|---|
| cliente_sk | INT |
| cliente_id | BIGINT |
| nome_cliente | VARCHAR(100) |
| email | VARCHAR(150) |
| cidade | VARCHAR(100) |

---

# DIM_PRODUTO

| Coluna | Tipo |
|---|---|
| produto_sk | INT |
| produto_id | BIGINT |
| nome_produto | VARCHAR(100) |
| categoria | VARCHAR(100) |
| preco_produto | DECIMAL(10,2) |

---

# DIM_TEMPO

| Coluna | Tipo |
|---|---|
| data_sk | INT |
| data_completa | DATE |
| ano | INT |
| mes | INT |
| dia | INT |
| trimestre | INT |

---

# DIM_STATUS

| Coluna | Tipo |
|---|---|
| status_sk | INT |
| status | VARCHAR(50) |
| descricao | VARCHAR(150) |

---

# FATO_VENDAS

| Coluna | Tipo |
|---|---|
| venda_sk | INT |
| cliente_sk | INT |
| produto_sk | INT |
| data_sk | INT |
| status_sk | INT |
| quantidade | BIGINT |
| valor_total | DECIMAL(10,2) |
| lucro | DECIMAL(10,2) |