set -eu

function rebuild_image() {
    local image_name=$1
    local dockerfile_path=$2
    containers=$(docker ps -a -q --filter ancestor=${image_name} --format="{{.ID}}")

    if [ ! -z $containers ]; then
        docker rm -f ${containers}
    fi

    docker rmi -f ${image_name} || echo "No image ${image_name}"
    docker build -t ${image_name} -f ${dockerfile_path} ${PROJECT_PATH}
}

while getopts ":e:p:" option; do
    case "${option}" in
    e) ENVIRONMET=${OPTARG} ;;
    p) PROJECT_PATH=${OPTARG} ;;
    esac
done

PROJECT_NAME="master-thesis"

# docker-compose images
INIT_IMAGE="master-thesis/init:latest"
EXPORTER_IMAGE="master-thesis/metricsexporter:latest"

# cron images
METRICPRECALCULATION_IMAGE="master-thesis/metricprecalculation:latest"
POSTCOLLECTOR_IMAGE="master-thesis/postcollector:latest"
POSTACTUALIZER_IMAGE="master-thesis/postactualizer:latest"

rebuild_image ${INIT_IMAGE} ${PROJECT_PATH}/init.Dockerfile
rebuild_image ${EXPORTER_IMAGE} ${PROJECT_PATH}/metricsexporter.Dockerfile
rebuild_image ${METRICPRECALCULATION_IMAGE} ${PROJECT_PATH}/metricsprecalculation.Dockerfile
rebuild_image ${POSTCOLLECTOR_IMAGE} ${PROJECT_PATH}/postcollector.Dockerfile
rebuild_image ${POSTACTUALIZER_IMAGE} ${PROJECT_PATH}/postactualizer.Dockerfile