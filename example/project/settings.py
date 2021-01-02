"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's917$+d8re=1@0sg39l985abmhlen3mo(o7=xy4v86#ka2pdsa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*', ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend_forms',
    'django_select2',
    'query_inspector',
    'project',
    'backend',
    'samples',
    'others',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'query_inspector.middleware.QueryCountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public', 'static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public', 'media'))

#
# Npm configuration
#

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_FINDERS.append('npm.finders.NpmFinder')


X_FRAME_OPTIONS='SAMEORIGIN' # only if django version >= 3.0
FRONTEND_FORMS_FORM_LAYOUT_FLAVOR = 'bs4'


PROJECT_INSTANCE_PREFIX = "frontend_forms_example_"

#REDIS_URL = 'redis://localhost:6379/0'
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = 6379
REDIS_URL = 'redis://%s:%d/0' % (redis_host, redis_port)

CACHES = {
    # … default cache config and others
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # … default cache config and others
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://%s:%d/1' % (redis_host, redis_port),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Tell select2 which cache configuration to use;
# Best practices:
# 1) either usa a specific Redis db (for example: 1),
# 2) or use a Project's specific prefix
SELECT2_CACHE_BACKEND = "select2"
SELECT2_CACHE_PREFIX = PROJECT_INSTANCE_PREFIX + 'select2_'
SELECT2_JS = ''
SELECT2_CSS = ''

QUERYCOUNT = {
    'IGNORE_ALL_REQUESTS': False,
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG': 0,
        'MIN_QUERY_COUNT_TO_LOG': 0
    },
    'DISPLAY_ALL': True,
    'DISPLAY_PRETTIFIED': True,
    'COLOR_FORMATTER_STYLE': 'monokai',
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count',
    'DISPLAY_DUPLICATES': 0,
}

LOGIN_URL = reverse_lazy('frontend_forms:login')
LOGOUT_URL = reverse_lazy('frontend_forms:logout')
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')

# Load local settings when supplied
try:
    from project.local import *
    print('Local settings loaded !')
except ModuleNotFoundError as e:
    pass
