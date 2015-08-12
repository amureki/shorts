from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from utils.models import BaseModel


class Vote(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=u'votes')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(u'content_type', u'object_id')
    value = models.IntegerField()

    def __unicode__(self):
        return u'{} vote for {}'.format(self.value, self.content_object)
