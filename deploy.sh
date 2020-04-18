set -eu

ansible-playbook -i ./deploy/inventory.yml ./deploy/deploy.yml