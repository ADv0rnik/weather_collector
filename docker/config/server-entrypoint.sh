#!/bin/sh

until cd /app/config
do
    echo "Waiting for server volume ..."
done


python manage.py runserver