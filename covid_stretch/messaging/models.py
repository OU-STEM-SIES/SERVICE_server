# The messaging system is intended to store messages btweeen Linkworkers, clients, and admins.
# its intended for the txt based system which may be required initally

from django.db import models
from django.utils import timezone
from user_profile.models import UserProfile


class MessageManager(models.Manager):
    def create_message(self, send, recip, new_message):
        mess = self.create(sender=send, recipient=recip, message=new_message)
        return mess


class Messages(models.Model):
    TEXT_MESSAGE = "TXT"
    ADMIN_MESSAGE = "ADM"

    MESSAGE_TYPES = (
        (TEXT_MESSAGE, "text"),
        (ADMIN_MESSAGE, "admin"),
        )
    sender = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="sender")
    recipient = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="receiver")
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    message_type = models.CharField(max_length=3, choices=MESSAGE_TYPES, default=TEXT_MESSAGE)

    objects = MessageManager()

    def get_message_details(self):
        return "Message: From: {} To: {} Date: {} Type: {} Body:{} ".format(
                self.sender.user.username, self.recipient.user.username, self.date, self.message_type, self.message,
                )

    def __str__(self):
        return self.get_message_details()
