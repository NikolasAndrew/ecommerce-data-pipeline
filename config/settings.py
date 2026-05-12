from pathlib import Path
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

#Configurações de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = BASE_DIR / "logs" / "pipeline.log"


# Configurações de banco de dados
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mssql+pyodbc://@{DB_HOST}/{DB_NAME}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&Trusted_Connection=yes"
)

