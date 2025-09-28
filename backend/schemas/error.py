from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Erro de base de dados
    """
    mesage: str