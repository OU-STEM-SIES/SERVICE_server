#!/bin/bash
VENVFILE=../venv/bin/activate
if test -f "$VENVFILE"; then
  # virtual environment already exists - launching config.py
  source ../venv/bin/activate
  python3 config.py
else
  echo "Performing first-time setup of SERVICE environment."
  python3 -m venv ../venv
  source ../venv/bin/activate
  cd ../covid_stretch || exit  # if cd fails, then quit
  pip install -U pip
  OUFILE=requirements-OUSTEM.txt
  if test -f "$OUFILE"; then
    pip install -r requirements-OUSTEM.txt
  else
    pip install -r requirements.txt
  fi
  cd ../SETUP || exit  # if cd fails, then quit
  python3 config.py
fi

