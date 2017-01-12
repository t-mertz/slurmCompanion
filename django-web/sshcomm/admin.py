from django.contrib import admin

from .models import RemoteServer

# Register your models here.

# this will go into the User admin
"""
class UserDataAdmin(admin.ModelAdmin):
    fields = ['server_url']

admin.site.register(UserData, UserDataAdmin)
"""

class RemoteServerAdmin(admin.ModelAdmin):
    fields = ['server_name', 'server_url', 'date_added']
    list_display = ('server_name', 'date_added')

admin.site.register(RemoteServer, RemoteServerAdmin)