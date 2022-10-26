from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Name')
    color = ColorField(
        default='#FF0000',
        unique=True,
        verbose_name='Colour code')
    slug = models.SlugField(
        unique=True,
        max_length=30,
        verbose_name='slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['-id']


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Name')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Measurement unit'
    )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_to_recipe'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Ingredients amount',
        validators=(
            MinValueValidator(1, 'Minimal ingredients amount is one'),
        ),
    )

    def __str__(self):
        return f' {self.ingredient} - {self.amount}'

    class Meta:
        verbose_name = 'Ingredient in recipe'
        verbose_name_plural = 'Ingredients in recipe'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'amount'],
                name='unique_ingredient_in_recipe'
            )
        ]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author',
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Name',
    )
    image = models.ImageField(
        verbose_name='Image',
        upload_to='static/images/',
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Description'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message='Minimal cooking time - one minute'
            )
        ],
        verbose_name='Cooking time (minutes)',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='recipes')
    ingredients = models.ManyToManyField(
        IngredientInRecipe,
        verbose_name='Ingredients',
        related_name='recipes'
    )

    def recipe_count(self):
        return self.favorite.count()

    def __str__(self):
        return f'{self.name} from {self.author}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        constraints = [
            models.UniqueConstraint(fields=['author', 'name'],
                                    name='unique_recipe')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Recipe'
    )

    class Meta:
        verbose_name = 'Favorite'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='Recipe',
    )

    class Meta:
        verbose_name = 'Shopping list'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'
