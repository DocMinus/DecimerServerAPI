@echo off
set IMAGE_NAME=decimer_api

echo.
echo ------------------------------------
echo Starting the Docker build:
docker build -t %IMAGE_NAME% .
echo ------------------------------------
echo Use 'docker-compose up -d' to start the container
