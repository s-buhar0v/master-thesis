set -eu

PROJECT_PATH="/app/master-thesis/"
DOCKER_COMPOSE_PATH="${PROJECT_PATH}/docker-compose.prod.yml"

if [ -f ${DOCKER_COMPOSE_PATH} ]; then
    docker-compose -f ${DOCKER_COMPOSE_PATH} down
fi