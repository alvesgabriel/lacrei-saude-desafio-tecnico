#!/bin/sh

# Run database migrations
poetry run python manage.py migrate --noinput

# Start app
gunicorn --bind 0.0.0.0:8000 --workers 3 lacrei.wsgi
