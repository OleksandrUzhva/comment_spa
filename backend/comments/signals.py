from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Comment
from .serializers import CommentSerializer


@receiver(post_save, sender=Comment)
def announce_comment(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        data = CommentSerializer(instance).data
        async_to_sync(channel_layer.group_send)(
            "comments",
            {"type": "comment.created", "data": data},
        )