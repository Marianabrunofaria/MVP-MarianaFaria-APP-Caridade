from flask import jsonify, request
from models.bens import Bem

def adicionar_bem():
    bem = Bem(request.json['nome'], request.json['categoria'], request.json['quantidade'])
    bem.adicionar_bem()
    return jsonify({'mensagem': 'Bem adicionado com sucesso!'}), 201

def listar_bens():
    bens = Bem.listar_bens()
    return jsonify([{'id': b[0], 'nome': b[1], 'categoria': b[2], 'quantidade': b[3]} for b in bens])

def deletar_bem(id):
    Bem.deletar_bem(id)
    return jsonify({'mensagem': 'Bem deletado com sucesso!'})