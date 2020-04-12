from flask import Flask
import os
import pymongo


app = Flask(__name__, static_folder='static')
client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])
db = client.masterthesis
metrics = db.metrics


@app.route('/analyze')
def analyze():
    return {}

