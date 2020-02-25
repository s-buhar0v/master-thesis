set -eu

NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'

DATASOURCE_NAME="Operational"
GRAFANA_BASE_URL="grafana:3000/api"

datasources=$(curl -sS -w "\n" -X GET ${GRAFANA_BASE_URL}/datasources \
    -u admin:admin \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' | jq '.[].id')

for d in $datasources
do
    printf "${RED}# Delete unknown datasource with id ${d}...\n${NC}"
    curl -sS -w "\n" -X DELETE ${GRAFANA_BASE_URL}/datasources/${d} \
        -u admin:admin \
        -H 'Accept: application/json' \
        -H 'Content-Type: application/json' | jq -r '.message'
done

printf "${GREEN}# Add ${DATASOURCE_NAME} datasource ...\n${NC}"

curl -sS -w "\n" -X POST ${GRAFANA_BASE_URL}/datasources \
    -u admin:admin \
    -d @operational-datasource.json \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' | jq -r '.message'

curl -sS -w "\n" -X POST ${GRAFANA_BASE_URL}/dashboards/db \
    -u admin:admin \
    -d @operation-dashboard.json \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' | jq -r '.message'
