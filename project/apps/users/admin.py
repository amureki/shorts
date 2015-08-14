from django.contrib import admin

from users.forms import UserChangeForm
from users.models import User


class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    list_display = [u'id', u'email', u'username', u'is_active', u'is_superuser', u'date_joined']
    list_display_links = [u'id', u'email']
    list_filter = (u'is_active', u'is_superuser')
    search_fields = (u'id', u'email')


admin.site.register(User, UserAdmin)
