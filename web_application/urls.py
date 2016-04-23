from django.conf.urls import include, url
from django.contrib import admin

from web_application import views
from views import UserProfileView

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^user/(?P<slug>[\w.@+-]+)/$', UserProfileView.as_view(), name='user_profile'),
    url(r'^$', views.index, name='index'),
]
