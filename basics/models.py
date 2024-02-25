from django.db import models

from configurations.abstracts import AbstractModel
from configurations.constants import ERROR, STEP, DELIMITER


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
    interested_categories = models.ManyToManyField(
        'classifiers.Category',
        related_name='interested_users',
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
    is_banned = models.BooleanField(
        default=False,
    )
    step = models.PositiveSmallIntegerField(
        default=STEP.MAIN,
        choices=STEP.CHOICES,
    )
    data = models.TextField(
        null=True,
        blank=True,
    )

    def set_step(self, step: str = STEP.MAIN, *args):
        self.step = step
        if args:
            self.data = DELIMITER.join([str(item) for item in args])
        else:
            self.data = None
        self.save()

    def check_step(self, step: int):
        return step == self.step

    def get_data_list(self):
        if self.data is not None:
            return self.data.split(DELIMITER)
        return []

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
        max_length=63,
        choices=ERROR.TYPE.CHOICES,
    )
    text = models.TextField()

    def __str__(self):
        return f"ID{self.id} {self.user} (type {self.type})"

    class Meta:
        ordering = ('-id', )
