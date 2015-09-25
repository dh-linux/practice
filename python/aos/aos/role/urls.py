from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('',
    url(r'^$', 'role.views.index',name="role"),
    url(r'^index/$', 'role.views.index', name="role_index"),
    url(r'^add/$', 'role.views.add',name="role_add"),
    url(r'^delete/(?P<role_id>\d+)/$', 'role.views.delete',name="role_delete"),
    url(r'^edit/(?P<role_id>\d+)/$', 'role.views.edit',name="role_edit"),
    
)