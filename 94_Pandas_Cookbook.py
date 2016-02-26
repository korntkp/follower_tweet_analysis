"""
http://pandas.pydata.org/pandas-docs/version/0.15.2/tutorials.html
"""

# %matplotlib inline
# Import all libraries needed for the tutorial

# General syntax to import specific functions in a library:
##from (library) import (specific library function)
from pandas import DataFrame, read_csv

# General syntax to import a library but no functions:
##import (library) as (give the library a nickname/alias)
import matplotlib.pyplot as plt
import pandas as pd #this is how I usually import pandas
import sys #only needed to determine Python version number
import matplotlib #only needed to determine Matplotlib version number

# Enable inline plotting
# %matplotlib inline

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)
print("=====================")

# # The inital set of baby names and bith rates
# names = ['Bob', 'Jessica', 'Mary', 'John', 'Mel']
# births = [968, 155, 77, 578, 973]
#
# BabyDataSet = list(zip(names, births))
# print(BabyDataSet)
# print("=====================")
#
# df = pd.DataFrame(data=BabyDataSet, columns=['Names', 'Births'])
# print(df)
# print("=====================")
#
# df.to_csv('births1880.csv', index=False, header=False)

Location = r'births1880.csv'
df = pd.read_csv(Location, header=None)
print(df)

