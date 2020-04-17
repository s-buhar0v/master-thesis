FROM python:3.7-slim

ENV FLASK_APP=/app/analyticsapi/main.py

ADD ./analyticsapi /app/analyticsapi
ADD ./socialmonitor /app/socialmonitor

COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD flask run --host=0.0.0.0