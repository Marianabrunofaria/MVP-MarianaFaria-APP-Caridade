from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Bem
from logger import logger
from schemas import *
from flask_cors import CORS
import warnings
from flask import Flask

# Suprime todos os avisos
warnings.filterwarnings('ignore')

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
bem_tag = Tag(name="Bem", description="Adição, visualização e remoção de bems à base")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/bem', tags=[bem_tag],
          responses={"200": BemViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_bem(form: BemSchema):
    """Adiciona um novo Bem à base de dados

    Retorna uma representação dos bems 
    """
    bem = Bem(
        nome=form.nome,
        quantidade=form.quantidade)
    logger.debug(f"Adicionando bem de nome: '{bem.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando bem
        session.add(bem)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado bem de nome: '{bem.nome}'")
        return apresenta_bem(bem), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Bem de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar bem '{bem.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar bem '{bem.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/bems', tags=[bem_tag],
         responses={"200": ListagemBemsSchema, "404": ErrorSchema})
def get_bems():
    """Faz a busca por todos os Bens cadastrados

    Retorna uma representação da listagem de bens.
    """
    logger.debug(f"Coletando bens")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    bems = session.query(Bem).all()

    if not bems:
        # se não há bems cadastrados
        return {"bems": []}, 200
    else:
        logger.debug(f"bens encontrados" % len(bems))
        # retorna a representação de bem
        print(bems)
        return apresenta_bems(bems), 200


@app.get('/bem', tags=[bem_tag],
         responses={"200": BemViewSchema, "404": ErrorSchema})
def get_bem(query: BemBuscaSchema):
    """Faz a busca por um Bem a partir do id do bem

    Retorna uma representação dos bens.
    """
    bem_nome = query.nome
    logger.debug(f"Coletando dados sobre bem #{bem_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    bem = session.query(Bem).filter(Bem.nome == bem_nome).first()

    if not bem:
        # se o bem não foi encontrado
        error_msg = "Bem não encontrado na base :/"
        logger.warning(f"Erro ao buscar bem '{bem_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Bem encontrado: '{bem.nome}'")
        # retorna a representação de bem
        return apresenta_bem(bem), 200


@app.delete('/bem', tags=[bem_tag],
            responses={"200": BemDelSchema, "404": ErrorSchema})
def del_bem(query: BemBuscaSchema):
    """Deleta um Bem a partir do nome de bem informado

    Retorna uma mensagem de confirmação da remoção.
    """
    bem_nome = unquote(unquote(query.nome))
    print(bem_nome)
    logger.debug(f"Deletando dados sobre bem #{bem_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Bem).filter(Bem.nome == bem_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado bem #{bem_nome}")
        return {"mesage": "Bem removido", "id": bem_nome}
    else:
        # se o bem não foi encontrado
        error_msg = "Bem não encontrado na base :/"
        logger.warning(f"Erro ao deletar bem #'{bem_nome}', {error_msg}")
        return {"mesage": error_msg}, 404



   