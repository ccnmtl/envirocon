from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns(
    'teams.views',
    url(r'^admin$',
        'team_admin',
        name='team-admin'),

    url(r'^create/(?P<course_id>\w+)?/?$',
        'addteam',
        name='team-create'),
    url(r'^delete/(?P<team_id>\w+)/(?P<remove_group>remove_group)?$',
        'deleteteam',
        name='team-delete'),

    url(r'^member/(?P<user_id>\w+)/(?P<team_id>\w+)?(/(?P<course_id>\w+))?/?$',
        'addmember',
        name='team-addmember'),

    )

