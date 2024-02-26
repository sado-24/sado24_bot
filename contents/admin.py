from threading import Thread

from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin, messages

from bot.utils import helpers
from bot.views import bot
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

    def lookup_allowed(self, lookup, value, request=None):
        if lookup in ['channel__pk__exact']:
            return True
        return super().lookup_allowed(lookup, value, request)


@admin.register(models.Episode)
class EpisodeAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'podcast',
        'name',
        'description',
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
    readonly_fields = [
        'total_listens_count',
        'total_likes_count',
    ]
    exclude = [
        'liked_users',
    ]
    actions = [
        'notifying_all_subscribed_users_about_new_episode'
    ]

    def lookup_allowed(self, lookup, value, request=None):
        if lookup in ['podcast__pk__exact']:
            return True
        return super().lookup_allowed(lookup, value, request)

    @admin.action(description="Notifying all subscribed users about new episode.")
    def notifying_all_subscribed_users_about_new_episode(self, request, queryset):
        episode = queryset.first()
        thread = Thread(target=helpers.sending_new_episode_notification_to_subscribers, args=(bot, episode))
        thread.start()
        self.message_user(
            request,
            message=f"Notifying all users about new episode ID{episode.id} started.",
            level=messages.SUCCESS,
        )

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
