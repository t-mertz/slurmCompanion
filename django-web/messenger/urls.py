from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r"^$", views.messenger, name="messengerhome"),
    url(r"^(?P<user_id>[0-9]+)/$", views.messenger_session),
]