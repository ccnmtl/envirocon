from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns(
    'statefulgame.views',

    url(r'^save_assignment',
        'save_assignment',
        name='save-assignment'),

    )
