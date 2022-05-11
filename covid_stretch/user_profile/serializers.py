import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import Field

from .models import UserProfile, Person_at_centre, Supporter, UserLog


class TimeWithTimezoneField(Field):
    # See https://stackoverflow.com/questions/63548884/how-to-serialize-time-with-timezone-in-django-rest-frameworks-serializer

    default_error_messages = {
        'invalid': 'Time has wrong format, expecting %H:%M:%S%z.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, value):
        value_with_date = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + value
        try:
            parsed = datetime.datetime.strptime(value_with_date, '%Y-%m-%d %H:%M:%S%z')
        except (ValueError, TypeError) as e:
            pass
        else:
            return parsed
        self.fail('invalid')

    def to_representation(self, value):
        if not value:
            return None

        if isinstance(value, str):
            return value

        return timezone.make_naive(value, timezone.utc).strftime("%H:%M:%S+00:00")



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "last_login"]
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# NOT WORKING: get user profile http://127.0.0.1:8000/profile/1/ 1 = profile number
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        # fields='__all__'
        fields = ["id","user", "role", "phone", "image", "date_of_birth", "gender", "ethnicity", "education", "disability",
                  "marital_status", "smoking", "alcohol_units_per_week", "health_conditions",
                  "things_liked", "things_disliked", "family_has", "family_bond", "community_bond",
                  "social_groups", "social_group_other", "social_bond", "link_worker_has", "link_worker_bond"
                  ]

        # def create(self, validated_data):
        #     return UserProfile.objects.create(**validated_data)


class SupporterSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    class Meta:
        model = Supporter
        fields='__all__'

class CoSSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    circle_of_support_1 = SupporterSerializer(read_only=True, many=True)
    circle_of_support_2 = SupporterSerializer(read_only=True, many=True)
    circle_of_support_3 = SupporterSerializer(read_only=True, many=True)
    class Meta:
        model = Person_at_centre
        # fields='__all__'
        fields = ["user_profile",
                  "circle_of_support_1",
                  "circle_of_support_2",
                  "circle_of_support_3"
                  ]

class UserLogSerializer(serializers.ModelSerializer):
    LOG_ENTRY_TYPES = {
        "COFU": "User updated their Circle Of Friends",
        "PROF": "User updated their profile",
        "PSWD": "User changed their password (password is not logged)",
        "PRES": "User requested a password reset email",
        "DELE": "User and associated data deleted",
    }
    class Meta:
        model=UserLog
        fields = [
            "id",
            "timestamp",
            "user",
            "type",
            "description",
            "prediffjson",
            "postdiffjson",
        ]
