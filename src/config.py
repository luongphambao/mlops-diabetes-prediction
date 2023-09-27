import logging
import os
from pathlib import Path

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


class Config:
    MLFLOW_URI = os.environ.get("MLFLOW_TRACKING_URI")
    PREDICTOR_API_PORT = 8000
