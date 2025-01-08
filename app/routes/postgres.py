from flask import Flask, request, jsonify, Blueprint
from app.db import PostgreSQL

postgres_routes = Blueprint('postgres_routes', __name__)


@postgres_routes.route('/<table_name>/', methods=['GET'])
def get_all(table_name=None):
    try:
        db = PostgreSQL()
        data = db.get_all(table_name)
        if not data:
            return jsonify({"error": "Nenhum dado encontrado."}), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar dados: {str(e)}"}), 500


@postgres_routes.route('/<table_name>/<int:record_id>/', methods=['GET'])
def get_by_id(table_name=None, record_id=None):
    try:
        if not record_id:
            return jsonify({"error": "ID não fornecido."}), 400

        db = PostgreSQL()
        data = db.get_by_id(table_name, record_id)

        if not data:
            return jsonify({"error": "Registro não encontrado."}), 404

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar o registro: {str(e)}"}), 500


@postgres_routes.route('/<table_name>/', methods=['POST'])
def insert(table_name=None):
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Nenhum dado fornecido."}), 400

        db = PostgreSQL()
        new_id = db.insert(table_name, data)
        return jsonify({"id": new_id}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao inserir dados: {str(e)}"}), 500


@postgres_routes.route('/<table_name>/<int:record_id>/', methods=['PUT'])
def update(table_name=None, record_id=None):
    try:
        if not record_id:
            return jsonify({"error": "ID não fornecido."}), 400

        data = request.get_json()

        if not data:
            return jsonify({"error": "Nenhum dado fornecido para atualização."}), 400

        db = PostgreSQL()
        db.update(table_name, record_id, data)
        return jsonify({"message": "Registro atualizado com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar o registro: {str(e)}"}), 500


@postgres_routes.route('/<table_name>/<int:record_id>/', methods=['DELETE'])
def delete(table_name=None, record_id=None):
    try:
        if not record_id:
            return jsonify({"error": "ID não fornecido."}), 400

        db = PostgreSQL()
        data = db.get_by_id(table_name, record_id)

        if not data:
            return jsonify({"error": "Registro não encontrado."}), 404

        db.delete(table_name, record_id)
        return jsonify({"message": "Registro excluído com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir o registro: {str(e)}"}), 500


@postgres_routes.route('/<table_name>/bulk_edit/', methods=['POST'])
def bulk_edit(table_name=None):
    """Realiza operações em massa: insert, update, delete."""
    try:
        db = PostgreSQL()
        data = request.get_json()

        if not data:
            return jsonify({"error": "Nenhum dado fornecido."}), 400

        inserts = data.get("insert", [])
        updates = data.get("update", [])
        deletes = data.get("delete", [])

        insert_ids = []

        # Realiza inserções em massa
        try:
            for record in inserts:
                new_id = db.insert(table_name, record)
                insert_ids.append(new_id)
        except Exception as e:
            return jsonify({"error": f"Erro ao inserir registros: {str(e)}"}), 400

        # Realiza atualizações em massa
        try:
            for record in updates:
                record_id = record.get('id')
                if not record_id:
                    return jsonify({"error": "ID faltando para atualização."}), 400
                db.update(table_name, record_id, record)
        except Exception as e:
            return jsonify({"error": f"Erro ao atualizar registros: {str(e)}"}), 400

        # Realiza exclusões em massa
        try:
            for record in deletes:
                record_id = record.get('id')
                if not record_id:
                    return jsonify({"error": "ID faltando para exclusão."}), 400
                db.delete(table_name, record_id)
        except Exception as e:
            return jsonify({"error": f"Erro ao excluir registros: {str(e)}"}), 400

        return jsonify({
            "message": "Operações em massa realizadas com sucesso!",
            "inserted_ids": insert_ids
        }), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao realizar operações em massa: {str(e)}"}), 500


@postgres_routes.route('/<table_name>/', methods=['POST'])
def create_table(table_name=None):
    """Cria uma nova tabela no PostgreSQL."""
    try:
        if not table_name:
            return jsonify({"error": "Nome da tabela não fornecido."}), 400

        data = request.get_json()
        columns = data.get("columns", [])
        if not columns:
            return jsonify({"error": "É necessário fornecer as colunas para a tabela."}), 400

        db = PostgreSQL()
        db.create_table(table_name, columns)
        return jsonify({"message": f"Tabela {table_name} criada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao criar tabela: {str(e)}"}), 400


@postgres_routes.route('/<table_name>/', methods=['DELETE'])
def delete_table(table_name=None):
    """Exclui uma tabela no PostgreSQL."""
    try:
        if not table_name:
            return jsonify({"error": "Nome da tabela não fornecido."}), 400

        db = PostgreSQL()
        db.delete_table(table_name)
        return jsonify({"message": f"Tabela {table_name} excluída com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao excluir tabela: {str(e)}"}), 400
