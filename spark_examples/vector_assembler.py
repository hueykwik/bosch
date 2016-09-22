"""
Example of using VectorAssembler in spark
"""
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

spark = SparkSession\
    .builder\
    .appName("example-spark")\
    .config("spark.sql.crossJoin.enabled","true")\
    .getOrCreate()
dataset = spark.createDataFrame(
    [(0, 18, 1.0, Vectors.dense([0.0, 10.0, 0.5]), 1.0)],
    ["id", "hour", "mobile", "userFeatures", "clicked"])
assembler = VectorAssembler(
    inputCols=["hour", "mobile", "userFeatures"],
    outputCol="features")
output = assembler.transform(dataset)
print(output.select("features", "clicked").first())
