#!/bin/bash
cd /studypal

EXPOSE 8000

echo "----- Collect static files ------ " 
python manage.py collectstatic --noinput

echo "----- create super ------ " 
python manage.py migrate

echo "----- create super ------ " 
python create_user.py

echo "-----------Apply migration--------- "

python manage.py makemigrations 

python manage.py migrate --noinput  

echo "-----------Run django local server--------- "
python manage.py runserver 0.0.0.0:8000