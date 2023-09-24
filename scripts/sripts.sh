 docker run -d --restart=always -p 8080:80 image_name:version
 docker run -p 30000:30000 luongphambao/model_serving
 docker compose -f jenkins/docker-compose.yaml up -d
 docker build -t luongphambao/model_serving .
 k port-forward svc/diabetes 30002:30000 -n model-serving