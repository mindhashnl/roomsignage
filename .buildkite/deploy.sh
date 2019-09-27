#!/bin/sh

docker build -t mysign . # Build

cd /proj
docker-compose run --rm web python3 manage.py migrate # Run migrations
docker-compose up -d web # Restart