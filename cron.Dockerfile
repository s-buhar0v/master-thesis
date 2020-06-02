FROM python:3.7-slim

ARG PYTHON_SCRIPT_NAME

ENV PYTHONPATH=$PYTHONPATH:$(pwd)

COPY ./jobs/${PYTHON_SCRIPT_NAME}.py /app/${PYTHON_SCRIPT_NAME}.py
ADD ./socialmonitor /app/socialmonitor
COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV VK_API_ACCESS_TOKEN="ab8c9b34ab8c9b34ab8c9b3465abfec6a6aab8cab8c9b34f55ab94d61c856e04bf13408"
ENV MONGO_DB_CONNECTION_STRING="mongodb+srv://developer:38ea0b9d@master-thesis-kwsx7.azure.mongodb.net/masterthesis?retryWrites=true&w=majority"
ENV PYTHON_SCRIPT_NAME=$PYTHON_SCRIPT_NAME

CMD python3 /app/${PYTHON_SCRIPT_NAME}.py
