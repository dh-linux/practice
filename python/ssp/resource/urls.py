from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^device/web/(?P<appname>.*)/$', 'resource.service.device.app_list'),
    url(r'^device/add/$', 'resource.service.device.device_add'),
    url(r'^device/search/$', 'resource.service.device.search_list'),
    url(r'^domain/addweight/$', 'resource.service.domain.addweight'),
    url(r'^domain/addnew/$', 'resource.service.domain.addNew'),
    url(r'^domain/data/(?P<act>.*)/$', 'resource.service.domain.handles'),
    url(r'^domain/addnew/(?P<appname>.*)/$', 'resource.service.domain.ajGetInfo'),
    url(r'^domain/info/$', 'resource.service.domain.index'),
)
