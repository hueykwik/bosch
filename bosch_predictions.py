# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np 

# Type these into IPython console
# %matplotlib inline
# %matplotlib qt

import matplotlib
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.base import TransformerMixin

import time

from sklearn.linear_model import LogisticRegression

matplotlib.style.use('ggplot')

# Load training data
#categorical = pd.read_csv('train_categorical.csv', nrows=100)
#dates = pd.read_csv('train_date.csv', nrows=100)
numerics = pd.read_csv('train_numeric.csv', nrows=10000)
#categorical.head(20)

# Get all failed examples - > 53
failed = numerics.loc[numerics.Response == 1].index

success = numerics.loc[numerics.Response == 0].sample(53, random_state=9).index

indices = failed.append(success)

# Load test data

start = time.time()
numerics_test = pd.read_csv('test_numeric.csv')
print(time.time() - start)

# Predict on numerics
y_m = numerics.loc[indices, 'Response']
X_m = numerics[numerics.columns.difference(['Id', 'Response'])]
X_m = X_m.loc[indices]

X_m_test = numerics_test[numerics_test.columns.difference(['Id', 'Response'])]

X_m.head()
X_m.loc[:, 'L3_S51_F4256']  # example of NaN

class ZeroImputer(TransformerMixin):
    def __init__(self):
        """Impute missing values to zero.
        """
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X.fillna(0)
  
# Test imputer turns NAs to 0      
# ZeroImputer().fit_transform(X_m).loc[,'L3_S51_F4256']

# Pipeline example
pipe_clf = Pipeline([('impute', ZeroImputer()),
                     ('clf', LogisticRegression()),
])


pipe_clf = pipe_clf.fit(X_m, y_m)
y_pred = pipe_clf.predict(X_m_test)
print(y_pred.sum())

print(time.time() - start)
  
# Submission
submission = pd.read_csv('sample_submission.csv')
submission.Response = y_pred

print(time.time() - start)

submission.to_csv('first_submission.csv', index=False)