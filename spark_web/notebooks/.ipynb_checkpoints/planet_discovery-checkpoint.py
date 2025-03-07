
# -*- coding: utf-8 -*-



from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_date, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, DateType, BooleanType

# Initialisation de la session Spark
spark = SparkSession.builder \
    .appName("AppPlanetDiscovery") \
    .config("spark.sql.streaming.checkpointLocation", "/path/to/checkpoint") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0") \
    .getOrCreate()

# Schéma directement typé (en prenant en compte les données sous forme de chaîne)
schema = StructType([
    StructField("id", StringType(), True),
    StructField("nom", StringType(), True),
    StructField("decouvreur", StringType(), True),
    StructField("date_de_decouverte", StringType(), True), 
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

# Lecture du stream Kafka avec startingOffsets pour consommer depuis le début
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "planet-discoveries") \
    .option("startingOffsets", "earliest").load()

# Conversion du message Kafka (en bytes) en String
messages_df = kafka_df.selectExpr("CAST(value AS STRING)")

# Parsing JSON avec le schéma initial
json_df = messages_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Conversion explicite des colonnes aux bons types
final_df = json_df \
    .withColumn("date_de_decouverte", to_date(col("date_de_decouverte"), "yyyy-MM-dd")) \
    .withColumn("masse", col("masse").cast(DoubleType())) \
    .withColumn("rayon", col("rayon").cast(DoubleType())) \
    .withColumn("distance", col("distance").cast(DoubleType())) \
    .withColumn("temperature_moyenne", col("temperature_moyenne").cast(DoubleType())) \
    .withColumn("periode_orbitale", col("periode_orbitale").cast(DoubleType())) \
    .withColumn("nombre_de_satellites", col("nombre_de_satellites").cast(IntegerType())) \
    .withColumn("presence_deau", when(col("presence_deau") == "oui", True)
                                    .when(col("presence_deau") == "non", False)
                                    .otherwise(None))  

# Affichage dans la console (ou autre sink)
query = final_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
