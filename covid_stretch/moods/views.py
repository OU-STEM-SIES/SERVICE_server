import datetime
import json
import urllib

from django.contrib.auth.models import User
# from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status, viewsets, generics
from rest_framework.authentication import TokenAuthentication  # SessionAuthentication, BasicAuthentication
# from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user_profile.models import UserProfile
from . import serializers

from .models import Moods, Pastime, Supporter
from .serializers import MoodSerializer, PastimeSerializer


class MoodPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    limit_query_param = "howManyRecords"
    offset_query_param = "start"


class PagedMoodsList(generics.ListAPIView):
    """
    API endpoint that allows moods to be viewed in paged chunks.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # queryset = Moods.objects.all()
    serializer_class = MoodSerializer
    pagination_class = MoodPagination

    def get_queryset(self):
        try:  # if the requesting user is a Link Worker or Researcher they can request other people's data
            if (self.request.user.groups.filter(name="Linkworkers").exists()) \
                    or (self.request.user.groups.filter(name="Researchers").exists()):
                target_user = User.objects.get(id=self.request.query_params['id'])
            else:  # otherwise they can only have their own data (if it exists)
                target_user = self.request.user
        except User.DoesNotExist:
            raise Http404("Unknown user")

        if not target_user.groups.filter(name="PACs").exists():  # You can only request mood data for a PAC.
            raise Http404("No such PAC")

        current_profile = UserProfile.objects.filter(user=target_user)
        moodlist = Moods.objects.filter(user__in=current_profile).order_by("-time")
        return moodlist

def create_pastime(mood, pastime):
    new_pastime = Pastime.objects.create(
        mood = mood,
        whatdoing = pastime["whatdoing"],
        # whowith = supporterlist
    )
    supporterlist = []
    for supporter_id in pastime["whowith"]:
        supporterlist.append(Supporter.objects.get(id=supporter_id))
    new_pastime.whowith.set(supporterlist)

    new_pastime.save()
    # print("--- Saved new pastime object: " + str(new_pastime.id) + " - " + str(new_pastime.whatdoing) + " - " + str(supporterlist))
    return new_pastime

class MoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows moods to be viewed or created.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # queryset = Moods.objects.all()
    serializer_class = MoodSerializer

    def get_queryset(self):
        try:  # if the requesting user is a Link Worker or Researcher they can request other people's data
            if (self.request.user.groups.filter(name="Linkworkers").exists()) \
                    or (self.request.user.groups.filter(name="Researchers").exists()):
                target_user = User.objects.get(id=self.request.query_params['id'])
            else:  # otherwise they can only have their own data (if it exists)
                target_user = self.request.user
        except User.DoesNotExist:
            raise Http404("Unknown user")

        if not target_user.groups.filter(name="PACs").exists():  # You can only request mood data for a PAC.
            raise Http404("No such PAC")

        # Limit by number
        try:
            limit = int(self.request.query_params['limit'])
        except:
            limit = 0

        # Limit by dates. Expected format is javascript: encodeURIComponent("2015-02-04T05:10:58+05:30");  which results in 2015-02-04T05%3A10%3A58%2B05%3A30
        try:
            tmpdatestr = urllib.parse.unquote_plus(self.request.query_params['fromdt'])
            print("tmpdatestr: " + tmpdatestr)
            startdate = datetime.datetime.strptime(tmpdatestr, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            startdate = datetime.datetime.min
        try:
            tmpdatestr = urllib.parse.unquote_plus(self.request.query_params['todt'])
            print("tmpdatestr: " + tmpdatestr)
            enddate = datetime.datetime.strptime(tmpdatestr, "%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            enddate = datetime.datetime.max
        # print ("fromdt: " + str(startdate))
        # print ("todt: " + str(enddate))

        current_profile = UserProfile.objects.filter(user=target_user)
        if limit:  # We could just truncate afterwards, but doing it in the query line does the slice in the SQL & database engine, which is more efficient.
            moodlist = Moods.objects.filter(user__in=current_profile)\
                           .order_by("-time")\
                           .filter(time__gte=startdate, time__lte=enddate)\
                           [:limit]
        else:
            moodlist = Moods.objects.filter(user__in=current_profile).order_by("-time").filter(time__gte=startdate,
                                                                                               time__lte=enddate)

        return moodlist

    def create(self, request):
        payload = json.loads(request.body)
        # print("post: ", payload)  #request.data)
        current_profile = UserProfile.objects.get(user=request.user).id
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            # print("Got user profile " + str(user_profile.id))
            newrecordtimestamp = request.data.get("time")
            lastWellbeingRecord = Moods.objects.filter(user=user_profile, include_wellbeing=True, time__lte=newrecordtimestamp).latest("time")
            # print("Got lastwellbeing record " + str(lastWellbeingRecord.id))
            previouswellbeing = lastWellbeingRecord.wellbeing
            previousloneliness = lastWellbeingRecord.loneliness
        except:
            previouswellbeing = None
            previousloneliness = None
        if request.data.get("include_wellbeing"):
            newmooddata = {
                "user"                     : current_profile,
                "current_mood"             : request.data.get("current_mood"),
                "time"                     : request.data.get("time"),
                "include_wellbeing"        : True,
                "wellbeing"                : request.data.get("wellbeing"),
                "previouswellbeing"        : previouswellbeing,
                "loneliness"               : request.data.get("loneliness"),
                "previousloneliness"       : previousloneliness,
                # "pastimes"                 : request.data.get('pastimes'),

                # NOTE The following two items have been renamed in the database
                # but kept compatibility with old names in the API.
                # THIS SHOULD BE TEMPORARY.
                "spoketosomeone"           : request.data.get("spoketosomeone"),  # or request.data.get("whatdoing_withsomeone"),
                "spoketosomeone_who"       : request.data.get("spoketosomeone_who"),  # or request.data.get("whatdoing_withsomeone_who"),
                "hours_bed"                : request.data.get("hours_bed"),
                "hours_sofa"               : request.data.get("hours_sofa"),
                "hours_kitchen"            : request.data.get("hours_kitchen"),
                "hours_garden"             : request.data.get("hours_garden")
            }
            moodserializer = MoodSerializer(data=newmooddata)
            # print ("Got here #1")
            if moodserializer.is_valid():
                # print("Mood data is valid (excluding pastimes)")
                newmood = moodserializer.save()  # user=request.user)
                pastimelist = payload["pastimes"]
                if pastimelist:
                    for one_pastime in pastimelist:
                        # print("Pastime data isolated: " + str(one_pastime))
                        new_pastime = create_pastime(mood=newmood, pastime=one_pastime)
                        # print("Pastime " + str(new_pastime) + " created")
                return Response(moodserializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Mood data is NOT valid (ignoring any embedded pastimes)")
                return Response(moodserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            newmooddata = {
                "user"                     : current_profile,
                "current_mood"             : request.data.get("current_mood"),
                "time"                     : request.data.get("time"),
                "include_wellbeing"        : False,
                "wellbeing"                : 0,
                "previouswellbeing"        : previouswellbeing,
                "loneliness"               : 0,
                "previousloneliness"       : previousloneliness,
                # "pastimes"                 : None,
                "spoketosomeone"           : False,
                "spoketosomeone_who"       : "",
                "hours_bed"                : 0,
                "hours_sofa"               : 0,
                "hours_kitchen"            : 0,
                "hours_garden"             : 0
                }
            moodserializer = MoodSerializer(data=newmooddata)
            if moodserializer.is_valid():
                moodserializer.save()
                return Response(moodserializer.data, status=status.HTTP_201_CREATED)
            return Response(moodserializer.errors, status=status.HTTP_400_BAD_REQUEST)
