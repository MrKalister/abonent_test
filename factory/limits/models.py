from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class GetOrNoneManager(models.Manager):
    """Return object or None"""

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class Limit(models.Model):
    objects = GetOrNoneManager()
    name = models.CharField('Название ', max_length=150)
    description = models.CharField(
        'Описание',
        max_length=150,
        null=True,
        blank=True
    )
    order_id = models.AutoField(
        'Порядок',
        primary_key=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order_id',)
        verbose_name = 'Ограничение'
        verbose_name_plural = 'Ограничения'
