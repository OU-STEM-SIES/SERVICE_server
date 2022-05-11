# command that can be called by manage.py
import csv
import os
import random

from django.contrib.auth.models import Group, User
from django.core import management
from django.core.management.base import BaseCommand
from user_profile.models import Linkworker, Person_at_centre, Supporter, UserProfile


USER_FILE = "user_profile/management/commands/real_users.csv"
IMAGE_FOLDER = "./MEDIA/"

with open(USER_FILE) as foo:
    USER_FILE_LENGTH = len(foo.readlines()) -1  # subtract one beause we don't want the header line.

num_link_workers = 3 # How many of the input file should be marked as key/link workers?
num_pacs_per_lw = 5 # How many PACS should be pre-assigned to each key/link worker?
num_supporters_per_pac = 0  # 3
num_moods = 0  # 21
total_num_pacs = (USER_FILE_LENGTH - num_link_workers)  # 17  # num_link_workers * num_pacs_per_lw
total_num_supporters = 0  # total_num_pacs * num_supporters_per_pac
total_num_users = num_link_workers + total_num_pacs + total_num_supporters

# mock csv file columns = first_name,last_name,username,email,password,address,city,county,postal,phone1,phone2
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
        # delete old
        management.call_command("delete_all")
        
        management.call_command("generate_groups")
        
        researcher_group = Group.objects.get(name="Researchers")
        linkworker_group = Group.objects.get(name="Linkworkers")
        supporter_group = Group.objects.get(name="Supporters")
        pac_group = Group.objects.get(name="PACs")
        
        print("Generating test users...")

        # load mock details
        with open(USER_FILE) as csvfile:
            # live_users = list(csv.reader(csvfile, delimiter=","))
            live_reader = csv.reader(csvfile, delimiter=",")
            live_users = list(live_reader)
            live_row_count = len(live_users)
            live_index = 1
        
        #  lets create all the user profiles first
        for i in range(0, live_row_count-1):
            live_details = live_users[live_index]
            print("Adding " + str(live_index) + " of " + str(live_row_count-1) + " (" + live_details[FIRST_NAME] + " " + live_details[LAST_NAME] + "): ", end = "")
            new_user = User.objects.create_user(
                    first_name=live_details[FIRST_NAME],
                    last_name=live_details[LAST_NAME],
                    username=live_details[USERNAME],
                    email=live_details[EMAIL],
                    password=live_details[PASSWORD],
                    )
            print("Created User. ", end="")
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
                    )
            print("Created UserProfile.")
            # add user details additions
            # new_userprofile.randomise_personal_details()
            
            # save changes to user profile
            new_userprofile.save()
            
            live_index += 1
        
        print("Created live users.")

        print("Assigning test users' roles...")
        
        # now assign roles
        ups = UserProfile.objects.all()
        for i in range(0, num_link_workers):
            ups[i].role = UserProfile.LINKWORKER
            Linkworker.objects.create(linkworker=ups[i])
            linkworker_group.user_set.add(ups[i].user)
        
        for i in range(num_link_workers, num_link_workers + total_num_pacs):
            ups[i].role = UserProfile.PERSON_AT_CENTRE
            Person_at_centre.objects.create(user_profile=ups[i])
            pac_group.user_set.add(ups[i].user)
        
        for i in range((num_link_workers + total_num_pacs), total_num_users):
            ups[i].role = UserProfile.SUPPORTER
            Supporter.objects.create(user_profile=ups[i])
            supporter_group.user_set.add(ups[i].user)
        
        print("Assigned test users' roles.")

        # supporter_index = num_link_workers + total_num_pacs
        
        # assign supporters to clients
        all_linkworkers = Linkworker.objects.all()
        first_linkworker = Linkworker.objects.all().first()
        all_clients = Person_at_centre.objects.all()
        # all_supporters = Supporter.objects.all()
        
        # print("Adding supporters to PACs...")
        # # add supporters to clients
        # supp_index = 0
        # for client in all_clients:
        #     for i in range(0, num_supporters_per_pac):
        #         new_supporter = all_supporters[supp_index]
        #         client.supporters.add(new_supporter)
        #         supp_index += 1
        #
        # print("Added supporters to PACs.")

        print("Adding PACs to Linkworkers...")

        # add clients to linkworkers
        client_index = 0
        # for key in all_linkworkers:
        for i in range(0, num_pacs_per_lw):
            first_linkworker.pacs.add(all_clients[client_index])
            client_index += 1

        print("Added PACs to Linkworkers.")

        # add random moods
        # management.call_command("generate_random_moods")
        
        # add bill gates
        # management.call_command("generate_real_mood_user")
        
        # add emotions
        # management.call_command("generate_random_emotions")
        
        #  always add super log in for developers
        #  (note: at this point, profiles WON'T be created for them)
        management.call_command("generate_supers")

        #  always add accounts for researchers
        #  (note: profiles WON'T be created for them)
        management.call_command("generate_researchers")
