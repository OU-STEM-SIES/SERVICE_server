from rest_framework import viewsets

from .models import Emotional_status
from .serializers import EmotionSerializer


class EmotionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = Moods.objects.all()
    serializer_class = EmotionSerializer

    def get_queryset(self):
        # return currently logged in user details
        # current_profile = UserProfile.objects.filter(user=self.request.user)
        return Emotional_status.objects.filter(user=self.request.user)

# Create your views here.
