from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    """Message sent by one user to one or many others."""
    content = models.TextField()
    time_sent = models.DateTimeField()
    sender = models.ForeignKey(User)
    recipient = models.ForeignKey(User) # make one-to-many?
    #title = models.CharField()
    #attachment = models.FileField()
    #flag = models.BigIntegerField() # important

class MessageSettings(models.Model):
    """Settings for the messenger view."""
    user = models.ForeignKey(User, unique=True)

