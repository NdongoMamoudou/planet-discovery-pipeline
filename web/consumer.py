from kafka import KafkaConsumer
import json

# Configuration
KAFKA_BROKER = "kafka:9092"
TOPIC = "planet-discoveries"

# Création du consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',  # Lire depuis le début
    group_id="planet-discovery-group"
)

print("✅ Consumer démarré et en attente de messages...")

# Lecture des messages
for message in consumer:
    data = message.value
    print(f"📥 Message reçu : {json.dumps(data, indent=2, ensure_ascii=False)}")

