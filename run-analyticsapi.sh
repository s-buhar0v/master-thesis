set -eu

#MONGO_DB_CONNECTION_STRING='mongodb+srv://developer:38ea0b9d@master-thesis-kwsx7.azure.mongodb.net/masterthesis?retryWrites=true&w=majority'
MONGO_DB_CONNECTION_STRING='mongodb+srv://developer:38ea0b9d@local-development-2qesi.azure.mongodb.net/masterthesis?retryWrites=true&w=majority'

docker run -it -w /app \
    -v $(pwd):/app \
    -e MONGO_DB_CONNECTION_STRING=$MONGO_DB_CONNECTION_STRING \
    -e FLASK_APP=/app/analyticsapi/main.py \
    -p 5000:5000 \
    python:3 \
    /bin/bash