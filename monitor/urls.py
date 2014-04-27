from django.conf.urls import patterns, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^contribute$', 'docs.views.contribute',
                           name='contribute'),
                       url(r'^upload/', 'docs.views.upload',
                           name='upload_document'),
                       url(r'^browse/([a-zA-Z0-9-/_.]*)$', 'docs.views.browse',
                           name='browse'),
                       )