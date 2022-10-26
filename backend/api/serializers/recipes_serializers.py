from api.field_image import Base64ImageField
from api.serializers.users_serializers import UserSerializer
from django.shortcuts import get_object_or_404
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit")

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, recipe):
        current_user = self.context["request"].user
        if (
            self.context["request"].user.is_authenticated
            and Favorite.objects.filter(recipe=recipe,
                                        user=current_user).exists()
        ):
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        current_user = self.context["request"].user
        if (
            self.context["request"].user.is_authenticated
            and ShoppingCart.objects.filter(recipe=recipe,
                                            user=current_user).exists()
        ):
            return True
        return False


class CustomIngredientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(required=True)
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "amount", 'name', 'measurement_unit')

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Check that the ingredients amount is more than one'
            )
        return value

    def get_measurement_unit(self, ingredient):
        measurement_unit = ingredient.ingredient.measurement_unit
        return measurement_unit

    def get_name(self, ingredient):
        name = ingredient.ingredient.name
        return name


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = CustomIngredientSerializer(many=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True, required=False)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, recipe):
        current_user = self.context["request"].user
        if Favorite.objects.filter(recipe=recipe, user=current_user).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        current_user = self.context["request"].user
        if ShoppingCart.objects.filter(recipe=recipe,
                                       user=current_user).exists():
            return True
        return False

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient.objects.filter(id=ingredient['id'])[:1]
            )
            ing, _ = IngredientInRecipe.objects.get_or_create(
                ingredient=current_ingredient,
                amount=ingredient["amount"],
            )
            recipe.ingredients.add(ing.id)

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, recipe, validated_data):
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            recipe.ingredients.clear()
            self.create_ingredients(ingredients, recipe)
        if "tags" in validated_data:
            tags_data = validated_data.pop("tags")
            recipe.tags.set(tags_data)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        serializer = RecipeSerializer(recipe, context=self.context)
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class ShoppingListSerializer(serializers.ModelSerializer):
    ingredient = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("ingredient",)

    def get_ingredient(self, recipe):
        ingredient = recipe.ingredients.all()
        return IngredientSerializer(ingredient, many=True).data
