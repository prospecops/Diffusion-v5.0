"""
Django settings for user_registration project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yl$g!r59pvv!@ca7sskca#!b62gytuh77j6g)dvtp^5d11gzrr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',  # added
    'allauth',  # added
    'allauth.account',  # added
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration',
    'core',
    'ctm_tracking',
    'supplier',
    'depots',
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

ROOT_URLCONF = 'user_registration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Here
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

WSGI_APPLICATION = 'user_registration.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Or for production use something like this:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'  # replace with your actual smtp server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# TODO: change to env variables
EMAIL_HOST_USER = 'diffusion.helpdesk@gmail.com'
EMAIL_HOST_PASSWORD = 'fjxyhsqklvlughzd'

# allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_UNIQUE_EMAIL = False
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400  # one day in seconds
SITE_ID = 1
LOGIN_REDIRECT_URL = '/core/'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_FORMS = {'signup': 'registration.forms.CustomSignupForm'}

# Logging configuration
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         # Add your app's logger here:
#         'registration': {  # Replace 'registration' with your app's name if different
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#     },
# }

# ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
# ACCOUNT_SESSION_REMEMBER = True
# ACCOUNT_LOGOUT_ON_GET = True
# ACCOUNT_LOGOUT_REDIRECT_URL = '/'
# ACCOUNT_SESSION_COOKIE_AGE = 86400  # one day in seconds
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
# ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Diffusion: '
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/accounts/login/'
# ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/home/'
# ACCOUNT_EMAIL_CONFIRMATION_URL = 'accounts/confirm-email/'
# ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
# ACCOUNT_EMAIL_CONFIRMATION_HMAC = True

# ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
# ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
# ACCOUNT_PASSWORD_RESET_TIMEOUT_DAYS = 1
# ACCOUNT_PASSWORD_RESET_CONFIRM = True
