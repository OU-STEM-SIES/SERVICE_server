#!/usr/bin/env python3
##############################################################################
# An automated setup script for SERVICE project servers.
# BEFORE RUNNING THIS SCRIPT: pip install simple-term-menu
##############################################################################
# You can edit these to make things simpler for yourself:
defaultsuperuserfirstname = "Jeffery"
defaultsuperuserlastname = "Lay"
defaultsuperuseremail = "Jef.Lay@open.ac.uk"

# For fake data generation:
random_generation_seed_value = None  # Set this to an integer value to generate the same sequence of data every time, or None for different every time.
fake_data_linkworker_count = 5
fake_data_pacs_per_linkworker = 5
fake_data_supporters_per_pac = 4
fake_data_mood_days_per_pac=14

# For user icons
image_path = "../covid_stretch/MEDIA/"
##############################################################################
#
# DONE:
#  Add "make setup" to makefile
#  create DATABASE and MEDIA and STATIC folders, if not already present.
#  MEDIA dir templating
#  settings.py value templating
#  email backend configuration
#  Remove/disable several redundant makefile options such as test data
#  switch superuser creation to csv import
#  split Linkworker and PAC into separate CSV imports
#  adapt add_new_users to use the same CSV format as PAC
#  change all the above to ignore the first line
#  create template CSV file for superusers
#  create template CSV file for researchers
#  create template CSV file for linkworkers
#  create template CSV file for PACs
#  create template CSV file for additional users
#  move import CSV files to SETUP dir
#  Move other template files to SETUP
#  Test data generator (using Faker): Linkworkers/PACs/supporters/moods/wellbeings.
#  Sort FontAwesomePro/FontAwesome CSS import in templates/base.html
#  Solve why fontawesomefree/pro CSS isn't loading from container - maybe due to gunicorn?
#  New nginx image build script in one go without secrets
#  New nginx image launch script without secrets
#  New Django image build script in one go without secrets
#  New Django image launch script without secrets
#  Get rid of secrets!!
##############################################################################

import csv
import os
import sys
import random

# Make sure simple_term_menu is available
try:
    from simple_term_menu import TerminalMenu
except ModuleNotFoundError:
    print("This script requires two custom modules.")
    print("To use this script, please install the simple-term-menu module, by typing:")
    print("  pip install simple-term-menu")
    sys.exit()

# Make sure faker is available
try:
    from faker import Faker
    from faker.providers import profile, person
except ModuleNotFoundError:
    print("This script requires two custom modules.")
    print("To use this script, please install the Faker module, by typing:")
    print("  pip install Faker")
    sys.exit()


INSTALL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DJANGO_DIR = os.path.join(INSTALL_DIR, "covid_stretch")
managepypath = os.path.join(DJANGO_DIR, "manage.py")

if os.path.isfile(os.path.join(DJANGO_DIR, "requirements-OUSTEM.txt")):
    use_ou_installation_options = True  # This causes OU-specific settings to be included.
else:
    use_ou_installation_options = False



# See https://stackoverflow.com/questions/39723310/django-standalone-script/39724171
# for how to set up Django to be used within a standalone Python script.
sys.path.append(DJANGO_DIR)  # Include the app dir in our Python search path
if os.path.isfile(os.path.join(DJANGO_DIR, "covid_stretch", "settings.py")):
    use_temporary_config_file = False
else:
    # print("There is no Django settings file. We need to build a new one first.")
    # new_installation()
    use_temporary_config_file = True
    print("There is no Django settings file. Using a temporary settings file until you build your own.")
    if os.name == 'nt':  # Cope with both Windows and mature OSs
        os.system('copy templates\\settings.py_temporary_template ..\\covid_stretch\\covid_stretch\\settings.py')
    else:
        os.system('cp templates/settings.py_temporary_template ../covid_stretch/covid_stretch/settings.py')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "covid_stretch.settings")
import django
django.setup()
# Now we have access to Django models etc. despite being outside the normal file hierarchy
from django.core.management import utils
from django.conf import settings
from django.contrib.auth.models import User, Group
from user_profile.models import UserProfile, Linkworker, Person_at_centre, Supporter
from moods.models import Moods, get_random_mood, get_random_pastime, Pastime
from django.utils import timezone
import pytz
from freezegun import freeze_time
import datetime
from datetime import timedelta

# Constants so we can refer to csv imports by name rather than column number
USERNAME = 0
FIRST_NAME = 1
LAST_NAME = 2
EMAIL = 3
PASSWORD = 4


# define our clear-screen/terminal function
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')  # Cope with both Windows and mature OSs


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def generate_config_file_from_template(templatefilename: str, substitutions: dict, targetpath: str):
    # Takes a file from the templates, does a bunch of substitutions on it,
    # and outputs the result to a new location (same filename)
    substitutionstartdelimiter = "####"
    substitutionenddelimiter = "####"
    tmpsourcefile = os.path.join(INSTALL_DIR, "SETUP/templates/", templatefilename + "_template")
    tmptargetfile = os.path.join(INSTALL_DIR, targetpath, templatefilename)
    # print(f"Source file: {tmpsourcefile}")
    # print(f"Target file: {tmptargetfile}")
    if (not os.path.isfile(tmptargetfile)) or \
            (input(f"{tmptargetfile} already exists! Enter \"YES\" to overwrite, return to skip:") == "YES"):
        with open(tmpsourcefile, 'r') as sourcefile:
            filecontents = sourcefile.read()
            for onesubstitutionsrc, onesubstitutionreplacement in substitutions.items():
                filecontents = filecontents.replace(
                    substitutionstartdelimiter
                    + onesubstitutionsrc
                    + substitutionenddelimiter,
                    str(onesubstitutionreplacement)
                )
        with open(tmptargetfile, 'w') as targetfile:
            targetfile.write(filecontents)
            print(f"File {tmptargetfile} has been created.")
    else:
        print("!!! File was not overwritten, config has not been changed.")
        # print(filecontents)


def ensuredirectoryexists(tmppath):
    print(f"Directory {tmppath}", end="")
    if os.path.isdir(tmppath):
        print(" already exists and will be used.")
    else:
        os.mkdir(tmppath, 0o755)
        print(" has been created.")


def new_installation():
    print("""Configuring a new installation.
        
        You will need:
        • (optional) A Django secret key (generated from https://djecrety.ir or 
          https://miniwebtool.com/django-secret-key-generator/ or similar)
        • The first name, last name, username, email address, and password 
          for the first superuser
    """)

    print("""
If you're going to modify this server on your local computer for testing, you will need to 
enable DEBUG mode in order to get useful diagnostics if anything fails. However, you should 
never use DEBUG mode in production, as it will reveal sensitive data. 

Type "DEBUG" to enable debugging, or just hit return. If in doubt, leave it off!
    """)
    debugmode = (input("DEBUG:") == "DEBUG") or "False"
    print(f"DEBUG: {debugmode}\n")
    if debugmode != "False":
        print("************************************************************")
        print("WARNING: Do not use this server on the open internet, ")
        print("unless you first reconfigure and disable DEBUG mode.")
        print("************************************************************")
        print("")

    secret_key = \
        input("Paste a Django secret key here, or just hit return to generate a new one: ").strip() \
        or utils.get_random_secret_key()
    print(f"Django secret key: \"{secret_key}\"")

    print("""Optional. If you wish to restrict the hostnames to which your server 
    will respond, then type a comma-separated list of hostnames. 
    If in doubt, just hit return to respond to any hostnames: """)
    hostname = input("ALLOWED_HOSTS: ")
    if hostname == "":
        allowed_hosts = ["*"]
    else:
        allowed_hosts = hostname.split(",")

    print("In order to run the software, you'll need at least one super-user account to be created.")
    print("If you don't know who this will be, enter your own name for now, and add other users later.")
    superuserfirstname = input("Superuser's first name: ").strip() or defaultsuperuserfirstname
    superuserlastname = input("Superuser's last name: ").strip() or defaultsuperuserlastname
    tmpsuperusername = (superuserfirstname[:1] + superuserlastname).lower()
    superuserusername = input(f"Superuser's username (default '{tmpsuperusername}'): ").strip() or tmpsuperusername
    superuseremail = input("Superuser's email address: ").strip() or defaultsuperuseremail
    superuserpassword = input("Superuser's password: ").strip()
    superuserpassword_verify = input("Verify superuser's password: ").strip()
    if superuserpassword != superuserpassword_verify:
        raise ValueError("Superuser password verification doesn't match.")
    print(f"Superuser :{superuserfirstname} {superuserlastname} ({superuserusername}), ", end="")
    print(f"{superuseremail}, {superuserpassword}.")

    print("""




Outgoing mail (for password resets, etc.). You have three options. Choose one of the following:

1. Just save any would-be outgoing emails as text files on the local filesystem.
2. Set up a local SMTP-debugging server, which acts like a real SMTP server to test 
   communication, but never actually sends anything (messages are just printed to stdout).
3. Set up a real SMTP server. You will need to provide the server address and port number, 
   whether TLS may be used, a valid FROM address, and (if needed) a username and password.
""")
    mail_options = ["Just save messages as text files",
                    "Set up debugging-only SMTP server",
                    "Set up a real outgoing server"
                    ]
    mail_terminal_menu = TerminalMenu(mail_options)
    mail_menu_entry_index = mail_terminal_menu.show()
    if mail_menu_entry_index == 0:
        mail_config_text = """
# Fake email backend for password reset message testing.
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# This is the path on the local filesystem where outgoing messages will be saved as text files.
EMAIL_FILE_PATH = str(os.path.join(BASE_DIR, "sent_emails"))  
# This must be replaced with a real SMTP server for production use

# These are the real SMTP config fields, for future use:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Tells Django to use a real SMTP server
# DEFAULT_FROM_EMAIL = ''  # A valid address that outgoing emails go from and replies come to
# EMAIL_HOST = ''          # The hostname or IP address of the SMTP server
# EMAIL_USE_TLS = True     # Enable or disable Transport Layer Security (encryption). Highly desirable.
# EMAIL_PORT = 587         # The port on the server to use. Usually 25 without TLS, or 587 with TLS
# EMAIL_HOST_USER = ''     # A valid account username for the server, if required
# EMAIL_HOST_PASSWORD = '' # A valid account password for the server, if required

"""
    elif mail_menu_entry_index == 1:
        mail_config_text = """
# To run a local debugging SMTP server which just prints messages to stdout:
# sudo python -m smtpd -n -c DebuggingServer localhost:25

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = '""" + superuseremail + """'  # A valid address that outgoing emails go from and replies come to
EMAIL_HOST = 'localhost'  # The hostname or IP address of the SMTP server
EMAIL_USE_TLS = False  # Enable or disable Transport Layer Security (encryption). Highly desirable.
EMAIL_PORT = 25  # The port on the server to use. Usually 25 without TLS, or 587 with TLS
EMAIL_HOST_USER = ''  # A valid account username for the server, if required
EMAIL_HOST_PASSWORD = ''  # A valid account password for the server, if required
"""
    elif mail_menu_entry_index == 2:
        default_from_email = input(f"Address to send emails from (default {superuseremail}): ") or superuseremail
        email_host = input("SMTP server IP address or hostname: ")
        email_use_tls = input(f"Use TLS? (default True, or False): ") or "True"
        email_port_default = "25" if email_use_tls != "True" else "587"
        email_port = input(f"SMTP server port number (default {email_port_default}): ") or email_port_default
        email_host_user = input("SMTP server account username (if required): ")
        email_host_password = input("SMTP server account password (if required): ")

        mail_config_src_text = """
# SMTP server config fields:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Tells Django to use a real SMTP server
DEFAULT_FROM_EMAIL = '!!'  # A valid address that outgoing emails go from and replies come to
EMAIL_HOST = '@@'          # The hostname or IP address of the SMTP server
EMAIL_USE_TLS = ##     # Enable or disable Transport Layer Security (encryption). Highly desirable.
EMAIL_PORT = $$         # The port on the server to use. Usually 25 without TLS, or 587 with TLS
EMAIL_HOST_USER = '%%'     # A valid account username for the server, if required
EMAIL_HOST_PASSWORD = '^^' # A valid account password for the server, if required

"""
        mail_config_replacement_dict = {
            "!!": default_from_email,
            "@@": email_host,
            "##": email_use_tls,
            "$$": email_port,
            "%%": email_host_user,
            "^^": email_host_password,
        }
        mail_config_text = replace_all(mail_config_src_text, mail_config_replacement_dict)
    else:
        print(f"You have selected {mail_options[mail_menu_entry_index]}, which isn't coded yet.")
        sys.exit()

    print("Summary:")
    print(f"Django secret key: \"{secret_key}\"")
    print(f"Superuser :{superuserfirstname} {superuserlastname} ({superuserusername}), ", end="")
    print(f"{superuseremail}, {superuserpassword}.")
    print(f"SMTP server: {mail_options[mail_menu_entry_index]}")

    if input("Ready to configure. Enter \"YES\" to proceed, or anything else to abort: ") != "YES":
        sys.exit("Aborted at user request. (You didn't enter \"YES\")")
    else:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'covid_stretch.settings'

        # Include OU-specific configurations?
        if use_ou_installation_options:
            ou_installation_apps = "    \"fontawesomepro\","  # Note the indentation is important!
        else:
            ou_installation_apps = "    \"fontawesomefree\","  # Note the indentation is important!

        # Build a configuration file.
        generate_config_file_from_template(
            templatefilename="settings.py",
            targetpath="covid_stretch/covid_stretch/",
            substitutions={
                "SECRET_KEY": secret_key,
                "debugmode" : debugmode,
                "ALLOWED_HOSTS": allowed_hosts,
                "mail_config_text": mail_config_text,
                "ou_installation_apps": ou_installation_apps,
            }
        )

        try:
            superuseraccount = User.objects.create_superuser(
                username=tmpsuperusername,
                email=superuseremail,
                password=superuserpassword,
                first_name=superuserfirstname,
                last_name=superuserlastname
            )
            Group.objects.get(name='Researchers').user_set.add(superuseraccount)
            print("Superuser account created and added to researchers group")
        except Exception as e:
            print(f"!!! Superuser account was NOT created: {e}")

    print("\nMinimal installation completed.")
    print("Your server should now be able to run with the default settings.")
    print("To launch it, or to import user data, rerun this setup script.")
    print("\nIf you need to change the network port or other configuration settings, refer to the documentation in the README directory.")
    sys.exit()  # or main()


def import_users(csvfilepath: str):
    role = os.path.basename(csvfilepath)[:-4]
    with open(csvfilepath) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        userlist = list(csvreader)
        userlist = list(filter(None, userlist))[1:]  # filter out any empty/whitespace lines and the first header line
        userlist_count = len(userlist)
        userlist_index = 0

        for current_details in userlist:
            print(str(userlist_index + 1) + " of " + str(userlist_count) + " (" + current_details[USERNAME] + "): ",
                  end="")
            # First, create the account
            try:
                if role == "superusers":
                    new_user_account = User.objects.create_superuser(
                        username=current_details[USERNAME],
                        email=current_details[EMAIL],
                        password=current_details[PASSWORD],
                        first_name=current_details[FIRST_NAME],
                        last_name=current_details[LAST_NAME],
                    )  # User object is created; doesn't require manual saving.
                else:
                    new_user_account = User.objects.create_user(
                        username=current_details[USERNAME],
                        email=current_details[EMAIL],
                        password=current_details[PASSWORD],
                        first_name=current_details[FIRST_NAME],
                        last_name=current_details[LAST_NAME],
                    )  # User object is created; doesn't require manual saving.
                print("Account created. ", end='')
            except Exception as e:
                print(f"Failed! Account was NOT created. Reason: {e}")
                sys.exit()
            # Second, do additional operations such as groups, profiles, etc.
            if role == "superusers" or role == "researchers":
                Group.objects.get(name='Researchers').user_set.add(new_user_account)
                print("Added to Researchers. ")
            elif role == "linkworkers":
                Group.objects.get(name='Linkworkers').user_set.add(new_user_account)
                print("Added to Linkworkers. ", end='')
                new_user_profile = UserProfile.objects.create(
                    user=new_user_account,
                    role="LNK",
                    # image=getRandomImage(),
                )
                print("Profile created. ", end='')
                new_linkworker_record = Linkworker.objects.create(
                    linkworker=new_user_profile)  # Create a Linkworker record
                print("Linkworker created. ")
            elif role == "pacs":
                Group.objects.get(name='PACs').user_set.add(new_user_account)
                print("Added to PACs. ", end='')
                new_user_profile = UserProfile.objects.create(
                    user=new_user_account,
                    role="PAC",
                    # image=getRandomImage(),
                )
                print("Profile created. ", end='')
                new_pac_record = Person_at_centre.objects.create(user_profile=new_user_profile)  # Create a PAC record
                print("PAC created. ")
            else:
                Group.objects.get(name='Supporters').user_set.add(new_user_account)
                print("Added to Supporters group, as no role was detected. ", end='')
                # raise ValueError("Role detection came up with something unknown.")
                new_user_profile = UserProfile.objects.create(
                    user=new_user_account,
                    role="SUP",
                    # image=getRandomImage(),
                )
                print("Profile created. ", end='')
                new_supporter_record = Supporter.objects.create(
                    user_profile=new_user_profile)  # Create a Supporter record
                print("Supporter created. ")
            userlist_index += 1
        print("Import finished.")
        addusers()


def addusers():
    cls()
    print(f"CSV files for import can be found in {INSTALL_DIR}/SETUP/imports/")
    print("Edit these files to include details of the users you want to import.\n")
    options = ["Import Superusers from CSV",
               "Import Researchers from CSV",
               "Import Linkworkers from CSV",
               "Import Persons-At-Centre (PACs) from CSV",
               "Import Supporters from CSV",
               "Return to previous menu"
               ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        importsourcecsvfile = os.path.join(INSTALL_DIR, "SETUP/imports/superusers.csv")
        import_users(csvfilepath=importsourcecsvfile)
    elif menu_entry_index == 1:
        importsourcecsvfile = os.path.join(INSTALL_DIR, "SETUP/imports/researchers.csv")
        import_users(csvfilepath=importsourcecsvfile)
    elif menu_entry_index == 2:
        importsourcecsvfile = os.path.join(INSTALL_DIR, "SETUP/imports/linkworkers.csv")
        import_users(csvfilepath=importsourcecsvfile)
    elif menu_entry_index == 3:
        importsourcecsvfile = os.path.join(INSTALL_DIR, "SETUP/imports/pacs.csv")
        import_users(csvfilepath=importsourcecsvfile)
    elif menu_entry_index == 4:
        importsourcecsvfile = os.path.join(INSTALL_DIR, "SETUP/imports/supporters.csv")
        import_users(csvfilepath=importsourcecsvfile)
    elif menu_entry_index == len(options) - 1:
        main()
    else:
        print(f"You have selected {options[menu_entry_index]}, which isn't coded yet.")
        # username,first_name,last_name,email,password  # You can leave this line here


def generate_fake_user(fake):
    fake_first_name = fake.first_name()
    fake_first_initial = fake_first_name[:1]
    fake_last_name = fake.last_name()
    fake_username_digits = str(random.randint(1,9999)).zfill(4)
    fake_user_name = fake_first_initial + fake_last_name + fake_username_digits
    new_user_account = User.objects.create_user(
        # username=fake.profile()["username"],
        username=fake_user_name,
        first_name=fake_first_name,
        last_name=fake_last_name,
        email=fake.profile()["mail"],
        is_active=False,  # Don't want fake users logging in
    )  # User object is created by create_user; doesn't require manual saving unless edited.
    # new_user_account.set_unusable_password()  # should be automatic anyway if no pw is specified
    # new_user_account.save()  # should be automatic anyway
    return new_user_account


def generate_fake_profile(fake, user, role):
    new_profile = UserProfile.objects.create(
        user = user,
        role = role,
        phone = fake.phone_number(),
        image = random.choice(
            [x for x in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, x))]
            )
        )
    return new_profile


def generatefakedata():
    fake = Faker()
    Faker.seed(random_generation_seed_value)  # Use a fixed value to regenerate the same data, or remove the value to randomize

    linkworker_group = Group.objects.get(name="Linkworkers")
    supporter_group = Group.objects.get(name="Supporters")
    pac_group = Group.objects.get(name="PACs")

    for i in range(fake_data_linkworker_count):
        new_linkworker_user = generate_fake_user(fake)
        new_linkworker_profile = generate_fake_profile(fake, new_linkworker_user, "linkworker")
        new_linkworker_object = Linkworker.objects.create(linkworker=new_linkworker_profile)
        linkworker_group.user_set.add(new_linkworker_user)

        for i in range(fake_data_pacs_per_linkworker):
            new_pac_user = generate_fake_user(fake)
            new_pac_profile = generate_fake_profile(fake, new_pac_user, "pac")
            new_pac_object = Person_at_centre.objects.create(user_profile=new_pac_profile)
            pac_group.user_set.add(new_pac_user)
            new_linkworker_object.pacs.add(new_pac_object)

            for i in range(fake_data_supporters_per_pac):
                new_supporter_user = generate_fake_user(fake)
                new_supporter_profile = generate_fake_profile(fake, new_supporter_user, "supporter")
                new_supporter_object = Supporter.objects.create(user_profile=new_supporter_profile)
                supporter_group.user_set.add(new_supporter_user)
                # new_pac_object.add(new_supporter_object)
                if i == 0:
                    new_pac_object.circle_of_support_2.add(new_supporter_object)
                else:
                    new_pac_object.circle_of_support_1.add(new_supporter_object)

            initial_time = timezone.now() - timedelta(hours=(fake_data_mood_days_per_pac * 24))
            allsupporters = new_pac_object.get_all_circle_supporters()
            with freeze_time(initial_time) as frozen_time:
                for m in range(fake_data_mood_days_per_pac):
                    new_mood = Moods.objects.create(
                        user=new_pac_profile,
                        current_mood=get_random_mood(),
                        )
                    frozen_time.tick(delta=timedelta(hours=12))
                    new_wellbeing = Moods.objects.create(
                        user = new_pac_profile,
                        current_mood = get_random_mood(),
                        time = timezone.now(),
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
                            mood=new_wellbeing,
                            whatdoing=get_random_pastime(),
                            )
                        new_pastime.whowith.set(random.sample(allsupporters, k=random.randrange(0, 4)))
                        new_pastime.save()
                    frozen_time.tick(delta=timedelta(hours=12))
    main()


def builddocker():
    if settings.DEBUG:
        print("************************************************************")
        print("WARNING: The DEBUG setting is set to True. ")
        print("Do not use this server on the open internet. ")
        print("Reconfigure or edit settings and set DEBUG = False first.")
        print("************************************************************")
        print("")
        if input("Enter \"YES\" to proceed, or anything else to abort: ") != "YES":
            sys.exit("Aborted at user request. (You didn't enter \"YES\")")
    print("You must have the Docker Desktop app or Docker daemon running to build images.")
    print("\nAttempting to build Docker image...")
    os.chdir(INSTALL_DIR)
    dockerbuildpath = os.path.join(INSTALL_DIR, "build_service_image.sh")
    os.system("source " + dockerbuildpath)
    launchservicepath = os.path.join(INSTALL_DIR, "launch_service_image.sh")
    print(f"Image created. Run {launchservicepath} to instantiate it.")
    sys.exit()


def instantiatedocker():
    print("You must have the Docker Desktop app or Docker daemon running.")
    print("\nAttempting to instantiate container basked on default Docker image...")
    os.chdir(INSTALL_DIR)
    launchservicepath = os.path.join(INSTALL_DIR, "launch_service_image.sh")
    os.system("source " + launchservicepath)
    sys.exit()


def runlocal():
    print("Running the local server (without Docker).")
    print("\nIt may take a few moments before the webserver responds.")
    os.chdir(DJANGO_DIR)
    os.system("python manage.py runserver")
    sys.exit()


def main():
    # cls()
    print(f"Installation directory: {INSTALL_DIR}")

    # Create and populate (if necessary) required directories.
    ensuredirectoryexists(os.path.join(INSTALL_DIR, "covid_stretch", "DATABASE"))

    ensuredirectoryexists(os.path.join(INSTALL_DIR, "covid_stretch", "MEDIA"))
    # If the MEDIA dir is empty, then put the default files in it.
    if not os.listdir(path=os.path.join(INSTALL_DIR, "covid_stretch", "MEDIA")):
        print("The MEDIA folder is empty. Copying default media files into MEDIA directory.")
        if os.name == 'nt':  # Cope with both Windows and mature OSs
            os.system('copy templates\\MEDIA_template\\*.* ..\\covid_stretch\\MEDIA\\')
        else:
            os.system('cp templates/MEDIA_template/* ../covid_stretch/MEDIA/')

    ensuredirectoryexists(os.path.join(INSTALL_DIR, "covid_stretch", "STATIC"))
    # If the STATIC dir is empty, then run Django's collectstatic routine.
    if not os.listdir(path=os.path.join(INSTALL_DIR, "covid_stretch", "STATIC")):
        print("The STATIC cache folder is empty. Collecting static files. This may take a few minutes...")
        os.system("python3 " + managepypath + " collectstatic")

    if os.path.isfile(path=os.path.join(DJANGO_DIR, "DATABASE", "db.sqlite3")):
        print("A database already exists and will be used.\n")
    else:
        print("No database currently exists. Creating a new one.")
        print("Making migrations...")
        os.system("python3 " + managepypath + " makemigrations")
        print("Migrating... ")
        os.system("python3 " + managepypath + " migrate")

    # Create (if necessary) required groups
    try:
        for group in ["Researchers", "Linkworkers", "PACs", "Supporters"]:
            new_group, created = Group.objects.get_or_create(name=group)
            # Returns a tuple where first item is the group, and second is a
            # boolean indicating whether it was created (True) or extant (False).
            if created:
                print("Created group: ", new_group.name)
            else:
                print("Found existing group: ", new_group.name)
    except Exception as e:
        print(f"!!! Couldn't create groups: {e}")

    print("\nInitial checks complete. Proceeding with configuration.\n\n")

    options = ["Configure a new SERVICE installation for the first time",
               "Import additional users from CSV files",
               "Generate example (fake) Linkworkers, PACs, supporters, moods, and wellbeing data",
               "Run a local server (without Docker)",
               "Build a Docker image from your current working installation",
               "Start a new Docker container based on the image built using the above option",
               "Quit"
               ]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        new_installation()
    elif menu_entry_index == 1:
        addusers()
    elif menu_entry_index == 2:
        generatefakedata()
    elif menu_entry_index == 3:
        runlocal()
    elif menu_entry_index == 4:
        builddocker()
    elif menu_entry_index == 5:
        instantiatedocker()
    elif menu_entry_index == len(options) - 1:
        sys.exit()
    else:
        print(f"You have selected {options[menu_entry_index]}, which isn't coded yet.")


##############################################################################
if __name__ == "__main__":
    main()
