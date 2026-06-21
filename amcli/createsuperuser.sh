#!/bin/sh

cd work && env $(grep -v '^#' ../.env | xargs) python3 manage.py createsuperuser --noinput || true

cd ..

