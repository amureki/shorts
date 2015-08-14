from django.conf.urls import patterns, url, include

from users.views import LoginView, LogOut, RegistrationView, ActivationView, AcquireEmailView

urlpatterns = patterns(
    u'users.views',

    url(r'^login/$', LoginView.as_view(), name=u'login'),
    url(r'^logout/$', LogOut.as_view(), name=u'logout'),
    url(r'^register/$', RegistrationView.as_view(), name=u'register'),
    url(r'^acquire_email/(?P<user_id>\d+)/$', AcquireEmailView.as_view(), name=u'acquire_email'),
    url(r'^register/confirm/(?P<pk>\d+)/(?P<token>[0-9A-Za-z_\-\.]+)/$', ActivationView.as_view(), name=u'activation'),
    url('', include(u'django.contrib.auth.urls')),

)
