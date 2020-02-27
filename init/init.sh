set -eu

NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'

DATASOURCE_NAME="Operational"
DASHBOARD_UID="b5V2idQZk"
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


printf "${RED}# Delete unknown dashboard ...\n${NC}"

curl -sS -w "\n" -X DELETE ${GRAFANA_BASE_URL}/dashboards/uid/${DASHBOARD_UID} \
    -u admin:admin \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json'

printf "${GREEN}# Add dashboard ...\n${NC}"

dashboard_id=$(curl -sS -w "\n" -X POST ${GRAFANA_BASE_URL}/dashboards/db \
    -u admin:admin \
    -d @operation-dashboard.json \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json' | jq -r '.id')


curl -sS -w "\n" -X PUT ${GRAFANA_BASE_URL}/org/preferences \
    -u admin:admin \
    -d $(cat ./org-preferences.json | jq -c ".homeDashboardId = ${dashboard_id}") \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json'
