#!/bin/sh
# Applies migrations and seeds roles + the admin user before starting the API.
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Seeding roles and admin user..."
python -m app.initial_data

exec "$@"
