# command that can be called by manage.py
import csv
import os
import random
import datetime

from django.contrib.auth.models import Group, User
from django.core import management
from django.core.management.base import BaseCommand
from user_profile.models import Linkworker, Person_at_centre, Supporter, UserProfile

USER_FILE = "user_profile/management/commands/additionaluserstoimport.csv"
USER_FILE_NEW_NAME = "user_profile/management/commands/additionaluserstoimport_IMPORTED_AT_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"



IMAGE_FOLDER = "./MEDIA/"

# csv file columns = first_name,last_name,username,email,password,address,city,county,postal,phone1,phone2
FIRST_NAME = 0
LAST_NAME = 1
USERNAME = 2
EMAIL = 3
PASSWORD = 4
ADDRESS = 5
CITY = 6
COUNTY = 7
POSTCODE = 8
TELEPHONE_1 = 9
TELEPHONE_2 = 10
GENDER = 11
ETHNICITY = 12
EDUCATION = 13
DISABILITY = 14
MARITAL_STATUS = 15
SMOKING = 16
ALCOHOL_UNITS = 17
HEALTH_CONDITIONS = 18


def getRandomImage():
    path = IMAGE_FOLDER
    random_filename = random.choice(
            [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
            )
    return random_filename


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # researcher_group = Group.objects.get(name="Researchers")
        # linkworker_group = Group.objects.get(name="Linkworkers")
        # supporter_group = Group.objects.get(name="Supporters")
        pac_group = Group.objects.get(name="PACs")
        first_linkworker = Linkworker.objects.all().first()

        print("Importing users...")
        # load details
        with open(USER_FILE) as csvfile:
            # live_users = list(csv.reader(csvfile, delimiter=","))
            live_reader = csv.reader(csvfile, delimiter=",")
            live_users = list(live_reader)
            live_row_count = len(live_users)
            live_index = 0

        #  lets create all the user profiles first
        for i in range(0, live_row_count):
            live_details = live_users[live_index]
            print("Adding " + str(live_index+1) + " of " + str(live_row_count) + ": " + live_details[FIRST_NAME] + " " + live_details[LAST_NAME] + "... ")
            new_user = User.objects.create_user(
                first_name=live_details[FIRST_NAME],
                last_name=live_details[LAST_NAME],
                username=live_details[USERNAME],
                email=live_details[EMAIL],
                password=live_details[PASSWORD],
                )  # User is created; doesn't require manual saving.
            new_userprofile = UserProfile.objects.create(
                user=new_user,
                phone=live_details[TELEPHONE_1],
                image=getRandomImage(),
                gender=live_details[GENDER],
                ethnicity=live_details[ETHNICITY],
                education=live_details[EDUCATION],
                disability=live_details[DISABILITY],
                marital_status=live_details[MARITAL_STATUS],
                smoking=live_details[SMOKING],
                alcohol_units_per_week=live_details[ALCOHOL_UNITS],
                health_conditions=live_details[HEALTH_CONDITIONS],
                role=UserProfile.PERSON_AT_CENTRE
                )
            new_userprofile.save()  # save changes to user profile
            new_pac_record = Person_at_centre.objects.create(user_profile=new_userprofile)  # Create a PAC record
            pac_group.user_set.add(new_userprofile.user)  # join the PAC user group
            first_linkworker.pacs.add(new_pac_record)  # link all the new PACs to the first linkworker by default
            live_index += 1

        os.rename (USER_FILE, USER_FILE_NEW_NAME)  # rename the import file
        print("Imported additional users.")
