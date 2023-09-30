import argparse
import logging
import pickle
import time

import joblib
import numpy as np
import pandas as pd
import uvicorn
import yaml
from fastapi import FastAPI, Request
from loguru import logger
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from prometheus_client import start_http_server
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

from config import Config

PREDICTOR_API_PORT = Config.PREDICTOR_API_PORT


start_http_server(port=8099, addr="0.0.0.0")

set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "model_serving_manual"}))
)
tracer = get_tracer_provider().get_tracer("model_serving", "0.1.0")

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
get_tracer_provider().add_span_processor(span_processor)


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
        self.model = joblib.load("models/diabetes_model.pkl")
        self.scaler = joblib.load("models/scaler.pkl")
        logging.info("scaler loaded")
        logging.info("model loaded")

    def predict(self, data: Data):
        with tracer.start_as_current_span("processors") as processors:
            with tracer.start_as_current_span(
                "convert dataframe", links=[trace.Link(processors.get_span_context())]
            ):
                start_time = time.time()
                df = pd.DataFrame(data.data, columns=data.columns)
                end_convertdf = time.time()
                logger.info(f"convert df time: {end_convertdf-start_time}")
            with tracer.start_as_current_span(
                "transform", links=[trace.Link(processors.get_span_context())]
            ):
                df = self.scaler.transform(df)
                end_scaler = time.time()
                logger.info(f"scaler time: {end_scaler-end_convertdf}")
            with tracer.start_as_current_span(
                "model predict", links=[trace.Link(processors.get_span_context())]
            ):
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
            {
            "id": "123",
            "data": [[6,148,72,35,0,33.6,0.627,50]],
            "columns": ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"]
            }
            Output:
            {
            "id": "123",
            "predictions": [1]
            }
            """
            return self.predictor.predict(data)

    def run(self, port):
        Instrumentator().instrument(app=self.app).expose(app=self.app)
        # tracer = get_tracer_provider().get_tracer("model_serving", "0.1.0")
        FastAPIInstrumentor.instrument_app(self.app, excluded_urls="/metrics")

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
