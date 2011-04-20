from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'daily_edition.views.latest_edition'),
    url(r'^json/daily-edition\.json$',
        'daily_edition.views.latest_edition_json'),
    url(r'^json/issue-(?P<issue>\d+)\.json$',
        'daily_edition.views.edition_json'),
    url(r'^publish/$', 'daily_edition.views.publish_edition'),
)
