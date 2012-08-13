# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Recruitment
    url(r'^$', 'recruitment.views.register', name=u'register'),
    url(r'^confirm_email_address/(?P<pk>\d+)/(?P<email_hash>\w+)/$', 'recruitment.views.confirm_email_address', name=u'confirm_email_address'),
    url(r'^mypage/$', 'recruitment.views.mypage', name=u'mypage'),
    url(r'^edit_my_profile/$', 'recruitment.views.edit_my_profile', name=u'edit_my_profile'),
    url(r'^apply_for_position/$', 'recruitment.views.apply_for_position', name=u'apply_for_position'),

    # Backoffice
    url(r'^backoffice/$', TemplateView.as_view(template_name=u'recruitment/backoffice.html'), name='backoffice'),
    url(r'^backoffice/list_applications/$', 'recruitment.views.list_applications', name='list_applications'),
    url(r'^backoffice/show_application/(?P<pk>\d+)/$', 'recruitment.views.show_application', name='show_application'),

    # Comments
    url(r'^comment/add/(?P<pk>\d+)/$', 'recruitment.views.add_application_comment', name='add_application_comment'),

    url(r'^set_language/(?P<code>[\w\-]+)$', 'recruitment.views.set_language', name='set_language')
)

