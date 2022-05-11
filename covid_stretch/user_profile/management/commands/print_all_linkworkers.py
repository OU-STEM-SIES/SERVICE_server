# command that can be called by manage.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_profile.models import Linkworker
from django.apps import apps

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        profiles = Linkworker.objects.all()
        print("Displaying all {} Lineworkers".format(len(profiles)))
        for user in profiles:
            print(user)
