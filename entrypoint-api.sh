#!/bin/bash
cd /usr/src/app
pip3 install -r requirements.txt
cd api
python3 manage.py runserver