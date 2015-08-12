from django.conf.urls import patterns, url, include

from users.views import LoginView, LogOut, RegistrationView, ActivationView

urlpatterns = patterns(
    u'users.views',

    url(r'^login/$', LoginView.as_view(), name=u'login'),
    url(r'^logout/$', LogOut.as_view(), name=u'logout'),
    url(r'^register/$', RegistrationView.as_view(), name=u'register'),
    url(r'^register/confirm/(?P<pk>\d+)/(?P<token>[0-9A-Za-z_\-\.]+)/$', ActivationView.as_view(), name=u'activation'),
    url('', include(u'django.contrib.auth.urls')),

)
