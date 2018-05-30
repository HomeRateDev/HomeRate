#!/bin/sh
source .env/bin/activate
cd HomeRate/homerate
git pull origin master
python manage.py collectstatic --no-input
python manage.py migrate --no-input
supervisorctl restart homerate