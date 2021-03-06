"""
Django settings for alpakanews project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import configparser
import os
from pathlib import Path

config = configparser.RawConfigParser()
config.read_file(open('env.cfg', encoding='utf-8'))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5atbjzr#+l+2sytx()jhc!paw$$16%+z^ez^gk_i9jw9kf!!r6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'accounts',
    'tweet_overview'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alpakanews.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            "alpakanews/templates/"
        ],
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

WSGI_APPLICATION = 'alpakanews.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# User model
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKEND = [
    'accounts.EmailAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


TWITTER_CONSUMER_KEY = config.get("twitter", 'consumer_key')
TWITTER_CONSUMER_SECRET = config.get("twitter", 'consumer_secret')
TWITTER_ACCESS_TOKEN = config.get("twitter", 'access_token')
TWITTER_ACCESS_TOKEN_SECRET = config.get("twitter", 'access_token_secret')

CATEGORY_CHOICES = [
    ('politik', 'Politik'),
    ('wirtschaft', 'Wirtschaft'),
    ('wissenschaft', 'Wissenschaft'),
    ('kultur', 'Kultur'),
    ('beauty', 'Beauty'),
    ('sport', 'Sport'),
    ('sonstiges', 'Sonstiges')
]
VERIFIED_SOURCES = [
    'https://www.ard.de',
    'https://www.zdf.de',
    'https://www1.wdr.de',
    'https://www.rki.de',
    'https://de.wikipedia.org',
    'https://www.bmbf.de',
    'https://www.bbc.com',
    'https://www.nytimes.com',
    'https://www.zeit.de',
    'https://www.spiegel.de',
    'https://www.sueddeutsche.de',
    'https://www.tagesschau.de'
]

LOGOUT_REDIRECT_URL = "/"
