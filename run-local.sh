set -eu

ENVIRONMENT="dev"
./deploy/1-build.sh -e ${ENVIRONMENT} -p $(pwd)
./deploy/2-run.sh -e ${ENVIRONMENT} -p $(pwd)