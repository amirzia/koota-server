"""
Django settings for koota_prj project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys
sys.path.append('/srv/koota/pymod/') # for custom classes

# Local settings
MAIN_DOMAIN = 'koota.cs.aalto.fi'
POST_DOMAIN = 'data.koota.cs.aalto.fi'
POST_DOMAIN_SS = 'ss1.koota.cs.aalto.fi'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KOOTA_SSL_CERT_DER = os.path.join(BASE_DIR, 'static', 'ss1.koota.cs.aalto.fi.crt.der')
KOOTA_SSL_CERT_PEM = os.path.join(BASE_DIR, 'static', 'ss1.koota.cs.aalto.fi.pem')
import hashlib
KOOTA_SSL_CERT_DER_SHA256 = hashlib.sha256(open(KOOTA_SSL_CERT_DER,'rb').read()).hexdigest()
KOOTA_SSL_CERT_PEM_SHA256 = hashlib.sha256(open(KOOTA_SSL_CERT_PEM,'rb').read()).hexdigest()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'tk%jm^r%t+bssa1w3$(64g9a$3z*s2)!z1pg_vzp^u)ptf=g3e'
try:
    # dd if=/dev/random of=koota_prj/secret_key.txt bs=1 count=128
    SECRET_KEY = open(os.path.join(os.path.dirname(__file__), 'secret_key.txt'),'rb').read()
except IOError:
    import random, string
    SECRET_KEY = ''.join(random.choice(string.printable) for _ in range(30))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
import __main__
if hasattr(__main__, '__file__') and __main__.__file__.endswith('manage.py'):
    DEBUG = True
else:
    # production
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
#SECURE_SSL_REDIRECT = True # But server should do this before it gets here.
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
LOGIN_URL = 'login2'
LOGIN_REDIRECT_URL = 'device-list'


#### The following settings should go into settings_local.py, NOT here.
# Make a random salt using this and paste it here.  By default we have
# an epheremal random salt.
# bytes(bytearray((random.randint(0, 255) for _ in range(32))))
SALT = None
#TWITTER_KEY = ''    # Consumer Key (API Key)
#TWITTER_SECRET = '' # Consumer Secret (API Secret)
#FACEBOOK_KEY = ''
#FACEBOOK_SECRET = ''
FACEBOOK_PERMISSIONS = ['user_friends']


ALLOWED_HOSTS = [
    # aalto hosts
    'data.koota.cs.aalto.fi',
    'koota.cs.aalto.fi',
    'nossl.koota.cs.aalto.fi',
    'ss1.koota.cs.aalto.fi',
    'dev.koota.zgib.net',
    'aware.koota.zgib.net',
    # Raw hostname
    'koota.cs.hut.fi',
    # Legacy hostnames
    'data.koota.zgib.net',
    'koota.zgib.net',
    'nossl.koota.zgib.net',
    'ss1.koota.zgib.net',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kdata',

    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'floppyforms',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'kdata.middleware.KdataMiddleware',
]

ROOT_URLCONF = 'koota_prj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'koota_prj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Needs LD_LIBRARY_PATH=/opt/pgsql/lib/amd64/
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'koota',
        'USER': 'koota',
    },
    'data': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data.sqlite3'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'koota_prj', 'static')]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter':'console',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log.txt'),
            'formatter':'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'] if DEBUG else ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
        '': {
            'handlers': ['console'] if DEBUG else ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'console': {
            'format': '[%(levelname)s] %(name)s: %(message)s'
        },
    },
}

try:
    from .settings_local import *
except ImportError:
    pass
