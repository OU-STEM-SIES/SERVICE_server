from rest_framework import viewsets

from .models import Messages
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
