"""
Django settings for this project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# The SECRET_KEY is provided via an environment variable in OpenShift
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    # safe value used for development when DJANGO_SECRET_KEY might not be set
    '9e4@&tw46$l31)zrqe3wi+-slqm(ruvz&se0^%9#6(_w3ui!c0'
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'debug_toolbar',
    'soc',
    'djangosaml2',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'crispy_forms'
    )


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
    )

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
      'BACKEND': 'django.template.backends.django.DjangoTemplates',
      'DIRS': [BASE_DIR + '/templates/'],
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

#WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

from . import database

try:
  #try and open DB password file mounted by openshift
  with open('/usr/src/app/myapp/local/oracle/password', 'rb') as f:
    DB_PASSWORD = f.read()
except:
  DB_PASSWORD = 'Pw6517nP'
  print 'error reading DB secret file'



DATABASES = {
    'oracle': {
      'ENGINE': 'django.db.backends.oracle',
      'NAME': 'pinntst.dsc.umich.edu:1521/pinndev.world',
      'USER': 'paulowar',
      'PASSWORD': 'Pw6517nP',
      'schemas': ['PINN_CUSTOM'],
      'options':{
        'user_returning_into': False,
        'options': '-c search_path=PINN_CUSTOM'
        },
      },
    'default':{
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
      }

    }
DATABASE_ROUTERS = ['soc.models.DBRouter']

# prints sql statements made to db
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#      'console': {
#        'class': 'logging.StreamHandler',
#        },
#      },
#    'loggers': {
#      'django.db.backends': {
#        'level': 'DEBUG',
#        'handlers': ['console'],
#        }
#      },
#    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SAML2_URL_PATH = '/accounts/'
SAML2_URL_BASE = 'https://django-example-paulo-test.openshift.dsc.umich.edu/accounts/'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
    )

LOGIN_URL = '%slogin/' % SAML2_URL_PATH
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

from os import path
import saml2
BASEDIR = path.dirname(path.abspath(__file__))

SAML_CONFIG = {
    'xmlsec_binary': '/usr/bin/xmlsec1',
    'entityid': '%smetadata/' % SAML2_URL_BASE,

    # directory with attribute mapping
    # 'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),
    'name': 'Student Explorer',
    # this block states what services we provide
    'service': {
      # we are just a lonely SP
      'sp': {
        'name': 'Summary Of Charges',
        'name_id_format': ('urn:oasis:names:tc:SAML:2.0:'
          'nameid-format:transient'),
        'authn_requests_signed': 'true',
        'allow_unsolicited': True,
        'endpoints': {
          # url and binding to the assetion consumer service view
          # do not change the binding or service name
          'assertion_consumer_service': [
            ('%sacs/' % SAML2_URL_BASE,
              saml2.BINDING_HTTP_POST),

            ],
          # url and binding to the single logout service view+

          # do not change the binding or service name
          'single_logout_service': [
            ('%sls/' % SAML2_URL_BASE,
              saml2.BINDING_HTTP_REDIRECT),
            ('%sls/post' % SAML2_URL_BASE,
              saml2.BINDING_HTTP_POST),

            ],

          },

        # attributes that this project need to identify a user
        'required_attributes': ['uid'],

        # attributes that may be useful to have but not required
        'optional_attributes': ['eduPersonAffiliation'],

        },

      },

    # where the remote metadata is stored
    'metadata': {
      'local': [path.join(BASEDIR, 'saml/remote-metadata.xml')],
      },

    'debug': 1,
    # certificate
    'key_file': path.join(BASEDIR, 'saml/student-explorer-saml.key'),
    'cert_file': path.join(BASEDIR, 'saml/student-explorer-saml.pem'),
    'encryption_keypairs': [{
      'key_file': path.join(BASEDIR, 'saml/student-explorer-saml.key'),
      'cert_file': path.join(BASEDIR, 'saml/student-explorer-saml.pem'),
      }]
    }

SAML_CREATE_UNKNOWN_USER = True

SAML_ATTRIBUTE_MAPPING = {
    'uid': ('username', ),
    'mail': ('email', ),
    'givenName': ('first_name', ),
    'sn': ('last_name', ),

    }

CRISPY_TEMPLATE_PACK = 'bootstrap4'
