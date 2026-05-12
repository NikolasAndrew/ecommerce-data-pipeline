# Como Contribuir

Obrigado por contribuir com este projeto de Engenharia de Dados 🚀

Este documento descreve como configurar o ambiente local, seguir os padrões do projeto e executar os testes.

---

# Setup Local

## 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/pipeline-ecommerce.git
cd pipeline-ecommerce
```

---

## 2. Criar ambiente virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variáveis de ambiente

Criar arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=seu_database_url
```

---

## 5. Executar scripts SQL

Executar os scripts da pasta `sql/` na seguinte ordem:

```text
01_create_oltp_tables.sql
02_insert_mock_data.sql
03_create_staging.sql
04_create_dw.sql
```

---

# Estrutura do Projeto

```text
project/
│
├── config/
├── docs/
├── sql/
├── src/
│   ├── extraction/
│   ├── transform/
│   ├── load/
│   ├── analytics/
│   └── utils/
│
├── tests/
├── requirements.txt
└── README.md
```

---

# Padrões de Código

## Type Hints Obrigatórios

Todas as funções devem utilizar type hints.

Exemplo:

```python
def calcular_total(valor: float, quantidade: int) -> float:
    return valor * quantidade
```

---

## Docstrings

Toda função deve possuir docstring.

Exemplo:

```python
def carregar_dados() -> None:
    """
    Realiza carregamento de dados no Data Warehouse.
    """
```

---

## Logging

Utilizar logging nos pontos críticos:

- início de processos
- erros
- validações
- carregamentos
- transformações

Exemplo:

```python
logging.info("Iniciando transformação")
```

---

## Tratamento de Exceções

Utilizar try/except em operações críticas.

Exemplo:

```python
try:
    processar_dados()
except Exception as e:
    logging.error(f"Erro no processamento: {e}")
```

---

# Como Rodar o Projeto

## Executar pipeline principal

```bash
py -3.11 -m src.main
```

ou

```bash
python src/main.py
```

---

# Como Rodar os Testes

```bash
pytest tests/
```

---

# Tecnologias Utilizadas

- Python 3.11
- PySpark
- SQL Server
- SQLAlchemy
- PyODBC
- Pandas
- Pytest

---

# Convenções

## Nome de arquivos

Utilizar:

```text
snake_case.py
```

---

## Nome de variáveis

Utilizar:

```python
nome_cliente
valor_total
data_processamento
```

---

## Nome de tabelas DW

Utilizar:

```text
DIM_CLIENTE
DIM_PRODUTO
FATO_VENDAS
```

---

# Boas Práticas

- Evitar código duplicado
- Criar funções reutilizáveis
- Manter separação por camadas
- Validar dados antes do load
- Utilizar joins otimizados
- Evitar select *

---

# Fluxo de Contribuição

1. Criar branch feature
2. Desenvolver alteração
3. Executar testes
4. Abrir Pull Request
5. Revisão de código

---

# Contato

Projeto desenvolvido para fins de estudo e portfólio em Engenharia de Dados.