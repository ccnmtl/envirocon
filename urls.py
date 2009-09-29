from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
                       # Example:
                       # (r'^envirocon/', include('envirocon.foo.urls')),
                       ('^accounts/',include('djangowind.urls')),
                       (r'^admin/(.*)', admin.site.root),
		       (r'^survey/',include('survey.urls')),
                       (r'^tinymce/', include('tinymce.urls')),
                       (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
                       (r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),

                       (r'^gamepages/',include('game.urls')),
                       (r'',include('statefulgame.urls')), #import at root
                       (r'^teams/',include('teams.urls')),

                       (r'^about','envirocon_controller.views.about'),
                       (r'^help','envirocon_controller.views.help'),
                       (r'^contact','envirocon_controller.views.contact'),

                       
                       (r'', 'envirocon_controller.views.home'),
)
