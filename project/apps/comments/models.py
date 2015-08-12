from django.conf import settings
from django.db import models

from project.apps.utils.models import BaseModel


class Comment(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u'comments')
    topic = models.ForeignKey(u'topics.Topic', related_name=u'comments')
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __unicode__(self):
        return u'{}\'s comment at {}'.format(self.user, self.topic)
