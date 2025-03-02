# Utilise l'image Python 3.9 en version slim
FROM python:3.9-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier des dépendances et l'installe
COPY requirements.txt requirements.txt

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie l'ensemble de votre code dans le conteneur
COPY . .

