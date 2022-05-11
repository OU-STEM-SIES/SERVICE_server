#!/bin/bash
# See https://docs.docker.com/storage/volumes/ for the use of Docker volumes.
echo ""
echo "### Images ###"
docker images
echo ""
echo "### Launching ###"
docker run -d --mount source=SERVICE_database_volume,target=/opt/src/covid_stretch/DATABASE --mount source=SERVICE_media_volume,target=/opt/src/covid_stretch/MEDIA --publish 127.0.0.1:8000:8000/tcp --name service-django -t service-django-image-slim:latest
echo ""
echo "### Containers ###"
docker ps
echo "###"
echo ""
