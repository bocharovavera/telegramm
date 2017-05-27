# -*- coding: utf8 -*-

from django.conf.urls import url

from .views import CommandReceiveView

urlpatterns = [
    url(r'^bot/(?P<bot_token>.+)/$', CommandReceiveView.as_view(), name='command'),
]

#http://194.87.93.29/bot/308828925:AAFbww2ge3WxWcsYDXsdy5-PlLBCQWS97QQ/