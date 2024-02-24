from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin

from actions import models
from configurations.abstracts import AbstractModelAdmin


class UserFilter(AutocompleteFilter):
    title = 'User'
    field_name = 'user'


class PodcastFilter(AutocompleteFilter):
    title = 'Podcast'
    field_name = 'podcast'


@admin.register(models.Subscription)
class SubscriptionAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'user',
        'podcast',
        'is_notification_enabled',
    ]
    list_filter = [
        UserFilter,
        PodcastFilter,
        'is_notification_enabled',
    ]
    search_fields = [
        'id',
    ]
    autocomplete_fields = [
        'user',
        'podcast',
    ]


@admin.register(models.SearchQuery)
class SearchQueryAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'original_query',
        'latin_query',
        'cyrillic_query',
        'usages_count',
    ]
    list_filter = [
        'usages_count',
    ]
    search_fields = [
        'id',
        'original_query',
        'latin_query',
        'cyrillic_query'
    ]
