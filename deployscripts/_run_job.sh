#!/bin/bash

set -eu

PROJECT_PATH=${1}
IMAGE_NAME=${2}

source ${PROJECT_PATH}/deployscripts/_constants.sh

IMAGE_FULL_NAME="${PROJECT_NAME}/${IMAGE_NAME}:latest"

if [ ! -f "${PROJECT_PATH}/${IMAGE_NAME}.log" ]; then
  touch "${PROJECT_PATH}/${IMAGE_NAME}.log"
fi

docker run --name master-thesis-metricsprecalculation --rm ${IMAGE_FULL_NAME} >> "${PROJECT_PATH}/${IMAGE_NAME}.log"