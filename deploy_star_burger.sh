#!/bin/bash
set -e 
set -o pipefail

work_dir="/opt/star_burger"
python=$work_dir"/venv/bin/python"
pip=$work_dir"/venv/bin/pip"

source $work_dir"/star_burger/.env"

cd $work_dir
git pull

$pip install -r requirements.txt
$python manage.py collectstatic --noinput
$python manage.py migrate --noinput

npm ci --include=dev
export NODE_OPTIONS=--no-experimental-fetch
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
npm audit fix

systemctl restart star-burger.service

last_commit=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: ${ROLLBAR_ACCESS_TOKEN}" -H "Content-Type: application/json" -X POST "https://api.rollbar.com/api/1/deploy" -d '{"environment": "production", "revision": "'${last_commit}'", "rollbar_name": "leksus", "local_username": "root", "comment": "Yet Another Deployment", "status": "succeeded"}'

echo "star-burger was successfully delployed"
