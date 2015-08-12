import os


class BaseMediaSettings(object):
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'

    @property
    def STATICFILES_DIRS(self):
        return (
            os.path.join(self.PROJECT_ROOT, 'staticfiles'),
        )

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    )


class DevelopmentMediaSettings(BaseMediaSettings):
    @property
    def BASE_DIR(self):
        return self.PROJECT_ROOT

    @property
    def MEDIA_ROOT(self):
        return os.path.join(self.PROJECT_ROOT, 'media')

    @property
    def STATIC_ROOT(self):
        return os.path.join(self.PROJECT_ROOT, 'static')


class StagingMediaSettings(BaseMediaSettings):
    @property
    def MEDIA_ROOT(self):
        return u'/app/media'

    @property
    def STATIC_ROOT(self):
        return u'/app/static'


class ProductionMediaSettings(BaseMediaSettings):
    @property
    def MEDIA_ROOT(self):
        return u'/app/media'

    @property
    def STATIC_ROOT(self):
        return u'/app/static'
