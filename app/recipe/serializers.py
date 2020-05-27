from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag Objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', )


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredeint objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id', )


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe Objects"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,      # Many to Many Field
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Recipe.objects.all()
    )
    
    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'price', 'link', 'ingredients',
            'tags', 'time_minutes',
        )
        read_only_fields = ('id', )

