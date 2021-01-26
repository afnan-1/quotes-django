from rest_framework import serializers
from .models import Quote
from dataset.models import Question
from author.models import Author
from dataset.serializers import QuestionSerializer
import random

class AuthorSerializer(serializers.ModelSerializer):
    attribute = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    photo = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)
    class Meta:
        model = Author
        fields=('id','short_name','date_of_birth','date_of_death','attribute','alias','photo','sex')



class QuoteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    questions = serializers.SerializerMethodField('get_questions')
    class Meta:
        model = Quote
        fields=('id','author','difficulty','quote','questions')
    def get_questions(self,obj):
        questions = list(Question.objects.all())
        random_questions = random.sample(questions,5)
        q_serializer = QuestionSerializer(random_questions,many=True)
        return q_serializer.data