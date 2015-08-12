# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, View, CreateView

from users.forms import LoginForm, RegistrationForm
from utils.email import send_activation_email
from utils.tokens import UserActivationTokenGenerator

User = get_user_model()


class LoginView(FormView):
    template_name = u'users/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.redirect()
        return super(LoginView, self).get(request, *args, **kwargs)

    def redirect(self):
        if self.request.GET.get(u'next'):
            return HttpResponseRedirect(self.request.GET.get(u'next'))
        return HttpResponseRedirect(u'/')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return self.redirect()

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context[u'next'] = self.request.GET.get(u'next', None)
        return context


class LogOut(View):
    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
        return HttpResponseRedirect(u'/')


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = u'users/register.html'
    model = settings.AUTH_USER_MODEL

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(u'topics:list')

    def form_valid(self, form):
        user = form.save()
        send_activation_email(user)
        messages.info(self.request, u'We have sent you an email so you can activate your account!')
        return HttpResponseRedirect(self.get_success_url())


class ActivationView(View):
    def get_redirect_url(self):
        return reverse(u'users:login')

    def get(self, request, *args, **kwargs):
        pk = kwargs.get(u'pk')
        token = kwargs.get(u'token')

        user = get_object_or_404(User, pk=pk)
        activation = UserActivationTokenGenerator()

        if activation.is_valid(user, token):
            user.is_active = True
            user.save()
            messages.info(request, u'Please, sign in for complete your activation!')
        else:
            messages.error(request, u'There was something wrong, please contact support.')
        return HttpResponseRedirect(self.get_redirect_url())
