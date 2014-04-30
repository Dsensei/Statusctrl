from django.conf.urls import patterns, url

from django.contrib.auth.views import login, logout
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                        url(r'^introduction', 'monitor.views.introduction',
                            name='introduction'),
                        url(r'^monitor/$', 'monitor.views.monitor',
                            name='monitor'),
                        url(r'^monitor/(?P<module>\w+)/$', 'monitor.views.monitor',
                            name='monitor_arg'),
                        url(r'^help', 'monitor.views.help',
                            name='help'),
                        url(r'^contribute', 'monitor.views.contribute',
                            name='contribute'),
                        url(r'^status.json', 'monitor.views.status_json',
                            name='status_json'),
                        (r'^accounts/login/$',  login),
                        (r'^accounts/logout/$', logout),
                        )
