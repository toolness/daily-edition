from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'daily_edition.views.publish_edition'),
)
