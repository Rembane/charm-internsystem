from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'recruitment.views.register', name='register'),
    url(r'^confirmation/$', 'recruitment.views.confirmation', name='confirmation'),
)

