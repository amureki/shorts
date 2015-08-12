from django.contrib import admin

from topics.models import Topic


class TopicAdmin(admin.ModelAdmin):
    list_display = [u'id', u'title', u'user']
    list_display_links = [u'id', u'title', u'user']
    search_fields = (u'id', u'title')


admin.site.register(Topic, TopicAdmin)
