from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', 'common.views.index',name="index"),
    url(r'^loginpage/$','common.views.loginpage',name="loginpage"),
    url(r'^account/', include('account.urls')),
    url(r'^common/', include('common.urls')),
    url(r'^role/', include('role.urls')),
    url(r'^authority/', include('authority.urls')),
    url(r'^log/', include('log.urls')),
    url(r'^area/',include('area.urls')),
    url(r'^issue/',include('issue.urls')),
)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
