# Moods is a data base of mood reading recived into the system, this could befromn a physical mood device
# or a digital smart app.
#
import random

from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
from user_profile.models import UserProfile, Supporter

# NO_MOOD = "NM"
# HAPPY_MOOD = "HP"
# BORED_MOOD = "BD"
# SAD_MOOD = "SD"
# ANNOYED_MOOD = "AN"
# NERVOUS_MOOD = "NV"
# EXCITED_MOOD = "EX"
# RELAXED_MOOD = "RX"
# CALM_MOOD = "CL"
ANGRY_MOOD = "ANGR"
AFRAID_MOOD = "AFRA"
ASTONISHED_MOOD = "ASTO"
EXCITED_MOOD = "EXCI"
HAPPY_MOOD = "HAPP"
FRUSTRATED_MOOD = "FRUS"
TENSE_MOOD = "TENS"
ALARMED_MOOD = "ALAR"
DELIGHTED_MOOD = "DELI"
GLAD_MOOD = "GLAD"
DISTRESSED_MOOD = "DIST"
ANNOYED_MOOD = "ANNO"
NEUTRAL_MOOD = "NEUT"
PLEASED_MOOD = "PLEA"
CONTENT_MOOD = "CONT"
DEPRESSED_MOOD = "DEPR"
MISERABLE_MOOD = "MISR"
SLEEPY_MOOD = "SLEEP"
AT_EASE_MOOD = "ATEA"
SATISFIED_MOOD = "SATI"
BORED_MOOD = "BORE"
SAD_MOOD = "SAD"
TIRED_MOOD = "TIRE"
CALM_MOOD = "CALM"
RELAXED_MOOD = "RELA"

MOOD_CLOCK_DEVICE = "MCD"
MOOD_BOARD_DEVICE = "MBD"
APP_MOOD_CLOCK_DEVICE = "AMD"

MOOD_CHOICES = (
    # (HAPPY_MOOD, "happy"),
    # (BORED_MOOD, "bored"),
    # (SAD_MOOD, "sad"),
    # (ANNOYED_MOOD, "annoyed"),
    # (NERVOUS_MOOD, "nervous"),
    # (EXCITED_MOOD, "excited"),
    # (RELAXED_MOOD, "relaxed"),
    # (CALM_MOOD, "calm")
    (ANGRY_MOOD, "angry"),
    (AFRAID_MOOD, "afraid"),
    (ASTONISHED_MOOD, "astonished"),
    (EXCITED_MOOD, "excited"),
    (HAPPY_MOOD, "happy"),
    (FRUSTRATED_MOOD, "frustrated"),
    (TENSE_MOOD, "tense"),
    (ALARMED_MOOD, "alarmed"),
    (DELIGHTED_MOOD, "delighted"),
    (GLAD_MOOD, "glad"),
    (DISTRESSED_MOOD, "distressed"),
    (ANNOYED_MOOD, "annoyed"),
    (NEUTRAL_MOOD, "neutral"),
    (PLEASED_MOOD, "pleased"),
    (CONTENT_MOOD, "content"),
    (DEPRESSED_MOOD, "depressed"),
    (MISERABLE_MOOD, "miserable"),
    (SLEEPY_MOOD, "sleepy"),
    (AT_EASE_MOOD, "at ease"),
    (SATISFIED_MOOD, "satisfied"),
    (BORED_MOOD, "bored"),
    (SAD_MOOD, "sad"),
    (TIRED_MOOD, "tired"),
    (CALM_MOOD, "calm"),
    (RELAXED_MOOD, "relaxed")
    )

PASTIME_CHOICES = (
    ("", "Unspecified"),
    ("TV", "TV"),
    ("EXER", "Exercise"),
    ("ART", "Arts & Crafts"),
    ("COOK", "Cooking"),
    ("READ", "Reading"),
    ("SOC", "Socialising"),
    ("GARD", "Gardening"),
    ("COMP", "Computer"),
    ("HYG", "Hygiene"),
    ("CLEN", "Cleaning"),
    ("VOL", "Volunteering"),
    ("MUS", "Music"),
    ("WORK", "Working"),
    ("HELP", "Helping"),
    ("OTHER", "Other")
)

# in prep for mood board
MOOD_DEVICE = (
    (MOOD_CLOCK_DEVICE, "Mood Clock"),
    (MOOD_BOARD_DEVICE, "Mood Board"),
    (APP_MOOD_CLOCK_DEVICE, "App_mood")
    )


def get_random_mood():
    choice = random.choice(MOOD_CHOICES)
    return choice[0]


def get_random_pastime():
    choice = random.choice(PASTIME_CHOICES)
    # choice = random.choices(PASTIME_CHOICES, weights=[0,1,1,1,1,1,1,1,1,1,1])
    return choice[0]


def is_a_mood(mood):
    return_value = False
    for m in MOOD_CHOICES:
        if m[0] == mood:
            return_value = True
    return return_value


def is_a_pastime(pastime):
    return_value = False
    for m in PASTIME_CHOICES:
        if m[0] == pastime:
            return_value = True
    return return_value


class Moods(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    current_mood = models.CharField(max_length=24, choices=MOOD_CHOICES, default=NEUTRAL_MOOD)
    # in prep for mood board
    # mood_device = models.CharField(max_length=24, choices=MOOD_DEVICE, default=MOOD_CLOCK_DEVICE)
    time = models.DateTimeField(default=timezone.now)

    # Further fields used for full Wellbeing record
    include_wellbeing = models.BooleanField(default=False, null=True, blank=True)
    wellbeing = models.IntegerField(null=True, blank=True)
    previouswellbeing = models.IntegerField(null=True, blank=True)
    loneliness = models.IntegerField(null=True, blank=True)
    previousloneliness = models.IntegerField(null=True, blank=True)
    # whatdoing = MultiSelectField(choices=PASTIME_CHOICES, max_choices=9, max_length=9, null=True, blank=True)
        # models.CharField(max_length=4, choices=PASTIME_CHOICES, default="", null=True, blank=True)
    spoketosomeone = models.BooleanField(default=False, null=True, blank=True)
    spoketosomeone_who = models.CharField(max_length=256, null=True, blank=True)
    hours_bed = models.IntegerField(null=True, blank=True)
    hours_sofa = models.IntegerField(null=True, blank=True)
    hours_kitchen = models.IntegerField(null=True, blank=True)
    hours_garden = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.current_mood} - {self.time}"

    def get_pastimes(self):
        pastimes = Pastime.objects.filter(mood=self)
        return pastimes

    def add_pastime(self, whatdoing, supporterlist):
        new_pastime = Pastime.objects.create(
            mood=self,
            whatdoing=whatdoing
        )
        supporterlist = []
        for supporter_id in supporterlist:
            supporterlist.append(Supporter.objects.get(id=supporter_id))
        new_pastime.whowith.set(supporterlist)
        new_pastime.save()
        # print("--- Saved new pastime object: " + str(new_pastime.id) + " - " + str(new_pastime.whatdoing) + " - " + str(supporterlist))
        return new_pastime


class Pastime(models.Model):
    mood = models.ForeignKey(Moods, on_delete=models.CASCADE, related_name="pastimes")
    whatdoing = models.CharField(max_length=5, choices=PASTIME_CHOICES, default="", null=True, blank=True)
    whowith = models.ManyToManyField(Supporter)

    def __str__(self):
        allsupporters=self.whowith.all()
        supporterlist = []
        for onesupporter in allsupporters:
            supporterlist.append(onesupporter.user_profile.user.first_name + " " + onesupporter.user_profile.user.last_name + " (supporter id " + str(onesupporter.id) + ")" )
        if len(supporterlist):
            tmpsupporterliststring = " with " + str(supporterlist)
        else:
            tmpsupporterliststring = ""
        tmppastimestring = str(self.whatdoing) + tmpsupporterliststring + "."
        return tmppastimestring
