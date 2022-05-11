import random

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

EMOTIONAL_SUPPORT_SCALE_MIN = 1
EMOTIONAL_SUPPORT_SCALE_MAX = 10
EMOTIONAL_SUPPORT_DEFAULT = 1


def get_random_emotional_support_value():
    return random.randint(EMOTIONAL_SUPPORT_SCALE_MIN, EMOTIONAL_SUPPORT_SCALE_MAX)


class Emotional_status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    loneliness_level = models.IntegerField(
            default=EMOTIONAL_SUPPORT_DEFAULT,
            validators=[
                MaxValueValidator(EMOTIONAL_SUPPORT_SCALE_MAX),
                MinValueValidator(EMOTIONAL_SUPPORT_SCALE_MIN)
                ])
    general_wellbeing = models.IntegerField(
            default=EMOTIONAL_SUPPORT_DEFAULT,
            validators=[
                MaxValueValidator(EMOTIONAL_SUPPORT_SCALE_MAX),
                MinValueValidator(EMOTIONAL_SUPPORT_SCALE_MIN)
                ])

    def __str__(self):
        return f"{self.user.get_full_name()}: Loneliness = {self.loneliness_level} Wellbeing = {self.general_wellbeing} @ {self.time}"
