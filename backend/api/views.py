from collections import Counter
from io import StringIO

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import (Fav, Ingredient, Recipe, ShoppingCart,
                            Subscription, Tag)
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter
from .paginators import AddPageLimitPaginator
from .permissions import IsAuthorOrReadOnly
from .serializers import (FollowSerializer, IngredientSerializer,
                          GetRecipeSerializer, MyTagSerializer,
                          RecipesCreateSerializer, ShoppingCartFavsSerializer,
                          SubscriptionSerializer)

User = get_user_model()


class UsersListView(DjoserUserViewSet, mixins.CreateModelMixin):
    pagination_class = PageNumberPagination


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = MyTagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = AddPageLimitPaginator
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorOrReadOnly]
    filterset_fields = ['author']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GetRecipeSerializer
        return RecipesCreateSerializer


class CreateDestroyView:

    def create(self, instance, request, pk, model):
        item, created = model.objects.get_or_create(
            recipe=get_object_or_404(Recipe, id=pk),
            user=request.user)
        serializer = ShoppingCartFavsSerializer(item, data=request.data)
        serializer.is_valid(raise_exception=True)
        if not created:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def destroy(self, instance, request, pk, model):
        try:
            record = model.objects.filter(recipe__id=pk)
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except model.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartView(APIView, CreateDestroyView):

    def post(self, request, pk):
        return self.create(self, request, pk, ShoppingCart)

    def delete(self, request, pk):
        return self.destroy(self, request, pk, ShoppingCart)


class FavoriteView(APIView, CreateDestroyView):

    def post(self, request, pk):
        return self.create(self, request, pk, Fav)

    def delete(self, request, pk):
        return self.destroy(self, request, pk, Fav)


class DownloadShoppingCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        recipes = (shopping_card.recipe for shopping_card
                   in user.shopping_cart_users.all())
        ingredients = (r.ingredients.all() for r in recipes)
        flat_ingredients = (item for i in ingredients for item in i)
        data = ((f'{i.ingredient.name} ({i.ingredient.measurement_unit})',
                 i.amount) for i in flat_ingredients)
        ingredients_merged = Counter()
        for k, v in data:
            ingredients_merged[k] += v
        myfile = StringIO()
        if ingredients_merged:
            for k, v in ingredients_merged.items():
                myfile.write(f'\u2022  {k} \u2014 {v}\n')
        else:
            myfile.write('Ваш список пока покупок пуст')
        myfile.flush()
        myfile.seek(0)
        response = HttpResponse(myfile.getvalue(), content_type='text/plain')
        myfile.close()
        response['Content-Disposition'] = ('attachment; '
                                           'filename=shopping_card.txt')
        return response


class SubscriptionView(APIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        follow = User.objects.filter(
            following__user=request.user)

        page_size = request.GET.get('limit')
        if page_size:
            paginator = self.pagination_class()
            paginator.page_size = page_size
            paginate = paginator.paginate_queryset(queryset=follow,
                                                   request=request)
            serializer = FollowSerializer(paginate,
                                          context={'request': request},
                                          many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = FollowSerializer(follow,
                                          context={'request': request},
                                          many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        author = get_object_or_404(User, id=pk)
        data = {
            'user': request.user.id,
            'author': author.id,
        }
        serializer = SubscriptionSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        try:
            (get_object_or_404(Subscription, user=request.user, author_id=pk)
             .delete())
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
