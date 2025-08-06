@echo off
setlocal EnableDelayedExpansion

set "DATABASE_URL="

echo Do you want to use a remote PostgreSQL database? (y/n)
set /p USE_REMOTE=

if /i "%USE_REMOTE%"=="y" (
    call :getRemoteURL
    call docker-compose -f docker-compose.yml up --build
) else (
    set "DATABASE_URL=postgresql://postgres:postgres@database:5432/postgres"
    echo Using local Postgres DB at: !DATABASE_URL!
    call docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build
)

goto :eof

:getRemoteURL
echo Enter your remote DATABASE_URL (e.g. postgresql://user:pass@host:port/dbname):
set /p INPUT_URL=
set "DATABASE_URL=%INPUT_URL%"
echo Using remote DB: %DATABASE_URL%
goto :eof
