# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm, UserCreationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data[u'username']
        is_taken = User._default_manager.filter(username=username).exists()
        if is_taken:
            raise forms.ValidationError(u'Username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data[u'email']
        is_taken = User.objects.filter(email__iexact=email).exists()
        if is_taken:
            raise forms.ValidationError(u'Email is already taken.')
        return email

    class Meta:
        model = User
        fields = (u'username', u'email')


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=u'Password',
        help_text=(u'Raw passwords are not stored, so there is no way to see '
                   u'this user\'s password, but you can change the password '
                   u'using <a href="password/">this form</a>.')
    )

    class Meta:
        model = User
        exclude = (u'password',)
