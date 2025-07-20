#!/bin/bash

# Exit on any failure
set -e

echo "Starting HiTech Clan E-Commerce Platform..."

# Wait for database to be ready
echo "Waiting for database..."
python << END
import os
import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_db():
    db_conn = None
    while not db_conn:
        try:
            db_conn = psycopg2.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                port=os.environ.get('DB_PORT', '5432'),
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASSWORD', ''),
                database=os.environ.get('DB_NAME', 'hitech_store')
            )
        except OperationalError:
            print('Database unavailable, waiting 1 second...')
            time.sleep(1)
    
    print('Database available!')
    db_conn.close()

# Only wait for PostgreSQL if we're using it
if os.environ.get('DB_ENGINE', '').endswith('postgresql'):
    wait_for_db()
END

echo "Database is ready!"

# Run database migrations
echo "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Creating superuser if it doesn't exist..."
python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@hitechclan.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully!')
else:
    print(f'Superuser {username} already exists.')
END

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting application..."

# Execute the main command
exec "$@"