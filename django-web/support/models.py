from django.db import models


# Create your models here.

class SupportTicket(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField()
    user = models.CharField(max_length=100)