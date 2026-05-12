class PipelineError(Exception):
    """
    Exceção base para erros do pipeline.
    """
    pass


class DataExtractionError(PipelineError):
    """
    Erro na etapa de extração.
    """
    pass


class DataValidationError(PipelineError):
    """
    Erro na etapa de validação.
    """
    pass


class DataTransformationError(PipelineError):
    """
    Erro na etapa de transformação.
    """
    pass


class DWHError(PipelineError):
    """
    Erro na etapa de modelagem do Data Warehouse.
    """
    pass