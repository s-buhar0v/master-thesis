docker build -t sbukhar0v/master-thesis-init:latest -f init.Dockerfile .
docker build -t sbukhar0v/master-thesis-metricsexporter:latest -f metricsexporter.Dockerfile .

docker-compose up