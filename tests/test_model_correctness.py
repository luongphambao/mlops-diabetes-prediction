import logging
import time

import joblib
import numpy as np
import pandas as pd
import yaml

MODEL_DIR = "models"


def test_model_correctness():
    scaler = joblib.load(f"{MODEL_DIR}/scaler.pkl")
    clf = joblib.load(f"{MODEL_DIR}/diabetes_model.pkl")
    data = [
        -1.15332192,
        -0.05564105,
        0.12035144,
        -1.25882277,
        -1.08285125,
        -0.28446352,
        -0.49468374,
        -0.52559768,
    ]
    x = np.array(data).reshape(-1, 8)
    x = scaler.transform(x)
    pred = clf.predict(x)[0]
    assert pred == 0
