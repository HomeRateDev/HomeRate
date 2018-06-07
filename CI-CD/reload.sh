#!/bin/sh
cd ..
source ../.env/bin/activate
yes | pip install -r requirements.txt
cd homerate
git pull origin master
python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
supervisorctl restart homerate
