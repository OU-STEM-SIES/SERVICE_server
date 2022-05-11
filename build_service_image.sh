#!/bin/bash
# See https://docs.docker.com/storage/volumes/ for use of volumes
export DOCKER_BUILDKIT=1  # still needed on some systems

docker volume create SERVICE_database_volume
docker volume create SERVICE_media_volume
docker volume create SERVICE_static_volume

# Unwanted files are listed in .dockerignore
docker build --no-cache -t service-django-image-slim:latest .
