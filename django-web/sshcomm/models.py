from django.db import models
from django.forms import widgets
from django.contrib.auth.models import User

class RemoteServer(models.Model):
    server_url = models.CharField(max_length=50)
    server_name = models.CharField(max_length=20)
    date_added = models.DateField()

    def get_installed_servers():
        server_list = RemoteServer.objects.all()

        return [(entry.server_name, entry.server_name) for entry in server_list]

class UserData(models.Model):
    owner = models.ForeignKey(User)
    #user_id = models.IntegerField()
    profile_name = models.CharField(max_length=20)
    server = models.ForeignKey(RemoteServer)
    user_name = models.CharField(max_length=20)
    user_password = models.CharField(widgets.PasswordInput, max_length=40)
