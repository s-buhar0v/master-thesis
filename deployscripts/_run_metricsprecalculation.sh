#!/bin/bash

set -eu

PROJECT_PATH=${1}
METRICPRECALCULATION_IMAGE="master-thesis/metricprecalculation:latest"

if [ ! -f "${PROJECT_PATH}/metricsprecalculation.log" ]; then
  touch "${PROJECT_PATH}/metricsprecalculation.log"
fi

docker run --name master-thesis-metricprecalculation --rm ${METRICPRECALCULATION_IMAGE} >> "${PROJECT_PATH}/metricsprecalculation.log"