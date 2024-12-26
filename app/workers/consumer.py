from kafka import KafkaConsumer
import json
from app.services.xml_parser import process_xml

KAFKA_TOPIC = 'xml-files-topic'
KAFKA_SERVER = 'localhost:9093'

def start_kafka_consumer():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id='xml-consumer-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in consumer:
        xml_data = message.value
        xml_path = xml_data['file_path']
        
        process_xml(xml_path)