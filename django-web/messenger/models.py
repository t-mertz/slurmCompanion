from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Message(models.Model):
    """Message sent by one user to one or many others."""
    content = models.TextField()
    time_sent = models.DateTimeField()
    sender = models.ForeignKey(User, related_name='+')
    recipient = models.ForeignKey(User, related_name='+') # make one-to-many?
    #title = models.CharField()
    #attachment = models.FileField()
    #flag = models.BigIntegerField() # important

    def asdict(self):
        return {'content': self.content,
                'time_sent': self.time_sent,
                'sender': self.sender,
                'recipient': self.recipient}


def get_recent_messages(user, days=5):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=days)
    earliest_date = now - delta
    return Message.objects.filter(recipient=user, time_sent__gte=earliest_date)


class MessageSettings(models.Model):
    """Settings for the messenger view."""
    user = models.OneToOneField(User)

