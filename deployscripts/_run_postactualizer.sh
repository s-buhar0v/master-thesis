#!/bin/bash

set -eu

PROJECT_PATH=${1}
POSTCOLLECTOR_IMAGE="master-thesis/postactualizer:latest"

if [ ! -f "${PROJECT_PATH}/postactualizer.log" ]; then
  touch "${PROJECT_PATH}/postactualizer.log"
fi

docker run --name master-thesis-postactualizer --rm ${POSTCOLLECTOR_IMAGE} >> "${PROJECT_PATH}/postactualizer.log"