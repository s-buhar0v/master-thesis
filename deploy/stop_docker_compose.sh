set -eu

DOCKER_COMPOSE_PATH="/app/master-thesis/docker-compose.yml"

if [ -f ${DOCKER_COMPOSE_PATH} ]; then
    docker-compose -f ${DOCKER_COMPOSE_PATH} down
fi