from rest_framework import serializers
from .models import Quote
from author.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    # attribute = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    class Meta:
        model = Author
        fields=('id','full_name',)
class QuoteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Quote
        fields='__all__'