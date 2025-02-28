from flask import Flask, request, jsonify, render_template
from flask import  jsonify
from kafka import KafkaProducer
import json



# Configuration du Kafka Producer
KAFKA_BROKER = "kafka:9092"
TOPIC = "planet-discoveries"


# Initialisation du Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Sérialisation en JSON
)



# Initialisation de l'application Flask
app = Flask(__name__)



# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')



# Route pour l'ajout d'une découverte
# Les données de la découverte sont envoyées à Kafka
@app.route('/discovery', methods=['POST'])
def add_discovery():
    data = request.get_json()



    if not data:
        return jsonify({'error': 'Aucune donnée fournie'}), 400

    required_fields = [
        'id', 'nom', 'decouvreur', 'date_de_decouverte', 'masse', 
        'rayon', 'distance', 'type', 'statut', 'atmosphere', 
        'temperature_moyenne', 'periode_orbitale', 'nombre_de_satellites', 'presence_deau'
    ]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f"Champs requis manquants: {', '.join(missing_fields)}"}), 400

    print(f"Received discovery data: {data}")

    #  Envoi des données à Kafka
    try:
        producer.send(TOPIC, value=data)
        producer.flush()
        print("Donnée envoyée à Kafka avec succès.")
        return jsonify({'message': 'Donnée envoyée à Kafka'}), 200
    except Exception as e:
        print(f"Erreur lors de l'envoi à Kafka: {e}")
        return jsonify({'error': 'Erreur lors de l\'envoi à Kafka'}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5550)
