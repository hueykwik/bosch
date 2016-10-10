# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:48:10 2016

@author: Dave
"""

import pandas as pd
import os
import time

# get all categoricals

def notnull_colsbyrow(df, index):
    present = df.loc[index].notnull()
    colindices = present[present == True].index
    return df.loc[index,colindices]

numeric = pd.read_csv('train_numeric.csv',
                    nrows = 1000, 
                    index_col = 0, 
                    dtype = pd.np.float32,)

categoricals = pd.read_csv('train_categorical.csv',
                    nrows = 1000, 
                    index_col = 0)
                    
# use base to store response code
base = pd.read_csv('train_numeric.csv',
                     usecols = ['Id', 'Response'],
                     index_col = 0,
                     dtype = pd.np.float32)
                     
# read in categorical data one row at a time
print('start loading iterators')
iter_csv = pd.read_csv('train_categorical.csv', 
                           iterator = True, 
                           chunksize = 1000,
                           index_col = 0)

#find failing responses
failures = pd.concat([chunk[chunk['Response'] == 1] for chunk in iter_csv])
for chunk in iter_csv:
    for row in chunk.iterrows():
        present = notnull_colsbyrow(chunk, row)
        break
    break