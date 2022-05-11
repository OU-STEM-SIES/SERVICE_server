from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.models import UserProfile, Person_at_centre, Linkworker, Supporter
from rest_framework.test import APIRequestFactory
from django.test import Client
from rest_framework.test import APIClient
from django.utils import timezone
from freezegun import freeze_time
import datetime

# Create your tests here.
class UserProfileTest(TestCase):
    def setUp(self):
        # self.date_of_birth = datetime.date.today()
        self.phone_number = "0116 2767542"
        self.gender = "MAN"
        self.ethnicity = "CHIN"
        self.education = "GCE5"
        self.disability = "SVDS"
        self.marital_status = "DIVD"
        self.smoking = True
        self.alcohol_units_per_week = 10
        # self.health_conditions = 

        self.paul = User.objects.create_user(first_name="paul", last_name="lunn", username="user1", email="paul@email.com")
        self.user_profile = UserProfile(user=self.paul, 
        phone=self.phone_number,
        gender = self.gender,
        ethnicity = self.ethnicity,
        education =  self.education,
        disability = self.disability,
        marital_status = self.marital_status,
        smoking = self.smoking,
        alcohol_units_per_week = self.alcohol_units_per_week

        )

    def test_user_details(self):
        
        self.assertEqual(self.user_profile.user.first_name, "paul")
        self.assertEqual(self.user_profile.user.last_name, "lunn")
        self.assertEqual(self.user_profile.user.email, "paul@email.com")
        self.assertEqual(self.user_profile.user.username, "user1")

    def test_join_name(self):
       
        full_name = self.user_profile.get_full_name()
        extracted_name = self.paul.first_name + " " + self.paul.last_name
        self.assertEqual(full_name, extracted_name)

    def test_roles(self):

        # default role is NO_ROLE
        self.assertEqual(self.user_profile.role, UserProfile.SUPPORTER)

        # now check each role
        self.user_profile.role = UserProfile.SUPPORTER
        self.assertTrue(self.user_profile.is_supporter())

        # now check each role
        self.user_profile.role = UserProfile.LINKWORKER
        self.assertTrue(self.user_profile.is_linkworker())
        self.assertFalse(self.user_profile.is_supporter())

        # now check each role
        self.user_profile.role = UserProfile.PERSON_AT_CENTRE
        self.assertTrue(self.user_profile.is_pac())
        self.assertFalse(self.user_profile.is_supporter())

        # now check each role
        self.user_profile.role = UserProfile.NO_ROLE
        self.assertFalse(self.user_profile.is_supporter())

    def test_phone(self):
        self.assertEqual(self.user_profile.phone, self.phone_number)

    def test_get_id(self):
        self.assertEqual(self.user_profile.user.id, self.user_profile.get_id())

    def test_additional_data(self):
        self.assertEqual(self.user_profile.ethnicity , self.ethnicity)
        self.assertEqual(self.user_profile.education , self.education)
        self.assertEqual(self.user_profile.disability , self.disability)
        self.assertEqual(self.user_profile.marital_status , self.marital_status)
        self.assertEqual(self.user_profile.smoking , self.smoking)
        self.assertEqual(self.user_profile.alcohol_units_per_week , self.alcohol_units_per_week)



class SupportersTest(TestCase):
    def setUp(self):
        self.paul = User.objects.create_user(first_name="paul", last_name="lunn", username="user1", email="paul@email.com")

        self.user1 = User.objects.create_user(first_name="s1", last_name="S1", username="supp1", email="s1@email.com")
        self.user2 = User.objects.create_user(first_name="s2", last_name="S2", username="supp2", email="s2@email.com")
        self.user3 = User.objects.create_user(first_name="s3", last_name="S3", username="supp3", email="s3@email.com")

        self.profile1 = UserProfile.objects.create(user=self.user1)
        self.profile2 = UserProfile.objects.create(user=self.user2)
        self.profile3 = UserProfile.objects.create(user=self.user3)

        self.s1 = Supporter.objects.create(user_profile=self.profile1)
        self.s2 = Supporter.objects.create(user_profile=self.profile2)
        self.s3 = Supporter.objects.create(user_profile=self.profile3)

         
        self.paul_profile = UserProfile(user=self.paul, role=UserProfile.PERSON_AT_CENTRE)
        self.paul_profile.save()
        self.paul_pac = Person_at_centre.objects.create(user_profile= self.paul_profile)
        self.paul_pac.supporters.add(self.s1, self.s2, self.s3)


    def test_get_supporter(self):
        self.assertTrue(self.paul_pac.get_supporter(0) == self.s1)
        self.assertTrue(self.paul_pac.get_supporter(1) == self.s2)
        self.assertTrue(self.paul_pac.get_supporter(2) == self.s3)
        self.assertTrue(self.paul_pac.get_supporter(5) == None)
        self.assertTrue(self.paul_pac.get_supporter(-1) == None)

    def test_supporter_details(self):
        self.assertEqual(self.paul_pac.get_supporter(0).user_profile.user.first_name, self.s1.user_profile.user.first_name)
        self.assertEqual(self.paul_pac.get_supporter(0).user_profile.user.last_name, self.s1.user_profile.user.last_name)

class ApiUserProfileTest(TestCase):
    def test_api(self):
        fn = "paul"
        ln = "lunn"
        un = "user1"
        em = "paul@email.com"
        self.role = UserProfile.PERSON_AT_CENTRE
        pw = "pg39d2£"
        self.dob = datetime.date(2010, 1, 2)
        self.phone_number = "0116 2767542"
        self.gender = "MAN"
        self.ethnicity = "CHIN"
        self.education = "GCE5"
        self.disability = "SVDS"
        self.marital_status = "DIVD"
        self.smoking = True
        self.alcohol_units_per_week = 10

        self.paul = User.objects.create_user(first_name="paul", last_name="lunn", username="user1", email="paul@email.com", password=pw)
        self.user_profile = UserProfile(user=self.paul, 
        role = self.role,
        phone=self.phone_number,
        date_of_birth = self.dob,
        gender = self.gender,
        ethnicity = self.ethnicity,
        education =  self.education,
        disability = self.disability,
        marital_status = self.marital_status,
        smoking = self.smoking,
        alcohol_units_per_week = self.alcohol_units_per_week)
        self.user_profile.save()

        client = APIClient()
        client.login(username=un, password=pw)
        response = client.get('/profile/')
        self.assertEqual(response.status_code, 200)

        response_dict = response.json()[0]
        # print(response_dict['user']['username'])
        
        self.assertEqual(response_dict["user"]["username"], un)
        self.assertEqual(response_dict["user"]["first_name"], fn)
        self.assertEqual(response_dict["user"]["last_name"], ln)
        self.assertEqual(response_dict["user"]["email"], em)
        self.assertEqual(response_dict["role"], self.role)
        self.assertEqual(response_dict["phone"], self.phone_number)
        # self.assertEqual(response_dict["date_of_birth"], datetime.date(2010, 1, 2))
        self.assertEqual(response_dict["gender"], self.gender)
        self.assertEqual(response_dict["ethnicity"], self.ethnicity)
        self.assertEqual(response_dict["education"], self.education)
        self.assertEqual(response_dict["disability"], self.disability)
        self.assertEqual(response_dict["marital_status"], self.marital_status)
        self.assertEqual(response_dict["smoking"], self.smoking)
        self.assertEqual(response_dict["alcohol_units_per_week"], self.alcohol_units_per_week )
        



        
        
