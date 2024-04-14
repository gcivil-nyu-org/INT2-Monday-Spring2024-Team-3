"""
Django settings for nyu_event project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import ssl
from dotenv import load_dotenv
from os.path import join, dirname

load_dotenv(join(dirname(__file__), ".env"))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--1vz#!np5i3v)p_(cclo9t8a40^ufcl#!tdkfq$p@6-=)ck@gf"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = "APP_ENV" not in os.environ or os.environ["APP_ENV"] not in [
    "develop",
    "production",
]

# ALLOWED_HOSTS = ['*','nyu-event-dev.us-east-1.elasticbeanstalk.com']
ALLOWED_HOSTS = [
    "*",
    "127.0.0.1",
    "prod-env.eba-gqpxg4we.us-east-1.elasticbeanstalk.com",
    "dev-env.eba-gqpxg4we.us-east-1.elasticbeanstalk.com",
]


# Application definition

INSTALLED_APPS = [
    "backend.apps.BackendConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "nyu_event.urls"

AUTHENTICATION_BACKENDS = ["backend.backends.EmailBackend"]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nyu_event.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if "RDS_DB_NAME" in os.environ:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ["RDS_DB_NAME"],
            "USER": os.environ["RDS_USERNAME"],
            "PASSWORD": os.environ["RDS_PASSWORD"],
            "HOST": os.environ["RDS_HOSTNAME"],
            "PORT": os.environ["RDS_PORT"],
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "nyu_event",
            "USER": "postgres",
            "PASSWORD": "complexpassword123",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {  # 'root' logger
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
LOGIN_URL = "/user/login"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Emailing settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587  # SMTP port (usually 587 for TLS)
EMAIL_USE_TLS = True  # Using TLS for encryption
EMAIL_HOST_USER = "nyuevents24@gmail.com"
EMAIL_HOST_PASSWORD = "ogtoqvpmcniroelh"

DEFAULT_FROM_EMAIL = "nyuevents24@gmail.com"

PUSHER_APP_ID = "1773977"
PUSHER_KEY = "e44f77643020ff731b4f"
PUSHER_SECRET = "064da109d46ae1fd75ee"
PUSHER_CLUSTER = "mt1"
