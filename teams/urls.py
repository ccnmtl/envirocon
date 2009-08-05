from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns(
    'teams.views',
    url(r'^admin$',
        'team_admin',
        name='team-admin'),

    #url(r'^game/(?P<gamename>\w+)/(?P<page_id>\w+)?/?$',
    #    'gamepage',
    #    name='game-page'),

    )

