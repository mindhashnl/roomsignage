#!/bin/sh

docker build -t mysign . # Build

cd /proj
docker-compose run --rm web python3 manage.py migrate # Run migrations
docker-compose run --rm web -v ./static:/app/static python3 manage.py collectstatic --noinput # Collect static files, such that Nginx can serve
docker-compose up -d web # Restart