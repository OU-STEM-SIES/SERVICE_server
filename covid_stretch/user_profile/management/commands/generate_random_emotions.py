# command that can be called by manage.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.apps import apps
from user_profile.models import Person_at_centre
from emotional_status.models import Emotional_status, get_random_emotional_support_value
from django.utils import timezone
from freezegun import freeze_time
import datetime
from datetime import timedelta 

num_emotions = 42
num_days = 21

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Generating random emotions...")

        # give everyone several moods
        Emotional_status.objects.all().delete()
    
        clients = Person_at_centre.objects.all()
        for client in clients:
            generate_emotions(client)
        
        print("Created random emotions.")


def generate_emotions(client):
    initial_time = timezone.now() - timedelta( hours=(num_days*24) )
    with freeze_time(initial_time) as frozen_time:
        for m in range(0, num_emotions):
            this_user = client.user_profile.user
            l = get_random_emotional_support_value()
            w = get_random_emotional_support_value()
            new_emotion = Emotional_status.objects.create(user=this_user, loneliness_level=l, general_wellbeing= w )
            frozen_time.tick(delta=timedelta(hours=12))
            
            l = get_random_emotional_support_value()
            w = get_random_emotional_support_value()
            new_emotion = Emotional_status.objects.create(user=this_user, loneliness_level=l, general_wellbeing= w )
            frozen_time.tick(delta=timedelta(hours=12))
