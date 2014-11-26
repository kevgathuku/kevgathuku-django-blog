from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[-\w]+)/$', 'blog.views.show_post', name='post'),
)
