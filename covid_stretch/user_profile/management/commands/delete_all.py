# command that can be called by manage.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from messaging.models import Messages
from user_profile.models import UserProfile, Person_at_centre, Linkworker, Supporter
from moods.models import Moods
from django.apps import apps
from emotional_status.models import Emotional_status

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # warning deletes all ********************************
        print("Deleting all database entries")
        try:
            User.objects.all().delete()
        except:
            pass
        try:
            UserProfile.objects.all().delete()
        except:
            pass
        try:
            Person_at_centre.objects.all().delete()
        except:
            pass
        try:
            Linkworker.objects.all().delete()
        except:
            pass
        try:
            Moods.objects.all().delete()
        except:
            pass
        try:
            Supporter.objects.all().delete()
        except:
            pass
        try:
            Emotional_status.objects.all().delete()
        except:
            pass


    print("Deleting all groups")
    try:
        Group.objects.all().delete()
    except:
        pass

