import argparse
import logging
import time

import joblib
import pandas as pd
import uvicorn
from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel

from config import Config

PREDICTOR_API_PORT = Config.PREDICTOR_API_PORT


class Data(BaseModel):
    data: list
    id: str
    columns: list


class ModelPredictor:
    def __init__(self, config_file_path):
        self.model = joblib.load("models/diabetes_model.pkl")
        self.scaler = joblib.load("models/scaler.pkl")
        logging.info("scaler loaded")
        logging.info("model loaded")

    def predict(self, data: Data):
        start_time = time.time()
        # df=pd.DataFrame(data.data)
        # convert to numpy array
        df = pd.DataFrame(data.data, columns=data.columns)
        end_convertdf = time.time()
        logger.info(f"convert df time: {end_convertdf-start_time}")
        # df=df.to_numpy()
        df = self.scaler.transform(df)
        end_scaler = time.time()
        logger.info(f"scaler time: {end_scaler-end_convertdf}")
        y_pred = self.model.predict(df)
        end_pred = time.time()
        logger.info(f"predict time: {end_pred-end_scaler}")
        return {
            "id": data.id,
            "predictions": y_pred.tolist(),
        }


class ServingAPI:
    def __init__(self, predictor: ModelPredictor):
        self.predictor = predictor
        self.app = FastAPI()

        @self.app.get("/")
        async def root():
            logger.info("hello")
            return {"message": "hello"}

        @self.app.post("/predict")
        async def predict(data: Data):
            """
            Example request:
            {
            "id": "123",
            "data": [[6,148,72,35,0,33.6,0.627,50]],
            "columns": ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"]
            }
            """
            return self.predictor.predict(data)

    def run(self, port):
        logger.info("instrument app")
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
