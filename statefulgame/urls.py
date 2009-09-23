from django.conf.urls.defaults import *
import os.path
from django.views.i18n import null_javascript_catalog
media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns(
    'statefulgame.views',

    url(r'^save_assignment',
        'save_assignment',
        name='save-assignment'),

    url(r'^get_assignment/(?P<turn_id>\d+)/(?P<user_id>[^/]+)/$',
        'get_assignment_data',
        name='get-assignment'),

    url(r'^current',
        'current_turn',
        name='current-turn'),

    #note faculty_view is even more optional than page_id
    url(r'^assignment/(?P<assignment_id>\d+)(?P<faculty_view>/instructor/)?(?P<user_id>[^/]+)?/(?P<page_id>[^/]+)?$',
        'assignment_page',
        name='assignment-page'),

    url(r'^faculty_view/(?P<game_id>[^/]*)',
        'faculty_view',
        name='faculty-view'),
    url(r'^set_shock/?',
        'set_shock',
        name='set-shock'),
    url(r'^jsi18n/$',
        null_javascript_catalog,
        name='jsi18n'),


)

