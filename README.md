# diabetes_prediction_mlops

Final Project for MLE1 Course

In this project, I learn how to use most popular MLOPS tool to build a pipeline for model serving and CI/CD pipeline
Tech stack i used in this project:
- MLFlow: Model registry, artifact store

- FastAPI: model serving

- Prometheus,Cadvisor: metrics collector

- Grafana: metrics visualization

- Jaeger: tracing

- ElasticSearch, Logstash, Kibana: logs collector and analysis

- Locust: load test for model serving

- Docker,Docker-compose: containerization

- Kubernetes,Helm: container orchestration
- Jenkins: CI/CD pipeline

- Github: source version control

- Cloud service: Google Kubernetes Engine

- Infrastructure as code: Terraform,Ansible

## System Architecture
![](images/mle1_final1.png)

##   Training
```bash
$make mlflow_up
$python3 src/data_split.py #prepare data
$python3 src/train.py --model_name xgb
```

## Start local service
```bash
$make mlflow_up #start mlflow server
$make elk_up    #start logs collector
$make monitoring_up #start monitoring service(prometheus, grafana,jaeger)
$make predictor_up #start predictor service
```
Access to `localhost:8000/docs` for testing api

Access to `localhost:5601` for logs kibana search

Access to `localhost:3000` for grafana dashboard

Access to `localhost:16686` for jaeger tracing

Access to `localhost:9090` for prometheus
### Load test system
```bash
$locust -f locustfile.py
#localhost:8089
```
You can see dashboard for performance testing in grafana and tracing in jaeger
### Cloud Service
You can see `README_cloud.md` for details setup and deploy to cloud service(GKE )  model serving and CI/CD pipeline
