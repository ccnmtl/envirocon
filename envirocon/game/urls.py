import os.path
from django.conf.urls import patterns, url


media_root = os.path.join(os.path.dirname(__file__), "media")
rootdir = os.path.join(os.path.dirname(__file__), "../")

urlpatterns = patterns(
    '',

    url(r'^$',
        'envirocon.game.views.gamelist',
        name='game-list'),

    url(r'^game/(?P<gamename>\w+)/(?P<page_id>\w+)?$',
        'envirocon.game.views.gamepage',
        name='game-page'),
)
