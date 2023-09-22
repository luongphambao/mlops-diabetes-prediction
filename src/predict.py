import pandas as pd 
import numpy as np
import yaml
import logging
import mlflow
import os 
import time
import pickle
import joblib
from config import Config
class ModelPredictor:
    def __init__(self, config_file_path):
        with open(config_file_path, "r") as f:
            self.config = yaml.safe_load(f)
            print(self.config)
            print("load config")
        logging.info(f"model-config: {self.config}")
        self.model=joblib.load("models/diabetes_model.pkl")
        self.scaler=joblib.load("models/scaler.pkl")
        logging.info("scaler loaded")
    def predict(self,df:np.ndarray):
        start_time = time.time()
        df = self.scaler.transform(df)
        y_pred=self.model.predict(df)
        return y_pred
    
if __name__ == "__main__":
    val = pd.read_csv("data/val.csv")
    predictor = ModelPredictor("config/model.yaml")
    val_X = val.drop(columns=['Outcome'])
    val_y = val['Outcome']
    y_pred = predictor.predict(val_X)
    print(y_pred)