# mlflow
mlflow_up:
	docker compose -f deployment/mlflow/docker-compose.yml up -d
mlflow_down:
	docker compose -f deployment/mlflow/docker-compose.yml down

monitoring_up:
	docker compose -f deployment/prom-graf-docker-compose.yaml up -d
monitoring_down:
	docker compose -f deployment/prom-graf-docker-compose.yaml down
elk_up:
	cd deployment/elk/ && docker compose -f elk-docker-compose.yml -f extensions/filebeat/filebeat-compose.yml up -d
elk_down:
	cd deployment/elk/
	docker compose -f elk-docker-compose.yml -f extensions/filebeat/filebeat-compose.yml down
