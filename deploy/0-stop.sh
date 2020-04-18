set -eu

while getopts ":e:p:" option; do
    case "${option}" in
    e) ENVIRONMET=${OPTARG} ;;
    p) PROJECT_PATH=${OPTARG} ;;
    esac
done

PROJECT_NAME="master-thesis"
DOCKER_COMPOSE_PATH="${PROJECT_PATH}/docker-compose.${ENVIRONMET}.yml"

if [ -f ${DOCKER_COMPOSE_PATH} ]; then
    docker-compose -f ${DOCKER_COMPOSE_PATH} down
fi