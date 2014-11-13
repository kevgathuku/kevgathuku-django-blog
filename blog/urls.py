from django.conf.urls import patterns, url

from blog.views import ShowPost

urlpatterns = patterns('',
	
    url(r'^(?P<slug>[-\w]+)/$', ShowPost.as_view(), name='post'),
)
