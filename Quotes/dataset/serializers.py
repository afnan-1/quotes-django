from rest_framework import serializers
from author.models import Author
from .models import Dataset, Question


class AuthorSerializer(serializers.ModelSerializer):
    attribute = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    class Meta:
        model = Author
        fields=('full_name','date_of_birth','id','sex','attribute')

class DataSetSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)
    class Meta:
        model = Dataset
        fields=("id","type_dataset","dataset_name","morality","size","attributes","gender" ,"author")

class DataSetAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        exclude = ('author',)

class AuthorDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)
    class Meta:
        model = Dataset
        fields=('author',)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields='__all__'