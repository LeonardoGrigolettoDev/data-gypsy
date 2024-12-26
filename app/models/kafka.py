from kafka import KafkaProducer
import os
import json

KAFKA_TOPIC = 'xml-files-topic'
KAFKA_SERVER = 'localhost:9093'

def enqueue_xml_to_kafka(tmpdir):
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    for xml_file in os.listdir(tmpdir):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(tmpdir, xml_file)
            message = {"file_path": xml_path}
            
            # Enviar mensagem para o Kafka
            producer.send(KAFKA_TOPIC, message)
    
    producer.flush()  # Garantir que todas as mensagens foram enviadas


