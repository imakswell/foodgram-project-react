from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from recipes.models import Recipe, Tag

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name='favs_recipe',
        method='filter_it_is'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='shopping_cart_recipes',
        method='filter_it_is'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def filter_it_is(self, queryset, name, value):
        if not value:
            return queryset
        lookup = '__'.join([name, 'user'])
        return queryset.filter(**{lookup: self.request.user})
