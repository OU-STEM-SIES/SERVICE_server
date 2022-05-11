Covid-stretch back end:

Covid_stretch is a django project intended to encapsulate a database and REST API for a smart-phone application. 
The smart phone app will communicate with this back end via REST which is implemented by djangorestframework - https://www.django-rest-framework.org/


Project structure:
covid_stretch
    > user_profile
    > moods
    > messaging

Userprofile -> UserProfile adds additional data to the user base class like telephone number.
Moods -> is a data base of mood reading received into the system
Messaging -> is intended to store messages between Linkworkers, clients, and admins

How to install (linux):

1: Create folder called covid_stretch and cd into it
2: Create virtualenv "python3 -m venv env"
3: Activate virtualenv by "source env/bin/activate"
4: Clone from sourced by "git clone git@github.com:dalmatianrex/covid-stretch.git"
5: cd to covid_stretch folder
5a: run "make pip_install" to install packages
6: Lots of django commands are given in makefile, thses can be called by profixing with make i.e. make run
7: Create database by "make mm" and "make m" also add superuser "make super"
8: Run tests by "make test"

Engineering approaches included here:
djangorestframework - for rest API
pytest for test driven development
factories for test cases
Dummy command in user_profile/management/commands can be used to build a mock database