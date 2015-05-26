from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('',
    url(r'^$', 'authority.views.index',name="authority"),
    url(r'^index/$', 'authority.views.index', name="authority_index"),
    url(r'^search/$', 'authority.views.search', name="authority_search"),
    url(r'^add/$', 'authority.views.add',name="authority_add"),
    url(r'^delete/(?P<authority_id>\d+)/$', 'authority.views.delete',name="authority_delete"),
    url(r'^edit/(?P<authority_id>\d+)/$', 'authority.views.edit',name="authority_edit"),
    
)