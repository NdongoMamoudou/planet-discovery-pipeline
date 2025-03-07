import time
from kafka import KafkaProducer
import json

# Configuration
KAFKA_BROKER = "kafka:9092"
TOPIC = "planet-discoveries"

# Attendre quelques secondes pour s'assurer que Kafka est prêt
time.sleep(10)


# Initialisation du producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_discovery_to_kafka(data):
    """Envoie les données de découverte à Kafka."""
    try:
        producer.send(TOPIC, value=data)
        producer.flush()
        print("Donnée envoyée à Kafka avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi à Kafka: {e}")
        raise


