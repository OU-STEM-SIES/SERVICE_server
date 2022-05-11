# command that can be called by manage.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from django.apps import apps

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        userprofiles = UserProfile.objects.all()
        print("Displaying all {} Users".format(len(userprofiles)))
        for user in userprofiles:
            print(user)
