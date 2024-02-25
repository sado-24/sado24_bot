from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from basics import models
from configurations.abstracts import AbstractModelAdmin


class TextFilter(AutocompleteFilter):
    title = 'Text'
    field_name = 'text'


class UserFilter(AutocompleteFilter):
    title = 'User'
    field_name = 'user'


@admin.register(models.User)
class UserAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'telegram_id',
        'full_name',
        'username',
        'birth_date',
        'text',
        'is_moderator',
        'is_admin',
        'is_active',
        'is_banned',
        'step',
    ]
    list_filter = [
        ('birth_date', DateRangeFilterBuilder()),
        TextFilter,
        'is_moderator',
        'is_admin',
        'is_active',
        'is_banned',
        'step',
    ]
    search_fields = [
        'id',
        'telegram_id',
        'full_name',
        'username',
    ]
    autocomplete_fields = [
        'text',
    ]
    filter_horizontal = [
        'interested_categories',
    ]

    def lookup_allowed(self, lookup, value, request=None):
        if lookup in ['text__pk__exact']:
            return True
        return super().lookup_allowed(lookup, value, request)


@admin.register(models.Error)
class ErrorAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'user',
        'type',
        'text',
    ]
    list_filter = [
        UserFilter,
        'type',
    ]
    search_fields = [
        'id',
        'text',
    ]
    autocomplete_fields = [
        'user',
    ]

    def lookup_allowed(self, lookup, value, request=None):
        if lookup in ['user__pk__exact']:
            return True
        return super().lookup_allowed(lookup, value, request)
