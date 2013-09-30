import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/envirocon/envirocon/ve/lib/python2.6/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/')
sys.path.append('/var/www/envirocon/')
sys.path.append('/var/www/envirocon/envirocon/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'envirocon.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()