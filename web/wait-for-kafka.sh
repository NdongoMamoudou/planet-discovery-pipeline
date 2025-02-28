#!/bin/bash

# Attente que Kafka soit disponible sur le port 9092
while ! nc -z kafka 9092; do
  echo "En attente de Kafka..."
  sleep 2
done

# Une fois Kafka prêt, lancer l'application Flask
echo "Kafka est prêt, démarrage de Flask..."
python /app/app.py
