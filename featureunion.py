
# coding: utf-8

# In[1]:
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from numpy import ravel
from xgboost import XGBClassifier
from sklearn import linear_model, decomposition
from sklearn.pipeline import Pipeline, FeatureUnion
import numpy
import os
import matplotlib.pyplot as plt
# I call numpy thorugh pandas since pandas contains all of numpy


# In[2]:

# Only run this if you're on dave's machine
#os.chdir("../../")
scriptpath = ""

class regular(BaseEstimator, TransformerMixin):
    #return itself
    def fit(self, x, y=None):
        return self
    
    def transform(self, X):
        print(X.shape)
        return X


class absvalue(BaseEstimator, TransformerMixin):
    #return itself
    def fit(self, x, y=None):
        return self
    
    def transform(self, X, **transform_params):
        toreturn = X.abs()
        print(toreturn.shape)
        return toreturn

class numnon(BaseEstimator, TransformerMixin):
    #return itself
    def fit(self, x, y=None):
        return self
    
    def transform(self, X, **transform_params):
        toreturn = X
        toreturn = pd.DataFrame(toreturn[toreturn != 9999].count(axis = 1))
        print(toreturn.shape)
#        toreturn = pd.DataFrame({'Id':X.Id,'numnon':toreturn})
        return toreturn
        
# In[3]:

# import some testing data

dates = pd.read_csv('train_date.csv', nrows = 5000)
numeric = pd.read_csv('train_numeric.csv', nrows = 10000)
test = pd.read_csv('train_numeric.csv', nrows = 10000, header = 1,
                   skiprows = 106000)
test.columns = numeric.columns
comp = test.Response
test.drop('Response', axis = 1, inplace = True)
categorical = pd.read_csv('train_categorical.csv', nrows = 5000)
base = pd.read_csv("train_numeric.csv", usecols = ['Id','Response'])
fTest = test.fillna(value = 9999)

#%%

# import precalculated data

predate = pd.read_csv("gitcode/bosch.fail_date_score.csv")
onecol = pd.merge(predate, numer)

# In[15]:

# Build a dataframe to predict on
features = numeric.drop('Response', axis = 1)
fFeatures = features.fillna(value=9999)
proto = pd.merge(base,features, on='Id')
target = numeric.loc[:,['Response']]


# In[11]:
    
union = FeatureUnion([('first', regular()),  
                      ('second', absvalue()),
                      ('numnonNAvals',numnon())])

pipe = Pipeline([('union',union),
                 ('linear',XGBClassifier(base_score=0.55, seed=24))])
pipe.fit(fFeatures, target)
y = pipe.predict(fTest)

#clf = XGBClassifier(base_score=0.005, seed=24)
#clf.fit(X, y)

#%%
result = pd.Series(y == comp.values)
print(sum(y),sum(comp),sum(result))
fails = result[result == False].index
print(len(fails))

#%%
# this is the previous method, probably do not run
dumbpipe = Pipeline([('linear',linear_model.logistic.LogisticRegression(random_state = 37))])
dumbpipe.fit(fFeatures.abs(),target)
dumby = dumbpipe.predict(fTest)
dumbresult = pd.Series(dumby == comp.values)
print(sum(dumby),sum(comp),sum(dumbresult))
dumbfails = dumbresult[dumbresult == False].index
print(len(dumbfails))
# In[21]:

print(pca.components_)

