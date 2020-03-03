FROM python:3.7-slim

ARG PYTHON_SCRIPT_NAME

ENV PYTHONPATH=$PYTHONPATH:$(pwd)

COPY ./jobs/${PYTHON_SCRIPT_NAME}.py /app/${PYTHON_SCRIPT_NAME}.py
ADD ./socialmonitor /app/socialmonitor
COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV VK_API_ACCESS_TOKEN="b9cd2c82b9cd2c82b9cd2c824bb9a7e458bb9cdb9cd2c82e5278cc0f74ee04dd7e93222"
ENV MONGO_DB_CONNECTION_STRING="mongodb+srv://master-thesis:38ea0b9d@masterthesis-8vbh1.azure.mongodb.net/masterthesis?retryWrites=true&w=majority"
ENV PYTHON_SCRIPT_NAME=$PYTHON_SCRIPT_NAME

CMD python3 /app/${PYTHON_SCRIPT_NAME}.py
