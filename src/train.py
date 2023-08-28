import os as pd 
import pandas as pd
import numpy as np
import logging 
import mlflow
import argparse
import xgboost as xgb
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from lightgbm import LGBMClassifier
#import logistic regression
from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score,roc_auc_score


from config import Config


class ModelTrainer:
    
    EXPERIMENT_NAME=None
    @staticmethod
    def get_model(model_name):
        dict_model = {
            "xgb":xgb.XGBClassifier(),
            "svm": SVC(),
            "knn": KNeighborsClassifier(),
            "random_forest": RandomForestClassifier(),
            "mlp": MLPClassifier(),
            "ada_boost": AdaBoostClassifier(),
            "naive_bayes": GaussianNB(),
            "decision_tree": DecisionTreeClassifier(),
            "lightgbm": LGBMClassifier(),
            "logistic_regression": LogisticRegression(),
            

        }
        return  dict_model[model_name]
    @staticmethod 
    def train_model(model_name):
        ModelTrainer.EXPERIMENT_NAME = "diabetes_"+model_name
        logging.info(f"start training diates model {model_name}")
        
        #init mlflow experiment
        mlflow.set_tracking_url = Config.MLFLOW_URI
        mlflow.set_experiment(ModelTrainer.EXPERIMENT_NAME)
        
        #load data
        df_train=pd.read_csv("data/train.csv")
        df_test=pd.read_csv("data/test.csv")
        
        X_train = df_train.drop(columns=['Outcome'])
        y_train = df_train['Outcome']
        X_test = df_test.drop(columns=['Outcome'])
        y_test = df_test['Outcome']

        #scaler
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        #create model
        model = ModelTrainer.get_model(model_name)
        #training model
        model.fit(X_train, y_train)
        logging.info(f"model {model_name} is trained")
        y_pred = model.predict(X_test)

        #metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred)
        metrics = {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1, "roc_auc": roc_auc}
        logging.info(f"model {model_name} metrics: {metrics}")

        #mlflow logging
        mlflow.log_params(model.get_params())
        mlflow.log_metrics(metrics)
        signature = mlflow.models.infer_signature(X_test, y_pred)
        mlflow.sklearn.log_model(model, "model", signature=signature)
        mlflow.end_run()
        logging.info("finish training")

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--model_name",type=str,help="model name",default="xgb")
    args=parser.parse_args()
    ModelTrainer.train_model(args.model_name)

        