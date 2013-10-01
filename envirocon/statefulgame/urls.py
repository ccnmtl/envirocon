from django.conf.urls.defaults import patterns, url
import os.path
from django.views.i18n import null_javascript_catalog
media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns(
    'envirocon.statefulgame.views',

    url(r'^save_assignment',
        'save_assignment',
        name='save-assignment'),

    url(r'^get_assignment/(?P<turn_id>\d+)/(?P<user_id>[^/]+)/$',
        'get_assignment_data',
        name='get-assignment'),

    # url(r'^get_assignment_csv/(?P<assignment_id>\d+[^/]+)/$',
    url(r'^get_assignment_csv/(?P<assignment_id>[^/]+)/$',
        'get_assignment_csv',
        name='get-assignment-csv'),

    url(r'^current',
        'current_turn',
        name='current-turn'),

    # note faculty_view is even more optional than page_id
    url(r'^assignment/(?P<assignment_id>\d+)(?P<faculty_view>/instructor/)'
        '?(?P<user_id>[^/]+)?/(?P<page_id>[^/]+)?$',
        'assignment_page',
        name='assignment-page'),

    url(r'^assignment/(?P<assignment_id>\d+)/video/$',
        'assignment_video',
        name='assignment-video'),

    url(r'^faculty_view/(?P<game_id>[^/]*)',
        'faculty_view',
        name='faculty-view'),
    url(r'^set_shock/?',  # for backwards compatibility
        'set_turn',
        name='set-shock'),
    url(r'^set_turn/?',  # same as above
        'set_turn',
        name='set-turn'),
    url(r'^split_team/?',  # admin only
        'split_team',
        name='split-team'),
    url(r'^jsi18n/$',
        null_javascript_catalog,
        name='jsi18n'),
)
