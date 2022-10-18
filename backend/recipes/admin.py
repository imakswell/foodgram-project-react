from django.contrib import admin

from .models import (Fav, Ingredient, AmountIngredient, Recipe, ShoppingCart,
                     Subscription, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    list_filter = ['name', 'author', 'tags']
    readonly_fields = ['count']

    def count(self, obj):
        return Fav.object.filter(recipe=obj).count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = ['name']


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Subscription)
admin.site.register(Tag)
admin.site.register(AmountIngredient)
admin.site.register(Fav)
admin.site.register(ShoppingCart)
