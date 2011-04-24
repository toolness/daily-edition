from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'daily_edition.views.publish_edition'),
    url(r'^issue/latest/$', 'daily_edition.views.edition'),
    url(r'^issue/(?P<issue>\d+)/$', 'daily_edition.views.edition'),
    url(r'^issue/latest/data\.json$',
        'daily_edition.views.latest_edition_json'),
    url(r'^issue/(?P<issue>\d+)/data.json$',
        'daily_edition.views.edition_json'),
)
