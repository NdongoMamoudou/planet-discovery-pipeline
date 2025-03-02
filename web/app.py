from flask import Flask, request, jsonify, render_template
from kafka_web.producer import send_discovery_to_kafka

# Initialisation de l'application Flask
app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour l'ajout d'une découverte
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

    try:
        send_discovery_to_kafka(data)
        return jsonify({'message': 'Donnée envoyée à Kafka'}), 200
    except Exception as e:
        return jsonify({'error': 'Erreur lors de l\'envoi à Kafka'}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5550)
