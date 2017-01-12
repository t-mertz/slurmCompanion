from django.contrib import admin

from .models import Info

# Register your models here.

class InfoAdmin(admin.ModelAdmin):
    fields = ['title', 'author', 'pub_date', 'content']
    list_display = ('title', 'author', 'pub_date')

admin.site.register(Info, InfoAdmin)