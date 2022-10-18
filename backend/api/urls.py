from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCartView, FavoriteView, IngredientViewSet,
                    RecipeViewSet, ShoppingCartView, SubscriptionView,
                    TagViewSet, UsersListView)

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')


urlpatterns = [
    path('users/', UsersListView.as_view({'get': 'list', "post": "create"}),
         name='users_view'),
    path('users/subscriptions/',
         SubscriptionView.as_view(), name='get_subscribe'),
    path('users/<int:pk>/subscribe/',
         SubscriptionView.as_view(), name='subscribe'),
    path('recipes/<int:pk>/favorite/',
         FavoriteView.as_view(), name='add_to_favorite_list'),
    path('recipes/<int:pk>/shopping_cart/',
         ShoppingCartView.as_view(), name='add_to_shopping_cart'),
    path('recipes/download_shopping_cart/',
         DownloadShoppingCartView.as_view(), name='download_shopping_cart'),
    path('', include(router.urls)),
]
