from django.contrib import admin

from .models import SupportTicket

# Register your models here.

class SupportTicketAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'pub_date']
    list_display = ('title', 'pub_date', 'user')

admin.site.register(SupportTicket, SupportTicketAdmin)