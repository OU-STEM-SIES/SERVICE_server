# syntax = docker/dockerfile:1.0-experimental
# Enable BuildKit builder, which allows transmission of secrets into the container. See https://docs.docker.com/develop/develop-images/build_enhancements/

# STEM-SSU's SERVICE project build

# References:
# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

# Start with a known-good nginx base
FROM nginx:stable-alpine
#FROM nginx:stable         # stable is the safe, reliable version with supporting stuff
#FROM nginx:stable-alpine  # stable-alpine is the ultracompact stable version
#FROM nginx:latest         # latest is the latest version, but may not be stable

# Add descriptive metadata
LABEL org.label-schema.schema-version="1.0"
#LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="SERVICE project webserver"
LABEL org.label-schema.description="Web server reverse proxy for a Django-based web UI"
LABEL org.label-schema.url="https://serviceproject.org.uk"
LABEL org.label-schema.vcs-url="https://github.com/dalmatianrex/covid-stretch"
#LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="Software Innovation and Engineering Specialist Team of the STEM Faculty at The Open University, UK"
#LABEL org.label-schema.version=$BUILD_VERSION
#LABEL org.label-schema.docker.cmd="docker run -v ~/ballerina/packages:/ballerina/files -p 9090:9090 -d ballerinalang/ballerina"
LABEL maintainer="Jef.Lay@open.ac.uk"

# Remove the default config file, and insert our own
RUN rm /etc/nginx/conf.d/default.conf
#COPY nginx.conf /etc/nginx/conf.d

# This image listens on port 8080
EXPOSE 8080/tcp
