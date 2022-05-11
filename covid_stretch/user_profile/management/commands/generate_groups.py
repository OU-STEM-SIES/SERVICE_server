# command that can be called by manage.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.apps import apps


GROUPS = ["Researchers", "Linkworkers","PACs", "Supporters"]

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            print("Created Group : ", new_group.name)

       
        


 

                

            
                