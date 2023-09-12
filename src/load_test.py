import json
from locust import HttpUser, TaskSet, task, between
import os 
import pandas as pd 
import random 
import json 
class ModelServingTest(TaskSet):
    @task
    def predict(self):
        headers = {'content-type': 'application/json'}
        
        id_data = os.listdir("requests")
        index=random.randint(0,len(id_data)-1)
        data=json.load(open("requests/"+id_data[index]))
        
        self.client.post("predict",json=data,headers=headers)


class LoadTest(HttpUser):
    tasks = [ModelServingTest]
    wait_time = between(0,1)
    host = "http://127.0.0.1:8000/"
    stop_timeout = 10