from django.db import models
from django.db.models import Q

from configurations.abstracts import AbstractModel


class Channel(AbstractModel):
    name = models.TextField(
        max_length=127,
    )
    image = models.URLField(
        help_text="URL to the image",
    )
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id', )


class Podcast(AbstractModel):
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='podcasts',
    )
    name = models.TextField(
        max_length=255,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    image = models.URLField(
        help_text="URL to the image",
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
        ordering = ('-id', )


class Episode(AbstractModel):
    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name='episodes',
    )
    name = models.TextField(
        max_length=127,
    )
    description = models.TextField(
        null=True,
        blank=True,
        max_length=897,
    )
    timelapse = models.TextField(
        null=True,
        blank=True,
        max_length=1023,
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
    liked_users = models.ManyToManyField(
        'basics.User',
        related_name='liked_episodes',
        blank=True,
    )
    is_active = models.BooleanField(
        default=False,
    )

    @classmethod
    def filter_by_search_query(cls, search_query):
        return cls.objects.filter(
            Q(
                name__icontains=search_query.latin_query
            ) | Q(
                name__icontains=search_query.cyrillic_query
            ) | Q(
                podcast__name__icontains=search_query.latin_query
            ) | Q(
                podcast__name__icontains=search_query.cyrillic_query
            ) | Q(
                podcast__channel__name__icontains=search_query.latin_query
            ) | Q(
                podcast__channel__name__icontains=search_query.cyrillic_query
            ),
            is_active=True,
        )

    def __str__(self):
        return f"{self.name} [{self.podcast}]"

    class Meta:
        ordering = ('-total_listens_count', '-total_likes_count', '-id', )


class Collection(AbstractModel):
    sequence = models.PositiveIntegerField()
    name = models.CharField(
        max_length=127,
    )
    image = models.URLField(
        help_text="URL to the image",
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
