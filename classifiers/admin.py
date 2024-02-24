from django.contrib import admin

from classifiers import models
from configurations.abstracts import AbstractModelAdmin


@admin.register(models.Text)
class TextAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'sequence',
        'code',
        'name',
        'is_active',
    ]
    list_filter = [
        'is_active',
    ]
    search_fields = [
        'id',
        'code',
        'name',
    ]
    list_editable = [
        'sequence',
        'code',
        'name',
        'is_active',
    ]


@admin.register(models.Category)
class CategoryAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'sequence',
        'name',
        'is_active',
    ]
    list_filter = [
        'is_active',
    ]
    search_fields = [
        'id',
        'name',
    ]
    list_editable = [
        'sequence',
        'name',
        'is_active',
    ]


@admin.register(models.Constant)
class ConstantAdmin(AbstractModelAdmin):
    list_display = [
        'id',
        'key',
        'data',
    ]
    list_filter = [
        'key',
    ]
    search_fields = [
        'id',
        'data',
    ]
    list_editable = [
        'key',
        'data',
    ]
