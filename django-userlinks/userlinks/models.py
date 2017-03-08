from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class UserLink(models.Model):

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    # verb where "user VERB content_object", e.g. thayer likes Chocolate
    LIKES = 'likes',
    BOOKMARKED = 'saved'
    BEEN_TO='been_to'

    link_type = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        choices = (
            (LIKES, 'Likes'),
            (BOOKMARKED, 'Bookmarked'),
            (BEEN_TO, 'Visited'),
        )
    )
    updated_on = models.DateTimeField(
        auto_now_add=True,
    )

    # generic parts
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True,
    )
    object_id = models.PositiveIntegerField(
        blank=True, null=True,
    )
    content_object = GenericForeignKey(
        'content_type', 'object_id',
    )
                                       

class UserRatingMixin(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    rating = models.IntegerField(blank=True, null=True)
    updated_on = models.DateTimeField(
        auto_now_add=True,
    )
    class Meta:
        abstract = True
