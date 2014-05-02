from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'monitor.views.monitor', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('monitor.urls')),
)
