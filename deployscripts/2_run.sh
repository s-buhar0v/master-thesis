set -eu

while getopts ":e:p:" option; do
    case "${option}" in
    e) ENVIRONMET=${OPTARG} ;;
    p) PROJECT_PATH=${OPTARG} ;;
    esac
done

PROJECT_NAME="master-thesis"
DOCKER_COMPOSE_PATH="${PROJECT_PATH}/docker-compose.${ENVIRONMET}.yml"


if [ "${ENVIRONMET}" == "prod" ]; then
    docker-compose -f "${DOCKER_COMPOSE_PATH}" -p "${PROJECT_NAME}" up -d
else
    docker-compose -f "${DOCKER_COMPOSE_PATH}" -p "${PROJECT_NAME}" up
fi
