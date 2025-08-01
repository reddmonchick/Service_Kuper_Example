#!/bin/sh

set -e


echo "Waiting for database..."
while ! nc -z db ${DB_PORT:-5432}; do
  sleep 0.5
done
echo "Database is ready!"


echo "Installing application..."
poetry install --only-root --no-interaction


echo "Applying database migrations..."
alembic upgrade head


echo "Starting application..."
exec "$@"