from django.conf.urls import url, include

from . import views

app_name = 'messenger'

urlpatterns = [
    url(r"^$", views.messenger, name="messengerhome"),
    url(r"^(?P<user_id>[0-9]+)/$", views.messenger_session),
    url(r"^compose$", views.compose, name="compose"),
]