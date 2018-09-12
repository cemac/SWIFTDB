#!/bin/bash

initdb -D ~/postgresql_datar/
wait
postgres -D ~/postgresql_data/ &
wait
python manage.py db upgrade
wait
python manage.py runserver