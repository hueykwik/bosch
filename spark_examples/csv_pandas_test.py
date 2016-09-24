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
train = spark.read.csv("data/dates_small.csv", header="true", inferSchema="true")
print('here')
print(train)
print('there')
df = train.toPandas()

print(df.head())
