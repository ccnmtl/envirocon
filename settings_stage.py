from settings_shared import *

ADMINS = (
    ('CCNMTL-Kodos', 'ccnmtl-sysadmin+staging@columbia.edu'),
)

DATABASE_ENGINE = 'postgresql_psycopg2'

TEMPLATE_DIRS = (
    "/usr/local/share/sandboxes/common/envirocon/envirocon/templates",
)

MEDIA_ROOT = '/usr/local/share/sandboxes/common/envirocon/uploads/'

DEBUG = False
TEMPLATE_DEBUG = DEBUG