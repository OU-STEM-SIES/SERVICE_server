# command that can be called by manage.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.apps import apps
from user_profile.models import Person_at_centre, UserProfile, Linkworker
from moods.models import Moods, get_random_mood
from django.core import management
import datetime
import csv
import string
from datetime import datetime
from django.utils import timezone

MOODS_FILE = 'user_profile/management/commands/client_32_moods.csv'

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        # delete old
        # management.call_command('delete_all')
        print("Generating realistic user...")

        # Generate user for data
        fn = "Bill"
        ln = "Gates"
        un = "billgates62"
        em = "bill@microsoft.com"
        ph = "01290 000200"
        ro = UserProfile.PERSON_AT_CENTRE
        pw = "Bill is not a real user"

        # create bill user
        bill = User.objects.create_user(first_name=fn, last_name=ln, username=un, email=em, password=pw )
        bill_profile = UserProfile(user=bill, phone=ph, role=ro)
        bill_profile.randomise_personal_details()
        bill_profile.save()
        pac_group = Group.objects.get(name='PACs') 
        pac_group.user_set.add(bill)

        # find linworker
        pacs = Person_at_centre.objects.all()
        bill_pac = Person_at_centre.objects.create(user_profile=bill_profile)

        linkworker = Linkworker.objects.first()
        linkworker.pacs.add(bill_pac)

        # add bill to Garnet Biskup

        print("Created realistic user.")
        print("Generating realistic user's mood records...")

        # load moods from file        
        with open(MOODS_FILE) as csvfile:
            moods = list(csv.reader(csvfile, delimiter=','))

        for mood in moods:
            # CSV columns are: id,mood,timestamp,relative_position,device_type,subject
            id,mood_type,timestamp,relative_position,device_type,subject = mood

            new_mood = ""
            if device_type == "CL":
                # mood clock
                new_mood = mood_type
                
            if device_type == "BD":
                # mood Board
                # suffix, new_mood = mood_type.split()
                new_mood = mood_type
            
            mood_time = datetime.strptime(timestamp, "%d/%m/%Y %H:%M").replace(tzinfo=timezone.utc)
            Moods.objects.create(user=bill_profile, current_mood=new_mood, time=mood_time)
        
        print("Created realistic user's moods.")
