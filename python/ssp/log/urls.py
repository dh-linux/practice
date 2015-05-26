from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?P<appname>.*)/$','log.views.app'),
    url(r'^$', 'log.views.index'),
)
