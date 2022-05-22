from .settings import *


DEBUG = True

ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static')),]
MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR.joinpath('media_root'))


#! EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'