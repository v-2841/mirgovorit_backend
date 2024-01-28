from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Название',
    )
    cooked = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Приготовлено раз',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Название',
    )
    products = models.ManyToManyField(
        Product,
        through='RecipeProduct',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    weight = models.PositiveSmallIntegerField(
        verbose_name='Вес, г',
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Продукт рецепта'
        verbose_name_plural = 'Продукты рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'product'],
                name='unique_recipe_product',
            ),
        ]

    def __str__(self):
        return f'{self.product.name} для {self.recipe.name} - {self.weight} г'
