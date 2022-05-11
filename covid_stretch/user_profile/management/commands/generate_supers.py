# command that can be called by manage.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.apps import apps
from django.core import management


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        researcher_group = Group.objects.get(name='Researchers')
        print("Generating super-user accounts...")

        # To add a super-user to the system, add two lines like the following.
        # The variable name ("paul") isn't important as long as it's not re-used 
        # between the two lines, and is identical on both lines.
        # 
        # paul = User.objects.create_superuser(username="paul", email="paul@service.org", password="Paul has left the project.")
        # researcher_group.user_set.add(paul)

        sysadmin = User.objects.create_superuser(username="sysadmin", email="Jef.Lay@open.ac.uk", password="correcthorsebatterystaple", first_name="System", last_name="Administrator")
        researcher_group.user_set.add(sysadmin)

        jef = User.objects.create_superuser(username="jef", email="Jef.Lay@open.ac.uk", password="maqQuw-tuspum-8sergo", first_name="Jef", last_name="Lay")
        researcher_group.user_set.add(jef)

        hk = User.objects.create_superuser(username="henryk", email="STEM-SERVICE-Project@open.ac.uk", password="2U8UDGd9dYB8", first_name="Henryk", last_name="Krajinski")
        researcher_group.user_set.add(hk)


        print("Created super-user accounts.")
