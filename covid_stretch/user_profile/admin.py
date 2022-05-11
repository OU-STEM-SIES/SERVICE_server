from django.contrib import admin
from .models import UserProfile, Person_at_centre, Linkworker, Supporter

admin.site.register(UserProfile)
admin.site.register(Person_at_centre)
admin.site.register(Linkworker)
admin.site.register(Supporter)
