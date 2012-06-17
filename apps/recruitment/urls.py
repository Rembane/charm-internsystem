from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'recruitment.views.register', name='register'),
    url(r'^confirmation/$', 'recruitment.views.confirmation', name='confirmation'),

    url(r'^set_language/(?P<code>[\w\-]+)$', 'recruitment.views.set_language', name='set_language')
)

