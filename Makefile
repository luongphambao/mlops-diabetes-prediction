# mlflow
mlflow_up:
	docker compose -f deployment/mlflow/docker-compose.yml up -d
mlflow_down:
	docker compose -f deployment/mlflow/docker-compose.yml down