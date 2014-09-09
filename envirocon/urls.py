import os.path

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
import djangowind.urls
import survey.urls


admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = patterns(
    '',
    (r'^logout$',
     'django.contrib.auth.views.logout',
     {'next_page': '/accounts/login/?next=/'}),

    ('^accounts/', include(djangowind.urls)),

    (r'^admin/', include(admin.site.urls)),

    (r'^survey/', include(survey.urls)),

    (r'^smoketest/', include('smoketest.urls')),

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
        'envirocon.envirocon_main.views.new_envirocon_class',
        name='new-envirocon-class'),

    (r'^about', 'envirocon.envirocon_main.views.about'),
    (r'^help', 'envirocon.envirocon_main.views.help'),
    (r'^contact', 'envirocon.envirocon_main.views.contact'),

    (r'', 'envirocon.envirocon_main.views.home'),
)
