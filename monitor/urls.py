from django.conf.urls import patterns, url, include

from django.contrib.auth.views import login, logout
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^monitor/$', 'monitor.views.monitor', name='monitor'),
    url(r'^monitor/(?P<slug>[-\w]+)/$', 'monitor.views.monitor', name='monitor_arg'),
    url(r'^help', 'monitor.views.help', name='help'),
    url(r'^contribute', 'monitor.views.contribute', name='contribute'),
    url(r'^status.json', 'monitor.views.status_json'),
    url(r'^module/new$', 'monitor.views.create_module', name='create_module'),
    url(r'^module/edit/(?P<slug>[-\w]+)/$', 'monitor.views.edit_module', name='edit_module'),
    url(r'^module/delete/(?P<slug>[-\w]+)/$', 'monitor.views.delete_module', name='delete_module'),
    url(r'^watcher/new$', 'monitor.views.create_watcher', name='create_watcher'),
    url(r'^watcher/edit/(?P<slug>[-\w]+)/$', 'monitor.views.edit_watcher', name='edit_watcher'),
    url(r'^watcher/delete/(?P<slug>[-\w]+)/$', 'monitor.views.delete_watcher', name='delete_watcher'),
    url('^accounts/login/$', login, name='login'),
    url('^accounts/logout/$', logout, {'next_page': '/monitor/'}, name='logout'),
    url(r'^accounts/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    (r'^user/password/reset/done/$',
     'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
     'django.contrib.auth.views.password_reset_confirm',
     {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$',
     'django.contrib.auth.views.password_reset_complete'),
)
