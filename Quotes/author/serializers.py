from rest_framework import serializers
from .models import Author
class AuthorSerializer(serializers.ModelSerializer):
    attribute = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Author
        fields='__all__'