from django.db import models
from django.forms import widgets

# Create your models here.

class SupportTicket(models.Model):
    title = models.CharField()
    content = models.CharField(widget=widgets.TextArea)