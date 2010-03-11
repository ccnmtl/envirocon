from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

import survey.urls
import djangowind.urls
#import tinymce.urls
import game.urls
import statefulgame.urls
import teams.urls

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       # Example:
                       # (r'^envirocon/', include('envirocon.foo.urls')),
                       (r'^logout$', 'django.contrib.auth.views.logout', {'next_page':'/accounts/login/?next=/'}),
                       ('^accounts/',include(djangowind.urls)),
                       (r'^admin/(.*)', admin.site.root),
		       (r'^survey/',include(survey.urls)),
#                       (r'^tinymce/', include(tinymce.urls)),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),

                       (r'^gamepages/',include(game.urls)),
                       (r'',include(statefulgame.urls)), #import at root
                       (r'^teams/',include(teams.urls)),

                       url(r'^new',
                           'envirocon_main.views.new_envirocon_class',
                           name='new-envirocon-class'
                           ),

                       (r'^about','envirocon_main.views.about'),
                       (r'^help','envirocon_main.views.help'),
                       (r'^contact','envirocon_main.views.contact'),

                       
                       (r'', 'envirocon_main.views.home'),
)
