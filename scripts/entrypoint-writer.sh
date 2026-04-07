#!/bin/sh
set -e

echo "DB host: $TELEMETRY_DB_HOST"
echo "DB port: $TELEMETRY_DB_PORT"

echo "Waiting for PostgreSQL..."
until pg_isready -h "${TELEMETRY_DB_HOST}" -p "${TELEMETRY_DB_PORT}" -U "${TELEMETRY_DB_USER}"; do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is up"

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Starting command: $*"
exec "$@"