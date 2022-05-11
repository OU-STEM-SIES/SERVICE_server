# command that can be called by manage.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_profile.models import UserProfile
from moods.models import Moods
from django.apps import apps

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        moods = Moods.objects.all()
        print("Displaying all {} Moods".format(len(moods)))
        for mood in moods:
            print(mood)
