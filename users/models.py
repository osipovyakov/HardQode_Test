from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

USER_ROLES = [
    ('Администратор', 'admin'),
    ('Владелец продукта', 'owner'),
    ('Пользователь', 'user'),
]


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name='Электронная почта'
    )
    username = None
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль'
    )
    role = models.CharField(
        max_length=100,
        choices=USER_ROLES
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    object = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
