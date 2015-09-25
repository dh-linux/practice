#!usr/bin/env python
#coding: utf-8
from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('',
     url(r'^$', 'log.views.index',name="log"),
     url(r'^index$', 'log.views.index',name="log_index"),
     url(r'^search/$', 'log.views.search', name="log_search"),
)