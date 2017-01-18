from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cmd', views.cmd, name='cmd'),
    url(r'^cmd/(?P<server_name>.+)/$', views.cmd, name='server_cmd'),
    url(r'^clear', views.clear_cmd, name='clear_cmd')
]