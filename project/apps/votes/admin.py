from django.contrib import admin

from votes.models import Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = list_display_links = [u'id', u'user', u'content_object', u'value']


admin.site.register(Vote, VoteAdmin)
