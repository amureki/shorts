from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 3rd-party apps
urlpatterns += patterns(
    '',
    url(r'^u/social/', include(u'social.apps.django_app.urls', namespace=u'social'))
)

# Project apps
urlpatterns += patterns(
    '',
    url(r'^', include(u'topics.urls', namespace=u'topics')),
    url(r'^u/', include(u'users.urls', namespace=u'users')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^404/$', TemplateView.as_view(template_name='404.html'), name='404'),
        url(r'^500/$', TemplateView.as_view(template_name='500.html')),
    )

# Staticfiles
urlpatterns += staticfiles_urlpatterns()