from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns(
    'statefulgame.views',

    url(r'^save_assignment',
        'save_assignment',
        name='save-assignment'),

    url(r'^get_assignment',
        'get_assignment_data',
        name='get-assignment'),

    url(r'^current',
        'current_turn',
        name='current-turn'),

    url(r'^assignment/(?P<assignment_id>.*)/?$',
        'assignment_page',
        name='assignment-page'),

    )
