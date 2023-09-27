FROM python:3.9

# Create a folder /app if it doesn't exist,
# the /app folder is the current working directory
WORKDIR /app


COPY ./requirements.txt /app

COPY ./models /app/models
COPY ./src/config.py /app
# Copy necessary files to our app
COPY ./src/api.py /app

LABEL maintainer="luongphambao"

EXPOSE 30000

# Disable pip cache to shrink the image size a little bit,
# since it does not need to be re-installed
RUN pip install -r requirements.txt --no-cache-dir

CMD ["python3","api.py","--port","30000"]
