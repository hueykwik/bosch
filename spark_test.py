# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:39:28 2016

Copied from: http://www.elenacuoco.com/2016/08/28/pyspark-first-approaches-ml-classification/

@author: hkwik
"""

from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.classification import GBTClassifier

import numpy as np
import pandas as pd

spark = SparkSession\
    .builder\
    .appName("example-spark")\
    .config("spark.sql.crossJoin.enabled","true")\
    .getOrCreate()
#sc = SparkContext()
#sqlContext = SQLContext(sc)

print('reading csv')
train = spark.read.csv("data/train_numeric.csv", header="true", inferSchema="true")
print('done reading csv')
print('filling na')
train = train.na.fill(0.0)
print('done filling na')

from pyspark.ml.feature import VectorAssembler
ignore = ['Id', 'Response']
lista=[x for x in train.columns if x not in ignore]

assembler = VectorAssembler(
    inputCols=lista,
    outputCol='features')

train = (assembler.transform(train).select('Response',"features"))

## Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = train.randomSplit([0.7, 0.3])
# (trainingData, testData) = train.randomSplit([0.001, 0.99])  # Just for speed while testing correctness

# Train a GBT model.
gbt = GBTClassifier(labelCol="Response", featuresCol="features", maxIter=10)
#lr = LogisticRegression(labelCol="Response", featuresCol="features", maxIter=10, regParam=0.3, elasticNetParam=0.8)

# Chain indexers and GBT in a Pipeline
pipeline = Pipeline(stages=[gbt])

print('training model')
# Train model.  This also runs the indexers.
model = pipeline.fit(trainingData) # Make predictions.

# Test against validation set
print('testing against validation set')
predictions = model.transform(testData)
predsGBT=predictions.select("prediction").rdd.map(lambda r: r[0]).collect()
preds=np.asarray(predsGBT).astype(int)

# Make predictions and submit
data_test = spark.read.csv("data/test_numeric.csv", header="true", inferSchema="true")
data_test = data_test.na.fill(0.0)
data_test = (assembler.transform(data_test).select("features"))

preds = model.transform(data_test)

predsGBT=preds.select("prediction").rdd.map(lambda r: r[0]).collect()

sub = pd.read_csv("data/sample_submission.csv")
sub['Response'] = np.asarray(predsGBT).astype(int)
sub.to_csv('bosch-spark.csv', index=False)

print('done')
