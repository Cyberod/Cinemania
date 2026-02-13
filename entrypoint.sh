#!/bin/bash

set -e

echo "Running Django migrations..."
cd /app/cinemania
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
cd /app

# Use PORT environment variable from Render (defaults to 8000)
PORT=${PORT:-8000}

# Run gunicorn with proper settings
gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --worker-class sync \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    cinemania.wsgi:application
