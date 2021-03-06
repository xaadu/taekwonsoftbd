#!/bin/bash

set -e

python manage.py makemigrations
python manage.py migrate

if [ "$DEBUG" = "FALSE" ]
then
    python manage.py collectstatic --noinput
    uwsgi --socket :8000 --master --enable-threads --module taekwonsoftbd.wsgi
else
    python manage.py runserver 0.0.0.0:8000
fi
