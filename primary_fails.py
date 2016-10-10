# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 11:36:17 2016
primary failure detection from numerics
@author: Dave
"""

import pandas as pd
import os
import time

# get all times for a part id, associate with my time data
# numeric.loc[4.0].difference([numeric.loc[4.0].notnull()])

def notnull_colsbyrow(df, index):
    present = df.loc[index].notnull()
    colindices = present[present == True].index
    return df.loc[index,colindices]


#dates = pd.read_csv('train_date.csv',
#                    nrows = 20000, 
#                    index_col = 0, 
#                    dtype = pd.np.float64,)
#                    
numeric = pd.read_csv('train_numeric.csv',
                    nrows = 1000, 
                    index_col = 0, 
                    dtype = pd.np.float32,)

#categoricals = pd.read_csv('train_categorical.csv',
#                    nrows = 1000, 
#                    index_col = 0)


### save mean, count, std, meadian for failures, all values, and only R=0
# initialize storage
numeric_meta = pd.DataFrame(pd.np.nan,
                            index = numeric.columns,
                            columns = ['fail_mean', 'all_mean', 'lessfails_mean',
                                       'fail_count','all_count',
                                       'lessfails_count',
                                       'fail_std', 'all_std', 'lessfails_std',
                                       'fail_median', 'all_median', 'lessfails_median'])
# data on all, data on failures, value counts is set
valuecount_holder = {}
lessfailscount_holder = {}
failcount_holder = {}
base = pd.read_csv('train_numeric.csv',
                     usecols = ['Id', 'Response'],
                     index_col = 0,
                     dtype = pd.np.float32)
start_time = time.time()
curtime = time.time()
stillrun = True

# load in data one column at a time
for i in numeric.columns:
    twocol = base.copy()
    newcol = pd.read_csv('train_numeric.csv',
                     usecols = ['%s' % (i)],
                     squeeze = True,
                     dtype = pd.np.float32)
    twocol[i] = newcol.values
    twocol.dropna(inplace = True)
    twocol.loc[:,i] = twocol.loc[:,i].abs()
    fails = twocol[twocol.Response == 1]
    lessfails = twocol[twocol.Response == 0]
    valuecount_holder[i] = twocol.loc[:,i].value_counts()
    failcount_holder[i] = fails.loc[:,i].value_counts()
    lessfailscount_holder[i] = lessfails.loc[:,i].value_counts()
    numeric_meta.loc[i] = [fails.loc[:,i].mean(),
                           twocol.loc[:,i].mean(),
                           lessfails.loc[:,i].mean(),
                           len(fails),
                           len(twocol),
                           len(lessfails),
                           fails.loc[:,i].std(),
                           twocol.loc[:,i].std(),
                           lessfails.loc[:,i].std(),
                           fails.loc[:,i].median(),
                           twocol.loc[:,i].median(),
                           lessfails.loc[:,i].median()]
    print("""Finished one column (%s), time since start = %s, 
          time since last = %s"""% (i, str(time.time() - start_time), str(time.time()-curtime)))
    curtime = time.time()

    
#==============================================================================
# # DEPRECATED
# # goes through numeric to give meta-information
# df = numeric.loc[:,numeric.columns.difference(['Response'])]
# 
# # get a count of values by feature
# stop_at_index = 15000
# features_count = df[df.index < stop_at_index].count()
# features_fail_count = numeric[numeric.Response == 1].count()
# 
# allvals = pd.Series()
# lenall = 0
# for i in numeric.index:
#     temp = notnull_colsbyrow(df,i)
#     lenall += len(temp)
#     allvals = allvals.append(temp.abs())
#     if i > stop_at_index:
#         break
#     
# failvals = pd.Series()
# lenfail = 0
# for i in numeric[numeric.Response == 1].index:
#     temp = notnull_colsbyrow(df.loc[numeric[numeric.Response == 1].index],i)
#     lenfail += len(temp)
#     failvals = failvals.append(temp.abs())
# #    if i > 5000:
# #        break
# 
# 
# #slice by stations
# mean_features = pd.DataFrame()
# for col in allvals.index.unique():
#     original = allvals[allvals.index == col]
#     ori_mean = original.mean(skipna = True)
#     fails = failvals[failvals.index == col]
#     fail_mean = fails.mean(skipna = True)
#     onerow = pd.DataFrame({'original':ori_mean, 'fail': fail_mean}, index = [col])
#     mean_features = mean_features.append(onerow)
#     
# # get all features where failing values are outside of a percentage of original
# percent_diff = 0.6
# 
# high = mean_features.fail > mean_features.original * (1 + percent_diff)
# low = mean_features.fail < mean_features.original * (1 - percent_diff)
# 
# outside_map = high.values | low.values
# primary_features = mean_features[outside_map]
# 
# primary_features['all_count'] = features_count.loc[primary_features.index]
# primary_features['fail_count'] = features_fail_count.loc[primary_features.index]
# 
# # remove features with small numbers of measurements and all fails = 0
# primary_features = primary_features[primary_features.fail != 0]
# primary_features = primary_features[primary_features.all_count >= 50]
# 
#==============================================================================