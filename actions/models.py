from django.db import models

from configurations.abstracts import AbstractModel


class Subscription(AbstractModel):
    user = models.ForeignKey(
        'basics.User',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    podcast = models.ForeignKey(
        'contents.Podcast',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    is_notification_enabled = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.user}'s subscription to {self.podcast}"

    class Meta:
        ordering = ('added_time', )
