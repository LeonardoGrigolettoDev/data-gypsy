from flask import Flask, request, jsonify, Blueprint
from app.db import MongoDB
from bson.objectid import ObjectId

mongo_routes = Blueprint('mongo_routes', __name__)


@mongo_routes.route('/<collection_name>/', methods=['GET'])
def get_all(collection_name=None, filters=None):
    try:
        db = MongoDB()
        data = db.get_all(collection_name)
        if not data:
            return jsonify({"error": "Nenhum dado encontrado."}), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar dados: {str(e)}"}), 500


@mongo_routes.route('/<collection_name>/<record_id>/', methods=['GET'])
def get_by_id(collection_name=None, record_id=None):
    try:
        # Verificar se o ID é válido
        if not ObjectId.is_valid(record_id):
            return jsonify({"error": "ID inválido."}), 400

        db = MongoDB()
        data = db.get_by_id(collection_name, ObjectId(record_id))

        if not data:
            return jsonify({"error": "Registro não encontrado."}), 404

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar o registro: {str(e)}"}), 500


@mongo_routes.route('/<collection_name>/', methods=['GET'])
def insert(collection_name=None):
    try:
        data = request.get_json()

        # Verificar se os dados estão presentes
        if not data:
            return jsonify({"error": "Nenhum dado fornecido."}), 400

        db = MongoDB()
        new_id = db.insert(collection_name, data)
        return jsonify({"id": new_id}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao inserir dados: {str(e)}"}), 500


@mongo_routes.route('/<collection_name>/<record_id>/', methods=['PUT'])
def update(collection_name=None, record_id=None):
    try:
        # Verificar se o ID é válido
        if not ObjectId.is_valid(record_id):
            return jsonify({"error": "ID inválido."}), 400

        data = request.get_json()

        # Verificar se os dados foram fornecidos
        if not data:
            return jsonify({"error": "Nenhum dado fornecido para atualização."}), 400

        db = MongoDB()
        db.update(collection_name, ObjectId(record_id), data)
        return jsonify({"message": "Registro atualizado com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar o registro: {str(e)}"}), 500


@mongo_routes.route('/<collection_name>/<record_id>/', methods=['DELETE'])
def delete(collection_name=None, record_id=None):
    try:
        # Verificar se o ID é válido
        if not ObjectId.is_valid(record_id):
            return jsonify({"error": "ID inválido."}), 400

        db = MongoDB()
        data = db.get_by_id(collection_name, ObjectId(record_id))

        if not data:
            return jsonify({"error": "Registro não encontrado."}), 404

        db.delete(collection_name, ObjectId(record_id))
        return jsonify({"message": "Registro excluído com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir o registro: {str(e)}"}), 500


@mongo_routes.route('/<collection_name>/', methods=['POST'])
def create_collection(collection_name=None):
    """Cria uma nova coleção no MongoDB."""
    try:
        if not collection_name:
            return jsonify({"error": "É necessário fornecer um nome para a coleção."}), 400

        db = MongoDB()
        db.create_collection(collection_name)
        return jsonify({"message": f"Coleção {collection_name} criada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao criar coleção: {str(e)}"}), 500


@mongo_routes.route('/<collection_name>/', methods=['DELETE'])
def delete_collection(collection_name=None):
    """Exclui uma coleção no MongoDB."""
    try:
        if not collection_name:
            return jsonify({"error": "É necessário fornecer um nome para a coleção."}), 400

        db = MongoDB()
        data = db.db[collection_name]  # Verifica se a coleção existe
        if not data:
            return jsonify({"error": "Coleção não encontrada."}), 404

        db.delete_collection(collection_name)
        return jsonify({"message": f"Coleção {collection_name} excluída com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir coleção: {str(e)}"}), 500
