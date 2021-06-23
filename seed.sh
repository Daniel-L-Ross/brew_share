#!/bin/bash
rm -rf brew_shareapi/migrations
rm db.sqlite3
python manage.py makemigrations brew_shareapi
python manage.py migrate
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata brewer
python3 manage.py loaddata brewmethods
python3 manage.py loaddata coffee
python3 manage.py loaddata entries
python3 manage.py loaddata entryreports
python3 manage.py loaddata entrysteps
python3 manage.py loaddata favoriteentries