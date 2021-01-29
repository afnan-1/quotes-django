from rest_framework import serializers
from .models import Author
class AuthorSerializer(serializers.ModelSerializer):
    attribute = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    photo = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)
    class Meta:
        model = Author
        fields='__all__'


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id','first_name','last_name')
