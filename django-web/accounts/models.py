from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contact(models.Model):
    """A contact relation between users.

    A user's contact list is made up of the `contact` entries.
    This a one-sided relationship. Adding a UserB as contact to
    UserA does not add UserA as contact to UserB.
    """
    user = models.ForeignKey(User, related_name='thisuser')
    contact = models.ForeignKey(User, related_name='otheruser')

class UserLoginStatus(models.Model):
    """Login status of a user."""
    last_login = models.DateTimeField
    login_status = models.BooleanField
    status_hidden = models.BooleanField