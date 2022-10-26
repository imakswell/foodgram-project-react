from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name='E-mail address'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name='Unique username'
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='First name')
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Last name')
    password = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Password'
    )
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    def __str__(self):
        return f'{self.user} subscribed on {self.author}'

    class Meta:
        verbose_name = 'Subscribe'
        verbose_name_plural = 'Subscribes'
        db_table = 'db_follow'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='user_author'
            )
        ]
