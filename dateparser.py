# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 14:40:11 2016
Kaggle date data into steady state
@author: Dave
"""

import pandas as pd
import os

# get all times for a part id, associate with my time data
# numeric.loc[4.0].difference([numeric.loc[4.0].notnull()])

def notnull_colsbyrow(df, index):
    present = df.loc[index].notnull()
    colindices = present[present == True].index
    return df.loc[index,colindices]


dates = pd.read_csv('train_date.csv',
                    nrows = 10000, 
                    index_col = 0, 
                    dtype = pd.np.float64,)
                    
numeric = pd.read_csv('train_numeric.csv',
                    nrows = 10000, 
                    index_col = 0, 
                    dtype = pd.np.float64,)
                    
test =  pd.read_csv('test_date.csv',
                    nrows = 10000, 
                    index_col = 0, 
                    dtype = pd.np.float64,)

#==============================================================================
# categories = pd.read_csv('train_categorical.csv',
#                          nrows = 100, 
#                          index_col = 0, 
#                          low_memory = False)
#==============================================================================

counter = 0
line_station_dict = {}
for col in dates:
    #add all column names to set that correspond to line and station
#    print(col.split('_'))
    lsname = col.split('_')
    lsid = lsname[1] #lsname[0] + '_' + 

    if lsid in line_station_dict.keys():
        line_station_dict[lsid].append(col)
    else:
        line_station_dict[lsid] = [col]
    
#    if counter > 5:
#        break
    counter += 1

# collect all series for stations into one Series, remove duplicates, store
stationtimes = {}    
progress = 0
length = len(line_station_dict.keys())
for key in line_station_dict.keys():
    alltimes = pd.Series()
    for colname in line_station_dict[key]:
        alltimes = alltimes.append(dates[colname])
        alltimes.dropna(inplace = True)
        alltimes.drop_duplicates(inplace = True)
    
    stationtimes[key] = alltimes.sort_values().diff().iloc[1:]
    print('progress:',progress/length)
    progress += 1


avgtimes = {}
stdtimes = {}
hasoutliers = {}
for i in stationtimes.keys():
    avgtimes[i] = stationtimes[i].mean()
    stdtimes[i] = stationtimes[i].std()
    
    condition = avgtimes[i] + stdtimes[i]
    number = len(stationtimes[i])
    if ((stationtimes[i] - condition) > 0).sum() > 3: #(number/30):
        hasoutliers[i] = True
    else: 
        hasoutliers[i] = False

#==============================================================================
# timebin = pd.Series()    
# for i in hasoutliers.keys():
#     if hasoutliers[i]:
#         timebin = timebin.append(stationtimes[i])
#==============================================================================

hasoutliers = pd.Series(hasoutliers)

#shouldn't be needed
#==============================================================================
# prog_counter = 0
# numrows = len(numeric)
# for i in numeric.index:
#     present_cols = notnull_colsbyrow(numeric, i)
#     oneid = pd.DataFrame({'num_present':present_cols})
#     oneid['station'] = present_cols.index.str[3:6].str.strip('_')
#     oneid['late'] = oneid.station.isin(hasoutliers[hasoutliers == True].index)
#     total_through_late_stations = oneid.late.sum()
#     numeric.loc[i,'throughlate'] = total_through_late_stations
#     prog_counter += 1
#     
#     if prog_counter % 200 == 0:
#         print('stupid one row at a time',prog_counter / numrows)
#==============================================================================

stations = numeric.columns
onerow = {}
for j in range(len(stations)):
    string = stations[j][3:6].strip('_')
    if string in hasoutliers[hasoutliers == True].index:
        onerow[stations[j]] = 1
    else:
        onerow[stations[j]] = 0
    
tomult = pd.DataFrame(onerow,index = numeric.index)
numeric['throughlate'] = numeric.notnull().multiply(tomult).sum(axis = 1)

#timebin.plot(kind = 'hist')
#manhist = timebin.value_counts()
#print(manhist[manhist.index > 19])
#display = manhist[manhist.index > 19].sort_index()
#manhist[manhist.index > 19].sort_index().plot(kind = 'bar')

#counter = 0
#for cur in line_station_dict.keys():
#    print(cur)
#    print(line_station_dict[cur])
#    counter += 1
#    
#    if counter > 10:
#        break

##### Check if test and train have similar date profiles
####### read in only parts of a file to grab the failures only
iter_csv = pd.read_csv('train_numeric.csv', 
                           iterator = True, 
                           chunksize = 1000,
                           index_col = 0)

failures = pd.concat([chunk[chunk['Response'] == 1] for chunk in iter_csv])
indexfail = failures.index

#read in datefile and grab only the failure times
date_iter_csv = pd.read_csv('train_date.csv',
                            iterator = True,
                            chunksize = 1000)
                        
faildatedf = pd.concat([chunk[chunk.index.isin(indexfail)] 
                        for chunk in date_iter_csv])

train_profile = pd.Series()
for col in list(dates):
    current = dates[col].copy()
    current.dropna(inplace = True)
    train_profile = train_profile.append(current)
train_profile.drop_duplicates(inplace = True)
train_profile.plot(kind = 'hist')

fail_profile = pd.Series()
for col in list(faildatedf):
    current = faildatedf[col].copy()
    current.dropna(inplace = True)
    fail_profile = fail_profile.append(current)
fail_profile.drop_duplicates(inplace = True)
fail_profile.plot(kind = 'hist')



