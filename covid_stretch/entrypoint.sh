#!/bin/sh
if [ "$1" = "gunicorn" ]; then
  [ -f "/opt/src/covid_stretch/DATABASE/db.sqlite3" ] || cp "/opt/src/initialise/database/db.sqlite3" "/opt/src/covid_stretch/DATABASE/db.sqlite3"
  find "/opt/src/covid_stretch/MEDIA" -maxdepth 0 -empty -exec cp -nu "/opt/src/initialise/media/*" "/opt/src/covid_stretch/MEDIA/" \;
  python manage.py migrate
  python manage.py collectstatic --noinput
fi

# Start process
exec "$@"
