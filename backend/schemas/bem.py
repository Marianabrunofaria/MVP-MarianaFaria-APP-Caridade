from pydantic import BaseModel
from typing import Optional, List
from model.bem import Bem



class BemSchema(BaseModel):
    """ Define como um novo bem a ser inserido deve ser representado
    """
    nome: str = "Camisa Polo"
    quantidade: Optional[int] = 1



class BemBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do bem.
    """
    nome: str = "Teste"


class ListagemBemsSchema(BaseModel):
    """ Define como uma listagem de bens será retornada.
    """
    bems:List[BemSchema]


def apresenta_bems(bems: List[Bem]):
    """ Retorna uma representação do bem seguindo o schema definido em
        BemViewSchema.
    """
    result = []
    for bem in bems:
        result.append({
            "nome": bem.nome,
            "quantidade": bem.quantidade
            
        })

    return {"bems": result}


class BemViewSchema(BaseModel):
    """ Define como um bem será retornado: bem .
    """
    id: int = 1
    nome: str = "Camisa Polo"
    quantidade: Optional[int] = 1
    


class BemDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_bem(bem: Bem):
    """ Retorna uma representação do bem seguindo o schema definido em
        BemViewSchema.
    """
    return {
        "id": bem.id,
        "nome": bem.nome,
        "quantidade": bem.quantidade
       
    }