# syntax=docker/dockerfile:1.3
# Enable BuildKit builder, which allows transmission of secrets into the container. See https://docs.docker.com/develop/develop-images/build_enhancements/

# The SERVICE project's server software image build

# Start with a known-good Python3 base
FROM python:3-slim
#FROM python:3       # "3" is the default comprehensive stable build of python 3
#FROM python:3-slim  # "3-slim" is the default minimal stable build of python 3 - currently this requires 'make' to be added to the dependencies.

# Add descriptive metadata
LABEL org.label-schema.schema-version="1.0"
#LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="SERVICE project"
LABEL org.label-schema.description="A Django-based web UI & API for filling and interrogating a relational database"
LABEL org.label-schema.url="https://serviceproject.org.uk"
LABEL org.label-schema.vcs-url="https://stem-ts-gitlab.open.ac.uk/jal58/SERVICE"
#LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vendor="Software Innovation Engineering Services (SIES) Team, of the STEM Faculty at The Open University, UK"
LABEL org.label-schema.version="0.8.x"
#LABEL org.label-schema.version=$BUILD_VERSION
#LABEL org.label-schema.docker.cmd="docker run -v ~/ballerina/packages:/ballerina/files -p 9090:9090 -d ballerinalang/ballerina"
LABEL maintainer="Jef.Lay@open.ac.uk"

# Install the requirements list.
WORKDIR /opt/src/covid_stretch
COPY covid_stretch/requirement*.txt .

# We do all this in as few commands as possible to generate fewer image layers:
# Install current required packages for sqlite3 compilation,
# Install make (required if using python:3-slim as the base image, harmless otherwise)
# Remove the apt-get list caches, to save space
# Update pip to the current release,
# Install all required Python modules.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sqlite3 \
        make \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -U pip \
    && [ -f "requirements-OUSTEM.txt" ] && pip install -r requirements-OUSTEM.txt || pip install -r requirements.txt

#    && pip install -r requirements.txt
#    && pip -q install -r requirements-OUSTEM.txt \

# Import duplicates of some stuff. This is because Kubernetes persistent mount points
# don't inherit the contents of the underlying directories like Docker volumes do.
# We detect if there's no database and copy in this initial state.

#WORKDIR /opt/src/initialise/database
COPY covid_stretch/DATABASE/db.sqlite3 /opt/src/initialise/database/db.sqlite3

#WORKDIR /opt/src/initialise/media
COPY covid_stretch/MEDIA /opt/src/initialise/media/

# Import the rest of our code.
# We did the requirements earlier to avoid repeating that step every time we rebuild.
WORKDIR /opt/src/covid_stretch
COPY covid_stretch .

# We do all this in as few commands as possible to generate fewer image layers:
# Connect the "secrets" items to the /secrets/* mount points in the container, then
# Build or update Django's database,
# Now disabled, because we copy the database from the local installation
#RUN --mount=type=secret,id=DJANGO_SECRET_KEY,dst=/secrets/DJANGO_SECRET_KEY \
#    --mount=type=secret,id=DJANGO_SITENAME,dst=/secrets/DJANGO_SITENAME \
#    --mount=type=secret,id=DJANGO_FORCE_SCRIPT_NAME,dst=/secrets/DJANGO_FORCE_SCRIPT_NAME \
#    make delete_all_and_setup_new_live_instance
# or make delete_all_and_setup_new_test_instance

# Inform the user that this image listens on port 8000
EXPOSE 8000/tcp

# To use Green Unicorn to launch Django with a reasonably performant server:
# gunicorn --bind 0.0.0.0:8000 covid_stretch.wsgi
# Instead, we're using an entrypoint script which does some first-time-only preparations.
ENTRYPOINT ["/opt/src/covid_stretch/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "covid_stretch.wsgi"]
# NOTE: gunicorn must use 0.0.0.0, not 127.0.0.1, if it is to be reachable by the outside world.

