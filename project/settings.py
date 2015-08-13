# -*- coding:utf-8 -*-
import sys
import os
from django.core.exceptions import ImproperlyConfigured

from configurations import Settings

from config.django.database import DevelopmentDatabaseSettings, StagingDatabaseSettings
from config.django.email import EmailSettings
from config.django.i18n import LocaleSettings
from config.django.media import DevelopmentMediaSettings, StagingMediaSettings, ProductionMediaSettings
from config.django.middleware import MiddlewareSetings
from config.django.logging import LoggingSettings
from config.django.template import DevelopmentTemplateSettings, StagingTemplateSettings, ProductionTemplateSettings

from config.apps.social_auth import SocialAuthSettings

try:
    from config.django.secrets import SecretSettings
except ImportError:
    raise ImproperlyConfigured(u'config.django.secrets is improperly configured.')


class BaseSettings(EmailSettings, LocaleSettings, LoggingSettings, MiddlewareSetings,
                   SocialAuthSettings,
                   SecretSettings,
                   Settings):
    PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

    ADMINS = MANAGERS = []

    ALLOWED_HOSTS = [u'shorts.amureki.me']

    SITE_ID = 1

    ROOT_URLCONF = 'project.urls'

    WSGI_APPLICATION = 'project.wsgi.application'

    INSTALLED_APPS = (
        'flat',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',

        'gunicorn',
        'raven.contrib.django.raven_compat',
        'django',

        'compressor',
        'social.apps.django_app.default',

        'comments',
        'topics',
        'users',
        'votes',
    )

    AUTH_USER_MODEL = u'users.User'
    LOGIN_URL = u'/u/login/'
    LOGIN_REDIRECT_URL = u'/'
    LOGOUT_URL = u'/u/logout/'


class Development(DevelopmentDatabaseSettings, DevelopmentMediaSettings, DevelopmentTemplateSettings,
                  BaseSettings):
    DEBUG = TEMPLATE_DEBUG = True


class Staging(StagingDatabaseSettings, StagingMediaSettings, StagingTemplateSettings,
              BaseSettings):
    RAVEN_CONFIG = {
        u'dsn': u'http://068ddbee5ba3477095f2b76fc2ffb1bd:ff054123cf114895af6c7e69b163415a@sentry-07.redeploy.ru/68',
    }
