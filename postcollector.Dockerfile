FROM python:3.7-slim

ENV FLASK_APP=/app/metricsexporter/main.py

ADD ./metricsexporter /app/metricsexporter
ADD ./socialmonitor /app/socialmonitor

COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD flask run --host=0.0.0.0