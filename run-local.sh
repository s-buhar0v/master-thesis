set -eu

ENVIRONMENT="dev"
./deployscripts/1_build.sh -e ${ENVIRONMENT} -p $(pwd)
./deployscripts/2_run.sh -e ${ENVIRONMENT} -p $(pwd)