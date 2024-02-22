from django.db import models

from configurations.abstracts import AbstractModel


class Text(AbstractModel):
    sequence = models.IntegerField()
    code = models.CharField(
        max_length=3,
        unique=True,
        help_text='uz, ru, en and etc.'
    )
    name = models.CharField(
        max_length=31,
    )
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"[{self.code}] {self.name}"

    class Meta:
        ordering = ['sequence', ]


class Category(AbstractModel):
    sequence = models.IntegerField()
    name = models.CharField(
        max_length=31,
    )
    is_active = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sequence', ]
