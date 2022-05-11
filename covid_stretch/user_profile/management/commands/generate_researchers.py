# command that can be called by manage.py
# This is an in-progress routine to generate users (members of the researchers group) based on CSV input.
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
import csv

RESEARCHERS_FILE = "user_profile/management/commands/researchers_list.csv"
RESEARCHERS_GROUP = Group.objects.get(name="Researchers")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        
        print("Generating researcher accounts...")
        
        with open(RESEARCHERS_FILE) as csvfile:
            researcher_list = list(csv.reader(csvfile, delimiter=','))
            for one_researcher in researcher_list:
                tmp_username, tmp_email, tmp_first_name, tmp_last_name, tmp_password = one_researcher
                new_user = User.objects.create_user(
                                                    username=tmp_username,
                                                    email=tmp_email,
                                                    first_name=tmp_first_name,
                                                    last_name=tmp_last_name,
                                                    password=tmp_password
                                                    )
                RESEARCHERS_GROUP.user_set.add(new_user)
                print("Researcher imported: " + tmp_first_name + " " + tmp_last_name + ".")
                del new_user

        print("Created researcher accounts.")
