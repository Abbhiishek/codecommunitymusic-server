#!/bin/sh
if [ ! -f /app/superuser_created ]; then
    python manage.py createsuperuser --noinput
    touch /app/superuser_created
fi
python manage.py makemigrations
python manage.py migrate
