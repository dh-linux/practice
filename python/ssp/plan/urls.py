from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'plan.views.index'),
    url(r'^list/(?P<style>.*)/$', 'plan.views.list'),
    url(r'^list/$', 'plan.views.route'),
    url(r'^result/(?P<rsst>.*)/$', 'plan.views.result'),
    url(r'^task/api/$', 'plan.views.taskapi'),
    url(r'^task/$', 'plan.views.task'),
)
