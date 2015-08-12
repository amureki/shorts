from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

from project.apps.utils.models import BaseModel
from votes.models import Vote


class Topic(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u'topics')
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    rating = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(u'topics:detail', args=(self.id,))

    def vote(self, user, value):
        content_type = ContentType.objects.get_for_model(Topic)
        try:
            Vote.objects.get(user=user, content_type=content_type, object_id=self.id)
            return
        except Vote.DoesNotExist:
            Vote.objects.create(user=user, value=value, content_type=content_type, object_id=self.id)
        self.rating += value
        self.save()
