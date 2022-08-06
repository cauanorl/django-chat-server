from django.db import models

from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from authentication.models import Friend


# Create your models here.
class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    # Mesagens
    friend_model = models.ForeignKey(
        Friend,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        null=True,
        blank=True,
    )

    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='target_obj',
    )
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')


class MessageTextType(models.Model):
    content = models.TextField()


# class MessageImageType(MessageContentBase, models.Model):
#     content = models.ImageField(upload_to="media/%Y/%m/%d/")