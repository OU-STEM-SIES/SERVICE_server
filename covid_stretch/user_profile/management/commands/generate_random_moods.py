# command that can be called by manage.py
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.apps import apps
from user_profile.models import Person_at_centre
from moods.models import Moods, get_random_mood, get_random_pastime, Pastime

# from moods.models import Moods, get_random_mood

from django.utils import timezone
import pytz
from freezegun import freeze_time
import datetime
from datetime import timedelta 

num_moods = 21
num_days = 21

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # give everyone several moods
        Moods.objects.all().delete()
        print("Generating random moods.")
    
        clients = Person_at_centre.objects.all()
        for client in clients:
            generate_moods(client)
        
        print("Created random moods.")

def generate_moods(client):
    initial_time = timezone.now() - timedelta( hours=(num_days*24) )
    allsupporters = client.get_all_circle_supporters()
    with freeze_time(initial_time) as frozen_time:
        for m in range(0, num_moods):
            new_mood = Moods.objects.create(user=client.user_profile, current_mood=get_random_mood())
            frozen_time.tick(delta=timedelta(hours=12))

            new_mood = Moods.objects.create(
                user = client.user_profile,
                current_mood = get_random_mood(),
                time = timezone.now(), #datetime.datetime.now(),
                include_wellbeing = True,
                wellbeing = random.randrange(0,7),
                loneliness = random.randrange(0, 7),
                spoketosomeone = random.choice([True, False]),
                spoketosomeone_who = random.choice(allsupporters).user_profile.get_full_name(),
                hours_bed = random.randrange(0,8),
                hours_sofa=random.randrange(0, 8),
                hours_kitchen=random.randrange(0, 8),
                hours_garden=random.randrange(0, 8),
            )
            for r in range(random.randrange(0,4)):
                new_pastime = Pastime.objects.create(
                    mood=new_mood,
                    whatdoing=get_random_pastime(),
                )
                new_pastime.whowith.set(random.sample(allsupporters, k=random.randrange(0, 4)))
                new_pastime.save()

            frozen_time.tick(delta=timedelta(hours=12))
