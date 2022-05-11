# command that can be called by manage.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_profile.models import Linkworker, Person_at_centre
from django.apps import apps

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        profiles = Person_at_centre.objects.all()
        print("Displaying all {} Person_at_centres".format(len(profiles)))
        for user in profiles:
            print(user)
