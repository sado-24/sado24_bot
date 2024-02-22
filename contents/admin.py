from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin, messages

from configurations.abstracts import AbstractModelAdmin
from contents import models


class ChannelFilter(AutocompleteFilter):
    title = 'Channel'
    field_name = 'channel'


class ChannelOfPodcastFilter(AutocompleteFilter):
    title = 'Channel'
    rel_model = models.Podcast
    field_name = 'channel'
    parameter_name = 'podcast__channel'


class PodcastFilter(AutocompleteFilter):
    title = 'Podcast'
    field_name = 'podcast'


@admin.register(models.Channel)
class ChannelAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'name',
        'image',
        'is_active',
    ]
    list_filter = [
        'is_active',
    ]
    search_fields = [
        'id',
        'name',
    ]


@admin.register(models.Podcast)
class PodcastAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'channel',
        'name',
        'description',
        'image',
        'is_active',
    ]
    list_filter = [
        ChannelFilter,
        'categories',
        'is_active',
    ]
    search_fields = [
        'id',
        'name',
        'description',
    ]
    autocomplete_fields = [
        'channel',
    ]
    filter_horizontal = [
        'categories',
    ]


@admin.register(models.Episode)
class EpisodeAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'podcast',
        'name',
        'description',
        'timelapse',
        'url',
        'file_id',
        'duration',
        'total_listens_count',
        'total_likes_count',
        'is_active',
    ]
    list_filter = [
        ChannelOfPodcastFilter,
        PodcastFilter,
        'duration',
        'total_listens_count',
        'total_likes_count',
        'is_active',
    ]
    search_fields = [
        'id',
        'name',
        'description',
        'timelapse',
        'url',
        'file_id',
    ]
    autocomplete_fields = [
        'podcast',
    ]

    def save_model(self, request, obj: models.Episode, form, change):
        if obj.url or obj.file_id:
            obj.save()
        else:
            obj.is_active = False
            obj.save()
            self.message_user(
                request,
                "One of the url or file_id fields of the episode must be filled, please fill out one of the "
                "url or file_id fields and then set is_active to True.",
                messages.ERROR,
            )


@admin.register(models.Collection)
class CollectionAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'sequence',
        'image',
        'is_active',
    ]
    list_filter = [
        'is_active',
    ]
    search_fields = [
        'id',
        'name',
    ]
    filter_horizontal = [
        'podcasts',
    ]
    list_editable = [
        'sequence',
    ]
