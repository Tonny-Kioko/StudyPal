"""
Django settings for studypal project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from turtle import update
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

from aws_xray_sdk.ext.django.middleware import XRayMiddleware


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b38e7kl19rvvn@3*lq!betj$@mf*=oczorl5b+w7ci(vp&#fx4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*' ]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mpesa",
    "storages",
    "base.apps.BaseConfig",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.linkedin",
    "allauth.socialaccount.providers.twitter",
    "django_prometheus",
    "aws_xray_sdk.ext.django",
    "debug_toolbar",
]

# SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED ,
# SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED,
SOCIALACCOUNT_STORE_TOKENS=False, 

# Social Account Providers settings for signup options
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    },
     'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }, 
    'twitter':{
        'SCOPE': [
            'profile', 
            'email', 
        ], 
        'AUTH_PARAMS':{
            'access_type':'online',
        }
    }
}


MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "aws_xray_sdk.ext.django.middleware.XRayMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = 'studypal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':(BASE_DIR, 'templates'),
            
        
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

AUTHENTICATION_BACKENDS = (
    #'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# The account confirmation will require a new request after three days
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3, 

# This option allows you to set whether the email address should be verified to register
ACCOUNT_EMAIL_REQUIRED = True,

# email verification is necessary for a user to log in
ACCOUNT_EMAIL_VERIFICATION = "mandatory",

# Login Attempt Limit:
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5,

# Login Attempt Limit timeout:
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 3600, #Two Hours before retrying.

ACCOUNT_FORMS = {
    'signup': 'StudyPal.forms.MyUserCreationForm'
}


WSGI_APPLICATION = 'studypal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'studypaldb',
#         'USER': 'postgres',
#         'PASSWORD': 'c3po',
#         'HOST': 'pgdb',
#         'PORT': '5432',
#     }
# }

# import dj_database_url
# db_from_practice = dj_database_url.config(conn_max_age=600)
# DATABASES['default'], update()

# DATABASES = {
# 'default': {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'studypal',
#     'HOST': '127.0.0.1',
#     'PORT': '3306',
#     'USER': 'root',
#     'PASSWORD': '',
# }}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'studypaldb',
        'USER': 'postgres',
        'PASSWORD': 'c3po',
        'HOST': 'pgdb',
        'PORT': '5432',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            "redis://127.0.0.1:26379/0",
            "redis://127.0.0.1:26380/0",
            "redis://127.0.0.1:26381/0",
        ],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.SentinelClient",
            "SENTINEL_KWARGS": {
                "socket_timeout": 0.1,
            },
            "KEY_PREFIX": "studypal",
            "VERSION": 1,
        },
    }
}
CACHE_KEY_PREFIX = "studypal_"
CACHE_TTL = 60 * 10
# Optional: This is to ensure Django sessions are stored in Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'base.User'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
MEDIA_URL = '/images/'


STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
MEDIA_ROOT = BASE_DIR/ 'static/images'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # #S3 BUCKETS CONFIG
# AWS_ACCESS_KEY_ID = ''
# AWS_SECRET_ACCESS_KEY = ''
# AWS_STORAGE_BUCKET_NAME = 'studypaltonny'

# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# [
#     {
#         "AllowedHeaders": [
#             "*"
#         ],
#         "AllowedMethods": [
#             "HEAD",
#             "GET",
#             "PUT",
#             "POST",
#             "DELETE"
#         ],
#         "AllowedOrigins": [
#             "https://www.studypal.com"
#         ],
#         "ExposeHeaders": [
#              "ETag",
#              "x-amz-meta-custom-header"]
#     }
# ]

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Set the default storage backend to S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

XRAY_RECORDER = {
    'AWS_XRAY_TRACING_NAME': 'StudyPal Application', 
    'PLUGINS': ('EC2Plugin', 'ECSPlugin'),
    'SAMPLING': False,
    'AWS_XRAY_DAEMON_ADDRESS': 'xray-daemon:2000', 
    'AWS_XRAY_CONTEXT_MISSING': 'LOG_ERROR',
}

xray_recorder.configure(service='StudyPal Application')
plugins = ('EC2Plugin', 'ECSPlugin')
xray_recorder.configure(plugins=plugins)
patch_all()

INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.cache.CachePanel",

]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    # 'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            #'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            #'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
