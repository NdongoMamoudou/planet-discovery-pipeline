FROM jupyter/pyspark-notebook:spark-3.3.0

# Copier le fichier requirements.txt dans l'image
COPY requirements.txt /tmp/requirements.txt

# Installer les dépendances Python à partir du fichier requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# # Supprimer le fichier requirements.txt après installation (optionnel)
# RUN rm /tmp/requirements.txt
