from rest_framework import serializers

from .models import Moods, Pastime, UserProfile

class PastimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pastime
        fields = [
            # "mood",
            "whatdoing",
            "whowith"
        ]

    def create(self, validated_data):
        return Pastime.objects.create(**validated_data)


class MoodSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()
    # user = UserSerializer(required=False)
    # pastimes = PastimeSerializer(source="get_pastimes", required=False, many=True)
    pastimes = PastimeSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Moods
        fields = [
            "id", "user", "current_mood", "time", "include_wellbeing",
            "wellbeing", "previouswellbeing",
            "loneliness", "previousloneliness",
            "pastimes", # Special case, see override above
            "spoketosomeone", "spoketosomeone_who",
            "hours_bed", "hours_sofa", "hours_kitchen", "hours_garden"
            ]
    
    def create(self, validated_data):
        return Moods.objects.create(**validated_data)
