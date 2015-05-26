from django.conf.urls import include, url
from django.contrib import admin
from mysite.views import *
import blog

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search_form/', search_form),
    url(r'^search/$', search),
    url(r'^ua/', ua),
    url(r'',include('blog.urls')),
]
