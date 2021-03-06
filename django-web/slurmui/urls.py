"""slurmui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.sitehome, name="siteindex"),
    url(r'^user/$', views.user_home, name='userhome'),
    url(r'^user/(?P<user_id>[0-9]+)', views.user_home),
    url(r'^account/', include('accounts.urls')),
    url(r'^info/', include('infopage.urls')),
    url(r'^settings/$', views.settingspage, name="settingspage"),
    url(r'^settings/addserver/', views.serversettings_addserver, name="settings_addserver"),
    url(r'^cmd/', include('webcmd.urls')),
    url(r'^support/', include('support.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login_view, name='login')
]
