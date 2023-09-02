#!/bin/bash
cmd=$1
IMAGE_NAME="model_serving"
IMAGE_TAG="latest"

if [[ -z "$cmd" ]]; then
    echo "Missing command"
    exit 1
fi

run_model_serving(){
    # port=$1
    # if [[ -z "$port" ]]; then
    #     echo "missing port"
    #     exit 1
    # fi
    #build image
    docker build -f deployment/model_serving/Dockerfile -t $IMAGE_NAME:$IMAGE_TAG .
    IMAGE_NAME=$IMAGE_NAME IMAGE_TAG=$IMAGE_TAG docker compose -f deployment/model_serving/docker-compose.yml up -d
}
shift

case "$cmd" in
    run_model_serving)
        run_model_serving "$@"
        ;;
    *)
        echo "unknown command"
        exit 1
esac
