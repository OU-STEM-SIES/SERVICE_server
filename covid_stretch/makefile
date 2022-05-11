SHELL := /bin/bash
# SERVICE Django makefile

# This setup script supersedes several commands below, which I have
# now commented out, and will fully remove in a future update.
setup:
	cd ../!SETUP; python3 setup.py

m:
	python3 manage.py migrate
mm:
	python3 manage.py makemigrations 
run:
	python3 manage.py runserver
groups:
	python3 manage.py generate_groups
super:
	python3 manage.py generate_supers

# Launches a local fake SMTP server which pretends to send emails, for password
# reset requests etc, but actually just outputs them to stdout.
fakesmtp:
	sudo python -m smtpd -n -c DebuggingServer localhost:25


# Added by Jef: deletes existing database(s) and builds a new one from scratch
# HANDLE WITH CARE!
# delete_all_and_setup_new_test_instance:
# 	make delete_database
# 	make delete_migrations
# 	cp MEDIA-base/* MEDIA/
# 	make dummy
# 	python3 manage.py collectstatic --noinput

# Added by Jef: deletes existing database(s) and builds a new one from scratch
# HANDLE WITH CARE!
# delete_all_and_setup_new_live_instance:
# 	make delete_database
# 	make delete_migrations
# 	cp MEDIA-base/* MEDIA/
# 	make live
# 	python3 manage.py collectstatic --noinput

# import:
# 	python3 manage.py addnewusers
# Note: The new user CSV file should exist and contain new user data
# location: covid_stretch/user_profile/management/commands/additionaluserstoimport.csv

# test:
# 	pytest -s --ignore=user_profile/tests/test_selenium.py

# this requires selenium and webdriver to be installed.
# test_all:
# 	pytest -s

# delete_database:
# 	find . -path "*.sqlite3"  -delete
# 	find . -path "DATABASE/*.sqlite3"  -delete

delete_migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py migrate --run-syncdb

# add:
# 	python3 manage.py add_user

# dummy:
# 	python3 manage.py generate_test_db
# 	# python3 manage.py generate_random_moods

# live:
# 	python3 manage.py generate_live_db

real_mood:
	# imports real user mood data from STRETCH mood survey
	python3 manage.py generate_real_mood_user

freeze:
	pip freeze > requirements.txt

pip_install:
	pip install -r requirements.txt 

# coverage:
# 	coverage run --source='.' manage.py test
# 	coverage report

# fix_ssh:
# 	ssh-add ~/.ssh/id_rsa

#activate:
#	source /home/paul/Desktop/my_envs/service_env/bin/activate

# csv:
# 	python3 manage.py generate_csv
