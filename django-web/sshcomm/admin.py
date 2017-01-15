from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User

from .models import RemoteServer, UserData

# Register your models here.

# this will go into the User admin
class UserDataAdmin(admin.ModelAdmin):
    #fields = UserAdmin.fields + ['server_name']
    fields = ['owner', 'server', 'user_name']

admin.site.register(UserData, UserDataAdmin)



class RemoteServerAdmin(admin.ModelAdmin):
    fields = ['server_name', 'server_url', 'date_added']
    list_display = ('server_name', 'date_added')

admin.site.register(RemoteServer, RemoteServerAdmin)

