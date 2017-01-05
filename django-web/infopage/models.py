from django.db import models

# Create your models here.

class Info(models.Model):
    title = models.TextField()
    author = models.TextField()
    content = models.TextField()
    pub_date = models.DateTimeField()