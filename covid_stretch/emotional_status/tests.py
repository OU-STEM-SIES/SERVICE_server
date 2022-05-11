import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APIClient
from user_profile.models import UserProfile

from .models import Emotional_status, get_random_emotional_support_value


class EmotionTest(TestCase):
    @freeze_time("2012-01-14 12:00:01 UTC")
    def test_emotion(self):
        fn = "paul"
        ln = "lunn"
        un = "user1"
        em = "paul@email.com"
        ph = "01290 000200"
        ro = UserProfile.PERSON_AT_CENTRE
        pw = "pg39d2£"

        paull = User.objects.create_user(first_name=fn, last_name=ln, username=un, email=em, password=pw)
        loneliness = get_random_emotional_support_value()
        wellbeing = get_random_emotional_support_value()
        paull.save()

        new_emotion = Emotional_status.objects.create(user=paull, loneliness_level=loneliness,
                                                      general_wellbeing=wellbeing)

        self.assertEqual(new_emotion.loneliness_level, loneliness)
        self.assertEqual(new_emotion.general_wellbeing, wellbeing)
        self.assertEqual(new_emotion.time, datetime.datetime(2012, 1, 14, 12, 0, 1, tzinfo=timezone.utc))


class EmotionApiTest(TestCase):
    @freeze_time("2012-01-14 12:00:01 UTC")
    def test_emotion_api(self):
        fn = "paul"
        ln = "lunn"
        un = "user1"
        em = "paul@email.com"
        ph = "01290 000200"
        ro = UserProfile.PERSON_AT_CENTRE
        pw = "pg39d2£"

        paull = User.objects.create_user(first_name=fn, last_name=ln, username=un, email=em, password=pw)
        paull.save()

        Emotional_status.objects.create(user=paull, loneliness_level=5, general_wellbeing=4)
        Emotional_status.objects.create(user=paull, loneliness_level=9, general_wellbeing=1)

        client = APIClient()
        client.login(username=un, password=pw)
        response = client.get('/emotions/')
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        # print(response_dict)

        self.assertEqual(response_dict[0]["id"], 1)
        self.assertEqual(response_dict[0]["loneliness_level"], 5)
        self.assertEqual(response_dict[0]["general_wellbeing"], 4)
        self.assertEqual(response_dict[0]["time"], '2012-01-14T12:00:01Z')

        self.assertEqual(response_dict[1]["id"], 2)
        self.assertEqual(response_dict[1]["loneliness_level"], 9)
        self.assertEqual(response_dict[1]["general_wellbeing"], 1)
        self.assertEqual(response_dict[1]["time"], '2012-01-14T12:00:01Z')
