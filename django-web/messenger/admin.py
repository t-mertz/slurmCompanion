from django.contrib import admin

from .models import Message

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    fields = ['recipient', 'sender', 'time_sent', 'content']

admin.site.register(Message, MessageAdmin)