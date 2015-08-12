# -*- coding:utf-8 -*-
import sys
import os
from django.core.exceptions import ImproperlyConfigured

from configurations import Settings

from config.django.database import DevelopmentDatabaseSettings, StagingDatabaseSettings, ProductionDatabaseSettings
from config.django.email import EmailSettings
from config.django.i18n import LocaleSettings
from config.django.media import DevelopmentMediaSettings, StagingMediaSettings, ProductionMediaSettings
from config.django.middleware import MiddlewareSetings
from config.django.logging import LoggingSettings
from config.django.template import DevelopmentTemplateSettings, StagingTemplateSettings, ProductionTemplateSettings

try:
    from config.django.secrets import SecretSettings
except ImportError:
    raise ImproperlyConfigured(u'config.django.secrets is improperly configured.')


class BaseSettings(EmailSettings, LocaleSettings, LoggingSettings, MiddlewareSetings,
                   SecretSettings,
                   Settings):
    PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

    ADMINS = MANAGERS = []

    ALLOWED_HOSTS = []

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
    pass


class Production(ProductionDatabaseSettings, ProductionMediaSettings, ProductionTemplateSettings,
                 BaseSettings):
    pass
