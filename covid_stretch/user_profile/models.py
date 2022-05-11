import random

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
from phone_field import PhoneField

HOW_OFTEN_EXPECTED_INTERACTION_CHOICES = (
    (1, "Daily"),
    (2, "Weekly"),
    (3, "Fortnightly"),
    (4, "Monthly"),
    (5, "Yearly")
)

class UserProfile(models.Model):
    PERSON_AT_CENTRE = "PAC"
    LINKWORKER = "LNK"
    SUPPORTER = "SUP"
    ADMIN = "ADM"
    NO_ROLE = "NOR"
    
    ROLE_CHOICES = (
        (PERSON_AT_CENTRE, "pac"),
        (LINKWORKER, "linkworker"),
        (SUPPORTER, "supporter"),
        (ADMIN, "admin"),
        )
    
    GENDER_CHOICES = (
        ("WOM", "Woman"),
        ("MAN", "Man"),
        ("NBIN", "Non-binary"),
        ("PNTD", "Prefer not to disclose"),
        ("PTSD", "Prefer to self describe")
        )
    
    ETHNIC_CHOICES = (
        ("WHTE", "White"),
        ("MXED", "Mixed/Multiple ethnic groups"),
        ("ASIN", "Asian/Asian British"),
        ("BLCK", "Black/African/Caribbean/Black British"),
        ("CHIN", "Chinese"),
        ("ARAB", "Arab"),
        ("OTHR", "Other")
        )
    
    EDUCATION_CHOICES = (
        ("NONE", "No qualifications"),
        ("GCE1", "1-4 GCSEs, Scottish Standard Grade"),
        ("GCE5", "5 or more GCSEs, Scottish Higher, Scottish Advanced Higher"),
        ("APRT", "Apprenticeship"),
        ("ALEV", "2 or more A-levels, HNC, HND, SVQ level 4"),
        ("DEGR", "First or higher degree"),
        ("OTHR", "Other vocational / work related qualifications")
        )
    
    # https://meassociation.org.uk/2016/05/the-mea-disability-rating-scale-2016/
    DISABILITY_CHOICES = (
        ("NONE", "No disability"),
        ("MILD", "Mild to moderate disability"),
        ("MODD", "Moderate disability"),
        ("SVDS", "Severe disability"),
        ("VERY", "Very severe disability")
        )
    
    # ONS data
    HEALTH_CHOICES = (
        ("0", "No health problems"),
        ("1", "Arms or hands"),
        ("2", "Back or neck"),
        ("3", "Difficulty in seeing"),
        ("4", "Difficulty in hearing"),
        ("5", "Speech impediment"),
        ("6", "Skin conditions, allergies"),
        ("7", "Chest, breathing problems"),
        ("8", "Heart, blood, blood pressure, circulation"),
        ("9", "Stomach, liver, kidney, digestion"),
        ("10", "Diabetes"),
        ("11", "Depression, bad nerves"),
        ("12", "Epilepsy"),
        ("13", "Learning difficulties"),
        ("14", "Mental illness, phobia, panics"),
        ("15", "Progressive illness n.e.c."),
        ("16", "Other problems, disabilities")
        )
    
    # https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/populationestimatesbymaritalstatusandlivingarrangements/2002to2016
    MARITAL_CHOICES = (
        ("SING", "Single, never married or civil partnered"),
        ("MARR",
         "Married, including separated (this category includes those in both opposite-sex and same-sex marriages)"),
        ("CIVL", "Civil partnered, including separated "),
        ("DIVD", "Divorced, including legally dissolved civil partners"),
        ("WIDO", "Widowed, including surviving civil partners")
        )

    SOCIAL_GROUPS_CHOICES = (
        ("FAML", "Family"),
        ("FRND", "Friends"),
        ("SOCL", "Social club"),
        ("SPRT", "Sport"),
        ("PROF", "Professional"),
        ("VOLN", "Voluntary"),
        ("LEAR", "Learning"),
        ("NBOR", "Neighbourhood"),
        ("FATH", "Faith"),
        ("POLI", "Political"),
        ("OTHR", "Other group")
    )

    LIKES_DISLIKES_CHOICES = (
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
    )

    BOND_CHOICES = ( #zip(range(0, 8), range(0, 8))
        (None, "No answer"),
        (1, "1 - Very distant"),
        (2, "2 - Somewhat distant"),
        (3, "3 - Slightly distant"),
        (4, "4 - Neither close nor distant"),
        (5, "5 - Slightly close"),
        (6, "6 - Somewhat close"),
        (7, "7 - Very close"),

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default=SUPPORTER, blank=True, null=True)
    phone = PhoneField(help_text="Contact phone number", blank=True, null=True)
    image = models.ImageField(default="1.jpg", blank=True, null=True)
    date_of_birth = models.DateField(default=timezone.now, blank=True, null=True)
    gender = models.CharField(max_length=4, choices=GENDER_CHOICES, default="PTSD")
    ethnicity = models.CharField(max_length=4, choices=ETHNIC_CHOICES, default="OTHR")
    education = models.CharField(max_length=4, choices=EDUCATION_CHOICES, default="NONE")
    disability = models.CharField(max_length=4, choices=DISABILITY_CHOICES, default="NONE")
    marital_status = models.CharField(max_length=4, choices=MARITAL_CHOICES, default="SING")
    smoking = models.BooleanField(default=False)
    alcohol_units_per_week = models.PositiveIntegerField(choices=zip(range(0, 251), range(0, 251)),default=0)
    # https://pypi.org/project/django-multipleselectfield/
    health_conditions = MultiSelectField(choices=HEALTH_CHOICES, max_choices=15, max_length=3, default="0")
    things_liked = models.CharField(max_length=4, choices=LIKES_DISLIKES_CHOICES, default="")
    things_disliked = models.CharField(max_length=4, choices=LIKES_DISLIKES_CHOICES, default="")
    family_has = models.BooleanField(default=False)
    family_bond = models.IntegerField(choices=BOND_CHOICES, null=True, blank=True)
    community_bond = models.IntegerField(choices=BOND_CHOICES, null=True, blank=True)
    social_groups = models.CharField(max_length=4, choices=SOCIAL_GROUPS_CHOICES, blank=True, null=True)
    social_group_other = models.CharField(max_length=32, blank=True, null=True)
    social_bond = models.IntegerField(choices=BOND_CHOICES, null=True, blank=True)
    link_worker_has = models.BooleanField(default=False)
    link_worker_bond = models.IntegerField(choices=BOND_CHOICES, null=True, blank=True)
    # TODO: Privacy fields to follow
    
    def get_full_name(self):
        fn = self.user.first_name + " " + self.user.last_name
        return fn
    
    def is_linkworker(self):
        ret = False
        if self.role == self.LINKWORKER:
            ret = True
        return ret
    
    def is_supporter(self):
        ret = False
        if self.role == self.SUPPORTER:
            ret = True
        return ret
    
    def is_pac(self):
        ret = False
        if self.role == self.PERSON_AT_CENTRE:
            ret = True
        return ret
    
    def get_user_details(self):
        return "Name: {} UserName: {}".format(self.user.get_full_name(), self.user.username)
    
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return self.get_user_details()
    
    def randomise_personal_details(self):
        self.gender = random.choice(self.GENDER_CHOICES)[0]
        self.ethnicity = random.choice(self.ETHNIC_CHOICES)[0]
        self.education = random.choice(self.EDUCATION_CHOICES)[0]
        self.disability = random.choice(self.DISABILITY_CHOICES)[0]
        self.marital_status = random.choice(self.MARITAL_CHOICES)[0]
        self.smoking = random.choice([True, False])
        self.alcohol_units_per_week = random.randrange(30)
        self.health_conditions = random.choice(self.HEALTH_CHOICES)[0]
        # choices above this line were commented out until multi-user-pastimes were added
        self.things_liked = random.choice(self.LIKES_DISLIKES_CHOICES)[0]
        self.things_disliked = random.choice(self.LIKES_DISLIKES_CHOICES)[0]
        self.family_has = random.choice([True, False])
        self.family_bond = random.randrange(7)
        self.community_bond = random.randrange(7)
        self.social_groups = random.choice(self.SOCIAL_GROUPS_CHOICES)[0]
        self.social_group_other = random.choice(self.SOCIAL_GROUPS_CHOICES)[0]
        self.social_bond = random.randrange(7)
        self.link_worker_has = random.choice([True, False])
        self.link_worker_bond = random.randrange(7)


class Supporter(models.Model):
    SOCIAL_GROUPS_CHOICES = (
        ("FAML", "Family"),
        ("FRND", "Friends"),
        ("SOCL", "Social club"),
        ("SPRT", "Sport"),
        ("PROF", "Professional"),
        ("VOLN", "Voluntary"),
        ("LEAR", "Learning"),
        ("NBOR", "Neighbourhood"),
        ("FATH", "Faith"),
        ("POLI", "Political"),
        ("OTHR", "Other group")
    )

    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="supporters")
    group = models.CharField(max_length=4, choices=SOCIAL_GROUPS_CHOICES, blank=True, null=True)
    how_often_expected_interaction = models.IntegerField(choices=HOW_OFTEN_EXPECTED_INTERACTION_CHOICES, null=True, blank=True)
    user_profile.role = UserProfile.SUPPORTER


class Person_at_centre(models.Model):
    MOOD_STATUS_NEW = "NEW"  # this is a new account - no mood yet
    MOOD_STATUS_NORMAL = "NRM"  # Normal mode - moods are regularly updated
    MOOD_STATUS_DORMANT = "DRM"  # Dormant - client not responding
    MOOD_STATUS_REQUIRES_UPDATE = "UPD"  # Person_at_centre needs to add a new mood reading
    
    MOOD_STATUS_CHOICES = (
        (MOOD_STATUS_NEW, "new"),
        (MOOD_STATUS_NORMAL, "normal"),
        (MOOD_STATUS_DORMANT, "dormant"),
        (MOOD_STATUS_REQUIRES_UPDATE, "update"),
        )
    
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="my_clients")
    supporters = models.ManyToManyField(Supporter, related_name="my_supporters")
    status = models.CharField(max_length=3, choices=MOOD_STATUS_CHOICES, default=MOOD_STATUS_NEW)
    
    circle_of_support_1 = models.ManyToManyField(Supporter, related_name="circle1", blank=True)
    circle_of_support_2 = models.ManyToManyField(Supporter, related_name="circle2", blank=True)
    circle_of_support_3 = models.ManyToManyField(Supporter, related_name="circle3", blank=True)

    user_profile.role = UserProfile.PERSON_AT_CENTRE

    def get_circle_of_support_1(self, index):
        array = self.circle_of_support_1.all()
        if index < len(array) and index >= 0:
            return array[index]
        else:
            return None

    def get_circle_of_support_2(self, index):
        array = self.circle_of_support_2.all()
        if index < len(array) and index >= 0:
            return array[index]
        else:
            return None

    def get_circle_of_support_3(self, index):
        array = self.circle_of_support_3.all()
        if index < len(array) and index >= 0:
            return array[index]
        else:
            return None

    def get_all_circle_supporters(self):
        result = []
        result.extend (list(self.circle_of_support_1.all()))
        result.extend (list(self.circle_of_support_2.all()))
        result.extend (list(self.circle_of_support_3.all()))
        return result

    # def get_supporter(self, index):
    #     array = self.supporters.all()
    #     if index < len(array) and index >= 0:
    #         return array[index]
    #     else:
    #         return None

    def get_client_details(self):
        supporter_details = ""
        array = self.supporters.all()
        for supporter in array:
            supporter_details += supporter.user_profile.get_full_name() + ", "
        return self.get_client_details()


class Linkworker(models.Model):
    linkworker = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="key")
    pacs = models.ManyToManyField(Person_at_centre, related_name="list_of_clients")
    linkworker.role = UserProfile.LINKWORKER
    
    def get_linkworker_details(self):
        client_details = ""
        array = self.pacs.all()
        for client in array:
            client_details += client.user_profile.get_full_name() + ", "
        
        return "Linkworker: {} Person_at_centres: {}".format(self.linkworker.get_full_name(), client_details)
    
    def __str__(self):
        return self.get_linkworker_details()


class UserLog(models.Model):
    LOG_ENTRY_TYPES = (
        ("COFU", "User updated their Circle Of Friends"),
        ("PROF", "User updated their profile"),
        ("PSWD", "User changed their password (password is not logged)"),
        # ("PRES", "User requested a password reset email"),
        ("DELE", "User and associated data deleted"),
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=4, choices=LOG_ENTRY_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=128)
    prediffjson = models.JSONField(max_length=65535, blank=True, null=True)
    postdiffjson = models.JSONField(max_length=65535, blank=True, null=True)
