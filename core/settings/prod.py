from core.settings.base import *
from decouple import config
import os

SECRET_KEY = 'dfdhfjhdjfkjk3834'
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

## Email configuration
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST=''
EMAIL_PORT=''
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_USE_TLS = True
## End
