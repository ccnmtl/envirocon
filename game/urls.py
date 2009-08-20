from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns(
    'game.views',
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),

    url(r'^$',
        'gamelist',
        name='game-list'),

    url(r'^game/(?P<gamename>\w+)/(?P<page_id>\w+)?/?$',
        'gamepage',
        name='game-page'),

    )

