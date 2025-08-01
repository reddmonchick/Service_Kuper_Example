#!/bin/sh

set -e

# Ждем доступности БД
echo "Waiting for database..."
while ! nc -z db ${DB_PORT:-5432}; do
  sleep 0.5
done
echo "Database is ready!"

# Устанавливаем приложение (если нужно)
echo "Installing application..."
poetry install --only-root --no-interaction

# Применяем миграции
echo "Applying database migrations..."
alembic upgrade head

# Запускаем приложение
echo "Starting application..."
exec "$@"