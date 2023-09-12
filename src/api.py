import os
import random
import time
import mlflow
import pandas as pd
import numpy as np 
import uvicorn
import logging 
import yaml
import pickle 
from fastapi import FastAPI, Request
from pydantic import BaseModel
import argparse
from loguru import logger
from config import Config

PREDICTOR_API_PORT = Config.PREDICTOR_API_PORT


class Data(BaseModel):
    data: list
    id: str
    columns: list
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
        #self.model = mlflow.pyfunc.load_model(model_uri)
        self.model = mlflow.sklearn.load_model(model_uri)
        logging.info(f"model loaded from {model_uri}")
        self.scaler=pickle.load(open("models/scaler.pkl","rb"))
        logging.info("scaler loaded")
    def predict(self,data:Data):

        start_time = time.time()
        #df=pd.DataFrame(data.data)
        #convert to numpy array
        df=pd.DataFrame(data.data,columns=data.columns)
        end_convertdf=time.time()
        logger.info(f"convert df time: {end_convertdf-start_time}")
        #df=df.to_numpy()
        df = self.scaler.transform(df)
        end_scaler=time.time()
        logger.info(f"scaler time: {end_scaler-end_convertdf}")
        y_pred=self.model.predict(df)
        end_pred=time.time()
        logger.info(f"predict time: {end_pred-end_scaler}")
        return{
            "id":data.id,
            "predictions":y_pred.tolist(),
        }
class ServingAPI:
    def __init__(self,predictor:ModelPredictor):
        self.predictor = predictor
        self.app = FastAPI()
        @self.app.get("/")
        async def root():
            return {"message": "hello"}

        @self.app.post("/predict")
        async def predict(data: Data):
            """
            {
            "id": "123",
            "data": [[6,148,72,35,0,33.6,0.627,50]],
            "columns": ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"]
            }
            """
            return self.predictor.predict(data)
    def run(self,port):
        from prometheus_fastapi_instrumentator import Instrumentator
        Instrumentator().instrument(self.app).expose(self.app)
        uvicorn.run(self.app, host="0.0.0.0", port=port)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    return args
if __name__ == "__main__":
    predictor = ModelPredictor("config/model.yaml")
    api = ServingAPI(predictor)
    PREDICTOR_API_PORT = parse_args().port
    api.run(PREDICTOR_API_PORT)
