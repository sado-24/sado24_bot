from django.db import models

from configurations.abstracts import AbstractModel
from configurations.constants import ERROR, STEP


class User(AbstractModel):
    telegram_id = models.CharField(
        max_length=31,
        unique=True,
    )
    full_name = models.CharField(
        max_length=255,
    )
    username = models.CharField(
        max_length=127,
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    text = models.ForeignKey(
        'classifiers.Text',
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True,
    )
    is_moderator = models.BooleanField(
        default=False,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    step = models.PositiveSmallIntegerField(
        default=STEP.MAIN,
        choices=STEP.CHOICES,
    )
    data = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.full_name


class Error(AbstractModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='errors',
        null=True,
        blank=True,
    )
    type = models.CharField(
        max_length=31,
        choices=ERROR.TYPE.CHOICES,
    )
    text = models.TextField()

    def __str__(self):
        return f"ID{self.id} {self.user} (type {self.type})"
