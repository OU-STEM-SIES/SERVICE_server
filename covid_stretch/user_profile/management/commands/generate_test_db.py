# command that can be called by manage.py
import csv
import os
import random

from django.contrib.auth.models import Group, User
from django.core import management
from django.core.management.base import BaseCommand
from user_profile.models import Linkworker, Person_at_centre, Supporter, UserProfile


num_line_workers = 3
num_pacs_per_lw = 10
num_supporters_per_pac = 3
num_moods = 21
total_num_pacs = num_line_workers * num_pacs_per_lw
total_num_supporters = total_num_pacs * num_supporters_per_pac
total_num_users = num_line_workers + total_num_pacs + total_num_supporters

MOCK_USER_FILE = "user_profile/management/commands/mock_users_v3.csv"
MOCK_IMAGE_FOLDER = "./MEDIA/"
# mock csv file columns = first_name,last_name,username,email,password,address,city,county,postal,phone1,phone2
MOCK_FIRST_NAME = 0
MOCK_LAST_NAME = 1
MOCK_USERNAME = 2
MOCK_EMAIL = 3
MOCK_PASSWORD = 4
MOCK_ADDRESS = 5
MOCK_CITY = 6
MOCK_COUNTY = 7
MOCK_POSTCODE = 8
MOCK_TELEPHONE_1 = 9
MOCK_TELEPHONE_2 = 10
MOCK_GENDER = 11
MOCK_ETHNICITY = 12
MOCK_EDUCATION = 13
MOCK_DISABILITY = 14
MOCK_MARITAL_STATUS = 15
MOCK_SMOKING = 16
MOCK_ALCOHOL_UNITS = 17
MOCK_HEALTH_CONDITIONS = 18


def getRandomImage():
    path = MOCK_IMAGE_FOLDER
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
        with open(MOCK_USER_FILE) as csvfile:
            mock_users = list(csv.reader(csvfile, delimiter=","))
            mock_index = 1
        
        #  lets create all the user profiles first
        for i in range(0, total_num_users + 1):
            mock_details = mock_users[mock_index]
            new_user = User.objects.create_user(
                    first_name=mock_details[MOCK_FIRST_NAME],
                    last_name=mock_details[MOCK_LAST_NAME],
                    username=mock_details[MOCK_USERNAME],
                    email=mock_details[MOCK_EMAIL],
                    password=mock_details[MOCK_PASSWORD],
                    )
            new_userprofile = UserProfile.objects.create(
                    user=new_user,
                    # phone=mock_details[MOCK_TELEPHONE_1],
                    image=getRandomImage(),
                    # gender=mock_details[MOCK_GENDER],
                    # ethnicity=mock_details[MOCK_ETHNICITY],
                    # education=mock_details[MOCK_EDUCATION],
                    # disability=mock_details[MOCK_DISABILITY],
                    # marital_status=mock_details[MOCK_MARITAL_STATUS],
                    # smoking=mock_details[MOCK_SMOKING],
                    # alcohol_units_per_week=mock_details[MOCK_ALCOHOL_UNITS],
                    # health_conditions=mock_details[MOCK_HEALTH_CONDITIONS],
                    )
            # add user details additions
            new_userprofile.randomise_personal_details()
            
            # save changes to user profile
            new_userprofile.save()
            
            mock_index += 1
        
        print("Created test users.")
        print("Assigning test users' roles...")
        
        # now assign roles
        ups = UserProfile.objects.all()
        for i in range(0, num_line_workers):
            ups[i].role = UserProfile.LINKWORKER
            Linkworker.objects.create(linkworker=ups[i])
            linkworker_group.user_set.add(ups[i].user)
        
        for i in range(num_line_workers, num_line_workers + total_num_pacs):
            ups[i].role = UserProfile.PERSON_AT_CENTRE
            Person_at_centre.objects.create(user_profile=ups[i])
            pac_group.user_set.add(ups[i].user)
        
        for i in range((num_line_workers + total_num_pacs), total_num_users):
            ups[i].role = UserProfile.SUPPORTER
            Supporter.objects.create(user_profile=ups[i])
            supporter_group.user_set.add(ups[i].user)
        
        print("Assigned test users' roles.")

        # supporter_index = num_line_workers + total_num_pacs
        
        # assign supporters to clients
        all_linkworkers = Linkworker.objects.all()
        all_clients = Person_at_centre.objects.all()
        all_supporters = Supporter.objects.all()
        
        print("Adding supporters/CoSs to PACs...")
        # add supporters to clients
        supp_index = 0
        for client in all_clients:
            for i in range(0, num_supporters_per_pac):
                new_supporter = all_supporters[supp_index]
                client.supporters.add(new_supporter)
                supp_index += 1
                if i >= (num_supporters_per_pac -3):
                    client.circle_of_support_1.add(random.choice(all_supporters))
                if i >= (num_supporters_per_pac -1):
                    client.circle_of_support_2.add(random.choice(all_supporters))
                if i == num_supporters_per_pac:
                    client.circle_of_support_3.add(random.choice(all_supporters))
        print("Added supporters/CoSs to PACs.")

        print("Adding PACs to Linkworkers...")

        # add clients to linkworkers
        client_index = 0
        for key in all_linkworkers:
            for i in range(0, num_pacs_per_lw):
                key.pacs.add(all_clients[client_index])
                client_index += 1

        print("Added PACs to Linkworkers.")

        # add random moods
        management.call_command("generate_random_moods")
        
        # add bill gates
        management.call_command("generate_real_mood_user")
        
        # add emotions
        # management.call_command("generate_random_emotions")
        
        #  always add super log in for developers
        #  (note: at this point, profiles WON'T be created for them)
        management.call_command("generate_supers")

        #  always add accounts for researchers
        #  (note: profiles WON'T be created for them)
        management.call_command("generate_researchers")
