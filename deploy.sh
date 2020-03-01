set -eu

ansible-playbook -i ./deployscripts/inventory.yml ./deployscripts/deploy.yml