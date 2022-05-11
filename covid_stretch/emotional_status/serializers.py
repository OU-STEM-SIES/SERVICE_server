from rest_framework import serializers

from .models import Emotional_status


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotional_status
        fields = ["id", "loneliness_level", "general_wellbeing", "time"]
