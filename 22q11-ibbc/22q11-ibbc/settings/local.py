"""Development settings and globals."""

from __future__ import absolute_import

from os.path import join, normpath

from .base import *

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = ''
########## END SECRET CONFIGURATION

########## END SECRET_KEY CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########### EMAIL CONFIGURATION
## See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########### END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE':'',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########### CACHE CONFIGURATION
## See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#    }
#}
########### END CACHE CONFIGURATION