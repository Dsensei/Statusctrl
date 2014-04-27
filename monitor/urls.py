from django.conf.urls import patterns, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^introduction$', 'monitor.views.introduction',
                           name='introduction'),
                       url(r'^now$', 'monitor.views.monitor',
                           name='monitor'),
                       url(r'^help$', 'monitor.views.help',
                           name='help'),
                       url(r'^contribute$', 'monitor.views.contribute',
                           name='contribute'),
                       )