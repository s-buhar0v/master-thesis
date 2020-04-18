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

function rebuild_cron_image() {
    local image_name=$1
    local python_script_name=$2
    containers=$(docker ps -a -q --filter ancestor=${image_name} --format="{{.ID}}")

    if [ ! -z $containers ]; then
        docker rm -f ${containers}
    fi

    docker rmi -f ${image_name} || echo "No image ${image_name}"
    docker build -t ${image_name} \
        -f "${PROJECT_PATH}/cron.Dockerfile" \
        --build-arg PYTHON_SCRIPT_NAME=${python_script_name} \
        ${PROJECT_PATH}
}

while getopts ":e:p:" option; do
    case "${option}" in
    e) ENVIRONMET=${OPTARG} ;;
    p) PROJECT_PATH=${OPTARG} ;;
    esac
done

source ${PROJECT_PATH}/deployscripts/_constants.sh

INIT_IMAGE="${PROJECT_NAME}/${INIT_APP_NAME}:latest"
EXPORTER_IMAGE="${PROJECT_NAME}/${EXPORTER_APP_NAME}:latest"
ANALYTICSAPI_IMAGE="${PROJECT_NAME}/${ANALYTICSAPI_APP_NAME}:latest"

METRICSPRECALCULATION_IMAGE="${PROJECT_NAME}/${METRICSPRECALCULATION_APP_NAME}:latest"
ANALYTICSPRECALCULATION_IMAGE="${PROJECT_NAME}/${ANALYTICSPRECALCULATION_APP_NAME}:latest"
POSTCOLLECTOR_IMAGE="${PROJECT_NAME}/${POSTCOLLECTOR_APP_NAME}:latest"
POSTACTUALIZER_IMAGE="${PROJECT_NAME}/${POSTACTUALIZER_APP_NAME}:latest"
USEDATACOLLECTOR_IMAGE="${PROJECT_NAME}/${USEDATACOLLECTOR_APP_NAME}:latest"

rebuild_image ${INIT_IMAGE} ${PROJECT_PATH}/init.Dockerfile
rebuild_image ${EXPORTER_IMAGE} ${PROJECT_PATH}/metricsexporter.Dockerfile
rebuild_image ${ANALYTICSAPI_IMAGE} ${PROJECT_PATH}/analyticsapi.Dockerfile

rebuild_cron_image ${METRICSPRECALCULATION_IMAGE} ${METRICSPRECALCULATION_APP_NAME}
rebuild_cron_image ${ANALYTICSPRECALCULATION_IMAGE} ${ANALYTICSPRECALCULATION_APP_NAME}
rebuild_cron_image ${POSTCOLLECTOR_IMAGE} ${POSTCOLLECTOR_APP_NAME}
rebuild_cron_image ${POSTACTUALIZER_IMAGE} ${POSTACTUALIZER_APP_NAME}
rebuild_cron_image ${USEDATACOLLECTOR_IMAGE} ${USEDATACOLLECTOR_APP_NAME}