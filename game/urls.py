from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")
rootdir = os.path.join(os.path.dirname(__file__),"../")

urlpatterns = patterns(
    '',
    #'game.views',
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),

    url(r'^$',
        'game.views.gamelist',
        name='game-list'),

    #url(r'^game//files/(?P<path>.*)$',
    #    'django.views.static.serve', {'document_root': rootdir+'conflict_assessment'+'/files', 'show_indexes':True}
    #    ),

    url(r'^game/(?P<gamename>\w+)/(?P<page_id>\w+)?$',
        'game.views.gamepage',
        name='game-page'),
        

    )

