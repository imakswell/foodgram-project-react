from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views.recipes_views import (FavoriteView, IngredientsViewSet,
                                  RecipeViewSet, ShoppingCardView, TagViewSet)

app_name = 'api'

router = SimpleRouter()

router.register(r"tags", TagViewSet, basename="tags")
router.register(r"ingredients", IngredientsViewSet, basename="ingredients")
router.register(r"recipes", RecipeViewSet, basename="recipes")

urlpatterns = [
    path("recipes/<int:id>/favorite/", FavoriteView.as_view(),
         name="favorite"),
    path(
        "recipes/download_shopping_cart/",
        ShoppingCardView.as_view(),
        name="download_shopping_cart",
    ),
    path(
        "recipes/<int:id>/shopping_cart/",
        ShoppingCardView.as_view(),
        name="shopping_cart",
    ),
    path("", include(router.urls)),
]
