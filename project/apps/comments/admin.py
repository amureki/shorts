from django.contrib import admin

from comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = [u'id', u'user', u'topic']
    list_display_links = [u'id', u'user', u'topic']
    search_fields = (u'id', u'user')


admin.site.register(Comment, CommentAdmin)
