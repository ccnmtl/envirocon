from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns(
    'statefulgame.views',

    url(r'^save_assignment',
        'save_assignment',
        name='save-assignment'),

    url(r'^get_assignment/(?P<turn_id>\d+)/?$',
        'get_assignment_data',
        name='get-assignment'),

    url(r'^current',
        'current_turn',
        name='current-turn'),

    url(r'^files',
        'get_files',
        name='get-files'),

    url(r'^assignment/(?P<assignment_id>[^/]+)/(?P<page_id>[^/]+)?$',
        'assignment_page',
        name='assignment-page'),

    url(r'^faculty_view/(?P<game_id>[^/]*)',
        'faculty_view',
        name='faculty-view'),

    )
