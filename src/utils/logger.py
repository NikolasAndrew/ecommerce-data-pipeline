import logging
from config.settings import (
    LOG_FILE,
    LOG_LEVEL,
    LOG_FORMAT,
    LOG_DATE_FORMAT
)


def setup_logger(name: str = "pipeline") -> logging.Logger:
    """
    Cria e retorna um logger configurado para arquivo e console.

    Args:
        name (str): Nome do logger.

    Returns:
        logging.Logger: Logger configurado.
    """

    logger = logging.getLogger(name)

    # Evita adicionar handlers duplicados
    if logger.handlers:
        return logger

    # Define nível do logger
    logger.setLevel(LOG_LEVEL)

    # Handler para arquivo
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")

    # Handler para console
    console_handler = logging.StreamHandler()

    # Formato do log
    formatter = logging.Formatter(
        LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT
    )

    # Aplica formato
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Adiciona handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger