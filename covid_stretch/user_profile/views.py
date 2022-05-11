import json
from datetime import datetime
# from typing import Tuple, Any

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework import viewsets  # generics
from rest_framework.authentication import TokenAuthentication  # SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import UserProfile, Person_at_centre, Supporter, UserLog  # , Linkworker
from .serializers import UserSerializer, UserProfileSerializer, CoSSerializer, SupporterSerializer, UserLogSerializer


# from rest_framework.response import Response
# from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserSerializer
    
    def get_queryset(self):
        # return currently logged in user details
        user = self.request.user
        return User.objects.filter(username=user)


class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserProfileSerializer
    
    # queryset = UserProfile.objects.all()
    def get_queryset(self):
        try:
            userid = self.request.query_params['id']
            user = User.objects.get(id=userid)
        except:
            user = self.request.user
        
        return UserProfile.objects.filter(user=user)


class CoSViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    # queryset = Person_at_centre.objects.all()
    # .filter(user_profile=UserProfile.objects.filter(user=self.request.user))
    serializer_class = CoSSerializer

    def get_queryset(self):
        user = self.request.user
        profile = UserProfile.objects.filter(user=user)[0]
        return Person_at_centre.objects.filter(user_profile=profile)

# class LinkworkerViewSet(viewsets.ModelViewSet):
#     queryset = Linkworker.objects.all()
#     serializer_class = LinkworkerSerializer


class UserLogViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserLogSerializer

    def get_queryset(self):
        try:
            userid = self.request.query_params['id']
            user = User.objects.get(id=userid)
        except:
            user = self.request.user
        logentries = UserLog.objects.filter(user=user)
        print("Log entries: " + str(logentries.count()))
        return logentries


class RegisterNewUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

def create_user(user_details):
    if "password" in user_details:
        tmp_password = user_details['password']
    else:
        # tmp_password = User.objects.set_unusable_password()
        tmp_password = User.objects.make_random_password()
        # new_user.set_password(password)
        # new_user.save(update_fields=['password'])

    if "username" in user_details:
        tmp_username = user_details['username']
    else:
        tmp_username = user_details['first_name'] + "_" + user_details['last_name'] + "_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    if "email" in user_details:
        tmp_email = user_details['email']
    else:
        tmp_email = ""

    new_user = User.objects.create(
        username = tmp_username,
        password = tmp_password,
        first_name = user_details['first_name'],
        last_name = user_details['last_name'],
        email = tmp_email,
        is_active=False,
    )
    # new_user = User.objects.create(user_details)
    # print("--- Created new user object")

    if not ("password" in user_details):
        new_user.set_unusable_password()

    new_user.save()
    print("--- Saved new user object: " + str(new_user.id) + " - " + str(new_user.username))
    return new_user


@api_view(["POST"])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_supporter(request):
    payload = json.loads(request.body)
    user = request.user
    user_profile = UserProfile.objects.filter(user=user)[0]
    pac_record = Person_at_centre.objects.get(user_profile=user_profile)

    try:
        new_supporter = create_user(payload["new_supporter"])
        new_supporter_profile = UserProfile.objects.create(
            user=new_supporter,
            role="SUP",
        )
        new_supporter_profile.save()
        saved_new_supporter_profile = UserProfile.objects.get(id=new_supporter_profile.id)
        print("--- Saved new user profile object: " + str(new_supporter_profile.id))

        new_supporter_record = Supporter.objects.create(
            user_profile = saved_new_supporter_profile,
            group = payload["group"],
            how_often_expected_interaction = payload["how_often_expected_interaction"],
        )

        if payload["circle_of_support"] == 1:
            pac_record.circle_of_support_1.add(new_supporter_record)
            tmp_circlenumber = "1"
        elif payload["circle_of_support"] == 3:
            pac_record.circle_of_support_3.add(new_supporter_record)
            tmp_circlenumber = "3"
        else:
            pac_record.circle_of_support_2.add(new_supporter_record)
            tmp_circlenumber = "2"

        # serializer = UserProfileSerializer(saved_new_supporter_profile)
        serializer = SupporterSerializer(new_supporter_record)

        newUserLogEntry = UserLog.objects.create(
            type = "COFU",
            user = request.user,
            description = "User " + str(user.id) + " (" + str(user.first_name) + " " + str(user.last_name) + ") registered a new Supporter: " + str(new_supporter_record.user_profile.user.first_name) + " " + str(new_supporter_record.user_profile.user.last_name) + " to their circle " + tmp_circlenumber + ".",
            # prediffjson = json.dumps({}),
            postdiffjson = serializer.data
        )

        return JsonResponse({'supporter': serializer.data}, safe=False, status=status.HTTP_201_CREATED)

    except ObjectDoesNotExist as e:
        print("--- Error: " + str(e))
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        print("--- Error: " + str(e))
        return JsonResponse({'error': 'Something terrible went wrong: ' + str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def remove_supporter(request):
    # payload fields:
    # supporter_record_id
    # delete_supporter (Boolean)
    payload = json.loads(request.body)
    user = request.user
    user_profile = UserProfile.objects.filter(user=user)[0]
    pac_record = Person_at_centre.objects.get(user_profile=user_profile)
    supporter_record_id = payload["supporter_record_id"]

    supporter_record = Supporter.objects.filter(id=supporter_record_id)[0]
    supporter_profile = supporter_record.user_profile
    supporter_user = supporter_profile.user
    serializer = SupporterSerializer(supporter_record)

    pac_record.circle_of_support_1.remove(supporter_record)
    pac_record.circle_of_support_2.remove(supporter_record)
    pac_record.circle_of_support_3.remove(supporter_record)
    print("Removed instances from CoS lists")

    newUserLogEntry = UserLog.objects.create(
        type="COFU",
        user=request.user,
        description="User " + str(user.id) + " (" + str(user.first_name) + " " \
                    + str(user.last_name) + ") removed a Supporter: " \
                    + str(supporter_record.user_profile.user.first_name) + " " \
                    + str(supporter_record.user_profile.user.last_name)\
                    + " from their circles.",
        prediffjson=serializer.data,
        postdiffjson=json.dumps({})
    )

    if payload["delete_supporter"]:
        # delete_supporter(supporter_record_id)
        tmp_old_first_name = supporter_user.first_name
        tmp_old_last_name = supporter_user.last_name
        supporter_user.first_name = "Anonymised"
        supporter_user.last_name = "Anonymised"
        supporter_user.email = ""
        supporter_user.username = "Removed from " + user.first_name + " " + user.last_name + "'s circles of support at " + str(datetime.now())
        supporter_user.is_staff = False
        supporter_user.is_active = False
        supporter_user.save()

        anonserializer = SupporterSerializer(supporter_record)

        newUserLogEntry = UserLog.objects.create(
            type="DELE",
            user=request.user,
            description="User " + str(user.id) + " (" + str(user.first_name) + " " \
                        + str(user.last_name) + ") deleted (i.e. anonymised) a Supporter: " \
                        + tmp_old_first_name + " " \
                        + tmp_old_last_name \
                        + " from their circles.",
            prediffjson=serializer.data,
            postdiffjson=anonserializer.data
        )

        # return JsonResponse({'supporter': serializer.data}, safe=False, status=status.HTTP_410_GONE)
    return JsonResponse({'supporter': serializer.data}, safe=False, status=status.HTTP_205_RESET_CONTENT)

def delete_supporter(supporter_record_id):
    supporter_record = Supporter.objects.filter(id=supporter_record_id)[0]
    print ("Supporter record: " + str(supporter_record))
    supporter_profile = supporter_record.user_profile
    print ("Supporter profile: " + str(supporter_profile))
    supporter_user = supporter_profile.user
    print ("Supporter user: " + str(supporter_user))

    supporter_record.delete()
    print ("Supporter record has been deleted.")
    supporter_profile.delete()
    print ("Supporter profile has been deleted.")
    supporter_user.delete()
    print ("Supporter user has been deleted.")


@api_view(["POST"])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_supporter(request):
    payload = json.loads(request.body)
    supporter_record_id = payload["supporter_record_id"]
    to_circle = payload["to_circle"]
    first_name = payload["first_name"]
    last_name = payload["last_name"]
    group = payload["group"]
    how_often_expected_interaction = payload["how_often_expected_interaction"]

    user = request.user
    user_profile = UserProfile.objects.filter(user=user)[0]
    pac_record = Person_at_centre.objects.get(user_profile=user_profile)

    supporter_record = Supporter.objects.filter(id=supporter_record_id)[0]
    supporter_profile = supporter_record.user_profile
    supporter_user = supporter_profile.user
    serializer = SupporterSerializer(supporter_record)

    supporter_user.first_name = first_name
    supporter_user.last_name = last_name
    supporter_user.save()

    supporter_record.group = group
    supporter_record.how_often_expected_interaction = how_often_expected_interaction
    supporter_record.save()

    pac_record.circle_of_support_1.remove(supporter_record)
    pac_record.circle_of_support_3.remove(supporter_record)
    pac_record.circle_of_support_2.remove(supporter_record)

    if to_circle == 1:
        pac_record.circle_of_support_1.add(supporter_record)
    elif to_circle == 3:
        pac_record.circle_of_support_3.add(supporter_record)
    else:
        pac_record.circle_of_support_2.add(supporter_record)

    return JsonResponse({'supporter': serializer.data}, safe=False, status=status.HTTP_205_RESET_CONTENT)


class UserLogList(generics.ListAPIView):
    """
    API endpoint that allows UserLogs to be viewed.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # queryset = Moods.objects.all()
    serializer_class = UserLogSerializer

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

        UserLoglist = UserLog.objects.filter(user__in=target_user.order_by("-time"))
        return UserLoglist
