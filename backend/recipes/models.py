from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, blank=False
    )
    measurement_unit = models.CharField(
        max_length=100, blank=False
    )

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return self.ingredient.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, blank=False)

    ingredients = models.ManyToManyField(AmountIngredient,
                                         related_name='recipes',
                                         blank=False)

    tags = models.ManyToManyField(Tag, related_name='recipes')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )

    image = models.ImageField(upload_to='images/%Y/%m/%d/',
                              null=True,
                              default=None
                              )

    text = models.TextField(default=None, null=True)

    cooking_time = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Fav(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favs_recipe')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='favs_users')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favs'
            )
        ]

    def __str__(self):
        return f'{self.user.username} likes {self.recipe.name[:10]}'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shopping_cart_recipes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='shopping_cart_users')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_shopping_list'
            )
        ]

    def __str__(self):
        return (f'{self.user.username} add '
                f'{self.recipe.name[:10]} to shopping list')


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower'
            )
        ]
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return (f'Подписка пользователя {self.user.username} на '
                f'автора {self.author.username}')
