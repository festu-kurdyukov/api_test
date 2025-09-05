import shortuuid
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import UserProfile

class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=60,
        verbose_name="Название",
        unique=True
    )
    measurement_unit = models.CharField(
        max_length=30,
        verbose_name="Единица измерения"
    )

    class Meta:
        verbose_name = "Игредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    name = models.CharField(
        max_length=MAX_LEN_RECIPE_NAME,
        verbose_name="Название"
    )
    text = models.TextField(verbose_name="Описание")
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                "Время приготовления должно быть больше 0."
            )
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    short_link = models.CharField(
        verbose_name="Короткая сылка",
        unique=True,
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        default_related_name = "recipes"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name="Рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент"
    )
    amount = models.PositiveIntegerField(
        verbose_name="Колличество",
        validators=[
            MinValueValidator(
                1,
                "Кол-во должно быть большу 0."
            )
        ]
    )

    class Meta:
        verbose_name = "Состав рецепта"
        unique_together = ("recipe", "ingredient")
        ordering = ("recipe",)

    def __str__(self):
        return f"{self.recipe} - {self.amount} {self.ingredient}"


class ShopingCart(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("user", "recipe")
        verbose_name = "Список покупок"

    def __str__(self):
        return f"Покупка {self.recipe}"


class Favorite(models.Model):
    user = models.ForeignKey(
        UserProfile,
        related_name="favorite",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт в избранном"
    )

    class Meta:
        unique_together = ("user", "recipe")
        verbose_name = "Избранный рецепт"

    def __str__(self):
        return f"Рецепт {self.recipe} в избранном у {self.user}"
