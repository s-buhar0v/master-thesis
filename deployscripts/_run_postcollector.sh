#!/bin/bash

set -eu

PROJECT_PATH=${1}
POSTCOLLECTOR_IMAGE="master-thesis/postcollector:latest"

if [ ! -f "${PROJECT_PATH}/postcollector.log" ]; then
  touch "${PROJECT_PATH}/postcollector.log"
fi

docker run -n master-thesis-postcollector -d -rm ${POSTCOLLECTOR_IMAGE}