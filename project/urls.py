from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    url(r'^recruitment/', include('recruitment.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Django Auth
    url(r'^login/$',  'django.contrib.auth.views.login',  {'template_name': 'auth/login.html'},  name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'auth/logout.html'}, name='logout'),

)
