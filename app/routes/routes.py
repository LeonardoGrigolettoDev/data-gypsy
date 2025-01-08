from app.db import PostgreSQL, MongoDB
from flask import request, jsonify, Blueprint

general_routes = Blueprint('general_routes', __name__)

@general_routes.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return "File is not valid.", 400
    match(file):
        case file.filename.endswith('.zip'):
            return "Not implemented (ZIP)", 200
        case file.filename.endswith('.csv'):
            return "Not implemented (CSV)", 200

@general_routes.route('/health', methods=['GET'])
def health():
    # Verificando a conexão com o PostgreSQL
    postgres_db = PostgreSQL()
    if not postgres_db.check_connection():
        return jsonify({"status": "fail", "message": "PostgreSQL connection failed"}), 500

    # Verificando a conexão com o MongoDB
    mongo_db = MongoDB()
    if not mongo_db.check_connection():
        return jsonify({"status": "fail", "message": "MongoDB connection failed"}), 500

    # Se todas as conexões estiverem ok
    return jsonify({"status": "success", "message": "API is healthy"}), 200
