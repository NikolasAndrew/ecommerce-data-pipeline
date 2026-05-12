# E-Commerce Data Pipeline

## 📋 Descrição do Projeto

Pipeline ETL profissional desenvolvido para processamento e análise de dados de e-commerce utilizando Apache Spark e Python.

O pipeline realiza:

- Extração de dados de sistema OLTP
- Validação e tratamento de qualidade dos dados
- Transformação e modelagem dimensional
- Construção de Data Warehouse em Star Schema
- Geração de análises e métricas de vendas

---

# 🎯 Objetivos de Negócio

- Consolidar dados de múltiplas fontes
- Gerar insights de vendas por categoria
- Identificar clientes com maior valor de compra
- Monitorar qualidade e integridade dos dados
- Estruturar ambiente analítico escalável

---

# 🏗️ Arquitetura

```text
OLTP Database
      ↓
Extraction Layer
      ↓
Validation & Cleaning
      ↓
Transformation Layer
      ↓
Star Schema Data Warehouse
      ↓
Analytics & Insights
```

---

# 📊 Dados Processados

O pipeline processa dados relacionados a:

- Clientes
- Pedidos
- Itens de pedidos
- Produtos
- Categorias
- Status de vendas

Estrutura dimensional criada:

- DIM_CLIENTE
- DIM_PRODUTO
- DIM_TEMPO
- DIM_STATUS
- FATO_VENDAS

---

# 🚀 Como Usar

## 1. Clonar repositório

```bash
git clone https://github.com/NikolasAndrew/ecommerce-data-pipeline.git
```

---

## 2. Entrar na pasta

```bash
cd ecommerce-data-pipeline
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configurar banco de dados

Execute os scripts SQL da pasta:

```text
sql/
```

Ordem recomendada:

```text
01_create_oltp_tables.sql
03_create_staging.sql
04_create_dw.sql
```

---

## 5. Executar pipeline

```bash
py -3.11 -m src.main
```

---

# 📈 Resultados

O pipeline gera análises como:

- Vendas por categoria
- Top clientes por faturamento
- Produtos mais vendidos
- Ranking de produtos por categoria
- Evolução de vendas dos clientes
- Métricas de lucro e receita

Também realiza:

- Tratamento de valores nulos
- Padronização de dados
- Criação de surrogate keys
- Aplicação de Window Functions
- Modelagem Star Schema

---

# 🔧 Tecnologias

- Apache Spark
- PySpark
- Python 3.11
- SQL Server
- SQLAlchemy
- PyODBC
- Pandas
- Git & GitHub

---

# 📂 Estrutura do Projeto

```text
config/
docs/
sql/
src/
tests/
requirements.txt
README.md
```

---

# 📧 Contato

Nikolas Andrew  
📩 nikolasandrew2021@gmail.com