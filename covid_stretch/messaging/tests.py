from django.contrib.auth.models import User
from django.test import TestCase
from user_profile.models import UserProfile

from .models import Messages


# Create your tests here.
class MessagingTest(TestCase):
    def test_user_details(self):
        paul = User.objects.create_user(
                first_name="paul",
                last_name="lunn",
                username="user1",
                email="paul@email.com",
                )
        ozzy = User.objects.create_user(
                first_name="ozzy",
                last_name="lunn",
                username="user2",
                email="ozzy@email.com",
                )
        send = UserProfile(user=paul)
        send.save()

        self.assertEqual(send.user.first_name, "paul")
        self.assertEqual(send.user.last_name, "lunn")
        self.assertEqual(send.user.email, "paul@email.com")
        self.assertEqual(send.user.username, "user1")

        rec = UserProfile(user=ozzy)
        rec.save()
        self.assertEqual(rec.user.first_name, "ozzy")
        self.assertEqual(rec.user.last_name, "lunn")
        self.assertEqual(rec.user.email, "ozzy@email.com")
        self.assertEqual(rec.user.username, "user2")

        mess = Messages.objects.create(sender=send, recipient=rec, message="hello")
        self.assertEqual(mess.sender.user.first_name, "paul")
        self.assertEqual(mess.recipient.user.first_name, "ozzy")
        self.assertEqual(mess.message, "hello")
