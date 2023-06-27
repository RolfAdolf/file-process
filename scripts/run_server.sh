#!/bin/bash

cd file_process

python3 manage.py makemigrations

python3 manage.py migrate

uwsgi --ini /code/config/uwsgi/uwsgi.ini
