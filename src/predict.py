import pandas as pd 
import numpy as np
import yaml
import logging
import mlflow
import os 
import time
import joblib
from config import Config
class ModelPredictor:
    def __init__(self, config_file_path):
        with open(config_file_path, "r") as f:
            self.config = yaml.safe_load(f)
            print(self.config)
            print("load config")
        logging.info(f"model-config: {self.config}")
        mlflow.set_tracking_uri(Config.MLFLOW_URI )
        model_uri = os.path.join(
            "models:/", self.config["model_name"], str(self.config["model_version"])
        )
        self.model = mlflow.sklearn.load_model(model_uri)
        logging.info(f"model loaded from {model_uri}")
        joblib.dump(self.model, open("models/diabetes_model.pkl", 'wb'))
        logging.info(f"model saved successfully")
        self.scaler=joblib.load("models/scaler.pkl")
        logging.info("scaler loaded")
    def predict(self,df:np.ndarray):
        start_time = time.time()
        df = self.scaler.transform(df)
        y_pred=self.model.predict(df)
        end_pred = time.time()
        logging.info(f"predict time: {end_pred-start_time}")
        return y_pred
    
if __name__ == "__main__":
    val = pd.read_csv("data/val.csv")
    predictor = ModelPredictor("config/model.yaml")
    val_X = val.drop(columns=['Outcome'])
    val_y = val['Outcome']
    y_pred = predictor.predict(val_X)
    print(y_pred)