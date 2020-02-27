ENV="dev"
DOCKER_COMPOSE_PATH="./docker-compose.${ENV}.yml"

function delete_containers_and_image() {
    local image_name=$1
    docker rm -f $(docker ps -a -q --filter ancestor=${image_name} --format="{{.ID}}")
    docker rmi -f ${image_name}
}

INIT_IMAGE="sbukhar0v/master-thesis-init:latest"
EXPORTER_IMAGE="sbukhar0v/master-thesis-metricsexporter:latest"

delete_containers_and_image ${INIT_IMAGE}
delete_containers_and_image ${EXPORTER_IMAGE}

docker build -t ${INIT_IMAGE} -f init.Dockerfile .
docker build -t ${EXPORTER_IMAGE} -f metricsexporter.Dockerfile .

docker-compose -f "${DOCKER_COMPOSE_PATH}" up