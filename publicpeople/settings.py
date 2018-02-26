"""
Django settings for publicpeople project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'true') == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = '-r&cjf5&l80y&(q_fiidd$-u7&o$=gv)s84=2^a2$o^&9aco0o'
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# XXX set me
GOOGLE_ANALYTICS_ID = "UA-114651981-1"

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'django_extensions',

    'popolo',
    'popolo_sources',

    'publicpeople',

    'rest_framework',
    'django_filters',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'publicpeople.urls'

WSGI_APPLICATION = 'publicpeople.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url
db_config = dj_database_url.config(default='postgres://publicpeople@localhost/publicpeople')
db_config['ATOMIC_REQUESTS'] = True
DATABASES = {
    'default': db_config,
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
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "publicpeople.context_processors.google_analytics",
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
        'django': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        }
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
