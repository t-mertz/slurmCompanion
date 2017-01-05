from django.db import models
from django.forms import widgets
from django.contrib.auth.models import User

class UserData(models.Model):
    owner = models.ForeignKey(User)
    user_id = models.IntegerField()
    server_url = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(widgets.PasswordInput)