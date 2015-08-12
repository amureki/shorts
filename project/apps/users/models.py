import re
from django.core import validators
from django.contrib.auth.models import UserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone


class PermissionsMixin(models.Model):
    is_superuser = models.BooleanField(
        u'superuser status', default=False,
        help_text=u'Designates that this user has all permissions without explicitly assigning them.')

    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        u'username', max_length=255, unique=True,
        help_text=u'Required. 30 characters or fewer. Letters, numbers and /./-/_ characters',
        validators=[
            validators.RegexValidator(re.compile('^[\w.-]+$'), u'Enter a valid username.', u'invalid')
        ])
    email = models.EmailField(u'email address', max_length=255, unique=True)
    is_active = models.BooleanField(
        u'active', default=False,
        help_text=u'Designates whether this user should be treated as '
                  u'active. Unselect this instead of deleting accounts.')

    date_joined = models.DateTimeField(u'date joined', default=timezone.now)

    USERNAME_FIELD = u'username'
    REQUIRED_FIELDS = [u'email']

    objects = UserManager()

    class Meta:
        verbose_name = u'User'
        verbose_name_plural = u'Users'
        ordering = [u'username']

    def __unicode__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username
