from core.settings.base import *

SECRET_KEY = 'django-insecure-#r3$d7vg+nxi2kqqrf9enxoast=2nlgs1^p#p&fakcno+)letb'
DEBUG = True
ALLOWED_HOSTS = []

# ## Email configuration
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='bizname1990@gmail.com'
EMAIL_HOST_PASSWORD='ommafmxfowobugft'
EMAIL_USE_TLS = True
# ## End
