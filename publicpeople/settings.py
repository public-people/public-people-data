"""
Django settings for publicpeople project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import environ
env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', False)

DJANGO_DEBUG_TOOLBAR = env.bool('DJANGO_DEBUG_TOOLBAR', False) and DEBUG
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": 'publicpeople.settings.show_toolbar'
}


def show_toolbar(request):
    print("Checking whether to show toolbar: %r" % DJANGO_DEBUG_TOOLBAR)
    return DJANGO_DEBUG_TOOLBAR


# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = '-r&cjf5&l80y&(q_fiidd$-u7&o$=gv)s84=2^a2$o^&9aco0o'
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')


GOOGLE_TAG_MGR_ID = "GTM-W5PTM6R"

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'django_extensions',

    'ajax_select',
    'popolo',
    'simple_history',
    'popolo_sources',

    'publicpeople',

    'corsheaders',
    'rest_framework',
    'django_filters',
    'graphene_django',
]
if DJANGO_DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE = []

if DJANGO_DEBUG_TOOLBAR:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

MIDDLEWARE += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'publicpeople.urls'

WSGI_APPLICATION = 'publicpeople.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
)

db_config = dj_database_url.config(default='postgres://publicpeople@localhost/publicpeople')
db_config['ATOMIC_REQUESTS'] = True
DATABASES = {
    'default': db_config,
}

# Caches
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
        }
    }




# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                'django.template.context_processors.request',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "publicpeople.context_processors.google_tag_manager",
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

ASSETS_DEBUG = DEBUG
ASSETS_URL_EXPIRE = False

# assets must be placed in the 'static' dir of your Django app

# where the compiled assets go
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# the URL for assets
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
)

PYSCSS_LOAD_PATHS = [
    os.path.join(BASE_DIR, 'publicpeople', 'static'),
    os.path.join(BASE_DIR, 'publicpeople', 'static', 'bower_components'),
]

PIPELINE = {
    'STYLESHEETS': {
        'css': {
            'source_filenames': (
                'bower_components/fontawesome/css/font-awesome.css',
                'stylesheets/app.scss',
            ),
            'output_filename': 'app.css',
        },
    },
    'JAVASCRIPT': {
        'js': {
            'source_filenames': (
                'bower_components/jquery/dist/jquery.min.js',
                'bower_components/bootstrap-sass/assets/javascripts/bootstrap.min.js',
                'javascript/app.js',
            ),
            'output_filename': 'app.js',
        },
    },
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
    'COMPILERS': (
        'publicpeople.pipeline.PyScssCompiler',
    ),
}

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'publicpeople.pipeline.GzipManifestPipelineStorage'


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR'
    },
    'loggers': {
        # put any custom loggers here
        # 'your_package_name': {
        #    'level': 'DEBUG' if DEBUG else 'INFO',
        # },
        'django.template': {
            'level': 'ERROR',
        },
        'django': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        "urllib3": {
            "level": "DEBUG",
        },
    }
}


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}


GRAPHENE = {
    'SCHEMA': 'publicpeople.schema.schema'
}


import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN = env.str("SENTRY_DSN", None)

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
    )
