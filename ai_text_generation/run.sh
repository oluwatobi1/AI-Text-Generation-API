#!/bin/sh
echo "Applying database migrations..."
flask db upgrade


echo "Starting the app..."
gunicorn -b 0.0.0.0:5000 "app:create_app()"