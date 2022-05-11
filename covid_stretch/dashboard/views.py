import csv
import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.http import Http404, HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.template.defaulttags import register

from rest_framework.authtoken.models import Token

from moods.models import Moods, Pastime
from user_profile.models import Linkworker, Person_at_centre, Supporter, UserProfile, UserLog
from user_profile.serializers import UserProfileSerializer, UserSerializer
from .forms import UserPreferencesForm, UserAccountForm, UserProfileForm
from .models import UserPreferences

# TODO: Add "Allowed to view?" code, redirecting to user's own data if not
#  (e.g. one PAC trying to view another PAC's data should not be permitted)
# TODO: Make Linkworker and PAC details pages correctly deny access to lower-permission groups
# TODO: Make nav menu only show options available to the current user.
# TODO: Unify and improve export format to include linkworker details as well as PAC moods

NO_MOOD = "NONE"
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


MoodLookup = {
    # "NM": "No mood",
    # "HP": "Happy",
    # "BD": "Bored",
    # "SD": "Sad",
    # "AN": "Annoyed",
    # "NV": "Nervous",
    # "EX": "Excited",
    # "RX": "Relaxed",
    # "CL": "Calm",
    NO_MOOD: "No mood",
    ANGRY_MOOD: "Angry",
    AFRAID_MOOD: "Afraid",
    ASTONISHED_MOOD: "Astonished",
    EXCITED_MOOD: "Excited",
    HAPPY_MOOD: "Happy",
    FRUSTRATED_MOOD: "Frustrated",
    TENSE_MOOD: "Tense",
    ALARMED_MOOD: "Alarmed",
    DELIGHTED_MOOD: "Delighted",
    GLAD_MOOD: "Glad",
    DISTRESSED_MOOD: "Distressed",
    ANNOYED_MOOD: "Annoyed",
    NEUTRAL_MOOD: "Neutral",
    PLEASED_MOOD: "Pleased",
    CONTENT_MOOD: "Content",
    DEPRESSED_MOOD: "Depressed",
    MISERABLE_MOOD: "Miserable",
    SLEEPY_MOOD: "Sleepy",
    AT_EASE_MOOD: "At Ease",
    SATISFIED_MOOD: "Satisfied",
    BORED_MOOD: "Bored",
    SAD_MOOD: "Sad",
    TIRED_MOOD: "Tired",
    CALM_MOOD: "Calm",
    RELAXED_MOOD: "Relaxed"
}

MoodIconLookup = {
    # "NM": '<i class="far fa-meh-blank"></i>',
    # "HP": '<i class="far fa-grin"></i>',
    # "BD": '<i class="far fa-meh-rolling-eyes"></i>',
    # "SD": '<i class="far fa-sad-tear"></i>',
    # "AN": '<i class="far fa-angry"></i>',
    # "NV": '<i class="far fa-grimace"></i>',
    # "EX": '<i class="far fa-grin-stars"></i>',
    # "RX": '<i class="far fa-smile-beam"></i>',
    # "CL": '<i class="far fa-meh"></i>',
    NO_MOOD: '<i class="fa-regular fa-face-zipper"></i>',
    ANGRY_MOOD: '<i class="fa-regular fa-face-swear"></i>',
    AFRAID_MOOD: '<i class="fa-regular fa-face-fearful"></i>',
    ASTONISHED_MOOD: '<i class="fa-regular fa-face-astonished"></i>',
    EXCITED_MOOD: '<i class="fa-regular fa-face-grin-stars"></i>',
    HAPPY_MOOD: '<i class="fa-regular fa-face-grin"></i>',
    FRUSTRATED_MOOD: '<i class="fa-regular fa-face-confounded"></i>',
    TENSE_MOOD: '<i class="fa-regular fa-face-grimace"></i>',
    ALARMED_MOOD: '<i class="fa-regular fa-face-scream"></i>',
    DELIGHTED_MOOD: '<i class="fa-regular fa-face-awesome"></i>',
    GLAD_MOOD: '<i class="fa-regular fa-face-grin-beam"></i>',
    DISTRESSED_MOOD: '<i class="fa-regular fa-face-worried"></i>',
    ANNOYED_MOOD: '<i class="fa-regular fa-face-unamused"></i>',
    NEUTRAL_MOOD: '<i class="fa-regular fa-face-meh-blank"></i>',
    PLEASED_MOOD: '<i class="fa-regular fa-face-smile"></i>',
    CONTENT_MOOD: '<i class="fa-regular fa-face-relieved"></i>',
    DEPRESSED_MOOD: '<i class="fa-regular fa-face-disappointed"></i>',
    MISERABLE_MOOD: '<i class="fa-regular fa-face-sad-cry"></i>',
    SLEEPY_MOOD: '<i class="fa-regular fa-face-sleeping"></i>',
    AT_EASE_MOOD: '<i class="fa-regular fa-face-sunglasses"></i>',
    SATISFIED_MOOD: '<i class="fa-regular fa-face-smiling-hands"></i>',
    BORED_MOOD: '<i class="fa-regular fa-face-rolling-eyes"></i>',
    SAD_MOOD: '<i class="fa-regular fa-face-sad-tear"></i>',
    TIRED_MOOD: '<i class="fa-regular fa-face-weary"></i>',
    CALM_MOOD: '<i class="fa-regular fa-face-meh"></i>',
    RELAXED_MOOD: '<i class="fa-regular fa-face-smile-relaxed"></i>',
    }

MoodPositivityLookup = {
    # "NM": 0,
    # "HP": 2,
    # "BD": -1,
    # "SD": -2,
    # "AN": -2,
    # "NV": -1,
    # "EX": 2,
    # "RX": 1,
    # "CL": 1,
    NO_MOOD: 0,
    ANGRY_MOOD: -2,
    AFRAID_MOOD: -1,
    ASTONISHED_MOOD: 0,
    EXCITED_MOOD: 1,
    HAPPY_MOOD: 2,
    FRUSTRATED_MOOD: -2,
    TENSE_MOOD: -1,
    ALARMED_MOOD: 0,
    DELIGHTED_MOOD: 1,
    GLAD_MOOD: 2,
    DISTRESSED_MOOD: -2,
    ANNOYED_MOOD: -1,
    NEUTRAL_MOOD: 0,
    PLEASED_MOOD: 1,
    CONTENT_MOOD: 2,
    DEPRESSED_MOOD: -2,
    MISERABLE_MOOD: -1,
    SLEEPY_MOOD: 0,
    AT_EASE_MOOD: 1,
    SATISFIED_MOOD: 2,
    BORED_MOOD: -2,
    SAD_MOOD: -1,
    TIRED_MOOD: 0,
    CALM_MOOD: 1,
    RELAXED_MOOD: 2,
    }

MoodActivityLookup = {
    # "NM": 0,
    # "HP": 1,
    # "BD": -2,
    # "SD": -1,
    # "AN": 1,
    # "NV": -1,
    # "EX": 2,
    # "RX": -1,
    # "CL": 1,
    NO_MOOD: 0,
    ANGRY_MOOD: 2,
    AFRAID_MOOD: 2,
    ASTONISHED_MOOD: 2,
    EXCITED_MOOD: 2,
    HAPPY_MOOD: 2,
    FRUSTRATED_MOOD: 1,
    TENSE_MOOD: 1,
    ALARMED_MOOD: 1,
    DELIGHTED_MOOD: 1,
    GLAD_MOOD: 1,
    DISTRESSED_MOOD: 0,
    ANNOYED_MOOD: 0,
    NEUTRAL_MOOD: 0,
    PLEASED_MOOD: 0,
    CONTENT_MOOD: 0,
    DEPRESSED_MOOD: -1,
    MISERABLE_MOOD: -1,
    SLEEPY_MOOD: -1,
    AT_EASE_MOOD: -1,
    SATISFIED_MOOD: -1,
    BORED_MOOD: -2,
    SAD_MOOD: -2,
    TIRED_MOOD: -2,
    CALM_MOOD: -2,
    RELAXED_MOOD: -2,
    }

PastimeLookup = {
    "": "Unspecified",
    "TV": "TV",
    "EXER": "Exercise",
    "ART": "Arts & Crafts",
    "COOK": "Cooking",
    "READ": "Reading",
    "SOC": "Socialising",
    "GARD": "Gardening",
    "COMP": "Computer",
    "HYG": "Hygiene",
    "CLEN": "Cleaning",
    "VOL": "Volunteering",
    "MUS": "Music",
    "WORK": "Working",
    "HELP": "Helping",
    "OTHER": "Other",
}

LOG_ENTRY_TYPES = {
    "COFU": "User updated their Circle Of Friends",
    "PROF": "User updated their profile",
    "PSWD": "User changed their password (password is not logged)",
    "PRES": "User requested a password reset email",
    "DELE": "User and associated data deleted",
}


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in. See https://www.bedjango.com/blog/top-6-django-decorators/ """

    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)
    # The way to use this decorator is:
    #     @group_required("admins", "seller")
    #     def my_view(request, pk)
    #         ...


def getProfileMoodsByDTRange(profile_id: int,
                             start_dt: datetime.datetime = datetime.datetime.now(tz=timezone.utc),
                             end_dt: datetime.datetime = datetime.datetime.now(tz=timezone.utc)
                             ):
    profile_record = UserProfile.objects.filter(id=profile_id)[0]
    querysetofmoodobjects = Moods.objects.filter(user=profile_record).filter(time__range=(start_dt, end_dt)).order_by(
        "-time")
    return (list(querysetofmoodobjects))


def getDailyMoodsAndLabels(profile_id: int,
                           start_date: datetime.date = datetime.datetime.now(tz=timezone.utc).date(),
                           number_of_days: int = 1,
                           shortdatelabels: bool = False,
                           *args, **kwargs):
    ################################################################
    # Calculate a list of [number*2] of half-day chunks,
    # starting from [start_date AM], and get the most recent mood object
    # for [profile_id] in each half-day chunk of time.
    #
    # Return a dict: {
    # labels: [str timelabels, ..] # e.g. "Friday AM", "Friday PM", "26th Feb 2020 AM"
    # mood_objects: [ list of Moods.objects] corresponding to the above time labels
    # }
    ################################################################

    mood_objects = []
    time_labels = []

    for loop in range(number_of_days):
        time_range_start = start_date + (datetime.timedelta(days=1) * loop)
        time_range_midday = time_range_start + datetime.timedelta(hours=12)
        time_range_end = time_range_start + datetime.timedelta(hours=24)

        if shortdatelabels:
            tmpTimeString = time_range_start.strftime("%a")[0:2] \
                            + " " + str(time_range_start.day) \
                            + time_range_start.strftime(" %b %p")
        else:
            tmpTimeString = time_range_start.strftime("%A %d %B %Y %p")
        time_labels.append(tmpTimeString)
        tmpmoodentries = getProfileMoodsByDTRange(profile_id, time_range_start, time_range_midday)
        if len(tmpmoodentries) >= 1:
            mood_objects.append(tmpmoodentries[0])
        else:
            mood_objects.append(None)

        if shortdatelabels:
            tmpTimeString = time_range_midday.strftime("%a ")[0:2] \
                            + " " + str(time_range_midday.day) \
                            + time_range_midday.strftime(" %b %p")
        else:
            tmpTimeString = time_range_midday.strftime("%A %d %B %Y %p")
        time_labels.append(tmpTimeString)
        tmpmoodentries = getProfileMoodsByDTRange(profile_id, time_range_midday, time_range_end)
        if len(tmpmoodentries) >= 1:
            mood_objects.append(tmpmoodentries[0])
        else:
            mood_objects.append(None)

    # print("---- Time labels ----")
    # print(time_labels)
    # print("---- Mood objects ----")
    # print(mood_objects)
    # print("---- End ----")

    return {
        "labels": time_labels,
        "moods" : mood_objects
        }

@register.filter  # See https://fedingo.com/how-to-lookup-dictionary-value-with-key-in-django-template/
def get_value(dictionary, key):
    return dictionary.get(key)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            Token.objects.filter(user=request.user).delete()  # Remove outdated API login token
            messages.success(request, 'Your password was successfully updated.')
            newUserLogEntry = UserLog.objects.create(
                type="PSWD",
                user=request.user,
                description="User " + str(request.user.id) + " (" + str(request.user.first_name) + " " \
                            + str(request.user.last_name) + ") changed their password.",
                prediffjson=None,
                postdiffjson=None
            )
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
            newUserLogEntry = UserLog.objects.create(
                type="PSWD",
                user=request.user,
                description="User " + str(request.user.id) + " (" + str(request.user.first_name) + " " \
                            + str(request.user.last_name) + ") attempted AND FAILED to change their password.",
                prediffjson=None,
                postdiffjson=None
            )
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@login_required
def update_account_basics(request):
    context = {}
    current_user = request.user
    initialserializer = UserSerializer(current_user)
    initialserializer_json = initialserializer.data

    if request.method == 'POST':
        form = UserAccountForm(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            new_basics = form.save()
            messages.success(request, 'Your account was successfully updated.')
            finalserializer = UserSerializer(new_basics)
            newUserLogEntry = UserLog.objects.create(
                type="PROF",
                user=request.user,
                description="User " + str(request.user.id) + " (" + str(request.user.first_name) + " " \
                            + str(request.user.last_name) + ") updated their account basics.",
                prediffjson=initialserializer_json,
                postdiffjson=finalserializer.data
            )
            return redirect('dashboard')
    else:
        context = {
            "form": UserAccountForm(instance=request.user),
            }
        return render(request, 'account.html', context)


@login_required
def update_profile(request):
    context = {}
    try:
        current_users_profile = UserProfile.objects.filter(user=request.user)[0]
        initialserializer = UserProfileSerializer(current_users_profile)
        initialserializer_json = initialserializer.data
    except:
        print("Attempting to get profile of a user who doesn't have one.")
        messages.error(request, "Couldn't find a profile for you - sorry. Please let us know!")
        return redirect('dashboard')
        # print("For debugging purposes, getting profile of user3 instead.")
        # tmp_user = User.objects.filter(username="user3")[0]
        # print("Name: " + tmp_user.first_name + " " + tmp_user.last_name)
        # current_users_profile = UserProfile.objects.filter(user=tmp_user)[0]
        # print("Education: " + current_users_profile.education)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=current_users_profile)
        if form.is_valid():
            new_profile = form.save()
            messages.success(request, 'Your profile was successfully updated.')
            finalserializer = UserProfileSerializer(new_profile)
            newUserLogEntry = UserLog.objects.create(
                type="PROF",
                user=request.user,
                description="User " + str(request.user.id) + " (" + str(request.user.first_name) + " " \
                            + str(request.user.last_name) + ") updated their profile.",
                prediffjson=initialserializer_json,
                postdiffjson=finalserializer.data
            )
            return redirect('dashboard')
        else:
            messages.error(request, "The form submission wasn't valid: " + str(form.errors))
            context = {
                "form": UserProfileForm(instance=current_users_profile),
                }
            return render(request, 'profile.html', context)
    else:
        context = {
            "form": UserProfileForm(instance=current_users_profile),
            }
        return render(request, 'profile.html', context)


@login_required
@group_required("Researchers", "Linkworkers", "PACs", "Supporters")
def home_dashboard(request):
    tmpGrouplist = []  # Group membership documentation reference: https://www.thetopsites.net/article/53461584.shtml
    if request.user.groups.filter(name="Researchers").exists():
        # tmpGrouplist.append("User is a Researcher. ")
        return redirect('researcher_dashboard')  # , parameter=value)
    if request.user.groups.filter(name="Linkworkers").exists():
        # tmpGrouplist.append("User is a Linkworker. ")
        return redirect('linkworker_mydetails')  # , pk=request.user.id)
    if request.user.groups.filter(name="PACs").exists():
        # tmpGrouplist.append("User is a PAC. ")
        return redirect('pac_mydetails')
    if request.user.groups.filter(name="Supporters").exists():
        # tmpGrouplist.append("User is a Supporter. ")
        return redirect('supporter_mydetails')
    return HttpResponse("User is a member of groups: " + str(
        tmpGrouplist))  # Don't need this when the template is in use, it was only here to test the basic django config.


@login_required
@group_required("Researchers")
def researcher_dashboard(request):
    # lnks = UserProfile.objects.filter(role="LNK")
    lnks = Linkworker.objects.all()
    lnks_count = lnks.count()
    # print("Linkworkers count: " + str(lnks_count))
    # pacs = UserProfile.objects.filter(role="PAC")
    pacs = Person_at_centre.objects.all()
    pacs_count = pacs.count()
    # print("PACs count: " + str(pacs_count))
    moods = Moods.objects.all()
    moods_count = moods.count()
    # print("Moods count: " + str(moods_count))
    # sups = UserProfile.objects.filter(role="SUP")
    sups = Supporter.objects.all()
    sups_count = sups.count()
    # print("Supporters count: " + str(sups_count))

    # mood_lookups = [(MoodLookup.values()[i], MoodIconLookup.values()[i], MoodPositivityLookup.values()[i], MoodActivityLookup.values()[i]) for i in range(0, len(MoodLookup))]
    # print(mood_lookups)

    all_mood_lookups = []
    for onemood in MoodLookup.keys():
        tmp_mood = onemood
        all_mood_lookups.append([
            onemood,
            MoodLookup.get(tmp_mood),
            MoodIconLookup.get(tmp_mood),
            MoodPositivityLookup.get(tmp_mood),
            MoodActivityLookup.get(tmp_mood),
            ])

    # print(all_mood_lookups)

    context = {
        "includenavigation" : True,
        "pacs_count"        : pacs_count,
        "sups_count"        : sups_count,
        "lnks_count"        : lnks_count,
        "moods_count"       : moods_count,
        "all_mood_lookups"  : all_mood_lookups,
        'debugmessage'      : "We're getting somewhere.",
        }
    return render(request, 'researcher.html', context)


@login_required
@group_required("Researchers")
def export_people(request):
    querysetofpeoplerelatedobjects = UserProfile.objects.all().select_related("user").order_by("role",
                                                                                               "user__last_name")
    # print("Count: " + str(querysetofpeoplerelatedobjects.count()))
    results = []
    if querysetofpeoplerelatedobjects:  # Don't bother if there are no moods found
        for oneperson in querysetofpeoplerelatedobjects:
            results.append([
                # Assemble an iterable list of data we want to output
                oneperson.created_on.strftime("%Y/%m/%d %H:%M:%S"),
                oneperson.last_updated.strftime("%Y/%m/%d %H:%M:%S"),
                oneperson.user.username,
                oneperson.user.first_name,
                oneperson.user.last_name,
                oneperson.user.email,
                oneperson.user.id,
                oneperson.id,
                oneperson.role,
                str(oneperson.phone),
                oneperson.image.url.rpartition("/")[2],
                str(oneperson.date_of_birth),
                oneperson.gender,
                oneperson.ethnicity,
                oneperson.education,
                oneperson.disability,
                oneperson.marital_status,
                oneperson.smoking,
                str(oneperson.alcohol_units_per_week),
                str(oneperson.health_conditions),
                str(oneperson.things_liked),
                str(oneperson.things_disliked),
                str(oneperson.family_has),
                str(oneperson.family_bond),
                str(oneperson.community_bond),
                str(oneperson.social_groups),
                str(oneperson.social_group_other),
                str(oneperson.social_bond),
                str(oneperson.link_worker_has),
                str(oneperson.link_worker_bond),
                ])
        # Create a CSV output file (not saved to disk) of our data,
        # and serve it to the web user as a file attachment for download.
        now = datetime.datetime.now()  # We prefer a unique and informative filename.
        filename = "SERVICE_people_" + now.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
        response = HttpResponse(content_type='text/csv')  # Set the MIME type
        response[
            'Content-Disposition'] = 'attachment; filename="' + filename + '"'  # Tell the browser this is an attachment, not part of the HTML page.
        writer = csv.writer(response)
        # writer.writerow([filename])  # Just for debugging
        writer.writerow([  # Column headings
            "Profile created",
            "Profile updated",
            "Username",
            "First name",
            "Last name",
            "Email",
            "User ID",
            "Profile ID",
            "Profile role",
            "Phone",
            "Profile image filename",
            "Date of birth",
            "Gender",
            "Ethnicity",
            "Education",
            "Disabilities",
            "Marital status",
            "Smoker?",
            "Alcohol (units per week)",
            "Health conditions",
            "Things liked",
            "Things disliked",
            "Family?",
            "Family bond closeness",
            "Community bond closeness",
            "Social groups",
            "Social groups (other)",
            "Social group bond closeness",
            "Link worker assigned?",
            "Link worker bond closeness",
        ])
        writer.writerows(results)  # drop all our preprocessed data into the attachment

        return response
        # Send the attachment to the web user

        # return HttpResponse(response)
        # This will return the data within a page, readable in the browser, but not as an attachment


@login_required
@group_required("Researchers")
def export_moods(request):
    # Collect a queryset of data from mood, profile, and auth_user objects.from
    # Use a single query of relatable data, to avoid repeated database hits.
    querysetofmoodrelatedobjects = Moods.objects.all().order_by("user", "-time").select_related(
            "user").select_related("user")
    results = []
    if querysetofmoodrelatedobjects:  # Don't bother if there are no moods found
        for moodrelatedobject in querysetofmoodrelatedobjects:
            tmpMoodString = moodrelatedobject.current_mood  # MoodLookup.get(moodrelatedobject.current_mood)
            tmpPastimesString = str(list(Pastime.objects.filter(mood=moodrelatedobject)))
            results.append(
                    [  # Assemble an iterable list of data we want to output
                        moodrelatedobject.time.strftime("%Y/%m/%d %H:%M:%S"),
                        MoodLookup.get(tmpMoodString),
                        MoodPositivityLookup.get(tmpMoodString),
                        MoodActivityLookup.get(tmpMoodString),
                        # moodrelatedobject.user.user.username,
                        # moodrelatedobject.user.user.first_name,
                        # moodrelatedobject.user.user.last_name,
                        # moodrelatedobject.user.user.email,
                        moodrelatedobject.user.user.id,
                        moodrelatedobject.user.id,
                        # moodrelatedobject.user.role,
                        # str(moodrelatedobject.user.phone),
                        # moodrelatedobject.user.image.url.rpartition("/")[2],
                        str(moodrelatedobject.include_wellbeing),
                        moodrelatedobject.wellbeing,
                        moodrelatedobject.loneliness,
                        tmpPastimesString,
                        str(moodrelatedobject.spoketosomeone),
                        str(moodrelatedobject.spoketosomeone_who),
                        moodrelatedobject.hours_bed,
                        moodrelatedobject.hours_sofa,
                        moodrelatedobject.hours_kitchen,
                        moodrelatedobject.hours_garden,
                        ])

    # Create a CSV output file (not saved to disk) of our data,
    # and serve it to the web user as a file attachment for download.
    now = datetime.datetime.now()  # We prefer a unique and informative filename.
    filename = "SERVICE_moods_" + now.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    response = HttpResponse(content_type='text/csv')  # Set the MIME type
    response[
        'Content-Disposition'] = 'attachment; filename="' + filename + '"'  # Tell the browser this is an attachment, not part of the HTML page.
    writer = csv.writer(response)
    # writer.writerow([filename])  # Just for debugging
    writer.writerow([  # Column headings
        "Date/Time",
        "Mood",
        "Mood Positivity/Negativity",
        "Mood Activity/Passivity",
        "User ID",
        "Profile ID",
        "Include following wellbeing fields?",
        "Wellbeing",
        "Loneliness",
        "Pastimes",
        "Spoken to anyone?",
        "Spoke to",
        "Hours in bed",
        "Hours on sofa",
        "Hours in kitchen",
        "Hours in garden",
    ])
    writer.writerows(
            results)  # drop all our preprocessed data into the attachment

    return response  # Send the attachment to the web user
    # return HttpResponse(response)  # This will return the data within a page, readable in the browser, but not as an attachment


@login_required
@group_required("Researchers")
def export_userlog(request):
    # Collect a queryset of data from userlog objects
    logqueryset = UserLog.objects.all().order_by("user", "-timestamp")
    results = []
    if logqueryset:  # Don't bother if there are no moods found
        for logentry in logqueryset:
            tmpLogTypeString = LOG_ENTRY_TYPES.get(logentry.type)
            results.append([  # Assemble an iterable list of data we want to output
                logentry.id,
                logentry.timestamp.strftime("%Y/%m/%d %H:%M:%S"),
                logentry.user_id,
                logentry.type,
                tmpLogTypeString,
                logentry.description,
                logentry.prediffjson,
                logentry.postdiffjson,
                ])

    # Create a CSV output file (not saved to disk) of our data,
    # and serve it to the web user as a file attachment for download.
    now = datetime.datetime.now()  # We prefer a unique and informative filename.
    filename = "SERVICE_UserLog_" + now.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    response = HttpResponse(content_type='text/csv')  # Set the MIME type
    response[
        'Content-Disposition'] = 'attachment; filename="' + filename + '"'  # Tell the browser this is an attachment, not part of the HTML page.
    writer = csv.writer(response)
    # writer.writerow([filename])  # Just for debugging
    writer.writerow([  # Column headings
        "id",
        "Date/Time",
        "user_id",
        "type (code)",
        "type (long text)",
        "description",
        "prediffjson",
        "postdiffjson",
    ])
    writer.writerows(
            results)  # drop all our preprocessed data into the attachment

    return response  # Send the attachment to the web user
    # return HttpResponse(response)  # This will return the data within a page, readable in the browser, but not as an attachment



@login_required
@group_required("Researchers", "Linkworkers")
def linkworker_list(request):
    # Save/retrieve user's filter preferences
    sessionusername = request.user.get_username()
    page = "1"
    try:
        userpreferencesrecord = UserPreferences.objects.get(username=sessionusername)
    except:  # DoesNotExist
        userpreferencesrecord = UserPreferences(username=sessionusername, )
        userpreferencesrecord.save()

    userprefsform = UserPreferencesForm(instance=userpreferencesrecord)
    if request.method == "POST":
        if request.POST.get('resetUserPreferences') == "True":
            userpreferencesrecord.delete()
            userpreferencesrecord = UserPreferences(username=sessionusername, )
            userpreferencesrecord.save()
            userprefsform = UserPreferencesForm(instance=userpreferencesrecord)
        elif request.POST.get('rowsToDisplay'):
            userprefsform = UserPreferencesForm(instance=userpreferencesrecord)
            userpreferencesrecord = userprefsform.save(commit=False)
            userpreferencesrecord.rowsToDisplay = int(request.POST.get('rowsToDisplay'))
            userpreferencesrecord.username = sessionusername
            userpreferencesrecord.save()
            page = userpreferencesrecord.gotoPage
        elif request.POST.get('gotoPage'):
            userprefsform = UserPreferencesForm(instance=userpreferencesrecord)
            userpreferencesrecord = userprefsform.save(commit=False)
            userpreferencesrecord.gotoPage = int(request.POST.get('gotoPage'))
            userpreferencesrecord.username = sessionusername
            userpreferencesrecord.save()
            page = userpreferencesrecord.gotoPage
        else:
            userprefsform = UserPreferencesForm(request.POST, instance=userpreferencesrecord)
            userpreferencesrecord = userprefsform.save(commit=False)
            userpreferencesrecord.username = sessionusername
            userpreferencesrecord.save()
            page = userpreferencesrecord.gotoPage
    elif request.method == "GET":
        urlpage = request.GET.get('page')
        if urlpage:
            userprefsform = UserPreferencesForm(instance=userpreferencesrecord)
            # userprefsform = UserPreferencesForm(request.GET, instance=userpreferencesrecord)
            userpreferencesrecord = userprefsform.save(commit=False)
            userpreferencesrecord.gotoPage = urlpage
            userpreferencesrecord.username = sessionusername
            userpreferencesrecord.save()
            try:
                page = int(urlpage)
            except:
                page = 1
            if page == 0:
                page = 1
    rowsToDisplay = userpreferencesrecord.rowsToDisplay
    if rowsToDisplay:
        rowsToShow = rowsToDisplay
    else:
        rowsToShow = 6

    lnk_profiles = Linkworker.objects.all().select_related("linkworker").select_related("linkworker").select_related(
        "linkworker__user").order_by("linkworker__user__last_name")

    paginatedlist = lnk_profiles
    paginator = Paginator(paginatedlist, rowsToShow)  # Show n contacts per page
    paginatedpage = paginator.get_page(page)
    try:
        dummy = int(page)
    except:
        page = "1"
    paginatedpagecurrent = int(page)
    paginatedpagelist = []
    pageliststart = int(page) - 3
    pagelistend = int(page) + 4

    for pagenum in range(pageliststart, pagelistend):
        if pagenum < 0 or pagenum > paginator.num_pages:
            paginatedpagelist.append(0)
        else:
            paginatedpagelist.append(pagenum)

    debugmessage = "We're getting there.<br />LNK count: " + str(lnk_profiles.count())
    context = {
        "includenavigation"     : True,
        'paginatedrecordcount'  : paginatedlist.count(),
        'paginatedrecords'      : paginatedpage,
        'paginatedpagelist'     : paginatedpagelist,
        'paginatedpagecurrent'  : paginatedpagecurrent,
        'userpreferencesrecord' : userpreferencesrecord,
        'userpreferencesform'   : userprefsform,
        # 'profiles'              : lnk_profiles,
        # 'debugmessage'          : debugmessage,
        }
    return render(request, 'linkworker_list.html', context)


@login_required
@group_required("Researchers", "Linkworkers")
def linkworker_details(request, pk=0):
    # Per-user stuff
    try:
        if pk == 0 or (request.user.groups.filter(name="Linkworkers").exists()):
            # If no ID was specified, or the person asking is a Link Worker
            target_user = request.user
        else:
            # Otherwise
            target_user = User.objects.get(id=pk)
    except  User.DoesNotExist:
        raise Http404("Unknown user")

    if not target_user.groups.filter(name="Linkworkers").exists():
        raise Http404("No such Link worker")

    # Get basic user details
    current_user_name = target_user.get_full_name()  # current_user.first_name + " " + current_user.last_name
    current_user_id = target_user.id
    # print("DEBUG: " str(current_user.id) + " - " + current_user_name)

    # Get more info from the profile record
    current_user_profile = UserProfile.objects.filter(user=target_user)[0]
    current_user_image_url = current_user_profile.image.url

    # Link worker stuff
    try:  # See if we can find further details from a link worker record.
        linkworker_record = \
            Linkworker.objects.filter(linkworker=current_user_profile)[0]
    except:  # Not found
        linkworker_record = False

    # print("DEBUG: " + str(linkworker_record))

    linkworker_pac_records = []
    if linkworker_record:  # See if we can find further details of key worker clients
        # print("DEBUG: " + str(linkworker_record.pacs.all()))
        linkworker_pac_records = linkworker_record.pacs.all()
        linkworker_pac_count = linkworker_pac_records.count()
        clientdetails = []
        for pac in linkworker_pac_records:
            # print("DEBUG: " + str(pac.user_profile.user.first_name))
            tmpclientfirstname = pac.user_profile.user.first_name
            tmpclientlastname = pac.user_profile.user.last_name
            tmpclientname = tmpclientfirstname + " " + tmpclientlastname
            tmpclientid = pac.user_profile.user.id
            tmpclientprofileid = pac.user_profile.id
            tmpclientemail = pac.user_profile.user.email
            tmpclientphone = str(pac.user_profile.phone)
            tmpclientimageurl = pac.user_profile.image.url
            try:
                tmpMood = Moods.objects.filter(user=pac.user_profile).latest(
                        "time").current_mood
                tmpMoodDT = Moods.objects.filter(user=pac.user_profile).latest(
                        "time").time
            except:
                tmpMood = "NM"
                tmpMoodDT = None
            tmpclientmood = MoodLookup.get(tmpMood, "No mood")
            tmpclientmoodicon = MoodIconLookup.get(tmpMood,
                                                   '<i class="far fa-meh-blank"></i>')
            tmpclientmooddatetime = tmpMoodDT
            tmpsupportersnames = []
            for sup in pac.supporters.all():
                tmpsupportersnames.append(
                        sup.user_profile.user.first_name + " " + sup.user_profile.user.last_name)
            clientdetails.append(
                    [tmpclientname, tmpclientid, tmpclientprofileid,
                     tmpclientfirstname, tmpclientlastname, tmpclientemail,
                     tmpclientphone, tmpclientimageurl, tmpclientmood,
                     tmpclientmoodicon, tmpclientmooddatetime,
                     tmpsupportersnames])

    context = {
        "includenavigation"        : True,
        # Current user stuff
        'current_user_name'        : current_user_name,
        'current_user_image_url'   : current_user_image_url,
        # Key worker stuff
        'linkworker_client_count'  : linkworker_pac_count,
        'linkworker_client_records': linkworker_pac_records,
        'clientdetails'            : clientdetails,
        # 'debugmessage'             : clientdetails,
        }
    return render(request, 'linkworker.html', context)


#
# @login_required
# @group_required("Researchers", "Linkworkers", "PACs")
# def pac_mydetails(request):
#     try:
#         pac_user_id = request.user.id
#         pac_user = request.user
#     except  User.DoesNotExist:
#         raise Http404(
#             "Unknown user")  # handle Unrecognised User error at this point
#
#     pac_profile = UserProfile.objects.filter(user=pac_user)[0]
#     pac_instance = Person_at_centre.objects.filter(user_profile=pac_profile)[0]
#
#     # print("pac_profile: " + str(pac_profile))  # DEBUG
#
#     # pac_record = Person_at_centre.objects.filter(pac=pac_profile)[0]
#     pac_record = pac_profile.user
#
#     # print("pac_record: " + str(pac_record))  # DEBUG
#
#     pac_image_url = pac_profile.image.url
#     pacdetails = []
#     tmppacfirstname = pac_profile.user.first_name
#     tmppaclastname = pac_profile.user.last_name
#     tmppacname = tmppacfirstname + " " + tmppaclastname
#     tmppacid = pac_user.id
#     tmppacprofileid = pac_profile.id
#     tmppacemail = pac_profile.user.email
#     tmppacphone = str(pac_profile.phone)
#     tmppacimageurl = pac_profile.image.url
#     try:
#         tmpMood = Moods.objects.filter(user=pac_profile).latest(
#             "time").current_mood
#         tmpMoodDT = Moods.objects.filter(user=pac_profile).latest("time").time
#     except:
#         tmpMood = "NM"
#         tmpMoodDT = None
#     tmppacmood = MoodLookup.get(tmpMood, "No mood")
#     tmppacmoodicon = MoodIconLookup.get(tmpMood,
#                                         '<i class="far fa-meh-blank"></i>')
#     tmppacmooddatetime = tmpMoodDT
#     # tmp_supporters_profiles = Linkworker.objects.filter(linkworker=current_user_profile)[0]
#
#     tmp_pac_supporters_list = list(
#         Person_at_centre.objects.get(user_profile=pac_profile).supporters.all())
#     # print("tmp_pac_supporters_list: " + str(tmp_pac_supporters_list))  # DEBUG
#
#     tmpsupportersnames = []
#     for sup in tmp_pac_supporters_list:
#         tmpsupportersnames.append(
#                 sup.user_profile.user.first_name + " " + sup.user_profile.user.last_name)
#
#     tmp_linkworker_profile = \
#     Linkworker.objects.all().filter(pacs__in=[pac_instance]).distinct()[
#         0].linkworker
#     linkworker_name = tmp_linkworker_profile.user.first_name + " " + tmp_linkworker_profile.user.last_name
#     linkworker_phone = tmp_linkworker_profile.phone
#     linkworker_email = tmp_linkworker_profile.user.email
#
#     context = {
#         'client_user_name'       : pac_user.first_name + " " + pac_user.last_name,
#         'client_user_id'         : tmppacid,
#         'client_profile_id'      : tmppacprofileid,
#         'client_first_name'      : tmppacfirstname,
#         'client_last_name'       : tmppaclastname,
#         'client_email'           : tmppacemail,
#         'client_phone'           : tmppacphone,
#         'client_image_url'       : pac_image_url,
#         'client_mood'            : tmppacmood,
#         'client_moodicon'        : tmppacmoodicon,
#         'client_mood_datetime'   : tmppacmooddatetime,
#         'client_supporters_names': tmpsupportersnames,
#         'linkworker_name'        : linkworker_name,
#         'linkworker_phone'       : linkworker_phone,
#         'linkworker_email'       : linkworker_email,
#         # 'debugmessage':                 (str(tmpclientprofileid) + "/" + str(tmpclientid)),
#         }
#     return render(request, 'pac.html', context)


@login_required
@group_required("Researchers", "Linkworkers")
def pac_list(request):
    # Save/retrieve user's filter preferences
    sessionusername = request.user.get_username()
    page = "1"
    try:
        userpreferencesrecord = UserPreferences.objects.get(username=sessionusername)
    except:  # DoesNotExist
        userpreferencesrecord = UserPreferences(username=sessionusername, )
        userpreferencesrecord.save()

    userprefsform = UserPreferencesForm(instance=userpreferencesrecord)
    if request.method == "POST":
        if request.POST.get('resetUserPreferences') == "True":
            userpreferencesrecord.delete()
            userpreferencesrecord = UserPreferences(username=sessionusername, )
            userpreferencesrecord.save()
            userprefsform = UserPreferencesForm(instance=userpreferencesrecord)
        elif request.POST.get('rowsToDisplay'):
            userprefsform = UserPreferencesForm(instance=userpreferencesrecord)
            userpreferencesrecord = userprefsform.save(commit=False)
            userpreferencesrecord.rowsToDisplay = int(request.POST.get('rowsToDisplay'))
            userpreferencesrecord.username = sessionusername
            userpreferencesrecord.save()
            page = userpreferencesrecord.gotoPage
        elif request.POST.get('gotoPage'):
            userprefsform = UserPreferencesForm(instance=userpreferencesrecord)
            userpreferencesrecord = userprefsform.save(commit=False)
            userpreferencesrecord.gotoPage = int(request.POST.get('gotoPage'))
            userpreferencesrecord.username = sessionusername
            userpreferencesrecord.save()
            page = userpreferencesrecord.gotoPage
        else:
            userprefsform = UserPreferencesForm(request.POST, instance=userpreferencesrecord)
            userpreferencesrecord = userprefsform.save(commit=False)
            userpreferencesrecord.username = sessionusername
            userpreferencesrecord.save()
            page = userpreferencesrecord.gotoPage
    elif request.method == "GET":
        urlpage = request.GET.get('page')
        if urlpage:
            userprefsform = UserPreferencesForm(instance=userpreferencesrecord)
            # userprefsform = UserPreferencesForm(request.GET, instance=userpreferencesrecord)
            userpreferencesrecord = userprefsform.save(commit=False)
            userpreferencesrecord.gotoPage = urlpage
            userpreferencesrecord.username = sessionusername
            userpreferencesrecord.save()
            try:
                page = int(urlpage)
            except:
                page = 1
            if page == 0:
                page = 1
    rowsToDisplay = userpreferencesrecord.rowsToDisplay
    if rowsToDisplay:
        rowsToShow = rowsToDisplay
    else:
        rowsToShow = 6

    # pac_profiles = Person_at_centre.objects.all().select_related("user_profile").select_related("user_profile__user").order_by("user_profile__user__last_name")
    pac_profiles = Person_at_centre.objects.all().select_related("user_profile").select_related(
        "user_profile__user").order_by("user_profile__user__last_name")

    paginatedlist = pac_profiles
    paginator = Paginator(paginatedlist, rowsToShow)  # Show n contacts per page
    paginatedpage = paginator.get_page(page)
    try:
        dummy = int(page)
    except:
        page = "1"
    paginatedpagecurrent = int(page)
    paginatedpagelist = []
    pageliststart = int(page) - 3
    pagelistend = int(page) + 4

    for pagenum in range(pageliststart, pagelistend):
        if pagenum < 0 or pagenum > paginator.num_pages:
            paginatedpagelist.append(0)
        else:
            paginatedpagelist.append(pagenum)

    # UserProfile.objects.filter(role="SUP").select_related("user").order_by("user__last_name")

    debugmessage = "We're getting there.<br />PAC count: " + str(pac_profiles.count())
    context = {
        "includenavigation"    : True,
        'paginatedrecordcount' : paginatedlist.count(),
        'paginatedrecords'     : paginatedpage,
        'paginatedpagelist'    : paginatedpagelist,
        'paginatedpagecurrent' : paginatedpagecurrent,
        'userpreferencesrecord': userpreferencesrecord,
        'userpreferencesform'  : userprefsform,
        # 'profiles': pac_profiles,
        'debugmessage'         : debugmessage,
        }
    return render(request, 'pac_list.html', context)


@login_required
@group_required("Researchers", "Linkworkers", "PACs")
def pac_details(request, pk=0):
    # print(request.user)
    # Per-user stuff
    try:
        # if the person asking is a Link Worker or Researcher they can request other people's data
        if (request.user.groups.filter(name="Linkworkers").exists()) \
        or (request.user.groups.filter(name="Researchers").exists()):
            target_user = User.objects.get(id=pk)
        else:
            # but if not, they can only have their own data (if it exists)
            target_user = request.user
    except  User.DoesNotExist:
        raise Http404("Unknown user")

    if not target_user.groups.filter(name="PACs").exists():
        raise Http404("No such PAC")

    pac_profile = UserProfile.objects.filter(user=target_user)[0]
    # pac_record = Person_at_centre.objects.filter(user_profile=pac_profile)[0]

    try:
        tmpMood = Moods.objects.filter(user=pac_profile).latest("time").current_mood
        tmpMoodDT = Moods.objects.filter(user=pac_profile).latest("time").time
    except:
        tmpMood = "NM"
        tmpMoodDT = None
    tmppacmood = MoodLookup.get(tmpMood, "No mood")
    tmppacmoodicon = MoodIconLookup.get(tmpMood, '<i class="far fa-meh-blank"></i>')
    tmppacmooddatetime = tmpMoodDT

    # Get circles.
    try:
        pac_record = Person_at_centre.objects.filter(user_profile=pac_profile)[0]
        cos1_profiles = list(supporter.user_profile for supporter in pac_record.circle_of_support_1.all())
        cos2_profiles = list(supporter.user_profile for supporter in pac_record.circle_of_support_2.all())
        cos3_profiles = list(supporter.user_profile for supporter in pac_record.circle_of_support_3.all())
    except:
        raise Http404("Circle Of Support retrieval error.")

    try:
        pac_instance = Person_at_centre.objects.filter(user_profile=pac_profile)[0]
        linkworker_profile = Linkworker.objects.all().filter(pacs__in=[pac_instance]).distinct()[0].linkworker
    except:
        linkworker_profile=None

    context = {
        "includenavigation"      : True,
        'user_profile'           : pac_profile,
        'client_mood'            : tmppacmood,
        'client_moodicon'        : tmppacmoodicon,
        'client_mood_datetime'   : tmppacmooddatetime,
        'cos1_profiles'          : cos1_profiles,
        'cos2_profiles'          : cos2_profiles,
        'cos3_profiles'          : cos3_profiles,
        'linkworker_profile'     : linkworker_profile,
        # 'debugmessage'           : debugmessage,
        }
    return render(request, 'pac.html', context)


@login_required
@group_required("Researchers", "Linkworkers", "PACs")
def pac_timeline(request, pk=0):
    # Per-user stuff
    try:
        # if the person asking is a Link Worker or Researcher they can request other people's data
        if (request.user.groups.filter(name="Linkworkers").exists()) \
        or (request.user.groups.filter(name="Researchers").exists()):
            target_user = User.objects.get(id=pk)
        else:
            # but if not, they can only have their own data (if it exists)
            target_user = request.user
    except  User.DoesNotExist:
        raise Http404("Unknown user")

    if not target_user.groups.filter(name="PACs").exists():
        raise Http404("No such PAC")

    pac_profile = UserProfile.objects.filter(user=target_user)[0]
    # pac_record = Person_at_centre.objects.filter(user_profile=pac_profile)[0]

    tmpMoods = Moods.objects.filter(user=pac_profile.id).order_by("-time")
    tmp_moodpastimes={}
    for oneMood in tmpMoods:
        # print("--- oneMood: " + str(oneMood.id) + ": " + str(oneMood))
        onemoodspastimes = list(Pastime.objects.filter(mood=oneMood))
        # print ("--- # of pastimes for this mood: " + str(len(onemoodspastimes)))
        tmpallpastimesdetails=[]
        for onePastime in Pastime.objects.filter(mood=oneMood):
            # print("--- onePastime: " + str(onePastime))
            # print("--- onePastime.whowith: " + str(onePastime.whowith.all()))
            allpastimesupporters = []
            for oneSupporter in list(onePastime.whowith.all()):
                # print("--- oneSupporter ID: " + str(oneSupporter.id))
                tmponesupporterdetails = {
                    "id"        :   oneSupporter.id,
                    "first_name":   oneSupporter.user_profile.user.first_name,
                    "last_name" :   oneSupporter.user_profile.user.last_name
                    }
                allpastimesupporters.append(tmponesupporterdetails)
            # print(allpastimesupporters)
            tmponepastimedetails = {
                "id"        :   onePastime.id,
                "whatdoing" :   PastimeLookup[onePastime.whatdoing],
                "whowith"   :   allpastimesupporters,
                }
            tmpallpastimesdetails.append(tmponepastimedetails)
        # tmp_moodpastimes = {
        #     "mood_id"   :   oneMood.id,
        #     "pastimes"  :   tmpallpastimesdetails
        # }
        tmp_moodpastimes[oneMood.id]=tmpallpastimesdetails
    # print("ALL: " + str(tmp_moodpastimes))

    context = {
        "includenavigation"     : True,
        'pac_profile'           : pac_profile,
        'moods'                 : tmpMoods,
        'mood_lookup'           : MoodLookup,
        'mood_icon_lookup'      : MoodIconLookup,
        'mood_positivity_lookup': MoodPositivityLookup,
        'mood_activity_lookup'  : MoodActivityLookup,
        'pastimes'              : tmp_moodpastimes,
        # 'debugmessage'          : "ID: " + str(tmppacid) + "; profileID: " + str(tmppacprofileid) + " - " + str(tmpMoods),
        }
    return render(request, 'pac_timeline.html', context)


@login_required
@group_required("Researchers", "Linkworkers", "PACs")
def pac_export(request, pk):
    # personlist = Person.objects.all().order_by('staffSurname', 'initials').select_related().annotate(tutoring_count=Count('grade_associateLecturer'), monitoring_count=Count('grade_monitor'))
    try:
        client_user_id = pk
        client_user = User.objects.get(id=pk)
    except  User.DoesNotExist:
        raise Http404("Unknown user")  # handle Unrecognised User error at this point

    # Collect a queryset of data from mood, profile, and auth_user objects.from
    # Use a single query of relatable data, to avoid repeated database hits.
    client_profile = UserProfile.objects.filter(user=client_user)[0]
    querysetofmoodrelatedobjects = Moods.objects.filter(user=client_profile).order_by("-time").select_related(
        "user").select_related("user")
    results = []
    if querysetofmoodrelatedobjects:  # Don't bother if there are no moods found
        for moodrelatedobject in querysetofmoodrelatedobjects:
            tmpMoodString = moodrelatedobject.current_mood  # MoodLookup.get(moodrelatedobject.current_mood)
            tmpPastimesString = str(list(Pastime.objects.filter(mood=moodrelatedobject)))
            results.append(
                    [  # Assemble an iterable list of data we want to output
                        moodrelatedobject.time.strftime("%Y/%m/%d %H:%M:%S"),
                        MoodLookup.get(tmpMoodString),
                        MoodPositivityLookup.get(tmpMoodString),
                        MoodActivityLookup.get(tmpMoodString),
                        # moodrelatedobject.user.user.username,
                        # moodrelatedobject.user.user.first_name,
                        # moodrelatedobject.user.user.last_name,
                        # moodrelatedobject.user.user.email,
                        moodrelatedobject.user.user.id,
                        moodrelatedobject.user.id,
                        # moodrelatedobject.user.role,
                        # str(moodrelatedobject.user.phone),
                        # moodrelatedobject.user.image.url.rpartition("/")[2],
                        str(moodrelatedobject.include_wellbeing),
                        moodrelatedobject.wellbeing,
                        moodrelatedobject.loneliness,
                        # str(moodrelatedobject.whatdoing),
                        tmpPastimesString,
                        str(moodrelatedobject.spoketosomeone),
                        str(moodrelatedobject.spoketosomeone_who),
                        moodrelatedobject.hours_bed,
                        moodrelatedobject.hours_sofa,
                        moodrelatedobject.hours_kitchen,
                        moodrelatedobject.hours_garden,
                        ])

    # Create a CSV output file (not saved to disk) of our data,
    # and serve it to the web user as a file attachment for download.
    now = datetime.datetime.now()  # We prefer a unique and informative filename.
    filename = "SERVICE_" + client_user.first_name + "-" + client_user.last_name + "_" + now.strftime(
        "%Y-%m-%d-%H-%M-%S") + ".csv"
    response = HttpResponse(content_type='text/csv')  # Set the MIME type
    response[
        'Content-Disposition'] = 'attachment; filename="' + filename + '"'  # Tell the browser this is an attachment, not part of the HTML page.
    writer = csv.writer(response)
    # writer.writerow([filename])  # Just for debugging
    writer.writerow([  # Column headings
        "Date/Time",
        "Mood",
        "Mood Positivity/Negativity",
        "Mood Activity/Passivity",
        "User ID",
        "Profile ID",
        "Include following wellbeing fields?",
        "Wellbeing",
        "Loneliness",
        "Pastimes",
        "Spoken to anyone?",
        "Spoke to",
        "Hours in bed",
        "Hours on sofa",
        "Hours in kitchen",
        "Hours in garden",
        ])
    writer.writerows(results)  # drop all our preprocessed data into the attachment

    return response  # Send the attachment to the web user
    # return HttpResponse(response)  # This will return the data within a page, readable in the browser, but not as an attachment


@login_required
@group_required("Researchers", "Linkworkers", "PACs")
def pac_export_circles(request, pk):
    try:
        # if the person asking is a Link Worker or Researcher they can request other people's data
        if (request.user.groups.filter(name="Linkworkers").exists()) \
        or (request.user.groups.filter(name="Researchers").exists()):
            target_user = User.objects.get(id=pk)
        else:
            # but if not, they can only have their own data (if it exists)
            target_user = request.user
    except  User.DoesNotExist:
        raise Http404("Unknown user")

    if not target_user.groups.filter(name="PACs").exists():
        raise Http404("No such PAC")

    pac_profile = UserProfile.objects.filter(user=target_user)[0]

    # Get circles.
    try:
        pac_record = Person_at_centre.objects.filter(user_profile=pac_profile)[0]
        cos1_supporters = list(supporter for supporter in pac_record.circle_of_support_1.all())
        cos2_supporters = list(supporter for supporter in pac_record.circle_of_support_2.all())
        cos3_supporters = list(supporter for supporter in pac_record.circle_of_support_3.all())
    except:
        raise Http404("Circle Of Support retrieval error.")

    results = []
    for onesupporter in cos1_supporters:
        results.append(
            [   1,
                onesupporter.user_profile.user.first_name,
                onesupporter.user_profile.user.last_name,
                onesupporter.user_profile.user.username,
                onesupporter.user_profile.user.email,
                onesupporter.user_profile.user.id,
                onesupporter.user_profile.id,
                onesupporter.id
                ]
        )
    for onesupporter in cos2_supporters:
        results.append(
            [   2,
                onesupporter.user_profile.user.first_name,
                onesupporter.user_profile.user.last_name,
                onesupporter.user_profile.user.username,
                onesupporter.user_profile.user.email,
                onesupporter.user_profile.user.id,
                onesupporter.user_profile.id,
                onesupporter.id
                ]
        )
    for onesupporter in cos3_supporters:
        results.append(
            [   3,
                onesupporter.user_profile.user.first_name,
                onesupporter.user_profile.user.last_name,
                onesupporter.user_profile.user.username,
                onesupporter.user_profile.user.email,
                onesupporter.user_profile.user.id,
                onesupporter.user_profile.id,
                onesupporter.id
                ]
        )

    # Create a CSV output file (not saved to disk) of our data,
    # and serve it to the web user as a file attachment for download.
    now = datetime.datetime.now()  # We prefer a unique and informative filename.
    filename = "SERVICE_" \
               + pac_profile.user.first_name + "-" \
               + pac_profile.user.last_name + "_Circles_" \
               + now.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    response = HttpResponse(content_type='text/csv')  # Set the MIME type
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'  # Tell the browser this is an attachment, not part of the HTML page.
    writer = csv.writer(response)
    # writer.writerow([filename])  # Just for debugging
    writer.writerow([  # Column headings
        "circle",
        "first_name",
        "last_name",
        "username",
        "email",
        "user_id",
        "user_profile_id",
        "supporter_id",
        ])
    writer.writerows(results)  # drop all our preprocessed data into the attachment

    return response  # Send the attachment to the web user
    # return HttpResponse(response)  # This will return the data within a page, readable in the browser, but not as an attachment


@login_required
@group_required("Researchers")
def pac_export_userlog(request, pk):
    # Collect a queryset of data from userlog objects

    try:
        # if the person asking is a Link Worker or Researcher they can request other people's data
        if (request.user.groups.filter(name="Linkworkers").exists()) \
        or (request.user.groups.filter(name="Researchers").exists()):
            target_user = User.objects.get(id=pk)
        else:
            # but if not, they can only have their own data (if it exists)
            target_user = request.user
    except  User.DoesNotExist:
        raise Http404("Unknown user")

    if not target_user.groups.filter(name="PACs").exists():
        raise Http404("No such PAC")

    logqueryset = UserLog.objects.all().filter(user=target_user).order_by("-timestamp")
    results = []
    if logqueryset:  # Don't bother if there are no moods found
        for logentry in logqueryset:
            tmpLogTypeString = LOG_ENTRY_TYPES.get(logentry.type)
            results.append([  # Assemble an iterable list of data we want to output
                logentry.id,
                logentry.timestamp.strftime("%Y/%m/%d %H:%M:%S"),
                logentry.user_id,
                logentry.type,
                tmpLogTypeString,
                logentry.description,
                logentry.prediffjson,
                logentry.postdiffjson,
                ])

    # Create a CSV output file (not saved to disk) of our data,
    # and serve it to the web user as a file attachment for download.
    now = datetime.datetime.now()  # We prefer a unique and informative filename.
    filename = "SERVICE_" \
               + target_user.first_name + "-" \
               + target_user.last_name + "_UserLog_" \
               + now.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    response = HttpResponse(content_type='text/csv')  # Set the MIME type
    response[
        'Content-Disposition'] = 'attachment; filename="' + filename + '"'  # Tell the browser this is an attachment, not part of the HTML page.
    writer = csv.writer(response)
    # writer.writerow([filename])  # Just for debugging
    writer.writerow([  # Column headings
        "id",
        "Date/Time",
        "user_id",
        "type (code)",
        "type (long text)",
        "description",
        "prediffjson",
        "postdiffjson",
    ])
    writer.writerows(
            results)  # drop all our preprocessed data into the attachment

    return response  # Send the attachment to the web user
    # return HttpResponse(response)  # This will return the data within a page, readable in the browser, but not as an attachment



@login_required
@group_required("Researchers", "Linkworkers", "PACs")
def membership_chart(request):
    userprofilecount = UserProfile.objects.all().count()
    linkworkercount = Linkworker.objects.all().count()
    clientcount = Person_at_centre.objects.all().count()
    supportercount = userprofilecount - linkworkercount - clientcount

    labels = ["Key workers", "Person_at_centres", "Supporters"]
    data = [linkworkercount, clientcount, supportercount]

    return JsonResponse(data={
        'labels': labels,
        'data'  : data,
        })


@login_required
@group_required("Researchers", "Linkworkers", "PACs")
def moodspider_chart(request, pk):
    try:
        client_user_id = pk
        client_user = User.objects.get(id=pk)
    except  User.DoesNotExist:
        raise Http404("Unknown user")  # handle Unrecognised User error at this point
    client_profile = UserProfile.objects.filter(user=client_user)[0]

    datastartdate = datetime.datetime.combine(
            datetime.date.today(), datetime.time(0, 0, 0),
            tzinfo=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo  # timezone.utc
            )

    # Dataset 1: The last 7 days
    dataset1moodsandlabels = getDailyMoodsAndLabels(profile_id=client_profile.id,
                                                    start_date=datastartdate - datetime.timedelta(days=6),
                                                    number_of_days=7)
    dataset1labels = dataset1moodsandlabels.get("labels")
    dataset1moodobjects = dataset1moodsandlabels.get("moods")
    dataset1moodtitles = []
    for moodobj in dataset1moodobjects:
        if moodobj:
            dataset1moodtitles.append(MoodLookup.get(moodobj.current_mood))
        else:
            dataset1moodtitles.append("No mood")
    # End of dataset 1 lookups

    # Dataset 2: The 7 days before dataset 1
    dataset2moodsandlabels = getDailyMoodsAndLabels(profile_id=client_profile.id,
                                                    start_date=datastartdate - datetime.timedelta(days=13),
                                                    number_of_days=7)
    dataset2labels = dataset2moodsandlabels.get("labels")
    dataset2moodobjects = dataset2moodsandlabels.get("moods")
    dataset2moodtitles = []
    for moodobj in dataset2moodobjects:
        if moodobj:
            dataset2moodtitles.append(MoodLookup.get(moodobj.current_mood))
        else:
            dataset2moodtitles.append("No mood")
    # End of dataset 2 lookups

    # Dataset 3: The 7 days before dataset 2
    dataset3moodsandlabels = getDailyMoodsAndLabels(profile_id=client_profile.id,
                                                    start_date=datastartdate - datetime.timedelta(days=20),
                                                    number_of_days=7)
    dataset3labels = dataset3moodsandlabels.get("labels")
    dataset3moodobjects = dataset3moodsandlabels.get("moods")
    dataset3moodtitles = []
    for moodobj in dataset3moodobjects:
        if moodobj:
            dataset3moodtitles.append(MoodLookup.get(moodobj.current_mood))
        else:
            dataset3moodtitles.append("No mood")
    # End of dataset 3 lookups

    spiderlabels = [  # list(MoodLookup.values()), but sorted to arrange them differently
        "No mood",
        "Relaxed",
        "Excited",
        "Happy",
        "Calm",
        "Bored",
        "Sad",
        "Annoyed",
        "Nervous",
        ]
    dataset1counts = []
    dataset2counts = []
    dataset3counts = []
    for onemood in spiderlabels:
        dataset1counts.append(dataset1moodtitles.count(onemood))
        dataset2counts.append(dataset2moodtitles.count(onemood))
        dataset3counts.append(dataset3moodtitles.count(onemood))

    # print("Labels:")
    # print(dataset1labels)
    # print("Mood titles:")
    # print(dataset1moodtitles)
    # print("Mood counts:")
    # print(dataset1counts)

    return JsonResponse(data={
        'labels'        : spiderlabels,
        'dataset1labels': dataset1labels,
        'dataset1'      : dataset1counts,
        'dataset2labels': dataset2labels,
        'dataset2'      : dataset2counts,
        'dataset3labels': dataset3labels,
        'dataset3'      : dataset3counts,
        })


@login_required
@group_required("Researchers", "Linkworkers", "PACs")
def moodtimeline_chart(request, pk):
    try:
        client_user_id = pk
        client_user = User.objects.get(id=pk)
    except  User.DoesNotExist:
        raise Http404("Unknown user")  # handle Unrecognised User error at this point
    client_profile = UserProfile.objects.filter(user=client_user)[0]

    datastartdate = datetime.datetime.combine(
            datetime.date.today(), datetime.time(0, 0, 0),
            tzinfo=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo  # timezone.utc
            ) - datetime.timedelta(days=20)

    tmpMoodEntriesAndLabels = getDailyMoodsAndLabels(client_profile.id,
                                                     datastartdate,
                                                     21,
                                                     shortdatelabels=True,
                                                     )
    tmpMoodLabels = tmpMoodEntriesAndLabels.get("labels")
    tmpMoodEntries = tmpMoodEntriesAndLabels.get("moods")

    tmpMoodTimes = []
    tmpMoodStrings = []
    tmpMoodPositivityList = []
    tmpMoodActivityList = []

    for tmp_mood_entry in tmpMoodEntries:
        if tmp_mood_entry:
            tmpMoodTime = tmp_mood_entry.time
            # tmpMoodString = MoodLookup.get(tmp_mood_entry.current_mood, "No mood")
            tmpMoodString = tmp_mood_entry.current_mood
            tmpMoodPositivity = MoodPositivityLookup.get(tmpMoodString)
            tmpMoodActivity = MoodActivityLookup.get(tmpMoodString)
        else:
            tmpMoodTime = None
            tmpMoodString = "No mood"
            tmpMoodPositivity = 0
            tmpMoodActivity = 0
        tmpMoodTimes.append(tmpMoodTime)
        tmpMoodStrings.append(tmpMoodString)
        tmpMoodPositivityList.append(tmpMoodPositivity)
        tmpMoodActivityList.append(tmpMoodActivity)

    # print("---------------------------------------------")
    # print(tmpMoodTimes)
    # print("---------------------------------------------")
    # print(tmpMoodStrings)
    # print("---------------------------------------------")

    # data1 = ["-2", "-1", "-2",  "0",  "1",  "1",  "2", "-1",  "2", "-1"]
    # data2 = ["0",  "-1",  "0",  "1",  "2",  "1",  "2", "-2",  "0",  "1"]

    return JsonResponse(data={
        'labels'  : tmpMoodLabels,
        'dataset1': tmpMoodPositivityList,
        'dataset2': tmpMoodActivityList,
        })


@login_required
@group_required("Researchers", "Linkworkers", "PACs")
def moodsparkline_chart(request, pk):
    try:
        client_user_id = pk
        client_user = User.objects.get(id=pk)
    except  User.DoesNotExist:
        raise Http404("Unknown user")  # handle Unrecognised User error at this point
    client_profile = UserProfile.objects.filter(user=client_user)[0]

    datastartdate = datetime.datetime.combine(
            datetime.date.today(), datetime.time(0, 0, 0),
            tzinfo=datetime.datetime.now(
                    datetime.timezone.utc).astimezone().tzinfo  # timezone.utc
            ) - datetime.timedelta(days=7)

    tmpMoodEntriesAndLabels = getDailyMoodsAndLabels(client_profile.id,
                                                     datastartdate,
                                                     8,
                                                     shortdatelabels=True,
                                                     )
    tmpMoodLabels = tmpMoodEntriesAndLabels.get("labels")
    tmpMoodEntries = tmpMoodEntriesAndLabels.get("moods")

    tmpMoodTimes = []
    tmpMoodStrings = []
    tmpMoodPositivityList = []

    for tmp_mood_entry in tmpMoodEntries:
        if tmp_mood_entry:
            tmpMoodTime = tmp_mood_entry.time
            # tmpMoodString = MoodLookup.get(tmp_mood_entry.current_mood,"No mood")
            tmpMoodString = tmp_mood_entry.current_mood
            tmpMoodPositivity = MoodPositivityLookup.get(tmpMoodString)
        else:
            tmpMoodTime = None
            tmpMoodString = "No mood"
            tmpMoodPositivity = 0
        tmpMoodTimes.append(tmpMoodTime)
        tmpMoodStrings.append(tmpMoodString)
        tmpMoodPositivityList.append(tmpMoodPositivity)

    return JsonResponse(data={
        'labels'  : tmpMoodLabels,
        'dataset1': tmpMoodPositivityList,
        })
