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
