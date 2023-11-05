#!/bin/bash
set -e
set -o pipefail

work_dir="/opt/star_burger_docker"

source $work_dir"/backend/src/star_burger/.env"

cd $work_dir

git pull

docker compose -f $work_dir"/production/docker-compose-prod.yml" down
docker compose -f $work_dir"/production/docker-compose-prod.yml" up -d
docker exec -it production-app-1 python manage.py migrate --noinput

systemctl reload nginx.service

last_commit=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: ${ROLLBAR_ACCESS_TOKEN}" -H "Content-Type: application/json" -X POST "https://api.rollbar.com/api/1/deploy" -d '{"environment": "production", "revision": "'${last_commit}'", "rollbar_name": "leksus", "local_username": "root", "comment": "Yet Another Deployment", "status": "succeeded"}'

echo -e "\nstar-burger was successfully delployed"
