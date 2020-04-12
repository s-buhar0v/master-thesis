import os
import pymongo

from flask import Flask, jsonify

app = Flask(__name__, static_folder='static')
client = pymongo.MongoClient(os.environ['MONGO_DB_CONNECTION_STRING'])


@app.route('/api/analyze')
def analyze():

    analytics = client.masterthesis.analytics.find_one({})
    return jsonify({k: v for k, v in analytics.items() if k != '_id'}), 200
