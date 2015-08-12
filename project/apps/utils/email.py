# -*- coding: utf-8 -*-
import logging
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from utils.tokens import UserActivationTokenGenerator

logger = logging.getLogger(u'django')


def generate_email(subject, context, recipient):
    template_name = u'email/message.html'
    body = render_to_string(template_name, context)
    email = EmailMessage(subject, body, settings.EMAIL_SENDER, [recipient, ])
    email.content_subtype = u'html'
    return email


def sender(subject, context, recipient):
    email = generate_email(subject, context, recipient)
    try:
        email.send()
    except SMTPException as e:
        logger.exception(e)


def send_activation_email(user):
    token = UserActivationTokenGenerator().generate(user)
    site = Site.objects.get_current()

    subject = u'Complete you registration on pyshorts'
    url = u'http://%s%s' % (site, reverse(u'users:activation', kwargs={u'pk': user.pk, u'token': token}))
    message = u'Greetings!<br/>You can confirm your registration by visiting next url:<br/>{}'.format(url)

    context = {
        u'text': message,
        u'title': subject,
        u'footer': u'with regards, pyshorts'
    }

    sender(subject, context, recipient=user.email)


def send_notification_email(subject, message, url, url_text=u'Check more', email=None):
    if not email:
        raise Exception(u'No email provided')

    context = {
        u'title': subject,
        u'text': message,
        u'footer': u'with regards, pyshorts'
    }

    sender(subject, context, recipient=email)
