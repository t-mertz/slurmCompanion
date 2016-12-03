from django.contrib import admin

from .models import Command

# Register your models here.

class CommandAdmin(admin.ModelAdmin):
    fields = ['command_text']

admin.site.register(Command, CommandAdmin)