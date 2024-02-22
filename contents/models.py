from django.db import models

from configurations.abstracts import AbstractModel
from configurations.utils import get_channel_image_path, get_podcast_image_path, get_collection_image_path


class Channel(AbstractModel):
    name = models.CharField(
        max_length=127,
    )
    image = models.ImageField(
        upload_to=get_channel_image_path,
    )
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('added_time', )


class Podcast(AbstractModel):
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='podcasts',
    )
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to=get_podcast_image_path,
    )
    categories = models.ManyToManyField(
        'classifiers.Category',
        related_name='podcasts',
    )
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.name} ({self.channel})"

    class Meta:
        ordering = ('added_time', )


class Episode(AbstractModel):
    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name='episodes',
    )
    name = models.CharField(
        max_length=255,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    timelapse = models.TextField(
        null=True,
        blank=True,
    )
    url = models.URLField(
        null=True,
        blank=True,
        help_text="URL to the audio file",
    )
    file_id = models.CharField(
        max_length=511,
        null=True,
        blank=True,
        help_text="(Telegram) File ID of the audio"
    )
    duration = models.PositiveIntegerField(
        help_text="Duration of the podcast in seconds",
    )
    total_listens_count = models.PositiveIntegerField(
        default=0,
    )
    total_likes_count = models.PositiveIntegerField(
        default=0,
    )
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.name} [{self.podcast}]"

    class Meta:
        ordering = ('added_time', )


class Collection(AbstractModel):
    sequence = models.PositiveIntegerField()
    name = models.CharField(
        max_length=127,
    )
    image = models.ImageField(
        upload_to=get_collection_image_path,
    )
    podcasts = models.ManyToManyField(
        Podcast,
        related_name='collections',
    )
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sequence', )
