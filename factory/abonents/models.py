from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from limits.models import Limit


class CustomUsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\s\w.@+-]+\Z'


class PhoneValidator(CustomUsernameValidator):
    regex = r'^\d{4}$'


class Abonent(models.Model):
    """Model for abonents."""

    phone_validator = PhoneValidator()
    username_validator = CustomUsernameValidator()

    username = models.CharField(
        'ФИО',
        max_length=150,
        unique=True,
        help_text=(
            'Не более 150 символов. '
            'Только буквы, цифры и @/./+/-/_/ /.'
        ),
        validators=[username_validator],
    )
    phone = models.IntegerField(
        'Телефонный номер',
        unique=True,
        help_text='Должен только содержать 4 цифры.',
        validators=[phone_validator],
        error_messages={
            'unique': 'Пользователь с указанным номером уже существует.',
        },
    )
    limit = models.ForeignKey(
        Limit,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='abonents',
        verbose_name='Ограничения',
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)
        verbose_name = 'Абонент'
        verbose_name_plural = 'Абоненты'
