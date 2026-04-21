from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField('Телефон', max_length=20, blank=True, null=True)
    address = models.TextField('Адрес доставки', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name() or self.username