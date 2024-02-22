from rangefilter.filters import DateTimeRangeFilterBuilder

from django.contrib import admin
from django.db import models


class AbstractModel(models.Model):
    added_time = models.DateTimeField(
        auto_now_add=True,
    )
    last_updated_time = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class AbstractModelAdmin(admin.ModelAdmin):
    date_hierarchy = 'added_time'
    search_fields = []

    def get_list_display(self, request):
        return [
            *self.list_display,
            'added_time',
            'last_updated_time',
        ]

    def get_list_filter(self, request):
        return (
            *self.list_filter,
            ('added_time', DateTimeRangeFilterBuilder()),
            ('last_updated_time', DateTimeRangeFilterBuilder()),
        )

    def get_search_fields(self, request):
        return [
            *self.search_fields,
        ]

    def get_readonly_fields(self, request, obj=None):
        return [
            *self.readonly_fields,
            'added_time',
            'last_updated_time',
        ]
