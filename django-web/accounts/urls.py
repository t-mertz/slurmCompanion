from django.conf.urls import url

from .views import manage_servers

app_name = 'accounts'

urlpatterns=[
    url(r'^servers/manage/$', manage_servers, 'server_management'),
]