import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APIClient
from user_profile.models import UserProfile

from .models import Moods, get_random_mood, is_a_mood


class MoodTest(TestCase):
    def test_get_random_mood(self):
        mood = "HP"
        self.assertTrue(is_a_mood(mood))

        mood = get_random_mood()
        self.assertTrue(is_a_mood(mood))

        mood = "cats"
        self.assertFalse(is_a_mood(mood))


class MoodDataTest(TestCase):
    @freeze_time("2012-01-14 12:00:01 UTC")
    def test_mood_data(self):
        paul = User.objects.create_user(first_name="paul", last_name="lunn", username="user1", email="paul@email.com", )
        paul.save()
        user_profile = UserProfile(user=paul, role=UserProfile.PERSON_AT_CENTRE)
        user_profile.save()

        new_mood = Moods.objects.create(user=user_profile, current_mood="BD")

        self.assertEqual(new_mood.current_mood, "BD")
        self.assertEqual(new_mood.time, datetime.datetime(2012, 1, 14, 12, 0, 1, tzinfo=timezone.utc))


class MoodApiTest(TestCase):
    @freeze_time("2012-01-14 12:00:01 UTC")
    def test_mood_api(self):
        fn = "paul"
        ln = "lunn"
        un = "user1"
        em = "paul@email.com"
        ph = "01290 000200"
        ro = UserProfile.PERSON_AT_CENTRE
        pw = "pg39d2£"

        paull = User.objects.create_user(first_name=fn, last_name=ln, username=un, email=em, password=pw)
        user_profile = UserProfile(user=paull, phone=ph, role=ro)
        user_profile.save()

        new_mood = Moods.objects.create(user=user_profile, current_mood="BD")
        new_mood = Moods.objects.create(user=user_profile, current_mood="HP")

        client = APIClient()
        client.login(username=un, password=pw)
        response = client.get('/moods/')
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()
        # print(response_dict)

        self.assertEqual(response_dict[0]["id"], 1)
        self.assertEqual(response_dict[0]["current_mood"], "BD")
        self.assertEqual(response_dict[0]["time"], '2012-01-14T12:00:01Z')

        self.assertEqual(response_dict[1]["id"], 2)
        self.assertEqual(response_dict[1]["current_mood"], "HP")
        self.assertEqual(response_dict[1]["time"], '2012-01-14T12:00:01Z')
