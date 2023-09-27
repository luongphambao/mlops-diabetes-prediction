FROM python:3.9-slim

RUN apt-get update
RUN apt-get install libgomp1
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY deployment/model_serving/requirements.txt .
COPY ./src /serving/src
copy ./models /serving/models
COPY ./config /serving/config
RUN pip install --upgrade wheel setuptools pip
RUN pip install -r requirements.txt

# COPY predict.sh /serving/predict.sh
WORKDIR /serving
