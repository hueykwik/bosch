# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np 

import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use('ggplot')
np.set_printoptions(threshold=np.inf)

# Load training data
categorical = pd.read_csv('train_categorical.csv', nrows=100)
dates = pd.read_csv('train_date.csv', nrows=100)
numerics = pd.read_csv('train_numeric.csv', nrows=100)
categorical.head(20)

# Submission
submission = pd.read_csv('sample_submission.csv')