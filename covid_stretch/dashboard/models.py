# models.py in dashboard
# This file contains classes which extend the default User class defined in django.contrib.auth.models.

# UserProfile adds additional data to the user base class like telephone number.

# The UserProfile class is then extended by both linkworker and client class. Didnt bother
# with supporter class as this can be acheived by just using UserProfile as a supporter has no real functionality.

# Linkworker class contains linkworker details and an unlimited number of clients
# Person_at_centre class contains the person at centre and an unlimited amount of supporters.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phone_field import PhoneField

ROWS_TO_SHOW_CHOICES = (
    (3, "3"),
    (6, "6"),
    (9, "9"),
    (15, "15"),
    (30, "30"),
    (100, "100"),
    (250, "250"),
    (500, "500"),
    (99999, "All (slow)"),
    )


class UserPreferences(models.Model):
    username = models.CharField(max_length=10, blank=False)
    rowsToDisplay = models.PositiveIntegerField(choices=ROWS_TO_SHOW_CHOICES, blank=True, default=6)
    gotoPage = models.PositiveSmallIntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
