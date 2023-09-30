import os
import numpy as np
import pandas as pd
import argparse

from sklearn.model_selection import train_test_split

df = pd.read_csv("data/diabetes.csv")
train,val_test=train_test_split(df, test_size=0.4, random_state=42)
val,test=train_test_split(val_test, test_size=0.5, random_state=42)
train.to_csv("data/train.csv", index=False)
val.to_csv("data/val.csv", index=False)
test.to_csv("data/test.csv", index=False)
