from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', 'blog.views.about', name='about'),
    url(r'^contact/$', 'blog.views.contact', name='contact'),
)
