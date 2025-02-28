# #!/bin/bash

# # Attendre que Kafka soit prêt
# KAFKA_HOST="kafka"
# KAFKA_PORT="9092"

# echo "En attente que Kafka soit prêt..."

# # Boucle pour tester la connexion à Kafka toutes les 5 secondes
# while ! nc -z $KAFKA_HOST $KAFKA_PORT; do
#   echo "Kafka n'est pas prêt, réessayer..."
#   sleep 10
# done

# echo "Kafka est prêt!"
