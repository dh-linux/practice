from django.conf.urls import include, url
from django.conf.urls import include, url
from views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^index.html', index),
    url(r'^$', index),
    url(r'detail/(\d+)/$', blog_detail),
]
