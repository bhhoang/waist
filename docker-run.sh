#!/bin/bash

echo "Do you want to use a remote PostgreSQL database? (y/n)"
read -r USE_REMOTE

if [ "$USE_REMOTE" = "y" ]; then
  echo "Enter your remote DATABASE_URL (e.g. postgresql://user:pass@host:port/dbname):"
  read -r REMOTE_DB_URL

  export DATABASE_URL=$REMOTE_DB_URL

  echo "Using remote DB: $DATABASE_URL"
  docker-compose -f docker-compose.yml up --build
else
  export DATABASE_URL=postgresql://postgres:postgres@database:5432/postgres

  echo "Using local Postgres DB at: $DATABASE_URL"
  docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build
fi
