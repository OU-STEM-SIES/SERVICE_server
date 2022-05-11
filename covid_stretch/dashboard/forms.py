from django import forms  # import ModelForm, Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserPreferences
from user_profile.models import UserProfile

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

class UserAccountForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(UserAccountForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["phone", "date_of_birth", "gender", "ethnicity", "education",
                  "disability", "marital_status", "smoking", "alcohol_units_per_week",
                  "health_conditions", "things_liked", "things_disliked", "family_has",
                  "family_bond", "community_bond", "social_groups", "social_group_other",
                  "social_bond", "link_worker_has", "link_worker_bond"]  #, "image"]
        # fields = '__all__'

        labels = {
            'phone': 'Contact telephone number (optional)',
            'date_of_birth': 'When were you born?',
            'gender': 'What gender do you identify as?',
            'ethnicity': "Your ethnicity?",
            'education': "Your highest educational achievement?",
            'disability': 'Accessibility & disabilities',
            'marital_status': 'Your marital status',
            'smoking': "Check this box if you're a smoker",
            'alcohol_units_per_week': 'How many units of alcohol do you consume in an average week?',
            'health_conditions': 'Do you currently have any health conditions?',
            'things_liked': 'Do you particularly enjoy any of these activities?',
            'things_disliked': 'Do you particularly avoid any of these activities?',
            'family_has': 'Check this box if you have any close family members',
            'family_bond': 'How close do you feel to those family members?',
            'community_bond': 'How close do you feel to members of your local community?',
            'social_groups': 'Are you a member of any specific social groups?',
            'social_group_other': 'If you selected "other", please tell us more...',
            'social_bond': 'How close do you feel to this social group?',
            'link_worker_has': 'Check this box if you have a link worker assigned to you',
            'link_worker_bond': 'How close do you feel to that link worker?',
            'image': 'Select an image to represent yourself'
        }

        help_texts = {
           'phone': "",
        }

        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=range(1900,2004), empty_label=("Choose Year", "Choose Month", "Choose Day")),
            # 'staffTitle': forms.ComboField(attrs={'class': 'form-control'}),
            # 'staffSurname': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }

        error_messages = {
            'social_group_other': {
                'max_length': 'This information is too long, please summarise.',
            }
        }

    # phone = PhoneField(help_text="Contact phone number", blank=True, null=True)
    # image = models.ImageField(default="1.jpg", blank=True, null=True)
    # date_of_birth = models.DateField(default=timezone.now, blank=True, null=True)
    # gender = models.CharField(max_length=4, choices=GENDER_CHOICES, default="PTSD")
    # ethnicity = models.CharField(max_length=4, choices=ETHNIC_CHOICES, default="OTHR")
    # education = models.CharField(max_length=4, choices=EDUCATION_CHOICES, default="NONE")
    # disability = models.CharField(max_length=4, choices=DISABILITY_CHOICES, default="NONE")
    # marital_status = models.CharField(max_length=4, choices=MARITAL_CHOICES, default="SING")
    # smoking = models.BooleanField(default=False)
    # alcohol_units_per_week = models.PositiveIntegerField(default=0)
    # # https://pypi.org/project/django-multipleselectfield/
    # health_conditions = MultiSelectField(choices=HEALTH_CHOICES, max_choices=15, max_length=3, default="0")
    # things_liked = models.CharField(max_length=4, choices=LIKES_DISLIKES_CHOICES, default="")
    # things_disliked = models.CharField(max_length=4, choices=LIKES_DISLIKES_CHOICES, default="")
    # family_has = models.BooleanField(default=False)
    # family_bond = models.IntegerField(null=True, blank=True)
    # community_bond = models.IntegerField(null=True, blank=True)
    # social_groups = models.CharField(max_length=4, choices=SOCIAL_GROUPS_CHOICES, blank=True, null=True)
    # social_group_other = models.CharField(max_length=32, blank=True, null=True)
    # social_bond = models.IntegerField(null=True, blank=True)
    # link_worker_has = models.BooleanField(default=False)
    # link_worker_bond = models.IntegerField(null=True, blank=True)


class UserPreferencesForm(forms.ModelForm):
    rowsToDisplay = forms.ChoiceField(choices=ROWS_TO_SHOW_CHOICES, required=False)
    gotoPage = forms.IntegerField(required=False)
    
    class Meta:
        model = UserPreferences
        fields = ['rowsToDisplay',
                  'gotoPage',
                  ]
        labels = {
            'id'           : 'Record ID',
            'rowsToDisplay': 'Rows to show',
            'gotoPage'     : 'Go to page',
            }
        help_texts = {
            'rowsToDisplay': "Showing the full list is slow. Select how many rows to show at once.",
            'gotoPage'     : "Jump straight to the specified page",
            }
        widgets = {
            'rowsToDisplay': forms.Select(),
            'gotoPage'     : forms.NumberInput(),
            }
