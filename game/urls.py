from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns(
    'game.views',
    url(r'^$',
        'gamelist',
        name='game-list'),

    url(r'^game/(?P<gamename>\w+)/(?P<page_id>\w+)?/?$',
        'gamepage',
        name='game-page'),

    )

