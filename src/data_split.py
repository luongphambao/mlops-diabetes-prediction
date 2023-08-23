import os
import pandas as pd
import numpy as np
#import train_test_split
from sklearn.model_selection import train_test_split

df=pd.read_csv('data/diabetes.csv')

train,val=train_test_split(df,test_size=0.4,random_state=0)

#split validation data into validation and test data
val,test=train_test_split(val,test_size=0.5,random_state=0)

train.to_csv('data/train.csv',index=False)
val.to_csv('data/val.csv',index=False)
test.to_csv('data/test.csv',index=False)