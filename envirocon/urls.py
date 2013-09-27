from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

import survey.urls
import djangowind.urls


site_media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns('',
                       (r'^logout$',
                        'django.contrib.auth.views.logout',
                        {'next_page': '/accounts/login/?next=/'}),

                       ('^accounts/', include(djangowind.urls)),

                       (r'^admin/', include(admin.site.urls)),

                       (r'^survey/', include(survey.urls)),

                       (r'^site_media/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': site_media_root}),

                       (r'^uploads/(?P<path>.*)$',
                        'django.views.static.serve',
                        {'document_root': settings.MEDIA_ROOT}),

                       (r'^gamepages/', include('envirocon.game.urls')),
                       (r'', include('envirocon.statefulgame.urls')),
                       (r'^teams/', include('envirocon.teams.urls')),

                       url(r'^new',
                           'envirocon_main.views.new_envirocon_class',
                           name='new-envirocon-class'),

                       (r'^about', 'envirocon_main.views.about'),
                       (r'^help', 'envirocon_main.views.help'),
                       (r'^contact', 'envirocon_main.views.contact'),

                       (r'', 'envirocon_main.views.home'),
                       )
