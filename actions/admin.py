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

    def lookup_allowed(self, lookup, value, request=None):
        if lookup in ['user__pk__exact', 'podcast__pk__exact']:
            return True
        return super().lookup_allowed(lookup, value, request)


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
