import os, sys, site

# enable the virtualenv
site.addsitedir('/usr/local/share/sandboxes/common/envirocon/envirocon/ve/lib/python2.5/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/usr/local/share/sandboxes/common/')
sys.path.append('/usr/local/share/sandboxes/common/envirocon/')
sys.path.append('/usr/local/share/sandboxes/common/envirocon/envirocon/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'envirocon.settings_stage'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()