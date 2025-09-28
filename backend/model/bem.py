from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union



class Bem(Base):
    __tablename__ = 'bem'

    id = Column("pk_bem", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    quantidade = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, nome:str, quantidade:int, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Bem

        Arguments:
            nome: nome do bem.
            quantidade: quantidade que se espera doar daquele bem
            data_insercao: data de quando o bem foi inserido à base
        """
        self.nome = nome
        self.quantidade = quantidade
        

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
