# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np 

# Type these into IPython console
# %matplotlib inline
# %matplotlib qt

import matplotlib
import matplotlib.pyplot as plt

import time

from sklearn.linear_model import LogisticRegression

matplotlib.style.use('ggplot')
# np.set_printoptions(threshold=np.inf)

# Example plot
#plt.plot(range(10), 'o')
#plt.show()

# Load training data
#categorical = pd.read_csv('train_categorical.csv', nrows=100)
#dates = pd.read_csv('train_date.csv', nrows=100)
numerics = pd.read_csv('train_numeric.csv', nrows=10000)
#categorical.head(20)

# Get all failed examples - > 53
failed = numerics.loc[numerics.Response == 1].index

success = numerics.loc[numerics.Response == 0].sample(53, random_state=9).index

indices = failed.append(success)

# combine them into a dataframe

# Load test data

start = time.time()
numerics_test = pd.read_csv('test_numeric.csv')
print(time.time() - start)

# Run some ML to get predictions

# Predict on numerics
y_m = numerics.loc[indices, 'Response']
X_m = numerics[numerics.columns.difference(['Id', 'Response'])]
X_m = X_m.loc[indices]

# Impute NaNs to 0
for col in list(X_m):
    X_m[col].loc[X_m[col].isnull()] = 0
    
print(time.time() - start)
    
#X_m['L3_S48_F4196'].sum()  # currently 0
#numerics['L3_S48_F4196'].sum()  # 8.920000000000007

#numerics['L3_S48_F4196'].shape

clf = LogisticRegression()
clf.fit(X_m, y_m)

print(time.time() - start)

#print(clf.coef_)

X_m_test = numerics_test[numerics_test.columns.difference(['Id', 'Response'])]
# Impute NaNs to 0
for col in list(X_m_test):
    X_m_test[col].loc[X_m_test[col].isnull()] = 0

y_pred = clf.predict(X_m_test)
print(y_pred.sum())

# Submission
submission = pd.read_csv('sample_submission.csv')
submission.Response = y_pred

print(time.time() - start)