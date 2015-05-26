from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('',
    url(r'^$', 'issue.views.index',name="issue"),
    url(r'^index/$', 'issue.views.index', name="issue_index"),
    url(r'^search/$', 'issue.views.search', name="issue_search"),
    url(r'^add/$', 'issue.views.add',name="issue_add"),
    #url(r'^be/$', 'issue.views.be', name="issue_be"),
    #url(r'^langshou/$', 'issue.views.langshou',name="issue_langshou"),
    #url(r'^langshou_api/$', 'issue.views.langshou_api',name="issue_langshou_api"),
    #url(r'^add/$', 'issue.views.add',name="issue_add"),
)
