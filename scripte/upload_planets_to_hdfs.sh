#!/bin/bash

# Copier le fichier local dans le container namenode
docker cp "/mnt/d/CourIPPSSI_5émeAnnée/planet-discovery-pipeline/Data/planets_dataset.csv" namenode:/myhadoop/

# Créer un répertoire plus simple dans HDFS
docker exec namenode hdfs dfs -mkdir -p /user/hive/planets

# Envoyer le fichier CSV vers HDFS
docker exec namenode hdfs dfs -put -f /myhadoop/planets_dataset.csv /user/hive/planets/

# Vérification (liste le répertoire pour voir si le fichier est bien là)
docker exec namenode hdfs dfs -ls /user/hive/planets


#./upload_planets_to_hdfs.sh
