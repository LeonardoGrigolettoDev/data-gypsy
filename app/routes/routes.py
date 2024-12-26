from flask import Blueprint, request, jsonify
import app
import zipfile
import os
import tempfile
from app.models.mongodb import get_mongo_db
from app.models.postgres import get_postgres_session
from app.models.kafka import enqueue_xml_to_kafka
from ..utils.file import extract_zip
data_blueprint = Blueprint("data", __name__)

# Exemplo de rota para inserir dados no MongoDB


@data_blueprint.route("/insert_mongo", methods=["POST"])
def insert_mongo():
    data = request.json
    db = get_mongo_db()
    collection = db["data_collection"]
    collection.insert_one(data)
    return jsonify({"message": "Data inserted successfully!"}), 200

# Exemplo de rota para inserir dados no PostgreSQL


@data_blueprint.route("/insert_postgres", methods=["POST"])
def insert_postgres():
    data = request.json
    session = get_postgres_session()
    session.execute(
        "INSERT INTO my_table (data) VALUES (:data)", {"data": data})
    session.commit()
    return jsonify({"message": "Data inserted successfully!"}), 200

# Exemplo de rota para enviar dados para Kafka


# @data_blueprint.route("/send_kafka", methods=["POST"])
# def send_kafka():
#     data = request.json
#     send_message_to_kafka("my_topic", str(data))
#     return jsonify({"message": "Message sent to Kafka!"}), 200


@data_blueprint.route('/upload', methods=['POST'])
def upload_file():
    zip_file = request.files['file']

    if zip_file and zip_file.filename.endswith('.zip'):
        # Criar diretório temporário para armazenar os XMLs extraídos
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, zip_file.filename)
            zip_file.save(zip_path)

            # Descompactar o ZIP
            extract_zip(zip_path, tmpdir)

            # Enfileirar os XMLs no Kafka
            enqueue_xml_to_kafka(tmpdir)

        return "Arquivo processado com sucesso", 200
    return "Arquivo ZIP inválido", 400