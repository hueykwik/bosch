# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 12:46:30 2016
Dave plays around with Bosch data
@author: Dave
"""

import pandas as pd
import os

dates = pd.read_csv('train_date.csv',
                    nrows = 10000, 
                    index_col = 0, 
                    dtype = pd.np.float64,)
                    
numeric = pd.read_csv('train_numeric.csv',
                    nrows = 10000, 
                    index_col = 0, 
                    dtype = pd.np.float32,)
