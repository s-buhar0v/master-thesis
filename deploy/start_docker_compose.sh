set -eu

PROJECT_NAME="master-thesis"
PROJECT_PATH="/app/master-thesis/"
DOCKER_COMPOSE_PATH="${PROJECT_PATH}/docker-compose.prod.yml"

docker rmi -f sbukhar0v/master-thesis-init:latest
docker rmi -f sbukhar0v/master-thesis-metricsexporter:latest

docker build -t sbukhar0v/master-thesis-init:latest \
    -f "${PROJECT_PATH}/init.Dockerfile" ${PROJECT_PATH}
docker build -t sbukhar0v/master-thesis-metricsexporter:latest \
    -f "${PROJECT_PATH}/metricsexporter.Dockerfile" ${PROJECT_PATH}

docker-compose -f "${DOCKER_COMPOSE_PATH}" -p "${PROJECT_NAME}" up -d