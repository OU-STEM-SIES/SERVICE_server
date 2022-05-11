# command that can be called by manage.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from user_profile.models import Linkworker, Person_at_centre
from messaging.models import Messages
from user_profile.models import UserProfile, Person_at_centre, Linkworker, Supporter
from moods.models import Moods, get_random_mood
from django.apps import apps
import csv
CSV_BASE = './data/csv/'
USER_CSV_FILE = CSV_BASE + 'users.csv'
PROFILE_CSV_FILE = CSV_BASE + 'profiles.csv'
MOODS_CSV_FILE = CSV_BASE + 'moods.csv'

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.user_csv()
        self.profile_csv()
        self.moods_csv()

    def user_csv(self):
        with open(USER_CSV_FILE, mode='w') as user_file:
            writer = csv.writer(user_file)
            writer.writerow(['Username', 'First name', 'Last name', 'Email address'])
            
            users = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
            for user in users:
                writer.writerow(user)

    def profile_csv(self):
        with open(PROFILE_CSV_FILE, mode='w') as user_file:
            writer = csv.writer(user_file)
            writer.writerow(['User', 'Created', 'Last update', 'Role', 'Phone', 'image'])

            profiles = UserProfile.objects.all().values_list('user', 'created_on', 'last_updated', 'role', 'phone', 'image')
            for profile in profiles:
                writer.writerow(profile)

    def moods_csv(self):
        with open(MOODS_CSV_FILE, mode='w') as user_file:
            writer = csv.writer(user_file)
            writer.writerow(['User', 'Current Mood', 'Time'])

            all_data = Moods.objects.all().values_list('user', 'current_mood', 'time')
            for data in all_data:
                writer.writerow(data)

