from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'daily_edition.views.publish_edition'),
    url(r'^issue/latest/$', 'daily_edition.views.edition',
        name='latest-edition'),
    url(r'^issue/(?P<issue>\d+)/$', 'daily_edition.views.edition'),
)
