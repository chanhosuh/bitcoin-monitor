"""
Django settings for bitcoin_monitor project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import os
import sys
from distutils.util import strtobool


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    os.environ.get('DJANGO_SECRET_KEY') or
    '*p9-m^%=h20t$0$xf#s^z4p0x1lu+(de!j@^1#ba$^4t*y$^a6'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.environ.get('DEBUG', "False"))

# debug mode should be off during tests
IS_TEST = len(sys.argv) > 1 and sys.argv[1] == 'test'
if IS_TEST:
    DEBUG = False

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]
ALLOWED_HOSTS += os.environ.get('ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'django_celery_beat',
    'django_extensions',
    'debug_toolbar',
    'rest_framework',

    # Our apps
    'bitcoin_monitor.apps.BitcoinMonitorConfig',
    'blocks.apps.BlocksConfig',
    'transactions.apps.TransactionsConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bitcoin_monitor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'bitcoin_monitor.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bitcoinmonitor',
        'USER': 'bitcoinmonitor',
        'PASSWORD': 'bitcoinmonitor',
        'HOST': os.environ.get('DB_HOSTNAME', 'db'),
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Logging setup
DEFAULT_LOGGING_FORMAT = '[%(levelname)s][%(name)s] %(asctime)s: %(message)s'
CELERY_LOGGING_FORMAT = '[%(levelname)s][%(process)s][%(name)s] %(asctime)s: %(message)s'

CONTAINER_NAME = os.environ.get('CONTAINER_NAME', '')
if CONTAINER_NAME == 'celery':
    LOGGING_FORMAT = CELERY_LOGGING_FORMAT
else:
    LOGGING_FORMAT = DEFAULT_LOGGING_FORMAT

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': LOGGING_FORMAT,
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': DEFAULT_LOGGING_FORMAT,
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },

    'loggers': {
        '': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server', ],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# --- Celery --- #
CELERY_BROKER_HOST = {
    'hostname': os.environ.get('CELERY_BROKER_HOSTNAME'),
    'port': 6379,
}
CELERY_BROKER_URL = 'redis://{}:{}/0'.format(
    CELERY_BROKER_HOST['hostname'],
    CELERY_BROKER_HOST['port'],
)

# can't use redis yet as backend due to Celery conflict
# with Python 3.7
# CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'

if IS_TEST:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True

# --- Redis --- #
REDIS_HOST = 'redis'
REDIS_PORT = 6379

# --- Debug Toolbar --- #
DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG}

# --- bitcoind RPC --- #
RPC_VERSION = '2.0'
RPC_HEADERS = {'content-type': 'application/json'}
RPC_ID = 'bitcoin-monitor'
RPC_URL = 'http://bitcoind:8332'

# --- Jupyter Notebook --- #
NOTEBOOK_ARGUMENTS = [
    '--ip',
    '0.0.0.0',
    '--allow-root',
    '--no-browser',
]

# --- Django REST Framework --- #
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
