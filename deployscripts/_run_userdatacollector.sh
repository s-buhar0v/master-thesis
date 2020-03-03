#!/bin/bash

set -eu

PROJECT_PATH=${1}
USEDATACOLLECTOR_IMAGE="master-thesis/userdatacollector:latest"

if [ ! -f "${PROJECT_PATH}/userdatacollector.log" ]; then
  touch "${PROJECT_PATH}/userdatacollector.log"
fi

docker run --name master-thesis-metricprecalculation --rm ${USEDATACOLLECTOR_IMAGE} >> "${PROJECT_PATH}/userdatacollector.log"