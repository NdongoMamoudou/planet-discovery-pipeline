# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

# Initialisation de la session Spark
spark = SparkSession.builder \
    .appName("AppPlanetDiscovery") \
    .config("spark.sql.streaming.checkpointLocation", "/path/to/checkpoint") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0") \
    .getOrCreate()

# Schéma des données avec les bons types
# schema = StructType([
#     StructField("id", StringType(), True),
#     StructField("nom", StringType(), True),
#     StructField("decouvreur", StringType(), True),
#     StructField("date_de_decouverte", DateType(), True),  
#     StructField("masse", IntegerType(), True),  
#     StructField("rayon", IntegerType(), True),  
#     StructField("distance", IntegerType(), True),  
#     StructField("type", StringType(), True),
#     StructField("statut", StringType(), True),
#     StructField("atmosphere", StringType(), True),
#     StructField("temperature_moyenne", IntegerType(), True),  
#     StructField("periode_orbitale", IntegerType(), True),  
#     StructField("nombre_de_satellites", IntegerType(), True),  
#     StructField("presence_deau", StringType(), True)  
# ])

schema = StructType([
    StructField("id", StringType(), True),
    StructField("nom", StringType(), True),
    StructField("decouvreur", StringType(), True),
    StructField("date_de_decouverte", DateType(), True),  
    StructField("masse", StringType(), True),  
    StructField("rayon", StringType(), True),  
    StructField("distance", StringType(), True),  
    StructField("type", StringType(), True),
    StructField("statut", StringType(), True),
    StructField("atmosphere", StringType(), True),
    StructField("temperature_moyenne", StringType(), True),  
    StructField("periode_orbitale", StringType(), True),  
    StructField("nombre_de_satellites", StringType(), True),  
    StructField("presence_deau", StringType(), True)  
])


# Lecture du stream Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "planet-discoveries") \
    .load()

# Conversion du message Kafka (en bytes) en chaîne de caractères (String)
messages_df = kafka_df.selectExpr("CAST(value AS STRING)")

# Utilisation du schéma pour convertir les données JSON en DataFrame
json_df = messages_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Affichage des résultats dans la console
query = json_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Attente de la fin de l'opération
query.awaitTermination()
