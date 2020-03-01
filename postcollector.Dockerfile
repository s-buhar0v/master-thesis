FROM python:3.7-slim

ENV PYTHONPATH=$PYTHONPATH:$(pwd)

COPY ./jobs/postcollector.py /app/postcollector.py
ADD ./socialmonitor /app/socialmonitor

COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV VK_API_ACCESS_TOKEN="b9cd2c82b9cd2c82b9cd2c824bb9a7e458bb9cdb9cd2c82e5278cc0f74ee04dd7e93222"
ENV MONGO_DB_CONNECTION_STRING="mongodb+srv://master-thesis:38ea0b9d@master-thesis-8vbh1.azure.mongodb.net/social-networks?retryWrites=true&w=majority"

CMD python3 /app/postcollector.py
