FROM python:3.7-slim

ARG PYTHON_SCRIPT_NAME

ENV PYTHONPATH=$PYTHONPATH:$(pwd)

COPY ./jobs/${PYTHON_SCRIPT_NAME}.py /app/${PYTHON_SCRIPT_NAME}.py
ADD ./socialmonitor /app/socialmonitor
COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV VK_API_ACCESS_TOKEN="d3006a9ed3006a9ed3006a9e64d36aa244dd300d3006a9e8d8a76b1127efc4988386342"
ENV MONGO_DB_CONNECTION_STRING="mongodb+srv://developer:38ea0b9d@master-thesis-kwsx7.azure.mongodb.net/masterthesis?retryWrites=true&w=majority"
ENV PYTHON_SCRIPT_NAME=$PYTHON_SCRIPT_NAME

CMD python3 /app/${PYTHON_SCRIPT_NAME}.py
