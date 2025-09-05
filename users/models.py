from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    """Модель пользователя."""
    first_name = models.CharField(
        max_length=32,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=32,
        verbose_name="Фамилия",
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name="Почта",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        default_related_name = "users"

    def __str__(self):
        return self.username
