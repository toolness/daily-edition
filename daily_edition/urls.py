from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'daily_edition.views.publish_edition',
        name='publish-edition'),
    url(r'^list/edit/', 'daily_edition.views.edit_list',
        name='edit-list'),
    url(r'^list/', 'daily_edition.views.view_list',
        name='view-list'),
    url(r'^issue/latest/$', 'daily_edition.views.edition',
        name='latest-edition'),
    url(r'^issue/(?P<issue>\d+)/$', 'daily_edition.views.edition',
        name='view-edition'),
)
