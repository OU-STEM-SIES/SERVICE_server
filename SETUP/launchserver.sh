#!/bin/bash
FILE=../venv/bin/activate
if test -f "$FILE"; then
  # virtual environment already exists - launching server
  source ../venv/bin/activate
  cd ../covid_stretch || exit  # if cd fails, then quit
  python3 manage.py runserver
else
  echo "You can't launch the server until you've configured your new installation."
  echo "Run ./setup.sh first."
fi

