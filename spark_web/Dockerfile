# Utilisation d'une image de base 
FROM bde2020/spark-master:3.3.0-hadoop3.3

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de configuration
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN pip install -r requirements.txt

# # Copier tout le contenu du répertoire courant dans le conteneur
# COPY . .


